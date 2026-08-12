"""Oracle-diff cases for poketcg/src/home/write_number.asm.

WriteOneByteNumber (90-111) and WriteTwoByteNumber (115-125) drive
TwoByteNumberToText. WriteBCDDigitInTextFormat (78-86) and
WriteBCDNumberInTextFormat (69-74) are BCD digit/number primitives, portable
even though every caller in this file (WriteOneDigitBCDNumber,
WriteTwoDigitBCDNumber, WriteFourDigitBCDNumber) remains dead code per
docs/port-contract.md:370-372 (zero external callsites in poketcg/src).
WriteTwoDigitBCDNumber (3-19) and WriteFourDigitBCDNumber (43-64) are ported
below for the same reason: they call BCCoordToBGMap0Address and
SafeCopyDataHLtoDE (already landed in bg_map.c/empty_screen.c) through the
JPHblankCopyDataHLtoDE alias, so nothing left blocks them even though
WriteOneDigitBCDNumber does not yet exist in C.
"""

DEST = 0xC300
FILL = b"\xff" * 7  # seven bytes: the seventh proves de stops after five digits

CONTRACT = {
    "TwoByteNumberToText": {
        "compare": ("b", "c", "d", "e"),
        "preserve": ("b", "c"),
    },
    "WriteBCDDigitInTextFormat": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
    "WriteBCDNumberInTextFormat": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
    "WriteTwoDigitBCDNumber": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "WriteFourDigitBCDNumber": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "WriteOneDigitBCDNumber": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "WriteOneByteNumber": {
        "compare": ("b", "c", "hl"),
        "preserve": ("b", "c", "hl"),
    },
    "WriteTwoByteNumber": {
        "compare": ("b", "c"),
        "preserve": ("b", "c"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}


def case(hl, **kw):
    return dict(POISON, hl=hl, d=DEST >> 8, e=DEST & 0xFF, wram={DEST: FILL}, **kw)


BCD_DST = 0xC110


def bcd_case(a, **kw):
    return dict(POISON, a=a, hl=BCD_DST, wram={BCD_DST: b"\xff"}, read={BCD_DST: 1}, **kw)


def bcd2_case(a, **kw):
    return dict(POISON, a=a, hl=BCD_DST, wram={BCD_DST: b"\xff\xff"}, read={BCD_DST: 2}, **kw)


WSTR = 0xCAA0
BGMAP0 = 0x9800


def two_digit_case(a, b, c, **kw):
    dst = BGMAP0 + c * 32 + b
    return dict(POISON, a=a, b=b, c=c,
                wram={WSTR: b"\xff\xff\x11"}, read={WSTR: 3, dst: 3}, **kw)


def four_digit_case(hl, b, c, **kw):
    dst = BGMAP0 + c * 32 + b
    return dict(POISON, hl=hl, b=b, c=c,
                wram={WSTR: b"\xff\xff\xff\xff\x11"}, read={WSTR: 5, dst: 5}, **kw)


def one_digit_case(a, b, c, **kw):
    dst = BGMAP0 + c * 32 + b
    return dict(POISON, a=a, b=b, c=c,
                wram={WSTR: b"\xff\x11"}, read={WSTR: 2, dst: 2}, **kw)


def one_byte_case(a, b, c, **kw):
    dst = BGMAP0 + c * 32 + b
    return dict(POISON, a=a, b=b, c=c,
                wram={WSTR: b"\xff\xff\xff\x11"}, read={WSTR: 4, dst: 4}, **kw)


def two_byte_case(hl, b, c, **kw):
    dst = BGMAP0 + c * 32 + b
    return dict(POISON, hl=hl, b=b, c=c,
                wram={WSTR: b"\xff\xff\xff\xff\xff\xff\x11"}, read={WSTR: 7, dst: 6}, **kw)


CASES = {
    "TwoByteNumberToText": [
        {},
        case(0),  # "00000": no leading-zero suppression
        case(1),
        case(9),
        case(10),
        case(10000),
        case(12345),
        case(9999),  # "09999": every place but the first at its maximum digit
        case(65535),
        # de advanced by five, read back without seeding the buffer first.
        dict(POISON, hl=54321, d=DEST >> 8, e=DEST & 0xFF, read={DEST: 6}),
    ],
    "WriteBCDDigitInTextFormat": [
        {},
        bcd_case(0xF0),
        bcd_case(0x09),
        bcd_case(0x0A),
        bcd_case(0x0F),
        bcd_case(0xAA),
    ],
    "WriteBCDNumberInTextFormat": [
        {},
        bcd2_case(0x00),
        bcd2_case(0x99),
        bcd2_case(0x9A),
        bcd2_case(0xA9),
        bcd2_case(0xAA),
        bcd2_case(0xFF),
    ],
    "WriteTwoDigitBCDNumber": [
        {},
        two_digit_case(0xAA, 7, 4),
        two_digit_case(0x99, 27, 62),
    ],
    "WriteFourDigitBCDNumber": [
        {},
        four_digit_case(0xAAAA, 7, 4),
        four_digit_case(0x9999, 27, 62),
    ],
    "WriteOneDigitBCDNumber": [
        {},
        one_digit_case(0xAA, 7, 4),
        one_digit_case(0x99, 27, 62),
    ],
    "WriteOneByteNumber": [
        {},
        one_byte_case(0xFF, 7, 4),
        one_byte_case(100, 27, 62),
    ],
    "WriteTwoByteNumber": [
        {},
        two_byte_case(54321, 7, 4),
        two_byte_case(65535, 27, 62),
    ],
}
SCHEMA2_CASES = {
    "TwoByteNumberToText": [
        {
            "id": "TwoByteNumberToText-12345",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, hl=12345, d=DEST >> 8, e=DEST & 0xFF),
            "bus": {},
            "seeds": {"wram": {DEST: FILL}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 10000,
            "cycle_budget": 100000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
    ],
}
from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES["WriteBCDDigitInTextFormat"] = legacy_to_schema(
    {"WriteBCDDigitInTextFormat": CASES["WriteBCDDigitInTextFormat"]},
    {"WriteBCDDigitInTextFormat": CONTRACT["WriteBCDDigitInTextFormat"]},
)["WriteBCDDigitInTextFormat"]
SCHEMA2_CASES["WriteBCDNumberInTextFormat"] = legacy_to_schema(
    {"WriteBCDNumberInTextFormat": CASES["WriteBCDNumberInTextFormat"]},
    {"WriteBCDNumberInTextFormat": CONTRACT["WriteBCDNumberInTextFormat"]},
)["WriteBCDNumberInTextFormat"]
SCHEMA2_CASES["WriteTwoDigitBCDNumber"] = legacy_to_schema(
    {"WriteTwoDigitBCDNumber": CASES["WriteTwoDigitBCDNumber"]},
    {"WriteTwoDigitBCDNumber": CONTRACT["WriteTwoDigitBCDNumber"]},
)["WriteTwoDigitBCDNumber"]
SCHEMA2_CASES["WriteFourDigitBCDNumber"] = legacy_to_schema(
    {"WriteFourDigitBCDNumber": CASES["WriteFourDigitBCDNumber"]},
    {"WriteFourDigitBCDNumber": CONTRACT["WriteFourDigitBCDNumber"]},
)["WriteFourDigitBCDNumber"]
SCHEMA2_CASES["WriteOneDigitBCDNumber"] = legacy_to_schema(
    {"WriteOneDigitBCDNumber": CASES["WriteOneDigitBCDNumber"]},
    {"WriteOneDigitBCDNumber": CONTRACT["WriteOneDigitBCDNumber"]},
)["WriteOneDigitBCDNumber"]
SCHEMA2_CASES["WriteOneByteNumber"] = legacy_to_schema(
    {"WriteOneByteNumber": CASES["WriteOneByteNumber"]},
    {"WriteOneByteNumber": CONTRACT["WriteOneByteNumber"]},
)["WriteOneByteNumber"]
SCHEMA2_CASES["WriteTwoByteNumber"] = legacy_to_schema(
    {"WriteTwoByteNumber": CASES["WriteTwoByteNumber"]},
    {"WriteTwoByteNumber": CONTRACT["WriteTwoByteNumber"]},
)["WriteTwoByteNumber"]
MUTATIONS = {
    "TwoByteNumberToText": {
        "source_symbol": "TwoByteNumberToText",
        "before": "(uint16_t)-10, (uint16_t)-1,",
        "after": "(uint16_t)-10, (uint16_t)-2,",
        "case_ids": ["TwoByteNumberToText-12345"],
    },
    "WriteBCDDigitInTextFormat": {
        "source_symbol": "WriteBCDDigitInTextFormat",
        "before": "c = (uint8_t)(c + 0x07u);",
        "after": "c = (uint8_t)(c + 0x08u);",
        "case_ids": ["WriteBCDDigitInTextFormat-3", "WriteBCDDigitInTextFormat-4"],
    },
    "WriteBCDNumberInTextFormat": {
        "source_symbol": "WriteBCDNumberInTextFormat",
        "before": "uint8_t swapped = (uint8_t)((a << 4) | (a >> 4));",
        "after": "uint8_t swapped = (uint8_t)((a << 4) | (a >> 3));",
        "case_ids": ["WriteBCDNumberInTextFormat-3", "WriteBCDNumberInTextFormat-4"],
    },
    "WriteTwoDigitBCDNumber": {
        "source_symbol": "WriteTwoDigitBCDNumber",
        "before": "SafeCopyDataHLtoDE(&src, &dst, 2u);",
        "after": "SafeCopyDataHLtoDE(&src, &dst, 3u);",
        "case_ids": ["WriteTwoDigitBCDNumber-1", "WriteTwoDigitBCDNumber-2"],
    },
    "WriteFourDigitBCDNumber": {
        "source_symbol": "WriteFourDigitBCDNumber",
        "before": "SafeCopyDataHLtoDE(&src, &dst, 4u);",
        "after": "SafeCopyDataHLtoDE(&src, &dst, 5u);",
        "case_ids": ["WriteFourDigitBCDNumber-1", "WriteFourDigitBCDNumber-2"],
    },
    "WriteOneDigitBCDNumber": {
        "source_symbol": "WriteOneDigitBCDNumber",
        "before": "SafeCopyDataHLtoDE(&src, &dst, 1u);",
        "after": "SafeCopyDataHLtoDE(&src, &dst, 2u);",
        "case_ids": ["WriteOneDigitBCDNumber-1", "WriteOneDigitBCDNumber-2"],
    },
    "WriteOneByteNumber": {
        "source_symbol": "WriteOneByteNumber",
        "before": "SafeCopyDataHLtoDE(&src, &dst, 3u);",
        "after": "SafeCopyDataHLtoDE(&src, &dst, 4u);",
        "case_ids": ["WriteOneByteNumber-1", "WriteOneByteNumber-2"],
    },
    "WriteTwoByteNumber": {
        "source_symbol": "WriteTwoByteNumber",
        "before": "SafeCopyDataHLtoDE(&src, &dst, 5u);",
        "after": "SafeCopyDataHLtoDE(&src, &dst, 4u);",
        "case_ids": ["WriteTwoByteNumber-1", "WriteTwoByteNumber-2"],
    },
}
