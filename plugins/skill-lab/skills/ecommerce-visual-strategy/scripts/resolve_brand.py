"""Resolve brand -> series -> task settings, with leaf provenance."""
import argparse
import copy
import sys
from workflow_common import dump, load_json, nonempty, obj, version

SECTIONS = {
    "style": {"palette_roles", "typography", "icons", "spacing", "photography", "avoid"},
    "voice": {"tone", "avoid"},
    "glossary": None,
    "assets": None,
}


def check_settings(settings):
    obj(settings, "settings")
    for section, value in settings.items():
        if section not in SECTIONS:
            raise ValueError("not an inheritable brand section: " + section)
        if SECTIONS[section] is not None:
            obj(value, section)
            if set(value) - SECTIONS[section]:
                raise ValueError("unknown setting in " + section)
            for key, item in value.items():
                if not isinstance(item, (str, dict, list)) or item is None:
                    raise ValueError(section + "." + key + " must be text, object or array")
        else:
            if not isinstance(value, list):
                raise ValueError(section + " must be an array (replacement, not append)")
            for row in value:
                obj(row, section)
                fields = ("source", "target", "language", "status") if section == "glossary" else ("path", "license", "source")
                for key in fields:
                    nonempty(row.get(key), section + "." + key)
                if section == "glossary" and row["status"] not in ("approved", "proposed"):
                    raise ValueError("glossary status must be approved or proposed")


def resolve(profile, series=None, overrides=None):
    version(profile)
    allowed = {"schema_version", "brand_id", "revision", "status", "defaults", "series"}
    if set(profile) - allowed:
        raise ValueError("brand profile contains unsupported fields; product facts belong to SKU evidence")
    for key in ("brand_id", "revision"):
        nonempty(profile.get(key), key)
    if profile.get("status") not in ("confirmed", "hypothesis"):
        raise ValueError("brand status must be confirmed or hypothesis")
    series_map = obj(profile.get("series", {}), "series")
    check_settings(profile.get("defaults"))
    for settings in series_map.values():
        check_settings(settings)
    layers = [("brand:" + profile["revision"], profile["defaults"])]
    if series is not None:
        if series not in series_map:
            raise ValueError("unknown brand series: " + str(series))
        layers.append(("series:" + series, series_map[series]))
    if overrides is not None:
        check_settings(overrides)
        layers.append(("task", overrides))
    result, origins = {}, {}

    def merge(target, changes, prefix, origin):
        for key, value in changes.items():
            path = prefix + key
            if isinstance(value, dict):
                if not isinstance(target.get(key), dict):
                    target[key] = {}
                    for old in list(origins):
                        if old == path or old.startswith(path + "."):
                            del origins[old]
                merge(target[key], value, path + ".", origin)
            else:
                target[key] = copy.deepcopy(value)
                for old in list(origins):
                    if old == path or old.startswith(path + "."):
                        del origins[old]
                origins[path] = origin

    for origin, settings in layers:
        merge(result, settings, "", origin)
    return {"schema_version": 1, "brand_id": profile["brand_id"], "revision": profile["revision"],
            "status": profile["status"], "series": series, "settings": result, "origins": origins,
            "scope": "style and voice only; not product evidence or asset license verification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile")
    parser.add_argument("--series")
    parser.add_argument("--overrides", help="JSON containing inheritable settings only")
    args = parser.parse_args()
    try:
        result = resolve(load_json(args.profile), args.series,
                         load_json(args.overrides) if args.overrides else None)
    except (OSError, UnicodeError, ValueError) as exc:
        print(dump({"ok": False, "input_error": str(exc)}))
        return 2
    print(dump(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
