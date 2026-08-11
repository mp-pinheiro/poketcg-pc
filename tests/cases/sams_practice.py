POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
hTempCardIndex_ff98 = 0xFF98
wDuelTempList = 0xC510
wDuelTurns = 0xCC06
wDuelInitialPrizes = 0xCC08
wPlayerDeck = 0xC27E
wPlayerHand = 0xC242
wPlayerHandCount = 0xC2EE
wPlayerLocations = 0xC200

CONTRACT = {
    "IsAIPracticeScriptedTurn": {
        "compare": ("a", "f"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "SetSamsStartingPlayArea": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": (),
    },
}

CASES = {
    "IsAIPracticeScriptedTurn": [
        {"wram": {wDuelTurns: b"\x00"}},
        {"wram": {wDuelTurns: b"\x0d"}},
        {"wram": {wDuelTurns: b"\x0e"}},
        {"wram": {wDuelTurns: b"\x0f"}},
        dict(POISON, wram={wDuelTurns: b"\xff"}),
    ],
    "SetSamsStartingPlayArea": [
        {"c": 0, "wram": {hWhoseTurn: b"\xc2", wPlayerHandCount: b"\x00"},
         "read": {wDuelTempList: 1, wDuelInitialPrizes: 1}},
        {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
         "wram": {hWhoseTurn: b"\xc2", wPlayerHandCount: b"\x01",
                  wPlayerHand: b"\x00", wPlayerLocations: b"\x00",
                  wPlayerDeck: b"\x08"},
         "read": {wDuelTempList: 2, 0xC2EF: 1, wDuelInitialPrizes: 1}},
        dict(POISON, c=0, wram={hWhoseTurn: b"\xc2", wPlayerHandCount: b"\x01",
                                wPlayerHand: b"\x00", wPlayerLocations: b"\x00",
                                wPlayerDeck: b"\x00"},
             read={wDuelTempList: 2, wDuelInitialPrizes: 1}),
    ],
}

MUTATIONS = {
    "IsAIPracticeScriptedTurn": {
        "source_symbol": "IsAIPracticeScriptedTurn",
        "before": "uint8_t a = (uint8_t)(wDuelTurns >> 1);",
        "after": "uint8_t a = (uint8_t)(wDuelTurns >> 2);",
        "case_ids": ["IsAIPracticeScriptedTurn-0", "IsAIPracticeScriptedTurn-1",
                     "IsAIPracticeScriptedTurn-2", "IsAIPracticeScriptedTurn-3",
                     "IsAIPracticeScriptedTurn-4"],
    },
    "SetSamsStartingPlayArea": {
        "source_symbol": "SetSamsStartingPlayArea",
        "before": "if (a != MACHOP)",
        "after": "if (a == MACHOP)",
        "case_ids": ["SetSamsStartingPlayArea-0", "SetSamsStartingPlayArea-1",
                     "SetSamsStartingPlayArea-2"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
