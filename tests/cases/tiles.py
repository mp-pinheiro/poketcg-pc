SRC = 0xC100
DST = 0x8000
MAP = 0x9800
PAT = bytes((i * 37 + 11) & 0xFF for i in range(1024))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "FillRectangle": ("d", "e"),
    "Copy1bppTiles": ("d", "e", "hl"),
}

CASES = {
    "FillRectangle": [
        {"oracle": False, "why": "256 by 256 writes exceed the oracle frame budget.",
         "expect": {MAP: b"\0"}},
        dict(POISON, a=0x12, b=1, c=1, d=3, e=2, hl=0x0201,
             read={MAP: 0x400}),
        {"a": 0x40, "b": 0, "c": 1, "d": 0, "e": 0, "hl": 0x0101,
         "oracle": False, "why": "256 columns exceed the oracle frame budget.",
         "expect": {MAP + 255: b"\x3f"}},
    ],
    "Copy1bppTiles": [
        {},
        dict(POISON, hl=DST, d=SRC >> 8, e=SRC & 0xff,
             wram={SRC: PAT}, read={DST: 2048}),
    ],
}
