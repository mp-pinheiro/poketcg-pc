from tests.cases._symbols import sym
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTempCardIndex = sym("hTempCardIndex_ff98")
hWhoseTurn = sym("hWhoseTurn")
wDuelTurns = sym("wDuelTurns")
wDuelInitialPrizes = sym("wDuelInitialPrizes")
wDuelTempList = sym("wDuelTempList")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
wPlayerDeck = sym("wPlayerDeck")
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
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerBench"): b"\x01", sym("wPlayerBench") + 1: b"\x00", sym("wPlayerBench") + 2: b"\xFF",
              sym("wPlayerBench") + 3: b"\xFF", sym("wPlayerBench") + 4: b"\xFF",
              sym("wBoosterCardsDrawn"): b"\xA8", sym("wBoosterCardsDrawn") + 1: b"\xA3"},
     "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    # RATICATE absent (empty slot after two real cards); RATTATA found on the
    # second bench slot during the fallback search
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench") + 1: b"\x01", sym("wPlayerBench") + 2: b"\xFF",
              sym("wBoosterCardsDrawn"): b"\xA3", sym("wBoosterCardsDrawn") + 1: b"\xA7"},
     "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    # neither card present; both searches end via the empty bench1 slot
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench") + 1: b"\xFF",
              sym("wBoosterCardsDrawn"): b"\xA3"},
     "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    # bench is completely full with no match and no empty slot: the search
    # loop exhausts (b reaches MAX_PLAY_AREA_POKEMON) and the caller's
    # `cp $ff` test misses it, so it is reported as "found" at location 6
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench") + 1: b"\x00", sym("wPlayerBench") + 2: b"\x00",
              sym("wPlayerBench") + 3: b"\x00", sym("wPlayerBench") + 4: b"\x00",
              sym("wBoosterCardsDrawn"): b"\xA3"},
     "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerBench"): b"\x01", sym("wPlayerBench") + 1: b"\x00",
                        sym("wPlayerBench") + 2: b"\xFF", sym("wPlayerBench") + 3: b"\xFF", sym("wPlayerBench") + 4: b"\xFF",
                        sym("wBoosterCardsDrawn"): b"\xA8", sym("wBoosterCardsDrawn") + 1: b"\xA3"},
         read={sym("hTempPlayAreaLocation_ff9d"): 1}),
]
# <<< factory GetPlayAreaLocationOfRaticateOrRattata

# >>> factory AIPerformScriptedTurn
CONTRACT["AIPerformScriptedTurn"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIPerformScriptedTurn"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000,
     "keys": [0x00, 0x01],
     "wram": {sym("wDuelTurns"): b"\x00", sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wPlayerNumberOfCardsInHand"): b"\x00",
              sym("wPlayerArenaCardSubstatus2"): b"\x05", sym("wSkipDuelistIsThinkingDelay"): b"\x01", sym("wLCDC"): b"\x00",
              sym("hTempList"): b"\x42"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {sym("hTempList"): 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000,
     "keys": [0x00, 0x01],
     "wram": {sym("wDuelTurns"): b"\x04", sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wPlayerNumberOfCardsInHand"): b"\x00",
              sym("wPlayerArenaCardSubstatus2"): b"\x05", sym("wSkipDuelistIsThinkingDelay"): b"\x01", sym("wLCDC"): b"\x00",
              sym("hTempList"): b"\x42", sym("hAIPkmnPowerEffectParam"): b"\x42"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {sym("hTempList"): 1, sym("hAIPkmnPowerEffectParam"): 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "keys": [0x00, 0x01],
     "wram": {sym("wDuelTurns"): b"\x04", sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wPlayerNumberOfCardsInHand"): b"\x00",
              sym("wPlayerArenaCardSubstatus2"): b"\x05", sym("wSkipDuelistIsThinkingDelay"): b"\x01", sym("wLCDC"): b"\x00",
              sym("hTempList"): b"\x42", sym("hAIPkmnPowerEffectParam"): b"\x42"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {sym("hTempList"): 1, sym("hAIPkmnPowerEffectParam"): 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory AIPerformScriptedTurn

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
# >>> factory-mutation AIPerformScriptedTurn
MUTATIONS["AIPerformScriptedTurn"] = {"source_symbol": "AIPerformScriptedTurn", "before": "\t\thTempPlayAreaLocation_ffa1 = found.a;", "after": "\t\thTempPlayAreaLocation_ffa1 = 0u;", "case_ids": ["AIPerformScriptedTurn-1"]}
# <<< factory-mutation AIPerformScriptedTurn
