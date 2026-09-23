"""Oracle-diff cases for poketcg/src/home/palettes.asm."""

WCONSOLE = 0xCAB4   # wConsole
WLCDC = 0xCABB      # wLCDC (WRAM mirror of rLCDC, not the hw register)
WBGP = 0xCABC       # wBGP
WOBP0 = 0xCABD      # wOBP0
WOBP1 = 0xCABE      # wOBP1
WFLAG = 0xCABF      # wFlushPaletteFlags
RBGP = 0xFF47       # rBGP  \
ROBP0 = 0xFF48      # rOBP0   > DMG grayscale palette registers
ROBP1 = 0xFF49      # rOBP1  /

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}


CONTRACT = {
    "FlushAllPalettes": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FlushPalette": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetBGP": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FlushPalette0": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FlushPalettes": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetOBP0": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetOBP1": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FlushPalettesIfRequested": {"compare": ("b", "c", "d", "e"), "preserve": ()},
    "CopyCGBPalettes": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "FlushAllCGBPalettes": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
}

CASES = {
    "FlushPalettesIfRequested": [
        {"read": {WFLAG: 1}},
        dict(POISON, wram={WFLAG: b"\x80", WCONSOLE: b"\x01",
                           WBGP: b"\x11", WOBP0: b"\x22", WOBP1: b"\x33"},
             read={WFLAG: 1}),
        {"wram": {WFLAG: b"\x80", WBGP: b"\x11", WOBP0: b"\x22", WOBP1: b"\x33"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
        # flags=0 takes the ret z path before any palette write, so the seeded
        # registers must come back untouched on both sides.
        {"wram": {WFLAG: b"\x00", RBGP: b"\xAA", ROBP0: b"\xBB", ROBP1: b"\xCC"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
        # console==CGB, flags bit6 clear: single-palette dispatch to
        # CopyCGBPalettes(flags, PAL_SIZE) (palettes.asm:73-78). Index 9 selects
        # the second OBP palette (wObjectPalettesCGB+8), palette-RAM offset 72.
        dict(POISON, wram={WFLAG: b"\x89", WCONSOLE: b"\x02",
                           WBGP: b"\x11", WOBP0: b"\x22", WOBP1: b"\x33",
                           **{0xCB38 + i: bytes([0x40 + i]) for i in range(8)}},
             read={WFLAG: 1},
             pread={72: 8}),
        # console==CGB, flags bit6 set: all-palette dispatch to
        # FlushAllCGBPalettes (palettes.asm:74-75), which must also clear
        # wFlushPaletteFlags on the FlushPalettesIfRequested.done fallthrough.
        dict(POISON, wram={WFLAG: b"\xC0", WCONSOLE: b"\x02",
                           WBGP: b"\x44", WOBP0: b"\x55", WOBP1: b"\x66",
                           0xCAF0: bytes((0x80 + i) & 0xFF for i in range(128))},
             read={WFLAG: 1},
             pread={0: 128}),
    ],
    "FlushPalettes": [
        {"a": 0x80, "wram": {WLCDC: b"\x00"}, "read": {WFLAG: 1}},
        dict(POISON, a=0xC0, wram={WLCDC: b"\x80"}, read={WFLAG: 1}),
        {"a": 0x80, "wram": {WLCDC: b"\x00", WBGP: b"\x44", WOBP0: b"\x55", WOBP1: b"\x66"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
    ],
    "FlushPalette0": [
        {"wram": {WLCDC: b"\x00"}, "read": {WFLAG: 1}},
        dict(POISON, wram={WLCDC: b"\x80"}, read={WFLAG: 1}),
        {"wram": {WLCDC: b"\x00", WBGP: b"\x12", WOBP0: b"\x34", WOBP1: b"\x56"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
    ],
    "FlushAllPalettes": [
        {"wram": {WLCDC: b"\x00"}, "read": {WFLAG: 1}},
        dict(POISON, a=0x37, wram={WLCDC: b"\x80"}, read={WFLAG: 1}),
        {"wram": {WLCDC: b"\x00", WBGP: b"\x01", WOBP0: b"\x02", WOBP1: b"\x03"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
    ],
    "FlushPalette": [
        {"a": 0x02, "wram": {WLCDC: b"\x00"}, "read": {WFLAG: 1}},
        dict(POISON, a=0x05, wram={WLCDC: b"\x80"}, read={WFLAG: 1}),
        {"a": 0x03, "wram": {WLCDC: b"\x00", WBGP: b"\xA1", WOBP0: b"\xB2", WOBP1: b"\xC3"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
    ],
    "SetBGP": [
        {"a": 0xE4, "wram": {WLCDC: b"\x00"}, "read": {WBGP: 1, WFLAG: 1}},
        dict(POISON, a=0x3C, wram={WLCDC: b"\x00"}, read={WBGP: 1, WFLAG: 1}),
        {"a": 0x1B, "wram": {WLCDC: b"\x00", WOBP0: b"\x99", WOBP1: b"\x88"},
         "read": {RBGP: 1, ROBP0: 1, ROBP1: 1}},
    ],
    "SetOBP0": [
        {"a": 0xF0, "wram": {WLCDC: b"\x00"}, "read": {WOBP0: 1, WFLAG: 1}},
        dict(POISON, a=0x0F, wram={WLCDC: b"\x00"}, read={WOBP0: 1, WFLAG: 1}),
        {"a": 0x7E, "wram": {WLCDC: b"\x00", WBGP: b"\x77", WOBP1: b"\x66"},
         "read": {ROBP0: 1, RBGP: 1, ROBP1: 1}},
    ],
    "SetOBP1": [
        {"a": 0xD0, "wram": {WLCDC: b"\x00"}, "read": {WOBP1: 1, WFLAG: 1}},
        dict(POISON, a=0x07, wram={WLCDC: b"\x00"}, read={WOBP1: 1, WFLAG: 1}),
        {"a": 0x5A, "wram": {WLCDC: b"\x00", WBGP: b"\x11", WOBP0: b"\x22"},
         "read": {ROBP1: 1, RBGP: 1, ROBP0: 1}},
    ],
    "CopyCGBPalettes": [
        {"pread": {0: 64}},
        {"a": 0, "b": 8,
         "wram": {0xCAF0 + i: bytes([0x11 + i]) for i in range(8)},
         "pread": {0: 8}},
        {"a": 8, "b": 8,
         "wram": {0xCB30 + i: bytes([0x21 + i]) for i in range(8)},
         "pread": {64: 8}},
        dict(POISON, pread={64: 64}),
    ],
    "FlushAllCGBPalettes": [
        {"wram": {WFLAG: b"\x80"}, "read": {WFLAG: 1}, "pread": {0: 128}},
        dict(POISON, wram={WFLAG: b"\xC0"}, read={WFLAG: 1}, pread={0: 128}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "FlushPalettes": {
        "source_symbol": "FlushPalettes",
        "before": "\tif (gb_read8(wLCDC_ADDR) & 0x80u)",
        "after": "\tif (!(gb_read8(wLCDC_ADDR) & 0x80u))",
        "case_ids": ["FlushPalettes-0", "FlushPalettes-1", "FlushPalettes-2"],
    },
}
for _rec in SCHEMA2_CASES["FlushPalettesIfRequested"]:
    _rec.setdefault("bus", {}).update({0xCABF: 1})
MUTATIONS["CopyCGBPalettes"] = {
    "source_symbol": "CopyCGBPalettes",
    "before": "\tuint8_t e = (uint8_t)(off & 0xBFu);",
    "after": "\tuint8_t e = (uint8_t)(off & 0xC0u);",
    "case_ids": ["CopyCGBPalettes-2"],
}
MUTATIONS["FlushAllCGBPalettes"] = {
    "source_symbol": "FlushAllCGBPalettes",
    "before": "\tCopyCGBPalettesResult r = CopyCGBPalettes(NUM_BACKGROUND_PALETTES, (uint8_t)(8u * PAL_SIZE));",
    "after": "\tCopyCGBPalettesResult r = CopyCGBPalettes(NUM_BACKGROUND_PALETTES, (uint8_t)(9u * PAL_SIZE));",
    "case_ids": ["FlushAllCGBPalettes-0"],
}
MUTATIONS["FlushAllPalettes"] = {
    "source_symbol": "FlushAllPalettes",
    "before": "\tFlushPalettes(FLUSH_ALL_PALS);",
    "after": "\t;",
    "case_ids": ["FlushAllPalettes-1"],
}
MUTATIONS["FlushPalette"] = {
    "source_symbol": "FlushPalette",
    "before": "\tFlushPalettes((uint8_t)(a | FLUSH_ONE_PAL));",
    "after": "\tFlushPalettes((uint8_t)(a & FLUSH_ONE_PAL));",
    "case_ids": ["FlushPalette-1"],
}
MUTATIONS["FlushPalette0"] = {
    "source_symbol": "FlushPalette0",
    "before": "\tFlushPalettes(FLUSH_ONE_PAL);",
    "after": "\t;",
    "case_ids": ["FlushPalette0-1"],
}
MUTATIONS["SetBGP"] = {
    "source_symbol": "SetBGP",
    "before": "\tgb_write8(wBGP_ADDR, a);",
    "after": "\tgb_write8(wBGP_ADDR, (uint8_t)(a ^ 1u));",
    "case_ids": ["SetBGP-0"],
}
MUTATIONS["SetOBP0"] = {
    "source_symbol": "SetOBP0",
    "before": "\tgb_write8(wOBP0_ADDR, a);",
    "after": "\tgb_write8(wOBP0_ADDR, (uint8_t)(a ^ 1u));",
    "case_ids": ["SetOBP0-0"],
}
MUTATIONS["SetOBP1"] = {
    "source_symbol": "SetOBP1",
    "before": "\tgb_write8(wOBP1_ADDR, a);",
    "after": "\tgb_write8(wOBP1_ADDR, (uint8_t)(a ^ 1u));",
    "case_ids": ["SetOBP1-0"],
}
for _rec in SCHEMA2_CASES["FlushPalettesIfRequested"]:
    _rec.setdefault("bus", {}).update({0xdff0: 1})
MUTATIONS["FlushPalettesIfRequested"] = {
    "source_symbol": "FlushPalettesIfRequested_Registers",
    "before": "\tuint8_t flags = gb_read8(wFlushPaletteFlags_ADDR);",
    "after": "\tgb_write8(0xdff0u, 0xFFu);\n\tuint8_t flags = gb_read8(wFlushPaletteFlags_ADDR);",
    "case_ids": ["FlushPalettesIfRequested-0"],
}
