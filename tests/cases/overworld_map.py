"""Oracle-diff cases for poketcg/src/engine/overworld_map.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory OverworldMap_ContinuePlayerWalkingAnimation
CONTRACT["OverworldMap_ContinuePlayerWalkingAnimation"] = {"compare": ("b",), "preserve": ("b",)}
CASES["OverworldMap_ContinuePlayerWalkingAnimation"] = [
    {"wram": {0xD341: b"\x00\x00\x00\x00\x00\x00\x00\x00"}, "read": {0xC100: 0x900}},
    dict(POISON, wram={0xD341: b"\x01\x00\xFE\x03\x02\xFD\x05\xFF"}, read={0xC100: 0x900}),
    {"wram": {0xD341: b"\x00\x00\xFF\x01\xFF\x00\x00\x01"}, "read": {0xC100: 0x900}},
]
# <<< factory OverworldMap_ContinuePlayerWalkingAnimation

# >>> factory OverworldMap_NegateBC
CONTRACT["OverworldMap_NegateBC"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")};
CASES["OverworldMap_NegateBC"] = [
    {"b": 0x00, "c": 0x00},
    {"b": 0x00, "c": 0x01},
    {"b": 0x01, "c": 0x00},
    dict(POISON),
]
# <<< factory OverworldMap_NegateBC

# >>> factory-cases-statics
H_BANK = 0xFF80
CACHE_SIZE = 0xD618
SPRITE_BUFFER = 0xD4D0
wConsole = 0xCAB4

wOverworldMapCursorAnimation = 0xD33C
wOverworldMapCursorSprite = 0xD33B
wWhichSprite = 0xD4CF

wOverworldMapSelection = 0xD32E
wOverworldTransition = 0xD0B4
wTempMap = 0xD0BB
wTempPlayerXCoord = 0xD0BC
wTempPlayerYCoord = 0xD0BD
wTempPlayerDirection = 0xD0BE

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wOverworldMapPlayerMovementCounter = 0xD341
wOverworldMapPlayerPathHorizontalMovement = 0xD343
wOverworldMapPlayerPathVerticalMovement = 0xD345
wPlayerDirection = 0xD334

wOverworldMapSelection = 0xD32E
EVENT_VARS = 0xD3D2

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
wOverworldMapCursorAnimation = 0xD33C
wOverworldMapCursorSprite = 0xD33B
wOverworldMapPlayerAnimationState = 0xD33E
wOverworldMapSelection = 0xD32E
wOverworldMapStartingPosition = 0xD33D
wWhichSprite = 0xD4CF
wEventVars = 0xD3D2
SPRITE_BUFFER = 0xD4D0
# <<< factory-cases-statics

# >>> factory OverworldMap_InitVolcanoSprite
CONTRACT["OverworldMap_InitVolcanoSprite"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_InitVolcanoSprite"] = [
    {"f": 0x00, "wram": {H_BANK: b"\x04", CACHE_SIZE: b"\x00", wConsole: b"\x01", SPRITE_BUFFER: b"\x00" * 16}, "read": {CACHE_SIZE: 1, SPRITE_BUFFER: 16, wConsole: 1}},
    dict(POISON, wram={H_BANK: b"\x04", CACHE_SIZE: b"\x00", wConsole: b"\x02", SPRITE_BUFFER: b"\x00" * 16}, read={CACHE_SIZE: 1, SPRITE_BUFFER: 16, wConsole: 1}),
]
# <<< factory OverworldMap_InitVolcanoSprite

# >>> factory OverworldMap_UpdateCursorAnimation
CONTRACT["OverworldMap_UpdateCursorAnimation"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_UpdateCursorAnimation"] = [
    {"wram": {wOverworldMapCursorSprite: b"\x03", wOverworldMapCursorAnimation: b"\x10"}, "read": {wWhichSprite: 1}},
    {"wram": {wOverworldMapCursorSprite: b"\x00", wOverworldMapCursorAnimation: b"\xff"}, "read": {wWhichSprite: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wOverworldMapCursorSprite: b"\x7f", wOverworldMapCursorAnimation: b"\x80"}, "read": {wWhichSprite: 1}},
]
# <<< factory OverworldMap_UpdateCursorAnimation

# >>> factory OverworldMap_LoadSelectedMap
CONTRACT["OverworldMap_LoadSelectedMap"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_LoadSelectedMap"] = [
    {"wram": {wOverworldMapSelection: b"\x00", wOverworldTransition: b"\xa0", wTempMap: b"\xff", wTempPlayerXCoord: b"\xff", wTempPlayerYCoord: b"\xff", wTempPlayerDirection: b"\xff"}, "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1, wTempPlayerDirection: 1, wOverworldTransition: 1}},
    {"wram": {wOverworldMapSelection: b"\x01", wOverworldTransition: b"\x01", wTempMap: b"\x00", wTempPlayerXCoord: b"\x00", wTempPlayerYCoord: b"\x00", wTempPlayerDirection: b"\xff"}, "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1, wTempPlayerDirection: 1, wOverworldTransition: 1}},
    {"wram": {wOverworldMapSelection: b"\x0c", wOverworldTransition: b"\x00", wTempMap: b"\x55", wTempPlayerXCoord: b"\x55", wTempPlayerYCoord: b"\x55", wTempPlayerDirection: b"\x55"}, "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1, wTempPlayerDirection: 1, wOverworldTransition: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wOverworldMapSelection: b"\x02", wOverworldTransition: b"\x01", wTempMap: b"\x00", wTempPlayerXCoord: b"\x00", wTempPlayerYCoord: b"\x00", wTempPlayerDirection: b"\xff"}, "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1, wTempPlayerDirection: 1, wOverworldTransition: 1}},
]
# <<< factory OverworldMap_LoadSelectedMap

# >>> factory OverworldMap_InitPlayerEastWestMovement
CONTRACT["OverworldMap_InitPlayerEastWestMovement"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_InitPlayerEastWestMovement"] = [
    {"b": 0x04, "c": 0x01, "wram": {0xD343: b"\x00\x00", 0xD345: b"\x00\x00"}, "expect": {0xD341: b"\x04", 0xD343: b"\x40\x00", 0xD345: b"\x00\x01", 0xD334: b"\x01"}},
    {"b": 0x04, "c": 0x01, "wram": {0xD343: b"\x00\x80", 0xD345: b"\x00\x00"}, "expect": {0xD341: b"\x04", 0xD343: b"\x40\xff", 0xD345: b"\x00\x01", 0xD334: b"\x03"}},
    {"b": 0x04, "c": 0x01, "wram": {0xD343: b"\x00\x00", 0xD345: b"\x00\x80"}, "expect": {0xD341: b"\x04", 0xD343: b"\x40\x00", 0xD345: b"\xc0\xff", 0xD334: b"\x01"}},
    dict(POISON, wram={0xD343: b"\x12\x80", 0xD345: b"\x34\x80"}, expect={0xD341: b"\xbb", 0xD343: b"\x00\xff", 0xD345: b"\xe9\xfe", 0xD334: b"\x03"}),
]
# <<< factory OverworldMap_InitPlayerEastWestMovement

# >>> factory OverworldMap_GetOWMapID
CONTRACT["OverworldMap_GetOWMapID"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["OverworldMap_GetOWMapID"] = [
    {"wram": {wOverworldMapSelection: b"\x00"}},
    {"wram": {wOverworldMapSelection: b"\x01"}},
    {"wram": {wOverworldMapSelection: b"\x02", EVENT_VARS: b"\x00" * 64}},
    {"wram": {wOverworldMapSelection: b"\x02", EVENT_VARS: b"\xff" * 64}},
    dict(POISON, wram={wOverworldMapSelection: b"\x02", EVENT_VARS: b"\x00" * 64}),
]
# <<< factory OverworldMap_GetOWMapID

# >>> factory OverworldMap_InitCursorSprite
CONTRACT["OverworldMap_InitCursorSprite"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_InitCursorSprite"] = [
    {"wram": {wOverworldMapSelection: b"\x03", wConsole: b"\x01", wEventVars: b"\x00" * 64, SPRITE_BUFFER: b"\x00" * 16}, "read": {wOverworldMapStartingPosition: 1, wOverworldMapPlayerAnimationState: 1, wOverworldMapCursorSprite: 1, wOverworldMapCursorAnimation: 1, wWhichSprite: 1, SPRITE_BUFFER: 16}},
    {"wram": {wOverworldMapSelection: b"\x07", wConsole: b"\x02", wEventVars: b"\x00" * 64, SPRITE_BUFFER: b"\x00" * 16}, "read": {wOverworldMapStartingPosition: 1, wOverworldMapPlayerAnimationState: 1, wOverworldMapCursorSprite: 1, wOverworldMapCursorAnimation: 1, wWhichSprite: 1, SPRITE_BUFFER: 16}},
    {"wram": {wOverworldMapSelection: b"\x01", wConsole: b"\x01", wEventVars: b"\xFF" * 64, SPRITE_BUFFER: b"\x00" * 16}, "read": {wOverworldMapStartingPosition: 1, wOverworldMapPlayerAnimationState: 1, wOverworldMapCursorSprite: 1, wOverworldMapCursorAnimation: 1, wWhichSprite: 1, SPRITE_BUFFER: 16}},
    dict(POISON, wram={wOverworldMapSelection: b"\x02", wConsole: b"\x02", wEventVars: b"\x00" * 64, SPRITE_BUFFER: b"\x00" * 16}, read={wOverworldMapStartingPosition: 1, wOverworldMapPlayerAnimationState: 1, wOverworldMapCursorSprite: 1, wOverworldMapCursorAnimation: 1, wWhichSprite: 1, SPRITE_BUFFER: 16}),
]
# <<< factory OverworldMap_InitCursorSprite

# >>> factory OverworldMap_GetMapPosition
CONTRACT["OverworldMap_GetMapPosition"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")}
CASES["OverworldMap_GetMapPosition"] = [
	{"a": 0x00, "d": 0x00, "e": 0x00},
	{"a": 0x01, "d": 0x01, "e": 0x02},
	{"a": 0x0B, "d": 0x10, "e": 0x20},
	dict(POISON, a=0x02),
]
# <<< factory OverworldMap_GetMapPosition

# >>> factory OverworldMap_SetSpritePosition
CONTRACT["OverworldMap_SetSpritePosition"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_SetSpritePosition"] = [
    {"a": 0x01, "d": 0x02, "e": 0x03, "wram": {0xD4CF: b"\x00", 0xD4D0: b"\x99" * 16}, "expect": {0xD4D2: b"\x16", 0xD4D3: b"\x7B"}},
    dict(POISON, a=0x00, d=0x00, e=0x00, wram={0xD4CF: b"\x00", 0xD4D0: b"\x55" * 16}, expect={0xD4D2: b"\x08", 0xD4D3: b"\x10"})
]
# <<< factory OverworldMap_SetSpritePosition

# >>> factory OverworldMap_InitPlayerNorthSouthMovement
CONTRACT["OverworldMap_InitPlayerNorthSouthMovement"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_InitPlayerNorthSouthMovement"] = [
    {"b": 0x01, "c": 0x04, "wram": {0xD343: b"\x00\x00", 0xD345: b"\x00\x00"}, "expect": {0xD341: b"\x04", 0xD343: b"\x40\x00", 0xD345: b"\x00\x01", 0xD334: b"\x02"}},
    {"b": 0x01, "c": 0x04, "wram": {0xD343: b"\x00\xff", 0xD345: b"\x00\xff"}, "expect": {0xD341: b"\x04", 0xD343: b"\xc0\xff", 0xD345: b"\x00\xff", 0xD334: b"\x00"}},
    dict(POISON, b=0x01, c=0x04, wram={0xD343: b"\x00\x00", 0xD345: b"\x00\x00"}, expect={0xD341: b"\x04", 0xD343: b"\x40\x00", 0xD345: b"\x00\x01", 0xD334: b"\x02"}),
]
# <<< factory OverworldMap_InitPlayerNorthSouthMovement

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation OverworldMap_ContinuePlayerWalkingAnimation
MUTATIONS["OverworldMap_ContinuePlayerWalkingAnimation"] = {"source_symbol": "OverworldMap_ContinuePlayerWalkingAnimation", "before": "\twOverworldMapPlayerMovementCounter--;", "after": "\twOverworldMapPlayerMovementCounter++;", "case_ids": ["OverworldMap_ContinuePlayerWalkingAnimation-0", "OverworldMap_ContinuePlayerWalkingAnimation-1", "OverworldMap_ContinuePlayerWalkingAnimation-2"]}
# <<< factory-mutation OverworldMap_ContinuePlayerWalkingAnimation
# >>> factory-mutation OverworldMap_NegateBC
MUTATIONS["OverworldMap_NegateBC"] = {"source_symbol": "OverworldMap_NegateBC", "before": "\tuint16_t low_sum = (uint16_t)(c ^ 0xffu) + 1u;", "after": "\tuint16_t low_sum = (uint16_t)(c ^ 0xffu) + 2u;", "case_ids": ["OverworldMap_NegateBC-0", "OverworldMap_NegateBC-1", "OverworldMap_NegateBC-2", "OverworldMap_NegateBC-3"]}
# <<< factory-mutation OverworldMap_NegateBC
# >>> factory-mutation OverworldMap_InitVolcanoSprite
MUTATIONS["OverworldMap_InitVolcanoSprite"] = {"source_symbol": "OverworldMap_InitVolcanoSprite", "before": "uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);", "after": "uint16_t coords = GetSpriteAnimBufferProperty((uint8_t)(SPRITE_ANIM_COORD_X + 1u));", "case_ids": ["OverworldMap_InitVolcanoSprite-0", "OverworldMap_InitVolcanoSprite-1"]}
# <<< factory-mutation OverworldMap_InitVolcanoSprite
# >>> factory-mutation OverworldMap_UpdateCursorAnimation
MUTATIONS["OverworldMap_UpdateCursorAnimation"] = {"source_symbol": "OverworldMap_UpdateCursorAnimation", "before": "\twWhichSprite = wOverworldMapCursorSprite;", "after": "\twWhichSprite = (uint8_t)(wOverworldMapCursorSprite + 1u);", "case_ids": ["OverworldMap_UpdateCursorAnimation-0", "OverworldMap_UpdateCursorAnimation-1", "OverworldMap_UpdateCursorAnimation-2"]};
# <<< factory-mutation OverworldMap_UpdateCursorAnimation
# >>> factory-mutation OverworldMap_LoadSelectedMap
MUTATIONS["OverworldMap_LoadSelectedMap"] = {"source_symbol": "OverworldMap_LoadSelectedMap", "before": "	uint8_t selection = wOverworldMapSelection;", "after": "	uint8_t selection = (uint8_t)(wOverworldMapSelection + 1u);", "case_ids": ["OverworldMap_LoadSelectedMap-0", "OverworldMap_LoadSelectedMap-1", "OverworldMap_LoadSelectedMap-2", "OverworldMap_LoadSelectedMap-3"]}
# <<< factory-mutation OverworldMap_LoadSelectedMap
# >>> factory-mutation OverworldMap_InitPlayerEastWestMovement
MUTATIONS["OverworldMap_InitPlayerEastWestMovement"] = {"source_symbol": "OverworldMap_InitPlayerEastWestMovement", "before": "\tDivResult divided = DivideBCbyDE((uint16_t)((uint16_t)c << 8), (uint16_t)b);", "after": "\tDivResult divided = DivideBCbyDE((uint16_t)((uint16_t)c << 8), (uint16_t)(b + 1u));", "case_ids": ["OverworldMap_InitPlayerEastWestMovement-0", "OverworldMap_InitPlayerEastWestMovement-1", "OverworldMap_InitPlayerEastWestMovement-2", "OverworldMap_InitPlayerEastWestMovement-3"]}
# <<< factory-mutation OverworldMap_InitPlayerEastWestMovement
# >>> factory-mutation OverworldMap_GetOWMapID
MUTATIONS["OverworldMap_GetOWMapID"] = {"source_symbol": "OverworldMap_GetOWMapID", "before": "\tif (selection != OWMAP_ISHIHARAS_HOUSE)", "after": "\tif (selection == OWMAP_ISHIHARAS_HOUSE)", "case_ids": ["OverworldMap_GetOWMapID-0", "OverworldMap_GetOWMapID-1", "OverworldMap_GetOWMapID-2", "OverworldMap_GetOWMapID-3", "OverworldMap_GetOWMapID-4"]}
# <<< factory-mutation OverworldMap_GetOWMapID
# >>> factory-mutation OverworldMap_InitCursorSprite
MUTATIONS["OverworldMap_InitCursorSprite"] = {"source_symbol": "OverworldMap_InitCursorSprite", "before": "\tuint16_t flags = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);", "after": "\tuint16_t flags = GetSpriteAnimBufferProperty((uint8_t)(SPRITE_ANIM_FLAGS + 1u));", "case_ids": ["OverworldMap_InitCursorSprite-0", "OverworldMap_InitCursorSprite-1", "OverworldMap_InitCursorSprite-2", "OverworldMap_InitCursorSprite-3"]}
# <<< factory-mutation OverworldMap_InitCursorSprite
# >>> factory-mutation OverworldMap_GetMapPosition
MUTATIONS["OverworldMap_GetMapPosition"] = {"source_symbol": "OverworldMap_GetMapPosition", "before": "\t\t.d = x,", "after": "\t\t.d = (uint8_t)(x + 1u),", "case_ids": ["OverworldMap_GetMapPosition-0", "OverworldMap_GetMapPosition-1", "OverworldMap_GetMapPosition-2", "OverworldMap_GetMapPosition-3"]}
# <<< factory-mutation OverworldMap_GetMapPosition
# >>> factory-mutation OverworldMap_SetSpritePosition
MUTATIONS["OverworldMap_SetSpritePosition"] = {"source_symbol": "OverworldMap_SetSpritePosition", "before": "\tgb_write8((uint16_t)(hl + 1u), position.e);", "after": "\tgb_write8((uint16_t)(hl + 1u), (uint8_t)(position.e + 1u));", "case_ids": ["OverworldMap_SetSpritePosition-0", "OverworldMap_SetSpritePosition-1"]}
# <<< factory-mutation OverworldMap_SetSpritePosition
# >>> factory-mutation OverworldMap_InitPlayerNorthSouthMovement
MUTATIONS["OverworldMap_InitPlayerNorthSouthMovement"] = {"source_symbol": "OverworldMap_InitPlayerNorthSouthMovement", "before": "\tDivResult divided = DivideBCbyDE((uint16_t)((uint16_t)b << 8), (uint16_t)c);", "after": "\tDivResult divided = DivideBCbyDE((uint16_t)((uint16_t)b << 8), (uint16_t)(c + 1u));", "case_ids": ["OverworldMap_InitPlayerNorthSouthMovement-0", "OverworldMap_InitPlayerNorthSouthMovement-1", "OverworldMap_InitPlayerNorthSouthMovement-2"]}
# <<< factory-mutation OverworldMap_InitPlayerNorthSouthMovement
