"""Oracle-diff cases for poketcg/src/home/duel_menus.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
hBankROM_A = 0xFF80
wCheckMenuPlayAreaWhichLayout = 0xCE51
wTileMapFill = 0xCEC7
wVBlankOAMCopyToggle = 0xCAC0
# <<< factory-cases-statics

# >>> factory DrawPlayersPrizeAndBenchCards
CONTRACT["DrawPlayersPrizeAndBenchCards"] = {"compare": (), "preserve": ()}
CASES["DrawPlayersPrizeAndBenchCards"] = [
    {"wram": {hBankROM_A: b"\x01"}, "instruction_budget": 1000000, "cycle_budget": 4000000,
     "read": {hBankROM_A: 1, wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "expect": {hBankROM_A: b"\x01", wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}},
    dict(POISON, wram={hBankROM_A: b"\x01"}, instruction_budget=1000000, cycle_budget=4000000,
         read={hBankROM_A: 1, wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         expect={hBankROM_A: b"\x01", wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}),
]
# <<< factory DrawPlayersPrizeAndBenchCards

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DrawPlayersPrizeAndBenchCards
MUTATIONS["DrawPlayersPrizeAndBenchCards"] = {"source_symbol": "DrawPlayersPrizeAndBenchCards", "before": "\tBankswitchROM(saved_bank);", "after": "\tBankswitchROM(0u);", "case_ids": ["DrawPlayersPrizeAndBenchCards-0", "DrawPlayersPrizeAndBenchCards-1"]}
# <<< factory-mutation DrawPlayersPrizeAndBenchCards
