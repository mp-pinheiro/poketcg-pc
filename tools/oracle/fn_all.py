#!/usr/bin/env python3
"""Run every migrated schema-2 primary case and report uncovered registry entries."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from routines import ALL  # noqa: E402


def load_cases() -> dict[str, list[tuple[Path, dict]]]:
    found: dict[str, list[tuple[Path, dict]]] = {}
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        spec = importlib.util.spec_from_file_location(f"barrier_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise SystemExit(f"ARTIFACT cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for fn, records in getattr(module, "SCHEMA2_CASES", {}).items():
            found.setdefault(fn, []).extend((path, record) for record in records)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    args = parser.parse_args()
    if not all(path.is_absolute() and path.is_file()
               for path in (args.rom, args.symbols, args.probe, args.runner)):
        print("ARTIFACT missing absolute barrier input", file=sys.stderr)
        return 2
    cases = load_cases()
    failures = 0
    migrated = 0
    skipped = {"scene": 0, "intentional-transform": 0, "native-stress": 0, "dependency-blocked": 0}
    primary_missing = 0
    for fn in ALL:
        records = cases.get(fn, [])
        primary_records = [record for _, record in records if record.get("evidence") == "primary"]
        if not records:
            print(f"SCHEMA missing schema-2 cases {fn}")
            failures += 1
            continue
        if not primary_records:
            primary_missing += 1
            print(f"BOUNDARY no primary case {fn}")
            continue
        for index, (path, record) in enumerate(records):
            evidence = record.get("evidence")
            if evidence != "primary":
                if evidence in skipped:
                    skipped[evidence] += 1
                else:
                    print(f"SCHEMA invalid evidence {fn} case={record.get('id')}")
                    failures += 1
                continue
            migrated += 1
            command = [
                sys.executable, str(ROOT / "tools/oracle/gbref/compare_one.py"),
                "--fn", fn, "--index", str(index), "--case", str(path),
                "--rom", str(args.rom), "--symbols", str(args.symbols),
                "--probe", str(args.probe), "--runner", str(args.runner),
            ]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                    timeout=30, check=False)
            output = result.stdout.strip().splitlines()
            print(output[-1] if output else result.stderr.strip())
            if result.returncode:
                failures += 1
    counts = " ".join(f"{key}={value}" for key, value in skipped.items())
    print(f"INVENTORY routines={len(ALL)} migrated_cases={migrated} primary_missing={primary_missing} skipped_{counts} failures={failures}")
    return 2 if failures or primary_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
