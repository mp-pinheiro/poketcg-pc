#!/usr/bin/env python3
"""Execute the primary mutation witness for every registered routine."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
RECEIPT_DIR = ROOT / "tools" / "oracle" / "mutation_receipts"
OUTPUT = ROOT / "build" / "completion" / "mutation-campaign.json"


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(f"mutation_campaign_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def witness_index(case_ids: list[object]) -> int:
    for case_id in case_ids:
        match = re.search(r"-(\d+)$", str(case_id))
        if match:
            return int(match.group(1))
    return 0


def targets() -> list[tuple[str, str, int]]:
    found: list[tuple[str, str, int]] = []
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        module = load_module(path)
        for fn, mutation in getattr(module, "MUTATIONS", {}).items():
            case_ids = mutation.get("case_ids") if isinstance(mutation, dict) else None
            if isinstance(case_ids, list) and case_ids:
                found.append((fn, path.relative_to(ROOT).as_posix(), witness_index(case_ids)))
    return sorted(found)


def run_target(fn: str, case: str, index: int, build: Path, runner: Path, timeout: float) -> dict[str, Any]:
    command = [
        sys.executable,
        "tools/run_mutation.py",
        fn,
        case,
        "--index",
        str(index),
        "--build",
        str(build),
        "--runner",
        str(runner),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {"fn": fn, "case": case, "index": index, "status": "TIMEOUT", "detail": str(exc)}
    output = (completed.stdout + completed.stderr).strip()
    status = "RED" if completed.returncode == 0 and "MUTATION_RED" in output else "FAIL"
    return {"fn": fn, "case": case, "index": index, "status": status, "output": output}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="run every witness, including existing receipts")
    parser.add_argument("--missing", action="store_true", help="run only witnesses without a receipt")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--build", type=Path, default=ROOT / "build")
    parser.add_argument(
        "--runner",
        type=Path,
        default=ROOT / "tools" / "oracle" / "gbref" / "build" / "gbref_runner",
    )
    parser.add_argument("--timeout", type=float, default=1800.0)
    args = parser.parse_args(argv)
    if args.all and args.missing:
        parser.error("--all and --missing are mutually exclusive")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    build = args.build if args.build.is_absolute() else ROOT / args.build
    runner = args.runner if args.runner.is_absolute() else ROOT / args.runner
    if not (build / "poketcg_probe").is_file():
        raise SystemExit(f"missing {build / 'poketcg_probe'}; run just build")
    if not runner.is_file():
        raise SystemExit(f"missing {runner}; run just oracle-build-gbref")
    all_targets = targets()
    if not args.all:
        existing = {path.stem for path in RECEIPT_DIR.glob("*.json")}
        if args.missing:
            all_targets = [item for item in all_targets if item[0] not in existing]
        else:
            all_targets = [item for item in all_targets if item[0] not in existing]
    if args.limit is not None:
        all_targets = all_targets[: args.limit]
    results = []
    for fn, case, index in all_targets:
        result = run_target(fn, case, index, build, runner, args.timeout)
        results.append(result)
        print(json.dumps({key: result[key] for key in ("fn", "index", "status")}, sort_keys=True))
        if result["status"] != "RED":
            print(result.get("output", result.get("detail", "")), file=sys.stderr)
    summary = {
        "schema": 1,
        "mode": "all" if args.all else "missing",
        "targets": len(all_targets),
        "red": sum(result["status"] == "RED" for result in results),
        "failed": sum(result["status"] != "RED" for result in results),
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("mode", "targets", "red", "failed")}, sort_keys=True))
    return 0 if summary["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
