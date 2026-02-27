import json
import sys
import argparse


def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in '{filepath}': {e}")
        sys.exit(1)


def get_all_keys(data, prefix=""):
    keys = set()
    for k, v in data.items():
        full_key = f"{prefix}.{k}" if prefix else k
        keys.add(full_key)
        if isinstance(v, dict):
            keys |= get_all_keys(v, full_key)
    return keys


def get_empty_keys(data, prefix=""):
    empties = []
    for k, v in data.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            empties.extend(get_empty_keys(v, full_key))
        elif isinstance(v, str) and v.strip() == "":
            empties.append(full_key)
    return empties


def analyze(template_path, translation_path):
    template = load_json(template_path)
    translation = load_json(translation_path)

    template_keys = get_all_keys(template)
    translation_keys = get_all_keys(translation)

    total = len(template_keys)
    missing_keys = sorted(template_keys - translation_keys)
    present_count = len(template_keys & translation_keys)
    empty_keys = [k for k in get_empty_keys(translation) if k in template_keys]
    completeness = (present_count / total * 100) if total > 0 else 0
    effective_pct = (max(0, total - len(missing_keys) - len(empty_keys)) / total * 100) if total > 0 else 0

    print(f"\nTemplate   : {template_path}")
    print(f"Translation: {translation_path}\n")
    print(f"Total keys : {total}")
    print(f"Present    : {present_count}")
    print(f"Missing    : {len(missing_keys)}")
    print(f"Empty      : {len(empty_keys)}")
    print(f"\nCompleteness : {completeness:.1f}%  (effective: {effective_pct:.1f}%)")

    if missing_keys:
        print(f"\nMissing keys ({len(missing_keys)}):")
        for k in missing_keys:
            parts = k.split(".")
            val = template
            for p in parts:
                val = val.get(p, "") if isinstance(val, dict) else ""
            hint = f'  -> "{val}"' if isinstance(val, str) and val else ""
            print(f"  {k}{hint}")

    if empty_keys:
        print(f"\nEmpty values ({len(empty_keys)}):")
        for k in empty_keys:
            print(f"  {k}")

    extra_keys = sorted(translation_keys - template_keys)
    if extra_keys:
        print(f"\nExtra keys ({len(extra_keys)}):")
        for k in extra_keys:
            print(f"  {k}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Check completeness of a translation JSON file.")
    parser.add_argument("template", help="Template JSON file (reference language)")
    parser.add_argument("translation", help="Translation JSON file to check")
    args = parser.parse_args()
    analyze(args.template, args.translation)


if __name__ == "__main__":
    main()
