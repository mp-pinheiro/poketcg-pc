"""Oracle-diff cases for poketcg/src/engine/masters_beaten_list.asm."""

wMastersBeatenList = 0xD3BB
GUARD_LOW = wMastersBeatenList - 1
GUARD_HIGH = wMastersBeatenList + 10

CONTRACT = {
    "ClearMasterBeatenList": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "AddMasterBeatenToList": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CASES = {
    "ClearMasterBeatenList": [
        {"wram": {wMastersBeatenList: b"\xff" * 10}},
        dict(POISON, wram={wMastersBeatenList: b"\xaa\xbb\xcc\xdd\xee\xff\x11\x22\x33\x44"}),
        {"wram": {GUARD_LOW: b"\x5a", wMastersBeatenList: b"\x01" * 10, GUARD_HIGH: b"\xa5"}, "read": {wMastersBeatenList: 10}},
    ],
    "AddMasterBeatenToList": [
        {},
        dict(POISON, wram={wMastersBeatenList: b"\x00" * 10}, read={wMastersBeatenList: 10}),
        {"a": 0x07, "wram": {wMastersBeatenList: b"\x01\x02\x03\x04\x05\x06\x00\x08\x09\x0a"}, "read": {wMastersBeatenList: 10}},
        {"a": 0x07, "wram": {wMastersBeatenList: b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a"}, "read": {wMastersBeatenList: 10}},
        {"a": 0x0A, "wram": {wMastersBeatenList: b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x5a"}, "read": {wMastersBeatenList: 10}},
        {"a": 0x55, "wram": {GUARD_LOW: b"\x5a", wMastersBeatenList: b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a", GUARD_HIGH: b"\xa5"}, "read": {GUARD_LOW: 12}},
    ],
}

# >>> factory AddAllMastersToMastersBeatenList
CONTRACT["AddAllMastersToMastersBeatenList"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["AddAllMastersToMastersBeatenList"] = [
    {"wram": {wMastersBeatenList: b"\x00" * 10}, "read": {wMastersBeatenList: 10}},
    dict(POISON, wram={wMastersBeatenList: b"\x00" * 10}, read={wMastersBeatenList: 10}),
    {"wram": {wMastersBeatenList: b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a"}, "read": {wMastersBeatenList: 10}},
    {"wram": {GUARD_LOW: b"\x5a", wMastersBeatenList: b"\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00", GUARD_HIGH: b"\xa5"}, "read": {GUARD_LOW: 12}},
]
# <<< factory AddAllMastersToMastersBeatenList

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "ClearMasterBeatenList": {
        "source_symbol": "ClearMasterBeatenList",
        "before": "gb_write8(address, 0);",
        "after": "gb_write8(address, 0xFFu);",
        "case_ids": ["ClearMasterBeatenList-0", "ClearMasterBeatenList-1", "ClearMasterBeatenList-2"],
    },
    "AddMasterBeatenToList": {
        "source_symbol": "AddMasterBeatenToList",
        "before": "gb_write8(address, master);",
        "after": "gb_write8(address, (uint8_t)(master ^ 0xFFu));",
        "case_ids": ["AddMasterBeatenToList-1", "AddMasterBeatenToList-2", "AddMasterBeatenToList-4", "AddMasterBeatenToList-5"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation AddAllMastersToMastersBeatenList
MUTATIONS["AddAllMastersToMastersBeatenList"] = {
    "source_symbol": "AddAllMastersToMastersBeatenList",
    "before": "master_id <= MASTERS_BEATEN_COUNT",
    "after": "master_id < MASTERS_BEATEN_COUNT",
    "case_ids": [
        "AddAllMastersToMastersBeatenList-0",
        "AddAllMastersToMastersBeatenList-1",
        "AddAllMastersToMastersBeatenList-2",
        "AddAllMastersToMastersBeatenList-3",
    ],
}
# <<< factory-mutation AddAllMastersToMastersBeatenList
