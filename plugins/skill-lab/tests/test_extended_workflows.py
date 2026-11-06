"""Behavior tests use synthetic records only; no real experiment or market validation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/ecommerce-visual-strategy/scripts"
sys.path.insert(0, str(SCRIPTS))
import analyze_experiment as experiment
import audit_localization as localization
import batch_workflow as batch
import resolve_brand as brand
from workflow_common import dump, load_json


class BrandTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_json(ROOT / "examples/demo-brand.json")

    def test_merge_preserves_base_and_records_origins(self):
        before = copy.deepcopy(self.profile)
        result = brand.resolve(self.profile, "desk", {"style": {"palette_roles": {"accent": "red"}}})
        self.assertEqual(result["settings"]["style"]["palette_roles"]["accent"], "red")
        self.assertEqual(result["settings"]["style"]["palette_roles"]["body"], "charcoal")
        self.assertEqual(result["origins"]["style.palette_roles.accent"], "task")
        self.assertEqual(result["origins"]["style.palette_roles.body"], "brand:demo-1")
        self.assertEqual(self.profile, before)
        second = brand.resolve(self.profile, "desk")
        self.assertEqual(second["settings"]["style"]["palette_roles"]["accent"], "teal")

    def test_list_override_replaces_instead_of_appending(self):
        result = brand.resolve(self.profile, overrides={"glossary": []})
        self.assertEqual(result["settings"]["glossary"], [])
        self.assertEqual(result["origins"]["glossary"], "task")

    def test_unknown_series_product_facts_and_invalid_settings_rejected(self):
        for operation in (
            lambda: brand.resolve(self.profile, "missing"),
            lambda: brand.resolve(self.profile, overrides={"claims": ["load 100 kg"]}),
            lambda: brand.resolve(self.profile, overrides={"style": {"performance": "strong"}}),
            lambda: brand.resolve(self.profile, overrides={"assets": [{"path": "logo.png"}]}),
        ):
            with self.assertRaises(ValueError):
                operation()


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.source = load_json(ROOT / "examples/demo-delivery.json")
        self.target = load_json(ROOT / "examples/demo-delivery-de.json")
        self.packet = load_json(ROOT / "examples/demo-localization.json")

    def result(self):
        return localization.audit_localization(self.source, self.target, self.packet)

    def test_valid_draft_keeps_language_visual_and_audience_unknown(self):
        result = self.result()
        self.assertTrue(result["ok"], result)
        self.assertEqual(len(result["warnings"]), 3)

    def test_cross_sku_or_wrong_language_rejected(self):
        self.target["context"]["sku"] = "OTHER"
        self.assertFalse(self.result()["ok"])
        self.setUp()
        self.target["context"]["language"] = "en-US"
        self.assertFalse(self.result()["ok"])

    def test_evidence_change_and_added_claim_rejected(self):
        self.target["evidence"][0]["source"] = "Changed to another document"
        self.assertFalse(self.result()["ok"])
        self.setUp()
        self.target["claims"].append({"id": "C7", "text": "Unsupported new wording", "evidence_ids": ["E1"]})
        self.assertFalse(self.result()["ok"])

    def test_unit_conversion_exact_rounding_and_dimension_checks(self):
        row = {"claim_id": "C5", "source_value": "30", "source_unit": "cm", "target_value": "11.81", "target_unit": "in", "decimal_places": 2}
        self.packet["unit_conversions"] = [row]
        self.assertTrue(self.result()["ok"])
        row["target_value"] = "12"
        self.assertFalse(self.result()["ok"])
        row["target_unit"] = "kg"
        self.assertFalse(self.result()["ok"])

    def test_nonfinite_and_malformed_conversion_or_false_review_rejected(self):
        for value in ("NaN", "Infinity", "-1"):
            with self.assertRaises(ValueError):
                localization.check_conversion({"source_value": value, "source_unit": "cm", "target_value": "0", "target_unit": "in", "decimal_places": 2})
        self.packet["review"]["language"] = "reviewed"
        self.assertFalse(self.result()["ok"])
        self.packet["review"].update(language_by="synthetic reviewer", language_artifact="review-notes.md")
        self.assertTrue(self.result()["ok"])

    def test_omission_record_and_bad_shapes_rejected(self):
        self.packet["omitted_claim_ids"] = ["C5"]
        self.assertFalse(self.result()["ok"])
        for malformed in ([], {"schema_version": True}, {"schema_version": 1}):
            self.assertFalse(localization.audit_localization(self.source, self.target, malformed)["ok"])


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ("demo-delivery.json", "demo-delivery-de.json", "demo-brand.json", "demo-batch.json"):
            (self.root / name).write_text((ROOT / "examples" / name).read_text(encoding="utf-8"), encoding="utf-8")
        self.manifest = self.root / "demo-batch.json"
        self.output = self.root / "run"

    def run_batch(self, mode="prepare"):
        return batch.run(self.manifest, self.output, mode)

    def write_finished(self):
        for task in load_json(self.manifest)["tasks"]:
            (self.output / task["id"] / "delivery.json").write_text(dump(load_json(self.root / task["input"])), encoding="utf-8")

    def test_prepare_resume_preserves_finished_user_draft(self):
        self.assertTrue(self.run_batch()["ok"])
        self.write_finished()
        final = self.output / "rack-us/delivery.json"
        before = final.read_bytes()
        result = self.run_batch()
        self.assertTrue(result["ok"])
        self.assertEqual([r["status"] for r in result["results"]], ["preserved", "preserved"])
        self.assertEqual(final.read_bytes(), before)
        self.assertTrue(self.run_batch("audit")["ok"])

    def test_missing_draft_is_not_completion(self):
        self.run_batch()
        result = self.run_batch("audit")
        self.assertFalse(result["ok"])
        self.assertEqual(result["results"][0]["status"], "needs_draft")

    def test_one_bad_task_does_not_stop_another(self):
        self.run_batch()
        self.write_finished()
        path = self.output / "rack-us/delivery.json"
        bad = load_json(path)
        bad["context"]["language"] = "de-DE"
        path.write_text(dump(bad), encoding="utf-8")
        result = self.run_batch("audit")
        self.assertEqual([r["status"] for r in result["results"]], ["failed", "checked"])
        path.write_text('{"evidence": null, "context": {"sku": "DEMO-RACK-01", "market": "US", "language": "en-US", "category": "Desktop storage"}}', encoding="utf-8")
        self.assertEqual(self.run_batch("audit")["results"][0]["status"], "failed")

    def test_changed_input_or_snapshot_does_not_overwrite(self):
        self.run_batch()
        path = self.output / "rack-us/input-delivery.json"
        path.write_text("user edit", encoding="utf-8")
        self.assertFalse(self.run_batch()["ok"])
        self.assertEqual(path.read_text(encoding="utf-8"), "user edit")

    def test_interrupted_preparation_fails_without_deletion(self):
        (self.output / "rack-us").mkdir(parents=True)
        marker = self.output / "rack-us/marker.txt"
        marker.write_text("preserve", encoding="utf-8")
        result = self.run_batch()
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertEqual(result["results"][1]["status"], "prepared")
        self.assertTrue(marker.exists())

    def test_unsafe_duplicate_and_reserved_ids_fail_before_writes(self):
        original = load_json(self.manifest)
        for bad in ("../escape", "CON", "rack-us", "RACK-US"):
            data = copy.deepcopy(original)
            data["tasks"][1]["id"] = bad
            self.manifest.write_text(dump(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.run_batch()
            self.assertFalse(self.output.exists())

    def test_evidence_record_cannot_silently_change(self):
        self.run_batch()
        self.write_finished()
        path = self.output / "rack-us/delivery.json"
        changed = load_json(path)
        changed["evidence"][0]["source"] = "different source"
        path.write_text(dump(changed), encoding="utf-8")
        self.assertEqual(self.run_batch("audit")["results"][0]["status"], "failed")


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.plan = load_json(ROOT / "skills/ecommerce-visual-strategy/assets/experiment-plan.template.json")
        self.data = load_json(ROOT / "examples/demo-experiment-data.json")

    def valid_conditions(self):
        # Deliberately simulated conditions; these tests are not real experiment evidence.
        self.plan["design"]["registered_before_start"] = True
        self.data["data_kind"] = "observed"

    def test_no_data_and_synthetic_data_never_yield_winner(self):
        self.assertEqual(experiment.analyze(self.plan)["status"], "plan_only")
        result = experiment.analyze(self.plan, self.data)
        self.assertFalse(result["inference_allowed"])
        self.assertEqual(result["decision"], "descriptive_only")

    def test_supported_effect_and_metric_direction(self):
        self.valid_conditions()
        result = experiment.analyze(self.plan, self.data)
        self.assertTrue(result["inference_allowed"])
        self.assertAlmostEqual(result["difference_b_minus_a"], 0.05)
        self.assertEqual(result["decision"], "B_supported_for_primary_metric")
        self.plan["primary_metric"]["direction"] = "minimize"
        self.assertEqual(experiment.analyze(self.plan, self.data)["decision"], "A_supported_for_primary_metric")

    def test_equal_rates_and_practical_threshold_not_called_winner(self):
        self.valid_conditions()
        self.plan["minimum_absolute_effect"] = 0.1
        self.assertEqual(experiment.analyze(self.plan, self.data)["decision"], "inconclusive")
        self.data["arms"]["B"]["events"] = 100
        result = experiment.analyze(self.plan, self.data)
        self.assertLess(result["difference_95"][0], 0)
        self.assertGreater(result["difference_95"][1], 0)

    def test_known_wilson_interval_and_arm_swap_symmetry(self):
        lower, upper = experiment.wilson(50, 100)
        self.assertAlmostEqual(lower, 0.4038315304, places=9)
        self.assertAlmostEqual(upper, 0.5961684696, places=9)
        one = experiment.analyze(self.plan, self.data)
        self.data["arms"]["A"], self.data["arms"]["B"] = self.data["arms"]["B"], self.data["arms"]["A"]
        two = experiment.analyze(self.plan, self.data)
        self.assertAlmostEqual(one["difference_95"][0], -two["difference_95"][1])
        self.assertAlmostEqual(one["difference_95"][1], -two["difference_95"][0])

    def test_srm_observational_small_sample_and_quality_block_inference(self):
        self.valid_conditions()
        for kind in ("srm", "observational", "small", "quality", "unregistered"):
            plan, data = copy.deepcopy(self.plan), copy.deepcopy(self.data)
            if kind == "srm":
                data["arms"]["B"] = {"n": 1800, "events": 270}
            elif kind == "observational":
                plan["design"]["assignment"] = "observational"
            elif kind == "small":
                data["arms"]["A"] = {"n": 900, "events": 90}
                data["arms"]["B"] = {"n": 900, "events": 135}
            elif kind == "quality":
                data["checks"]["concurrent"] = False
            else:
                plan["design"]["registered_before_start"] = False
            self.assertFalse(experiment.analyze(plan, data)["inference_allowed"], kind)

    def test_zero_baseline_and_sparse_counts_are_descriptive(self):
        self.valid_conditions()
        self.data["arms"]["A"]["events"] = 0
        result = experiment.analyze(self.plan, self.data)
        self.assertIsNone(result["relative_lift_b_vs_a"])
        self.assertFalse(result["inference_allowed"])

    def test_invalid_counts_metric_dates_and_allocation_rejected(self):
        for kind in ("events", "metric", "dates", "allocation", "sku", "bad_shape"):
            plan, data = copy.deepcopy(self.plan), copy.deepcopy(self.data)
            if kind == "events":
                data["arms"]["A"]["events"] = 1001
            elif kind == "metric":
                data["unit"] = "sessions"
            elif kind == "dates":
                data["window"]["end"] = "2020-01-01"
            elif kind == "allocation":
                plan["design"]["allocation_b"] = 0.8
            elif kind == "sku":
                data["sku"] = "another-sku"
            else:
                data["arms"] = []
            with self.assertRaises(ValueError, msg=kind):
                experiment.analyze(plan, data)

    def test_cli_rejects_nonfinite_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            path.write_text('{"schema_version":1,"minimum_absolute_effect":NaN}', encoding="utf-8")
            result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "analyze_experiment.py"), str(path)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("non-finite", result.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
