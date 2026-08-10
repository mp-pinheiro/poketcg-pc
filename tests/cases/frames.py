POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DoAFrames": {"compare": ("b", "c", "d", "e", "hl"),
                  "preserve": ("b", "c", "d", "e", "hl")},
    "DoFrame": {"compare": ("b", "c", "d", "e", "hl"),
                "preserve": ("b", "c", "d", "e", "hl")},
    "HandleDPadRepeat": {"compare": ("b", "c", "d", "e", "hl"),
                         "preserve": ("b", "c", "d", "e")},
}

CASES = {
    "DoAFrames": [
        {"a": 0, "wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, a=1, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
    ],
    "DoFrame": [
        {"wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
        dict(POISON, wram={0xCAB8: b"\xff", 0xCABB: b"\x80", 0xFF40: b"\x80"},
             oracle=False,
             why="LCD-on DoFrame reaches the dissolved VBlank boundary",
             expect={0xCAB8: b"\x00"},
             expect_regs={"b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
    ],
    "HandleDPadRepeat": [
        {"wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x01"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x00"}, "read": {0xFF8D: 5}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DoAFrames": {
        "source_symbol": "DoAFrames",
        "before": "uint16_t count = a ? a : 0x100u;",
        "after": "uint16_t count = a ? a : 0x200u;",
        "case_ids": ["DoAFrames-0", "DoAFrames-1"],
    },
}
