SRC = 0xC100
HFFB0 = 0xFFB0

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "PrintLabels": ("b", "c", "d", "e", "hl"),
}
CASES = {
    "PrintLabels": [
        {"hl": SRC, "d": 0, "e": 0, "wram": {SRC: b"\x80", HFFB0: b"\x02"},
         "read": {SRC: 1, HFFB0: 1}},
        dict(POISON, hl=SRC, d=0, e=0, wram={SRC: b"\x80", HFFB0: b"\x02"},
             read={SRC: 1, HFFB0: 1}),
        {"hl": SRC, "d": 0x12, "e": 0x34,
         "oracle": False,
         "why": "text printing reaches banked text data outside the standalone label oracle contract",
         "wram": {SRC: b"\x01\x00\x00\x00\x80", HFFB0: b"\x02", 0xCABB: b"\x00"},
         "expect": {HFFB0: b"\x02", 0xFFAA: b"\x01\x98", 0xFFAD: b"\x01"},
         "expect_regs": {"b": 0, "c": 0, "d": 0x80, "e": 0, "hl": 0xC105}},
        dict(POISON, hl=SRC, d=0x12, e=0x34,
             oracle=False,
             why="text printing reaches banked text data outside the standalone label oracle contract",
             wram={SRC: b"\x01\x00\x00\x00\x80", HFFB0: b"\x02", 0xCABB: b"\x00"},
             expect={HFFB0: b"\x02", 0xFFAA: b"\x01\x98", 0xFFAD: b"\x01"},
             expect_regs={"b": 0xBB, "c": 0xCC, "d": 0x80, "e": 0, "hl": 0xC105}),
        {"hl": 0xFFFC, "d": 0x12, "e": 0x34,
         "oracle": False,
         "why": "the two-pass label scan wraps its list pointer from $FFFF to $0000, outside the oracle snapshot",
         "wram": {0xFFFC: b"\x01\x00\x00\x00", 0x0000: b"\x80", HFFB0: b"\x02", 0xCABB: b"\x00"},
         "expect": {HFFB0: b"\x02"},
         "read": {0xFFFC: 4, 0x0000: 1, HFFB0: 1, 0xCABB: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
