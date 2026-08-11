POISON = {"a": 0xaa, "f": 0xf0, "b": 0xbb, "c": 0xcc, "d": 0xdd, "e": 0xee, "hl": 0x1234}
GFX_WITNESS = bytes((i * 13 + 7) & 0xff for i in range(16))
GFX_BOUNDED_STATE = {
    "wram": {
        0xd4c2: b"\x00\x80", 0xd4c4: b"\x00\xc0", 0xd4c6: b"\x00",
        0xd4c7: b"\x10", 0xd4c8: b"\x01\x00", 0xd4ca: b"\x00",
        0xd4cb: b"\x00", 0xff4f: b"\x00", 0xc002: GFX_WITNESS,
    },
    "vread": {0: {0x8000: 0x10}},
}
GFX_POISON_STATE = {
    **POISON,
    "wram": GFX_BOUNDED_STATE["wram"],
    "vread": GFX_BOUNDED_STATE["vread"],
}
TILEMAP_STATE = {
    "wram": {
        0xd4c4: b"\x00\x98", 0xd4c2: b"\x00\x98",
        0xd12f: b"\x01", 0xd130: b"\x01", 0xd131: b"\x00",
    },
}
TILEMAP_POISON_STATE = {
    **POISON,
    "wram": TILEMAP_STATE["wram"],
}
GFX_BOUNDED_STATE_TILES = {
    **GFX_BOUNDED_STATE,
    "vread": {0: {0x9000: 0x10}},
}
def _max_gfx_case():
    return {
        "b": 0, "c": 0, "oracle": False,
        "why": "zero tile count and zero tile size expand to 65536 bytes, "
               "overwriting the synthesized call frame",
        "wram": {
            0xd4c2: b"\x00\x90", 0xd4c4: b"\x00\xc0", 0xd4c6: b"\x00",
            0xd4c7: b"\x00", 0xd4c8: b"\x00\x00", 0xd4ca: b"\x00",
            0xd4cb: b"\x01", 0xff4f: b"\x01", 0xc002: GFX_WITNESS,
            0xc202: GFX_WITNESS,
        },
        "expect_vram": {
            1: {0x9000: GFX_WITNESS, 0x9200: GFX_WITNESS},
        },
        "expect": {0xff4f: b"\xfe"},
        "expect_regs": {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
    }

NAMES = (
    "LoadTilemap_ToSRAM", "LoadTilemap_ToVRAM", "LoadTilemap",
    "LoadTilemap.InitAndDecompressBGMap", "LoadTilemap.Decompress", "Func_80148",
    "CopyBGDataToVRAMOrSRAM", "SafelyCopyBGMapFromSRAMToVRAM", "ClearSRAMBGMaps",
    "GetMapDataPointer", "LoadGraphicsPointerFromHL", "LoadSpriteGfx",
    "LoadGfxDataFromTempPointerToVRAMBank", "LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2",
    "LoadGfxDataFromTempPointer", "GetTileOffsetPointerAndSwitchVRAM",
    "Func_80238",
    "LoadTilesetGfx.LoadTileGfx", "LoadTilesetGfx.CopyGfxData", "Func_803b9",
    "LoadBGPalette", "LoadPaletteDataFromHL", "LoadOBPalette", "LoadPaletteDataToBuffer",
)

CONTRACT = {
    "LoadTilemap_ToSRAM": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilemap_ToVRAM": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilemap": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilemap.InitAndDecompressBGMap": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilemap.Decompress": {"compare": ("b", "d", "e", "hl"), "preserve": ("hl",)},
    "Func_80148": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CopyBGDataToVRAMOrSRAM": {"compare": ("c", "d", "e", "hl"), "preserve": ("c",)},
    "SafelyCopyBGMapFromSRAMToVRAM": {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "ClearSRAMBGMaps": {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetMapDataPointer": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "Func_80238": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadGraphicsPointerFromHL": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "LoadSpriteGfx": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadGfxDataFromTempPointerToVRAMBank": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadGfxDataFromTempPointer": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetTileOffsetPointerAndSwitchVRAM": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2": {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")},
    "LoadTilesetGfx": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilesetGfx.LoadTileGfx": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadTilesetGfx.CopyGfxData": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "Func_803b9": {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "LoadBGPalette": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadPaletteDataFromHL": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadOBPalette": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadPaletteDataToBuffer": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "LoadTilemap_ToSRAM": [{}, dict(POISON), {"b": 1, "c": 1}],
    "LoadTilemap_ToVRAM": [{}, dict(POISON), {"b": 1, "c": 1}],
    "LoadTilemap": [{}, dict(POISON), {"b": 1, "c": 1}],
    "LoadTilemap.InitAndDecompressBGMap": [dict(TILEMAP_STATE), dict(TILEMAP_POISON_STATE), dict(TILEMAP_STATE)],
    "LoadTilemap.Decompress": [dict(TILEMAP_STATE), dict(TILEMAP_POISON_STATE), {"b": 1, "wram": TILEMAP_STATE["wram"]}],
    "Func_80148": [{}, dict(POISON), {"b": 1}, {"b": 0xff}],
    "CopyBGDataToVRAMOrSRAM": [{}, dict(POISON), {"b": 1}, {"b": 0xff}, {"b": 0, "wram": {0xff80: b"\x20", 0xd4c2: b"\x00\x98"}, "read": {0x9800: 0x100}}],
    "SafelyCopyBGMapFromSRAMToVRAM": [{}, dict(POISON), {"wram": {0xff80: b"\x20"}, "sram": {1: {0xa000: bytes(range(256)) * 8}}, "vread": {0: {0x9800: 0x400}, 1: {0x9800: 0x400}}}],
    "ClearSRAMBGMaps": [{"wram": {0xff81: b"\x01"}, "sram": {1: {0xa000: b"\xaa" * 0x800}}, "sread": {1: {0xa000: 0x800}}}, dict(POISON)],
    "GetMapDataPointer": [{}, dict(POISON), {"a": 0, "hl": 0}, {"a": 0xff, "hl": 4}],
    "LoadGraphicsPointerFromHL": [{}, dict(POISON), {"hl": 0x7fff}, {"hl": 0x8000}],
    "LoadSpriteGfx": [{}, dict(POISON)],
    "LoadGfxDataFromTempPointerToVRAMBank": [
        dict(GFX_BOUNDED_STATE), dict(GFX_POISON_STATE), dict(GFX_BOUNDED_STATE),
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x00\x01"},
         "vread": {0: {0x8000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x01\x00"},
         "vread": {0: {0x8000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x01\x01"},
         "vread": {0: {0x8000: 0x10}}},
        {**_max_gfx_case(), "expect_vram": {1: {0x8000: GFX_WITNESS, 0x8200: GFX_WITNESS}}},
    ],
    "LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2": [
        dict(GFX_BOUNDED_STATE_TILES), dict(GFX_POISON_STATE), dict(GFX_BOUNDED_STATE_TILES),
        {"wram": {**GFX_BOUNDED_STATE_TILES["wram"], 0xd4c8: b"\x00\x01"},
         "vread": {0: {0x9000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE_TILES["wram"], 0xd4c8: b"\x01\x00"},
         "vread": {0: {0x9000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE_TILES["wram"], 0xd4c8: b"\x01\x01"},
         "vread": {0: {0x9000: 0x10}}},
        _max_gfx_case(),
    ],
    "LoadGfxDataFromTempPointer": [
        dict(GFX_BOUNDED_STATE), dict(GFX_POISON_STATE), dict(GFX_BOUNDED_STATE),
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x00\x01"},
         "vread": {0: {0x8000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x01\x00"},
         "vread": {0: {0x8000: 0x10}}},
        {"wram": {**GFX_BOUNDED_STATE["wram"], 0xd4c8: b"\x01\x01"},
         "vread": {0: {0x8000: 0x10}}},
        _max_gfx_case(),
    ],
    "GetTileOffsetPointerAndSwitchVRAM": [{}, dict(POISON), {"wram": {0xd4ca: b"\x00", 0xd4cb: b"\x00"}, "read": {0xd4ca: 1, 0xd4cb: 1}}],
    "GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2": [{}, dict(POISON), {"wram": {0xd4ca: b"\x80", 0xd4cb: b"\x01"}, "read": {0xd4ca: 1, 0xd4cb: 1}}],
    "LoadTilesetGfx": [{}, dict(POISON)],
    "Func_80238": [
        {"vread": {0: {0x8000: 0x10, 0x9000: 0x10}}},
        {**POISON, "vread": {0: {0x8000: 0x10, 0x9000: 0x10}}},
        {"a": 0, "hl": 0, "vread": {0: {0x8000: 0x10, 0x9000: 0x10}}},
        {"a": 0xff, "hl": 0xffff, "vread": {0: {0x8000: 0x10, 0x9000: 0x10}}},
    ],
    "LoadTilesetGfx.LoadTileGfx": [
        {}, dict(POISON),
        {"wram": {0xd4c2: b"\x80\x00", 0xd4ca: b"\x80",
                  0xd4c8: b"\x01\x00", 0xd4c4: b"\x00\x40",
                  0xd4c6: b"\x20"}}
    ],
    "LoadTilesetGfx.CopyGfxData": [
        {
            "oracle": False,
            "why": "zero remaining count expands to the 65536-tile copy and "
                   "overwrites the synthesized call frame",
            "expect": {0xd4c8: b"\x00\x00"},
            "expect_regs": {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
        },
        dict(POISON),
        {
            "b": 0, "c": 0, "oracle": False,
            "why": "zero remaining count expands to the 65536-tile copy and "
                   "overwrites the synthesized call frame",
            "expect": {0xd4c8: b"\x00\x00"},
            "expect_regs": {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
        },
        {"b": 0, "c": 0x80}, {"b": 1, "c": 0}, {"b": 1, "c": 0x80},
        {"b": 0, "c": 0xff},
    ],
    "Func_803b9": [{}, dict(POISON)],
    "LoadBGPalette": [{}, dict(POISON)],
    "LoadPaletteDataFromHL": [{}, dict(POISON), {"b": 0, "c": 0}, {"b": 0, "c": 1}, {"b": 15, "c": 8}, {"b": 16, "c": 1}, {"b": 23, "c": 1}, {"b": 24, "c": 1}, {"b": 0, "c": 9}],
    "LoadOBPalette": [{}, dict(POISON)],
    "LoadPaletteDataToBuffer": [{}, dict(POISON), {"a": 0}, {"a": 0xff}],
}
for _name in (
    "LoadTilemap_ToSRAM", "LoadTilemap_ToVRAM", "LoadTilemap",
    "LoadTilemap.InitAndDecompressBGMap", "LoadTilemap.Decompress",
):
    for _case in CASES[_name]:
        _case.setdefault("wram", {})[0xff80] = b"\x20"
for _name in ("LoadTilesetGfx", "LoadTilesetGfx.LoadTileGfx"):
    for _case in CASES[_name]:
        _case.setdefault("wram", {})[0xff80] = b"\x20"
for _case in CASES["Func_80238"]:
    _case.setdefault("wram", {})[0xff80] = b"\x20"
for _name in (
    "LoadGfxDataFromTempPointerToVRAMBank",
    "LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2",
    "LoadGfxDataFromTempPointer",
):
    for _case in CASES[_name]:
        _case.setdefault("wram", {})[0xff80] = b"\x20"
for _case in CASES["LoadSpriteGfx"]:
    _case.setdefault("wram", {})[0xff80] = b"\x20"
for _name in (
    "LoadBGPalette", "LoadPaletteDataFromHL", "LoadOBPalette",
    "LoadPaletteDataToBuffer",
):
    for _case in CASES[_name]:
        _case.setdefault("wram", {})[0xff80] = b"\x20"

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "LoadBGPalette": {
        "source_symbol": "LoadBGPalette",
        "before": "SetBGP(p[1]);",
        "after": "SetBGP((uint8_t)(p[1] ^ 1u));",
        "case_ids": ["LoadBGPalette-0", "LoadBGPalette-1"],
    },
    "Func_80238": {
        "source_symbol": "Func_80238",
        "before": "\twVRAMTileOffset = 0x80;",
        "after": "\twVRAMTileOffset = 0x00;",
        "case_ids": ["Func_80238-0", "Func_80238-1"],
    },
}
