"""Oracle-diff cases for poketcg/src/engine/menus/deck_selection.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetPointerToDeckCards
CONTRACT["GetPointerToDeckCards"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["GetPointerToDeckCards"] = [
	{},
	{"wram": {0xCEB1: b"\x01"}},
	{"wram": {0xCEB1: b"\xFF"}},
	dict(POISON, wram={0xCEB1: b"\x02"}),
]
# <<< factory GetPointerToDeckCards

# >>> factory ResetCheckMenuCursorPositionAndBlink
CONTRACT["ResetCheckMenuCursorPositionAndBlink"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ResetCheckMenuCursorPositionAndBlink"] = [
	{"wram": {0xCEA3: b"\x00", 0xCEAF: b"\x00", 0xCEB0: b"\x00"}},
	dict(POISON, wram={0xCEA3: b"\x11", 0xCEAF: b"\x22", 0xCEB0: b"\x33"}),
]
# <<< factory ResetCheckMenuCursorPositionAndBlink

# >>> factory-cases-statics
wCurDeck = 0xCEB1
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sHasPromotionalCards = 0xB703
sUnnamedDeckCounter = 0xB701

wConsole = 0xCAB4
wTileMapFill = 0xCAB6
wVBlankOAMCopyToggle = 0xCAC0
wLCDC = 0xCABB

wCurDeck = 0xCEB1
# <<< factory-cases-statics

# >>> factory GetPointerToDeckName
CONTRACT["GetPointerToDeckName"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetPointerToDeckName"] = [
    {"wram": {wCurDeck: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "hl": 0xA200}},
    dict(POISON, wram={wCurDeck: b"\x01"}, expect_regs={"a": 0x00, "f": 0x80, "hl": 0xA254}),
]
# <<< factory GetPointerToDeckName

# >>> factory InitDeckBuildingParams
CONTRACT["InitDeckBuildingParams"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c",)}
CASES["InitDeckBuildingParams"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x50\x04\x01\x34\x12\x78\x56"}, "read": {0xC100: 7}},
    dict(POISON, hl=0xC100, wram={0xC100: b"\x01\x23\x45\x67\x89\xAB\xCD"}, read={0xC100: 7}),
    {"a": 0xFF, "f": 0x01, "c": 0x7E, "d": 0x11, "e": 0x22, "hl": 0xC1F8,
     "wram": {0xC1F8: b"\xFF\x00\x80\x7F\xAA\x55\x33"}, "read": {0xC1F8: 7}},
]
# <<< factory InitDeckBuildingParams

# >>> factory CheckIfCurDeckIsValid
CONTRACT["CheckIfCurDeckIsValid"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["CheckIfCurDeckIsValid"] = [
    {"wram": {0xCEB1: b"\x00", 0xCEB2: b"\x00"}},
    {"wram": {0xCEB1: b"\x02", 0xCEB2: b"\x00\x00\x01"}},
    dict(POISON, wram={0xCEB1: b"\x01", 0xCEB2: b"\x00\x00"}, expect_regs={"a": 0x00, "f": 0x90, "b": 0x00, "c": 0x01, "d": 0xDD, "e": 0xEE, "hl": 0xCEB3}),
]
# <<< factory CheckIfCurDeckIsValid

# >>> factory CancelDeckSelectionSubMenu
CONTRACT["CancelDeckSelectionSubMenu"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CancelDeckSelectionSubMenu"] = [
	{"wram": {0xCEB1: b"\x00"}},
	dict(POISON, wram={0xCEB1: b"\x7F"}),
]
# <<< factory CancelDeckSelectionSubMenu

# >>> factory CopyDeckFromSRAM
CONTRACT["CopyDeckFromSRAM"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": ()}
CASES["CopyDeckFromSRAM"] = [
    {"d": 0xA0, "e": 0x00, "hl": 0xC500, "sram": {0: {0xA000: bytes(range(60))}}, "wram": {0xC500: bytes(61)}, "read": {0xC500: 61}},
    dict(POISON, d=0xA0, e=0x00, hl=0xC500, sram={0: {0xA000: bytes(range(60))}}, wram={0xC500: bytes(61)}, read={0xC500: 61}),
]
# <<< factory CopyDeckFromSRAM

# >>> factory Func_9001
CONTRACT["Func_9001"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["Func_9001"] = [
    {"hl": 257, "read": {0xD00A: 3}},
    dict(POISON, hl=257, read={0xD00A: 3}),
    {"hl": 999, "read": {0xD00A: 3}},
    {"hl": 5, "read": {0xD00A: 3}},
]
# <<< factory Func_9001

# >>> factory LoadHandCardsIcon
CONTRACT["LoadHandCardsIcon"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["LoadHandCardsIcon"] = [
    {"vread": {0: {0x9380: 32}}},
    dict(POISON),
]
# <<< factory LoadHandCardsIcon

# >>> factory InitPromotionalCardAndDeckCounterSaveData
CONTRACT["InitPromotionalCardAndDeckCounterSaveData"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["InitPromotionalCardAndDeckCounterSaveData"] = [
    {"sram": {0: {sHasPromotionalCards: b"\xFF\xFF\xFF\xFF", sUnnamedDeckCounter: b"\xFF"}},
     "vread": {0: {0x9380: 32}}, "sread": {0: {sHasPromotionalCards: 4, sUnnamedDeckCounter: 1}}},
    dict(POISON, sram={0: {sHasPromotionalCards: b"\x00\x00\x00\x00", sUnnamedDeckCounter: b"\x00"}},
         vread={0: {0x9380: 32}}, sread={0: {sHasPromotionalCards: 4, sUnnamedDeckCounter: 1}}),
]
# <<< factory InitPromotionalCardAndDeckCounterSaveData

# >>> factory PrepareMenuGraphics
CONTRACT["PrepareMenuGraphics"] = {"compare": (), "preserve": ()}
CASES["PrepareMenuGraphics"] = [
    {"wram": {wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
     "read": {wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32}}},
    dict(POISON, wram={wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
         read={wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32}}),
]
# <<< factory PrepareMenuGraphics

# >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons
CONTRACT["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = {"compare": (), "preserve": ()}
CASES["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = [
    {"wram": {wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
     "read": {wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "vread": {0: {0x8D00: 768, 0x9000: 896, 0x9380: 32}}},
    dict(POISON, wram={wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
         read={wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         vread={0: {0x8D00: 768, 0x9000: 896, 0x9380: 32}}),
]
# <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons

# >>> factory PrintThereIsNoDeckHereText
CONTRACT["PrintThereIsNoDeckHereText"] = {"compare": ("a",), "preserve": ()}
CASES["PrintThereIsNoDeckHereText"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "keys": 0x01, "wram": {wCurDeck: b"\x02"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         keys=0x01, wram={wCurDeck: b"\x03"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintThereIsNoDeckHereText

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetPointerToDeckCards
MUTATIONS["GetPointerToDeckCards"] = {"source_symbol": "GetPointerToDeckCards", "before": "#define DECK_CARD_STRIDE 0x54u", "after": "#define DECK_CARD_STRIDE 0x55u", "case_ids": ["GetPointerToDeckCards-1", "GetPointerToDeckCards-2", "GetPointerToDeckCards-3"]}
# <<< factory-mutation GetPointerToDeckCards
# >>> factory-mutation ResetCheckMenuCursorPositionAndBlink
MUTATIONS["ResetCheckMenuCursorPositionAndBlink"] = {"source_symbol": "ResetCheckMenuCursorPositionAndBlink", "before": "\twCheckMenuCursorYPosition = 0u;", "after": "\twCheckMenuCursorXPosition = 0u;", "case_ids": ["ResetCheckMenuCursorPositionAndBlink-1"]}
# <<< factory-mutation ResetCheckMenuCursorPositionAndBlink
# >>> factory-mutation GetPointerToDeckName
MUTATIONS["GetPointerToDeckName"] = {"source_symbol": "GetPointerToDeckName", "before": "\treturn (uint16_t)(sDeck1Name_ADDR + offset);", "after": "\treturn (uint16_t)(sDeck1Name_ADDR + offset + 1u);", "case_ids": ["GetPointerToDeckName-0", "GetPointerToDeckName-1"]}
# <<< factory-mutation GetPointerToDeckName
# >>> factory-mutation InitDeckBuildingParams
MUTATIONS["InitDeckBuildingParams"] = {"source_symbol": "InitDeckBuildingParams", "before": "for (uint8_t i = 0; i < 7u; i++)", "after": "for (uint8_t i = 0; i < 6u; i++)", "case_ids": ["InitDeckBuildingParams-0", "InitDeckBuildingParams-1", "InitDeckBuildingParams-2"]}
# <<< factory-mutation InitDeckBuildingParams
# >>> factory-mutation CheckIfCurDeckIsValid
MUTATIONS["CheckIfCurDeckIsValid"] = {"source_symbol": "CheckIfCurDeckIsValid", "before": "\tuint8_t value = gb_read8(hl);", "after": "\tuint8_t value = (uint8_t)(gb_read8(hl) ^ 1u);", "case_ids": ["CheckIfCurDeckIsValid-0", "CheckIfCurDeckIsValid-1", "CheckIfCurDeckIsValid-2"]}
# <<< factory-mutation CheckIfCurDeckIsValid
# >>> factory-mutation CancelDeckSelectionSubMenu
MUTATIONS["CancelDeckSelectionSubMenu"] = {"source_symbol": "CancelDeckSelectionSubMenu", "before": "\treturn;", "after": "\tgb_write8(wCurDeck_ADDR, (uint8_t)(gb_read8(wCurDeck_ADDR) + 1u));", "case_ids": ["CancelDeckSelectionSubMenu-0", "CancelDeckSelectionSubMenu-1"]}
# <<< factory-mutation CancelDeckSelectionSubMenu
# >>> factory-mutation CopyDeckFromSRAM
MUTATIONS["CopyDeckFromSRAM"] = {"source_symbol": "CopyDeckFromSRAM", "before": "\tfor (uint8_t i = 0; i < DECK_SIZE; i++) {", "after": "\tfor (uint8_t i = 0; i < (uint8_t)(DECK_SIZE - 1u); i++) {", "case_ids": ["CopyDeckFromSRAM-0", "CopyDeckFromSRAM-1"]}
# <<< factory-mutation CopyDeckFromSRAM
# >>> factory-mutation Func_9001
MUTATIONS["Func_9001"] = {"source_symbol": "Func_9001", "before": "\tstatic const uint16_t steps[3] = {(uint16_t)-100, (uint16_t)-10, (uint16_t)-1};", "after": "\tstatic const uint16_t steps[3] = {(uint16_t)-100, (uint16_t)-10, (uint16_t)-2};", "case_ids": ["Func_9001-0", "Func_9001-2"]}
# <<< factory-mutation Func_9001
# >>> factory-mutation LoadHandCardsIcon
MUTATIONS["LoadHandCardsIcon"] = {"source_symbol": "LoadHandCardsIcon", "before": "\tuint16_t de = v0Tiles2_dest;", "after": "\tuint16_t de = (uint16_t)(v0Tiles2_dest + 1u);", "case_ids": ["LoadHandCardsIcon-0"]}
# <<< factory-mutation LoadHandCardsIcon
# >>> factory-mutation InitPromotionalCardAndDeckCounterSaveData
MUTATIONS["InitPromotionalCardAndDeckCounterSaveData"] = {"source_symbol": "InitPromotionalCardAndDeckCounterSaveData", "before": "\tgb_write8(sUnnamedDeckCounter_ADDR, 1u);", "after": "\tgb_write8(sUnnamedDeckCounter_ADDR, 0u);", "case_ids": ["InitPromotionalCardAndDeckCounterSaveData-0", "InitPromotionalCardAndDeckCounterSaveData-1"]}
# <<< factory-mutation InitPromotionalCardAndDeckCounterSaveData
# >>> factory-mutation PrepareMenuGraphics
MUTATIONS["PrepareMenuGraphics"] = {"source_symbol": "PrepareMenuGraphics", "before": "\twVBlankOAMCopyToggle = TRUE;", "after": "\twVBlankOAMCopyToggle = 0u;", "case_ids": ["PrepareMenuGraphics-0", "PrepareMenuGraphics-1"]}
# <<< factory-mutation PrepareMenuGraphics
# >>> factory-mutation EmptyScreenAndLoadFontDuelAndHandCardsIcons
MUTATIONS["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = {"source_symbol": "EmptyScreenAndLoadFontDuelAndHandCardsIcons", "before": "\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = TRUE;", "after": "\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = 0u;", "case_ids": ["EmptyScreenAndLoadFontDuelAndHandCardsIcons-0", "EmptyScreenAndLoadFontDuelAndHandCardsIcons-1"]}
# <<< factory-mutation EmptyScreenAndLoadFontDuelAndHandCardsIcons
# >>> factory-mutation PrintThereIsNoDeckHereText
MUTATIONS["PrintThereIsNoDeckHereText"] = {"source_symbol": "PrintThereIsNoDeckHereText", "before": "\treturn wCurDeck;", "after": "\treturn (uint8_t)(wCurDeck + 1u);", "case_ids": ["PrintThereIsNoDeckHereText-0", "PrintThereIsNoDeckHereText-1"]}
# <<< factory-mutation PrintThereIsNoDeckHereText
