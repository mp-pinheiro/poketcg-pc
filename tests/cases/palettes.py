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

# rBGP/rOBP0/rOBP1 ($FF47-$FF49) are I/O registers: they sit in the g_io region
# ($FF00-$FF7F) that the oracle's snapshot (WRAM/HRAM/OAM/VRAM/SRAM only) does not
# capture, so the palette-register writes are verified against the C alone.
WHY_IO = ("rBGP/rOBP0/rOBP1 are I/O registers outside the oracle snapshot; "
          "the WRAM effects are covered by the oracle-run cases, the register "
          "writes by this C-only expect map")

# CopyCGBPalettes/FlushAllCGBPalettes feed CGB palette RAM through the
# auto-incrementing $FF68-$FF6B ports. The flat g_io model has no 64-byte
# indexed store behind those ports, so only the register tail each leaves is
# oracle:False-verified; register math derived by mirroring the asm's byte-exact
# loop (see palettes.asm:93-127, 80-89), never read off the oracle.
WHY_CGB_PAL = ("CGB palette RAM behind $FF68-$FF6B has no model in the flat g_io "
               "array (see BankedReadback's g_pal, unused by the bus); only the "
               "register tail is oracle:False-verified against the asm")


def _copy_cgb_palettes(a, b, wram=None):
    """Mirrors palettes.asm CopyCGBPalettes byte-for-byte (palettes.asm:93-127)."""
    wram = wram or {}
    off = (a * 8) & 0xFF
    hl = (0xCAF0 + off) & 0xFFFF   # wBackgroundPalettesCGB
    c = 0x6A if (off & 0x40) else 0x68
    e = off & 0xBF
    data = 0
    bb = b
    while True:
        c = (c + 1) & 0xFF
        data = wram.get(hl, 0) & 0xFF
        c = (c - 1) & 0xFF
        hl = (hl + 1) & 0xFFFF
        e = (e + 1) & 0xFF
        bb = (bb - 1) & 0xFF
        if bb == 0:
            break
    return {"a": data, "b": bb, "c": c, "d": 0, "e": e, "hl": hl}


def _flush_all_cgb_palettes(wram=None):
    _copy_cgb_palettes(0, 8 * 8, wram)
    r = _copy_cgb_palettes(8, 8 * 8, wram)
    return {"b": r["b"], "c": r["c"], "d": r["d"], "e": r["e"], "hl": r["hl"]}


CONTRACT = {
    "FlushAllPalettes": ("b", "c", "d", "e", "hl"),
    "FlushPalette": ("b", "c", "d", "e", "hl"),
    "SetBGP": ("b", "c", "d", "e", "hl"),
    "FlushPalette0": ("b", "c", "d", "e", "hl"),
    "FlushPalettes": ("b", "c", "d", "e", "hl"),
    "SetOBP0": ("b", "c", "d", "e", "hl"),
    "SetOBP1": ("b", "c", "d", "e", "hl"),
    "FlushPalettesIfRequested": ("b", "c", "d", "e"),
    "CopyCGBPalettes": ("a", "b", "c", "d", "e", "hl"),
    "FlushAllCGBPalettes": ("b", "c", "d", "e", "hl"),
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
        dict(oracle=False, why=WHY_CGB_PAL,
             expect_regs=_copy_cgb_palettes(0, 0)),
        dict(a=0, b=8, wram={0xCAF0 + i: bytes([0x11 + i]) for i in range(8)},
             oracle=False, why=WHY_CGB_PAL,
             expect_regs=_copy_cgb_palettes(0, 8, {0xCAF0 + i: 0x11 + i for i in range(8)})),
        dict(a=8, b=8, wram={0xCB30 + i: bytes([0x21 + i]) for i in range(8)},
             oracle=False, why=WHY_CGB_PAL,
             expect_regs=_copy_cgb_palettes(8, 8, {0xCB30 + i: 0x21 + i for i in range(8)})),
        dict(POISON, oracle=False, why=WHY_CGB_PAL,
             expect_regs=_copy_cgb_palettes(0xAA, 0xBB)),
    ],
    "FlushAllCGBPalettes": [
        dict(wram={WFLAG: b"\x80"}, oracle=False, why=WHY_CGB_PAL,
             expect={WFLAG: b"\x00"}, expect_regs=_flush_all_cgb_palettes()),
        dict(POISON, wram={WFLAG: b"\xC0"}, oracle=False, why=WHY_CGB_PAL,
             expect={WFLAG: b"\x00"}, expect_regs=_flush_all_cgb_palettes()),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
