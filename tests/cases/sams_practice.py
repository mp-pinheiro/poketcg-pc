POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTempCardIndex = 0xFF98
hWhoseTurn = 0xFF97
wDuelTurns = 0xCC06
wDuelInitialPrizes = 0xCC08
wDuelTempList = 0xC510
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
CONTRACT = {
    "IsAIPracticeScriptedTurn": {
        "compare": ("f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "SetSamsStartingPlayArea": {"compare": (), "preserve": ()},
}

CASES = {
    "IsAIPracticeScriptedTurn": [
        {"wram": {wDuelTurns: b"\x00"}},
        {"wram": {wDuelTurns: b"\x0E"}},
        {"wram": {wDuelTurns: b"\x0F"}},
        {"wram": {wDuelTurns: b"\x1C"}},
        dict(POISON, wram={wDuelTurns: b"\xFF"}),
    ],
    "SetSamsStartingPlayArea": [
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x00"},
         "read": {wDuelTempList: 1, hTempCardIndex: 1,
                  wPlayerDuelVariables: 240, wDuelInitialPrizes: 1}},
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x01",
                  wPlayerDuelVariables: b"\x00", wPlayerDeck: b"\x7D"},
         "read": {wDuelTempList: 2, hTempCardIndex: 1,
                  wPlayerDuelVariables: 240, wDuelInitialPrizes: 1}},
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x01",
                  wPlayerDuelVariables: b"\x00", wPlayerDeck: b"\x01"},
         "read": {wDuelTempList: 2, hTempCardIndex: 1,
                  wPlayerDuelVariables: 240, wDuelInitialPrizes: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           wPlayerDuelVariables + 0xEE: b"\x01",
                           wPlayerDuelVariables: b"\x00", wPlayerDeck: b"\x7D"},
             read={wDuelTempList: 2, hTempCardIndex: 1,
                   wPlayerDuelVariables: 240, wDuelInitialPrizes: 1}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SetSamsStartingPlayArea": {
        "source_symbol": "SetSamsStartingPlayArea",
        "before": "LoadCardDataToBuffer1_FromDeckIndex(a) == 0x7du",
        "after": "LoadCardDataToBuffer1_FromDeckIndex(a) == 0x7eu",
        "case_ids": ["SetSamsStartingPlayArea-1", "SetSamsStartingPlayArea-3"],
    },
    "IsAIPracticeScriptedTurn": {
        "source_symbol": "IsAIPracticeScriptedTurn",
        "before": "shifted >= 7 ? 0x10u : 0u",
        "after": "shifted >= 8 ? 0x10u : 0u",
        "case_ids": ["IsAIPracticeScriptedTurn-2"],
    },
}
