"""Oracle-diff cases for poketcg/src/engine/duel/animations/screen_effects.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DecrementScreenAnimDuration
CONTRACT["DecrementScreenAnimDuration"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e")}
CASES["DecrementScreenAnimDuration"] = [
	# all-zero: 0 -> 0xff, Z clear, half-borrow set, carry clear -> f=0x60
	{},
	# entry carry passes through untouched (0 -> 0xff) -> f=0x70
	{"f": 0x10},
	# boundary 1 -> 0: Z set, H clear; poison proves a/b/c/d/e/hl preserved and C carried -> f=0xd0
	dict(POISON, wram={0xD4BB: b"\x01"}),
	# half-borrow boundary 0x10 -> 0x0f; entry Z/N/H bits must not leak into f -> f=0x60
	{"f": 0xE0, "wram": {0xD4BB: b"\x10"}},
	# plain decrement, no flags produced by dec -> f=0x40
	{"wram": {0xD4BB: b"\xff"}},
	# 2 -> 1: result nonzero, no half-borrow -> f=0x40
	{"wram": {0xD4BB: b"\x02"}},
]
# <<< factory DecrementScreenAnimDuration

# >>> factory UpdateShakeOffset
CONTRACT["UpdateShakeOffset"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["UpdateShakeOffset"] = [
	{},
	{"wram": {0xD4BB: b"\x00", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	{"wram": {0xD4BB: b"\x15", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	{"wram": {0xD4BB: b"\x20", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	dict(POISON, wram={0xD4BB: b"\x01", 0xD4BC: b"\x00\xC1", 0xC100: b"\x01\xFF"}, read={0xD4BC: 2, 0xC100: 1}),
]
# <<< factory UpdateShakeOffset

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DecrementScreenAnimDuration
MUTATIONS["DecrementScreenAnimDuration"] = {
	"source_symbol": "DecrementScreenAnimDuration",
	"before": "(v == 0u ? 0x80u : 0u)",
	"after": "(v == 0u ? 0x00u : 0x80u)",
	"case_ids": ["DecrementScreenAnimDuration-0", "DecrementScreenAnimDuration-1", "DecrementScreenAnimDuration-2", "DecrementScreenAnimDuration-3", "DecrementScreenAnimDuration-4", "DecrementScreenAnimDuration-5"],
}
# <<< factory-mutation DecrementScreenAnimDuration
# >>> factory-mutation UpdateShakeOffset
MUTATIONS["UpdateShakeOffset"] = {"source_symbol": "UpdateShakeOffset", "before": "\tif (duration >= timer)", "after": "\tif (duration > timer)", "case_ids": ["UpdateShakeOffset-2", "UpdateShakeOffset-4"]}
# <<< factory-mutation UpdateShakeOffset
