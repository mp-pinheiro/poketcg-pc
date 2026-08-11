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
