#!/usr/bin/env python3
"""Compare one schema-2 function case through GBRT and the native probe."""

from __future__ import annotations
import argparse
import importlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path

REGISTERS = ("a", "f", "b", "c", "d", "e", "hl")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fn", required=True)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    args = parser.parse_args()
    if args.case.suffix == ".py":
        spec = importlib.util.spec_from_file_location("schema2_case", args.case)
        if spec is None or spec.loader is None:
            raise SystemExit("SCHEMA cannot load case module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = getattr(module, "SCHEMA2_CASES", {}).get(args.fn, [])
        if args.index < 0 or args.index >= len(records):
            raise SystemExit(f"SCHEMA case index {args.index} is out of range for {args.fn}")
        case = records[args.index]
    else:
        case = json.loads(args.case.read_text())
    if case.get("fn") != args.fn:
        raise SystemExit("SCHEMA case function does not match --fn")
    if case.get("completion") != "return" or not isinstance(case.get("registers"), dict):
        raise SystemExit("SCHEMA case requires completion=return and registers")
    if not args.rom.is_absolute() or not args.symbols.is_absolute():
        raise SystemExit("SCHEMA --rom and --symbols must be absolute paths")
    if not args.rom.is_file() or not args.symbols.is_file():
        raise SystemExit("ARTIFACT ROM or symbols path is unavailable")
    required = {
        "id", "fn", "entry", "completion", "instruction_budget", "cycle_budget",
        "mapper", "registers", "compare", "preserve", "bus", "sram", "vram",
        "setup", "input_events", "evidence",
    }
    if set(case) != required:
        raise SystemExit("SCHEMA case keys do not match schema-2")
    if set(case["registers"]) != set(REGISTERS):
        raise SystemExit("SCHEMA registers must declare exactly seven fields")
    if (not isinstance(case["compare"], list) or not isinstance(case["preserve"], list)
            or not case["compare"] or not set(case["preserve"]).issubset(case["compare"])
            or any(field not in REGISTERS for field in case["compare"] + case["preserve"])):
        raise SystemExit("SCHEMA compare/preserve contract is invalid")
    if case["evidence"] != "primary":
        raise SystemExit("SCHEMA comparator slice requires primary evidence")
    for name in ("entry", "instruction_budget", "cycle_budget"):
        value = case[name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise SystemExit(f"SCHEMA invalid positive integer {name}")
    if case["entry"] > 0xffff or case["instruction_budget"] > 0xffffffff or case["cycle_budget"] > 0xffffffff:
        raise SystemExit("SCHEMA numeric field out of range")
    if not isinstance(case["id"], str) or not case["id"]:
        raise SystemExit("SCHEMA id must be non-empty")
    if not all(isinstance(case[name], dict) for name in ("bus", "sram", "vram")):
        raise SystemExit("SCHEMA state sections must be objects")
    if not isinstance(case["setup"], list) or not isinstance(case["input_events"], list):
        raise SystemExit("SCHEMA setup and input_events must be arrays")
    if not isinstance(case["mapper"], dict) or set(case["mapper"]) != {
        "rom_bank", "ram_bank", "ram_enable"
    }:
        raise SystemExit("SCHEMA mapper must declare rom_bank, ram_bank, ram_enable")
    if any(case.get(name) for name in ("bus", "sram", "vram", "setup", "input_events")):
        raise SystemExit("SCHEMA non-register state is not supported by this runner slice")
    if args.fn not in args.symbols.read_text():
        raise SystemExit("ARTIFACT function is absent from symbols")
    registers = {name: int(case["registers"].get(name, 0)) for name in REGISTERS}
    env = os.environ.copy()
    env["POKETCG_ROM"] = str(args.rom.resolve())
    request = {
        "completion": "return",
        "entry": int(case["entry"]),
        "instruction_budget": int(case["instruction_budget"]),
        "cycle_budget": int(case["cycle_budget"]),
        "rom_bank": int(case["mapper"]["rom_bank"]),
        "ram_bank": int(case["mapper"]["ram_bank"]),
        "ram_enable": int(bool(case["mapper"]["ram_enable"])),
        **registers,
    }
    primary = subprocess.run(
        [str(args.runner), "--rom", str(args.rom.resolve())],
        input=json.dumps(request), text=True, capture_output=True, check=False,
        timeout=30, env=env,
    )
    if primary.returncode != 0:
        raise SystemExit(primary.stdout or primary.stderr)
    payload = next((line for line in reversed(primary.stdout.splitlines())
                    if line.startswith("{")), None)
    if payload is None:
        raise SystemExit("BACKEND missing JSON result")
    reference = json.loads(payload)
    if reference.get("status") != "REFERENCE_OK":
        raise SystemExit("BACKEND invalid completion result")
    pairs = {}
    for pair in ("af", "bc", "de"):
        value = reference.get(pair)
        if not isinstance(value, int) or not 0 <= value <= 0xffff:
            raise SystemExit(f"BACKEND missing or invalid {pair}")
        pairs[pair] = value
    hl = reference.get("hl")
    if not isinstance(hl, int) or not 0 <= hl <= 0xffff:
        raise SystemExit("BACKEND missing or invalid hl")
    reference.update({
        "a": pairs["af"] >> 8, "f": pairs["af"] & 0xff,
        "b": pairs["bc"] >> 8, "c": pairs["bc"] & 0xff,
        "d": pairs["de"] >> 8, "e": pairs["de"] & 0xff,
    })
    preservation = {
        name: (registers[name], reference.get(name))
        for name in case["preserve"]
        if reference.get(name) != registers[name]
    }
    if preservation:
        print(json.dumps({"status": "PORT", "fn": case["fn"],
                          "mismatches": {f"preserve:{name}": values
                                         for name, values in preservation.items()}}))
        return 1
    probe = subprocess.run(
        [str(args.probe)], input=json.dumps({"fn": case["fn"], **registers}),
        text=True, capture_output=True, check=False, timeout=30, env=env,
    )
    if probe.returncode != 0:
        raise SystemExit(probe.stderr)
    native = json.loads(probe.stdout)
    mismatches = {
        name: (reference.get(name), native.get(name))
        for name in case["compare"]
        if reference.get(name) != native.get(name)
    }
    if mismatches:
        print(json.dumps({"status": "PORT", "fn": case["fn"], "mismatches": mismatches}))
        return 1
    print(json.dumps({"status": "PASS", "fn": case["fn"], "registers": native}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
