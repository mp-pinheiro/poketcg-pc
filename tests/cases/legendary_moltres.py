"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_moltres.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
hTemp_ffa0 = sym("hTemp_ffa0")
wAlreadyPlayedEnergy = sym("wAlreadyPlayedEnergy")
hWhoseTurn = sym("hWhoseTurn")
wAIBarrierFlagCounter = sym("wAIBarrierFlagCounter")
wPlayerHandCount = sym("wPlayerNumberOfCardsInHand")
wOpponentHandCount = sym("wOpponentNumberOfCardsInHand")
wPlayerArenaCard = sym("wPlayerArenaCard")
wOpponentArenaCard = sym("wOpponentArenaCard")
wPlayerBenchList = sym("wPlayerBench")
wOpponentBenchList = sym("wOpponentBench")
wPlayerDeck = sym("wPlayerDeck")
wOpponentDeck = sym("wc600")
wDuelDisplayedScreen = sym("wDuelDisplayedScreen")
wLCDC = sym("wLCDC")
wSkipDuelistIsThinkingDelay = sym("wSkipDuelistIsThinkingDelay")
wPreviousAIFlags = sym("wPreviousAIFlags")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory AIDoTurn_LegendaryMoltres
CONTRACT["AIDoTurn_LegendaryMoltres"] = {"compare": ("f",), "preserve": ()}
CASES["AIDoTurn_LegendaryMoltres"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {wPreviousAIFlags: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9", wAlreadyPlayedEnergy: b"\x01", wDuelDisplayedScreen: b"\x01", wSkipDuelistIsThinkingDelay: b"\x01"}, read={wPreviousAIFlags: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDoTurn_LegendaryMoltres

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIDoTurn_LegendaryMoltres
MUTATIONS["AIDoTurn_LegendaryMoltres"] = {"source_symbol": "AIDoTurn_LegendaryMoltres", "before": "\treturn (AIDoTurn_LegendaryMoltresResult){decision.f};", "after": "\treturn (AIDoTurn_LegendaryMoltresResult){(uint8_t)(decision.f ^ 0x01u)};", "case_ids": ["AIDoTurn_LegendaryMoltres-0", "AIDoTurn_LegendaryMoltres-1"]}
# <<< factory-mutation AIDoTurn_LegendaryMoltres
