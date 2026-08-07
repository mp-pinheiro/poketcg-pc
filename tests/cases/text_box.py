"""Oracle-diff cases for poketcg/src/home/text_box.asm."""

SRC = 0xC100
DST = 0x9800
PAT = bytes((i * 29 + 3) & 0xFF for i in range(260))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SafeCopyDataDEtoHL": ("b", "d", "e", "hl"),
    "DECoordToBGMap0Address": ("d", "e", "hl"),
    "AdjustCoordinatesForBGScroll": ("a", "f", "b", "c", "d", "e"),
    "CopyLine": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "SafeCopyDataDEtoHL": [
        {"read": {DST: 1}},
        dict(POISON, c=1, d=SRC >> 8, e=SRC & 0xff, hl=DST,
             wram={SRC: PAT[:1]}, read={DST: 1}),
        {"c": 0, "d": SRC >> 8, "e": SRC & 0xff, "hl": DST,
         "wram": {SRC: PAT[:256]}, "read": {DST: 256}},
        {"c": 1, "d": SRC >> 8, "e": SRC & 0xff, "hl": DST,
         "wram": {SRC: PAT[:257]}, "read": {DST: 1}},
    ],
    "DECoordToBGMap0Address": [
        {},
        dict(POISON, d=7, e=4),
        {"d": 0xff, "e": 0xff},
    ],
    "AdjustCoordinatesForBGScroll": [
        {},
        dict(POISON, d=7, e=9),
        {"d": 0xff, "e": 0xff},
    ],
    "CopyLine": [
        {"hl": DST, "b": 3, "d": 0x11, "e": 0x22, "a": 0x33,
         "read": {DST: 3}},
        dict(POISON, hl=DST, b=4, d=0x11, e=0x22, a=0x33,
             read={DST: 4}),
        {"hl": DST, "b": 0, "d": 0x11, "e": 0x22, "a": 0x33,
         "oracle": False, "why": "zero width runs the 8-bit post-test loop and corrupts the call stack",
         "expect": {DST: bytes([0x11] + [0x33] * 254 + [0x22])}},
    ],
}
