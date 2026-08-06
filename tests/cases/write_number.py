"""Oracle-diff cases for poketcg/src/home/write_number.asm."""

DEST = 0xC300
FILL = b"\xff" * 7  # seven bytes: the seventh proves de stops after five digits

CONTRACT = {
    # bc is pushed/popped; de is the advanced write pointer. hl (0) and a (0) on
    # exit are residue no caller reads.
    "TwoByteNumberToText": ("b", "c", "d", "e"),
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}


def case(hl, **kw):
    return dict(POISON, hl=hl, d=DEST >> 8, e=DEST & 0xFF, wram={DEST: FILL}, **kw)


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
}
