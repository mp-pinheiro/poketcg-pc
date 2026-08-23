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

# >>> factory-cases-statics
wBGMapBank = 0xD23D
wBGMapHeight = 0xD130
wBGMapPermissionDataPtr = 0xD23A
wBGMapWidth = 0xD12F
wConsole = 0xCAB4
wCurTilemap = 0xD131
wOWMapEvents = 0xD323
wPermissionMap = 0xD133
# <<< factory-cases-statics

# >>> factory SetOWMapEvent_SRAMOrVRAM
CONTRACT["SetOWMapEvent_SRAMOrVRAM"] = {"compare": ("a", "hl", "b", "c", "d", "e"), "preserve": ("hl", "b", "c", "d", "e")}
CASES["SetOWMapEvent_SRAMOrVRAM"] = [
    {"a": 0x00, "wram": {wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wOWMapEvents: 1, wCurTilemap: 1, wPermissionMap: 256}},
    {"a": 0x02, "wram": {wCurTilemap: b"\x00", wConsole: b"\x02"},
     "read": {(wOWMapEvents + 2): 1, wCurTilemap: 1, wPermissionMap: 256}},
    dict(POISON, a=0x00, wram={wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wOWMapEvents: 1, wCurTilemap: 1, wPermissionMap: 256}),
]
# <<< factory SetOWMapEvent_SRAMOrVRAM

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
# >>> factory-mutation SetOWMapEvent_SRAMOrVRAM
MUTATIONS["SetOWMapEvent_SRAMOrVRAM"] = {"source_symbol": "SetOWMapEvent_SRAMOrVRAM", "before": "\tgb_write8((uint16_t)(wOWMapEvents_ADDR + event_index), TRUE);", "after": "\tgb_write8((uint16_t)(wOWMapEvents_ADDR + event_index), 0u);", "case_ids": ["SetOWMapEvent_SRAMOrVRAM-0", "SetOWMapEvent_SRAMOrVRAM-1"]}
# <<< factory-mutation SetOWMapEvent_SRAMOrVRAM
