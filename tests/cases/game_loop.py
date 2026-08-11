POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

WCONSOLE = 0xCAB4
WTILE_MAP_FILL = 0xCAB6
WLCDC = 0xCABB
WBGP = 0xCABC
WOBP0 = 0xCABD
WOBP1 = 0xCABE
WFLUSH_PALETTE_FLAGS = 0xCABF

READ = {
    WTILE_MAP_FILL: 1,
    WLCDC: 1,
    WBGP: 1,
    0xCAB7: 1,
    0xFFFF: 1,
    WOBP0: 1,
    WOBP1: 1,
    WFLUSH_PALETTE_FLAGS: 1,
    0xCD04: 1,
    0xFF40: 1,
    0xFF47: 1,
    0xFF48: 1,
    0xFF49: 1,
    0xFFA8: 1,
    0xFFA9: 1,
    0xFFB0: 1,
    0xC600: 0x100,
}

CONTRACT = {
    "SetupResetBackUpRamScreen": {"compare": (), "preserve": ()},
}

CASES = {
    "SetupResetBackUpRamScreen": [
        {"wram": {WCONSOLE: b"\x00", WTILE_MAP_FILL: b"\x00",
                  WLCDC: b"\x00", WBGP: b"\x00", WOBP0: b"\x00",
                  WOBP1: b"\x00", WFLUSH_PALETTE_FLAGS: b"\x00",
                  0xFF47: b"\xFC", 0xFF48: b"\xFF", 0xFF49: b"\xFF"},
         "read": READ, "vread": {0: {0x9000: 896}}},
        dict(POISON,
             wram={WCONSOLE: b"\x00", WTILE_MAP_FILL: b"\xA5",
                   WLCDC: b"\x80", WBGP: b"\x11", WOBP0: b"\x22",
                   WOBP1: b"\x33", WFLUSH_PALETTE_FLAGS: b"\x44",
                   0xFF47: b"\xFC", 0xFF48: b"\xFF", 0xFF49: b"\xFF"},
             read=READ, vread={0: {0x9000: 896}}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SetupResetBackUpRamScreen": {
        "source_symbol": "SetupResetBackUpRamScreen",
        "before": "wTileMapFill = 0;",
        "after": "wTileMapFill = 0xFF;",
        "case_ids": ["SetupResetBackUpRamScreen-0", "SetupResetBackUpRamScreen-1"],
    },
}
