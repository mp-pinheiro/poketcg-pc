"""Oracle-diff cases for poketcg/src/home/bg_map.asm."""

SRC = 0xC100
DST = 0xC500
VRAM = 0x9800
PAT = bytes((i * 13 + 5) & 0xFF for i in range(520))

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "WriteDataBlocksToBGMap0": ("a", "b", "c", "d", "e", "hl"),
    "WriteDataBlockToBGMap0": ("a", "b", "c", "d", "e", "hl"),
    "WriteByteToBGMap0": ("a", "b", "c", "d", "e", "hl"),
    "HblankWriteByteToBGMap0": ("a", "b", "c", "d", "e", "hl"),
    "CopyDataToBGMap0": ("d", "e", "hl"),
    "SafeCopyDataHLtoDE": ("c", "d", "e", "hl"),
    "JPHblankCopyDataHLtoDE": ("c", "d", "e", "hl"),
}

BLOCK = bytes((2, 3, 0x11, 0x22, 0))
BLOCKS = bytes((1, 1, 7, 0, 4, 2, 8, 9, 0, 0xFF))

CASES = {
    "WriteDataBlocksToBGMap0": [
        {"hl": SRC, "wram": {SRC: bytes((0, 0, 0, 0xFF))}, "read": {VRAM: 1}},
        dict(POISON, hl=SRC, wram={SRC: BLOCKS}, read={VRAM + 32 + 1: 1, VRAM + 64 + 4: 2}),
    ],
    "WriteDataBlockToBGMap0": [
        {"hl": SRC, "wram": {SRC: bytes((0, 0, 0))}, "read": {VRAM: 1}},
        dict(POISON, hl=SRC, wram={SRC: BLOCK}, read={VRAM + 98: 2}),
        {"hl": SRC, "wram": {SRC: bytes((0, 0)) + PAT[:256] + b"\0"}, "read": {VRAM: 256}},
        {"hl": SRC, "wram": {SRC: bytes((0, 0)) + PAT[:257] + b"\0"}, "read": {VRAM: 256}},
    ],
    "WriteByteToBGMap0": [
        {"read": {VRAM: 1}},
        dict(POISON, a=0x5A, b=7, c=4, read={VRAM + 135: 1}),
    ],
    "HblankWriteByteToBGMap0": [
        {"read": {VRAM: 1}},
        dict(POISON, a=0xA5, b=9, c=6, read={VRAM + 201: 1}),
    ],
    "CopyDataToBGMap0": [
        {"a": 1, "hl": SRC, "wram": {SRC: b"\x42"}, "read": {VRAM: 1}},
        {"a": 0, "b": 1, "c": 2, "hl": SRC, "wram": {SRC: PAT[:256]}, "read": {VRAM + 65: 256}},
        {"a": 1, "b": 2, "c": 3, "hl": SRC, "wram": {SRC: PAT[:257]}, "read": {VRAM + 98: 1}},
    ],
    "SafeCopyDataHLtoDE": [
        {"b": 1, "hl": SRC, "d": 0x98, "e": 0, "wram": {SRC: b"\x42"}, "read": {VRAM: 1}},
        {"b": 0, "hl": SRC, "d": 0x98, "e": 0, "wram": {SRC: PAT[:256]}, "read": {VRAM: 256}},
        {"b": 1, "hl": SRC, "d": 0x98, "e": 0, "wram": {SRC: PAT[:257]}, "read": {VRAM: 1}},
    ],
    "JPHblankCopyDataHLtoDE": [
        {"b": 1, "hl": SRC, "d": 0x98, "e": 0, "wram": {SRC: b"\x42"}, "read": {VRAM: 1}},
        {"b": 0, "hl": SRC, "d": 0x98, "e": 0, "wram": {SRC: PAT[:256]}, "read": {VRAM: 256}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
