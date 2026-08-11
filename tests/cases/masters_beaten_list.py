"""Oracle-diff cases for poketcg/src/engine/masters_beaten_list.asm."""

MASTERS_BEATEN_LIST = 0xD3BB
LIST_SIZE = 10

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "AddMasterBeatenToList": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "ClearMasterBeatenList": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "AddMasterBeatenToList": [
        {"a": 0x01, "wram": {MASTERS_BEATEN_LIST: b"\x00" * LIST_SIZE},
         "read": {MASTERS_BEATEN_LIST: LIST_SIZE}},
        dict(POISON, a=0x00,
             wram={MASTERS_BEATEN_LIST: bytes(range(1, LIST_SIZE + 1))},
             read={MASTERS_BEATEN_LIST: LIST_SIZE}),
        dict(POISON, a=0x01,
             wram={MASTERS_BEATEN_LIST: bytes([0x01] + [0x00] * (LIST_SIZE - 1))},
             read={MASTERS_BEATEN_LIST: LIST_SIZE}),
        dict(POISON, a=0x0A,
             wram={MASTERS_BEATEN_LIST: bytes(range(1, LIST_SIZE)) + b"\x00"},
             read={MASTERS_BEATEN_LIST: LIST_SIZE + 1}),
        dict(POISON, a=0xFF,
             wram={MASTERS_BEATEN_LIST: bytes(range(1, LIST_SIZE + 1))},
             read={MASTERS_BEATEN_LIST: LIST_SIZE}),
    ],
    "ClearMasterBeatenList": [
        {"wram": {MASTERS_BEATEN_LIST: b"\xff" * LIST_SIZE},
         "read": {MASTERS_BEATEN_LIST: LIST_SIZE}},
        dict(POISON, wram={MASTERS_BEATEN_LIST: b"\xaa\xbb\xcc\xdd\xee\xff\x11\x22\x33\x44"},
             read={MASTERS_BEATEN_LIST: LIST_SIZE}),
    ],
}

MUTATIONS = {
    "AddMasterBeatenToList": {
        "source_symbol": "AddMasterBeatenToList",
        "before": "gb_write8((uint16_t)(wMastersBeatenList_ADDR + i), a);",
        "after": "gb_write8((uint16_t)(wMastersBeatenList_ADDR + i + 1u), a);",
        "case_ids": ["AddMasterBeatenToList-0", "AddMasterBeatenToList-2", "AddMasterBeatenToList-3"],
    },
    "ClearMasterBeatenList": {
        "source_symbol": "ClearMasterBeatenList",
        "before": "i < MASTERS_BEATEN_LIST_SIZE",
        "after": "i < (MASTERS_BEATEN_LIST_SIZE - 1u)",
        "case_ids": ["ClearMasterBeatenList-0", "ClearMasterBeatenList-1"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
