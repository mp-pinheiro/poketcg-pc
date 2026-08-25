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

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hBankROM_B = 0xFF80
hWhoseTurn_B = 0xFF97
wCheckMenuPlayAreaWhichDuelist_B = 0xCE50
wCheckMenuPlayAreaWhichLayout_B = 0xCE51
wDefaultText_B = 0xC590

hBankROM = 0xFF80
hWhoseTurn = 0xFF97
wDefaultText = 0xC590
wVBlankOAMCopyToggle = 0xCAC0
wYourOrOppPlayAreaCurPosition = 0xCE52
wMenuInputTablePointer = 0xCE53
wIsSwapTurnPending = 0xCE56
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

# >>> factory DrawPlayAreaToPlacePrizeCards
CONTRACT["DrawPlayAreaToPlacePrizeCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawPlayAreaToPlacePrizeCards"] = [
    {"instruction_budget": 2000000, "cycle_budget": 8000000,
     "hram": {0xFF80: b"\x01", 0xFF97: b"\xC2"},
     "wram": {0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00"},
     "read": {0xFF80: 1, 0xCE51: 1, 0xCE56: 1},
     "expect": {0xFF80: b"\x01"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=2000000, cycle_budget=8000000,
         hram={0xFF80: b"\x37", 0xFF97: b"\xC2"},
         wram={0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00"},
         read={0xFF80: 1, 0xCE51: 1, 0xCE56: 1},
         expect={0xFF80: b"\x37"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawPlayAreaToPlacePrizeCards

# >>> factory DrawYourOrOppPlayAreaScreen_Bank0
CONTRACT["DrawYourOrOppPlayAreaScreen_Bank0"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayAreaScreen_Bank0"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM_B: b"\x01", hWhoseTurn_B: b"\xC2"},
     "wram": {wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText_B: b"\x00" * 16},
     "read": {hBankROM_B: 1, wCheckMenuPlayAreaWhichDuelist_B: 1, wCheckMenuPlayAreaWhichLayout_B: 1},
     "expect": {hBankROM_B: b"\x01", wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "hl": 0xC2C2},
    dict(POISON, hl=0xC2C2, instruction_budget=20000000, cycle_budget=80000000,
         hram={hBankROM_B: b"\x37", hWhoseTurn_B: b"\xC2"},
         wram={wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText_B: b"\x00" * 16},
         read={hBankROM_B: 1, wCheckMenuPlayAreaWhichDuelist_B: 1, wCheckMenuPlayAreaWhichLayout_B: 1},
         expect={hBankROM_B: b"\x37", wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayAreaScreen_Bank0

# >>> factory DrawAIPeekScreen
CONTRACT["DrawAIPeekScreen"] = {"compare": ("a", "f"), "preserve": ("f",)}
CASES["DrawAIPeekScreen"] = [
    {"keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM: b"\x01", hWhoseTurn: b"\xC2"},
     "wram": {0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
     "read": {hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         hram={hBankROM: b"\x37", hWhoseTurn: b"\xC2"},
         wram={0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
         read={hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
         vread={0: {0x9800: 32, 0x9C00: 32}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
    {"a": 0xFF, "f": 0x00, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM: b"\x02", hWhoseTurn: b"\xC2"},
     "wram": {0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
     "read": {hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]}]
# <<< factory DrawAIPeekScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DrawPlayersPrizeAndBenchCards
MUTATIONS["DrawPlayersPrizeAndBenchCards"] = {"source_symbol": "DrawPlayersPrizeAndBenchCards", "before": "\tBankswitchROM(saved_bank);", "after": "\tBankswitchROM(0u);", "case_ids": ["DrawPlayersPrizeAndBenchCards-0", "DrawPlayersPrizeAndBenchCards-1"]}
# <<< factory-mutation DrawPlayersPrizeAndBenchCards
# >>> factory-mutation DrawPlayAreaToPlacePrizeCards
MUTATIONS["DrawPlayAreaToPlacePrizeCards"] = {
    "source_symbol": "DrawPlayAreaToPlacePrizeCards",
    "before": "\t_DrawPlayAreaToPlacePrizeCards();\n\tBankswitchROM(saved_bank);",
    "after": "\t_DrawPlayAreaToPlacePrizeCards();\n\tBankswitchROM((uint8_t)(saved_bank ^ 1u));",
    "case_ids": ["DrawPlayAreaToPlacePrizeCards-0", "DrawPlayAreaToPlacePrizeCards-1"],
}
# <<< factory-mutation DrawPlayAreaToPlacePrizeCards
# >>> factory-mutation DrawYourOrOppPlayAreaScreen_Bank0
MUTATIONS["DrawYourOrOppPlayAreaScreen_Bank0"] = {"source_symbol": "DrawYourOrOppPlayAreaScreen_Bank0", "before": "\t(void)DrawWideTextBox();\n\tBankswitchROM(saved_bank);", "after": "\t(void)DrawWideTextBox();\n\tBankswitchROM(0u);", "case_ids": ["DrawYourOrOppPlayAreaScreen_Bank0-0", "DrawYourOrOppPlayAreaScreen_Bank0-1"]}
# <<< factory-mutation DrawYourOrOppPlayAreaScreen_Bank0
# >>> factory-mutation DrawAIPeekScreen
MUTATIONS["DrawAIPeekScreen"] = {"source_symbol": "DrawAIPeekScreen", "before": "\tBankswitchROM(saved_bank);\n\treturn (DrawAIPeekScreenResult){saved_bank, f};", "after": "\tBankswitchROM((uint8_t)(saved_bank ^ 1u));\n\treturn (DrawAIPeekScreenResult){saved_bank, f};", "case_ids": ["DrawAIPeekScreen-0", "DrawAIPeekScreen-1"]}
# <<< factory-mutation DrawAIPeekScreen
