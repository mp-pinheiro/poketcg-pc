#!/usr/bin/env python3
"""Audit case declarations before they enter a primary or release gate."""

from __future__ import annotations

import argparse
import re
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "oracle"))

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests" / "cases"))
sys.path.insert(0, str(ROOT))
from schema import SchemaValidationError, validate_cases
sys.path.insert(0, str(ROOT / "tests"))
from routines import ALL, EXCLUSIONS

ALLOWED_EXCLUSION_KINDS = {
    "dead-zero-callsites",
    "hardware-transform",
    "sgb-only",
    "fallthrough-only",
    "trampoline-direct-call",
    "dependency-pending",
}

def load_modules() -> list[tuple[Path, object]]:
    result = []
    for path in sorted((ROOT / "tests/cases").glob("*.py")):
        if path.name == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location(f"audit_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result.append((path, module))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("routine", "release"), required=True)
    args = parser.parse_args()
    failures = 0
    modules = load_modules()
    for basename, entries in EXCLUSIONS.items():
        if not isinstance(entries, dict):
            print(f"EXCLUSION {basename}: entries must be a mapping")
            failures += 1
            continue
        owned = set()
        for path, module in modules:
            if path.stem == basename:
                owned = set(getattr(module, "SCHEMA2_CASES", {}))
                break
        for fn, exclusion in entries.items():
            if fn not in ALL:
                print(f"EXCLUSION {basename}:{fn}: not in registry")
                failures += 1
            if not isinstance(exclusion, dict) or any(
                not isinstance(exclusion.get(key), str) or not exclusion[key].strip()
                for key in ("kind", "source", "reason")
            ):
                print(f"EXCLUSION {basename}:{fn}: requires kind/source/reason")
                failures += 1
                continue
            match = re.fullmatch(r"(.+):([1-9][0-9]*)-([1-9][0-9]*)", exclusion["source"])
            if match is None:
                print(f"EXCLUSION {basename}:{fn}: source must include line range")
                failures += 1
                continue
            source = ROOT / match.group(1)
            start, end = int(match.group(2)), int(match.group(3))
            if not source.is_file():
                print(f"EXCLUSION {basename}:{fn}: missing source {exclusion['source']}")
                failures += 1
            elif not start <= end <= len(source.read_text().splitlines()):
                print(f"EXCLUSION {basename}:{fn}: source range out of bounds")
                failures += 1
            if fn in owned:
                print(f"EXCLUSION {basename}:{fn}: cannot also declare schema cases")
                failures += 1
            if args.stage == "release" and exclusion["kind"] == "dependency-pending":
                print(f"EXCLUSION dependency-pending blocks release {basename}:{fn}")
                failures += 1
    for path, module in load_modules():
        if not hasattr(module, "SCHEMA2_CASES") and getattr(module, "CASES", {}):
            print(f"MIGRATION_PENDING {path}: legacy CASES has no SCHEMA2_CASES")
            failures += 1
            continue
        cases = getattr(module, "SCHEMA2_CASES", {})
        flattened = {}
        for fn, records in cases.items():
            if not isinstance(records, list):
                print(f"SCHEMA {path}: {fn} cases must be a list")
                failures += 1
                continue
            for record in records:
                if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                    print(f"SCHEMA {path}: {fn} case must have a stable id")
                    failures += 1
                    continue
                flattened[record["id"]] = record
        try:
            validate_cases(flattened)
        except SchemaValidationError as exc:
            print(f"SCHEMA {path}: {exc}")
            failures += 1
        if args.stage == "release":
            mutations = getattr(module, "MUTATIONS", None)
            if flattened and not isinstance(mutations, dict):
                print(f"SCHEMA {path}: release stage requires MUTATIONS mapping")
                failures += 1
            elif flattened and not mutations:
                print(f"SCHEMA {path}: release stage requires non-empty MUTATIONS")
                failures += 1
    if failures:
        print(f"AUDIT_FAIL stage={args.stage} failures={failures}")
        return 2
    print(f"AUDIT_OK stage={args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
