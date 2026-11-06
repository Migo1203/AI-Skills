import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/ecommerce-visual-strategy/scripts/audit_delivery.py"
spec = importlib.util.spec_from_file_location("audit_delivery", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/demo-delivery.json").read_text(encoding="utf-8"))

    def errors(self, data=None):
        return module.audit(self.data if data is None else data)["errors"]

    def test_valid_draft_keeps_policy_unknown(self):
        result = module.audit(self.data)
        self.assertTrue(result["ok"])
        self.assertTrue(any(w["path"] == "rules" for w in result["warnings"]))
        self.assertEqual(result["metrics"]["images"], 4)

    def test_photo_cannot_prove_material_or_rating(self):
        self.data["claims"][1]["evidence_ids"] = ["V1"]
        self.assertTrue(self.errors())

    def test_unverified_document_and_wrong_sku(self):
        self.data["evidence"][0]["verified"] = False
        self.assertTrue(self.errors())
        self.data["evidence"][0]["verified"] = True
        self.data["evidence"][0]["sku"] = "OTHER-SKU"
        self.assertTrue(self.errors())

    def test_supplier_requires_cross_check(self):
        self.data["evidence"][0]["kind"] = "supplier"
        self.assertTrue(self.errors())
        self.data["evidence"][0]["cross_checked"] = True
        self.assertFalse(self.errors())

    def test_broken_and_duplicate_references(self):
        self.data["listing"]["title"]["claim_ids"] = ["MISSING"]
        self.assertTrue(self.errors())
        self.data["listing"]["title"]["claim_ids"] = ["C1", "C1"]
        self.assertTrue(self.errors())

    def test_duplicate_ids(self):
        self.data["evidence"].append(copy.deepcopy(self.data["evidence"][0]))
        self.assertTrue(self.errors())

    def test_main_cannot_use_promotional_layout(self):
        self.data["images"][0]["layout_id"] = "08"
        self.data["images"][0]["text"] = "Best Rack"
        self.assertTrue(self.errors())

    def test_limits_are_supplied_not_assumed(self):
        self.data["rules"] = {"source": "Synthetic limit for testing, not an Amazon rule",
                              "verified_on": "2026-11-06", "limits": {"title_max_chars": 5}}
        self.assertTrue(self.errors())

    def test_module_dimension_mismatch(self):
        self.data["rules"] = {"source": "Synthetic slot for testing", "verified_on": "2026-11-06",
                              "modules": {"slot1": {"width": 1000, "height": 500}}}
        self.data["images"][2].update(module_id="slot1", dimensions={"width": 1000, "height": 600})
        self.assertTrue(self.errors())
        self.data["images"][2]["dimensions"]["height"] = 500
        self.assertFalse(self.errors())

    def test_unknown_layout_and_context_dependent_prompt(self):
        self.data["images"][1]["layout_id"] = "17"
        self.data["images"][1]["prompt"]["text"] = "同上"
        self.assertTrue(self.errors())

    def test_background_and_product_reference_boundaries(self):
        prompt = self.data["images"][1]["prompt"]
        prompt["no_product"] = False
        self.assertTrue(self.errors())
        prompt["mode"] = "product_concept"
        self.assertTrue(self.errors())
        prompt["reference_ids"] = ["V1"]
        self.assertFalse(self.errors())

    def test_bad_shapes_produce_errors_instead_of_crashing(self):
        for mutation in ([], {"schema_version": True}, {"schema_version": 1, "evidence": 3}):
            self.assertTrue(self.errors(mutation))
        self.data["images"][0]["kind"] = []
        self.data["images"][0]["layout_id"] = {}
        self.assertTrue(self.errors())

    def test_empty_delivery_and_fake_publish_status(self):
        empty_listing = copy.deepcopy(self.data)
        empty_listing["listing"] = {"bullets": [], "attributes": []}
        self.assertTrue(self.errors(empty_listing))
        self.data.pop("listing")
        self.data["images"] = []
        self.assertTrue(self.errors())
        self.data["status"] = "ready_to_publish"
        self.assertTrue(self.errors())

    def test_cli_input_failure_has_exit_code_two(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "invalid.json"
            path.write_text('{"status": "draft", "status": "published"}', encoding="utf-8")
            result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(path)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate JSON key", result.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
