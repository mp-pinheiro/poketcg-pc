#!/usr/bin/env python3
"""Run every migrated schema-2 primary case and report uncovered registry entries."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import json
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from routines import ALL, EXCLUSIONS  # noqa: E402
EXCLUDED = {
    fn: entry
    for basename, entries in EXCLUSIONS.items()
    for fn, entry in entries.items()
}


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
    parser.add_argument("--report", type=Path, help="write gate record to JSON")
    args = parser.parse_args()
    if not all(path.is_absolute() and path.is_file()
               for path in (args.rom, args.symbols, args.probe, args.runner)):
        print("ARTIFACT missing absolute barrier input", file=sys.stderr)
        return 2
    report_data = None
    report_commit = None
    if args.report:
        try:
            rr = subprocess.run(
                ["jj", "log", "-r", "@-", "--no-graph", "-T", "commit_id"],
                capture_output=True, text=True, timeout=5,
            )
            if rr.returncode == 0:
                report_commit = rr.stdout.strip()
        except Exception:
            pass
        report_data = {
            "schema": 1,
            "generated_at": 0,
            "commit": report_commit,
            "complete": False,
            "routines": {},
        }
    cases = load_cases()
    failures = 0
    fn_failures = {}
    primary = 0
    evidence_counts = {
        "scene": 0,
        "intentional-transform": 0,
        "native-stress": 0,
        "dependency-blocked": 0,
    }
    for fn in ALL:
        fn_failures.setdefault(fn, 0)
    primary_missing = 0
    for fn in ALL:
        records = cases.get(fn, [])
        if fn in EXCLUDED:
            entry = EXCLUDED[fn]
            kind = entry.get("kind")
            if kind == "dependency-pending":
                evidence_counts["dependency-blocked"] += 1
                print(f"EXCLUSION dependency-pending {fn}: {entry['reason']}")
            else:
                evidence_counts["intentional-transform"] += 1
                print(f"EXCLUSION {kind} {fn}: {entry['reason']}")
            continue
        if not records:
            print(f"SCHEMA missing schema-2 cases {fn}")
            failures += 1
            continue
        primary_records = [record for _, record in records if record.get("evidence") == "primary"]
        if not primary_records:
            primary_missing += 1
            print(f"BOUNDARY no primary case {fn}")
            continue
        for index, (path, record) in enumerate(records):
            evidence = record.get("evidence")
            if evidence != "primary":
                if evidence in evidence_counts:
                    evidence_counts[evidence] += 1
                else:
                    print(f"SCHEMA invalid evidence {fn} case={record.get('id')}")
                    failures += 1
                continue
            primary += 1
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
                fn_failures[fn] += 1
                failures += 1
        if report_data is not None and fn in fn_failures:
            total_cases = len(primary_records)
            failing = fn_failures[fn]
            report_data["routines"][fn] = {
                "status": "fail" if failing else "pass",
                "cases": total_cases,
                "failing": failing,
            }
            report_data["generated_at"] = int(time.time())
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(
                json.dumps(report_data, sort_keys=True, separators=(",", ":"))
            )
    counts = " ".join(
        f"{key}={value}" for key, value in evidence_counts.items()
    )
    print(
        f"INVENTORY routines={len(ALL)} primary={primary} "
        f"primary_missing={primary_missing} {counts} failures={failures}"
    )
    if report_data is not None:
        report_data["inventory"] = {
            "routines": len(ALL),
            "primary": primary,
            "primary_missing": primary_missing,
            **evidence_counts,
            "failures": failures,
        }
        report_data["complete"] = True
        report_data["generated_at"] = int(time.time())
        args.report.write_text(
            json.dumps(report_data, sort_keys=True, separators=(",", ":"))
        )
    return 2 if failures or primary_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
