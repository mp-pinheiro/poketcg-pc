"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/general.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wAIPlayAreaCardToSwitch = 0xCDD5
wAIRetreatedThisTurn = 0xCE03
wPreviousAIFlags = 0xCE20
wConfusionRetreatCheckWasUnsuccessful = 0xCC0C
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

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
# <<< factory-cases-statics

# >>> factory AIProcessRetreat
CONTRACT["AIProcessRetreat"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIProcessRetreat"] = [
    {"wram": {wAIRetreatedThisTurn: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00}},
    {"wram": {wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00}},
    {"wram": {wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x80"}, "expect_regs": {"a": 0x80, "f": 0x00}},
    dict(POISON, wram={wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x01"}, expect_regs={"a": 0x01, "f": 0x00}),
]
# <<< factory AIProcessRetreat

# >>> factory AIMainTurnLogic
CONTRACT["AIMainTurnLogic"] = {"compare": ("f",), "preserve": ()}
CASES["AIMainTurnLogic"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {wPreviousAIFlags: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wSkipDuelistIsThinkingDelay: b"\x01"}, read={wPreviousAIFlags: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIMainTurnLogic

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIProcessRetreat
MUTATIONS["AIProcessRetreat"] = {"source_symbol": "AIProcessRetreat", "before": "AIProcessRetreatResult AIProcessRetreat(void)\n{\n\tuint8_t already_retreated = wAIRetreatedThisTurn;", "after": "AIProcessRetreatResult AIProcessRetreat(void)\n{\n\tuint8_t already_retreated = 0u;", "case_ids": ["AIProcessRetreat-0"]}
# <<< factory-mutation AIProcessRetreat
# >>> factory-mutation AIMainTurnLogic
MUTATIONS["AIMainTurnLogic"] = {"source_symbol": "AIMainTurnLogic", "before": "AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tInitAITurnVars();", "after": "AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t unused = 0u;", "case_ids": ["AIMainTurnLogic-0", "AIMainTurnLogic-1"]}
# <<< factory-mutation AIMainTurnLogic
