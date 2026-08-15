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
