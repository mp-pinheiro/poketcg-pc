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
        dict(POISON, a=1, keys=[0x01, 0x00],
             wram={0xFF8D: b"\0\0\0\0\0"},
             read={0xFF8D: 5, 0xFF90: 1, 0xFF91: 1}),
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
    # $FF8D..$FF91 = hDPadRepeat, hKeysReleased, hDPadHeld, hKeysHeld,
    # hKeysPressed. The last four rows walk a held direction through the
    # repeat schedule: new press (counter 24, d-pad reported), counting down
    # (d-pad masked to the newly pressed buttons -- the row the port used to
    # fail), expiry (counter 6, d-pad reported), and a button pressed during
    # the countdown (only that button reported).
    "HandleDPadRepeat": [
        {"wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x01"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x00"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\x00\x00\x00\x40\x40"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\x0A\x00\x00\x40\x00"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\x01\x00\x00\x40\x00"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\x05\x00\x00\x41\x01"}, "read": {0xFF8D: 5}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DoAFrames": {
        "source_symbol": "DoAFrames",
        "before": "uint16_t count = a ? a : 0x100u;",
        "after": "uint16_t count = a ? (uint16_t)(a + 1u) : 0x100u;",
        "case_ids": ["DoAFrames-1", "DoAFrames-0"],
    },
}
