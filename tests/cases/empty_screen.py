wConsole = 0xCAB4
wTileMapFill = 0xCAB6
wDuelDisplayedScreen = 0xCAC2

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "EmptyScreen": {"compare": (), "preserve": ()},
    "BCCoordToBGMap0Address": {"compare": ("d", "e"), "preserve": ()},
}

CASES = {
    "EmptyScreen": [
        {"wram": {wTileMapFill: b"\x00", wConsole: b"\x00"},
         "read": {0x9800: 0x800, 0xFF82: 1}},
        dict(POISON,
             wram={wTileMapFill: b"\xA5", wConsole: b"\x00",
                   wDuelDisplayedScreen: b"\x7F"},
             read={0x9800: 0x800, 0xFF82: 1}),
        {"wram": {wTileMapFill: b"\x5A", wConsole: b"\x02"},
         "read": {0x9800: 0x800, 0xFF82: 1}},
    ],
    "BCCoordToBGMap0Address": [
        {},
        dict(POISON, b=0x12, c=0x34),
        {"b": 0xFF, "c": 0xFF},
        {"b": 0x01, "c": 0x20},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "BCCoordToBGMap0Address": {
        "source_symbol": "BCCoordToBGMap0Address",
        "before": "uint16_t offset = (uint16_t)((uint16_t)c * TILEMAP_W + b);",
        "after": "uint16_t offset = (uint16_t)((uint16_t)b * TILEMAP_W + c);",
        "case_ids": ["BCCoordToBGMap0Address-1", "BCCoordToBGMap0Address-2", "BCCoordToBGMap0Address-3"],
    },
}
