"""Oracle-diff cases for poketcg/src/home/objects.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOAM = 0xCA00
OAM_SIZE = 160
wOAMOffset = 0xCAB5

CONTRACT = {
    "SetOneObjectAttributes": ("b", "c", "d", "e", "hl"),
    "ZeroObjectPositions": ("b", "d", "e"),
}

OBJ = bytes((0x11, 0x22, 0x33, 0x44)) * 40

CASES = {
    "SetOneObjectAttributes": [
        {"e": 0x10, "d": 0x20, "c": 0x30, "b": 0x40, "wram": {wOAMOffset: b"\x00"}, "read": {wOAM: 4, wOAMOffset: 1}},
        dict(POISON, e=0x50, d=0x60, c=0x70, b=0x80, wram={wOAMOffset: b"\x08"}, read={wOAM + 8: 4, wOAMOffset: 1}),
        {"e": 0xA5, "d": 0x5A, "c": 0x01, "b": 0x02, "wram": {wOAMOffset: b"\x9C"}, "read": {wOAM + 0x9C: 4, wOAMOffset: 1}},
        {"wram": {wOAMOffset: bytes((OAM_SIZE,))}, "read": {wOAM: 4, wOAMOffset: 1}},
    ],
    "ZeroObjectPositions": [
        {"read": {wOAM: OAM_SIZE, wOAMOffset: 1}},
        dict(POISON, wram={wOAM: OBJ, wOAMOffset: b"\x28"}, read={wOAM: OAM_SIZE, wOAMOffset: 1}),
    ],
}
