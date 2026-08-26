POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPCPackSelection = 0xD11D
wPCPacks = 0xD11E

CONTRACT = {
    "GePCPackSelectionCoordinates": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "TryGivePCPack": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "GePCPackSelectionCoordinates": [
        {"wram": {wPCPackSelection: b"\x00"}},
        {"wram": {wPCPackSelection: b"\x0e"}},
        dict(POISON, wram={wPCPackSelection: b"\x0e"}),
    ],
    "TryGivePCPack": [
        {"wram": {wPCPacks: bytes(15)}},
        {"a": 1, "wram": {wPCPacks: bytes(15)}, "read": {wPCPacks: 15}},
        {"a": 15, "wram": {wPCPacks: bytes(14) + b"\x01"}, "read": {wPCPacks: 15}},
        dict(POISON, a=10, wram={wPCPacks: b"\x81\x02" + bytes(13)}, read={wPCPacks: 15}),
        {"a": 0x7f, "wram": {wPCPacks: bytes([1] * 15)}, "read": {wPCPacks: 15}},
    ],
}

# >>> factory InitPCPacks

CONTRACT["InitPCPacks"] = {"compare": (), "preserve": ()}
CASES["InitPCPacks"] = [
	{"wram": {wPCPacks: bytes(15), wPCPackSelection: b"\x05"},
	 "read": {wPCPacks: 15}},
	dict(POISON, wram={wPCPacks: bytes([0xff] * 15), wPCPackSelection: b"\x0e"},
	     read={wPCPacks: 15}),
]
# <<< factory InitPCPacks

# >>> factory DrawMailMenuCursor

CONTRACT["DrawMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["DrawMailMenuCursor"] = [
	{"a": 0x3f, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"a": 1, "wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, a=2, wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory DrawMailMenuCursor

# >>> factory GetPCPackCoordinates

CONTRACT["GetPCPackCoordinates"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetPCPackCoordinates"] = [
	{"a": 0, "wram": {wPCPackSelection: b"\x00"}},
	{"a": 14, "wram": {wPCPackSelection: b"\x00"}},
	dict(POISON, a=7, wram={wPCPackSelection: b"\x03"}),
]
# <<< factory GetPCPackCoordinates

# >>> factory ShowMailMenuCursor
CONTRACT["ShowMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["ShowMailMenuCursor"] = [
	{"wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory ShowMailMenuCursor

# >>> factory HideMailMenuCursor
CONTRACT["HideMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["HideMailMenuCursor"] = [
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, setup=[{"fn": "ShowMailMenuCursor"}], wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory HideMailMenuCursor

# >>> factory PrintEmptyPCPackName
CONTRACT["PrintEmptyPCPackName"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PrintEmptyPCPackName"] = [
	{"setup": [{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 2, "c": 2}],
	 "a": 0, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9842: 1}}},
	{"setup": [{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 14, "c": 10}],
	 "a": 14, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x994e: 1}}},
	dict(POISON, setup=[{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 8, "c": 6}],
	     a=7, wram={wPCPackSelection: b"\x03"}, vread={0: {0x98c8: 1}}),
]
# <<< factory PrintEmptyPCPackName

# >>> factory-cases-statics
wCursorBlinkTimer = 0xD11C

hDPadHeld = 0xFF8F
wPCLastDirectionPressed = 0xD12D
# <<< factory-cases-statics

# >>> factory UpdateMailMenuCursor
CONTRACT["UpdateMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["UpdateMailMenuCursor"] = [
	{"wram": {0xD11C: b"\x00", wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {0xD11C: b"\x10", wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, wram={0xD11C: b"\x0f", wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory UpdateMailMenuCursor

# >>> factory PCMailHandleDPadInput
CONTRACT["PCMailHandleDPadInput"] = {"compare": (), "preserve": ()}
CASES["PCMailHandleDPadInput"] = [
    {"hDPadHeld": 0, "wram": {hDPadHeld: b"\x00", wPCPackSelection: b"\x00", wCursorBlinkTimer: b"\xAA"}, "read": {wPCPackSelection: 1, wCursorBlinkTimer: 1}},
    {"hDPadHeld": 0x10, "wram": {hDPadHeld: b"\x10", wPCPackSelection: b"\x00", wPCPacks: bytes([1] * 15), wCursorBlinkTimer: b"\xAA"}, "read": {wPCLastDirectionPressed: 1, wPCPackSelection: 1, wCursorBlinkTimer: 1}, "vread": {0: {0x9841: 1, 0x9847: 1}, 1: {0x9841: 1, 0x9847: 1}}},
    dict(POISON, hDPadHeld=0x40, wram={hDPadHeld: b"\x40", wPCPackSelection: b"\x0E", wPCPacks: bytes([1] * 15), wCursorBlinkTimer: b"\xAA"}, read={wPCLastDirectionPressed: 0, wPCPackSelection: 11, wCursorBlinkTimer: 1}, vread={0: {0x994D: 1, 0x9901: 1}, 1: {0x994D: 1, 0x9901: 1}}),
]
# <<< factory PCMailHandleDPadInput

# >>> factory GetPCPackNameTextID
CONTRACT["GetPCPackNameTextID"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")}
CASES["GetPCPackNameTextID"] = [
    {"a": 0, "expect_regs": {"b": 0, "c": 0, "d": 0x03, "e": 0x5D, "hl": 0}},
    {"a": 0x0E, "expect_regs": {"b": 0, "c": 0, "d": 0x03, "e": 0x6B, "hl": 0}},
    dict(POISON, a=1, expect_regs={"b": 0xBB, "c": 0xCC, "d": 0x03, "e": 0x5E, "hl": 0x1234}),
]
# <<< factory GetPCPackNameTextID

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GePCPackSelectionCoordinates": {
        "source_symbol": "GePCPackSelectionCoordinates",
        "before": "pc_mail_coordinates[selection][0],",
        "after": "pc_mail_coordinates[selection][1],",
        "case_ids": ["GePCPackSelectionCoordinates-0", "GePCPackSelectionCoordinates-1", "GePCPackSelectionCoordinates-2"],
    },
    "TryGivePCPack": {
        "source_symbol": "TryGivePCPack",
        "before": "if ((uint8_t)(gb_read8(slot) & 0x7f) == 0)",
        "after": "if ((uint8_t)(gb_read8(slot) & 0x7f) != 0)",
        "case_ids": ["TryGivePCPack-0", "TryGivePCPack-1", "TryGivePCPack-3", "TryGivePCPack-4"],
    },
}
# >>> factory-mutation InitPCPacks

MUTATIONS["InitPCPacks"] = {
	"source_symbol": "InitPCPacks",
	"before": "TryGivePCPack(1u);",
	"after": "TryGivePCPack(0u);",
	"case_ids": ["InitPCPacks-0", "InitPCPacks-1"],
}
# <<< factory-mutation InitPCPacks
# >>> factory-mutation DrawMailMenuCursor

MUTATIONS["DrawMailMenuCursor"] = {
	"source_symbol": "DrawMailMenuCursor",
	"before": "WriteByteToBGMap0(symbol, coords.b, coords.c);",
	"after": "WriteByteToBGMap0(symbol, coords.c, coords.b);",
	"case_ids": ["DrawMailMenuCursor-0", "DrawMailMenuCursor-1", "DrawMailMenuCursor-2"],
}
# <<< factory-mutation DrawMailMenuCursor
# >>> factory-mutation GetPCPackCoordinates

MUTATIONS["GetPCPackCoordinates"] = {
	"source_symbol": "GetPCPackCoordinates",
	"before": "coords.b++;",
	"after": "coords.b--;",
	"case_ids": ["GetPCPackCoordinates-0", "GetPCPackCoordinates-1", "GetPCPackCoordinates-2"],
}
# <<< factory-mutation GetPCPackCoordinates
# >>> factory-mutation ShowMailMenuCursor
MUTATIONS["ShowMailMenuCursor"] = {
	"source_symbol": "ShowMailMenuCursor",
	"before": "void ShowMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_CURSOR_R);\n}",
	"after": "void ShowMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_SPACE);\n}",
	"case_ids": ["ShowMailMenuCursor-0", "ShowMailMenuCursor-1", "ShowMailMenuCursor-2"],
}
# <<< factory-mutation ShowMailMenuCursor
# >>> factory-mutation HideMailMenuCursor
MUTATIONS["HideMailMenuCursor"] = {
	"source_symbol": "HideMailMenuCursor",
	"before": "void HideMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_SPACE);\n}",
	"after": "void HideMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_CURSOR_R);\n}",
	"case_ids": ["HideMailMenuCursor-0", "HideMailMenuCursor-1", "HideMailMenuCursor-2"],
}
# <<< factory-mutation HideMailMenuCursor
# >>> factory-mutation PrintEmptyPCPackName
MUTATIONS["PrintEmptyPCPackName"] = {
	"source_symbol": "PrintEmptyPCPackName",
	"before": "InitTextPrinting(coords.b, coords.c);",
	"after": "InitTextPrinting(coords.c, coords.b);",
	"case_ids": ["PrintEmptyPCPackName-1", "PrintEmptyPCPackName-2"],
}
# <<< factory-mutation PrintEmptyPCPackName
# >>> factory-mutation UpdateMailMenuCursor
MUTATIONS["UpdateMailMenuCursor"] = {
	"source_symbol": "UpdateMailMenuCursor",
	"before": "if ((wCursorBlinkTimer & 0x10u) == 0u)",
	"after": "if ((wCursorBlinkTimer & 0x10u) != 0u)",
	"case_ids": ["UpdateMailMenuCursor-1", "UpdateMailMenuCursor-0", "UpdateMailMenuCursor-2"],
}
# <<< factory-mutation UpdateMailMenuCursor
# >>> factory-mutation PCMailHandleDPadInput
MUTATIONS["PCMailHandleDPadInput"] = {"source_symbol": "PCMailHandleDPadInput", "before": "if ((gb_read8(hDPadHeld_ADDR) & PAD_CTRL_PAD) == 0u)", "after": "if ((gb_read8(hDPadHeld_ADDR) & 0x00u) == 0u)", "case_ids": ["PCMailHandleDPadInput-1", "PCMailHandleDPadInput-2"]}
# <<< factory-mutation PCMailHandleDPadInput
# >>> factory-mutation GetPCPackNameTextID
MUTATIONS["GetPCPackNameTextID"] = {"source_symbol": "GetPCPackNameTextID", "before": "uint16_t GetPCPackNameTextID(uint8_t a)\n{\n\treturn (uint16_t)(0x035Du + (uint16_t)a);\n}", "after": "uint16_t GetPCPackNameTextID(uint8_t a)\n{\n\treturn (uint16_t)(0x035Eu + (uint16_t)a);\n}", "case_ids": ["GetPCPackNameTextID-0", "GetPCPackNameTextID-1", "GetPCPackNameTextID-2"]}
# <<< factory-mutation GetPCPackNameTextID
