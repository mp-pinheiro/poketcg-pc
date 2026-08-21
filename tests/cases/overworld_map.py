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
# <<< factory-cases-statics

# >>> factory OverworldMap_InitVolcanoSprite
CONTRACT["OverworldMap_InitVolcanoSprite"] = {"compare": (), "preserve": ()}
CASES["OverworldMap_InitVolcanoSprite"] = [
    {"f": 0x00, "wram": {H_BANK: b"\x04", CACHE_SIZE: b"\x00", wConsole: b"\x01", SPRITE_BUFFER: b"\x00" * 16}, "read": {CACHE_SIZE: 1, SPRITE_BUFFER: 16, wConsole: 1}},
    dict(POISON, wram={H_BANK: b"\x04", CACHE_SIZE: b"\x00", wConsole: b"\x02", SPRITE_BUFFER: b"\x00" * 16}, read={CACHE_SIZE: 1, SPRITE_BUFFER: 16, wConsole: 1}),
]
# <<< factory OverworldMap_InitVolcanoSprite

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
