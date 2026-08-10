#!/usr/bin/env python3
"""Oracle diff driver: PyBoy references and the native probe."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, TYPE_CHECKING


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "oracle"))
sys.path.insert(0, str(ROOT / "tests"))

from routines import ALL, ROUTINES  # noqa: E402
CACHE_SEMANTICS = 1
REGS = ("a", "f", "b", "c", "d", "e", "hl")
CACHE_SCHEMA = 1


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
        for name, contract in getattr(mod, "CONTRACT", {}).items():
            if name in contracts:
                raise SystemExit(f"duplicate CONTRACT entry for {name}")
            fields = contract["compare"] if isinstance(contract, dict) else contract
            contracts[name] = tuple(fields)
    return cases, contracts


def run_probe(probe: Path, fn: str, case: dict, reads: dict[int, int],
              sreads: dict[int, dict[int, int]] | None = None,
              vreads: dict[int, dict[int, int]] | None = None) -> dict:
    req: dict[str, Any] = {"fn": fn}
    for r in REGS:
        req[r] = int(case.get(r, 0))
    req["wram"] = {str(addr): bytes(data).hex() for addr, data in case.get("wram", {}).items()}
    req["read"] = {str(addr): n for addr, n in reads.items()}
    if case.get("sram"):
        req["sram"] = {str(b): {str(a): bytes(d).hex() for a, d in sp.items()}
                        for b, sp in case["sram"].items()}
    if sreads:
        req["sread"] = {str(bank): {str(addr): n for addr, n in spans.items()}
                         for bank, spans in sreads.items()}
    if vreads:
        req["vread"] = {str(bank): {str(addr): n for addr, n in spans.items()}
                         for bank, spans in vreads.items()}
    if case.get("ramg") is not None:
        req["ramg"] = 1 if case["ramg"] else 0
    if case.get("setup"):
        req["setup"] = [{k: int(v) if k != "fn" else v for k, v in pre.items()}
                        for pre in case["setup"]]
    if case.get("keys"):
        req["keys"] = int(case["keys"])
    try:
        out = subprocess.run(
            [str(probe)],
            input=json.dumps(req),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("probe timed out after 30 seconds") from exc
    if out.returncode != 0:
        raise RuntimeError(f"probe failed ({out.returncode}): {out.stderr.strip()}")
    try:
        result = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"probe emitted non-JSON: {out.stdout!r} {out.stderr.strip()}")
    if "error" in result:
        raise RuntimeError(f"probe error: {result['error']}")
    return result


def merged_spans(case: dict) -> tuple[dict[int, int], dict[int, dict[int, int]], dict[int, dict[int, int]]]:
    reads = {addr: len(data) for addr, data in case.get("wram", {}).items()}
    reads.update({int(addr): int(n) for addr, n in case.get("read", {}).items()})
    sreads: dict[int, dict[int, int]] = {}
    for bank, spans in case.get("sread", {}).items():
        sreads.setdefault(int(bank), {}).update({int(addr): int(n) for addr, n in spans.items()})
    for bank, spans in case.get("sram", {}).items():
        sreads.setdefault(int(bank), {}).update({int(addr): len(data) for addr, data in spans.items()})
    vreads: dict[int, dict[int, int]] = {}
    for bank, spans in case.get("vread", {}).items():
        vreads.setdefault(int(bank), {}).update({int(addr): int(n) for addr, n in spans.items()})
    return (dict(sorted(reads.items())),
            {bank: dict(sorted(spans.items())) for bank, spans in sorted(sreads.items())},
            {bank: dict(sorted(spans.items())) for bank, spans in sorted(vreads.items())})


def compare_observables(ref: dict[str, Any], got: dict, fields: tuple[str, ...],
                        reads: dict[int, int], sreads: dict[int, dict[int, int]],
                        vreads: dict[int, dict[int, int]], prefix: str) -> list[str]:
    bad: list[str] = []
    for field in fields:
        if ref["registers"][field] != got[field]:
            width = 4 if field == "hl" else 2
            bad.append(f"{field}: {prefix} ${ref['registers'][field]:0{width}X} != C ${got[field]:0{width}X}")
    for addr, n in sorted(reads.items()):
        want = bytes.fromhex(ref["wram"][str(addr)])
        have = bytes.fromhex(got["wram"][str(addr)])
        if want != have:
            bad.append(f"${addr:04X}: {prefix} {want.hex()} != C {have.hex()}")
    for bank in sorted(sreads):
        for addr in sorted(sreads[bank]):
            want = bytes.fromhex(ref["sram"][str(bank)][str(addr)])
            have = bytes.fromhex(got["sram"][str(bank)][str(addr)])
            if want != have:
                bad.append(f"sram{bank}:${addr:04X}: {prefix} {want.hex()} != C {have.hex()}")
    for bank in sorted(vreads):
        for addr in sorted(vreads[bank]):
            want = bytes.fromhex(ref["vram"][str(bank)][str(addr)])
            have = bytes.fromhex(got["vram"][str(bank)][str(addr)])
            if want != have:
                bad.append(f"vram{bank}:${addr:04X}: {prefix} {want.hex()} != C {have.hex()}")
    return bad


def direct_case(oracle: Oracle, probe: Path, fn: str, fields: tuple[str, ...], case: dict) -> list[str]:
    if not case.get("oracle", True):
        if not case.get("why"):
            return ["oracle=False case must carry a `why` string"]
        expect = case.get("expect") or {}
        expect_regs = case.get("expect_regs") or {}
        expect_sram = case.get("expect_sram") or {}
        expect_vram = case.get("expect_vram") or {}
        if not (expect or expect_regs or expect_sram or expect_vram):
            return ["oracle=False case must carry a derived expectation"]
        reads, sreads, vreads = merged_spans(case)
        reads.update({int(a): len(v) for a, v in expect.items()})
        sreads.update({int(b): {int(a): len(v) for a, v in spans.items()} for b, spans in expect_sram.items()})
        vreads.update({int(b): {int(a): len(v) for a, v in spans.items()} for b, spans in expect_vram.items()})
        got = run_probe(probe, fn, case, reads, sreads, vreads)
        bad: list[str] = []
        for addr, want in expect.items():
            have = bytes.fromhex(got["wram"][str(addr)])
            if bytes(want) != have:
                bad.append(f"${addr:04X}: asm expects {bytes(want).hex()} != C {have.hex()}")
        for field, want in expect_regs.items():
            if want != got[field]:
                width = 4 if field == "hl" else 2
                bad.append(f"{field}: asm expects ${want:0{width}X} != C ${got[field]:0{width}X}")
        for bank, spans in expect_sram.items():
            for addr, want in spans.items():
                have = bytes.fromhex(got["sram"][str(bank)][str(addr)])
                if bytes(want) != have:
                    bad.append(f"sram{bank}:${addr:04X}: asm expects {bytes(want).hex()} != C {have.hex()}")
        for bank, spans in expect_vram.items():
            for addr, want in spans.items():
                have = bytes.fromhex(got["vram"][str(bank)][str(addr)])
                if bytes(want) != have:
                    bad.append(f"vram{bank}:${addr:04X}: asm expects {bytes(want).hex()} != C {have.hex()}")
        return bad
    ref = oracle.call(fn, a=case.get("a", 0), f=case.get("f", 0), b=case.get("b", 0),
                      c=case.get("c", 0), d=case.get("d", 0), e=case.get("e", 0),
                      hl=case.get("hl", 0), wram=case.get("wram"), sram=case.get("sram"),
                      ramg=case.get("ramg"), setup=case.get("setup"), keys=case.get("keys", 0))
    reads, sreads, vreads = merged_spans(case)
    got = run_probe(probe, fn, case, reads, sreads, vreads)
    reference = {"registers": {field: getattr(ref, field) for field in fields},
                 "wram": {str(addr): ref.mem(addr, n).hex() for addr, n in reads.items()},
                 "sram": {str(bank): {str(addr): ref.mem(addr, n, bank=bank).hex() for addr, n in spans.items()}
                          for bank, spans in sreads.items()},
                 "vram": {str(bank): {str(addr): ref.mem(addr, n, bank=bank).hex() for addr, n in spans.items()}
                          for bank, spans in vreads.items()}}
    return compare_observables(reference, got, fields, reads, sreads, vreads, "oracle")


def normalize_case(case: dict, fn: str, fields: tuple[str, ...], dependencies: dict[str, str], rom: Path) -> dict:
    def byte_map(mapping: dict) -> list[list[Any]]:
        return [[int(addr), bytes(data).hex()] for addr, data in sorted(mapping.items(), key=lambda x: int(x[0]))]
    def span_map(mapping: dict) -> list[list[Any]]:
        return [[int(bank), int(addr), int(n)] for bank, spans in sorted(mapping.items(), key=lambda x: int(x[0]))
                for addr, n in sorted(spans.items(), key=lambda x: int(x[0]))]
    setup = []
    for pre in case.get("setup", []):
        setup.append({"fn": pre["fn"], **{r: int(pre.get(r, 0)) for r in REGS}})
    reads, sreads, vreads = merged_spans(case)
    return {"semantic": CACHE_SEMANTICS, "dependencies": dependencies, "fn": fn,
            "contract": list(fields), "registers": {r: int(case.get(r, 0)) for r in REGS},
            "seeds": {"wram": byte_map(case.get("wram", {})),
                      "sram": [[int(bank), int(addr), bytes(data).hex()] for bank, spans in sorted(case.get("sram", {}).items(), key=lambda x: int(x[0]))
                               for addr, data in sorted(spans.items(), key=lambda x: int(x[0]))]},
            "ramg": None if case.get("ramg") is None else bool(case["ramg"]), "setup": setup,
            "keys": int(case.get("keys", 0)), "wram": [[int(a), int(n)] for a, n in sorted(reads.items())],
            "sread": span_map(sreads), "vread": span_map(vreads)}


def dependencies(rom: Path) -> dict[str, str]:
    files = {"rom": rom, "sym": rom.with_suffix(".sym"), "harness": Path(__file__),
             "oracle": ROOT / "tools" / "oracle" / "pyboy_oracle.py"}
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in files.items()} | {
        "pyboy": importlib.metadata.version("pyboy")}


def cache_reference(cache_dir: Path, key: str, fn: str, fields: tuple[str, ...], reference: dict) -> dict:
    entry = {"schema": CACHE_SCHEMA, "key": key, "fn": fn, "contract": list(fields),
             "registers": reference["registers"], "wram": [[int(a), v] for a, v in sorted(reference["wram"].items(), key=lambda x: int(x[0]))],
             "sram": [[int(b), int(a), v] for b, spans in sorted(reference["sram"].items(), key=lambda x: int(x[0])) for a, v in sorted(spans.items(), key=lambda x: int(x[0]))],
             "vram": [[int(b), int(a), v] for b, spans in sorted(reference["vram"].items(), key=lambda x: int(x[0])) for a, v in sorted(spans.items(), key=lambda x: int(x[0]))]}
    cache_dir.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{key}.", suffix=".tmp", dir=cache_dir)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(entry, stream, sort_keys=True, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, cache_dir / f"{key}.json")
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return entry


def load_reference(cache_dir: Path, key: str, fn: str, fields: tuple[str, ...], normalized: dict,
                   case_index: int, warm_hint: str) -> dict:
    miss = f"cache miss for {fn}[{case_index}]; run {warm_hint}"
    path = cache_dir / f"{key}.json"
    try:
        entry = json.loads(path.read_text())
        if not isinstance(entry, dict):
            raise ValueError
        required = {"schema", "key", "fn", "contract", "registers", "wram", "sram", "vram"}
        if set(entry) != required:
            raise ValueError
        if (entry.get("schema") != CACHE_SCHEMA or entry.get("key") != key
                or entry.get("fn") != fn or entry.get("contract") != list(fields)):
            raise ValueError
        if not isinstance(entry["registers"], dict) or set(entry["registers"]) != set(fields):
            raise ValueError
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 or v > 0xFFFF
               for v in entry["registers"].values()):
            raise ValueError

        def decode(rows: Any, arity: int) -> list[list[Any]]:
            if not isinstance(rows, list):
                raise ValueError
            out = []
            for row in rows:
                if (not isinstance(row, list) or len(row) != arity
                        or any(not isinstance(v, int) or v < 0 for v in row[:-1])
                        or not isinstance(row[-1], str)
                        or row[-1] != row[-1].lower()):
                    raise ValueError
                bytes.fromhex(row[-1])
                out.append(row)
            if out != sorted(out, key=lambda row: tuple(row[:-1])):
                raise ValueError
            return out

        wram = decode(entry["wram"], 2)
        sram = decode(entry["sram"], 3)
        expected_wram = [(a, n) for a, n in normalized["wram"]]
        expected_sram = sorted((b, a, n) for b, a, n in normalized["sread"])
        expected_vram = sorted((b, a, n) for b, a, n in normalized["vread"])
        vram = decode(entry["vram"], 3)
        actual_wram = [(a, len(bytes.fromhex(data))) for a, data in wram]
        actual_sram = [(b, a, len(bytes.fromhex(data))) for b, a, data in sram]
        actual_vram = [(b, a, len(bytes.fromhex(data))) for b, a, data in vram]
        if actual_wram != expected_wram or actual_sram != expected_sram or actual_vram != expected_vram:
            raise ValueError
        return {"registers": entry["registers"], "wram": {str(a): data for a, data in wram},
                "sram": {str(b): {str(a): data for bb, a, data in sram if bb == b}
                         for b in sorted({b for b, _, _ in sram})},
                "vram": {str(b): {str(a): data for bb, a, data in vram if bb == b}
                         for b in sorted({b for b, _, _ in vram})}}
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise RuntimeError(miss)


def describe(case: dict) -> str:
    regs = " ".join(f"{r}=${case[r]:X}" for r in REGS if case.get(r))
    mem = " ".join(f"${a:04X}={bytes(d).hex()}" for a, d in case.get("wram", {}).items())
    sram = " ".join(f"sram{b}:${a:04X}={bytes(d).hex()}" for b, sp in case.get("sram", {}).items() for a, d in sp.items())
    sread = " ".join(f"sread{b}:${a:04X}+{n}" for b, sp in case.get("sread", {}).items() for a, n in sp.items())
    latch = "" if case.get("ramg") is None else f"ramg={int(bool(case['ramg']))}"
    keys = f"keys=${case['keys']:02X}" if case.get("keys") else ""
    tag = "" if case.get("oracle", True) else "[c-only] "
    return tag + (" ".join(x for x in (regs, mem, sram, sread, latch, keys) if x) or "all-zero")


def main() -> int:
    ap = argparse.ArgumentParser()
    selectors = ap.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--fn", action="append", help="routine to diff (repeatable)")
    selectors.add_argument("--group", action="append", help="routine basename group (repeatable)")
    selectors.add_argument("--all", action="store_true", help="diff every routine")
    ap.add_argument("--oracle-mode", choices=("live", "refresh", "cache"), default="live")
    ap.add_argument("--cache-dir", type=Path)
    ap.add_argument("--probe", type=Path, default=ROOT / "build" / "poketcg_probe")
    ap.add_argument("--rom", default=os.environ.get("POKETCG_ROM", str(ROOT / "poketcg" / "poketcg.gbc")))
    args = ap.parse_args()
    if args.oracle_mode in ("refresh", "cache") and args.cache_dir is None:
        ap.error("--cache-dir is required for refresh and cache modes")
    if not args.probe.exists():
        raise SystemExit(f"{args.probe} not built; run `just build`")
    os.environ.setdefault("POKETCG_ROM", args.rom)
    cases, contracts = load_cases()
    if args.fn:
        wanted = list(dict.fromkeys(args.fn))
    elif args.group:
        wanted = []
        for group in args.group:
            if group not in ROUTINES:
                ap.error(f"unknown group {group}")
            wanted.extend(ROUTINES[group])
        wanted = list(dict.fromkeys(wanted))
    else:
        wanted = list(ALL)
    if args.group:
        warm_hint = "just oracle-warm-group " + args.group[0]
    else:
        warm_hint = "just oracle-warm {fn}"
    oracle = None
    if args.oracle_mode in ("live", "refresh"):
        from pyboy_oracle import Oracle, OracleError
        oracle = Oracle(args.rom)
    failures = 0
    try:
        deps = dependencies(Path(args.rom)) if args.oracle_mode in ("refresh", "cache") else None
        for fn in wanted:
            entries = cases.get(fn)
            if not entries:
                print(f"FAIL {fn}: no cases"); failures += 1; continue
            fields = contracts.get(fn)
            if fields is None:
                print(f"FAIL {fn}: no CONTRACT entry naming the fields to diff"); failures += 1; continue
            bad_cases = 0
            for i, case in enumerate(entries):
                try:
                    if not case.get("oracle", True):
                        bad = direct_case(oracle, args.probe, fn, fields, case)
                    elif args.oracle_mode == "cache":
                        normalized = normalize_case(case, fn, fields, deps, Path(args.rom))
                        payload = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
                        key = hashlib.sha256(payload).hexdigest()
                        ref = load_reference(args.cache_dir, key, fn, fields, normalized, i, warm_hint.format(fn=fn))
                        reads, sreads, vreads = merged_spans(case)
                        bad = compare_observables(ref, run_probe(args.probe, fn, case, reads, sreads, vreads), fields, reads, sreads, vreads, "cache")
                    else:
                        if args.oracle_mode == "refresh":
                            normalized = normalize_case(case, fn, fields, deps, Path(args.rom))
                            payload = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
                            key = hashlib.sha256(payload).hexdigest()
                            ref = None
                            result = oracle.call(fn, a=case.get("a", 0), f=case.get("f", 0), b=case.get("b", 0), c=case.get("c", 0), d=case.get("d", 0), e=case.get("e", 0), hl=case.get("hl", 0), wram=case.get("wram"), sram=case.get("sram"), ramg=case.get("ramg"), setup=case.get("setup"), keys=case.get("keys", 0))
                            reads, sreads, vreads = merged_spans(case)
                            ref = {"registers": {field: getattr(result, field) for field in fields}, "wram": {str(a): result.mem(a, n).hex() for a, n in reads.items()}, "sram": {str(b): {str(a): result.mem(a, n, bank=b).hex() for a, n in spans.items()} for b, spans in sreads.items()}, "vram": {str(b): {str(a): result.mem(a, n, bank=b).hex() for a, n in spans.items()} for b, spans in vreads.items()}}
                            cache_reference(args.cache_dir, key, fn, fields, ref)
                            bad = compare_observables(ref, run_probe(args.probe, fn, case, reads, sreads, vreads), fields, reads, sreads, vreads, "oracle")
                        else:
                            bad = direct_case(oracle, args.probe, fn, fields, case)
                except Exception as ex:
                    bad = [f"{type(ex).__name__}: {ex}"]
                if bad:
                    bad_cases += 1; print(f"  fail {fn}[{i}] {describe(case)}"); [print(f"        {line}") for line in bad]
                else:
                    print(f"  ok   {fn}[{i}] {describe(case)}")
            if bad_cases:
                failures += 1; print(f"FAIL {fn}: {bad_cases}/{len(entries)} cases differ")
            else:
                print(f"PASS {fn}: {len(entries)} cases")
    finally:
        if oracle is not None:
            oracle.close()
    print(f"\n{len(wanted) - failures}/{len(wanted)} routines clean")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
