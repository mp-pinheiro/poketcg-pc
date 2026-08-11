POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCardPopCardCandidates = 0xC400

CONTRACT = {
    "CreateCardPopCandidateList": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CalculateNameHash": {"compare": ("b", "d", "e", "hl"), "preserve": ("b",)},
}

CASES = {
    "CreateCardPopCandidateList": [
        {"wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        {"a": 1, "wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        {"a": 2, "wram": {wCardPopCardCandidates: b"\xaa" * 0x80}, "read": {wCardPopCardCandidates: 0x80}},
        dict(POISON, a=0, wram={wCardPopCardCandidates: b"\xaa" * 0x80}, read={wCardPopCardCandidates: 0x80}),
        dict(POISON, a=0xff, wram={wCardPopCardCandidates: b"\xaa" * 0x80}, read={wCardPopCardCandidates: 0x80}),
    ],
    "CalculateNameHash": [
        {"wram": {0xC100: b"\x00" * 16}},
        {"hl": 0xC100, "wram": {0xC100: bytes(range(16))}},
        {"hl": 0xC200, "wram": {0xC200: b"\xff\x01\xfe\x02\xfd\x03\xfc\x04\xfb\x05\xfa\x06\xf9\x07\xf8\x08"}},
        dict(POISON, hl=0xC300, wram={0xC300: bytes((0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0xFF))}),
    ],
}

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
        "before": "\t\thigh ^= value;",
        "after": "\t\thigh += value;",
        "case_ids": ["CalculateNameHash-1", "CalculateNameHash-2", "CalculateNameHash-3"],
    },
}
