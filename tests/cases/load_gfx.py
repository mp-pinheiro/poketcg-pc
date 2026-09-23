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
        {"vread": {0: {0x8000: 0x10, 0x9000: 0x10}}, "read": {0xD4CA: 1}},
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
    # a=1 has a zero DMG-BGP flag byte, so the CGB count sits one byte earlier
    # than for a=0. Reading wBackgroundPalettesCGB is what makes the
    # conditional pointer advance observable at all; the register-only
    # contract above cannot see it.
    "LoadBGPalette": [
        {"read": {0xFF47: 1}},
        {"a": 1, "read": {0xCAF0: 64}},
        {"a": 0, "read": {0xCAF0: 64}},
        dict(POISON, a=1, read={0xCAF0: 64}),
    ],
    "LoadPaletteDataFromHL": [{}, dict(POISON), {"b": 0, "c": 0}, {"b": 0, "c": 1}, {"b": 15, "c": 8}, {"b": 16, "c": 1}, {"b": 23, "c": 1}, {"b": 24, "c": 1}, {"b": 0, "c": 9}],
    # a=0x00 (PALETTE_DEFAULT_CGB): DMG count=1, wWhichOBP!=1, CGB size=8 (the
    # boundary c=8 case) -- this is the exact ordinal-199 signature (b=8,
    # c=8): LoadPaletteDataFromHL's source hl was the size byte's own
    # address instead of one past it, so wObjectPalettesCGB[0] came back
    # holding the size byte's value.
    "LoadOBPalette": [
        {"read": {0xCB30: 64}},
        dict(POISON),
        # a=0x75 (PALETTE_BOOSTER_OAM): DMG count=0 (skips both OBP0/OBP1),
        # CGB size=1 (smallest nonzero loop count).
        {"a": 0x75, "read": {0xCB30: 64}},
        # a=0x00 with wWhichOBP==1: DMG count=1, jumps straight to .obp1.
        {"a": 0x00, "wram": {0xd4ca: b"\x01"}, "read": {0xCB30: 64}},
        # a=0x6c (PALETTE_DEFAULT_DMG): DMG count=1, CGB size=0 -> .done,
        # LoadPaletteDataFromHL is never called.
        {"a": 0x6c, "read": {0xCB30: 64}},
        # a=0x72 (PALETTE_GB_LINK_OAM): DMG count=2, wWhichOBP!=1 -- both
        # OBP0 and OBP1 consumed, no extra hl skip before the size byte.
        {"a": 0x72, "read": {0xCB30: 64}},
        # Same blob with wWhichOBP==1: count=2 but only one DMG byte is
        # consumed, so the "if (count) p++" skip must still land on the
        # real size byte.
        {"a": 0x72, "wram": {0xd4ca: b"\x01"}, "read": {0xCB30: 64}},
    ],
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
for _rec in SCHEMA2_CASES["Func_803b9"]:
    _rec.setdefault("bus", {}).update({0xD239: 1, 0xD4C4: 1, 0xD4C6: 1})
for _rec in SCHEMA2_CASES["GetTileOffsetPointerAndSwitchVRAM"]:
    _rec.setdefault("bus", {}).update({0xD4C2: 2})
for _rec in SCHEMA2_CASES["LoadPaletteDataToBuffer"]:
    _rec.setdefault("bus", {}).update({0xD4C4: 1, 0xD4C6: 1})
for _rec in SCHEMA2_CASES["LoadTilemap"]:
    _rec.setdefault("bus", {}).update({0xD12F: 1, 0xD130: 1, 0xD239: 1, 0xD23A: 1, 0xD23C: 1, 0xD23D: 1, 0xD4C2: 2})
for _rec in SCHEMA2_CASES["LoadTilemap.InitAndDecompressBGMap"]:
    _rec.setdefault("bus", {}).update({0xD28E: 1})
for _rec in SCHEMA2_CASES["LoadTilemap_ToSRAM"]:
    _rec.setdefault("bus", {}).update({0xD12F: 1, 0xD130: 1, 0xD23A: 1, 0xD23C: 1, 0xD23D: 1, 0xD292: 1, 0xD4C2: 2})
for _rec in SCHEMA2_CASES["LoadTilemap_ToVRAM"]:
    _rec.setdefault("bus", {}).update({0xD12F: 1, 0xD130: 1, 0xD23A: 1, 0xD23C: 1, 0xD23D: 1, 0xD292: 1, 0xD4C2: 2})
for _rec in SCHEMA2_CASES["LoadTilesetGfx"]:
    _rec.setdefault("bus", {}).update({0xD4C4: 2, 0xD4C6: 1, 0xD4C8: 2})
for _rec in SCHEMA2_CASES["LoadTilesetGfx.CopyGfxData"]:
    _rec.setdefault("bus", {}).update({0xD4C4: 2, 0xD4C8: 2, 0xD4CA: 1, 0xD4CB: 1})
MUTATIONS["ClearSRAMBGMaps"] = {
    "source_symbol": "ClearSRAMBGMaps",
    "before": "\tFillMemoryWithA(0xa000u, 0x0800u, 0);",
    "after": "\tFillMemoryWithA(0x9FFFu, 0x0800u, 0);",
    "case_ids": ["ClearSRAMBGMaps-0"],
}
MUTATIONS["CopyBGDataToVRAMOrSRAM"] = {
    "source_symbol": "CopyBGDataToVRAMOrSRAM",
    "before": "\t\tSafeCopyDataHLtoDE(hl, de, b);",
    "after": "\t\t;",
    "case_ids": ["CopyBGDataToVRAMOrSRAM-0"],
}
MUTATIONS["GetMapDataPointer"] = {
    "source_symbol": "GetMapDataPointer",
    "before": "\tuint16_t offset = (uint16_t)a * 4u;",
    "after": "\tuint16_t offset = (uint16_t)a * 5u;",
    "case_ids": ["GetMapDataPointer-1"],
}
MUTATIONS["GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2"] = {
    "source_symbol": "GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2",
    "before": "\tuint8_t saved = wVRAMTileOffset;",
    "after": "\tuint8_t saved = (wVRAMTileOffset) ^ 1u;",
    "case_ids": ["GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2-2"],
}
MUTATIONS["Func_803b9"] = {
    "source_symbol": "Func_803b9",
    "before": "void Func_803b9(void)\n{\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x20u);",
    "after": "void Func_803b9(void)\n{\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x21u);",
    "case_ids": ["Func_803b9-0"],
}
MUTATIONS["GetTileOffsetPointerAndSwitchVRAM"] = {
    "source_symbol": "GetTileOffsetPointerAndSwitchVRAM",
    "before": "\tput16(wVRAMPointer_ADDR, (uint16_t)(0x8000u + ((uint16_t)offset << 4)));",
    "after": "\tput16(wVRAMPointer_ADDR, (uint16_t)(0x7FFFu + ((uint16_t)offset << 4)));",
    "case_ids": ["GetTileOffsetPointerAndSwitchVRAM-0"],
}
MUTATIONS["LoadGfxDataFromTempPointer"] = {
    "source_symbol": "LoadGfxDataFromTempPointer",
    "before": "    uint16_t src = (uint16_t)(state16(wTempPointer_ADDR) + 2u);",
    "after": "    uint16_t src = (uint16_t)(state16(wTempPointer_ADDR) + 3u);",
    "case_ids": ["LoadGfxDataFromTempPointer-0"],
}
MUTATIONS["LoadGraphicsPointerFromHL"] = {
    "source_symbol": "LoadGraphicsPointerFromHL",
    "before": "\tgb_write8(wTempPointer_ADDR + 1u, gb_read8(p++));",
    "after": "\t;",
    "case_ids": ["LoadGraphicsPointerFromHL-0"],
}
MUTATIONS["LoadOBPalette"] = {
    "source_symbol": "LoadOBPalette",
    "before": "\t\t\t\t(uint16_t)(p - wLoadedPalData_PTR + wLoadedPalData_ADDR + 1u),",
    "after": "\t\t\t\t(uint16_t)(p - wLoadedPalData_PTR - wLoadedPalData_ADDR + 1u),",
    "case_ids": ["LoadOBPalette-0"],
}
MUTATIONS["LoadSpriteGfx"] = {
    "source_symbol": "LoadSpriteGfx",
    "before": "\treturn total;",
    "after": "\treturn 1u + total;",
    "case_ids": ["LoadSpriteGfx-0"],
}
MUTATIONS["LoadTilemap.Decompress"] = {
    "source_symbol": "LoadTilemap.Decompress",
    "before": "\t\tif ((uint8_t)(row + 1u) == rows)",
    "after": "\t\tif ((uint8_t)(row + 1u) != rows)",
    "case_ids": ["LoadTilemap.Decompress-0"],
}
MUTATIONS["LoadTilesetGfx.LoadTileGfx"] = {
    "source_symbol": "LoadTilesetGfx.LoadTileGfx",
    "before": "\tif (wConsole != 2u)",
    "after": "\tif (wConsole == 2u)",
    "case_ids": ["LoadTilesetGfx.LoadTileGfx-2"],
}
MUTATIONS["SafelyCopyBGMapFromSRAMToVRAM"] = {
    "source_symbol": "SafelyCopyBGMapFromSRAMToVRAM",
    "before": "\t\tuint16_t src = (uint16_t)(0xa000u + row * 32u);",
    "after": "\t\tuint16_t src = (uint16_t)(0x9FFFu + row * 32u);",
    "case_ids": ["SafelyCopyBGMapFromSRAMToVRAM-2"],
}
MUTATIONS["LoadGfxDataFromTempPointerToVRAMBank"] = {
    "source_symbol": "LoadGfxDataFromTempPointerToVRAMBank",
    "before": "\tGetTileOffsetPointerAndSwitchVRAM();\n\tLoadGfxDataFromTempPointer();",
    "after": "\tGetTileOffsetPointerAndSwitchVRAM();\n\t;",
    "case_ids": ["LoadGfxDataFromTempPointerToVRAMBank-0"],
}
MUTATIONS["LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2"] = {
    "source_symbol": "LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2",
    "before": "{\n\tGetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2();",
    "after": "{\n\t;",
    "case_ids": ["LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2-0"],
}
MUTATIONS["LoadPaletteDataToBuffer"] = {
    "source_symbol": "LoadPaletteDataToBuffer",
    "before": "\t      + (uint16_t)((size & 0xf0u) >> 1)",
    "after": "\t      - (uint16_t)((size & 0xf0u) >> 1)",
    "case_ids": ["LoadPaletteDataToBuffer-0"],
}
MUTATIONS["LoadTilemap"] = {
    "source_symbol": "LoadTilemap",
    "before": "\twBGMapCGBMode = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 4u));",
    "after": "\twBGMapCGBMode = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 5u));",
    "case_ids": ["LoadTilemap-0"],
}
MUTATIONS["LoadTilemap.InitAndDecompressBGMap"] = {
    "source_symbol": "LoadTilemap.InitAndDecompressBGMap",
    "before": "\t\tLoadTilemap_Decompress(&de);",
    "after": "\t\t;",
    "case_ids": ["LoadTilemap.InitAndDecompressBGMap-0"],
}
MUTATIONS["LoadTilemap_ToSRAM"] = {
    "source_symbol": "LoadTilemap_ToSRAM",
    "before": "\twWriteBGMapToSRAM = 1;\n\tLoadTilemap(b, c);",
    "after": "\twWriteBGMapToSRAM = 1;\n\tLoadTilemap((uint8_t)(b ^ 1u), c);",
    "case_ids": ["LoadTilemap_ToSRAM-0"],
}
MUTATIONS["LoadTilemap_ToVRAM"] = {
    "source_symbol": "LoadTilemap_ToVRAM",
    "before": "\twWriteBGMapToSRAM = 0;\n\tLoadTilemap(b, c);",
    "after": "\twWriteBGMapToSRAM = 0;\n\tLoadTilemap((uint8_t)(b ^ 1u), c);",
    "case_ids": ["LoadTilemap_ToVRAM-0"],
}
MUTATIONS["LoadTilesetGfx"] = {
    "source_symbol": "LoadTilesetGfx",
    "before": "{\n\tuint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;\n\tLoadGraphicsPointerFromHL(&hl);",
    "after": "{\n\tuint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;\n\t;",
    "case_ids": ["LoadTilesetGfx-0"],
}
