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

# >>> factory Func_f5cc
CONTRACT["Func_f5cc"] = {
    "compare": ("a", "f", "c", "d", "e"),
    "preserve": ("c", "d", "e"),
}
CASES["Func_f5cc"] = [
    {"c": 0, "wram": {FLAGS: b"\x00\x00\x00\x00"}},
    dict(POISON, c=0, wram={FLAGS: b"\x80\x00\x00\x00"}),
    {"c": 0, "wram": {FLAGS: b"\x80\x00\x00\x00"}},
    {"c": 7, "wram": {FLAGS: b"\x01\x00\x00\x00"}},
    {"c": 8, "wram": {FLAGS: b"\x00\x80\x00\x00"}},
    {"c": 31, "wram": {FLAGS: b"\x00\x00\x00\x01"}},
    dict(POISON, c=31, wram={FLAGS: b"\x00\x00\x00\x00"}),
]
# <<< factory Func_f5cc

# >>> factory Func_f5d4
CONTRACT["Func_f5d4"] = {
    "compare": ("a", "f", "c", "d", "e"),
    "preserve": ("c", "d", "e"),
}
CASES["Func_f5d4"] = [
    {"c": 0, "wram": {FLAGS: b"\x00\x00\x00\x00"}, "read": {FLAGS: 4}},
    dict(POISON, c=0, wram={FLAGS: b"\x7F\x00\x00\x00"}, read={FLAGS: 4}),
    {"c": 7, "wram": {FLAGS: b"\x00\x00\x00\x00"}, "read": {FLAGS: 4}},
    {"c": 8, "wram": {FLAGS: b"\x00\x00\x00\x00"}, "read": {FLAGS: 4}},
    {"c": 31, "wram": {FLAGS: b"\xFF\xFF\xFF\xFE"}, "read": {FLAGS: 4}},
    dict(POISON, c=31, wram={FLAGS: b"\x00\x00\x00\x00"}, read={FLAGS: 4}),
]
# <<< factory Func_f5d4

# >>> factory ChallengeHallAfterDuel
CONTRACT["ChallengeHallAfterDuel"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": (), "wram_out": True}
CASES["ChallengeHallAfterDuel"] = [
    {"wram": {0xD0C3: b"\x00", 0xD3AB: b"\x00"}, "read": {0xD3AB: 1}},
    dict(POISON, wram={0xD0C3: b"\x01", 0xD3AB: b"\x00"}, read={0xD3AB: 1}),
]
# <<< factory ChallengeHallAfterDuel

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
# >>> factory-mutation Func_f5cc
MUTATIONS["Func_f5cc"] = {
    "source_symbol": "Func_f5cc",
    "before": "uint8_t f = a ? 0x10u : 0xA0u;",
    "after": "uint8_t f = a ? 0xA0u : 0x10u;",
    "case_ids": ["Func_f5cc-0", "Func_f5cc-1", "Func_f5cc-2",
                  "Func_f5cc-3", "Func_f5cc-4", "Func_f5cc-5", "Func_f5cc-6"],
}
# <<< factory-mutation Func_f5cc
# >>> factory-mutation Func_f5d4
MUTATIONS["Func_f5d4"] = {
    "source_symbol": "Func_f5d4",
    "before": "uint8_t a = (uint8_t)(gb_read8(bit.hl) | bit.b);",
    "after": "uint8_t a = (uint8_t)(gb_read8(bit.hl) & bit.b);",
    "case_ids": ["Func_f5d4-0", "Func_f5d4-1", "Func_f5d4-2",
                  "Func_f5d4-3", "Func_f5d4-4", "Func_f5d4-5"],
}
# <<< factory-mutation Func_f5d4
# >>> factory-mutation ChallengeHallAfterDuel
MUTATIONS["ChallengeHallAfterDuel"] = {"source_symbol": "ChallengeHallAfterDuel", "before": "\tuint8_t c = (wDuelResult == DUEL_WIN) ? 0u : 2u;", "after": "\tuint8_t c = (wDuelResult == DUEL_WIN) ? 2u : 0u;", "case_ids": ["ChallengeHallAfterDuel-0", "ChallengeHallAfterDuel-1"]}
# <<< factory-mutation ChallengeHallAfterDuel
