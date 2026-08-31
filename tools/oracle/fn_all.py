#!/usr/bin/env python3
"""Run every migrated schema-2 primary case and report uncovered registry entries."""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import json
import tempfile
import time
import sys
from concurrent.futures import ThreadPoolExecutor
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


# The gate's own measured inputs, identified by tree object id so the record
# survives a rebase: a landing that CI re-parents onto a release commit keeps
# byte-identical trees, while the commit id it was built at is orphaned.
# tools/progress/report.py recomputes this exact list at HEAD.
# Every path must be tracked: include/ (only gitignored generated headers) and
# poketcg/ (the ignored pret checkout, pinned by tools/oracle/artifacts.json)
# have no tree object, and one unresolvable path voids the whole record.
GATE_INPUT_PATHS = ("src", "tests", "tools/oracle", "CMakeLists.txt")


def gate_input_trees(commit: str) -> dict[str, str] | None:
    """Map every measured gate input to its git tree id at `commit`."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", *(f"{commit}:{path}" for path in GATE_INPUT_PATHS)],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None
    ids = result.stdout.split()
    if result.returncode != 0 or len(ids) != len(GATE_INPUT_PATHS):
        return None
    return dict(zip(GATE_INPUT_PATHS, ids))


def write_json_atomic(path: Path, payload: dict) -> None:
    """Publish the gate record by rename, never in place.

    Every factory selection reads site/data/gate.json while the landing driver
    is still writing it; a torn read would fail an unrelated attempt.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
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
            "input_trees": gate_input_trees(report_commit) if report_commit else None,
            "complete": False,
            "routines": {},
        }
    cases = load_cases()
    failures = 0
    fn_failures: dict[str, int] = {}
    fn_primaries: dict[str, int] = {}
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
    jobs: list[tuple[str, int, Path]] = []
    reported_fns: list[str] = []
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
        reported_fns.append(fn)
        fn_primaries[fn] = len(primary_records)
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
            jobs.append((fn, index, path))

    def run_job(job: tuple[str, int, Path]) -> tuple[str, str, int]:
        fn, index, path = job
        command = [
            sys.executable, str(ROOT / "tools/oracle/gbref/compare_one.py"),
            "--fn", fn, "--index", str(index), "--case", str(path),
            "--rom", str(args.rom), "--symbols", str(args.symbols),
            "--probe", str(args.probe), "--runner", str(args.runner),
        ]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                timeout=120, check=False)
        output = result.stdout.strip().splitlines()
        line = output[-1] if output else result.stderr.strip()
        return fn, line, result.returncode

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for fn, line, returncode in pool.map(run_job, jobs):
            print(line)
            if returncode:
                fn_failures[fn] += 1
                failures += 1

    if report_data is not None:
        for fn in reported_fns:
            failing = fn_failures[fn]
            report_data["routines"][fn] = {
                "status": "fail" if failing else "pass",
                "cases": fn_primaries[fn],
                "failing": failing,
            }
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
        write_json_atomic(args.report, report_data)
    return 2 if failures or primary_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
