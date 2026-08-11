POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPCPackSelection = 0xD11D
wPCPacks = 0xD11E

CONTRACT = {
    "GePCPackSelectionCoordinates": {"compare": ("b", "c", "d", "e", "f", "hl"), "preserve": ("d", "e", "f", "hl")},
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
