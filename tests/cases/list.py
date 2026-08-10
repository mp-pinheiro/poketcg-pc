"""Oracle-diff cases for poketcg/src/home/list.asm."""

wListPointer = 0xCB72
BUF = 0xC200

CONTRACT = {
    "SetListPointer": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
    "SetNextElementOfList": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CASES = {
    "SetListPointer": [
        {"wram": {wListPointer: b"\xff\xff"}},
        dict(POISON, wram={wListPointer: b"\x00\x00"}),
        dict(POISON, d=0xFF, e=0xFF, wram={wListPointer: b"\x11\x22"}),
        dict(POISON, d=BUF >> 8, e=BUF & 0xFF, wram={wListPointer: b"\xff\xff"}),
    ],
    "SetNextElementOfList": [
        {"wram": {wListPointer: bytes([BUF & 0xFF, BUF >> 8]), BUF: b"\xff"}},
        # Reads back both the written element and the advanced pointer.
        dict(POISON, wram={wListPointer: b"\x10\xc2", 0xC210: b"\x00"},
             read={wListPointer: 2}),
        # $DFFF + 1 crosses a page: the stored pointer must become $E000.
        dict(POISON, a=0x5A, wram={wListPointer: b"\xff\xdf", 0xDFFF: b"\x00"},
             read={wListPointer: 2}),
        dict(POISON, a=0x01, wram={wListPointer: b"\xff\xc0", 0xC0FF: b"\x00"},
             read={wListPointer: 2}),
        # The list pointing at itself pins the write order of the inlined writeback.
        dict(POISON, wram={wListPointer: b"\x72\xcb"}, read={wListPointer: 2}),
        # $FFFF + 1 wraps the 16-bit pointer to $0000.
        dict(POISON, a=0x3C, wram={wListPointer: b"\xff\xff", 0xFFFF: b"\x00"},
             read={wListPointer: 2}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SetListPointer": {
        "source_symbol": "SetListPointer",
        "before": "gb_write8(wListPointer_ADDR, (uint8_t)de);",
        "after": "gb_write8(wListPointer_ADDR, (uint8_t)(de ^ 0xFF));",
        "case_ids": ["SetListPointer-0", "SetListPointer-1", "SetListPointer-2", "SetListPointer-3"],
    },
}
