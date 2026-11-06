"""Check source/target fact references and recorded unit conversions, not translation quality."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import sys
from audit_delivery import audit
from workflow_common import dump, load_json, nonempty, obj, version

# Exact conversion definitions; factors use metres, kilograms and litres.
UNITS = {"mm": ("length", "0.001"), "cm": ("length", "0.01"), "m": ("length", "1"),
         "in": ("length", "0.0254"), "ft": ("length", "0.3048"),
         "g": ("mass", "0.001"), "kg": ("mass", "1"), "oz": ("mass", "0.028349523125"),
         "lb": ("mass", "0.45359237"), "ml": ("volume", "0.001"), "L": ("volume", "1"),
         "fl_oz_us": ("volume", "0.0295735295625")}


def check_conversion(row):
    obj(row, "conversion")
    source_unit = row.get("source_unit")
    target_unit = row.get("target_unit")
    if not isinstance(source_unit, str) or not isinstance(target_unit, str) or source_unit not in UNITS or target_unit not in UNITS:
        raise ValueError("unsupported unit; distinguish oz mass from fl_oz_us volume")
    if UNITS[source_unit][0] != UNITS[target_unit][0]:
        raise ValueError("conversion dimensions do not match")
    places = row.get("decimal_places")
    if type(places) is not int or not 0 <= places <= 6:
        raise ValueError("decimal_places must be integer 0..6")
    for key in ("source_value", "target_value"):
        if not isinstance(row.get(key), str):
            raise ValueError("conversion values must be decimal strings")
    try:
        source = Decimal(row["source_value"])
        target = Decimal(row["target_value"])
        if not source.is_finite() or not target.is_finite() or source < 0 or target < 0:
            raise ValueError("conversion values must be finite and nonnegative")
        expected = source * Decimal(UNITS[source_unit][1]) / Decimal(UNITS[target_unit][1])
        rounded = expected.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError("invalid or excessively large decimal conversion") from exc
    if target != rounded:
        raise ValueError("conversion mismatch: expected " + str(rounded) + " " + target_unit)


def audit_localization(source, target, packet):
    errors, warnings = [], []
    try:
        version(packet)
        for name, data in (("source", source), ("target", target)):
            result = audit(data)
            if not result["ok"]:
                raise ValueError(name + " draft fails mechanical checks: " + dump(result["errors"]))
        sku = source["context"]["sku"]
        if packet.get("sku") != sku or target["context"]["sku"] != sku:
            raise ValueError("source/target/packet SKU mismatch")
        for label, data in (("source_context", source), ("target_context", target)):
            context = obj(packet.get(label), label)
            for key in ("market", "language"):
                nonempty(context.get(key), label + "." + key)
                if data["context"].get(key) != context[key]:
                    raise ValueError(label + " does not match delivery " + key)
        facts = {item["id"]: item for item in source["claims"]}
        evidence = {item["id"]: item for item in source["evidence"]}
        retained = set()
        for fact in target["claims"]:
            cid = fact["id"]
            if cid not in facts or set(fact["evidence_ids"]) != set(facts[cid]["evidence_ids"]):
                raise ValueError("target claim added or evidence changed: " + cid)
            retained.add(cid)
        for item in target["evidence"]:
            if item["id"] not in evidence or item != evidence[item["id"]]:
                raise ValueError("target evidence differs from source; reconcile source first")
        omitted = packet.get("omitted_claim_ids", [])
        if not isinstance(omitted, list) or any(not isinstance(cid, str) for cid in omitted) or len(set(omitted)) != len(omitted):
            raise ValueError("omitted_claim_ids must be unique strings")
        if set(omitted) != set(facts) - retained:
            raise ValueError("omitted claims must be recorded exactly")
        conversions = packet.get("unit_conversions", [])
        if not isinstance(conversions, list):
            raise ValueError("unit_conversions must be an array")
        for row in conversions:
            obj(row, "conversion")
            if row.get("claim_id") not in retained:
                raise ValueError("conversion must refer to a retained claim")
            check_conversion(row)
        audience = packet.get("audience", [])
        if not isinstance(audience, list):
            raise ValueError("audience must be an array")
        for row in audience:
            obj(row, "audience item")
            nonempty(row.get("finding"), "audience.finding")
            if row.get("basis") not in ("evidence", "hypothesis"):
                raise ValueError("audience basis must be evidence or hypothesis")
            if row["basis"] == "evidence":
                nonempty(row.get("source"), "audience.source")
            else:
                warnings.append("Audience assumption needs validation: " + row["finding"])
        terms = packet.get("terminology", [])
        if not isinstance(terms, list):
            raise ValueError("terminology must be an array")
        for row in terms:
            obj(row, "term")
            nonempty(row.get("source"), "term.source")
            nonempty(row.get("target"), "term.target")
            if row.get("status") not in ("approved", "proposed"):
                raise ValueError("terminology status must be approved or proposed")
        review = obj(packet.get("review"), "review")
        for key in ("language", "visual"):
            state = review.get(key)
            if state not in ("not_reviewed", "reviewed"):
                raise ValueError("review statuses must be not_reviewed or reviewed")
            if state == "reviewed":
                nonempty(review.get(key + "_by"), "review." + key + "_by")
                nonempty(review.get(key + "_artifact"), "review." + key + "_artifact")
            else:
                warnings.append(key + " review is outstanding")
    except (ValueError, TypeError) as exc:
        errors.append(str(exc))
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "scope": "reference and recorded conversion checks only; no semantic translation or audience verification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("packet")
    args = parser.parse_args()
    try:
        result = audit_localization(load_json(args.source), load_json(args.target), load_json(args.packet))
    except (OSError, UnicodeError, ValueError) as exc:
        print(dump({"ok": False, "input_error": str(exc)}))
        return 2
    print(dump(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
