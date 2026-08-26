#!/usr/bin/env python3
"""Validate mutation declarations against their owned C source."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from run_mutation import resolve_anchor  # noqa: E402  (shared anchor rule)


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"mutation_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("routine", "release"), default="routine")
    args = parser.parse_args()
    failures = 0
    declarations = 0
    for case_path in sorted((ROOT / "tests/cases").glob("*.py")):
        module = load(case_path)
        mutations = getattr(module, "MUTATIONS", {})
        if not mutations:
            if args.stage == "release" and getattr(module, "SCHEMA2_CASES", {}):
                print(f"MUTATION missing {case_path}")
                failures += 1
            continue
        for fn, mutation in mutations.items():
            declarations += 1
            required = ("source_symbol", "before", "after", "case_ids")
            before = mutation.get("before") if isinstance(mutation, dict) else None
            if not isinstance(mutation, dict) or any(key not in mutation for key in required):
                print(f"MUTATION schema {case_path}:{fn}")
                failures += 1
                continue
            source_value = mutation.get("source", f"src/home/{case_path.stem}.c")
            if (not isinstance(source_value, str) or not source_value
                    or Path(source_value).is_absolute() or ".." in Path(source_value).parts
                    or Path(source_value).parts[:2] != ("src", "home")):
                print(f"MUTATION source {case_path}:{fn}")
                failures += 1
                continue
            source_path = ROOT / source_value
            source = source_path.read_text() if source_path.is_file() else ""
            # This used to accept `count < 1`, i.e. it only caught a MISSING
            # anchor and silently tolerated an AMBIGUOUS one -- while
            # run_mutation refuses to run an ambiguous anchor at all. That
            # disagreement let 184 of 1837 canaries protect nothing while the
            # release gate stayed green. Audit and runner now share one rule.
            try:
                resolve_anchor(source, mutation["source_symbol"], before)
            except SystemExit as exc:
                print(f"MUTATION anchor {case_path}:{fn} {exc}")
                failures += 1
            if not isinstance(mutation["case_ids"], list) or not mutation["case_ids"]:
                print(f"MUTATION cases {case_path}:{fn}")
                failures += 1
    print(f"MUTATION_AUDIT declarations={declarations} failures={failures}")
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
