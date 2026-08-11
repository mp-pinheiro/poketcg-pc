HRAM_KEYS_HELD = 0xFF90
HRAM_KEYS_PRESSED = 0xFF91

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "WaitUntilKeysArePressed": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "WaitUntilKeysArePressed": [
        {"a": 0x01, "keys": 0x01,
         "setup": [{"fn": "DisableLCD"}],
         "wram": {HRAM_KEYS_HELD: b"\x01", HRAM_KEYS_PRESSED: b"\x01"},
         "read": {HRAM_KEYS_PRESSED: 1}},
        dict(POISON, a=0x01, keys=0x01,
             setup=[{"fn": "DisableLCD"}],
             wram={HRAM_KEYS_HELD: b"\x01", HRAM_KEYS_PRESSED: b"\x01"},
             read={HRAM_KEYS_PRESSED: 1}),
        {"a": 0x80, "keys": 0x80,
         "setup": [{"fn": "DisableLCD"}],
         "wram": {HRAM_KEYS_HELD: b"\x80", HRAM_KEYS_PRESSED: b"\x80"},
         "read": {HRAM_KEYS_PRESSED: 1}},
        {"a": 0xFF, "keys": 0xFF,
         "setup": [{"fn": "DisableLCD"}],
         "wram": {HRAM_KEYS_HELD: b"\xFF", HRAM_KEYS_PRESSED: b"\xFF"},
         "read": {HRAM_KEYS_PRESSED: 1}},
        {"a": 0x03, "keys": 0x03,
         "setup": [{"fn": "DisableLCD"}],
         "wram": {HRAM_KEYS_HELD: b"\x03", HRAM_KEYS_PRESSED: b"\x01"},
         "read": {HRAM_KEYS_PRESSED: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)


MUTATIONS = {
    "WaitUntilKeysArePressed": {
        "source_symbol": "WaitUntilKeysArePressed",
        "before": "if (pressed != 0)",
        "after": "if (pressed == 0)",
        "case_ids": ["WaitUntilKeysArePressed-0", "WaitUntilKeysArePressed-1",
                      "WaitUntilKeysArePressed-2", "WaitUntilKeysArePressed-3",
                      "WaitUntilKeysArePressed-4"],
    },
}