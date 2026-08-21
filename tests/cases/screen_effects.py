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

# >>> factory-cases-statics
wActiveScreenAnim = 0xD42A
wScreenAnimUpdatePtr = 0xD4B9
hSCX = 0xFF92
rSCX = 0xFF43
hSCY = 0xFF93
rSTAT = 0xFF41
rIE = 0xFFFF
# <<< factory-cases-statics

# >>> factory DefaultScreenAnimationUpdate
CONTRACT["DefaultScreenAnimationUpdate"] = {"compare": (), "preserve": ()}
CASES["DefaultScreenAnimationUpdate"] = [
    {"wram": {0xD42A: b"\x00", 0xD4B9: b"\x00\x00"}, "hram": {0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, "expect": {0xD42A: b"\xFF", 0xD4B9: b"\xBC\x4C", 0xFF92: b"\x00", 0xFF93: b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}},
    dict(POISON, wram={0xD42A: b"\x12", 0xD4B9: b"\x34\x56"}, hram={0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, expect={0xD42A: b"\xFF", 0xD4B9: b"\xBC\x4C", 0xFF92: b"\x00", 0xFF93: b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}),
]
# <<< factory DefaultScreenAnimationUpdate

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
# >>> factory-mutation DefaultScreenAnimationUpdate
MUTATIONS["DefaultScreenAnimationUpdate"] = {
    "source_symbol": "DefaultScreenAnimationUpdate",
    "before": "gb_write8(wActiveScreenAnim_ADDR, 0xffu);",
    "after": "gb_write8(wActiveScreenAnim_ADDR, 0xfeu);",
    "case_ids": ["DefaultScreenAnimationUpdate-0", "DefaultScreenAnimationUpdate-1"],
}
# <<< factory-mutation DefaultScreenAnimationUpdate
