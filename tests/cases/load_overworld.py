"""Oracle-diff cases for poketcg/src/engine/overworld/load_overworld.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory LoadMapTilesAndPals
CONTRACT["LoadMapTilesAndPals"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LoadMapTilesAndPals"] = [
    {"wram": {0xD32F: b"\x00", 0xD291: b"\x00"},
     "instruction_budget": 4000000, "cycle_budget": 16000000,
     "read": {0xD4CA: 1, 0xD4CB: 1}},
    dict(POISON, wram={0xD32F: b"\x00", 0xD291: b"\x00"},
         instruction_budget=4000000, cycle_budget=16000000,
         read={0xD4CA: 1, 0xD4CB: 1}),
]
# <<< factory LoadMapTilesAndPals

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation LoadMapTilesAndPals
MUTATIONS["LoadMapTilesAndPals"] = {"source_symbol": "LoadMapTilesAndPals", "before": "\twWhichBGPalIndex = wd291;\n\tuint8_t pal = wCurMapPalette;", "after": "\twWhichBGPalIndex = (uint8_t)(wd291 + 1u);\n\tuint8_t pal = wCurMapPalette;", "case_ids": ["LoadMapTilesAndPals-0", "LoadMapTilesAndPals-1"]}
# <<< factory-mutation LoadMapTilesAndPals
