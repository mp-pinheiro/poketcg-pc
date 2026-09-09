"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_ronald.asm."""

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
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

from tests.cases._fixtures import ronald_turn_fixture as _ronald_turn_fixture, RONALD_TURN_REGS as _RONALD_TURN_REGS

# >>> factory AIDoTurn_LegendaryRonald
CONTRACT["AIDoTurn_LegendaryRonald"] = {"compare": ("f",), "preserve": ()}
CASES["AIDoTurn_LegendaryRonald"] = [
    # The live turn: wAITrainerCardPhase ($CE18) ends at PHASE_15 because Oak was
    # not used; the trainer phases past it belong to the Oak re-run only.
    dict(_ronald_turn_fixture(bank=5), **_RONALD_TURN_REGS, read={0xC200: 0x200, 0xCC00: 0x100, 0xCE00: 0x40}),
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {wPreviousAIFlags: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wSkipDuelistIsThinkingDelay: b"\x01"}, read={wPreviousAIFlags: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDoTurn_LegendaryRonald

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIDoTurn_LegendaryRonald
MUTATIONS["AIDoTurn_LegendaryRonald"] = {"source_symbol": "AIDoTurn_LegendaryRonald", "before": "\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);\n\tAIProcessRetreat();", "after": "\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);", "case_ids": ["AIDoTurn_LegendaryRonald-0"]}
# <<< factory-mutation AIDoTurn_LegendaryRonald
