"""Plan or describe a two-arm binary experiment. Aggregate records are not verified raw data."""
import argparse
from datetime import date
import math
import sys
from workflow_common import dump, load_json, nonempty, obj, version

Z95 = 1.959963984540054


def number(value, name, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(name + " is outside its allowed finite range")
    return value


def positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(name + " must be a positive integer")
    return value


def check_plan(plan):
    version(plan)
    for key in ("experiment_id", "sku", "market", "hypothesis", "variable", "sample_size_basis"):
        nonempty(plan.get(key), key)
    metric = obj(plan.get("primary_metric"), "primary_metric")
    for key in ("name", "event", "denominator"):
        nonempty(metric.get(key), "primary_metric." + key)
    if metric.get("direction") not in ("maximize", "minimize"):
        raise ValueError("metric direction must be maximize or minimize")
    if metric.get("unit") != "unique_user_binary":
        raise ValueError("only a binary outcome per independently assigned unique user is supported")
    variants = obj(plan.get("variants"), "variants")
    if set(variants) != {"A", "B"}:
        raise ValueError("exactly two variants A and B are supported")
    for value in variants.values():
        nonempty(value, "variant description")
    if variants["A"] == variants["B"]:
        raise ValueError("variants must differ")
    design = obj(plan.get("design"), "design")
    if design.get("assignment") not in ("randomized_concurrent", "observational"):
        raise ValueError("assignment must be randomized_concurrent or observational")
    if design.get("stopping_rule") != "fixed_sample":
        raise ValueError("sequential/adaptive analysis is not implemented")
    if type(design.get("registered_before_start")) is not bool:
        raise ValueError("registered_before_start must be boolean")
    number(design.get("allocation_b"), "allocation_b", 0.01, 0.99)
    positive_int(design.get("planned_n_a"), "planned_n_a")
    positive_int(design.get("planned_n_b"), "planned_n_b")
    planned_total = design["planned_n_a"] + design["planned_n_b"]
    if abs(design["planned_n_b"] / planned_total - design["allocation_b"]) > 1 / planned_total:
        raise ValueError("planned arm sizes conflict with allocation_b")
    number(plan.get("minimum_absolute_effect"), "minimum_absolute_effect", 0, 1)


def wilson(events, n):
    p = events / n
    z2 = Z95 ** 2
    denominator = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denominator
    half = Z95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / denominator
    return [max(0.0, center - half), min(1.0, center + half)]


def analyze(plan, data=None):
    check_plan(plan)
    if data is None:
        return {"ok": True, "status": "plan_only", "experiment_id": plan["experiment_id"],
                "warnings": ["Sample size is supplied by the operator, not a computed power recommendation.",
                             "Verify platform experiment eligibility and record the plan before data collection."],
                "inference_allowed": False, "decision": "no_data"}
    version(data)
    for key in ("experiment_id", "sku", "market"):
        if data.get(key) != plan[key]:
            raise ValueError("data/plan mismatch: " + key)
    nonempty(data.get("source"), "data.source")
    if data.get("data_kind") not in ("synthetic", "observed"):
        raise ValueError("data_kind must be synthetic or observed")
    if data.get("metric") != plan["primary_metric"]["name"] or data.get("unit") != "unique_user_binary":
        raise ValueError("data metric or denominator unit mismatch")
    window = obj(data.get("window"), "window")
    start, end = date.fromisoformat(nonempty(window.get("start"), "window.start")), date.fromisoformat(nonempty(window.get("end"), "window.end"))
    if end < start:
        raise ValueError("window ends before it starts")
    arms = obj(data.get("arms"), "arms")
    if set(arms) != {"A", "B"}:
        raise ValueError("data requires exactly A and B")
    rates, intervals = {}, {}
    reasons = []
    for name, arm in arms.items():
        obj(arm, name)
        n = positive_int(arm.get("n"), name + ".n")
        events = arm.get("events")
        if type(events) is not int or not 0 <= events <= n:
            raise ValueError(name + ".events must be an integer between 0 and n")
        rates[name] = events / n
        intervals[name] = wilson(events, n)
        if min(events, n - events) < 10:
            reasons.append(name + ": sparse outcomes; this approximation is descriptive only")
    a, b = rates["A"], rates["B"]
    difference = b - a
    # Newcombe method 10: independent Wilson score intervals, no continuity correction.
    lower = max(-1.0, difference - math.hypot(b - intervals["B"][0], intervals["A"][1] - a))
    upper = min(1.0, difference + math.hypot(intervals["B"][1] - b, a - intervals["A"][0]))
    total = arms["A"]["n"] + arms["B"]["n"]
    allocation = plan["design"]["allocation_b"]
    expected_b = total * allocation
    expected_a = total - expected_b
    chi2 = (arms["B"]["n"] - expected_b) ** 2 / expected_b + (arms["A"]["n"] - expected_a) ** 2 / expected_a
    srm_p = math.erfc(math.sqrt(chi2 / 2))  # chi-square, 1 degree of freedom
    if min(expected_a, expected_b) < 5 or srm_p < 0.001:
        reasons.append("sample-ratio mismatch or insufficient expected allocation counts")
    design = plan["design"]
    if design["assignment"] != "randomized_concurrent":
        reasons.append("observational/before-after comparison cannot establish a causal winner")
    if not design["registered_before_start"]:
        reasons.append("plan was not declared as registered before data collection")
    for arm, key in (("A", "planned_n_a"), ("B", "planned_n_b")):
        if arms[arm]["n"] < design[key]:
            reasons.append("planned sample not reached: " + arm)
    checks = obj(data.get("checks"), "checks")
    for key in ("deduplicated", "concurrent", "instrumentation_stable", "no_known_confounders", "fixed_horizon_reached"):
        if type(checks.get(key)) is not bool:
            raise ValueError("checks." + key + " must be boolean")
        if not checks[key]:
            reasons.append("data quality condition not met: " + key)
    if data["data_kind"] == "synthetic":
        reasons.append("synthetic data: illustration only")
    decision = "descriptive_only" if reasons else "inconclusive"
    threshold = plan["minimum_absolute_effect"]
    signed_low, signed_high = (lower, upper) if plan["primary_metric"]["direction"] == "maximize" else (-upper, -lower)
    if not reasons:
        if signed_low > threshold:
            decision = "B_supported_for_primary_metric"
        elif signed_high < -threshold:
            decision = "A_supported_for_primary_metric"
    return {"ok": True, "status": "analysis", "experiment_id": plan["experiment_id"],
            "rates": rates, "arm_wilson_95": intervals, "difference_b_minus_a": difference,
            "difference_95": [lower, upper], "relative_lift_b_vs_a": difference / a if a else None,
            "sample_ratio_p": srm_p, "inference_allowed": not reasons, "decision": decision,
            "blockers": reasons, "method": "Wilson + Newcombe method 10, two-sided 95%; SRM chi-square 1df at 0.001",
            "limitations": ["Aggregate data and asserted experiment conditions are not independently verified.",
                            "One prespecified binary primary metric; no sequential or multiple-comparison correction.",
                            "A supported primary metric does not establish profitability or other guardrails."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan")
    parser.add_argument("--data")
    args = parser.parse_args()
    try:
        result = analyze(load_json(args.plan), load_json(args.data) if args.data else None)
    except (OSError, UnicodeError, ValueError, OverflowError) as exc:
        print(dump({"ok": False, "input_error": str(exc)}))
        return 2
    print(dump(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
