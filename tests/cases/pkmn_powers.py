from tests.cases._symbols import card_id_size, const, deck_bytes, rom_byte, sym, sym_bank
from tests.cases._fixtures import ai_heal_fixture as _ai_heal_fixture, AI_HEAL_REGS as _AI_HEAL_REGS
from tests.cases._fixtures import strange_behavior_fixture as _strange_behavior_fixture, STRANGE_BEHAVIOR_REGS as _STRANGE_BEHAVIOR_REGS
from tests.cases._fixtures import energy_trans_fixture as _energy_trans_fixture, ENERGY_TRANS_REGS as _ENERGY_TRANS_REGS
from tests.cases._fixtures import AI_PKMN_POWERS_REGS, ai_pkmn_powers_fixture
from tests.cases._fixtures import AI_PKMN_POWERS_MASTER_REGS, ai_pkmn_powers_master_fixture
from tests.cases._fixtures import cowardice_fixture as _cowardice_fixture, COWARDICE_REGS as _COWARDICE_REGS
"""Oracle-diff cases for poketcg/src/engine/duel/ai/pkmn_powers.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory HandleAIShift
# c = Play Area location of Venomoth (0 = Arena). Every nonzero (bench or
# invalid) location exits at the first `ret nz` with a = c, Z clear, and all
# other registers and RAM untouched, so those cases fully pin the c-gate, the
# a/f exit contract, and every preservation claim.
# No c==0 case is included: that path drives live duel state -- GetArenaCardColor
# and GetArenaCardWeakness dereference the turn duelist's arena-card/deck data
# via GetTurnDuelistVariable and SwapTurn, and .found dispatches the bank:1
# AIMakeDecision action handlers -- none of whose addresses are seedable from
# this case schema, so the oracle cannot be driven to a reproducible exit.
CONTRACT["HandleAIShift"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["HandleAIShift"] = [
	{"c": 1, "wram": {sym("wAIDefendingPokemonWeakness"): b"\xab"}},  # bench location: must skip the weakness write too
	{"c": 5},
	{"c": 0xff},
	dict(POISON),
]
# <<< factory HandleAIShift

# >>> factory HandleAIPeek
hTemp_ffa0 = sym("hTemp_ffa0")
hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
hAIPkmnPowerEffectParam = sym("hAIPkmnPowerEffectParam")
wAIPeekedPrizes = sym("wAIPeekedPrizes")
wDuelTempList = sym("wDuelTempList")
wce08 = sym("wce08")
CONTRACT["HandleAIPeek"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIPeek"] = [
	{"c": 0},
	{"c": 1, "wram": {wAIPeekedPrizes: b"\x24", wce08: b"\x37", hTemp_ffa0: b"\x00", hAIPkmnPowerEffectParam: b"\x00"}},
	{"c": 5, "wram": {wAIPeekedPrizes: b"\x3f", wDuelTempList: b"\x02\x10\x1f\xff", wce08: b"\x01", hAIPkmnPowerEffectParam: b"\xee"}},
	{"c": 2, "wram": {wAIPeekedPrizes: b"\x01", wce08: b"\x0c"}},
	{"c": 3, "wram": {wAIPeekedPrizes: b"\x20", wDuelTempList: b"\xff"}},
	dict(POISON, c=0x05, wram={wAIPeekedPrizes: b"\x2a", wce08: b"\x81", hTemp_ffa0: b"\x77", hTempCardIndex_ff9f: b"\x66", hAIPkmnPowerEffectParam: b"\x55", wDuelTempList: b"\x04\x0c\x11\x2a\xff"}),
]
# <<< factory HandleAIPeek

# >>> factory HandleAIStrangeBehavior
CONTRACT["HandleAIStrangeBehavior"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["HandleAIStrangeBehavior"] = [
	{"c": 0},
	dict(POISON, c=0),
	dict(_strange_behavior_fixture(vram=False, damage=0), **_STRANGE_BEHAVIOR_REGS),
	dict(_strange_behavior_fixture(vram=False, damage=10), **_STRANGE_BEHAVIOR_REGS, compare=("f",)),
]
# <<< factory HandleAIStrangeBehavior

# >>> factory HandleAICurse
CONTRACT["HandleAICurse"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAICurse"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): b"\x71", sym("wBoosterCardsDrawn"): b"\x01"},
        "hram": {sym("hWhoseTurn"): b"\xC3"},
        "expect_regs": {"a": 0x01, "f": 0x00},
        "expect": {sym("hTempList"): b"\xCC", sym("hWhoseTurn"): b"\xC3"},
    },
    # ai-duel-2b 40109: one damaged card in the player's play area is not enough for Curse
    # (pkmn_powers.asm:887 wants two); hTempRetreatCostCards keeps the retreat's card index.
    {
        "c": 0x00,
        "wram": {sym("wPlayerNumberOfPokemonInPlayArea"): b"\x02", sym("wPlayerArenaCard"): b"\x00\x01\xFF", sym("wPlayerArenaCardHP"): b"\x1E\x28", sym("wBoosterCardsDrawn"): deck_bytes((8, 8)), sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentArenaCard"): b"\x00\xFF", sym("wOpponentDeck"): deck_bytes((8,))},
        "hram": {sym("hWhoseTurn"): b"\xC3", sym("hAIEnergyTransEnergyCard"): b"\x09"},
        "read": {sym("hTempList"): 3},
    },
    # Two damaged player cards: the lowest-HP one is stored before the second scan.
    {
        "c": 0x00,
        "wram": {sym("wPlayerNumberOfPokemonInPlayArea"): b"\x02", sym("wPlayerArenaCard"): b"\x00\x01\xFF", sym("wPlayerArenaCardHP"): b"\x1E\x14", sym("wBoosterCardsDrawn"): deck_bytes((8, 8)), sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentArenaCard"): b"\x00\xFF", sym("wOpponentDeck"): deck_bytes((8,)), sym("wOpponentArenaCardHP"): b"\x28"},
        "hram": {sym("hWhoseTurn"): b"\xC3", sym("hAIEnergyTransEnergyCard"): b"\x09"},
        "read": {sym("hTempList"): 3},
    },
]
# <<< factory HandleAICurse

# >>> factory-cases-statics
hWhoseTurn = sym("hWhoseTurn")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOpponentDeckID = sym("wOpponentDeckID")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hAIPkmnPowerEffectParam = sym("hAIPkmnPowerEffectParam")
hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
hTemp_ffa0 = sym("hTemp_ffa0")
wce08 = sym("wce08")

hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")

wAINumberOfEnergyTransCards = sym("wAINumberOfEnergyTransCards")
# <<< factory-cases-statics

# >>> factory HandleAIDamageSwap
CONTRACT["HandleAIDamageSwap"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIDamageSwap"] = [
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEF: b"\x01"}),
    {"a": 0x11, "f": 0xE0, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x6789, "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEF: b"\x01"}},
    # Boss deck (never skips), bench present, no Alakazam with an active power.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x0E", wPlayerDuelVariables + 0xEF: b"\x02", wPlayerDuelVariables + 0xBB: b"\x00\x01\xFF", wPlayerDuelVariables + 0x00: b"\x01\x11", wPlayerDuelVariables + 0xC8: b"\x50\x78", sym("wBoosterCardsDrawn"): b"\x60\xB8"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    # Alakazam in the arena at full HP: nothing to swap.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x0E", wPlayerDuelVariables + 0xEF: b"\x02", wPlayerDuelVariables + 0xBB: b"\x00\x01\xFF", wPlayerDuelVariables + 0x00: b"\x01\x11", wPlayerDuelVariables + 0xC8: b"\x50\x78", sym("wBoosterCardsDrawn"): b"\x90\xB8"}, "read": {sym("wAIDefendingPokemonWeakness"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    # Damaged Alakazam, but the only benched card cannot take counters.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x0E", wPlayerDuelVariables + 0xEF: b"\x02", wPlayerDuelVariables + 0xBB: b"\x00\x01\xFF", wPlayerDuelVariables + 0x00: b"\x01\x11", wPlayerDuelVariables + 0xC8: b"\x30\x28", sym("wBoosterCardsDrawn"): b"\x90\x60"}, "read": {sym("wAIDefendingPokemonWeakness"): 1, sym("wAISetupEnergyCount"): 1}, "expect": {sym("wAIDefendingPokemonWeakness"): b"\x05", sym("wAISetupEnergyCount"): b"\x00"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    # Damaged Alakazam, a benched Chansey with only 10 HP left is skipped.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x0E", wPlayerDuelVariables + 0xEF: b"\x02", wPlayerDuelVariables + 0xBB: b"\x00\x01\xFF", wPlayerDuelVariables + 0x00: b"\x01\x11", wPlayerDuelVariables + 0xC8: b"\x30\x0A", sym("wBoosterCardsDrawn"): b"\x90\xB8"}, "read": {sym("wAIDefendingPokemonWeakness"): 1, sym("wAISetupEnergyCount"): 1}, "expect": {sym("wAIDefendingPokemonWeakness"): b"\x05", sym("wAISetupEnergyCount"): b"\x00"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory HandleAIDamageSwap

# >>> factory HandleAIHeal
CONTRACT["HandleAIHeal"] = {"compare": ("a", "f"), "preserve": ()}
_NULL_CARD_HP = bytes((rom_byte(0, const("CARD_DATA_HP")),))
CASES["HandleAIHeal"] = [
    {"c": 0, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerCardLocations"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): _NULL_CARD_HP, sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}, "read": {sym("hTempList"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 1, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerCardLocations"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): _NULL_CARD_HP, sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}, "read": {sym("hTempList"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0xE4, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerCardLocations"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): _NULL_CARD_HP, sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}, "read": {sym("hTempList"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0xCC, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerCardLocations"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): _NULL_CARD_HP, sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}, read={sym("hTempList"): 1}, instruction_budget=20000000, cycle_budget=80000000),
    {"c": 1, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerCardLocations"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): _NULL_CARD_HP, sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}, "read": {sym("hTempList"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(_ai_heal_fixture(vram=False, bank=8), **_AI_HEAL_REGS, instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory HandleAIHeal

# >>> factory HandleAIPkmnPowers
CONTRACT["HandleAIPkmnPowers"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIPkmnPowers"] = [
    # water-master 419138: Amy's turn, the live entry the sweep flagged (a, f).
    dict(ai_pkmn_powers_master_fixture(vram=False, bank=sym_bank("HandleAIPkmnPowers")), **AI_PKMN_POWERS_MASTER_REGS, read={sym("wAISetupEnergyCount"): 1, sym("hTempPlayAreaLocation_ff9d"): 1}),
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): deck_bytes((const("MUK"),)), sym("wOpponentDeck"): deck_bytes((const("MUK"),)), sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {sym("wTempPokemonID_ce7c"): card_id_size()}},
    {"a": 0x11, "f": 0xE0, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x6789, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): deck_bytes((const("MUK"),)), sym("wOpponentDeck"): deck_bytes((const("MUK"),)), sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {sym("wTempPokemonID_ce7c"): card_id_size()}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): deck_bytes((const("MUK"),)), sym("wOpponentDeck"): deck_bytes((const("MUK"),)), sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, read={sym("wTempPokemonID_ce7c"): card_id_size()}),
    dict(ai_pkmn_powers_fixture(vram=False), **AI_PKMN_POWERS_REGS),
]
# <<< factory HandleAIPkmnPowers

# >>> factory HandleAIGoGoRainDanceEnergy
CONTRACT["HandleAIGoGoRainDanceEnergy"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIGoGoRainDanceEnergy"] = [
	{"wram": {wOpponentDeckID: b"\x00"}},
	{"wram": {wOpponentDeckID: b"\x01"}},
	{"wram": {wOpponentDeckID: b"\xE4"}},
	dict(POISON, wram={wOpponentDeckID: b"\x00"}),
]
# <<< factory HandleAIGoGoRainDanceEnergy

# >>> factory HandleAICowardice
CONTRACT["HandleAICowardice"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAICowardice"] = [
	{"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {sym("wTempPokemonID_ce7c"): 1}},
	{"a": 0x11, "f": 0xE0, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x6789, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {sym("wTempPokemonID_ce7c"): 1}},
	dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, read={sym("wTempPokemonID_ce7c"): 1}),
    dict(_cowardice_fixture(bank=8), **_COWARDICE_REGS, read={sym("wAISetupEnergyCount"): 1, sym("wOpponentArenaCard"): 6, sym("wOpponentArenaCardHP"): 6}),
]
# <<< factory HandleAICowardice

# >>> factory AIEnergyTransTransferEnergyToBench
# The carry-set path drives live duel state through subsequent AI routines and is omitted because it cannot be reproducibly exited from this case schema.
CONTRACT["AIEnergyTransTransferEnergyToBench"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIEnergyTransTransferEnergyToBench"] = [
	{"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {hTempPlayAreaLocation_ff9d: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
	dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, read={hTempPlayAreaLocation_ff9d: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AIEnergyTransTransferEnergyToBench

# >>> factory HandleAIEnergyTrans
# The first carry exit is fully seeded; deeper Venusaur/Muk and transfer paths drive live duel state and are omitted because they are not reproducibly exitable from this schema.
# The stub preserved b/c/d/e/hl; the real body leaves each exit's callee
# registers (hl is a duelist-variable pointer past the play-area count) and
# every caller in general.c reads a and f alone.
CONTRACT["HandleAIEnergyTrans"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIEnergyTrans"] = [
	{"a": 0x09, "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, "read": {wAINumberOfEnergyTransCards: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
	dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wPlayerBench"): b"\x00\xC5", sym("wOpponentBench"): b"\x01\xC5", sym("wBoosterCardsDrawn"): b"\x27", sym("wOpponentDeck"): b"\x27", sym("wNameBuffer"): b"\xFF", sym("wNameBuffer") + 1: b"\xFF"}, read={wAINumberOfEnergyTransCards: 1}, instruction_budget=20000000, cycle_budget=80000000),
	dict(_energy_trans_fixture(vram=False, bank=5), **_ENERGY_TRANS_REGS, read={sym("wAIDefendingPokemonWeakness"): 1, sym("wTempPokemonID_ce7c"): 1, sym("wRNG1"): 3}),
]
# <<< factory HandleAIEnergyTrans

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation HandleAIShift
MUTATIONS["HandleAIShift"] = {
	"source_symbol": "HandleAIShift",
	"before": "return (AIShiftResult){c, 0x00u};",
	"after": "return (AIShiftResult){c, 0x80u};",
	"case_ids": ["HandleAIShift-0", "HandleAIShift-1", "HandleAIShift-2", "HandleAIShift-3"],
}
# <<< factory-mutation HandleAIShift
# >>> factory-mutation HandleAIPeek
MUTATIONS["HandleAIPeek"] = {
	"source_symbol": "HandleAIPeek",
	"before": "\thTemp_ffa0 = c;",
	"after": "\thTemp_ffa0 = 0u;",
	"case_ids": ["HandleAIPeek-1", "HandleAIPeek-2", "HandleAIPeek-3", "HandleAIPeek-4", "HandleAIPeek-5"],
}
# <<< factory-mutation HandleAIPeek
# >>> factory-mutation HandleAIStrangeBehavior
MUTATIONS["HandleAIStrangeBehavior"] = {"source_symbol": "HandleAIStrangeBehavior", "before": "\t\treturn (HandleAIStrangeBehaviorResult){damage.a, 0x80u, damage.c, d, e, hl};", "after": "\t\treturn (HandleAIStrangeBehaviorResult){damage.a, 0x80u, c, d, e, hl};", "case_ids": ["HandleAIStrangeBehavior-2"]}
# <<< factory-mutation HandleAIStrangeBehavior
# >>> factory-mutation HandleAICurse
MUTATIONS["HandleAICurse"] = {
    "source_symbol": "HandleAICurse",
    "before": "if (found <= 1u) {",
    "after": "if (found == 0u) {",
    "case_ids": ["HandleAICurse-1"],
}
# <<< factory-mutation HandleAICurse
# >>> factory-mutation HandleAIDamageSwap
MUTATIONS["HandleAIDamageSwap"] = {
    "source_symbol": "HandleAIDamageSwap",
    "before": "\tgb_write8(WCE06_ADDR, ConvertHPToDamageCounters_Bank8(arena.a));",
    "after": "\tgb_write8(WCE06_ADDR, (uint8_t)(ConvertHPToDamageCounters_Bank8(arena.a) + 1u));",
    "case_ids": ["HandleAIDamageSwap-4", "HandleAIDamageSwap-5"],
}
# <<< factory-mutation HandleAIDamageSwap
# >>> factory-mutation HandleAIHeal
MUTATIONS["HandleAIHeal"] = {"source_symbol": "HandleAIHeal", "before": "\t\t\tgoto heal_arena;", "after": "\t\t\treturn (HandleAIHealResult){PLAY_AREA_ARENA, ko.f};", "case_ids": ["HandleAIHeal-5"]}
# <<< factory-mutation HandleAIHeal
# >>> factory-mutation HandleAIPkmnPowers
MUTATIONS["HandleAIPkmnPowers"] = {"source_symbol": "HandleAIPkmnPowers", "before": "\treturn (HandleAIPkmnPowersResult){c, 0xC0u};", "after": "\treturn (HandleAIPkmnPowersResult){c, 0x80u};", "case_ids": ["HandleAIPkmnPowers-0"]}
# <<< factory-mutation HandleAIPkmnPowers
# >>> factory-mutation HandleAIGoGoRainDanceEnergy
MUTATIONS["HandleAIGoGoRainDanceEnergy"] = {"source_symbol": "HandleAIGoGoRainDanceEnergy", "before": "\t\treturn (HandleAIGoGoRainDanceEnergyResult){deck, f};", "after": "\t\treturn (HandleAIGoGoRainDanceEnergyResult){deck, (uint8_t)(f ^ 0x10u)};", "case_ids": ["HandleAIGoGoRainDanceEnergy-0", "HandleAIGoGoRainDanceEnergy-1", "HandleAIGoGoRainDanceEnergy-2", "HandleAIGoGoRainDanceEnergy-3"]}
# <<< factory-mutation HandleAIGoGoRainDanceEnergy
# >>> factory-mutation HandleAICowardice
MUTATIONS["HandleAICowardice"] = {"source_symbol": "HandleAICowardice", "before": "\t\tuint8_t used = card_id < TENTACOOL;", "after": "\t\tuint8_t used = 0u;", "case_ids": ["HandleAICowardice-3"]}
# <<< factory-mutation HandleAICowardice
# >>> factory-mutation AIEnergyTransTransferEnergyToBench
MUTATIONS["AIEnergyTransTransferEnergyToBench"] = {"source_symbol": "AIEnergyTransTransferEnergyToBench", "before": "AIEnergyTransTransferEnergyToBenchResult AIEnergyTransTransferEnergyToBench(void)\n{\n\thTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;", "after": "AIEnergyTransTransferEnergyToBenchResult AIEnergyTransTransferEnergyToBench(void)\n{\n\thTempPlayAreaLocation_ff9d = 1u;", "case_ids": ["AIEnergyTransTransferEnergyToBench-0", "AIEnergyTransTransferEnergyToBench-1"]}
# <<< factory-mutation AIEnergyTransTransferEnergyToBench
# >>> factory-mutation HandleAIEnergyTrans
MUTATIONS["HandleAIEnergyTrans"] = {"source_symbol": "HandleAIEnergyTrans", "before": "\tPkmnPowerCountResult venusaur = CountTurnDuelistPokemonWithActivePkmnPower(VENUSAUR_LV67);", "after": "\tPkmnPowerCountResult venusaur = CountTurnDuelistPokemonWithActivePkmnPower(MUK);", "case_ids": ["HandleAIEnergyTrans-2"]}
# <<< factory-mutation HandleAIEnergyTrans
