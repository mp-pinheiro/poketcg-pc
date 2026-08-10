#!/usr/bin/env python3
"""Generate the deterministic minimal ROM used for runner health checks."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rom = bytearray(0x8000)
    rom[0x100] = 0xC9
    args.output.write_bytes(rom)


if __name__ == "__main__":
    main()
