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

# >>> factory AdvanceCreditsSequenceCmdPtrBy6
CONTRACT["AdvanceCreditsSequenceCmdPtrBy6"] = {
    "compare": ("b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["AdvanceCreditsSequenceCmdPtrBy6"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: b"\xFA\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xF9\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFC\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy6

# >>> factory AdvanceCreditsSequenceCmdPtrBy4
CONTRACT["AdvanceCreditsSequenceCmdPtrBy4"] = {
    "compare": ("b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["AdvanceCreditsSequenceCmdPtrBy4"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: b"\xFC\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFB\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFE\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy4

# >>> factory CreditsSequenceCmd_Wait
# wSequenceDelay = 0xD633 (given). SEQ_AREA is a diff-only watch window around the
# sequence-variable block: AdvanceCreditsSequenceCmdPtrBy3's pointer advance lands
# in WRAM near wSequenceDelay, so the window catches advance-corrupting mutations.
wSequenceDelay = 0xD633
SEQ_AREA = 0xD600
SEQ_AREA_LEN = 0x80
CONTRACT["CreditsSequenceCmd_Wait"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_Wait"] = [
	{"c": 0, "wram": {wSequenceDelay: b"\xff"}, "read": {SEQ_AREA: SEQ_AREA_LEN}},
	{"c": 1, "wram": {wSequenceDelay: b"\x00"}, "read": {SEQ_AREA: SEQ_AREA_LEN}},
	{"c": 0x80, "wram": {wSequenceDelay: b"\x01"}},
	dict(POISON, c=0x2A, wram={wSequenceDelay: b"\x7e"}, read={SEQ_AREA: SEQ_AREA_LEN}),
]
# <<< factory CreditsSequenceCmd_Wait


# >>> factory CreditsSequenceCmd_DisableLCD
# No register inputs are consumed and no register outputs survive the tail jump,
# so the cases watch the sequence-variable window the callee advances.
wSequenceDelay = 0xD633
SEQ_AREA = 0xD600
SEQ_AREA_LEN = 0x80
CONTRACT["CreditsSequenceCmd_DisableLCD"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_DisableLCD"] = [
	{"read": {SEQ_AREA: SEQ_AREA_LEN}},
	dict(POISON, read={SEQ_AREA: SEQ_AREA_LEN}),
]
# <<< factory CreditsSequenceCmd_DisableLCD


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
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy6
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy6"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy6",
    "before": "void AdvanceCreditsSequenceCmdPtrBy6(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(6u);\n}",
    "after": "void AdvanceCreditsSequenceCmdPtrBy6(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(7u);\n}",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy6-0", "AdvanceCreditsSequenceCmdPtrBy6-2",
                 "AdvanceCreditsSequenceCmdPtrBy6-3", "AdvanceCreditsSequenceCmdPtrBy6-4"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy6
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy4
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy4"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy4",
    "before": "void AdvanceCreditsSequenceCmdPtrBy4(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(4u);\n}",
    "after": "void AdvanceCreditsSequenceCmdPtrBy4(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(5u);\n}",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy4-0", "AdvanceCreditsSequenceCmdPtrBy4-2",
                 "AdvanceCreditsSequenceCmdPtrBy4-3", "AdvanceCreditsSequenceCmdPtrBy4-4"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy4
# >>> factory-mutation CreditsSequenceCmd_Wait
MUTATIONS["CreditsSequenceCmd_Wait"] = {
	"source_symbol": "CreditsSequenceCmd_Wait",
	"before": "\twSequenceDelay = c;",
	"after": "\twSequenceDelay = 0x00u;",
	"case_ids": ["CreditsSequenceCmd_Wait-1", "CreditsSequenceCmd_Wait-2", "CreditsSequenceCmd_Wait-3"],
}
# <<< factory-mutation CreditsSequenceCmd_Wait
# >>> factory-mutation CreditsSequenceCmd_DisableLCD
MUTATIONS["CreditsSequenceCmd_DisableLCD"] = {
	"source_symbol": "CreditsSequenceCmd_DisableLCD",
	"before": "\tDisableLCD();\n\tAdvanceCreditsSequenceCmdPtrBy2();",
	"after": "\tDisableLCD();\n\tAdvanceCreditsSequenceCmdPtrBy3();",
	"case_ids": ["CreditsSequenceCmd_DisableLCD-0", "CreditsSequenceCmd_DisableLCD-1"],
}
# <<< factory-mutation CreditsSequenceCmd_DisableLCD
