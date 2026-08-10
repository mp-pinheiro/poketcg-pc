"""Oracle-diff cases for poketcg/src/home/objects.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOAM = 0xCA00
OAM_SIZE = 160
wOAMOffset = 0xCAB5

CONTRACT = {
    "SetOneObjectAttributes": ("b", "c", "d", "e", "hl"),
    "ZeroObjectPositions": ("b", "d", "e"),
    "SetManyObjectsAttributes": ("f", "d", "e", "hl"),
}

OBJ = bytes((0x11, 0x22, 0x33, 0x44)) * 40
SPRITE = bytes((0x11, 0x22, 0x33, 0x44))
SRC40 = bytes((0,)) + SPRITE * 40  # count 0 means 256; only 40 fit before OAM fills
SRC1 = bytes((1,)) + SPRITE
SRC = 0xC100

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
    "SetManyObjectsAttributes": [
        # All-zero registers: hl=0 reads real ROM bytes at $0000, off defaults 0.
        # OAM fills at 40 sprites regardless of how large that count byte is.
        {"read": {wOAM: OAM_SIZE, wOAMOffset: 1}},
        # n==0 means 256: off=0 still bails exactly at 40 sprites (160 bytes).
        {"hl": SRC, "d": 0x20, "e": 0x10, "wram": {SRC: SRC40, wOAMOffset: b"\x00"},
         "read": {wOAM: OAM_SIZE, wOAMOffset: 1}},
        {"hl": SRC, "wram": {SRC: SRC1, wOAMOffset: b"\x00"},
         "read": {wOAM: 4, wOAMOffset: 1}},
        dict(POISON, hl=SRC, d=0x05, e=0x03,
             wram={SRC: bytes((2,)) + SPRITE * 2, wOAMOffset: b"\x08"},
             read={wOAM + 8: 8, wOAMOffset: 1}),
        # Exact boundary: one sprite lands right at OAM_SIZE (carry, Z set).
        {"hl": SRC, "wram": {SRC: SRC1, wOAMOffset: bytes((OAM_SIZE - 4,))},
         "read": {wOAM + OAM_SIZE - 4: 4, wOAMOffset: 1}},
        # Off-by-one past OAM_SIZE (carry, Z clear).
        {"hl": SRC, "wram": {SRC: SRC1, wOAMOffset: bytes((OAM_SIZE - 3,))},
         "read": {wOAM + OAM_SIZE - 3: 4, wOAMOffset: 1}},
        # Initial reject, offset exactly OAM_SIZE.
        {"hl": SRC, "wram": {wOAMOffset: bytes((OAM_SIZE,))}, "read": {wOAMOffset: 1}},
        # Initial reject, offset past OAM_SIZE.
        {"hl": SRC, "wram": {wOAMOffset: b"\xC8"}, "read": {wOAMOffset: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
