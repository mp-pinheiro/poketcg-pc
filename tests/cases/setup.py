"""Oracle-diff cases for poketcg/src/home/setup.asm."""

WCONSOLE = 0xCAB4
WTILEMAPFILL = 0xCAB6
WCAB0, WCAB1, WCAB2 = 0xCAB0, 0xCAB1, 0xCAB2
WREENTRANCYFLAG = 0xCABA
WLCDC = 0xCABB
WBGP, WOBP0, WOBP1 = 0xCABC, 0xCABD, 0xCABE
WFLAG = 0xCABF
WLCDC_TRAMPOLINE = 0xCACD
WVBLANK_TRAMPOLINE = 0xCAD0
WBACKGROUND_PAL_CGB = 0xCAF0
WOBJECT_PAL_CGB = 0xCB30

HSCX, HSCY, HWX, HWY = 0xFF92, 0xFF93, 0xFF94, 0xFF95
HBANKVRAM = 0xFF82

RBGP, ROBP0, ROBP1 = 0xFF47, 0xFF48, 0xFF49
RSCY, RSCX, RWY, RWX = 0xFF42, 0xFF43, 0xFF4A, 0xFF4B
RWBK = 0xFF70

CONSOLE_DMG = 0x00
CONSOLE_CGB = 0x02
BOOTUP_A_CGB = 0x11
BOOTUP_A_DMG = 0x01

NOOP_ADDR = 0x0348          # poketcg.sym: bank 0, fixed for this disassembly
INITIAL_PALETTE = bytes.fromhex("9c63b5424a210000")  # poketcg.gbc @ $0399, 8 bytes

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

WHY_ZERO_RAM = ("zeroes $C000-$DFFF (including the oracle's own $CF00-$CFFF call "
                 "frame and stack) and $FF80-$FFEF, so it destroys the very frame "
                 "running it and cannot execute on the PyBoy oracle at all")
WHY_CGB_PAL = ("chains through FlushAllCGBPalettes/CopyCGBPalettes, which are "
               "oracle:False themselves (CGB palette RAM behind $FF68-$FF6B has "
               "no model in the flat g_io array)")

CONTRACT = {
    "NoOp": ("a", "f", "b", "c", "d", "e", "hl"),
    # Exit a/b/c/d/e/hl are NOT part of the contract: on real hardware the DMG
    # branch always calls DetectSGB and the CGB branch always calls
    # SwitchToCGBDoubleSpeed, and both are dropped/deleted per the exclusion
    # taxonomy -- their real clobbering of hl (DMG) and a/b/hl (CGB) shows up on
    # the oracle but is not something this port reproduces or owes a caller.
    # wConsole and rWBK, written before either dropped call, are the real contract.
    "DetectConsole": (),
    "SetupPalettes": ("b", "c", "d", "e", "hl"),
    "FillTileMap": ("d", "e", "hl"),
    "SetupVRAM": ("d", "e", "hl"),
    "SetupRegisters": ("b", "c", "d", "e", "hl"),
    "ZeroRAM": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "NoOp": [
        {},
        dict(POISON),
    ],
    "DetectConsole": [
        # DMG: entry a is not BOOTUP_A_CGB. rWBK seeded and must survive untouched.
        {"a": 0x00, "wram": {RWBK: b"\xEE"},
         "read": {WCONSOLE: 1, RWBK: 1}},
        dict(POISON, a=BOOTUP_A_DMG, wram={RWBK: b"\xEE"},
             read={WCONSOLE: 1, RWBK: 1}),
        # CGB: entry a is BOOTUP_A_CGB. rWBK is written before the dropped
        # SwitchToCGBDoubleSpeed call, so it is still reliably testable.
        dict(POISON, a=BOOTUP_A_CGB, wram={RWBK: b"\xEE"},
             read={WCONSOLE: 1, RWBK: 1}),
    ],
    "SetupPalettes": [
        {"wram": {WCONSOLE: bytes([CONSOLE_DMG])},
         "read": {WBGP: 1, WOBP0: 1, WOBP1: 1, WFLAG: 1, RBGP: 1, ROBP0: 1, ROBP1: 1}},
        dict(POISON, wram={WCONSOLE: bytes([CONSOLE_DMG])},
             read={WBGP: 1, WOBP0: 1, WOBP1: 1, WFLAG: 1, RBGP: 1, ROBP0: 1, ROBP1: 1}),
        # CGB: chains into FlushAllCGBPalettes, so this branch is oracle:False too.
        {"wram": {WCONSOLE: bytes([CONSOLE_CGB])},
         "oracle": False, "why": WHY_CGB_PAL,
         "expect": {
             WBGP: b"\xE4", WOBP0: b"\xE4", WOBP1: b"\xE4", WFLAG: b"\x00",
             RBGP: b"\xE4", ROBP0: b"\xE4", ROBP1: b"\xE4",
             WBACKGROUND_PAL_CGB: INITIAL_PALETTE,
             WBACKGROUND_PAL_CGB + 15 * 8: INITIAL_PALETTE,  # last of the 16 palettes
         },
         "expect_regs": {"b": 0x00, "c": 0x6A, "d": 0x00, "e": 0x40, "hl": 0xCB70}},
    ],
    "FillTileMap": [
        {"wram": {WCONSOLE: bytes([CONSOLE_DMG])},
         "read": {HBANKVRAM: 1}, "vread": {0: {0x9800: 0x400}}},
        dict(POISON, wram={WCONSOLE: bytes([CONSOLE_CGB]), WTILEMAPFILL: b"\xAB"},
             read={HBANKVRAM: 1}, vread={0: {0x9800: 0x400}, 1: {0x9800: 0x400}}),
    ],
    "SetupVRAM": [
        {"wram": {WCONSOLE: bytes([CONSOLE_DMG])},
         "read": {HBANKVRAM: 1},
         "vread": {0: {0x8000: 0xE00, 0x8E00: 0xE00}}},
        dict(POISON, wram={WCONSOLE: bytes([CONSOLE_CGB]), WTILEMAPFILL: b"\xAB"},
             read={HBANKVRAM: 1},
             vread={0: {0x8000: 0xE00, 0x8E00: 0xE00}, 1: {0x8000: 0xE00, 0x8E00: 0xE00}}),
    ],
    "SetupRegisters": [
        {"read": {
            RSCY: 1, RSCX: 1, RWY: 1, RWX: 1,
            WCAB0: 1, WCAB1: 1, WCAB2: 1,
            HSCX: 1, HSCY: 1, HWX: 1, HWY: 1,
            WREENTRANCYFLAG: 1, WLCDC_TRAMPOLINE: 1, WVBLANK_TRAMPOLINE: 3, WLCDC: 1,
        }},
        dict(POISON, read={
            RSCY: 1, RSCX: 1, RWY: 1, RWX: 1,
            WCAB0: 1, WCAB1: 1, WCAB2: 1,
            HSCX: 1, HSCY: 1, HWX: 1, HWY: 1,
            WREENTRANCYFLAG: 1, WLCDC_TRAMPOLINE: 1, WVBLANK_TRAMPOLINE: 3, WLCDC: 1,
        }),
    ],
    "ZeroRAM": [
        {"wram": {0xC000: b"\xAA\xBB", 0xDFFE: b"\xCC\xDD",
                  0xFF80: b"\x11\x22", 0xFFED: b"\x33\x44"},
         "oracle": False, "why": WHY_ZERO_RAM,
         "expect": {0xC000: b"\x00\x00", 0xDFFE: b"\x00\x00",
                    0xFF80: b"\x00\x00", 0xFFED: b"\x00\x00"},
         "expect_regs": {"a": 0x00, "b": 0x00, "c": 0xF0, "d": 0x00, "e": 0x00, "hl": 0xE000}},
        dict(POISON, wram={0xC000: b"\xFF", 0xDFFF: b"\xFF", 0xFF80: b"\xFF", 0xFFEF: b"\xFF"},
             oracle=False, why=WHY_ZERO_RAM,
             expect={0xC000: b"\x00", 0xDFFF: b"\x00", 0xFF80: b"\x00", 0xFFEF: b"\x00"},
             expect_regs={"a": 0x00, "b": 0x00, "c": 0xF0, "d": 0xDD, "e": 0xEE, "hl": 0xE000}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
