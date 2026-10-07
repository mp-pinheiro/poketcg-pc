"""Oracle-diff cases for poketcg/src/home/setup.asm."""
from tests.cases._symbols import HRAM_START, STACK_CANARY, WRAMX_START, sym

WCONSOLE = sym("wConsole")
WTILEMAPFILL = sym("wTileMapFill")
WCAB0, WCAB1, WCAB2 = sym("wcab0"), sym("wcab1"), sym("wcab2")
WREENTRANCYFLAG = sym("wReentrancyFlag")
WLCDC = sym("wLCDC")
WBGP, WOBP0, WOBP1 = sym("wBGP"), sym("wOBP0"), sym("wOBP1")
WFLAG = sym("wFlushPaletteFlags")
WLCDC_TRAMPOLINE = sym("wLCDCFunctionTrampoline")
WVBLANK_TRAMPOLINE = sym("wVBlankFunctionTrampoline")
WBACKGROUND_PAL_CGB = sym("wBackgroundPalettesCGB")

HSCX, HSCY, HWX, HWY = sym("hSCX"), sym("hSCY"), sym("hWX"), sym("hWY")
HBANKVRAM = sym("hBankVRAM")

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
        # $FE is the CGB readback shape (bank 6, upper bits set): the native
        # register model normalises every SVBK store (src/mem.c), PyBoy hands
        # back the raw byte, so only a normalised seed compares on both lanes.
        {"a": 0x00, "wram": {RWBK: b"\xFE"},
         "read": {WCONSOLE: 1, RWBK: 1},
         "evidence": "intentional-transform",
         "reason": "Phase 1 drops DetectSGB and InitSGB from the native console probe."},
        dict(POISON, a=BOOTUP_A_DMG, wram={RWBK: b"\xFE"},
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
        {"wram": {sym("wDeckToBuild"): b"\xAA\xBB", WRAMX_START + 0xFFE: b"\xCC\xDD",
                  sym("hBankROM"): b"\x11\x02", HRAM_START + 0x6D: b"\x33\x44"},
         "read": {sym("wDeckToBuild"): 2, WRAMX_START + 0xFFE: 2, sym("hBankROM"): 2, HRAM_START + 0x6D: 2}},
        dict(POISON, wram={sym("wDeckToBuild"): b"\xFF", WRAMX_START + 0xFFF: b"\xFF",
                           sym("hBankROM"): b"\xFF", HRAM_START + 0x6F: b"\xFF"},
             read={sym("wDeckToBuild"): 1, WRAMX_START + 0xFFF: 1, sym("hBankROM"): 1, HRAM_START + 0x6F: 1}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for record in SCHEMA2_CASES["ZeroRAM"]:
    record["completion"] = {"mode": "pre-ret", "pc": sym("ZeroRAM.zero_hram_loop") + 5}

MUTATIONS = {
    "DetectConsole": {
        "source_symbol": "DetectConsole",
        "before": "a == BOOTUP_A_CGB",
        "after":  "a != BOOTUP_A_CGB",
        "case_ids": ["DetectConsole-2", "DetectConsole-0", "DetectConsole-1"],
    },
}
MUTATIONS["FillTileMap"] = {
    "source_symbol": "FillTileMap",
    "before": "\t\treturn hl;",
    "after": "\t\treturn 1u + hl;",
    "case_ids": ["FillTileMap-0"],
}
MUTATIONS["SetupPalettes"] = {
    "source_symbol": "SetupPalettes",
    "before": "\tuint8_t a = 0xE4u; /* ldgbpal a, SHADE_WHITE, SHADE_LIGHT, SHADE_DARK, SHADE_BLACK */",
    "after": "\tuint8_t a = 0xE5u; /* ldgbpal a, SHADE_WHITE, SHADE_LIGHT, SHADE_DARK, SHADE_BLACK */",
    "case_ids": ["SetupPalettes-0"],
}
MUTATIONS["SetupRegisters"] = {
    "source_symbol": "SetupRegisters",
    "before": "\tgb_write8(wLCDCFunctionTrampoline_ADDR, 0xC3u);",
    "after": "\tgb_write8(wLCDCFunctionTrampoline_ADDR, 0xC4u);",
    "case_ids": ["SetupRegisters-0"],
}
MUTATIONS["SetupVRAM"] = {
    "source_symbol": "SetupVRAM",
    "before": "\tFillTileMap();",
    "after": "\t;",
    "case_ids": ["SetupVRAM-1"],
}
MUTATIONS["ZeroRAM"] = {
    "source_symbol": "ZeroRAM",
    "before": "\tuint16_t hl = 0xC000u;",
    "after": "\tuint16_t hl = 0xBFFFu;",
    "case_ids": ["ZeroRAM-0"],
}
for _rec in SCHEMA2_CASES["NoOp"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["NoOp"] = {
    "source_symbol": "NoOp",
    "before": "void NoOp(void)\n{",
    "after": "void NoOp(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["NoOp-1"],
}
