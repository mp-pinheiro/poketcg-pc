"""Oracle-diff cases for poketcg/src/engine/duel/core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetLineSeparation
CONTRACT["SetLineSeparation"] = {"compare": ("a",), "preserve": ()}
wLineSeparation = 0xCD08
CASES["SetLineSeparation"] = [
	{"a": 0, "wram": {wLineSeparation: b"\xff"}},
	{"a": 1, "wram": {wLineSeparation: b"\x00"}},
	dict(POISON, a=0x20, wram={wLineSeparation: b"\x00"}),
]
# <<< factory SetLineSeparation

# >>> factory PlayAreaScreenMenuFunction
CONTRACT["PlayAreaScreenMenuFunction"] = {"compare": ("f",), "preserve": ()}
CASES["PlayAreaScreenMenuFunction"] = [
    {"keys": 0},
    {"keys": 0x01},
    {"keys": 0x02},
    {"keys": 0x08},
    dict(POISON, keys=0x02),
    dict(POISON, keys=0x00),
]
# <<< factory PlayAreaScreenMenuFunction

# >>> factory SwitchAttackPage
CONTRACT["SwitchAttackPage"] = {"compare": (), "preserve": ()}
CASES["SwitchAttackPage"] = [
	{"wram": {0xCC04: b"\x00"}, "read": {0xCC04: 1}},
	{"wram": {0xCC04: b"\x01"}, "read": {0xCC04: 1}},
	dict(POISON, wram={0xCC04: b"\xff"}, read={0xCC04: 1}),
]
# <<< factory SwitchAttackPage

# >>> factory CopyCGBCardPalette
CONTRACT["CopyCGBCardPalette"] = {"compare": (), "preserve": ()}
CASES["CopyCGBCardPalette"] = [
    {"wram": {0xCE23: bytes(range(8))}, "read": {0xCAF0: 8}},
    dict(POISON, a=2, wram={0xCE23: bytes(range(0x10, 0x18))},
         read={0xCAF0 + 16: 8}),
]
# <<< factory CopyCGBCardPalette

# >>> factory CreateCardAttrBlkPacket_DataSet
CONTRACT["CreateCardAttrBlkPacket_DataSet"] = {"compare": ("hl",), "preserve": (), "wram_out": True}
CASES["CreateCardAttrBlkPacket_DataSet"] = [
    {"hl": 0xC100, "a": 0, "d": 0, "e": 0, "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
    dict(POISON, hl=0xC100, wram={0xC100: b"\x00" * 6}, read={0xC100: 6}),
    {"hl": 0xC100, "a": 0x12, "d": 0x30, "e": 0x40, "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
]
# <<< factory CreateCardAttrBlkPacket_DataSet

# >>> factory SaveDuelDataToDE
CONTRACT["SaveDuelDataToDE"] = {"compare": (), "preserve": ()}
sCurrentDuel = 0xBC00
sCurrentDuelData = 0xBC04
wDuelType = 0xCC09
wPlayerDuelVariables = 0xC200
CASES["SaveDuelDataToDE"] = [
	{"d": 0xBC, "e": 0x00, "wram": {wDuelType: b"\x02"}, "sread": {0: {sCurrentDuel: 4}}},
	dict(POISON, d=0xBC, e=0x00, wram={wDuelType: b"\x03", wPlayerDuelVariables: b"\x11\x22"}),
	{"d": 0xBC, "e": 0x00, "wram": {wDuelType: b"\x00"}, "sread": {0: {sCurrentDuel: 1}}},
]
# <<< factory SaveDuelDataToDE

# >>> factory LoadSavedDuelDataFromDE
CONTRACT["LoadSavedDuelDataFromDE"] = {"compare": (), "preserve": ()}
sCurrentDuelData = 0xBC04
wPlayerDuelVariables = 0xC200
hWhoseTurn = 0xFF97
CASES["LoadSavedDuelDataFromDE"] = [
	{"d": 0xBC, "e": 0x00, "sram": {0: {sCurrentDuelData: bytes(range(0, 4))}},
	 "read": {wPlayerDuelVariables: 4}},
	dict(POISON, d=0xBC, e=0x00, sram={0: {sCurrentDuelData: bytes([0xAA, 0xBB])}}),
	{"d": 0xBC, "e": 0x00, "sram": {0: {sCurrentDuelData: b"\x00" * 4}},
	 "read": {wPlayerDuelVariables: 4}},
]
# <<< factory LoadSavedDuelDataFromDE

# >>> factory SetBGP7OrSGB2ToCardPalette
CONTRACT["SetBGP7OrSGB2ToCardPalette"] = {"compare": (), "preserve": ()}
CASES["SetBGP7OrSGB2ToCardPalette"] = [
	{"wram": {0xCAB4: bytes([0x00])}},
	{"wram": {0xCAB4: bytes([0x01]), 0xCE23: bytes([0x11, 0x22, 0x33, 0x44])},
	 "read": {0xCAE1: 4}},
	dict(POISON, wram={0xCAB4: bytes([0x02])}),
]
# <<< factory SetBGP7OrSGB2ToCardPalette

# >>> factory JPWriteByteToBGMap0
CONTRACT["JPWriteByteToBGMap0"] = {"compare": (), "preserve": ()}
CASES["JPWriteByteToBGMap0"] = [
	{"a": 0x41, "b": 0, "c": 0, "read": {0x9800: 1}},
	dict(POISON, a=0x50, b=5, c=3, read={0x9800 + 3 * 32 + 5: 1}),
]
# <<< factory JPWriteByteToBGMap0

# >>> factory ZeroObjectPositionsAndToggleOAMCopy
wVBlankOAMCopyToggle = 0xCAC0
CONTRACT["ZeroObjectPositionsAndToggleOAMCopy"] = {"compare": (), "preserve": ()}
CASES["ZeroObjectPositionsAndToggleOAMCopy"] = [
	{"wram": {wVBlankOAMCopyToggle: b"\x00"}},
	dict(POISON, wram={wVBlankOAMCopyToggle: b"\xFF"}),
]
# <<< factory ZeroObjectPositionsAndToggleOAMCopy

# >>> factory LoadPlayerDeck
CONTRACT["LoadPlayerDeck"] = {"compare": (), "preserve": ()}
sCurrentlySelectedDeck_ = 0xB700
sDeck1Cards_ = 0xA218
wPlayerDeck_ = 0xC400
CASES["LoadPlayerDeck"] = [
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes(range(60))}},
     "read": {wPlayerDeck_: 60}},
    dict(POISON, sram={0: {sCurrentlySelectedDeck_: b"\x01", sDeck1Cards_: bytes(range(60)), sDeck1Cards_ + 60: bytes(range(60))}},
         read={wPlayerDeck_: 60}),
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes([0xFF] * 60)}},
     "read": {wPlayerDeck_: 60}},
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x01", sDeck1Cards_: bytes([1] * 60), sDeck1Cards_ + 60: bytes([2] * 60)}},
     "read": {wPlayerDeck_: 60}},
    {"ramg": False, "sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes(range(60))}},
     "read": {wPlayerDeck_: 60}},
]
# <<< factory LoadPlayerDeck

# >>> factory PrintPracticeDuelDrMasonInstructions
CONTRACT["PrintPracticeDuelDrMasonInstructions"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["PrintPracticeDuelDrMasonInstructions"] = [
    {"hl": 0x01DB, "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, hl=0x01DC, keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelDrMasonInstructions

# >>> factory PrintPracticeDuelInstructionsTextBoxLabel
CONTRACT["PrintPracticeDuelInstructionsTextBoxLabel"] = {"compare": (), "preserve": ()}
CASES["PrintPracticeDuelInstructionsTextBoxLabel"] = [
    {"wram": {0xCC06: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    {"wram": {0xCC06: b"\x07"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, wram={0xCC06: b"\x06"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelInstructionsTextBoxLabel

# >>> factory SwitchCardPage
CONTRACT["SwitchCardPage"] = {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["SwitchCardPage"] = [
    {"a": 0},
    dict(POISON, a=0, f=0),
]
# <<< factory SwitchCardPage

# >>> factory CardPageSwitch_00
CONTRACT["CardPageSwitch_00"] = {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_00"] = [
    {},
    dict(POISON, f=0),
]
# <<< factory CardPageSwitch_00

# >>> factory LoadLoaded1CardGfx
CONTRACT["LoadLoaded1CardGfx"] = {"compare": (), "preserve": ()}
CASES["LoadLoaded1CardGfx"] = [
    {"d": 0x88, "e": 0x00, "wram": {0xCC25: b"\xA7\x02"}, "vread": {0: {0x8800: 0x300}}},
    {"d": 0x90, "e": 0x00, "wram": {0xCC25: b"\x00\x18"}, "vread": {0: {0x9000: 0x300}}},
    dict(POISON, d=0x88, e=0x00, wram={0xCC25: b"\xA7\x02"}, vread={0: {0x8800: 0x300}}),
]
# <<< factory LoadLoaded1CardGfx

# >>> factory SetSGB3ToCardPalette
CONTRACT["SetSGB3ToCardPalette"] = {"compare": (), "preserve": ()}
CASES["SetSGB3ToCardPalette"] = [
    {"wram": {0xCE25: b"\x00" * 6, 0xCAE9: b"\xAA" * 6}},
    {"wram": {0xCE25: b"\x01\x02\x03\x04\x05\x06", 0xCAE9: b"\x00" * 6}},
    dict(POISON, wram={0xCE25: b"\xFE\xDC\xBA\x98\x76\x54", 0xCAE9: b"\x11" * 6}),
]
# <<< factory SetSGB3ToCardPalette

# >>> factory LookForCardIDInPlayArea_Bank5
CONTRACT["LookForCardIDInPlayArea_Bank5"] = {"compare": ("a", "f", "b", "d", "e"), "preserve": ("d", "e")}
CASES["LookForCardIDInPlayArea_Bank5"] = [
    {"a": 0, "b": 0, "read": {0xCDD4: 1}},
    {"a": 1, "b": 0, "read": {0xCDD4: 1}},
    {"a": 0x08, "b": 3, "read": {0xCDD4: 1}},
    {"a": 0x20, "b": 5, "read": {0xCDD4: 1}},
    {"a": 0xFF, "b": 0, "read": {0xCDD4: 1}},
    dict(POISON, a=0x08, b=0, read={0xCDD4: 1}),
]
# <<< factory LookForCardIDInPlayArea_Bank5

# >>> factory ClearMemory_Bank5
CONTRACT["ClearMemory_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank5"] = [
    {"a": 0, "hl": 0xC300, "wram": {0xC300: b"\xaa" * 0x101}},
    {"a": 1, "hl": 0xC300, "wram": {0xC300: b"\xaa\xbb"}},
    {"a": 8, "hl": 0xC400, "wram": {0xC400: b"\x55" * 9}},
    dict(POISON, a=4, hl=0xC300, wram={0xC300: b"\xaa" * 5}),
]
# <<< factory ClearMemory_Bank5

# >>> factory CheckCardPageExists
CONTRACT["CheckCardPageExists"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["CheckCardPageExists"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00\x00"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x0F\xF0"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x00\x01"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x80\x00"}},
    dict(POISON, hl=0xC200, wram={0xC200: b"\x12\x34"}),
]
# <<< factory CheckCardPageExists

# >>> factory CardPageSwitch_PokemonEnd
CONTRACT["CardPageSwitch_PokemonEnd"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_PokemonEnd"] = [
    {},
    dict(POISON),
    {"f": 0x80},
]
# <<< factory CardPageSwitch_PokemonEnd

# >>> factory SetCardListInfoBoxText
CONTRACT["SetCardListInfoBoxText"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetCardListInfoBoxText"] = [
    {"hl": 0x0000, "read": {0xCBDA: 2}},
    {"hl": 0x1234, "read": {0xCBDA: 2}},
    dict(POISON, hl=0xBEEF, wram={0xCBDA: b"\x00\x00"}, read={0xCBDA: 2}),
]
# <<< factory SetCardListInfoBoxText

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetLineSeparation
MUTATIONS["SetLineSeparation"] = {
	"source_symbol": "SetLineSeparation",
	"before": "wLineSeparation = a;",
	"after": "wLineSeparation = (uint8_t)(a + 1u);",
	"case_ids": ["SetLineSeparation-0", "SetLineSeparation-1"],
}
# <<< factory-mutation SetLineSeparation
# >>> factory-mutation PlayAreaScreenMenuFunction
MUTATIONS["PlayAreaScreenMenuFunction"] = {
    "source_symbol": "PlayAreaScreenMenuFunction",
    "before": "return 0xA0u;",
    "after": "return 0x80u;",
    "case_ids": ["PlayAreaScreenMenuFunction-0", "PlayAreaScreenMenuFunction-5"],
}
# <<< factory-mutation PlayAreaScreenMenuFunction
# >>> factory-mutation SwitchAttackPage
MUTATIONS["SwitchAttackPage"] = {
	"source_symbol": "SwitchAttackPage",
	"before": "wAttackPageNumber ^ 0x01u",
	"after": "wAttackPageNumber & 0x01u",
	"case_ids": ["SwitchAttackPage-0", "SwitchAttackPage-1"],
}
# <<< factory-mutation SwitchAttackPage
# >>> factory-mutation CopyCGBCardPalette
MUTATIONS["CopyCGBCardPalette"] = {
    "source_symbol": "CopyCGBCardPalette",
    "before": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE)",
    "after": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE) + 1u",
    "case_ids": ["CopyCGBCardPalette-0", "CopyCGBCardPalette-1"],
}
# <<< factory-mutation CopyCGBCardPalette
# >>> factory-mutation CreateCardAttrBlkPacket_DataSet
MUTATIONS["CreateCardAttrBlkPacket_DataSet"] = {
    "source_symbol": "CreateCardAttrBlkPacket_DataSet",
    "before": "gb_write8(hl++, (uint8_t)(d + 7u));",
    "after": "gb_write8(hl++, (uint8_t)(d + 8u));",
    "case_ids": ["CreateCardAttrBlkPacket_DataSet-2"],
}
# <<< factory-mutation CreateCardAttrBlkPacket_DataSet
# >>> factory-mutation SaveDuelDataToDE
MUTATIONS["SaveDuelDataToDE"] = {
	"source_symbol": "SaveDuelDataToDE",
	"before": "gb_write8(base, TRUE);",
	"after": "gb_write8(base, 0u);",
	"case_ids": ["SaveDuelDataToDE-0"],
}
# <<< factory-mutation SaveDuelDataToDE
# >>> factory-mutation LoadSavedDuelDataFromDE
MUTATIONS["LoadSavedDuelDataFromDE"] = {
	"source_symbol": "LoadSavedDuelDataFromDE",
	"before": "de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE);",
	"after": "de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE - 1u);",
	"case_ids": ["LoadSavedDuelDataFromDE-0"],
}
# <<< factory-mutation LoadSavedDuelDataFromDE
# >>> factory-mutation SetBGP7OrSGB2ToCardPalette
MUTATIONS["SetBGP7OrSGB2ToCardPalette"] = {
	"source_symbol": "SetBGP7OrSGB2ToCardPalette",
	"before": "if (console == CONSOLE_SGB) {",
	"after": "if (console != CONSOLE_SGB) {",
	"case_ids": ["SetBGP7OrSGB2ToCardPalette-1"],
}
# <<< factory-mutation SetBGP7OrSGB2ToCardPalette
# >>> factory-mutation JPWriteByteToBGMap0
MUTATIONS["JPWriteByteToBGMap0"] = {
	"source_symbol": "JPWriteByteToBGMap0",
	"before": "WriteByteToBGMap0(a, b, c);",
	"after": "WriteByteToBGMap0(a, c, b);",
	"case_ids": ["JPWriteByteToBGMap0-1"],
}
# <<< factory-mutation JPWriteByteToBGMap0
# >>> factory-mutation ZeroObjectPositionsAndToggleOAMCopy
MUTATIONS["ZeroObjectPositionsAndToggleOAMCopy"] = {
	"source_symbol": "ZeroObjectPositionsAndToggleOAMCopy",
	"before": "wVBlankOAMCopyToggle = TRUE;",
	"after": "wVBlankOAMCopyToggle = 0u;",
	"case_ids": ["ZeroObjectPositionsAndToggleOAMCopy-0", "ZeroObjectPositionsAndToggleOAMCopy-1"],
}
# <<< factory-mutation ZeroObjectPositionsAndToggleOAMCopy
# >>> factory-mutation LoadPlayerDeck
MUTATIONS["LoadPlayerDeck"] = {
    "source_symbol": "LoadPlayerDeck",
    "before": "hl = (uint16_t)(hl + sDeck1Cards_ADDR);",
    "after": "hl = (uint16_t)(hl + sDeck1Cards_ADDR + 1u);",
    "case_ids": ["LoadPlayerDeck-0", "LoadPlayerDeck-2"],
}
# <<< factory-mutation LoadPlayerDeck
# >>> factory-mutation PrintPracticeDuelDrMasonInstructions
MUTATIONS["PrintPracticeDuelDrMasonInstructions"] = {
    "source_symbol": "PrintPracticeDuelDrMasonInstructions",
    "before": "PrintScrollableText_WithTextBoxLabel(hl, DrMasonText)",
    "after": "PrintScrollableText_WithTextBoxLabel(hl, DrMasonText + 1u)",
    "case_ids": ["PrintPracticeDuelDrMasonInstructions-0", "PrintPracticeDuelDrMasonInstructions-1"],
}
# <<< factory-mutation PrintPracticeDuelDrMasonInstructions
# >>> factory-mutation PrintPracticeDuelInstructionsTextBoxLabel
MUTATIONS["PrintPracticeDuelInstructionsTextBoxLabel"] = {
    "source_symbol": "PrintPracticeDuelInstructionsTextBoxLabel",
    "before": "if (a == 7u)",
    "after": "if (a == 8u)",
    "case_ids": ["PrintPracticeDuelInstructionsTextBoxLabel-1"],
}
# <<< factory-mutation PrintPracticeDuelInstructionsTextBoxLabel
# >>> factory-mutation SwitchCardPage
MUTATIONS["SwitchCardPage"] = {
    "source_symbol": "SwitchCardPage",
    "before": "\treturn CardPageSwitch_00();\n}",
    "after": "\treturn (CardPageResult){0u, 0u};\n}",
    "case_ids": ["SwitchCardPage-0", "SwitchCardPage-1"],
}
# <<< factory-mutation SwitchCardPage
# >>> factory-mutation CardPageSwitch_00
MUTATIONS["CardPageSwitch_00"] = {
    "source_symbol": "CardPageSwitch_00",
    "before": "return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C, 1u};",
    "after": "return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C + 1u, 1u};",
    "case_ids": ["CardPageSwitch_00-0", "CardPageSwitch_00-1"],
}
# <<< factory-mutation CardPageSwitch_00
# >>> factory-mutation LoadLoaded1CardGfx
MUTATIONS["LoadLoaded1CardGfx"] = {
    "source_symbol": "LoadLoaded1CardGfx",
    "before": "LoadCardGfx(hl, de, 0x30u, TILE_SIZE);",
    "after": "LoadCardGfx(hl, de, 0x20u, TILE_SIZE);",
    "case_ids": ["LoadLoaded1CardGfx-0", "LoadLoaded1CardGfx-1", "LoadLoaded1CardGfx-2"],
}
# <<< factory-mutation LoadLoaded1CardGfx
# >>> factory-mutation SetSGB3ToCardPalette
MUTATIONS["SetSGB3ToCardPalette"] = {
    "source_symbol": "SetSGB3ToCardPalette",
    "before": "for (uint8_t i = 0; i < SGB3_COPY_LEN; i++)",
    "after": "for (uint8_t i = 0; i < 5u; i++)",
    "case_ids": ["SetSGB3ToCardPalette-0", "SetSGB3ToCardPalette-1", "SetSGB3ToCardPalette-2"],
}
# <<< factory-mutation SetSGB3ToCardPalette
# >>> factory-mutation LookForCardIDInPlayArea_Bank5
MUTATIONS["LookForCardIDInPlayArea_Bank5"] = {
    "source_symbol": "LookForCardIDInPlayArea_Bank5",
    "before": "\twTempCardIDToLook = a;",
    "after": "\twTempCardIDToLook = (uint8_t)(a + 1u);",
    "case_ids": ["LookForCardIDInPlayArea_Bank5-0", "LookForCardIDInPlayArea_Bank5-1", "LookForCardIDInPlayArea_Bank5-2", "LookForCardIDInPlayArea_Bank5-3", "LookForCardIDInPlayArea_Bank5-4", "LookForCardIDInPlayArea_Bank5-5"],
}
# <<< factory-mutation LookForCardIDInPlayArea_Bank5
# >>> factory-mutation ClearMemory_Bank5
MUTATIONS["ClearMemory_Bank5"] = {
    "source_symbol": "ClearMemory_Bank5",
    "before": "uint32_t n = a ? a : 0x100u;",
    "after": "uint32_t n = a ? a : 0x1u;",
    "case_ids": ["ClearMemory_Bank5-0"],
}
# <<< factory-mutation ClearMemory_Bank5
# >>> factory-mutation CheckCardPageExists
MUTATIONS["CheckCardPageExists"] = {
    "source_symbol": "CheckCardPageExists",
    "before": "\ta |= gb_read8(*hl);",
    "after": "\ta &= gb_read8(*hl);",
    "case_ids": ["CheckCardPageExists-2", "CheckCardPageExists-3", "CheckCardPageExists-4"],
}
# <<< factory-mutation CheckCardPageExists
# >>> factory-mutation CardPageSwitch_PokemonEnd
MUTATIONS["CardPageSwitch_PokemonEnd"] = {
    "source_symbol": "CardPageSwitch_PokemonEnd",
    "before": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 1u};",
    "after": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 0u};",
    "case_ids": ["CardPageSwitch_PokemonEnd-0", "CardPageSwitch_PokemonEnd-1", "CardPageSwitch_PokemonEnd-2"],
}
# <<< factory-mutation CardPageSwitch_PokemonEnd
# >>> factory-mutation SetCardListInfoBoxText
MUTATIONS["SetCardListInfoBoxText"] = {
    "source_symbol": "SetCardListInfoBoxText",
    "before": "wCardListInfoBoxText = (uint8_t)hl;",
    "after": "wCardListInfoBoxText = (uint8_t)(hl >> 8);",
    "case_ids": ["SetCardListInfoBoxText-1", "SetCardListInfoBoxText-2"],
}
# <<< factory-mutation SetCardListInfoBoxText
