"""Oracle-diff cases for the Pokemon Dome NPC preload helpers."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadNPCXPos = 0xD3AC
wLoadNPCYPos = 0xD3AD
wLoadNPCDirection = 0xD3AE

CONTRACT = {
    "PlacePokemonDomeOpponentAtDuelTable": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "b", "c", "d", "e", "hl"),
    },
    "Func_f762": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "b", "c", "d", "e", "hl"),
    },
    "Func_f782": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "PlacePokemonDomeOpponentAtDuelTable": [
        {"wram": {wLoadNPCXPos: b"\x00", wLoadNPCYPos: b"\x00", wLoadNPCDirection: b"\x00"},
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
        dict(POISON, f=0x00,
             wram={wLoadNPCXPos: b"\xaa", wLoadNPCYPos: b"\xbb", wLoadNPCDirection: b"\xcc"},
             read={wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}),
        {"f": 0x80, "wram": {wLoadNPCXPos: b"\xff", wLoadNPCYPos: b"\xff", wLoadNPCDirection: b"\xff"},
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
    ],
    "Func_f762": [
        {"wram": {wLoadNPCYPos: b"\x00"}, "read": {wLoadNPCYPos: 1}},
        dict(POISON, f=0x00, wram={wLoadNPCYPos: b"\xaa"}, read={wLoadNPCYPos: 1}),
        {"f": 0x80, "wram": {wLoadNPCYPos: b"\xff"}, "read": {wLoadNPCYPos: 1}},
    ],
    "Func_f782": [
        {"b": 0x00, "c": 0x00, "wram": {wLoadNPCXPos: b"\xff", wLoadNPCYPos: b"\xff"},
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1}},
        dict(POISON, f=0x00, b=0x12, c=0x34,
             wram={wLoadNPCXPos: b"\xaa", wLoadNPCYPos: b"\xbb"},
             read={wLoadNPCXPos: 1, wLoadNPCYPos: 1}),
        {"f": 0x80, "b": 0xFF, "c": 0xFE,
         "wram": {wLoadNPCXPos: b"\x00", wLoadNPCYPos: b"\x00"},
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "PlacePokemonDomeOpponentAtDuelTable": {
        "source_symbol": "PlacePokemonDomeOpponentAtDuelTable",
        "before": "wLoadNPCXPos = 0x12;",
        "after": "wLoadNPCXPos = 0x13;",
        "case_ids": ["PlacePokemonDomeOpponentAtDuelTable-0", "PlacePokemonDomeOpponentAtDuelTable-1", "PlacePokemonDomeOpponentAtDuelTable-2"],
    },
    "Func_f762": {
        "source_symbol": "Func_f762",
        "before": "wLoadNPCYPos = (uint8_t)(wLoadNPCYPos + 2u);",
        "after": "wLoadNPCYPos = (uint8_t)(wLoadNPCYPos + 3u);",
        "case_ids": ["Func_f762-0", "Func_f762-1", "Func_f762-2"],
    },
    "Func_f782": {
        "source_symbol": "Func_f782",
        "before": "wLoadNPCXPos = b;",
        "after": "wLoadNPCXPos = (uint8_t)(b + 1u);",
        "case_ids": ["Func_f782-0", "Func_f782-1", "Func_f782-2"],
    },
}
