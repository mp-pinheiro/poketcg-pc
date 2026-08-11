"""Oracle-diff cases for scripts/challenge_hall.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SB818 = 0xB818

CONTRACT = {
    "Func_f5db": ("b", "c", "d", "e", "hl"),
    "Func_f5e9": ("b", "c", "d", "e", "hl"),
    "Script_Host": ("a", "f", "b", "c", "d", "e", "hl"),
}

CASES = {
    "Func_f5db": [
        {"sram": {0: {SB818: b"\xA1\xB2\xC3\xD4"}}},
        dict(POISON, sram={0: {SB818: b"\x10\x20\x30\x40"}}),
        {"mapper": {"ram_bank": 2}, "sram": {2: {SB818: b"\xFF\xEE\xDD\xCC"}}},
    ],
    "Func_f5e9": [
        {"c": 0},
        {"c": 1},
        {"c": 7},
        {"c": 8},
        dict(POISON, c=0xFF),
    ],
    "Script_Host": [
        {"wram": {0xC100: b"\x5A"}, "read": {0xC100: 1}},
        dict(POISON, wram={0xC100: b"\xA5"}, read={0xC100: 1}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Func_f5db": {
        "source_symbol": "Func_f5db",
        "before": "gb_write8(sb818_ADDR, 0x00);",
        "after": "gb_write8(sb818_ADDR, 0xFF);",
        "case_ids": ["Func_f5db-0", "Func_f5db-1", "Func_f5db-2"],
    },
    "Func_f5e9": {
        "source_symbol": "Func_f5e9",
        "before": "uint8_t b = 0x80u;",
        "after": "uint8_t b = 0x40u;",
        "case_ids": ["Func_f5e9-0", "Func_f5e9-1", "Func_f5e9-2", "Func_f5e9-3", "Func_f5e9-4"],
    },
    "Script_Host": {
        "source_symbol": "Script_Host",
        "before": "void Script_Host(void)\n{\n}",
        "after": "void Script_Host(void)\n{\n\tgb_write8(0xC100, 0x01);\n}",
        "case_ids": ["Script_Host-0", "Script_Host-1"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
