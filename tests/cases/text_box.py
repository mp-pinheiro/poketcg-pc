"""Oracle-diff cases for poketcg/src/home/text_box.asm."""

SRC = 0xC100
DST = 0x9800
PAT = bytes((i * 29 + 3) & 0xFF for i in range(260))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SafeCopyDataDEtoHL": {"compare": ("a", "b", "d", "e", "hl"), "preserve": ("b",)},
    "DECoordToBGMap0Address": {"compare": ("d", "e", "hl"), "preserve": ("d", "e")},
    "AdjustCoordinatesForBGScroll": {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("a", "f", "b", "c")},
    "CopyLine": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "DrawRegularTextBox": {"compare": ("b", "hl"), "preserve": ("b",)},
    "DrawRegularTextBoxDMG": {"compare": ("b", "hl"), "preserve": ("b",)},
    "ContinueDrawingTextBoxDMGorSGB": {"compare": ("b", "hl"), "preserve": ("b",)},
    "DrawRegularTextBoxCGB": {"compare": ("b", "hl"), "preserve": ("b",)},
    "ContinueDrawingTextBoxCGB": {"compare": ("b", "hl"), "preserve": ("b",)},
    "CopyCurrentLineTilesAndAttrCGB": {"compare": ("b", "hl"), "preserve": ("b",)},
    "CopyCurrentLineAttrCGB": {"compare": ("b", "hl"), "preserve": ("b",)},
    "DrawLabeledTextBox": {"compare": ("b",), "preserve": ("b",)},
}

CASES = {
    "SafeCopyDataDEtoHL": [
        {"read": {DST: 1}},
        # deck-explore 105873: with the LCD on the copy runs through
        # HblankCopyDataDEtoHL, whose exit a is the STAT mode it waited for.
        {"c": 2, "d": SRC >> 8, "e": SRC & 0xff, "hl": DST,
         "wram": {SRC: PAT[:2], 0xCD3B: b"\x80"}, "read": {DST: 2}},
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
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SafeCopyDataDEtoHL": {
        "source_symbol": "SafeCopyDataDEtoHL",
        "before": "*de = source;",
        "after": "*de = (uint16_t)(source + 1u);",
        "case_ids": ["SafeCopyDataDEtoHL-0", "SafeCopyDataDEtoHL-2", "SafeCopyDataDEtoHL-3", "SafeCopyDataDEtoHL-4"],
    },
}
MUTATIONS["AdjustCoordinatesForBGScroll"] = {
    "source_symbol": "AdjustCoordinatesForBGScroll",
    "before": "\tuint8_t x = (uint8_t)((hSCX >> 3) & 0x1f);",
    "after": "\tuint8_t x = (uint8_t)((hSCX >> 3) | 0x1f);",
    "case_ids": ["AdjustCoordinatesForBGScroll-0"],
}
MUTATIONS["ContinueDrawingTextBoxCGB"] = {
    "source_symbol": "ContinueDrawingTextBoxCGB",
    "before": "\t\tgb_write8(0xff4f, 1);",
    "after": "\t\t;",
    "case_ids": ["ContinueDrawingTextBoxCGB-0"],
}
MUTATIONS["ContinueDrawingTextBoxDMGorSGB"] = {
    "source_symbol": "ContinueDrawingTextBoxDMGorSGB",
    "before": "\tdraw_line(hl, 0x1d, 0x1a, 0x1b, b);",
    "after": "\t;",
    "case_ids": ["ContinueDrawingTextBoxDMGorSGB-0"],
}
MUTATIONS["CopyCurrentLineAttrCGB"] = {
    "source_symbol": "CopyCurrentLineAttrCGB",
    "before": "\tCopyLine(hl, wTextBoxFrameType, b, wTextBoxFrameType, wTextBoxFrameType);",
    "after": "\t;",
    "case_ids": ["CopyCurrentLineAttrCGB-0"],
}
MUTATIONS["CopyCurrentLineTilesAndAttrCGB"] = {
    "source_symbol": "CopyCurrentLineTilesAndAttrCGB",
    "before": "\tCopyLine(hl, a, b, d, e);",
    "after": "\t;",
    "case_ids": ["CopyCurrentLineTilesAndAttrCGB-0"],
}
MUTATIONS["CopyLine"] = {
    "source_symbol": "CopyLine",
    "before": "\tuint8_t middle_raw = (uint8_t)(b - 2);",
    "after": "\tuint8_t middle_raw = (uint8_t)(b + 2);",
    "case_ids": ["CopyLine-0"],
}
MUTATIONS["DECoordToBGMap0Address"] = {
    "source_symbol": "DECoordToBGMap0Address",
    "before": "\treturn (uint16_t)(0x9800u + offset);",
    "after": "\treturn (uint16_t)(0x97FFu + offset);",
    "case_ids": ["DECoordToBGMap0Address-0"],
}
MUTATIONS["DrawLabeledTextBox"] = {
    "source_symbol": "DrawLabeledTextBox",
    "before": "\tif (wConsole == CONSOLE_CGB) {",
    "after": "\tif (wConsole != CONSOLE_CGB) {",
    "case_ids": ["DrawLabeledTextBox-1"],
}
MUTATIONS["DrawRegularTextBox"] = {
    "source_symbol": "DrawRegularTextBox",
    "before": "\t\tDrawRegularTextBoxCGB(hl, a, b, c, d, e);",
    "after": "\t\t;",
    "case_ids": ["DrawRegularTextBox-1"],
}
MUTATIONS["DrawRegularTextBoxCGB"] = {
    "source_symbol": "DrawRegularTextBoxCGB",
    "before": "\tCopyCurrentLineTilesAndAttrCGB(hl, 0x1c, b, 0x18, 0x19);",
    "after": "\t;",
    "case_ids": ["DrawRegularTextBoxCGB-0"],
}
MUTATIONS["DrawRegularTextBoxDMG"] = {
    "source_symbol": "DrawRegularTextBoxDMG",
    "before": "\tdraw_line(hl, 0x1c, 0x18, 0x19, b);",
    "after": "\t;",
    "case_ids": ["DrawRegularTextBoxDMG-0"],
}
