#!/usr/bin/env python3
"""Differential fuzz for thin case matrices. Advisory; never part of the gate.

Perturbs declared inputs of existing primary schema-2 cases - input registers
and seeded WRAM bytes only, never the observation contract - and replays each
variant through tools/oracle/gbref/compare_one.py. Both oracles receive the
identical variant, so a `status=PORT` verdict is a real native/reference
divergence the landed matrix missed. Harness rejections (SCHEMA/BACKEND
messages, reference-side hangs or divergence) mean the perturbed input is not
comparable, and count as inconclusive, not as findings.

Findings land in `.factory/fuzz-report.json` (untracked operational state) and
on stdout. A divergence is handled through the revocation + re-port flow, plus
a blocked.toml stanza when it exposes a harness gap.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "site" / "data" / "gate.json"
PROGRESS = ROOT / "site" / "data" / "progress.json"
REPORT = ROOT / ".factory" / "fuzz-report.json"
COMPARE = ROOT / "tools" / "oracle" / "gbref" / "compare_one.py"
REGS8 = ("a", "b", "c", "d", "e")
THIN_MAX_CASES = 4


def _load_module(path: Path):
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("fuzz_cases", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load case module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _paths() -> dict[str, Path]:
    paths = {
        "rom": ROOT / "poketcg" / "poketcg.gbc",
        "symbols": ROOT / "poketcg" / "poketcg.sym",
        "probe": ROOT / "build-barrier" / "poketcg_probe",
        "runner": ROOT / "tools" / "oracle" / "gbref" / "build" / "gbref_runner",
    }
    missing = [str(p) for p in paths.values() if not p.is_file()]
    if missing:
        raise SystemExit("missing oracle inputs (run `just bootstrap`, "
                         f"`just build-barrier`, `just oracle-build-gbref`): {missing}")
    return paths


def _variant(record: dict, rng: random.Random) -> dict:
    out = copy.deepcopy(record)
    for reg in REGS8:
        if reg in out:
            out[reg] = rng.randrange(256)
    if "hl" in out:
        out["hl"] = rng.randrange(0x10000)
    if "f" in out:
        out["f"] = rng.randrange(16) * 16
    seeds = out.get("seeds") or {}
    wram = seeds.get("wram") or {}
    for address, payload in wram.items():
        parsed = int(address, 0) if isinstance(address, str) else int(address)
        if 0xFF00 <= parsed <= 0xFF7F:
            # IO registers: the reference PPU/timer owns these (rLY reads as
            # hardware state, not as the seeded byte), so a perturbed value
            # diverges by backend semantics, not by port behavior.
            continue
        wram[address] = [rng.randrange(256) for _ in payload]
    return out


def _basename_for(fn: str) -> str | None:
    functions = json.loads(PROGRESS.read_text()).get("functions", [])
    for record in functions:
        if record.get("name") == fn and record.get("file"):
            return Path(record["file"]).stem
    return None


def fuzz_fn(fn: str, module_path: Path, variants: int,
            paths: dict[str, Path]) -> dict:
    module = _load_module(module_path)
    records = getattr(module, "SCHEMA2_CASES", {}).get(fn) or []
    contract = getattr(module, "CONTRACT", {}).get(fn)
    primaries = [(index, record) for index, record in enumerate(records)
                 if isinstance(record, dict) and record.get("evidence") == "primary"]
    result = {"fn": fn, "module": str(module_path), "variants": 0,
              "pass": 0, "inconclusive": 0, "divergences": []}
    if not primaries or not isinstance(contract, dict):
        result["inconclusive"] = variants
        print(f"FUZZ {fn} skipped detail=no primary cases or contract")
        return result
    with tempfile.TemporaryDirectory(prefix="poketcg-fuzz-") as tmp:
        case_path = Path(tmp) / "case.py"
        for index in range(variants):
            base_index, base = primaries[index % len(primaries)]
            rng = random.Random(f"{fn}:{base_index}:{index}")
            record = _variant(base, rng)
            case_path.write_text(
                f"CONTRACT = {{{fn!r}: {contract!r}}}\n"
                f"SCHEMA2_CASES = {{{fn!r}: [{record!r}]}}\n"
            )
            command = [
                sys.executable, str(COMPARE), "--fn", fn, "--index", "0",
                "--case", str(case_path), "--rom", str(paths["rom"]),
                "--symbols", str(paths["symbols"]), "--probe", str(paths["probe"]),
                "--runner", str(paths["runner"]),
            ]
            try:
                run = subprocess.run(command, capture_output=True, text=True,
                                     timeout=120, check=False)
            except subprocess.TimeoutExpired:
                result["inconclusive"] += 1
                result["variants"] += 1
                continue
            result["variants"] += 1
            verdict = None
            for line in reversed(run.stdout.splitlines()):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        verdict = json.loads(line)
                    except json.JSONDecodeError:
                        verdict = None
                    break
            if run.returncode == 0 and verdict and verdict.get("status") == "PASS":
                result["pass"] += 1
            elif verdict and verdict.get("status") == "PORT":
                result["divergences"].append({
                    "variant": index,
                    "base_index": base_index,
                    "mismatches": verdict.get("mismatches"),
                    "inputs": {key: record.get(key)
                               for key in (*REGS8, "f", "hl", "seeds")
                               if key in record},
                })
            else:
                result["inconclusive"] += 1
    print(f"FUZZ {fn} variants={result['variants']} pass={result['pass']} "
          f"divergence={len(result['divergences'])} "
          f"inconclusive={result['inconclusive']}")
    return result


def thinnest(limit: int) -> list[tuple[str, Path]]:
    routines = json.loads(GATE.read_text()).get("routines") or {}
    ranked = sorted(
        ((name, row) for name, row in routines.items()
         if row.get("status") == "pass"
         and 0 < int(row.get("cases", 0)) <= THIN_MAX_CASES),
        key=lambda item: (int(item[1].get("cases", 0)), item[0]),
    )
    selected: list[tuple[str, Path]] = []
    for name, _row in ranked:
        basename = _basename_for(name)
        if basename is None:
            continue
        module_path = ROOT / "tests" / "cases" / f"{basename}.py"
        if module_path.is_file():
            selected.append((name, module_path))
        if len(selected) >= limit:
            break
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--fn", help="fuzz one routine")
    target.add_argument("--thinnest", type=int,
                        help="fuzz the N thinnest passing routines")
    parser.add_argument("--variants", type=int, default=16,
                        help="variants per routine")
    arguments = parser.parse_args(argv)
    if arguments.variants < 1:
        parser.error("--variants must be at least 1")
    paths = _paths()
    if arguments.fn:
        basename = _basename_for(arguments.fn)
        if basename is None:
            raise SystemExit(f"{arguments.fn}: no source mapping in progress.json")
        targets = [(arguments.fn, ROOT / "tests" / "cases" / f"{basename}.py")]
    else:
        targets = thinnest(arguments.thinnest)
    results = [fuzz_fn(fn, module_path, arguments.variants, paths)
               for fn, module_path in targets]
    divergences = sum(len(result["divergences"]) for result in results)
    REPORT.write_text(json.dumps({
        "generated_at": int(time.time()),
        "variants_per_routine": arguments.variants,
        "results": results,
    }, indent=1, sort_keys=True))
    print(f"FUZZ status routines={len(results)} divergences={divergences} "
          f"report={REPORT}")
    return 1 if divergences else 0


if __name__ == "__main__":
    raise SystemExit(main())
