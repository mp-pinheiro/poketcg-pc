"""Oracle-diff cases for poketcg/src/engine/overworld/overworld.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Func_c6cc
wPlayerXCoordPixels = 0xD332
wPlayerYCoordPixels = 0xD333
wPlayerSpriteIndex = 0xD336
wWhichSprite = 0xD4CF
wSpriteAnimScratch = 0xD4D0
CONTRACT["Func_c6cc"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c6cc"] = [
	{"a": 0, "wram": {wPlayerXCoordPixels: b"\x00"}},
	{"a": 1, "wram": {wPlayerXCoordPixels: b"\x02"}},
	{"a": 0x08, "wram": {wPlayerXCoordPixels: b"\x08"}},
	{"a": 0x80, "wram": {wPlayerXCoordPixels: b"\x80"}},
	{"a": 0x0F, "wram": {wPlayerXCoordPixels: b"\x01"}},
	dict(POISON, a=0x11, wram={wPlayerXCoordPixels: b"\xee"}),
]
# <<< factory Func_c6cc

# >>> factory Func_c6d4
CONTRACT["Func_c6d4"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c6d4"] = [
	{"a": 0, "wram": {wPlayerYCoordPixels: b"\x00"}},
	{"a": 1, "wram": {wPlayerYCoordPixels: b"\x02"}},
	{"a": 0x70, "wram": {wPlayerYCoordPixels: b"\x90"}},
	{"a": 0x0F, "wram": {wPlayerYCoordPixels: b"\x0F"}},
	{"a": 0xFF, "wram": {wPlayerYCoordPixels: b"\x01"}},
	dict(POISON, a=0x40, wram={wPlayerYCoordPixels: b"\x40"}),
]
# <<< factory Func_c6d4

# >>> factory Func_c6f7
CONTRACT["Func_c6f7"] = {"compare": ("a", "hl", "b", "d", "e"), "preserve": ("b", "d", "e")}
CASES["Func_c6f7"] = [
	{"wram": {wPlayerSpriteIndex: b"\x00"}},
	{"wram": {wPlayerSpriteIndex: b"\x01", wWhichSprite: b"\x00", wSpriteAnimScratch: b"\x00" * 0x80}},
	{"wram": {wPlayerSpriteIndex: b"\x02", wWhichSprite: b"\x00", wSpriteAnimScratch: b"\xff" * 0x80}},
	dict(POISON, wram={wPlayerSpriteIndex: b"\x03", wWhichSprite: b"\xaa", wSpriteAnimScratch: b"\x55" * 0x80}),
]
# <<< factory Func_c6f7

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_c6cc
MUTATIONS["Func_c6cc"] = {
	"source_symbol": "Func_c6cc",
	"before": "wPlayerXCoordPixels = sum;",
	"after": "wPlayerXCoordPixels = a;",
	"case_ids": ["Func_c6cc-1", "Func_c6cc-2", "Func_c6cc-3", "Func_c6cc-4", "Func_c6cc-5"],
}
# <<< factory-mutation Func_c6cc
# >>> factory-mutation Func_c6d4
MUTATIONS["Func_c6d4"] = {
	"source_symbol": "Func_c6d4",
	"before": "wPlayerYCoordPixels = sum;",
	"after": "wPlayerYCoordPixels = a;",
	"case_ids": ["Func_c6d4-1", "Func_c6d4-2", "Func_c6d4-3", "Func_c6d4-4", "Func_c6d4-5"],
}
# <<< factory-mutation Func_c6d4
# >>> factory-mutation Func_c6f7
MUTATIONS["Func_c6f7"] = {
	"source_symbol": "Func_c6f7",
	"before": "wWhichSprite = wPlayerSpriteIndex;",
	"after": "wWhichSprite = 0u;",
	"case_ids": ["Func_c6f7-1", "Func_c6f7-2", "Func_c6f7-3"],
}
# <<< factory-mutation Func_c6f7
