"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_zapdos.asm."""
from tests.cases._symbols import sym
from tests.cases._fixtures import Fixture


POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

_ZAPDOS_AI = Fixture("legendary-zapdos-aidoturn-entry")
_ZAPDOS_VOLTORB = _ZAPDOS_AI.case({
    sym("wOpponentArenaCard"): b"\x00",
    sym("wOpponentBench"): b"\x03\xFF\xFF\xFF\xFF\xFF",
    sym("wOpponentNumberOfPokemonInPlayArea"): b"\x02",
    sym("wOpponentHand"): b"\x01\x02",
    sym("wOpponentNumberOfCardsInHand"): b"\x02",
    sym("wOpponentDeck"): b"\x6D\x04\x0F\x75",
    sym("wPlayerNumberOfCardsInHand"): b"\x04",
})
# >>> factory-cases-statics
hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
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
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory AIDoTurn_LegendaryZapdos
CONTRACT["AIDoTurn_LegendaryZapdos"] = {"compare": ("f",), "preserve": ()}
CASES["AIDoTurn_LegendaryZapdos"] = [
    _ZAPDOS_VOLTORB,
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, "read": {sym("wPreviousAIFlags"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wAIBarrierFlagCounter: b"\x80", wPlayerHandCount: b"\x00", wOpponentHandCount: b"\x00", wPlayerArenaCard: b"\x00", wOpponentArenaCard: b"\x00", wPlayerBenchList: b"\xFF", wOpponentBenchList: b"\xFF", wPlayerDeck: b"\xB9\xFF", wOpponentDeck: b"\xB9\xFF", wAlreadyPlayedEnergy: b"\x01", wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wSkipDuelistIsThinkingDelay: b"\x01"}, read={sym("wPreviousAIFlags"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDoTurn_LegendaryZapdos

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIDoTurn_LegendaryZapdos
MUTATIONS["AIDoTurn_LegendaryZapdos"] = {"source_symbol": "AIDoTurn_LegendaryZapdos", "before": "\t\t\t\tattach_to_arena = (LookForCardIDInHandList_Bank5(ELECTRODE_LV35).f & 0x10u) != 0u;", "after": "\t\t\t\tattach_to_arena = (LookForCardIDInHandList_Bank5(ELECTRODE_LV35).f & 0x10u) == 0u;", "case_ids": ["AIDoTurn_LegendaryZapdos-0"]}
# <<< factory-mutation AIDoTurn_LegendaryZapdos
