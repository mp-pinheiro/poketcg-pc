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

# >>> factory SetOverworldNPCFlags
CONTRACT["SetOverworldNPCFlags"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetOverworldNPCFlags"] = [
    {"wram": {0xD0C1: b"\x00"}},
    dict(POISON, a=0x0F, wram={0xD0C1: b"\xF0"}),
    {"a": 0x00, "wram": {0xD0C1: b"\x80"}},
]
# <<< factory SetOverworldNPCFlags

# >>> factory Func_c158
CONTRACT["Func_c158"] = {"compare": ("a",), "preserve": ()}
CASES["Func_c158"] = [
	{},  # all-zero: wActiveGameEvent=0 -> cp/r nz early return
	{"wram": {0xD0C2: b"\x01", 0xD3AB: b"\x00", 0xD0C4: b"\x42", 0xD0C5: b"\x0c", 0xD3AA: b"\x01"},
	 "read": {0xD0C2: 1, 0xD0C4: 1}},  # duel event: wTempNPC <- wNPCDuelist before FindLoadedNPC
	{"wram": {0xD0C2: b"\x02", 0xD3AB: b"\x77"}, "read": {0xD0C2: 1}},  # not duel -> early return, wTempNPC untouched
	dict(POISON, wram={0xD0C2: b"\x01", 0xD3AB: b"\x33", 0xD0C4: b"\x21", 0xD0C5: b"\x06"},
	     read={0xD0C2: 1, 0xD0C4: 1}),
]
# <<< factory Func_c158

# >>> factory Func_c184
CONTRACT["Func_c184"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c184"] = [
	{},  # all-zero: wCurMap=0 -> OWMODE_MAP written to both mode bytes
	{"wram": {0xD0BF: b"\x5a", 0xD0C0: b"\xa5"}, "read": {0xD32F: 1}},  # wCurMap=0 overwrites both with 00
	{"wram": {0xD32F: b"\x01", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, "read": {0xD32F: 1}},  # first nonzero map id
	{"wram": {0xD32F: b"\xff", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, "read": {0xD32F: 1}},
	dict(POISON, wram={0xD32F: b"\x02", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, read={0xD32F: 1}),
]
# <<< factory Func_c184

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
# >>> factory-mutation SetOverworldNPCFlags
MUTATIONS["SetOverworldNPCFlags"] = {"source_symbol": "SetOverworldNPCFlags", "before": "uint8_t value = (uint8_t)(a | wOverworldNPCFlags);", "after": "uint8_t value = (uint8_t)(a & wOverworldNPCFlags);", "case_ids": ["SetOverworldNPCFlags-1", "SetOverworldNPCFlags-2"]}
# <<< factory-mutation SetOverworldNPCFlags
# >>> factory-mutation Func_c158
MUTATIONS["Func_c158"] = {
	"source_symbol": "Func_c158",
	"before": "if (event != GAME_EVENT_DUEL)",
	"after": "if (event == GAME_EVENT_DUEL)",
	"case_ids": ["Func_c158-1", "Func_c158-2", "Func_c158-3"],
}
# <<< factory-mutation Func_c158
# >>> factory-mutation Func_c184
MUTATIONS["Func_c184"] = {
	"source_symbol": "Func_c184",
	"before": "if (wCurMap == OVERWORLD_MAP)",
	"after": "if (wCurMap != OVERWORLD_MAP)",
	"case_ids": ["Func_c184-1", "Func_c184-2", "Func_c184-3", "Func_c184-4"],
}
# <<< factory-mutation Func_c184
