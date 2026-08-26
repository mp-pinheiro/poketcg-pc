"""Oracle-diff cases for poketcg/src/engine/menus/diary.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory _PauseMenu_Diary
CONTRACT["_PauseMenu_Diary"] = {"compare": (), "preserve": ()}
CASES["_PauseMenu_Diary"] = [
    {"keys": [0x00, 0x01], "setup": SETUP, "wram": {0xD291: b"\x5A"}, "read": {0xD291: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x01], setup=SETUP, wram={0xD291: b"\x5A"}, read={0xD291: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory _PauseMenu_Diary

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _PauseMenu_Diary
MUTATIONS["_PauseMenu_Diary"] = {"source_symbol": "_PauseMenu_Diary", "before": "void _PauseMenu_Diary(void)\n{\n\tuint8_t saved_d291 = wd291;", "after": "void _PauseMenu_Diary(void)\n{\n\tuint8_t saved_d291 = 0u;", "case_ids": ["_PauseMenu_Diary-0", "_PauseMenu_Diary-1"]}
# <<< factory-mutation _PauseMenu_Diary
