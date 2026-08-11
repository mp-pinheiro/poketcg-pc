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
