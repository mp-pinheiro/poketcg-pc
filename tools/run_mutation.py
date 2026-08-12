#!/usr/bin/env python3
"""Run one declared source mutation in place and record a red oracle result.

The mutation is applied to the working tree (repo root or a factory lane),
rebuilt incrementally with ninja, compared through the GBRT lane, restored,
and rebuilt again.  No tempdir clean-room: the caller owns the tree, and the
restore runs in a ``finally`` so a crash never leaves the mutated source.
"""

from __future__ import annotations

import argparse
import json
import subprocess
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
    parser.add_argument("--build", type=Path, default=ROOT / "build-barrier",
                        help="ninja build dir whose probe is rebuilt in place")
    parser.add_argument("--runner", type=Path,
                        default=ROOT / "tools/oracle/gbref/build/gbref_runner")
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

    build_dir = args.build if args.build.is_absolute() else ROOT / args.build
    probe = build_dir / "poketcg_probe"
    if not probe.exists():
        raise SystemExit(f"{probe} not built; configure {build_dir} first")
    runner = args.runner if args.runner.is_absolute() else ROOT / args.runner
    if not runner.exists():
        raise SystemExit(f"{runner} missing; run just oracle-build-gbref")

    compare_command = [
        sys.executable, "tools/oracle/gbref/compare_one.py", "--fn", args.fn,
        "--index", str(args.index), "--case", str(case_path.relative_to(ROOT)),
        "--rom", str((ROOT / "poketcg/poketcg.gbc").resolve()),
        "--symbols", str((ROOT / "poketcg/poketcg.sym").resolve()),
        "--probe", str(probe.resolve()),
        "--runner", str(runner.resolve()),
    ]

    def compare() -> subprocess.CompletedProcess[str]:
        return subprocess.run(compare_command, cwd=ROOT, text=True,
                              capture_output=True, check=False)

    def rebuild() -> None:
        built = subprocess.run(["ninja", "-C", str(build_dir)], cwd=ROOT,
                               text=True, capture_output=True, check=False)
        if built.returncode != 0:
            raise SystemExit(f"MUTATION_BUILD_FAILED: {built.stdout}{built.stderr}")

    baseline = compare()
    if baseline.returncode != 0 or comparison_status(baseline) != "PASS":
        raise SystemExit(f"MUTATION_BASELINE_FAILED: {baseline.stdout or baseline.stderr}")

    result = None
    try:
        source_path.write_text(original.replace(mutation["before"], mutation["after"], 1))
        rebuild()
        result = compare()
    finally:
        source_path.write_text(original)

    result_status = comparison_status(result)
    if result.returncode == 0 and result_status == "PASS":
        rebuild()
        raise SystemExit(
            "MUTATION_GREEN: corrupted routine still passed\n"
            + (result.stdout or result.stderr)
        )
    if result.returncode != 1 or result_status != "PORT":
        rebuild()
        raise SystemExit(
            "MUTATION_EXECUTION_FAILED: comparator did not report a port mismatch\n"
            + (result.stdout or result.stderr)
        )

    rebuild()
    restored = compare()
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
