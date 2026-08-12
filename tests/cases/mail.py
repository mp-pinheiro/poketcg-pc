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
