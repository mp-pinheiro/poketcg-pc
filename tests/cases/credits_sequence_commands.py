wSequenceCmdPtr = 0xD631
wSequenceDelay = 0xD633

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SetCreditsSequenceCmdPtr": {"compare": ("b", "c", "d", "e", "hl"),
                                  "preserve": ("b", "c", "d", "e", "hl")},
    "ExecuteCreditsSequenceCmd": {"compare": ("b", "c", "d", "e", "hl"),
                                  "preserve": ("b", "c", "d", "e", "hl")},
    "AdvanceCreditsSequenceCmdPtr": {"compare": ("b", "c", "d", "e", "hl"),
                                     "preserve": ("b", "c", "d", "e", "hl")},
}
CASES = {
    "SetCreditsSequenceCmdPtr": [
        {"read": {wSequenceCmdPtr: 2, wSequenceDelay: 1}},
        dict(POISON, read={wSequenceCmdPtr: 2, wSequenceDelay: 1}),
    ],
    "ExecuteCreditsSequenceCmd": [
        {"wram": {wSequenceDelay: b"\xFF"}, "read": {wSequenceDelay: 1}},
        dict(POISON, wram={wSequenceDelay: b"\xFF"}, read={wSequenceDelay: 1}),
        {"wram": {wSequenceDelay: b"\x01"}, "read": {wSequenceDelay: 1}},
        {"wram": {wSequenceDelay: b"\x02"}, "read": {wSequenceDelay: 1}},
        {"wram": {wSequenceDelay: b"\x00", wSequenceCmdPtr: b"\x00\xC1"},
         "oracle": False,
         "why": "zero delay dispatches through CallHL2 into an unported credits command",
         "expect": {wSequenceDelay: b"\x00"}},
    ],
    "AdvanceCreditsSequenceCmdPtr": [
        {"a": 0, "wram": {wSequenceCmdPtr: b"\x00\x00"},
         "read": {wSequenceCmdPtr: 2}},
        dict(POISON, a=1, wram={wSequenceCmdPtr: b"\x00\x00"},
             read={wSequenceCmdPtr: 2}),
        {"a": 0xFF, "wram": {wSequenceCmdPtr: b"\xFF\xFF"},
         "read": {wSequenceCmdPtr: 2}},
        {"a": 0x00, "wram": {wSequenceCmdPtr: b"\xFE\x00"},
         "read": {wSequenceCmdPtr: 2}},
        {"a": 0xFF, "wram": {wSequenceCmdPtr: b"\x02\x01"},
         "read": {wSequenceCmdPtr: 2}},
    ],
}
# >>> factory AdvanceCreditsSequenceCmdPtrBy2
CONTRACT["AdvanceCreditsSequenceCmdPtrBy2"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy2"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([254, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy2

# >>> factory AdvanceCreditsSequenceCmdPtrBy3
CONTRACT["AdvanceCreditsSequenceCmdPtrBy3"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy3"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([253, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy3

# >>> factory AdvanceCreditsSequenceCmdPtrBy5
CONTRACT["AdvanceCreditsSequenceCmdPtrBy5"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy5"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([251, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy5

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "SetCreditsSequenceCmdPtr": {
        "source_symbol": "SetCreditsSequenceCmdPtr",
        "before": "gb_write8(wSequenceDelay_ADDR, 0);",
        "after": "gb_write8(wSequenceDelay_ADDR, 1);",
        "case_ids": ["SetCreditsSequenceCmdPtr-0", "SetCreditsSequenceCmdPtr-1"],
    },
    "ExecuteCreditsSequenceCmd": {
        "source_symbol": "ExecuteCreditsSequenceCmd",
        "before": "gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 1u));",
        "after": "gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 2u));",
        "case_ids": ["ExecuteCreditsSequenceCmd-2", "ExecuteCreditsSequenceCmd-3"],
    },
    "AdvanceCreditsSequenceCmdPtr": {
        "source_symbol": "AdvanceCreditsSequenceCmdPtr",
        "before": "ptr = (uint16_t)(ptr + a);",
        "after": "ptr = (uint16_t)(ptr + (uint8_t)(a << 1));",
        "case_ids": ["AdvanceCreditsSequenceCmdPtr-1", "AdvanceCreditsSequenceCmdPtr-2",
                     "AdvanceCreditsSequenceCmdPtr-4"],
    },
}
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy2
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy2"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy2",
    "before": "AdvanceCreditsSequenceCmdPtr(2u);",
    "after": "AdvanceCreditsSequenceCmdPtr(3u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy2-0", "AdvanceCreditsSequenceCmdPtrBy2-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy2
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy3
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy3"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy3",
    "before": "AdvanceCreditsSequenceCmdPtr(3u);",
    "after": "AdvanceCreditsSequenceCmdPtr(4u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy3-0", "AdvanceCreditsSequenceCmdPtrBy3-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy3
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy5
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy5"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy5",
    "before": "AdvanceCreditsSequenceCmdPtr(5u);",
    "after": "AdvanceCreditsSequenceCmdPtr(6u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy5-0", "AdvanceCreditsSequenceCmdPtrBy5-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy5
