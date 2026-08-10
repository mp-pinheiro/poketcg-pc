#!/usr/bin/env python3
"""Run the shared register, call, and memory conformance vector on GBRT."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from conformance_rom import main as build_rom

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/oracle/gbref/build/gbref_runner"


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        rom = Path(directory) / "conformance.gb"
        old_argv = sys.argv
        try:
            sys.argv = ["conformance_rom.py", str(rom)]
            build_rom()
        finally:
            sys.argv = old_argv
        request = {
            "completion": "return",
            "entry": 0x100,
            "instruction_budget": 100,
            "cycle_budget": 1000,
            "rom_bank": 1,
            "ram_bank": 0,
            "ram_enable": 0,
            "a": 0,
            "f": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "e": 0,
            "hl": 0,
        }
        result = subprocess.run(
            [str(RUNNER), "--rom", str(rom)],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        print("BACKEND_UNHEALTHY gbrt conformance process", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return 2
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("BACKEND_UNHEALTHY gbrt invalid result", file=sys.stderr)
        return 2
    expected = {"af": 0x5500, "bc": 0xBBCC, "de": 0xDDEE, "hl": 0x1234}
    actual = {key: payload.get(key) for key in expected}
    if payload.get("status") != "REFERENCE_OK" or actual != expected:
        print(f"BACKEND_UNHEALTHY gbrt conformance expected={expected} actual={actual}")
        return 2
    wram = bytes.fromhex(payload["wram"])
    hram = bytes.fromhex(payload["hram"])
    if wram[0] != 0x55 or hram[0] != 0x55:
        print("BACKEND_UNHEALTHY gbrt memory vector mismatch")
        return 2
    print("BACKEND_HEALTHY gbrt conformance=registers,calls,stack,wram,hram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
