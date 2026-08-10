#!/usr/bin/env python3
"""Generate the deterministic ROM used by both oracle health lanes."""

from __future__ import annotations

import argparse
from pathlib import Path

ENTRY = 0x0200
FIXED_MARKER_ADDRESS = 0x0150
FIXED_MARKER = 0xA5
TRACE_ADDRESS = 0xC000
TRACE_BYTES = bytes((FIXED_MARKER, 0x01, 0x00, 0x05, 0x05, 0x33, 0x44, 0xFF, 0x44))
ROM_BANK_COUNT = 64
ROM_BANK_SIZE = 0x4000
ROM_SIZE = ROM_BANK_COUNT * ROM_BANK_SIZE
SRAM_TRACE_ADDRESS = 0xA123
SRAM_BANK0_VALUE = 0x44
SRAM_BANK3_VALUE = 0x33
WRAM_HEALTH_ADDR = 0xC100
HELPER_ADDRESS = 0x0300
NESTED_HELPER_ADDRESS = 0x0310
_OPCODE_CYCLES = {
    0x01: 12,
    0x11: 12,
    0x21: 12,
    0x23: 8,
    0x3E: 8,
    0x77: 8,
    0xB7: 4,
    0xC1: 12,
    0xC5: 16,
    0xC9: 16,
    0xCD: 24,
    0xD1: 12,
    0xD5: 16,
    0xE1: 12,
    0xE5: 16,
    0xEA: 16,
    0xF1: 12,
    0xF5: 16,
    0xFA: 16,
}


def _instruction_cycles(data: bytes) -> int:
    if not data:
        raise ValueError("cannot emit an empty instruction")
    try:
        return _OPCODE_CYCLES[data[0]]
    except KeyError as exc:
        raise ValueError(f"unknown opcode: 0x{data[0]:02X}") from exc


def _build_helper_program() -> tuple[bytes, int, int]:
    code = bytearray()
    instructions = 0
    cycles = 0

    def emit(data: bytes) -> None:
        nonlocal instructions, cycles
        code.extend(data)
        instructions += 1
        cycles += _instruction_cycles(data)

    emit(bytes((0xCD, NESTED_HELPER_ADDRESS & 0xFF,
                NESTED_HELPER_ADDRESS >> 8)))
    emit(bytes((0xC9,)))
    return bytes(code), instructions, cycles


def _build_nested_helper_program() -> tuple[bytes, int, int]:
    code = bytearray()
    instructions = 0
    cycles = 0

    def emit(data: bytes) -> None:
        nonlocal instructions, cycles
        code.extend(data)
        instructions += 1
        cycles += _instruction_cycles(data)

    emit(_ld_a(0x99))
    emit(bytes((0xC9,)))
    return bytes(code), instructions, cycles




def _ld_a(value: int) -> bytes:
    return bytes((0x3E, value))


def _write_a(address: int) -> bytes:
    return bytes((0xEA, address & 0xFF, address >> 8))


def _read_a(address: int) -> bytes:
    return bytes((0xFA, address & 0xFF, address >> 8))


def _build_program() -> tuple[bytes, int, int]:
    code = bytearray()
    instructions = 0
    cycles = 0

    def emit(data: bytes) -> None:
        nonlocal instructions, cycles
        code.extend(data)
        instructions += 1
        cycles += _instruction_cycles(data)

    emit(bytes((0x21, TRACE_ADDRESS & 0xFF, TRACE_ADDRESS >> 8)))
    emit(_read_a(FIXED_MARKER_ADDRESS)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_read_a(0x4000)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x00)); emit(_write_a(0x2000))
    emit(_read_a(0x4000)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x45)); emit(_write_a(0x2000))
    emit(_read_a(0x4000)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x01)); emit(_write_a(0x3000))
    emit(_read_a(0x4000)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x0A)); emit(_write_a(0x0000))
    emit(_ld_a(0x03)); emit(_write_a(0x4000))
    emit(_ld_a(SRAM_BANK3_VALUE)); emit(_write_a(SRAM_TRACE_ADDRESS))
    emit(_ld_a(0x04)); emit(_write_a(0x4000))
    emit(_ld_a(SRAM_BANK0_VALUE)); emit(_write_a(SRAM_TRACE_ADDRESS))
    emit(_ld_a(0x03)); emit(_write_a(0x4000))
    emit(_read_a(SRAM_TRACE_ADDRESS)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x04)); emit(_write_a(0x4000))
    emit(_read_a(SRAM_TRACE_ADDRESS)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x1A)); emit(_write_a(0x0000))
    emit(_read_a(SRAM_TRACE_ADDRESS)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x55)); emit(_write_a(SRAM_TRACE_ADDRESS))
    emit(_ld_a(0x0A)); emit(_write_a(0x0000))
    emit(_ld_a(0x00)); emit(_write_a(0x4000))
    emit(_read_a(SRAM_TRACE_ADDRESS)); emit(bytes((0x77,))); emit(bytes((0x23,)))
    emit(_ld_a(0x00)); emit(_write_a(0x0000))

    emit(bytes((0x01, 0xCC, 0xBB)))
    emit(bytes((0x11, 0xEE, 0xDD)))
    emit(bytes((0x21, 0x34, 0x12)))
    emit(_ld_a(0x55)); emit(bytes((0xB7,)))
    emit(bytes((0xF5,))); emit(bytes((0xC5,)))
    emit(bytes((0xD5,))); emit(bytes((0xE5,)))
    emit(bytes((0xCD, HELPER_ADDRESS & 0xFF, HELPER_ADDRESS >> 8)))
    emit(bytes((0xE1,))); emit(bytes((0xD1,)))
    emit(bytes((0xC1,))); emit(bytes((0xF1,)))
    emit(_write_a(0xFF80))
    emit(_write_a(WRAM_HEALTH_ADDR))

    return bytes(code) + bytes((0xC9,)), instructions, cycles


def _install_helper(rom: bytearray) -> None:
    program_end = ENTRY + len(PROGRAM)
    helper_end = HELPER_ADDRESS + len(HELPER_PROGRAM)
    nested_end = NESTED_HELPER_ADDRESS + len(NESTED_HELPER_PROGRAM)
    if HELPER_ADDRESS < program_end or NESTED_HELPER_ADDRESS < program_end:
        raise ValueError("helper overlaps main program")
    if HELPER_ADDRESS <= FIXED_MARKER_ADDRESS < helper_end:
        raise ValueError("helper overlaps fixed marker")
    if NESTED_HELPER_ADDRESS <= FIXED_MARKER_ADDRESS < nested_end:
        raise ValueError("nested helper overlaps fixed marker")
    rom[HELPER_ADDRESS:helper_end] = HELPER_PROGRAM
    rom[NESTED_HELPER_ADDRESS:nested_end] = NESTED_HELPER_PROGRAM
HELPER_PROGRAM, HELPER_INSTRUCTION_COUNT, HELPER_CYCLE_COUNT = (
    _build_helper_program()
)
NESTED_HELPER_PROGRAM, NESTED_HELPER_INSTRUCTION_COUNT, NESTED_HELPER_CYCLE_COUNT = (
    _build_nested_helper_program()
)


PROGRAM, MAIN_INSTRUCTION_COUNT, MAIN_CYCLE_COUNT = _build_program()
INSTRUCTION_COUNT = (
    MAIN_INSTRUCTION_COUNT
    + HELPER_INSTRUCTION_COUNT
    + NESTED_HELPER_INSTRUCTION_COUNT
)
CYCLE_COUNT = MAIN_CYCLE_COUNT + HELPER_CYCLE_COUNT + NESTED_HELPER_CYCLE_COUNT
PRE_RET_PC = ENTRY + len(PROGRAM) - 1




def build_rom() -> bytes:
    rom = bytearray(ROM_SIZE)
    for bank in range(ROM_BANK_COUNT):
        start = bank * ROM_BANK_SIZE
        rom[start : start + ROM_BANK_SIZE] = bytes((bank,)) * ROM_BANK_SIZE
    rom[0x147] = 0x1B
    rom[0x148] = 0x05
    rom[0x149] = 0x03
    rom[0x14D] = (-sum(rom[0x134:0x14D]) - 25) & 0xFF
    rom[FIXED_MARKER_ADDRESS] = FIXED_MARKER
    rom[ENTRY : ENTRY + len(PROGRAM)] = PROGRAM
    _install_helper(rom)
    return bytes(rom)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_bytes(build_rom())


if __name__ == "__main__":
    main()
