#!/usr/bin/env python3
"""Oracle diff driver: PyBoy vs poketcg_probe, per routine, per case.

The input matrix lives here (tests/cases/<pret file>.py), not in the ports, so a
port cannot pick the inputs that make it look correct. Each case module exports:

    CONTRACT = {"<pret symbol>": ("a", "b", "c", "d", "e", "hl")}   # fields to diff
    CASES    = {"<pret symbol>": [ {"a":..., "wram": {addr: bytes}}, ... ]}

Every address a case supplies under "wram" is read back and diffed too. A routine
listed in tests/routines.py with no cases fails; it is never reported as a pass.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "oracle"))
sys.path.insert(0, str(ROOT / "tests"))

from pyboy_oracle import Oracle, OracleError  # noqa: E402
from routines import ALL  # noqa: E402

REGS = ("a", "f", "b", "c", "d", "e", "hl")


def load_cases() -> tuple[dict[str, list[dict]], dict[str, tuple[str, ...]]]:
    cases: dict[str, list[dict]] = {}
    contracts: dict[str, tuple[str, ...]] = {}
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        if path.name == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location(f"cases_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name, entries in getattr(mod, "CASES", {}).items():
            if name in cases:
                raise SystemExit(f"duplicate CASES entry for {name} in {path}")
            cases[name] = entries
        for name, fields in getattr(mod, "CONTRACT", {}).items():
            if name in contracts:
                raise SystemExit(f"duplicate CONTRACT entry for {name} in {path}")
            contracts[name] = tuple(fields)
    return cases, contracts


def run_probe(probe: Path, fn: str, case: dict, reads: dict[int, int]) -> dict:
    req = {"fn": fn}
    for r in REGS:
        req[r] = int(case.get(r, 0))
    req["wram"] = {str(addr): bytes(data).hex() for addr, data in case.get("wram", {}).items()}
    req["read"] = {str(addr): n for addr, n in reads.items()}
    out = subprocess.run([str(probe)], input=json.dumps(req), capture_output=True, text=True)
    if out.returncode != 0 and not out.stdout.strip():
        raise RuntimeError(f"probe failed ({out.returncode}): {out.stderr.strip()}")
    try:
        res = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"probe emitted non-JSON: {out.stdout!r} {out.stderr.strip()}")
    if "error" in res:
        raise RuntimeError(f"probe error: {res['error']}")
    return res


def diff_case(oracle: Oracle, probe: Path, fn: str, fields: tuple[str, ...], case: dict) -> list[str]:
    bad: list[str] = []

    # A handful of documented boundaries cannot run on the oracle: bc=0 on a
    # counted routine means 65536, which overwrites the whole address space
    # including the synthesized call frame. Those carry oracle=False plus an
    # `expect` map derived from the asm, and are diffed against the C alone.
    if not case.get("oracle", True):
        if not case.get("why"):
            return ["oracle=False case must carry a `why` string"]
        expect = case.get("expect")
        if not expect:
            return ["oracle=False case must carry an `expect` map"]
        reads = {a: len(v) for a, v in expect.items()}
        got = run_probe(probe, fn, case, reads)
        for addr, want in expect.items():
            have = bytes.fromhex(got["wram"][str(addr)])
            if bytes(want) != have:
                bad.append(f"${addr:04X}: asm expects {bytes(want).hex()} != C {have.hex()}")
        return bad

    ref = oracle.call(
        fn,
        a=case.get("a", 0), f=case.get("f", 0), b=case.get("b", 0), c=case.get("c", 0),
        d=case.get("d", 0), e=case.get("e", 0), hl=case.get("hl", 0),
        wram=case.get("wram"),
    )
    reads = {addr: len(data) for addr, data in case.get("wram", {}).items()}
    reads.update(case.get("read", {}))
    got = run_probe(probe, fn, case, reads)

    for field in fields:
        want, have = getattr(ref, field), got[field]
        if want != have:
            width = 4 if field == "hl" else 2
            bad.append(f"{field}: oracle ${want:0{width}X} != C ${have:0{width}X}")
    for addr, n in sorted(reads.items()):
        want = ref.mem(addr, n)
        have = bytes.fromhex(got["wram"][str(addr)])
        if want != have:
            bad.append(f"${addr:04X}: oracle {want.hex()} != C {have.hex()}")
    return bad


def describe(case: dict) -> str:
    regs = " ".join(f"{r}=${case[r]:X}" for r in REGS if case.get(r))
    mem = " ".join(f"${a:04X}={bytes(d).hex()}" for a, d in case.get("wram", {}).items())
    tag = "" if case.get("oracle", True) else "[c-only] "
    return tag + (" ".join(x for x in (regs, mem) if x) or "all-zero")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fn", action="append", help="routine to diff (repeatable)")
    ap.add_argument("--all", action="store_true", help="diff every routine in tests/routines.py")
    ap.add_argument("--probe", type=Path, default=ROOT / "build" / "poketcg_probe")
    ap.add_argument("--rom", default=os.environ.get("POKETCG_ROM", str(ROOT / "poketcg" / "poketcg.gbc")))
    args = ap.parse_args()

    if not args.fn and not args.all:
        ap.error("pass --fn NAME or --all")
    if not args.probe.exists():
        raise SystemExit(f"{args.probe} not built; run `just build`")
    os.environ.setdefault("POKETCG_ROM", args.rom)

    cases, contracts = load_cases()
    wanted = tuple(ALL) if args.all else tuple(args.fn)

    failures = 0
    with Oracle(args.rom) as oracle:
        for fn in wanted:
            entries = cases.get(fn)
            if not entries:
                print(f"FAIL {fn}: no cases")
                failures += 1
                continue
            fields = contracts.get(fn)
            if fields is None:
                print(f"FAIL {fn}: no CONTRACT entry naming the fields to diff")
                failures += 1
                continue
            bad_cases = 0
            for i, case in enumerate(entries):
                try:
                    bad = diff_case(oracle, args.probe, fn, fields, case)
                except (OracleError, RuntimeError) as ex:
                    bad = [f"{type(ex).__name__}: {ex}"]
                if bad:
                    bad_cases += 1
                    print(f"  fail {fn}[{i}] {describe(case)}")
                    for line in bad:
                        print(f"        {line}")
                else:
                    print(f"  ok   {fn}[{i}] {describe(case)}")
            if bad_cases:
                failures += 1
                print(f"FAIL {fn}: {bad_cases}/{len(entries)} cases differ")
            else:
                print(f"PASS {fn}: {len(entries)} cases")

    print(f"\n{len(wanted) - failures}/{len(wanted)} routines clean")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
