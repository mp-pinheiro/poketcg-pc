"""Oracle-diff cases for poketcg/src/engine/overworld/load_overworld.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory LoadMapTilesAndPals
CONTRACT["LoadMapTilesAndPals"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LoadMapTilesAndPals"] = [
    {"wram": {sym("wCurMap"): b"\x00", sym("wd291"): b"\x00"},
     "instruction_budget": 4000000, "cycle_budget": 16000000,
     "read": {sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1}},
    dict(POISON, wram={sym("wCurMap"): b"\x00", sym("wd291"): b"\x00"},
         instruction_budget=4000000, cycle_budget=16000000,
         read={sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1}),
]
# <<< factory LoadMapTilesAndPals

# >>> factory ReloadMapAfterTextClose
CONTRACT["ReloadMapAfterTextClose"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ReloadMapAfterTextClose"] = [
    {"wram": {sym("wBoosterViableCardList"): b"\x00" * 0x100}, "read": {sym("wBoosterViableCardList"): 0x100}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wBoosterViableCardList"): b"\xFF" * 0x100}, read={sym("wBoosterViableCardList"): 0x100}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ReloadMapAfterTextClose

# >>> factory LoadMapGfxAndPermissions
CONTRACT["LoadMapGfxAndPermissions"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LoadMapGfxAndPermissions"] = [
    {"wram": {sym("wCurMap"): b"\x01"}, "read": {sym("wTextBoxFrameType"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wCurMap"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {sym("wTextBoxFrameType"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wCurMap"): b"\x01"}, read={sym("wTextBoxFrameType"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LoadMapGfxAndPermissions

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation LoadMapTilesAndPals
MUTATIONS["LoadMapTilesAndPals"] = {"source_symbol": "LoadMapTilesAndPals", "before": "\twWhichBGPalIndex = wd291;\n\tuint8_t pal = wCurMapPalette;", "after": "\twWhichBGPalIndex = (uint8_t)(wd291 + 1u);\n\tuint8_t pal = wCurMapPalette;", "case_ids": ["LoadMapTilesAndPals-0", "LoadMapTilesAndPals-1"]}
# <<< factory-mutation LoadMapTilesAndPals
# >>> factory-mutation ReloadMapAfterTextClose
MUTATIONS["ReloadMapAfterTextClose"] = {"source_symbol": "ReloadMapAfterTextClose", "before": "\tFunc_c3ee();", "after": "\tFunc_c3ff();", "case_ids": ["ReloadMapAfterTextClose-1"]}
# <<< factory-mutation ReloadMapAfterTextClose
# >>> factory-mutation LoadMapGfxAndPermissions
MUTATIONS["LoadMapGfxAndPermissions"] = {"source_symbol": "LoadMapGfxAndPermissions", "before": "void LoadMapGfxAndPermissions(void)\n{\n\tClearSRAMBGMaps();\n\twTextBoxFrameType = 0u;", "after": "void LoadMapGfxAndPermissions(void)\n{\n\tClearSRAMBGMaps();\n\twTextBoxFrameType = 1u;", "case_ids": ["LoadMapGfxAndPermissions-0", "LoadMapGfxAndPermissions-1", "LoadMapGfxAndPermissions-2"]}
# <<< factory-mutation LoadMapGfxAndPermissions
