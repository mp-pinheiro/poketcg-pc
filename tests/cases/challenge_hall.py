"""Oracle-diff cases for poketcg/src/scripts/challenge_hall.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

FLAGS = 0xD698

CONTRACT = {
    "Func_f5db": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "Func_f5e9": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("c", "d", "e"),
    },
    "Script_Host": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Func_f5db": [
        {"wram": {FLAGS: b"\x11\x22\x33\x44"}, "read": {FLAGS: 4}},
        dict(POISON, wram={FLAGS: b"\xFF\xFF\xFF\xFF"}, read={FLAGS: 4}),
    ],
    "Func_f5e9": [
        {"c": 0},
        {"c": 1},
        {"c": 7},
        {"c": 8},
        dict(POISON, c=0xFF),
    ],
    "Script_Host": [
        {"wram": {FLAGS: b"\xFF\xFF\xFF\xFF"}, "read": {FLAGS: 4}},
        dict(POISON, wram={FLAGS: b"\xFF\xFF\xFF\xFF"}, read={FLAGS: 4}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Func_f5db": {
        "source_symbol": "Func_f5db",
        "before": "gb_write8(wd698_ADDR + 3u, 0);",
        "after": "gb_write8(wd698_ADDR + 3u, 1);",
        "case_ids": ["Func_f5db-0", "Func_f5db-1"],
    },
    "Func_f5e9": {
        "source_symbol": "Func_f5e9",
        "before": "uint8_t b = (uint8_t)(0x80u >> (c & 7u));",
        "after": "uint8_t b = (uint8_t)(0x80u >> ((c + 1u) & 7u));",
        "case_ids": ["Func_f5e9-0", "Func_f5e9-1", "Func_f5e9-2", "Func_f5e9-3", "Func_f5e9-4"],
    },
    "Script_Host": {
        "source_symbol": "Script_Host",
        "before": "void Script_Host(void)\n{\n}",
        "after": "void Script_Host(void)\n{\n\tFunc_f5db();\n}",
        "case_ids": ["Script_Host-0", "Script_Host-1"],
    },
}
