"""Oracle-diff cases for poketcg/src/engine/menus/config.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DrawConfigMenuCursor": {
        "compare": ("a", "d", "e", "f"),
        "preserve": ("a", "d", "e", "f"),
    },
}

CASES = {
    "DrawConfigMenuCursor": [
        {"a": 0, "c": 0, "read": {0x9800 + 6 * 32 + 5: 1}},
        dict(POISON, a=0x5A, c=1, wram={0xD119: b"\x02"},
             read={0x9800 + 12 * 32 + 15: 1}),
        {"a": 0x33, "c": 0, "wram": {0xD118: b"\x01"},
         "read": {0x9800 + 6 * 32 + 7: 1}},
        {"a": 0x44, "c": 0, "wram": {0xD118: b"\x04"},
         "read": {0x9800 + 6 * 32 + 13: 1}},
        {"a": 0x66, "c": 1, "wram": {0xD119: b"\x00"},
         "read": {0x9800 + 12 * 32 + 1: 1}},
        {"a": 0x77, "c": 1, "wram": {0xD119: b"\x01"},
         "read": {0x9800 + 12 * 32 + 7: 1}},
        {"a": 0x88, "c": 1, "wram": {0xD119: b"\x02"},
         "read": {0x9800 + 12 * 32 + 15: 1}},
        {"a": 0x99, "c": 2, "read": {0x9800 + 16 * 32 + 1: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawConfigMenuCursor": {
        "source_symbol": "DrawConfigMenuCursor",
        "before": "x = (uint8_t)(5u + (uint8_t)(cursor << 1));",
        "after": "x = (uint8_t)(5u + (uint8_t)(cursor << 1) + 1u);",
        "case_ids": ["DrawConfigMenuCursor-2", "DrawConfigMenuCursor-3"],
    },
}
