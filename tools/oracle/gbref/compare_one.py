#!/usr/bin/env python3
"""Compare one schema-2 function case through GBRT and the native probe."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REGISTERS = ("a", "f", "b", "c", "d", "e", "hl")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    args = parser.parse_args()
    case = json.loads(args.case.read_text())
    if case.get("completion") != "return" or not isinstance(case.get("registers"), dict):
        raise SystemExit("SCHEMA case requires completion=return and registers")
    if not args.rom.is_absolute() or not args.symbols.is_absolute():
        raise SystemExit("SCHEMA --rom and --symbols must be absolute paths")
    if not args.rom.is_file() or not args.symbols.is_file():
        raise SystemExit("ARTIFACT ROM or symbols path is unavailable")
    registers = {name: int(case["registers"].get(name, 0)) for name in REGISTERS}
    request = {
        "completion": "return",
        "entry": int(case["entry"]),
        "instruction_budget": int(case["instruction_budget"]),
        "cycle_budget": int(case["cycle_budget"]),
        **registers,
    }
    primary = subprocess.run(
        [str(args.runner), "--rom", str(args.rom.resolve())],
        input=json.dumps(request), text=True, capture_output=True, check=False,
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
    probe = subprocess.run(
        [str(args.probe)], input=json.dumps({"fn": case["fn"], **registers}),
        text=True, capture_output=True, check=False,
    )
    if probe.returncode != 0:
        raise SystemExit(probe.stderr)
    native = json.loads(probe.stdout)
    mismatches = {
        name: (reference.get(name), native.get(name))
        for name in REGISTERS
        if reference.get(name) != native.get(name)
    }
    if mismatches:
        print(json.dumps({"status": "PORT", "fn": case["fn"], "mismatches": mismatches}))
        return 1
    print(json.dumps({"status": "PASS", "fn": case["fn"], "registers": native}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
