"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_articuno.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
ARTICUNO_SCORE = 0xCDE5

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

from tests.cases._fixtures import articuno_turn_fixture as _articuno_turn_fixture, ARTICUNO_TURN_REGS as _ARTICUNO_TURN_REGS
from tests.cases._fixtures import articuno_scoring_fixture as _articuno_scoring_fixture, ARTICUNO_SCORING_REGS as _ARTICUNO_SCORING_REGS

# >>> factory ScoreLegendaryArticunoCards
CONTRACT["ScoreLegendaryArticunoCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ScoreLegendaryArticunoCards"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, "expect": {ARTICUNO_SCORE: b"\x05"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, expect={ARTICUNO_SCORE: b"\x05"}),
    # dome-3 745559: Jack's Lapras on the bench already holds three energies, so
    # `.lapras` falls through to `.articuno` and Articuno's bench score rises.
    dict(_articuno_scoring_fixture(vram=False, bank=5), **_ARTICUNO_SCORING_REGS, read={ARTICUNO_SCORE: 1, 0xCDD4: 1, 0xCE00: 0x40}),
]
# <<< factory ScoreLegendaryArticunoCards

# >>> factory AIDoTurn_LegendaryArticuno
CONTRACT["AIDoTurn_LegendaryArticuno"] = {"compare": ("f",), "preserve": ()}
CASES["AIDoTurn_LegendaryArticuno"] = [
    # dome-3 728162: Jack's turn. AIDecidePlayPokemonCard leaves no carry and the
    # retreat's carry is not a return (legendary_articuno.asm:165-167), so the
    # turn goes on to the energy attach; both duelists' state and the AI scratch
    # are observed.
    dict(_articuno_turn_fixture(bank=5), **_ARTICUNO_TURN_REGS, read={0xC200: 0x200, 0xCC00: 0x100, 0xCE00: 0x40}),
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {wPreviousAIFlags: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wPreviousAIFlags: b"\x00", wDuelDisplayedScreen: b"\x01", wSkipDuelistIsThinkingDelay: b"\x01"}, read={wPreviousAIFlags: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDoTurn_LegendaryArticuno

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation ScoreLegendaryArticunoCards
MUTATIONS["ScoreLegendaryArticunoCards"] = {"source_symbol": "ScoreLegendaryArticunoCards", "before": "\t\t\tif (energy.a < 3u) {\n\t\t\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(LAPRAS);\n\t\t\t\treturn;\n\t\t\t}", "after": "\t\t\tif (energy.a < 3u)\n\t\t\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(LAPRAS);\n\t\t\treturn;", "case_ids": ["ScoreLegendaryArticunoCards-2"]}
# <<< factory-mutation ScoreLegendaryArticunoCards
# >>> factory-mutation AIDoTurn_LegendaryArticuno
MUTATIONS["AIDoTurn_LegendaryArticuno"] = {"source_symbol": "AIDoTurn_LegendaryArticuno", "before": "\t\t(void)AIProcessRetreat();\n\t\ttrainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);", "after": "\t\tAIProcessRetreatResult retreat = AIProcessRetreat();\n\t\tif ((retreat.f & 0x10u) != 0u)\n\t\t\treturn (AIDoTurn_LegendaryArticunoResult){retreat.f};\n\t\ttrainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);", "case_ids": ["AIDoTurn_LegendaryArticuno-0"]}
# <<< factory-mutation AIDoTurn_LegendaryArticuno
