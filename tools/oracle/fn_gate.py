#!/usr/bin/env python3
"""Inventory the fixed function barrier without routing through PyBoy."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from routines import ALL, ROUTINES  # noqa: E402


def main() -> int:
    groups = len(ROUTINES)
    routines = len(ALL)
    print(f"INVENTORY groups={groups} routines={routines} probe=build-barrier/poketcg_probe")
    print("SCHEMA primary GBRT case driver is not integrated with legacy fixtures")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
