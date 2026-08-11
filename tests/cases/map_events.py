"""Oracle-diff cases for engine/overworld/map_events.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOWMapEvents = 0xD323
GUARD_LOW = wOWMapEvents - 1
GUARD_HIGH = wOWMapEvents + 11

CONTRACT = {
    "ClearOWMapEvents": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "ClearOWMapEvents": [
        # All-zero registers; clear all eleven event bytes.
        {"wram": {wOWMapEvents: b"\xff" * 11},
         "read": {wOWMapEvents: 11}},
        # The routine consumes no input registers and preserves the saved pairs.
        dict(POISON,
             wram={wOWMapEvents: b"\xaa\xbb\xcc\xdd\xee\xff\x11\x22\x33\x44\x55"},
             read={wOWMapEvents: 11}),
        # Guard bytes prove the target is exactly NUM_MAP_EVENTS bytes wide.
        {"wram": {GUARD_LOW: b"\x11", wOWMapEvents: b"\x99" * 11,
                   GUARD_HIGH: b"\x22"},
         "read": {GUARD_LOW: 13}},
        # A second seeded state exercises clearing already-zero and nonzero values.
        {"wram": {wOWMapEvents: b"\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00"},
         "read": {wOWMapEvents: 11}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "ClearOWMapEvents": {
        "source_symbol": "ClearOWMapEvents",
        "before": "for (uint8_t i = 0; i < NUM_MAP_EVENTS; i++)",
        "after": "for (uint8_t i = 0; i < NUM_MAP_EVENTS - 1u; i++)",
        "case_ids": ["ClearOWMapEvents-0", "ClearOWMapEvents-1", "ClearOWMapEvents-2", "ClearOWMapEvents-3"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
