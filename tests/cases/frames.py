from tests.cases._symbols import sym
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
        {"a": 0, "wram": {sym("hDPadRepeat"): b"\0\0\0\0\0"}, "read": {sym("hDPadRepeat"): 5}},
        dict(POISON, a=1, keys=[0x01, 0x00],
             wram={sym("hDPadRepeat"): b"\0\0\0\0\0"},
             read={sym("hDPadRepeat"): 5, sym("hKeysHeld"): 1, sym("hKeysPressed"): 1}),
    ],
    "DoFrame": [
        {"wram": {sym("hDPadRepeat"): b"\0\0\0\0\0"}, "read": {sym("hDPadRepeat"): 5}},
        dict(POISON, wram={sym("hDPadRepeat"): b"\0\0\0\0\0"}, read={sym("hDPadRepeat"): 5}),
        dict(POISON, wram={sym("wVBlankCounter"): b"\xff", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"},
             oracle=False,
             why="LCD-on DoFrame reaches the dissolved VBlank boundary",
             expect={sym("wVBlankCounter"): b"\x00"},
             expect_regs={"b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
        # lcd.asm:2-16: LCD off (wLCDC $CABB, rLCDC $FF40 bit 7 clear) makes
        # WaitForVBlank return at once with no ISR, so wVBlankCounter ($CAB8)
        # stands; the oracle runs this one, there is nothing to wait for.
        dict(POISON, wram={sym("wVBlankCounter"): b"\x2a", sym("wLCDC"): b"\x00", 0xFF40: b"\x00", sym("hDPadRepeat"): b"\0\0\0\0\0"},
             read={sym("wVBlankCounter"): 1, sym("hDPadRepeat"): 5}),
    ],
    # $FF8D..$FF91 = hDPadRepeat, hKeysReleased, hDPadHeld, hKeysHeld,
    # hKeysPressed. The last four rows walk a held direction through the
    # repeat schedule: new press (counter 24, d-pad reported), counting down
    # (d-pad masked to the newly pressed buttons -- the row the port used to
    # fail), expiry (counter 6, d-pad reported), and a button pressed during
    # the countdown (only that button reported).
    "HandleDPadRepeat": [
        {"wram": {sym("hDPadRepeat"): b"\0\0\0\0\0"}, "read": {sym("hDPadRepeat"): 5}},
        dict(POISON, wram={sym("hDPadRepeat"): b"\0\0\0\0\0"}, read={sym("hDPadRepeat"): 5}),
        {"wram": {sym("hDPadRepeat"): b"\xF0\x00\x00\x00\x01"}, "read": {sym("hDPadRepeat"): 5}},
        {"wram": {sym("hDPadRepeat"): b"\xF0\x00\x00\x00\x00"}, "read": {sym("hDPadRepeat"): 5}},
        {"wram": {sym("hDPadRepeat"): b"\x00\x00\x00\x40\x40"}, "read": {sym("hDPadRepeat"): 5}},
        {"wram": {sym("hDPadRepeat"): b"\x0A\x00\x00\x40\x00"}, "read": {sym("hDPadRepeat"): 5}},
        {"wram": {sym("hDPadRepeat"): b"\x01\x00\x00\x40\x00"}, "read": {sym("hDPadRepeat"): 5}},
        {"wram": {sym("hDPadRepeat"): b"\x05\x00\x00\x41\x01"}, "read": {sym("hDPadRepeat"): 5}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DoFrame": {"source_symbol": "DoFrame", "before": "\tif (!frame_boundary_is_installed() && (gb_read8(wLCDC_ADDR) & 0x80u) != 0u)", "after": "\tif (!frame_boundary_is_installed() && (gb_read8(wLCDC_ADDR) & 0x80u) == 0u)", "case_ids": ["DoFrame-3"]},
    "DoAFrames": {
        "source_symbol": "DoAFrames",
        "before": "uint16_t count = a ? a : 0x100u;",
        "after": "uint16_t count = a ? (uint16_t)(a + 1u) : 0x100u;",
        "case_ids": ["DoAFrames-1", "DoAFrames-0"],
    },
}
MUTATIONS["HandleDPadRepeat"] = {
    "source_symbol": "HandleDPadRepeat",
    "before": "\t\tif (repeat == 0) {",
    "after": "\t\tif (repeat != 0) {",
    "case_ids": ["HandleDPadRepeat-5"],
}
