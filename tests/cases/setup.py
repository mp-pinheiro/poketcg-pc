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

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}


CONTRACT = {
    "NoOp": {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
             "preserve": ("a", "f", "b", "c", "d", "e", "hl")},
    "DetectConsole": {"compare": (), "preserve": ()},
    "SetupPalettes": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "FillTileMap": {"compare": ("d", "e", "hl"), "preserve": ("d", "e")},
    "SetupVRAM": {"compare": ("d", "e", "hl"), "preserve": ("d", "e")},
    "SetupRegisters": {"compare": ("b", "c", "d", "e", "hl"),
                       "preserve": ("b", "c", "d", "e")},
    "ZeroRAM": {"compare": ("a", "b", "c", "d", "e", "hl"),
                "preserve": ("d", "e")},
}

CASES = {
    "NoOp": [
        {},
        dict(POISON),
    ],
    "DetectConsole": [
        # DMG: entry a is not BOOTUP_A_CGB. rWBK seeded and must survive untouched.
        {"a": 0x00, "wram": {RWBK: b"\xEE"},
         "read": {WCONSOLE: 1, RWBK: 1},
         "evidence": "intentional-transform",
         "reason": "Phase 1 drops DetectSGB and InitSGB from the native console probe."},
        dict(POISON, a=BOOTUP_A_DMG, wram={RWBK: b"\xEE"},
             read={WCONSOLE: 1, RWBK: 1},
             evidence="intentional-transform",
             reason="Phase 1 drops DetectSGB and InitSGB from the native console probe."),
        # CGB: entry a is BOOTUP_A_CGB. rWBK is written before the dropped
        # SwitchToCGBDoubleSpeed call; its hardware read-back masking (bits
        # 3-7 always 1) is not emulated by native GBRT, so omit from bus.
        dict(POISON, a=BOOTUP_A_CGB, wram={},
             read={WCONSOLE: 1}),
    ],
    "SetupPalettes": [
        {"wram": {WCONSOLE: bytes([CONSOLE_DMG])},
         "read": {WBGP: 1, WOBP0: 1, WOBP1: 1, WFLAG: 1, RBGP: 1, ROBP0: 1, ROBP1: 1}},
        dict(POISON, wram={WCONSOLE: bytes([CONSOLE_DMG])},
             read={WBGP: 1, WOBP0: 1, WOBP1: 1, WFLAG: 1, RBGP: 1, ROBP0: 1, ROBP1: 1}),
        {"wram": {WCONSOLE: bytes([CONSOLE_CGB])},
         "read": {
             WBGP: 1, WOBP0: 1, WOBP1: 1, WFLAG: 1,
             RBGP: 1, ROBP0: 1, ROBP1: 1,
             WBACKGROUND_PAL_CGB: 128,
         },
         "pread": {0: 128}},
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
             vread={0: {0x8000: 0xE00, 0x8E00: 0xE00}, 1: {0x8000: 0xE00, 0x8E00: 0xE00}},
             cycle_budget=600000),
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
                  0xFF80: b"\x11\x02", 0xFFED: b"\x33\x44"},
         "read": {0xC000: 2, 0xDFFE: 2, 0xFF80: 2, 0xFFED: 2}},
        dict(POISON, wram={0xC000: b"\xFF", 0xDFFF: b"\xFF",
                           0xFF80: b"\xFF", 0xFFEF: b"\xFF"},
             read={0xC000: 1, 0xDFFF: 1, 0xFF80: 1, 0xFFEF: 1}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for record in SCHEMA2_CASES["ZeroRAM"]:
    record["completion"] = {"mode": "pre-ret", "pc": 0x0403}

MUTATIONS = {
    "DetectConsole": {
        "source_symbol": "DetectConsole",
        "before": "a == BOOTUP_A_CGB",
        "after":  "a != BOOTUP_A_CGB",
        "case_ids": ["DetectConsole-2", "DetectConsole-0", "DetectConsole-1"],
    },
}
