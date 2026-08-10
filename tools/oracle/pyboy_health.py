#!/usr/bin/env python3
"""Validate the installed PyBoy path with a register-preserving ROM call."""

from __future__ import annotations
import importlib.metadata
import subprocess
import sys
from pathlib import Path

from pyboy_oracle import Oracle

ROOT = Path(__file__).resolve().parents[2]
ROM = ROOT / "poketcg" / "poketcg.gbc"
SYMBOLS = ROOT / "poketcg" / "poketcg.sym"


def main() -> int:
    identity = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "verify_oracle_artifacts.py"),
            "--root",
            str(ROOT),
            "--pyboy-identity",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if identity.stdout:
        print(identity.stdout, end="")
    if identity.returncode:
        if identity.stderr:
            print(identity.stderr, end="", file=sys.stderr)
        print("BACKEND_UNHEALTHY pyboy identity")
        return 2
    version = importlib.metadata.version("pyboy")
    with Oracle(ROM, SYMBOLS) as oracle:
        result = oracle.call("_ResetAnimationQueue", b=0xBB, c=0xCC, hl=0x1234)
    print(
        f"PYBOY version={version} python={sys.version_info.major}."
        f"{sys.version_info.minor}.{sys.version_info.micro}"
    )
    actual = (result.b << 8) | result.c
    if actual != 0xBBCC or result.hl != 0x1234:
        print(
            "BACKEND_QUARANTINED pyboy reason=POP_BC expected=BBCC "
            f"actual={actual:04X} hl={result.hl:04X}"
        )
        return 2
    print("BACKEND_HEALTHY pyboy POP_BC=BBCC HL=1234")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
