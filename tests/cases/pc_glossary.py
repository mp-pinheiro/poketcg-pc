"""Oracle-diff cases for poketcg/src/engine/menus/pc_glossary.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory _PCMenu_Glossary
CONTRACT["_PCMenu_Glossary"] = {"compare": (), "preserve": ()}
CASES["_PCMenu_Glossary"] = [
    {"keys": [0x00, 0x02], "setup": SETUP, "wram": {0xCABB: b"\x00", 0xD291: b"\x5A"}, "read": {0xD291: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x02], setup=SETUP, wram={0xCABB: b"\x00", 0xD291: b"\x5A"}, read={0xD291: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory _PCMenu_Glossary

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _PCMenu_Glossary
MUTATIONS["_PCMenu_Glossary"] = {"source_symbol": "_PCMenu_Glossary", "before": "void _PCMenu_Glossary(void)\n{\n\tuint8_t saved_d291 = wd291;", "after": "void _PCMenu_Glossary(void)\n{\n\tuint8_t saved_d291 = 0u;", "case_ids": ["_PCMenu_Glossary-0", "_PCMenu_Glossary-1"]}
# <<< factory-mutation _PCMenu_Glossary
