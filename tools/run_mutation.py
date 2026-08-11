#!/usr/bin/env python3
"""Run one declared source mutation and record a red oracle result."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load_case(path: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("mutation_case", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def comparison_status(result: subprocess.CompletedProcess[str]) -> str | None:
    for line in reversed(result.stdout.splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and isinstance(payload.get("status"), str):
            return payload["status"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fn")
    parser.add_argument("case", type=Path)
    parser.add_argument("--index", type=int, default=0)
    args = parser.parse_args()
    case_path = (ROOT / args.case).resolve()
    module = load_case(case_path)
    mutation = module.MUTATIONS[args.fn]
    source_value = mutation.get("source", f"src/home/{case_path.stem}.c")
    if not isinstance(source_value, str) or not source_value:
        raise SystemExit("mutation source must be a relative src/home path")
    source_rel = Path(source_value)
    if (source_rel.is_absolute() or ".." in source_rel.parts
            or source_rel.parts[:2] != ("src", "home")):
        raise SystemExit("mutation source must be a relative src/home path")
    source_path = ROOT / source_rel
    original = source_path.read_text()
    if original.count(mutation["before"]) != 1:
        raise SystemExit("mutation anchor is not unique")
    baseline_command = [
        "python3", "tools/oracle/gbref/compare_one.py", "--fn", args.fn,
        "--index", str(args.index), "--case", str(case_path.relative_to(ROOT)),
        "--rom", str((ROOT / "poketcg/poketcg.gbc").resolve()),
        "--symbols", str((ROOT / "poketcg/poketcg.sym").resolve()),
        "--probe", str((ROOT / "build-barrier/poketcg_probe").resolve()),
        "--runner", str((ROOT / "tools/oracle/gbref/build/gbref_runner").resolve()),
    ]
    baseline = subprocess.run(baseline_command, cwd=ROOT, text=True, capture_output=True, check=False)
    if baseline.returncode != 0 or comparison_status(baseline) != "PASS":
        raise SystemExit(f"MUTATION_BASELINE_FAILED: {baseline.stdout or baseline.stderr}")
    with tempfile.TemporaryDirectory(prefix="poketcg-mutation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("CMakeLists.txt", "cmake", "src", "poketcg", "tests", "tools"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, tmp / name, symlinks=True)
            elif source.is_file():
                shutil.copy2(source, tmp / name)
        mutated = original.replace(mutation["before"], mutation["after"], 1)
        (tmp / source_rel).write_text(mutated)
        build = tmp / "build-mutation"
        subprocess.run(["cmake", "-G", "Ninja", "-B", str(build), "-DPORT_FILES="], cwd=tmp, check=True)
        subprocess.run(["ninja", "-C", str(build)], cwd=tmp, check=True)
        command = [
            "python3", "tools/oracle/gbref/compare_one.py", "--fn", args.fn,
            "--index", str(args.index), "--case", str(case_path.relative_to(ROOT)),
            "--rom", str((ROOT / "poketcg/poketcg.gbc").resolve()),
            "--symbols", str((ROOT / "poketcg/poketcg.sym").resolve()),
            "--probe", str((build / "poketcg_probe").resolve()),
            "--runner", str((ROOT / "tools/oracle/gbref/build/gbref_runner").resolve()),
        ]
        result = subprocess.run(command, cwd=tmp, text=True, capture_output=True, check=False)
        result_status = comparison_status(result)
        if result.returncode == 0 and result_status == "PASS":
            raise SystemExit(
                "MUTATION_GREEN: corrupted routine still passed\n"
                + (result.stdout or result.stderr)
            )
        if result.returncode != 1 or result_status != "PORT":
            raise SystemExit(
                "MUTATION_EXECUTION_FAILED: comparator did not report a port mismatch\n"
                + (result.stdout or result.stderr)
            )
        restored = subprocess.run(baseline_command, cwd=ROOT, text=True, capture_output=True, check=False)
        if restored.returncode != 0 or comparison_status(restored) != "PASS":
            raise SystemExit(f"MUTATION_RESTORE_FAILED: {restored.stdout or restored.stderr}")
        receipt = ROOT / "tools/oracle/mutation_receipts"
        receipt.mkdir(parents=True, exist_ok=True)
        output = {
            "fn": args.fn, "case": str(args.case), "index": args.index,
            "status": "RED", "baseline": baseline.stdout,
            "output": result.stdout or result.stderr,
            "restored": restored.stdout,
        }
        (receipt / f"{args.fn}.json").write_text(json.dumps(output, indent=2) + "\n")
        print(f"MUTATION_RED fn={args.fn} index={args.index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
