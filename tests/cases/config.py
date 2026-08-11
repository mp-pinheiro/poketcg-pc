POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DrawConfigMenuCursor": {"compare": (), "preserve": ()},
}

CASES = {
    "DrawConfigMenuCursor": [
        {"a": 0, "c": 0, "wram": {
            0xD118: b"\x00", 0xD119: b"\x00", 0xD1AC: b"\x03\x04"},
         "vread": {0: {0x9883: 1}, 1: {0x9883: 1}}},
        dict(POISON, a=0xAA, c=1, wram={
            0xD119: b"\x00", 0xD11A: b"\x00", 0xD1AD: b"\x07\x06"},
             vread={0: {0x98C7: 1}, 1: {0x98C7: 1}}),
        {"a": 0xFF, "c": 2, "wram": {
            0xD11A: b"\x00", 0xD11B: b"\x00", 0xD1AE: b"\x0F\x0B"},
         "vread": {0: {0x98EF: 1}, 1: {0x98EF: 1}}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawConfigMenuCursor": {
        "source_symbol": "DrawConfigMenuCursor",
        "before": "lookup << 1",
        "after": "lookup",
        "case_ids": ["DrawConfigMenuCursor-0", "DrawConfigMenuCursor-1",
                      "DrawConfigMenuCursor-2"],
    },
}
