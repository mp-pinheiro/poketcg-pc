#!/usr/bin/env python3
"""Generate the deterministic ROM used by both oracle health lanes."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rom = bytearray(0x8000)
    # Register pair PUSH/POP, CALL/RET, and HRAM/WRAM reads and writes.
    program = bytes(
        (
            0x3E, 0x12,  # LD A,$12
            0x06, 0xBB,  # LD B,$BB
            0x0E, 0xCC,  # LD C,$CC
            0x16, 0xDD,  # LD D,$DD
            0x1E, 0xEE,  # LD E,$EE
            0x26, 0x12,  # LD H,$12
            0x2E, 0x34,  # LD L,$34
            0xF5, 0xC5, 0xD5, 0xE5,  # PUSH AF/BC/DE/HL
            0xE1, 0xD1, 0xC1, 0xF1,  # POP HL/DE/BC/AF
            0xCD, 0x50, 0x01,  # CALL $0150
            0x3E, 0x55,  # LD A,$55
            0xE0, 0x80,  # LDH [$FF80],A
            0xF0, 0x80,  # LDH A,[$FF80]
            0xEA, 0x00, 0xC0,  # LD [$C000],A
            0xFA, 0x00, 0xC0,  # LD A,[$C000]
            0xC9,  # RET
        )
    )
    rom[0x100 : 0x100 + len(program)] = program
    rom[0x150 : 0x152] = b"\x3e\x66"  # LD A,$66
    rom[0x152] = 0xC9
    args.output.write_bytes(rom)


if __name__ == "__main__":
    main()
