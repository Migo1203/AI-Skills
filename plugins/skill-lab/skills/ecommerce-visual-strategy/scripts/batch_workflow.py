"""Prepare isolated drafting tasks or audit finished drafts; never call paid APIs."""
import argparse
import hashlib
from pathlib import Path
import re
import sys
from audit_delivery import audit
from resolve_brand import resolve
from workflow_common import dump, load_json, nonempty, obj, version, write_new

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"{p}{n}" for p in ("COM", "LPT") for n in range(1, 10)}


def manifest_tasks(data):
    version(data)
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("tasks must be a nonempty array")
    ids, contexts = set(), set()
    for task in tasks:
        obj(task, "task")
        tid = nonempty(task.get("id"), "task.id")
        if not ID.fullmatch(tid) or tid.upper() in RESERVED or tid.casefold() in ids:
            raise ValueError("unsafe or duplicate task ID: " + tid)
        ids.add(tid.casefold())
        context = obj(task.get("context"), "task.context")
        if set(context) - {"sku", "market", "language", "category", "brand_id"}:
            raise ValueError("unsupported context field")
        for key in ("sku", "market", "language", "category"):
            nonempty(context.get(key), "context." + key)
        key = tuple(context[k].casefold() for k in ("sku", "market", "language"))
        if key in contexts:
            raise ValueError("duplicate SKU/market/language task")
        contexts.add(key)
        nonempty(task.get("input"), "task.input")
        if set(task) - {"id", "context", "input", "brand", "series", "brand_overrides"}:
            raise ValueError("unsupported task field")
        if ("series" in task or "brand_overrides" in task) and "brand" not in task:
            raise ValueError("series/brand_overrides require a brand profile")
    return tasks


def bundle(task, base):
    source_path = (base / task["input"]).resolve()
    source = load_json(source_path)
    checked = audit(source)
    if not checked["ok"]:
        raise ValueError("input draft fails mechanical checks: " + dump(checked["errors"]))
    for key in ("sku", "market", "category"):
        if source["context"][key] != task["context"][key]:
            raise ValueError("input context mismatch: " + key)
    if "language" in source["context"] and source["context"]["language"] != task["context"]["language"]:
        raise ValueError("input context mismatch: language")
    files = {"input-delivery.json": dump(source)}
    if "brand" in task:
        profile = load_json(base / nonempty(task["brand"], "brand"))
        resolved = resolve(profile, task.get("series"), task.get("brand_overrides"))
        if source["context"].get("brand_id", resolved["brand_id"]) != resolved["brand_id"]:
            raise ValueError("input brand identity mismatch")
        files["brand-resolved.json"] = dump(resolved)
    files["task.md"] = (
        "# Amazon draft task\n\nContext: " + dump(task["context"]) +
        "\nRead $ecommerce-visual-strategy and its references/amazon modules required by this task. "
        "Read input-delivery.json as the provided draft and evidence index; "
        "inspect its real source documents before making factual assertions. "
        "A copied evidence record is not a copied or verified source document.\n\n"
        "Original input: " + str(source_path) + "\n\n"
        "When present, read brand-resolved.json as style only. "
        "Keep this SKU separate from every other task. Use the target language; "
        "preserve evidence IDs and constraints. Write the actual finished draft to delivery.json, "
        "with context.language matching this task. For actual image-production requests, read "
        "references/editable-production.md and follow the available image-generation skill; "
        "preserve editable SVG and preview files. Draft-only requests do not trigger image generation. "
        "Do not publish or silently switch to paid APIs. "
        "Do not overwrite a reviewed delivery without the user's instruction. "
        "Run the batch audit afterwards.\n")
    return files


def fingerprint(task, files):
    return hashlib.sha256(dump({"task": task, "files": files}).encode("utf-8")).hexdigest()


def run(manifest, output, mode):
    manifest = Path(manifest).resolve()
    tasks = manifest_tasks(load_json(manifest))  # validate identities before any mutation
    root = Path(output).resolve()
    results = []
    for task in tasks:
        tid = task["id"]
        directory = root / tid
        try:
            if directory.resolve().parent != root or directory.is_symlink():
                raise ValueError("task directory redirects outside the batch root")
            files = bundle(task, manifest.parent)
            digest = fingerprint(task, files)
            metadata = {"schema_version": 1, "fingerprint": digest, "context": task["context"]}
            if mode == "prepare" and not directory.exists():
                root.mkdir(parents=True, exist_ok=True)
                directory.mkdir(exist_ok=False)
                # Metadata last: interrupted preparation is never treated as complete.
                for name, content in files.items():
                    write_new(directory / name, content)
                write_new(directory / "prepared.json", dump(metadata))
                results.append({"id": tid, "status": "prepared", "path": str(directory)})
                continue
            if load_json(directory / "prepared.json") != metadata:
                raise ValueError("prepared input changed; use a new batch output directory")
            for name, content in files.items():
                if (directory / name).read_text(encoding="utf-8") != content:
                    raise ValueError("prepared snapshot was modified: " + name)
            if mode == "prepare":
                results.append({"id": tid, "status": "preserved", "path": str(directory)})
                continue
            delivery_path = directory / "delivery.json"
            if not delivery_path.exists():
                results.append({"id": tid, "status": "needs_draft"})
                continue
            data = load_json(delivery_path)
            obj(data, "delivery")
            context = obj(data.get("context"), "delivery.context")
            for key, value in task["context"].items():
                if context.get(key) != value:
                    raise ValueError("finished draft context mismatch: " + key)
            report = audit(data)
            source = load_json(directory / "input-delivery.json")
            source_evidence = {item["id"]: item for item in source["evidence"]}
            final_evidence = data.get("evidence", [])
            for item in final_evidence if isinstance(final_evidence, list) else []:
                if isinstance(item, dict) and item.get("id") in source_evidence and item != source_evidence[item["id"]]:
                    report["errors"].append({"path": "evidence", "message": "source evidence record modified; reconcile original input first"})
            report["ok"] = not report["errors"]
            results.append({"id": tid, "status": "checked" if report["ok"] else "failed", "report": report})
        except (OSError, UnicodeError, ValueError) as exc:
            results.append({"id": tid, "status": "failed", "error": str(exc)})
    return {"ok": all(r["status"] in ("prepared", "preserved", "checked") for r in results),
            "mode": mode, "scope": "local task preparation and mechanical checks; no automatic drafting",
            "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "audit"))
    parser.add_argument("manifest")
    parser.add_argument("--output", required=True, help="batch task root, not a report file")
    args = parser.parse_args()
    try:
        result = run(args.manifest, args.output, args.mode)
    except (OSError, UnicodeError, ValueError) as exc:
        print(dump({"ok": False, "input_error": str(exc)}))
        return 2
    print(dump(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
