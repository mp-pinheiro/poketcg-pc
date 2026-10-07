from tests.cases._symbols import sym
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOWFramesetSubgroups_ADDR = sym("wOWFramesetSubgroups")
wCurOWFrameDataOffset = sym("wCurOWFrameDataOffset")
wCurOWFrameDuration = sym("wCurOWFrameDuration")
wNumLoadedFramesetSubgroups = sym("wNumLoadedFramesetSubgroups")


CONTRACT = {
    "ClearNumLoadedFramesetSubgroups": {"compare": (), "preserve": ()},
    "ClearOWFramesetSubgroups": {"compare": (), "preserve": ()},
    "GetOWFramesetSubgroupData": {"compare": (), "preserve": ()},
    "LoadOWFramesetSubgroup": {"compare": ("a",), "preserve": ()},
    "StoreOWFramesetSubgroup": {"compare": (), "preserve": ()},
# >>> factory LoadOWFrameTiles
    "LoadOWFrameTiles": {"compare": (), "preserve": ()},
# <<< factory LoadOWFrameTiles

}

CASES = {
    "ClearNumLoadedFramesetSubgroups": [
        {"wram": {wNumLoadedFramesetSubgroups: b"\xAA"}},
        dict(POISON, wram={wNumLoadedFramesetSubgroups: b"\x7F"}),
    ],
    "ClearOWFramesetSubgroups": [
        {"wram": {wOWFramesetSubgroups_ADDR: b"\x00" * 6}},
        dict(POISON, wram={wOWFramesetSubgroups_ADDR: b"\xAA\xBB\xCC\xDD\xEE\xFF"}),
    ],
    "GetOWFramesetSubgroupData": [
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "c": 0, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x00"}},
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "c": 1, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x12: b"\x04", sym("wDecompressionSecondaryBufferStart") + 0x15: b"\x22"}},
        dict(POISON, hl=sym("wPlayerCardLocations"), c=2, wram={sym("wPlayerCardLocations") + 2: b"\x05", sym("wPlayerCardLocations") + 5: b"\x33",
                                             wCurOWFrameDataOffset: b"\x99", wCurOWFrameDuration: b"\x88"}),
        {"hl": sym("wOpponentCardLocations"), "c": 1, "wram": {sym("wOpponentCardLocations") + 1: b"\x04", sym("wOpponentCardLocations") + 4: b"\xFF",
                                             wCurOWFrameDataOffset: b"\x77", wCurOWFrameDuration: b"\x66"}},
    ],
    "LoadOWFramesetSubgroup": [
        {"c": 0, "wram": {wOWFramesetSubgroups_ADDR: b"\x12\x34"}},
        {"c": 1, "wram": {wOWFramesetSubgroups_ADDR + 2: b"\x56\x78"}},
        dict(POISON, c=2, wram={wOWFramesetSubgroups_ADDR + 4: b"\x9A\xBC"}),
        {"c": 3, "wram": {wOWFramesetSubgroups_ADDR + 6: b"\xDE\xF0"}},
    ],
    "StoreOWFramesetSubgroup": [
        {"c": 0, "wram": {wCurOWFrameDataOffset: b"\x12", wCurOWFrameDuration: b"\x34",
                            wOWFramesetSubgroups_ADDR: b"\x00\x00"}},
        {"c": 1, "wram": {wCurOWFrameDataOffset: b"\x56", wCurOWFrameDuration: b"\x78",
                            wOWFramesetSubgroups_ADDR: b"\x00" * 4}},
        dict(POISON, c=2, wram={wCurOWFrameDataOffset: b"\x9A", wCurOWFrameDuration: b"\xBC",
                                 wOWFramesetSubgroups_ADDR: b"\x00" * 6}),
        {"c": 3, "wram": {wCurOWFrameDataOffset: b"\xDE", wCurOWFrameDuration: b"\xF0",
                            wOWFramesetSubgroups_ADDR: b"\x00" * 8}},
    ],
# >>> factory LoadOWFrameTiles
    "LoadOWFrameTiles": [
        dict(POISON, wram={wCurOWFrameDuration: b"\x02"}),
        dict(POISON, wram={wCurOWFrameDuration: b"\x03"}),
        dict(POISON, wram={wCurOWFrameDuration: b"\x04"}),
        dict(POISON, wram={wCurOWFrameDuration: b"\x05"}),
    ],
# <<< factory LoadOWFrameTiles
}

# >>> factory-cases-statics
wNumLoadedFramesetSubgroups = sym("wNumLoadedFramesetSubgroups")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCurMap = sym("wCurMap")
wConsole = sym("wConsole")
# <<< factory-cases-statics

# >>> factory DoLoadedFramesetSubgroupsFrame
CONTRACT["DoLoadedFramesetSubgroupsFrame"] = {"compare": (), "preserve": ()}
CASES["DoLoadedFramesetSubgroupsFrame"] = [
    {"wram": {wNumLoadedFramesetSubgroups: b"\x00"}},
    {"wram": {wNumLoadedFramesetSubgroups: b"\x01", sym("wOWFramesetSubgroups"): b"\xff" * 6}},
    dict(POISON, wram={wNumLoadedFramesetSubgroups: b"\x02", sym("wOWFramesetSubgroups"): b"\xff" * 6}),
    {"c": 0x7F, "wram": {wNumLoadedFramesetSubgroups: b"\x03", sym("wOWFramesetSubgroups"): b"\xff" * 6}},
]
# <<< factory DoLoadedFramesetSubgroupsFrame

# >>> factory ProcessOWFrameset
CONTRACT["ProcessOWFrameset"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ProcessOWFrameset"] = [
    {"hl": sym("wNameBuffer"), "wram": {sym("wOWFramesetSubgroups"): b"\xFF" * 6, sym("wNameBuffer"): bytes([3, 4, 5, 0xFF, 0xFF, 0xFF])}, "read": {sym("wNumLoadedFramesetSubgroups"): 1}},
    dict(POISON, hl=sym("wNameBuffer"), wram={sym("wOWFramesetSubgroups"): b"\xFF" * 6, sym("wNameBuffer"): bytes([3, 4, 5, 0xFF, 0xFF, 0xFF])}, read={sym("wNumLoadedFramesetSubgroups"): 1}),
]
# <<< factory ProcessOWFrameset

# >>> factory DoMapOWFrame
CONTRACT["DoMapOWFrame"] = {"compare": (), "preserve": ()}
CASES["DoMapOWFrame"] = [
    {"wram": {wCurMap: b"\x02", wConsole: b"\x00", sym("wOWFramesetSubgroups"): b"\xFF" * 6}, "rom_bank": 0x20, "read": {sym("wOWFramesetSubgroups"): 6}},
    dict(POISON, wram={wCurMap: b"\x02", wConsole: b"\x00", sym("wOWFramesetSubgroups"): b"\xFF" * 6}, rom_bank=0x20, read={sym("wOWFramesetSubgroups"): 6}),
]
# <<< factory DoMapOWFrame

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "ClearNumLoadedFramesetSubgroups": {
        "source_symbol": "ClearNumLoadedFramesetSubgroups",
        "before": "wNumLoadedFramesetSubgroups = 0;",
        "after": "wNumLoadedFramesetSubgroups = 1;",
        "case_ids": ["ClearNumLoadedFramesetSubgroups-0", "ClearNumLoadedFramesetSubgroups-1"],
    },
    "ClearOWFramesetSubgroups": {
        "source_symbol": "ClearOWFramesetSubgroups",
        "before": "gb_write8((uint16_t)(wOWFramesetSubgroups_ADDR + i), 0xff);",
        "after": "gb_write8((uint16_t)(wOWFramesetSubgroups_ADDR + i), 0x00);",
        "case_ids": ["ClearOWFramesetSubgroups-0", "ClearOWFramesetSubgroups-1"],
    },
    "GetOWFramesetSubgroupData": {
        "source_symbol": "GetOWFramesetSubgroupData",
        "before": "if (frame != 0xff) {",
        "after": "if (frame == 0xff) {",
        "case_ids": ["GetOWFramesetSubgroupData-2"],
    },
    "LoadOWFramesetSubgroup": {
        "source_symbol": "LoadOWFramesetSubgroup",
        "before": "wCurOWFrameDataOffset = gb_read8(address);",
        "after": "wCurOWFrameDataOffset = gb_read8((uint16_t)(address + 1u));",
        "case_ids": ["LoadOWFramesetSubgroup-1", "LoadOWFramesetSubgroup-2", "LoadOWFramesetSubgroup-3"],
    },
    "StoreOWFramesetSubgroup": {
        "source_symbol": "StoreOWFramesetSubgroup",
        "before": "gb_write8(address, wCurOWFrameDataOffset);",
        "after": "gb_write8(address, wCurOWFrameDuration);",
        "case_ids": ["StoreOWFramesetSubgroup-1", "StoreOWFramesetSubgroup-2", "StoreOWFramesetSubgroup-3"],
    },
}
# >>> factory-mutation LoadOWFrameTiles
MUTATIONS["LoadOWFrameTiles"] = {
    "source_symbol": "LoadOWFrameTiles",
    "before": "wCurOWFrameDuration = (uint8_t)(duration - 1u);",
    "after": "wCurOWFrameDuration = (uint8_t)(duration - 2u);",
    "case_ids": ["LoadOWFrameTiles-0", "LoadOWFrameTiles-1", "LoadOWFrameTiles-2", "LoadOWFrameTiles-3"],
}
# <<< factory-mutation LoadOWFrameTiles
# >>> factory-mutation DoLoadedFramesetSubgroupsFrame
MUTATIONS["DoLoadedFramesetSubgroupsFrame"] = {
    "source_symbol": "DoLoadedFramesetSubgroupsFrame",
    "before": "if (LoadOWFramesetSubgroup(c) != 0xffu) {",
    "after": "if (LoadOWFramesetSubgroup(c) == 0xffu) {",
    "case_ids": ["DoLoadedFramesetSubgroupsFrame-1", "DoLoadedFramesetSubgroupsFrame-2", "DoLoadedFramesetSubgroupsFrame-3"],
}
# <<< factory-mutation DoLoadedFramesetSubgroupsFrame
# >>> factory-mutation ProcessOWFrameset
MUTATIONS["ProcessOWFrameset"] = {"source_symbol": "ProcessOWFrameset", "before": "\t\tif (gb_read8(wCurOWFrameDataOffset_ADDR) == 0xFFu) {", "after": "\t\tif (gb_read8(wCurOWFrameDataOffset_ADDR) == 0xFEu) {", "case_ids": ["ProcessOWFrameset-0", "ProcessOWFrameset-1"]}
# <<< factory-mutation ProcessOWFrameset
# >>> factory-mutation DoMapOWFrame
MUTATIONS["DoMapOWFrame"] = {
    "source_symbol": "DoMapOWFrame",
    "before": "\tuint8_t c = (uint8_t)(map * 4u);",
    "after": "\tuint8_t c = (uint8_t)(map * 4u + 1u);",
    "case_ids": ["DoMapOWFrame-0", "DoMapOWFrame-1"],
}
# <<< factory-mutation DoMapOWFrame
