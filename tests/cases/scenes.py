"""Oracle-diff cases for poketcg/src/engine/scenes.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetBoosterLogoOAM
CONTRACT["SetBoosterLogoOAM"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetBoosterLogoOAM"] = [
	{},
	{"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
	 "hl": 0x1234,
	 "wram": {
		 0xCAB4: b"\x02",
		 0xCAC0: b"\x7F",
		 0xD4CA: b"\x55",
		 0xD4CB: b"\x66",
		 0xD61C: b"\x20",
		 0xD61D: b"\x30",
		 0xFF92: b"\x04",
		 0xFF93: b"\x08",
	 },
	 "read": {0xC000: 0x100}},
	{"wram": {
		 0xCAB4: b"\x01",
		 0xCAC0: b"\xFF",
		 0xD4CA: b"\xA5",
		 0xD4CB: b"\xA6",
		 0xD61C: b"\x40",
		 0xD61D: b"\x40",
		 0xFF92: b"\x10",
		 0xFF93: b"\x20",
	 }}
]
# <<< factory SetBoosterLogoOAM

# >>> factory _DrawPortrait
CONTRACT["_DrawPortrait"] = {"compare": (), "preserve": ()}
CASES["_DrawPortrait"] = [
	{"wram": {0xD131: b"\x62", 0xD291: b"\x19", 0xD61E: b"\x00"}, "read": {0xD131: 1, 0xD239: 1, 0xD4CA: 1, 0xD4CB: 1, 0xD291: 1, 0xD61E: 1}},
	dict(POISON, wram={0xD131: b"\x00", 0xD291: b"\x2A", 0xD61E: b"\x02"}, read={0xD131: 1, 0xD239: 1, 0xD4CA: 1, 0xD4CB: 1, 0xD291: 1, 0xD61E: 1}),
]
# <<< factory _DrawPortrait

# >>> factory LoadScene_LoadSGBPacket
CONTRACT["LoadScene_LoadSGBPacket"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadScene_LoadSGBPacket"] = [
    {"a": 0x11, "f": 0x00, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x2468, "wram": {0xCAB4: b"\x00", 0xD620: b"\x00\x00"}, "read": {0xCAB4: 1, 0xD620: 2}},
    {"a": 0x66, "f": 0x10, "b": 0x77, "c": 0x88, "d": 0x99, "e": 0xAA, "hl": 0x1357, "wram": {0xCAB4: b"\x02", 0xD620: b"\x00\x00"}, "read": {0xCAB4: 1}},
    dict(POISON, wram={0xCAB4: b"\x01", 0xD620: b"\x00\x00"}, read={0xCAB4: 1, 0xD620: 2}),
]
# <<< factory LoadScene_LoadSGBPacket

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
wSceneSGBPacketPtr = 0xD620

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wSceneBaseX = 0xD61C
wSceneBaseY = 0xD61D
wSceneSGBPacketPtr = 0xD620
wSceneSGBRoutinePtr = 0xD622
wConsole = 0xCAB4
wCurTilemap = 0xD131
wCurTileset = 0xD239
wBGP = 0xCABC
wWhichBGPalIndex = 0xD4CB
wd291 = 0xD291
wVRAMTileOffset = 0xD4CA
wWhichVRAMBank = 0xD4CB
wAllSpriteAnimationsDisabled = 0xD5D7
# <<< factory-cases-statics

# >>> factory LoadScene_LoadCompressedSGBPacket
CONTRACT["LoadScene_LoadCompressedSGBPacket"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadScene_LoadCompressedSGBPacket"] = [
    {"a": 0x11, "f": 0x00, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x2468,
     "wram": {wConsole: b"\x00", wSceneSGBPacketPtr: b"\x00\x00"}, "read": {wConsole: 1},
     "expect_regs": {"a": 0x00, "f": 0x70}},
    {"a": 0x66, "f": 0x10, "b": 0x77, "c": 0x88, "d": 0x99, "e": 0xAA, "hl": 0x1357,
     "wram": {wConsole: b"\x01", wSceneSGBPacketPtr: b"\x00\x00"}, "read": {wConsole: 1, wSceneSGBPacketPtr: 2},
     "expect_regs": {"a": 0x00, "f": 0x80}},
    dict(POISON, wram={wConsole: b"\x00", wSceneSGBPacketPtr: b"\x00\x00"}, read={wConsole: 1},
         expect_regs={"a": 0x00, "f": 0x70}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory LoadScene_LoadCompressedSGBPacket

# >>> factory LoadScene_SetCardPopAttrBlk
CONTRACT["LoadScene_SetCardPopAttrBlk"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadScene_SetCardPopAttrBlk"] = [
    {"expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, expect_regs={"a": 0x00, "f": 0x80, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory LoadScene_SetCardPopAttrBlk

# >>> factory LoadScene_SetGameBoyPrinterAttrBlk
CONTRACT["LoadScene_SetGameBoyPrinterAttrBlk"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadScene_SetGameBoyPrinterAttrBlk"] = [
    {"wram": {}, "sram": {0: {}}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={}, sram={0: {}}, expect_regs={"a": 0x00, "f": 0x80, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory LoadScene_SetGameBoyPrinterAttrBlk

# >>> factory _LoadScene
CONTRACT["_LoadScene"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["_LoadScene"] = [
    {"a": 0x00, "b": 0x00, "c": 0x00, "wram": {wConsole: b"\x00", wAllSpriteAnimationsDisabled: b"\x00", wCurTilemap: b"\x00", wd291: b"\x00"}, "sram": {0: {}},
     "read": {wSceneBaseX: 1, wSceneBaseY: 1, wSceneSGBPacketPtr: 2, wSceneSGBRoutinePtr: 2, wBGP: 1, wd291: 1, wCurTilemap: 1},
     "instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, a=0x00, b=0x00, c=0x00, wram={wConsole: b"\x00", wAllSpriteAnimationsDisabled: b"\x00", wCurTilemap: b"\x77", wd291: b"\x22"}, sram={0: {}},
         read={wSceneBaseX: 1, wSceneBaseY: 1, wSceneSGBPacketPtr: 2, wSceneSGBRoutinePtr: 2, wBGP: 1, wd291: 1, wCurTilemap: 1},
         instruction_budget=4000000, cycle_budget=20000000),
    {"a": 0x13, "b": 0x02, "c": 0x03, "wram": {wConsole: b"\x02", wAllSpriteAnimationsDisabled: b"\x00", wCurTilemap: b"\x00", wd291: b"\x00"}, "sram": {0: {}},
     "read": {wSceneBaseX: 1, wSceneBaseY: 1, wSceneSGBPacketPtr: 2, wSceneSGBRoutinePtr: 2, wBGP: 1, wd291: 1, wCurTilemap: 1},
     "instruction_budget": 4000000, "cycle_budget": 20000000},
]
# <<< factory _LoadScene

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetBoosterLogoOAM
MUTATIONS["SetBoosterLogoOAM"] = {"source_symbol": "SetBoosterLogoOAM", "before": "wWhichVRAMBank = 0u;", "after": "wWhichVRAMBank = 1u;", "case_ids": ["SetBoosterLogoOAM-1", "SetBoosterLogoOAM-2"]}
# <<< factory-mutation SetBoosterLogoOAM
# >>> factory-mutation _DrawPortrait
MUTATIONS["_DrawPortrait"] = {"source_symbol": "_DrawPortrait", "before": "wCurTileset = tileset;", "after": "wCurTileset = (uint8_t)(tileset + 1u);", "case_ids": ["_DrawPortrait-0", "_DrawPortrait-1"]}
# <<< factory-mutation _DrawPortrait
# >>> factory-mutation LoadScene_LoadSGBPacket
MUTATIONS["LoadScene_LoadSGBPacket"] = {"source_symbol": "LoadScene_LoadSGBPacket", "before": "\tif (console != CONSOLE_SGB)", "after": "\tif (console == CONSOLE_SGB)", "case_ids": ["LoadScene_LoadSGBPacket-0", "LoadScene_LoadSGBPacket-1", "LoadScene_LoadSGBPacket-2"]}
# <<< factory-mutation LoadScene_LoadSGBPacket
# >>> factory-mutation LoadScene_LoadCompressedSGBPacket
MUTATIONS["LoadScene_LoadCompressedSGBPacket"] = {
    "source_symbol": "LoadScene_LoadCompressedSGBPacket",
    "before": "\tif (console != CONSOLE_SGB)\n\t\treturn (LoadScene_LoadCompressedSGBPacketResult){console, cmp_f, b, c, d, e, hl};",
    "after": "\tif (console == CONSOLE_SGB)\n\t\treturn (LoadScene_LoadCompressedSGBPacketResult){console, cmp_f, b, c, d, e, hl};",
    "case_ids": ["LoadScene_LoadCompressedSGBPacket-0", "LoadScene_LoadCompressedSGBPacket-1"],
}
# <<< factory-mutation LoadScene_LoadCompressedSGBPacket
# >>> factory-mutation LoadScene_SetCardPopAttrBlk
MUTATIONS["LoadScene_SetCardPopAttrBlk"] = {"source_symbol": "LoadScene_SetCardPopAttrBlk", "before": "\treturn (LoadScene_SetCardPopAttrBlkResult){result.a, result.f, b, c, d, e, hl};", "after": "\treturn (LoadScene_SetCardPopAttrBlkResult){1u, result.f, b, c, d, e, hl};", "case_ids": ["LoadScene_SetCardPopAttrBlk-0", "LoadScene_SetCardPopAttrBlk-1"]}
# <<< factory-mutation LoadScene_SetCardPopAttrBlk
# >>> factory-mutation LoadScene_SetGameBoyPrinterAttrBlk
MUTATIONS["LoadScene_SetGameBoyPrinterAttrBlk"] = {
    "source_symbol": "LoadScene_SetGameBoyPrinterAttrBlk",
    "before": "\tuint8_t result_f = result.f;",
    "after": "\tuint8_t result_f = 0u;",
    "case_ids": ["LoadScene_SetGameBoyPrinterAttrBlk-0", "LoadScene_SetGameBoyPrinterAttrBlk-1"],
}
# <<< factory-mutation LoadScene_SetGameBoyPrinterAttrBlk
# >>> factory-mutation _LoadScene
MUTATIONS["_LoadScene"] = {
    "source_symbol": "_LoadScene",
    "before": "\tgb_write8(wCurTilemap_ADDR, saved_tilemap);",
    "after": "\tgb_write8(wCurTilemap_ADDR, tilemap);",
    "case_ids": ["_LoadScene-0", "_LoadScene-1"],
}
# <<< factory-mutation _LoadScene
