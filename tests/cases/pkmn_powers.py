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
	{"c": 1, "wram": {0xCE06: b"\xab"}},  # bench location: must skip the weakness write too
	{"c": 5},
	{"c": 0xff},
	dict(POISON),
]
# <<< factory HandleAIShift

# >>> factory HandleAIPeek
hTemp_ffa0 = 0xFFA0
hTempCardIndex_ff9f = 0xFF9F
hAIPkmnPowerEffectParam = 0xFFA1
wAIPeekedPrizes = 0xCDA5
wDuelTempList = 0xC510
wce08 = 0xCE08
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
CONTRACT["HandleAIStrangeBehavior"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["HandleAIStrangeBehavior"] = [
	{"c": 0},
	dict(POISON, c=0),
]
# <<< factory HandleAIStrangeBehavior

# >>> factory HandleAICurse
CONTRACT["HandleAICurse"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAICurse"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {0xC2EF: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\x71", 0xC400: b"\x01"},
        "hram": {0xFF97: b"\xC3"},
        "expect_regs": {"a": 0x01, "f": 0x00},
        "expect": {0xFFA0: b"\xCC", 0xFF97: b"\xC3"},
    },
]
# <<< factory HandleAICurse

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory HandleAIDamageSwap
CONTRACT["HandleAIDamageSwap"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIDamageSwap"] = [
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEF: b"\x01"}),
    {"a": 0x11, "f": 0xE0, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x6789, "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEF: b"\x01"}},
]
# <<< factory HandleAIDamageSwap

# >>> factory HandleAIHeal
CONTRACT["HandleAIHeal"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIHeal"] = [
    {"c": 0, "wram": {0xFF97: b"\xC2", 0xC200: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\xC9", 0xC2EF: b"\x01"}, "read": {0xFFA0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 1, "wram": {0xFF97: b"\xC2", 0xC200: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\xC9", 0xC2EF: b"\x01"}, "read": {0xFFA0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0xE4, "wram": {0xFF97: b"\xC2", 0xC200: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\xC9", 0xC2EF: b"\x01"}, "read": {0xFFA0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0xCC, wram={0xFF97: b"\xC2", 0xC200: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\xC9", 0xC2EF: b"\x01"}, read={0xFFA0: 1}, instruction_budget=20000000, cycle_budget=80000000),
    {"c": 1, "wram": {0xFF97: b"\xC2", 0xC200: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\xC9", 0xC2EF: b"\x01"}, "read": {0xFFA0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory HandleAIHeal

# >>> factory HandleAIPkmnPowers
CONTRACT["HandleAIPkmnPowers"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIPkmnPowers"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC3BB: b"\x00", 0xC2BC: b"\x00\xC5", 0xC3BC: b"\x01\xC5", 0xC400: b"\x27", 0xC480: b"\x27", 0xC500: b"\xFF", 0xC501: b"\xFF"}, "read": {0xCE7C: 1}},
    {"a": 0x11, "f": 0xE0, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x6789, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC3BB: b"\x00", 0xC2BC: b"\x00\xC5", 0xC3BC: b"\x01\xC5", 0xC400: b"\x27", 0xC480: b"\x27", 0xC500: b"\xFF", 0xC501: b"\xFF"}, "read": {0xCE7C: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC3BB: b"\x00", 0xC2BC: b"\x00\xC5", 0xC3BC: b"\x01\xC5", 0xC400: b"\x27", 0xC480: b"\x27", 0xC500: b"\xFF", 0xC501: b"\xFF"}, read={0xCE7C: 1}),
]
# <<< factory HandleAIPkmnPowers

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
MUTATIONS["HandleAIStrangeBehavior"] = {"source_symbol": "HandleAIStrangeBehavior", "before": "\tif (c == 0u)", "after": "\tif (c != 0u)", "case_ids": ["HandleAIStrangeBehavior-1"]}
# <<< factory-mutation HandleAIStrangeBehavior
# >>> factory-mutation HandleAICurse
MUTATIONS["HandleAICurse"] = {
    "source_symbol": "HandleAICurse",
    "before": "return (HandleAICurseResult){1u, 0x00u};",
    "after": "return (HandleAICurseResult){2u, 0x00u};",
    "case_ids": ["HandleAICurse-0"],
}
# <<< factory-mutation HandleAICurse
# >>> factory-mutation HandleAIDamageSwap
MUTATIONS["HandleAIDamageSwap"] = {
    "source_symbol": "HandleAIDamageSwap",
    "before": "\t\treturn (HandleAIDamageSwapResult){0u, (uint8_t)(0xc0u | (f & 0x10u))};",
    "after": "\t\treturn (HandleAIDamageSwapResult){1u, (uint8_t)(0xc0u | (f & 0x10u))};",
    "case_ids": ["HandleAIDamageSwap-0", "HandleAIDamageSwap-1"],
}
# <<< factory-mutation HandleAIDamageSwap
# >>> factory-mutation HandleAIHeal
MUTATIONS["HandleAIHeal"] = {"source_symbol": "HandleAIHeal", "before": "\tuint8_t copy_length = PKMN_CARD_DATA_LENGTH;", "after": "\tuint8_t copy_length = 0x40u;", "case_ids": ["HandleAIHeal-1", "HandleAIHeal-2", "HandleAIHeal-4"]}
# <<< factory-mutation HandleAIHeal
# >>> factory-mutation HandleAIPkmnPowers
MUTATIONS["HandleAIPkmnPowers"] = {"source_symbol": "HandleAIPkmnPowers", "before": "\tif (muk.f & 0x10u)\n\t\treturn (HandleAIPkmnPowersResult){muk.a, 0x00u};", "after": "\tif (muk.f & 0x10u)\n\t\treturn (HandleAIPkmnPowersResult){(uint8_t)(muk.a + 1u), 0x00u};", "case_ids": ["HandleAIPkmnPowers-0", "HandleAIPkmnPowers-1", "HandleAIPkmnPowers-2"]}
# <<< factory-mutation HandleAIPkmnPowers
