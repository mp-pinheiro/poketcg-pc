"""Oracle-diff cases for poketcg/src/home/write_number.asm.

WriteOneByteNumber (90-111) and WriteTwoByteNumber (115-125) drive
TwoByteNumberToText. WriteBCDDigitInTextFormat (78-86) is a standalone BCD
digit primitive, portable even though its own callers
(WriteOneDigitBCDNumber, WriteTwoDigitBCDNumber, WriteFourDigitBCDNumber,
WriteBCDNumberInTextFormat) remain dead code per docs/port-contract.md:370-372
(zero external callsites in poketcg/src).
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
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}


def case(hl, **kw):
    return dict(POISON, hl=hl, d=DEST >> 8, e=DEST & 0xFF, wram={DEST: FILL}, **kw)


BCD_DST = 0xC110


def bcd_case(a, **kw):
    return dict(POISON, a=a, hl=BCD_DST, wram={BCD_DST: b"\xff"}, read={BCD_DST: 1}, **kw)


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
}
