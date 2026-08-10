"""Oracle-diff cases for ClearSavedDuel (engine/duel/core.asm:6183-6191)."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sCurrentDuelValid = 0xBC00
sCurrentDuelChecksum = 0xBC01
GUARD_LOW = 0xBBFF        # byte just below sCurrentDuelValid
GUARD_HIGH = 0xBC03       # sCurrentDuelType, the byte just past the checksum
hBankSRAM = 0xFF81

CONTRACT = {
    "ClearSavedDuel": {
        "compare": ("b", "c", "d", "e"),
        "preserve": ("b", "c", "d", "e"),
    },
}

CASES = {
    "ClearSavedDuel": [
        # All-zero baseline.
        {"sread": {0: {sCurrentDuelValid: 3}}},
        # Poisoned registers: none are consumed by the routine.
        dict(POISON,
             sram={0: {sCurrentDuelValid: b"\xaa\xbb\xcc"}}),
        # Guard bytes on both sides of the 3-byte target prove the clear is exactly
        # $BC00-$BC02 wide.
        {"sram": {0: {GUARD_LOW: b"\x11", sCurrentDuelValid: b"\xaa\xbb\xcc",
                      GUARD_HIGH: b"\x22"}}},
        {"sram": {0: {sCurrentDuelValid: b"\x44\x55\x66"},
                  2: {sCurrentDuelValid: b"\xaa\xbb\xcc"}}},
        {"sram": {0: {sCurrentDuelValid: b"\xaa\xbb\xcc"}}, "ramg": False},
    ],
}
from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "ClearSavedDuel": {
        "source_symbol": "ClearSavedDuel",
        "before": "gb_write8(sCurrentDuelValid_ADDR, 0x00);",
        "after": "gb_write8(sCurrentDuelValid_ADDR, 0xFF);",
        "case_ids": ["ClearSavedDuel-0", "ClearSavedDuel-1", "ClearSavedDuel-2", "ClearSavedDuel-3", "ClearSavedDuel-4"],
    },
}
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
