"""Oracle-diff cases for poketcg/src/home/input.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ReadJoypad": {"compare": ("d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "SaveButtonsHeld": {"compare": ("b", "c", "d", "e", "f", "hl"), "preserve": ("b", "d", "e", "f", "hl")},
    "ClearJoypad": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "ReadJoypad": [
        {"wram": {0xFF8D: b"\x00\x00\x00\x00\x00"},
         "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\x12\x34\x56\x78\x9A"},
             read={0xFF8D: 5}),
        {"keys": 0x01, "wram": {0xFF8D: b"\x00\x00\x00\x00\x00"},
         "read": {0xFF8D: 5}},
    ],
    "SaveButtonsHeld": [
        {"c": 0x00, "read": {0xFF90: 1}},
        dict(POISON, c=0xA5, read={0xFF90: 1}),
    ],
    "ClearJoypad": [
        {"wram": {0xFF8D: b"\x01\x02\x03\x04\x05"},
         "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\x01\x02\x03\x04\x05"},
             read={0xFF8D: 5}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SaveButtonsHeld": {
        "source_symbol": "SaveButtonsHeld",
        "before": "gb_write8(JOYP, JOYP_GET_NONE);",
        "after": "gb_write8(JOYP, JOYP_GET_CTRL_PAD);",
        "case_ids": ["SaveButtonsHeld-0", "SaveButtonsHeld-1"],
    },
}
