"""Oracle-diff cases for poketcg/src/engine/unused_copyright.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
FRAME_SETUP = [{"fn": "CopyDMAFunction"}]
SCREEN_READ = {0xD61C: 2}
# <<< factory-cases-statics

# >>> factory UnusedCopyrightScreen
CONTRACT["UnusedCopyrightScreen"] = {"compare": (), "preserve": ()}
CASES["UnusedCopyrightScreen"] = [
    {"keys": [0x00, 0x01], "wram": {0xCAB4: b"\x00", 0xCABB: b"\x00", 0xFF40: b"\x00"}, "setup": FRAME_SETUP, "read": SCREEN_READ, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xCAB4: b"\x00", 0xCABB: b"\x00", 0xFF40: b"\x00"}, setup=FRAME_SETUP, read=SCREEN_READ, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory UnusedCopyrightScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation UnusedCopyrightScreen
MUTATIONS["UnusedCopyrightScreen"] = {"source_symbol": "UnusedCopyrightScreen", "before": "\t(void)LoadScene(SCENE_COPYRIGHT, 0u, 0u, 0u, 0u, 0u, 0u);", "after": "\t(void)LoadScene(SCENE_COPYRIGHT, 0u, 1u, 0u, 0u, 0u, 0u);", "case_ids": ["UnusedCopyrightScreen-0", "UnusedCopyrightScreen-1"]}
# <<< factory-mutation UnusedCopyrightScreen
