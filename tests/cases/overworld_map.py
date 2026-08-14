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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation OverworldMap_ContinuePlayerWalkingAnimation
MUTATIONS["OverworldMap_ContinuePlayerWalkingAnimation"] = {"source_symbol": "OverworldMap_ContinuePlayerWalkingAnimation", "before": "\twOverworldMapPlayerMovementCounter--;", "after": "\twOverworldMapPlayerMovementCounter++;", "case_ids": ["OverworldMap_ContinuePlayerWalkingAnimation-0", "OverworldMap_ContinuePlayerWalkingAnimation-1", "OverworldMap_ContinuePlayerWalkingAnimation-2"]}
# <<< factory-mutation OverworldMap_ContinuePlayerWalkingAnimation
