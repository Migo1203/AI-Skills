#!/usr/bin/env python3
"""Check a v1 draft delivery. No network, generation, publishing or legal verdict."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

PLACEHOLDER = re.compile(r"待(?:确认|补证|核验)|\b(?:TODO|TBD|FIXME)\b|同上|same as above", re.I)
KINDS = {"main", "secondary", "a_plus", "mobile_a_plus", "concept"}
LAYOUTS = {f"{n:02d}" for n in range(1, 17)}


class Audit:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.metrics = {"title_chars": None, "bullet_chars": [], "images": 0}

    def error(self, path, message):
        self.errors.append({"path": path, "message": message})

    def warn(self, path, message):
        self.warnings.append({"path": path, "message": message})

    def obj(self, value, path):
        if not isinstance(value, dict):
            self.error(path, "expected object")
            return {}
        return value

    def array(self, value, path):
        if not isinstance(value, list):
            self.error(path, "expected array")
            return []
        return value

    def text(self, value, path, visible=False):
        if not isinstance(value, str) or not value.strip():
            self.error(path, "expected nonempty string")
            return ""
        if visible and PLACEHOLDER.search(value):
            self.error(path, "placeholder or context-dependent text in final copy")
        return value

    def records(self, value, path):
        indexed = {}
        for i, raw in enumerate(self.array(value, path)):
            item = self.obj(raw, f"{path}[{i}]")
            key = self.text(item.get("id"), f"{path}[{i}].id")
            if key in indexed:
                self.error(f"{path}[{i}].id", "duplicate ID")
            if key:
                indexed[key] = item
        return indexed

    def refs(self, value, known, path, required=True):
        refs = self.array(value, path)
        if required and not refs:
            self.error(path, "at least one reference required")
        valid = []
        for i, ref in enumerate(refs):
            if not isinstance(ref, str) or ref not in known:
                self.error(f"{path}[{i}]", "unknown reference")
            elif ref in valid:
                self.error(f"{path}[{i}]", "duplicate reference")
            else:
                valid.append(ref)
        return valid

    def positive(self, value, path):
        if type(value) is not int or value <= 0:
            self.error(path, "expected positive integer")
            return None
        return value

    def size(self, value, path):
        item = self.obj(value, path)
        width = self.positive(item.get("width"), path + ".width")
        height = self.positive(item.get("height"), path + ".height")
        return (width, height) if width and height else None


def audit(data):
    a = Audit()
    data = a.obj(data, "$")
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        a.error("schema_version", "supported version is integer 1")
    if data.get("status") != "draft":
        a.error("status", "this checker supports drafts only, not publish approval")
    context = a.obj(data.get("context"), "context")
    for key in ("sku", "market", "category"):
        a.text(context.get(key), "context." + key)
    evidence = a.records(data.get("evidence"), "evidence")
    allowed = set()
    for key, item in evidence.items():
        path = "evidence." + key
        a.text(item.get("source"), path + ".source")
        a.text(item.get("sku"), path + ".sku")
        kind = item.get("kind")
        if kind not in ("document", "supplier", "visual", "hypothesis"):
            a.error(path + ".kind", "unknown evidence kind")
        if type(item.get("verified")) is not bool:
            a.error(path + ".verified", "expected boolean")
        if (item.get("sku") == context.get("sku") and item.get("verified") is True
                and (kind == "document" or
                     (kind == "supplier" and item.get("cross_checked") is True))):
            allowed.add(key)
    claims = a.records(data.get("claims"), "claims")
    for key, item in claims.items():
        path = "claims." + key
        a.text(item.get("text"), path + ".text", visible=True)
        refs = a.refs(item.get("evidence_ids"), evidence, path + ".evidence_ids")
        if refs and not any(ref in allowed for ref in refs):
            a.error(path, "no verified product evidence for this SKU")

    rules = a.obj(data.get("rules", {}), "rules")
    limits = a.obj(rules.get("limits", {}), "rules.limits")
    modules = a.obj(rules.get("modules", {}), "rules.modules")
    checked_limits = {}
    for key, value in limits.items():
        if key not in ("title_max_chars", "bullet_max_chars", "bullet_max_count"):
            a.error("rules.limits." + key, "unknown limit")
        else:
            checked_limits[key] = a.positive(value, "rules.limits." + key)
    if limits or modules:
        a.text(rules.get("source"), "rules.source")
        try:
            date.fromisoformat(rules.get("verified_on", ""))
        except (ValueError, TypeError):
            a.error("rules.verified_on", "expected ISO date YYYY-MM-DD")
    else:
        a.warn("rules", "current platform limits and modules not verified")
    checked_modules = {key: a.size(value, "rules.modules." + key)
                       for key, value in modules.items()}

    copy_texts = []

    def copy_item(raw, path, limit=None):
        item = a.obj(raw, path)
        text = a.text(item.get("text"), path + ".text", visible=True)
        if text:
            copy_texts.append(text)
        a.refs(item.get("claim_ids"), claims, path + ".claim_ids")
        if limit and len(text) > limit:
            a.error(path + ".text", "exceeds supplied character limit")
        return text

    if "listing" in data:
        listing = a.obj(data["listing"], "listing")
        if not any(key in listing for key in ("title", "bullets", "attributes")):
            a.error("listing", "no supported copy fields")
        if "title" in listing:
            title = copy_item(listing["title"], "listing.title", checked_limits.get("title_max_chars"))
            a.metrics["title_chars"] = len(title)
        if "bullets" in listing:
            bullets = a.array(listing["bullets"], "listing.bullets")
            maximum = checked_limits.get("bullet_max_count")
            if maximum and len(bullets) > maximum:
                a.error("listing.bullets", "exceeds supplied bullet count")
            for i, item in enumerate(bullets):
                text = copy_item(item, f"listing.bullets[{i}]", checked_limits.get("bullet_max_chars"))
                a.metrics["bullet_chars"].append(len(text))
        if "attributes" in listing:
            for i, item in enumerate(a.array(listing["attributes"], "listing.attributes")):
                path = f"listing.attributes[{i}]"
                copy_item(item, path)
                a.text(a.obj(item, path).get("name"), path + ".name")
        if not copy_texts:
            a.error("listing", "no nonempty copy was supplied")

    images = a.records(data.get("images", []), "images")
    a.metrics["images"] = len(images)
    for key, image in images.items():
        path = "images." + key
        kind = image.get("kind")
        if not isinstance(kind, str) or kind not in KINDS:
            a.error(path + ".kind", "unknown image kind")
        a.text(image.get("task"), path + ".task")
        layout = image.get("layout_id")
        if not isinstance(layout, str) or (layout not in LAYOUTS and not (kind == "main" and layout == "product_only")):
            a.error(path + ".layout_id", "unknown layout ID")
        a.refs(image.get("claim_ids", []), claims, path + ".claim_ids", required=False)
        text = image.get("text", "")
        if not isinstance(text, str):
            a.error(path + ".text", "expected string")
        elif text:
            a.text(text, path + ".text", visible=True)
            a.refs(image.get("claim_ids", []), claims, path + ".claim_ids")
        if kind == "main" and (text or layout != "product_only"):
            a.error(path, "internal conservative main-image mode requires product_only without added text")
        actual_size = a.size(image["dimensions"], path + ".dimensions") if "dimensions" in image else None
        if kind in ("a_plus", "mobile_a_plus"):
            module = image.get("module_id")
            if not isinstance(module, str) or module not in checked_modules:
                a.warn(path + ".module_id", "actual A+ slot not verified")
            elif actual_size and checked_modules[module] and actual_size != checked_modules[module]:
                a.error(path + ".dimensions", "does not match supplied module dimensions")
            if actual_size is None:
                a.warn(path + ".dimensions", "A+ size pending verification")
        if "prompt" in image:
            prompt = a.obj(image["prompt"], path + ".prompt")
            a.text(prompt.get("text"), path + ".prompt.text", visible=True)
            constraints = a.array(prompt.get("constraints"), path + ".prompt.constraints")
            if not constraints:
                a.error(path + ".prompt.constraints", "explicit constraints required")
            for i, constraint in enumerate(constraints):
                a.text(constraint, f"{path}.prompt.constraints[{i}]")
            refs = a.refs(prompt.get("reference_ids", []), evidence,
                          path + ".prompt.reference_ids", required=False)
            if prompt.get("mode") == "background":
                if prompt.get("no_product") is not True:
                    a.error(path + ".prompt.no_product", "background must explicitly exclude products")
            elif prompt.get("mode") == "product_concept":
                if not any(evidence[ref].get("kind") == "visual" and
                           evidence[ref].get("sku") == context.get("sku") for ref in refs):
                    a.error(path + ".prompt.reference_ids", "matching SKU visual reference required")
            else:
                a.error(path + ".prompt.mode", "unknown prompt mode")
    if "listing" not in data and not images:
        a.error("$", "delivery has no copy or image plan")
    return {"ok": not a.errors, "scope": "mechanical draft checks only; not publication approval",
            "errors": a.errors, "warnings": a.warnings, "metrics": a.metrics}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.file.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "input_error": str(exc)}, ensure_ascii=False))
        return 2
    result = audit(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
