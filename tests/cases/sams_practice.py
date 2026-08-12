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

# >>> factory GetPlayAreaLocationOfRaticateOrRattata
CONTRACT["GetPlayAreaLocationOfRaticateOrRattata"] = {"compare": (), "preserve": ()}
CASES["GetPlayAreaLocationOfRaticateOrRattata"] = [
    # found via RATICATE search, not on the very first bench slot scanned
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\x01", 0xC2BD: b"\x00", 0xC2BE: b"\xFF",
              0xC2BF: b"\xFF", 0xC2C0: b"\xFF",
              0xC400: b"\xA8", 0xC401: b"\xA3"},
     "read": {0xFF9D: 1}},
    # RATICATE absent (empty slot after two real cards); RATTATA found on the
    # second bench slot during the fallback search
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\x00", 0xC2BD: b"\x01", 0xC2BE: b"\xFF",
              0xC400: b"\xA3", 0xC401: b"\xA7"},
     "read": {0xFF9D: 1}},
    # neither card present; both searches end via the empty bench1 slot
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\x00", 0xC2BD: b"\xFF",
              0xC400: b"\xA3"},
     "read": {0xFF9D: 1}},
    # bench is completely full with no match and no empty slot: the search
    # loop exhausts (b reaches MAX_PLAY_AREA_POKEMON) and the caller's
    # `cp $ff` test misses it, so it is reported as "found" at location 6
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\x00", 0xC2BD: b"\x00", 0xC2BE: b"\x00",
              0xC2BF: b"\x00", 0xC2C0: b"\x00",
              0xC400: b"\xA3"},
     "read": {0xFF9D: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BC: b"\x01", 0xC2BD: b"\x00",
                        0xC2BE: b"\xFF", 0xC2BF: b"\xFF", 0xC2C0: b"\xFF",
                        0xC400: b"\xA8", 0xC401: b"\xA3"},
         read={0xFF9D: 1}),
]
# <<< factory GetPlayAreaLocationOfRaticateOrRattata

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
# >>> factory-mutation GetPlayAreaLocationOfRaticateOrRattata
MUTATIONS["GetPlayAreaLocationOfRaticateOrRattata"] = {
    "source_symbol": "GetPlayAreaLocationOfRaticateOrRattata",
    "before": "	hTempPlayAreaLocation_ff9d = PLAY_AREA_BENCH_1;",
    "after": "	hTempPlayAreaLocation_ff9d = 0u;",
    "case_ids": ["GetPlayAreaLocationOfRaticateOrRattata-2"],
}
# <<< factory-mutation GetPlayAreaLocationOfRaticateOrRattata
