"""Oracle-diff cases for poketcg/src/home/unsafe_bg_map.asm."""

SRC = 0xC100
VRAM = 0x9800

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "UnsafeWriteDataBlockToBGMap0": {"compare": ("d", "e", "hl"), "preserve": ()},
}


def addr(x, y):
    return VRAM + y * 32 + x


CASES = {
    "UnsafeWriteDataBlockToBGMap0": [
        {"hl": SRC, "wram": {SRC: bytes((0, 0))}, "read": {addr(0, 0): 1}},
        {"hl": SRC,
         "wram": {SRC: bytes((2, 3)), addr(2, 3): bytes((0x11, 0x22, 0))},
         "read": {addr(2, 3): 3}},
        dict(POISON, hl=SRC,
             wram={SRC: bytes((1, 1)), addr(1, 1): bytes((0x77, 0))},
             read={addr(1, 1): 2}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)


MUTATIONS = {
    "UnsafeWriteDataBlockToBGMap0": {
        "source_symbol": "UnsafeWriteDataBlockToBGMap0",
        "before": "if (a)",
        "after": "if (!a)",
        "case_ids": ["UnsafeWriteDataBlockToBGMap0-0",
                      "UnsafeWriteDataBlockToBGMap0-1",
                      "UnsafeWriteDataBlockToBGMap0-2"],
    },
}