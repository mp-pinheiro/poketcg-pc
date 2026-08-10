#!/usr/bin/env python3
"""Audit case declarations before they enter a primary or release gate."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "oracle"))

ROOT = Path(__file__).resolve().parent.parent
from schema import SchemaValidationError, validate_cases

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
    for path, module in load_modules():
        cases = getattr(module, "CASES", {})
        if not isinstance(cases, dict):
            print(f"SCHEMA {path}: CASES must be a mapping")
            failures += 1
            continue
        try:
            validate_cases(cases)
        except SchemaValidationError as exc:
            print(f"SCHEMA {path}: {exc}")
            failures += 1
        if args.stage == "release" and not hasattr(module, "MUTATIONS"):
            print(f"SCHEMA {path}: release stage requires MUTATIONS")
            failures += 1
    if failures:
        print(f"AUDIT_FAIL stage={args.stage} failures={failures}")
        return 2
    print(f"AUDIT_OK stage={args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
