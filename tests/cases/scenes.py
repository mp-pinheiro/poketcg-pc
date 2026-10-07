"""Oracle-diff cases for poketcg/src/engine/scenes.asm."""
from tests.cases._symbols import sym

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
		 sym("wConsole"): b"\x02",
		 sym("wVBlankOAMCopyToggle"): b"\x7F",
		 sym("wTempBoosterChances"): b"\x55",
		 sym("wWhichBGPalIndex"): b"\x66",
		 sym("wSceneBaseX"): b"\x20",
		 sym("wSceneBaseY"): b"\x30",
		 sym("hSCX"): b"\x04",
		 sym("hSCY"): b"\x08",
	 },
	 "read": {sym("wDeckToBuild"): 0x100}},
	{"wram": {
		 sym("wConsole"): b"\x01",
		 sym("wVBlankOAMCopyToggle"): b"\xFF",
		 sym("wTempBoosterChances"): b"\xA5",
		 sym("wWhichBGPalIndex"): b"\xA6",
		 sym("wSceneBaseX"): b"\x40",
		 sym("wSceneBaseY"): b"\x40",
		 sym("hSCX"): b"\x10",
		 sym("hSCY"): b"\x20",
	 }}
]
# <<< factory SetBoosterLogoOAM

# >>> factory _DrawPortrait
CONTRACT["_DrawPortrait"] = {"compare": (), "preserve": ()}
CASES["_DrawPortrait"] = [
	{"wram": {sym("wCurTilemap"): b"\x62", sym("wd291"): b"\x19", sym("wCurPortrait"): b"\x00"}, "read": {sym("wCurTilemap"): 1, sym("wCurTileset"): 1, sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wd291"): 1, sym("wCurPortrait"): 1}},
	dict(POISON, wram={sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x2A", sym("wCurPortrait"): b"\x02"}, read={sym("wCurTilemap"): 1, sym("wCurTileset"): 1, sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wd291"): 1, sym("wCurPortrait"): 1}),
	{"wram": {sym("wCurTilemap"): b"\x62", sym("wd291"): b"\x19", sym("wCurPortrait"): b"\x29"}, "read": {sym("wCurTilemap"): 1, sym("wCurTileset"): 1, sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wd291"): 1, sym("wCurPortrait"): 1}},
	{"wram": {sym("wCurTilemap"): b"\x62", sym("wd291"): b"\x19", sym("wCurPortrait"): b"\x2A"}, "read": {sym("wCurTilemap"): 1, sym("wCurTileset"): 1, sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wd291"): 1, sym("wCurPortrait"): 1}},
]
# <<< factory _DrawPortrait

# >>> factory LoadScene_LoadSGBPacket
CONTRACT["LoadScene_LoadSGBPacket"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadScene_LoadSGBPacket"] = [
    {"a": 0x11, "f": 0x00, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x2468, "wram": {sym("wConsole"): b"\x00", sym("wSceneSGBPacketPtr"): b"\x00\x00"}, "read": {sym("wConsole"): 1, sym("wSceneSGBPacketPtr"): 2}},
    {"a": 0x66, "f": 0x10, "b": 0x77, "c": 0x88, "d": 0x99, "e": 0xAA, "hl": 0x1357, "wram": {sym("wConsole"): b"\x02", sym("wSceneSGBPacketPtr"): b"\x00\x00"}, "read": {sym("wConsole"): 1}},
    dict(POISON, wram={sym("wConsole"): b"\x01", sym("wSceneSGBPacketPtr"): b"\x00\x00"}, read={sym("wConsole"): 1, sym("wSceneSGBPacketPtr"): 2}),
]
# <<< factory LoadScene_LoadSGBPacket

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = sym("wConsole")
wSceneSGBPacketPtr = sym("wSceneSGBPacketPtr")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wSceneBaseX = sym("wSceneBaseX")
wSceneBaseY = sym("wSceneBaseY")
wSceneSGBPacketPtr = sym("wSceneSGBPacketPtr")
wSceneSGBRoutinePtr = sym("wSceneSGBRoutinePtr")
wConsole = sym("wConsole")
wCurTilemap = sym("wCurTilemap")
wBGP = sym("wBGP")
wd291 = sym("wd291")
wAllSpriteAnimationsDisabled = sym("wAllSpriteAnimationsDisabled")

wCurTilemap = sym("wCurTilemap")
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

# >>> factory LoadBoosterGfx
CONTRACT["LoadBoosterGfx"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["LoadBoosterGfx"] = [
    {"a": 0x00, "b": 0x00, "c": 0x00, "wram": {wCurTilemap: b"\x42"}, "sram": {0: {}}, "instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, a=0x00, b=0x00, c=0x00, wram={wCurTilemap: b"\x3C"}, sram={0: {}}, instruction_budget=4000000, cycle_budget=20000000),
]
# <<< factory LoadBoosterGfx

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
# >>> factory-mutation LoadBoosterGfx
MUTATIONS["LoadBoosterGfx"] = {
    "source_symbol": "LoadBoosterGfx",
    "before": "\twCurTilemap = saved_tilemap;\n\treturn wCurTilemap;",
    "after": "\twCurTilemap = 0u;\n\treturn wCurTilemap;",
    "case_ids": ["LoadBoosterGfx-0", "LoadBoosterGfx-1"],
}
# <<< factory-mutation LoadBoosterGfx
