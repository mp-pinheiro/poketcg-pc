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
