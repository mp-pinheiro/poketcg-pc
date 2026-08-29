POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCardPopCardCandidates = 0xC400

CONTRACT = {
    "CreateCardPopCandidateList": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "CalculateNameHash": {"compare": ("b", "d", "e", "hl"), "preserve": ("b",)},
}

CASES = {
    "CreateCardPopCandidateList": [
        {"instruction_budget": 500000, "cycle_budget": 5000000, "wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        {"instruction_budget": 500000, "cycle_budget": 5000000, "a": 1, "wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        {"instruction_budget": 500000, "cycle_budget": 5000000, "a": 2, "wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        dict(POISON, a=0, instruction_budget=500000, cycle_budget=5000000, wram={wCardPopCardCandidates: b"\xaa" * 0x80}, read={wCardPopCardCandidates: 0x80}),
        dict(POISON, a=0xff, instruction_budget=500000, cycle_budget=5000000, wram={wCardPopCardCandidates: b"\xaa" * 0x80}, read={wCardPopCardCandidates: 0x80}),
    ],
    "CalculateNameHash": [
        {"wram": {0xC100: b"\x00" * 16}},
        {"hl": 0xC100, "wram": {0xC100: bytes(range(16))}},
        {"hl": 0xC200, "wram": {0xC200: b"\xff\x01\xfe\x02\xfd\x03\xfc\x04\xfb\x05\xfa\x06\xf9\x07\xf8\x08"}},
        dict(POISON, hl=0xC300, wram={0xC300: bytes((0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0xFF))}),
    ],
}

# >>> factory LookUpNameInCardPopNameList
CONTRACT["LookUpNameInCardPopNameList"] = {"compare": (), "preserve": ()}
CASES["LookUpNameInCardPopNameList"] = [
    {"wram": {0xC000: b"ALICE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xC500: b"ALICE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"}, "read": {0xC5F3: 1}},
    {"ramg": False, "wram": {0xC000: b"BOB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xC200: b"CAROL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xC500: b"ALICE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"}, "sram": {0: {0xA010: b"CAROL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"}}, "read": {0xC5F3: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xC000: b"DAVE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xC500: b"DAVE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"}, "read": {0xC5F3: 1}}
]
# <<< factory LookUpNameInCardPopNameList

# >>> factory DecideCardToReceiveFromCardPop
CONTRACT["DecideCardToReceiveFromCardPop"] = {"compare": ("a",), "preserve": ()}
CASES["DecideCardToReceiveFromCardPop"] = [
    {"sram": {0: {0xA010: b"\x00" * 16}}, "wram": {0xC500: b"\x00" * 16},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, sram={0: {0xA010: b"\x00" * 16}}, wram={0xC500: b"\x00" * 16},
         instruction_budget=20000000, cycle_budget=80000000),
    {"sram": {0: {0xA010: b"\x00" * 16}}, "wram": {0xC500: b"\xFB" + b"\x00" * 15}},
]
# <<< factory DecideCardToReceiveFromCardPop

# >>> factory HandleCardPopCommunications
CONTRACT["HandleCardPopCommunications"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["HandleCardPopCommunications"] = [
    {"oracle": True, "evidence": "primary", "why": "Card Pop communication depends on external infrared hardware; this deterministic native no-peer case drives the D-pad abort and checks the SRAM-to-WRAM name-list copy and failure return.", "keys": 0x02, "setup": [{"fn": "EnableLCD"}], "sram": {0: {0xBB00: bytes([0x5a]) * 0x100}}, "read": {0xC000: 0x100}, "expect": {0xC000: bytes([0x5a]) * 0x100}, "expect_regs": {"a": 0x02, "f": 0x10, "hl": 0x018B}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="Card Pop communication depends on external infrared hardware; this deterministic native no-peer case drives the D-pad abort with poisoned registers and checks the SRAM-to-WRAM name-list copy and failure return.", keys=0x02, setup=[{"fn": "EnableLCD"}], sram={0: {0xBB00: bytes([0x5a]) * 0x100}}, read={0xC000: 0x100}, expect={0xC000: bytes([0x5a]) * 0x100}, expect_regs={"a": 0x02, "f": 0x10, "hl": 0x018B}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandleCardPopCommunications

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
hWhoseTurn = 0xFF97
wLCDC = 0xCABB
# <<< factory-cases-statics

# >>> factory _DoCardPop
CONTRACT["_DoCardPop"] = {"compare": (), "preserve": ()}
CASES["_DoCardPop"] = [
    {"oracle": False, "evidence": "primary", "why": "The SGB guard deterministically takes Card Pop!'s error-screen path without requiring infrared hardware; the seeded turn byte verifies that the communication branch is not entered.", "wram": {wConsole: b"\x01", hWhoseTurn: b"\x00", wLCDC: b"\x00"}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {hWhoseTurn: 1}, "expect": {hWhoseTurn: b"\x00"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The SGB guard deterministically takes Card Pop!'s error-screen path without requiring infrared hardware; poisoned entry registers must not alter the turn byte.", wram={wConsole: b"\x01", hWhoseTurn: b"\x00", wLCDC: b"\x00"}, keys=[0x00, 0x01], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={hWhoseTurn: 1}, expect={hWhoseTurn: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _DoCardPop

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CreateCardPopCandidateList": {
        "source_symbol": "CreateCardPopCandidateList",
        "before": "\t\tif ((uint8_t)(wLoadedCard1Type & TYPE_ENERGY) != 0)",
        "after": "\t\tif ((uint8_t)(wLoadedCard1Type & TYPE_ENERGY) == 0)",
        "case_ids": ["CreateCardPopCandidateList-0", "CreateCardPopCandidateList-1", "CreateCardPopCandidateList-2", "CreateCardPopCandidateList-3", "CreateCardPopCandidateList-4"],
    },
    "CalculateNameHash": {
        "source_symbol": "CalculateNameHash",
        "before": "\t\tlow = (uint8_t)(low + value);",
        "after": "\t\tlow = (uint8_t)(low ^ value);",
        "case_ids": ["CalculateNameHash-1", "CalculateNameHash-2", "CalculateNameHash-3"],
    },
}
# >>> factory-mutation LookUpNameInCardPopNameList
MUTATIONS["LookUpNameInCardPopNameList"] = {"source_symbol": "LookUpNameInCardPopNameList", "before": "\t\t\tresult = 0xff;", "after": "\t\t\tresult = 0x00;", "case_ids": ["LookUpNameInCardPopNameList-0", "LookUpNameInCardPopNameList-2"]}
# <<< factory-mutation LookUpNameInCardPopNameList
# >>> factory-mutation DecideCardToReceiveFromCardPop
MUTATIONS["DecideCardToReceiveFromCardPop"] = {"source_symbol": "DecideCardToReceiveFromCardPop", "before": "card_e = (d & 0x01u) ? MEW_LV15 : VENUSAUR_LV64;", "after": "card_e = (d & 0x01u) ? VENUSAUR_LV64 : MEW_LV15;", "case_ids": ["DecideCardToReceiveFromCardPop-2"]}
# <<< factory-mutation DecideCardToReceiveFromCardPop
# >>> factory-mutation HandleCardPopCommunications
MUTATIONS["HandleCardPopCommunications"] = {"source_symbol": "HandleCardPopCommunications", "before": "HandleCardPopCommunicationsResult HandleCardPopCommunications(void)\n{\n\tuint16_t copy_src = sCardPopNameList_ADDR;", "after": "HandleCardPopCommunicationsResult HandleCardPopCommunications(void)\n{\n\tuint16_t copy_src = wCardPopNameList_ADDR;", "case_ids": ["HandleCardPopCommunications-0", "HandleCardPopCommunications-1"]}
# <<< factory-mutation HandleCardPopCommunications
# >>> factory-mutation _DoCardPop
MUTATIONS["_DoCardPop"] = {"source_symbol": "_DoCardPop", "before": "\tif (wConsole == CONSOLE_SGB)\n\t\tgoto error;", "after": "\tif (wConsole == CONSOLE_SGB) {\n\t\thWhoseTurn = 1u;\n\t\tgoto error;\n\t}", "case_ids": ["_DoCardPop-0", "_DoCardPop-1"]}
# <<< factory-mutation _DoCardPop
