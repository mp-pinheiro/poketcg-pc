POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOWFramesetSubgroups_ADDR = 0xD31A
wCurOWFrameDataOffset = 0xD320
wCurOWFrameDuration = 0xD321
wNumLoadedFramesetSubgroups = 0xD322

CONTRACT = {
    "ClearNumLoadedFramesetSubgroups": {"compare": (), "preserve": ()},
    "ClearOWFramesetSubgroups": {"compare": (), "preserve": ()},
    "GetOWFramesetSubgroupData": {"compare": (), "preserve": ()},
    "LoadOWFramesetSubgroup": {"compare": ("a",), "preserve": ()},
    "StoreOWFramesetSubgroup": {"compare": (), "preserve": ()},
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
        {"hl": 0xC100, "c": 0, "wram": {0xC100: b"\x00\x00"}},
        {"hl": 0xC100, "c": 1, "wram": {0xC101: b"\x04", 0xC104: b"\x22"}},
        dict(POISON, hl=0xC200, c=2, wram={0xC202: b"\x05", 0xC205: b"\x33",
                                             wCurOWFrameDataOffset: b"\x99", wCurOWFrameDuration: b"\x88"}),
        {"hl": 0xC300, "c": 1, "wram": {0xC301: b"\x04", 0xC304: b"\xFF",
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
}

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
