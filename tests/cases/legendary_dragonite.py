"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_dragonite.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wAlreadyPlayedEnergy = 0xCC0B
wPreviousAIFlags = 0xCE20
wAIBarrierFlagCounter = 0xCDA7
wPlayerHandCount = 0xC2EE
wOpponentHandCount = 0xC3EE
wPlayerArenaCard = 0xC2BB
wOpponentArenaCard = 0xC3BB
wPlayerBenchList = 0xC2BC
wOpponentBenchList = 0xC3BC
wPlayerDeck = 0xC400
wOpponentDeck = 0xC600
wDuelDisplayedScreen = 0xCAC2
wLCDC = 0xCABB
wSkipDuelistIsThinkingDelay = 0xCBF9
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory AIDoTurn_LegendaryDragonite
CONTRACT["AIDoTurn_LegendaryDragonite"] = {"compare": ("f",), "preserve": ()}
CASES["AIDoTurn_LegendaryDragonite"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {wPreviousAIFlags: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, read={wPreviousAIFlags: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDoTurn_LegendaryDragonite

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIDoTurn_LegendaryDragonite
MUTATIONS["AIDoTurn_LegendaryDragonite"] = {"source_symbol": "AIDoTurn_LegendaryDragonite", "before": "\treturn (AIDoTurn_LegendaryDragoniteResult){decision.f};", "after": "\treturn (AIDoTurn_LegendaryDragoniteResult){0xffu};", "case_ids": ["AIDoTurn_LegendaryDragonite-0", "AIDoTurn_LegendaryDragonite-1"]}
# <<< factory-mutation AIDoTurn_LegendaryDragonite
