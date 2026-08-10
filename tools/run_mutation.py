#!/usr/bin/env python3
"""Run one declared source mutation and record a red oracle result."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_case(path: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("mutation_case", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fn")
    parser.add_argument("case", type=Path)
    parser.add_argument("--index", type=int, default=0)
    args = parser.parse_args()
    case_path = (ROOT / args.case).resolve()
    module = load_case(case_path)
    mutation = module.MUTATIONS[args.fn]
    source_path = ROOT / "src/home" / f"{case_path.stem}.c"
    original = source_path.read_text()
    if original.count(mutation["before"]) != 1:
        raise SystemExit("mutation anchor is not unique")
    with tempfile.TemporaryDirectory(prefix="poketcg-mutation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("CMakeLists.txt", "cmake", "src", "poketcg", "tests", "tools"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, tmp / name, symlinks=True)
            elif source.is_file():
                shutil.copy2(source, tmp / name)
        mutated = original.replace(mutation["before"], mutation["after"], 1)
        (tmp / "src/home" / source_path.name).write_text(mutated)
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
        if result.returncode == 0:
            raise SystemExit("MUTATION_GREEN: corrupted routine still passed")
        receipt = ROOT / "tools/oracle/mutation_receipts"
        receipt.mkdir(parents=True, exist_ok=True)
        output = {"fn": args.fn, "case": str(args.case), "index": args.index, "status": "RED", "output": result.stdout or result.stderr}
        (receipt / f"{args.fn}.json").write_text(json.dumps(output, indent=2) + "\n")
        print(f"MUTATION_RED fn={args.fn} index={args.index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
