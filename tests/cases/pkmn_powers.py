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
