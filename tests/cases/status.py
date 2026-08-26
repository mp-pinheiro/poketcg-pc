"""Oracle-diff cases for poketcg/src/engine/menus/status.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
wMedalScreenYOffset = 0xD114
# <<< factory-cases-statics

# >>> factory _PauseMenu_Status
CONTRACT["_PauseMenu_Status"] = {"compare": (), "preserve": ()}
CASES["_PauseMenu_Status"] = [
    {"keys": [0x00, 0x01], "setup": SETUP, "wram": {0xCABB: b"\x00", 0xD291: b"\x5A"}, "read": {0xD291: 1, 0xD114: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x01], setup=SETUP, wram={0xCABB: b"\x00", 0xD291: b"\x5A"}, read={0xD291: 1, 0xD114: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory _PauseMenu_Status

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _PauseMenu_Status
MUTATIONS["_PauseMenu_Status"] = {"source_symbol": "_PauseMenu_Status", "before": "void _PauseMenu_Status(void)\n{\n\tuint8_t saved_d291 = wd291;", "after": "void _PauseMenu_Status(void)\n{\n\tuint8_t saved_d291 = 0u;", "case_ids": ["_PauseMenu_Status-0", "_PauseMenu_Status-1"]}
# <<< factory-mutation _PauseMenu_Status
