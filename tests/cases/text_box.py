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
    "DrawRegularTextBox": ("b", "hl"),
    "DrawRegularTextBoxDMG": ("b", "hl"),
    "ContinueDrawingTextBoxDMGorSGB": ("b", "hl"),
    "DrawRegularTextBoxCGB": ("b", "hl"),
    "ContinueDrawingTextBoxCGB": ("b", "hl"),
    "CopyCurrentLineTilesAndAttrCGB": ("b", "hl"),
    "CopyCurrentLineAttrCGB": ("b", "hl"),
    "DrawLabeledTextBox": ("b", "hl"),
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
    # Dispatches on wConsole ($CAB4): CGB (2) takes the attribute-writing path, and
    # everything else falls through to DMG. wConsole == SGB (1) is deliberately NOT
    # covered -- the asm routes it to DrawRegularTextBoxSGB, which is dropped per #2,
    # so this port folds SGB into DMG and a case there would diverge by design.
    "DrawRegularTextBox": [
        {"b": 4, "c": 3, "d": 0, "e": 0, "hl": DST, "wram": {0xCAB4: b"\x00"},
         "read": {DST: 96}, "vread": {0: {DST: 96}, 1: {DST: 96}}},
        dict(POISON, b=4, c=3, d=0, e=0, hl=DST, wram={0xCAB4: b"\x02", 0xccf3: b"\x03"},
             read={DST: 96}, vread={0: {DST: 96}, 1: {DST: 96}}),
    ],
    "DrawRegularTextBoxDMG": [
        {"b": 4, "c": 3, "d": 0, "e": 0, "hl": DST, "read": {DST: 96}},
        dict(POISON, b=4, c=4, d=2, e=1, hl=DST, read={DST + 32: 128}),
    ],
    "ContinueDrawingTextBoxDMGorSGB": [
        {"b": 4, "c": 3, "hl": DST, "read": {DST: 64}},
        dict(POISON, b=4, c=4, hl=DST, read={DST: 96}),
    ],
    "DrawRegularTextBoxCGB": [
        {"b": 4, "c": 3, "d": 0, "e": 0, "hl": DST,
         "wram": {0xccf3: b"\x03"}, "read": {DST: 96}},
    ],
    # The body rows write TILES to VRAM bank 0 and ATTRIBUTES to bank 1, and the
    # routine restores bank 0 before returning -- so a plain `read` sees only the
    # tiles and the whole attribute path false-greens. `vread` indexes g_vram per
    # bank directly, which is the only way to observe what landed in bank 1.
    # The asm fills a body row's middle with 0 (`xor a`) and only its two borders
    # with wTextBoxFrameType, so a port that fills the middle with the frame type
    # differs on every interior column.
    "ContinueDrawingTextBoxCGB": [
        {"b": 4, "c": 3, "hl": DST, "wram": {0xccf3: b"\x03"},
         "read": {DST: 64}, "vread": {0: {DST: 64}, 1: {DST: 64}}},
        dict(POISON, b=6, c=4, hl=DST, wram={0xccf3: b"\x05"},
             read={DST: 96}, vread={0: {DST: 96}, 1: {DST: 96}}),
    ],
    "CopyCurrentLineTilesAndAttrCGB": [
        {"b": 4, "a": 0x1c, "d": 0x18, "e": 0x19, "hl": DST,
         "wram": {0xccf3: b"\x03"}, "read": {DST: 32}},
    ],
    "CopyCurrentLineAttrCGB": [
        {"b": 4, "hl": DST, "wram": {0xccf3: b"\x03"}, "read": {DST: 32}},
    ],

}

CASES.update({
    # The text engine keeps its generated tiles in a linked list across $C6-$C9;
    # Func_235e walks it and only terminates because index 0 holds a zero key.
    # SetupText is what establishes that, so it runs as a prelude -- without it the
    # walk finds next[0] == 0, treats node 0 as its own successor, and never returns.
    "DrawLabeledTextBox": [
        {"hl": 0, "b": 20, "c": 6, "d": 0, "e": 0,
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "wram": {0xCAB4: b"\x00", 0xCABB: b"\x00", 0xFF97: b"\x00"},
         "sram": {0: {0xA010: b"\x41\x42\x00"}},
         "read": {0x9800: 192, 0xFFAA: 2, 0xFFA9: 1, 0xFFB0: 1, 0xC000: 8}},
        dict(POISON, hl=0, b=20, c=6, d=0, e=0,
             setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
             wram={0xCAB4: b"\x02", 0xCCF3: b"\x03", 0xCABB: b"\x00", 0xFF97: b"\x00"},
             sram={0: {0xA010: b"\x41\x42\x00"}},
             read={0x9800: 192},
             vread={0: {0x9800: 192}, 1: {0x9800: 192}}),
    ],
})
