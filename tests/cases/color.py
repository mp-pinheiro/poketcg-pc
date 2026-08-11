BGP = 0xCABC
OBP0 = 0xCABD
OBP1 = 0xCABE
LCDC = 0xCABB
CONSOLE = 0xCAB4
PALETTE = 0xD293
RLCDC = 0xFF40
TEMP_BGP = 0xD294
TEMP_OBP0 = 0xD295
TEMP_OBP1 = 0xD296
BG_PALS = 0xCAF0
OBJ_PALS = 0xCB30
TEMP_BG_PALS = 0xD297
TEMP_OBJ_PALS = 0xD2D7
VBLANK = 0xCAB8
WD317 = 0xD317

CONTRACT = {
    "LoadConsolePaletteData": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FadeScreenToWhite": {"compare": (), "preserve": ()},
    "FadeScreenFromWhite.BackupPalsAndSetWhite": {"compare": (), "preserve": ()},
    "SetWhitePalettes": {"compare": (), "preserve": ()},
    "Func_10d17": {"compare": (), "preserve": ()},
    "Func_10d50": {"compare": (), "preserve": ()},
    "FadeScreenFromWhite": {"compare": ("a",), "preserve": ()},
    "FadeScreenToTempPals": {"compare": ("a",), "preserve": ()},
    "RestoreFirstColorInOBPals": {"compare": ("b",), "preserve": ("b",)},
    "FadeDMGPalettes": {"compare": ("b", "c"), "preserve": ("b", "c")},
    "FadeDMGPalettes.CalculateMixPalette": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "FadeDMGPalettes.GetMixShadeValue": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FadeOBPalIntoTemp": {"compare": ("b", "c"), "preserve": ("b", "c")},
    "FadeBGPalIntoTemp1": {"compare": ("b", "c"), "preserve": ("b", "c")},
    "FadeBGPalIntoTemp2": {"compare": ("b", "c"), "preserve": ("b", "c")},
    "FadeBGPalIntoTemp3": {"compare": ("b", "c"), "preserve": ("b", "c")},
    "FadePalIntoAnother.GetFadedColor": {"compare": ("a", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "FadePalIntoAnother.FadeColor": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FlashScreenToWhite": {"compare": ("f",), "preserve": ()},
    "CopyPalsToSRAMBuffer": {"compare": ("f",), "preserve": ()},
    "LoadPalsFromSRAMBuffer": {"compare": ("f",), "preserve": ()},
    "Func_10d74": {"compare": ("b",), "preserve": ("b",)},
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
PALETTE_SEED = {
    BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4",
    BG_PALS: bytes(range(64)), OBJ_PALS: bytes(range(64, 128)),
    TEMP_BGP: b"\x00", TEMP_OBP0: b"\x55", TEMP_OBP1: b"\xAA",
    TEMP_BG_PALS: bytes(reversed(range(64))), TEMP_OBJ_PALS: bytes(reversed(range(64, 128))),
}
PALETTE_EXPECT = {
    BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4",
    BG_PALS: bytes(range(64)), OBJ_PALS: bytes(range(64, 128)),
    TEMP_BGP: b"\x00", TEMP_OBP0: b"\x55", TEMP_OBP1: b"\xAA",
    TEMP_BG_PALS: bytes(reversed(range(64))), TEMP_OBJ_PALS: bytes(reversed(range(64, 128))),
}
SRAM_PALETTE = bytes([0xE4, 0x1B, 0xB4]) + bytes(range(128))
MIX_CASES = [
    {"b": 0, "c": 0}, {"b": 0, "c": 1}, {"b": 0, "c": 2}, {"b": 0, "c": 3},
    {"b": 1, "c": 0}, {"b": 1, "c": 1}, {"b": 1, "c": 2}, {"b": 1, "c": 3},
    {"b": 2, "c": 0}, {"b": 2, "c": 1}, {"b": 2, "c": 2}, {"b": 2, "c": 3},
    {"b": 3, "c": 0}, {"b": 3, "c": 1}, {"b": 3, "c": 2}, {"b": 3, "c": 3},
]

CASES = {
    "LoadConsolePaletteData": [
        {"wram": {CONSOLE: b"\x00"}, "read": {CONSOLE: 1, PALETTE: 1, WD317: 1}},
        dict(POISON, wram={CONSOLE: b"\x01"}, read={CONSOLE: 1, PALETTE: 1, WD317: 1}),
    ],
    "FadeScreenToWhite": [
        {"wram": {LCDC: b"\x00", CONSOLE: b"\x02", **PALETTE_SEED}, "read": {BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64}},
        dict(POISON, wram={LCDC: b"\x00", CONSOLE: b"\x1F", **PALETTE_SEED}, read={BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64}),
    ],
    "FadeScreenFromWhite.BackupPalsAndSetWhite": [
        {"wram": PALETTE_SEED, "read": {TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1, TEMP_BG_PALS: 128, BGP: 1}},
        dict(POISON, wram=PALETTE_SEED, read={TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1, TEMP_BG_PALS: 128, BGP: 1}),
    ],
    "SetWhitePalettes": [
        {"wram": {PALETTE: b"\x00", **PALETTE_SEED}, "read": {BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64}},
        dict(POISON, wram={PALETTE: b"\x1F", **PALETTE_SEED}, read={BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64}),
    ],
    "Func_10d17": [
        {"wram": {CONSOLE: b"\x03", **PALETTE_SEED}, "read": {TEMP_BGP: 1, TEMP_BG_PALS: 128, BGP: 1, WD317: 1}},
        dict(POISON, wram={CONSOLE: b"\x1C", **PALETTE_SEED}, read={TEMP_BGP: 1, TEMP_BG_PALS: 128, BGP: 1, WD317: 1}),
    ],
    "Func_10d50": [
        {"wram": {CONSOLE: b"\x03", **PALETTE_SEED}, "read": {TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1, TEMP_BG_PALS: 128, WD317: 1}},
        dict(POISON, wram={CONSOLE: b"\x1C", **PALETTE_SEED}, read={TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1, TEMP_BG_PALS: 128, WD317: 1}),
    ],
    "FadeScreenFromWhite": [
        {"wram": {LCDC: b"\x00", VBLANK: b"\xFE"},
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "read": {LCDC: 1, RLCDC: 1, VBLANK: 1, BGP: 1, OBP0: 1, OBP1: 1,
                  BG_PALS: 64, OBJ_PALS: 64, TEMP_BGP: 1, TEMP_OBP0: 1,
                  TEMP_OBP1: 1, TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}},
        dict(POISON, wram={LCDC: b"\x00", VBLANK: b"\xFE"},
             instruction_budget=1000000, cycle_budget=4000000,
             read={LCDC: 1, RLCDC: 1, VBLANK: 1, BGP: 1, OBP0: 1, OBP1: 1,
                   BG_PALS: 64, OBJ_PALS: 64, TEMP_BGP: 1, TEMP_OBP0: 1,
                   TEMP_OBP1: 1, TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}),
    ],
    "FadeScreenToTempPals": [
        {"wram": {LCDC: b"\x00", **PALETTE_SEED},
         "read": {BGP: 3, BG_PALS: 64, OBJ_PALS: 64}},
        dict(POISON, wram={LCDC: b"\x00", **PALETTE_SEED},
             read={BGP: 3, BG_PALS: 64, OBJ_PALS: 64}),
        {"wram": {LCDC: b"\x80", RLCDC: b"\x80", VBLANK: b"\xFE", **PALETTE_SEED,
                  BG_PALS: bytes([0x42] * 64), TEMP_BG_PALS: bytes([0x42] * 64),
                  OBJ_PALS: bytes([0x18] * 64), TEMP_OBJ_PALS: bytes([0x18] * 64)},
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "read": {VBLANK: 1, LCDC: 1, RLCDC: 1, BG_PALS: 64,
                  TEMP_BG_PALS: 64, OBJ_PALS: 64, TEMP_OBJ_PALS: 64}},
    ],
    "RestoreFirstColorInOBPals": [
        {"wram": {OBJ_PALS: bytes([0x10, 0x11, 0x20, 0x21, 0x30, 0x31, 0x40, 0x41] * 8), TEMP_OBJ_PALS: bytes(range(128))}, "read": {OBJ_PALS: 16}},
        dict(POISON, wram={OBJ_PALS: bytes([0x10, 0x11] * 32), TEMP_OBJ_PALS: bytes(reversed(range(128)))}, read={OBJ_PALS: 16}),
    ],
    "FadeDMGPalettes": [
        {"wram": {BGP: b"\x00", OBP0: b"\x55", OBP1: b"\xAA", TEMP_BGP: b"\xFF", TEMP_OBP0: b"\x00", TEMP_OBP1: b"\x55"}, "read": {BGP: 3}},
        dict(POISON, wram={BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4", TEMP_BGP: b"\x1B", TEMP_OBP0: b"\xB4", TEMP_OBP1: b"\xE4"}, read={BGP: 3}),
    ],
    "FadeDMGPalettes.CalculateMixPalette": [
        {"b": 0, "c": 0}, {"b": 0xFF, "c": 0xFF}, {"b": 0xE4, "c": 0x1B},
        dict(POISON, b=0xE4, c=0x1B),
    ],
    "FadeDMGPalettes.GetMixShadeValue": MIX_CASES + [dict(POISON, b=0x03, c=0x03)],
    "FadeOBPalIntoTemp": [
        {"wram": {OBJ_PALS: bytes(range(64, 128)), TEMP_OBJ_PALS: bytes(reversed(range(64, 128)))}, "read": {OBJ_PALS: 64, TEMP_OBJ_PALS: 64}},
        dict(POISON, wram={OBJ_PALS: bytes(reversed(range(64, 128))), TEMP_OBJ_PALS: bytes(range(64, 128))}, read={OBJ_PALS: 64, TEMP_OBJ_PALS: 64}),
    ],
    "FadeBGPalIntoTemp1": [
        {"wram": PALETTE_SEED, "read": {BG_PALS: 32, TEMP_BG_PALS: 32}},
        dict(POISON, wram=PALETTE_SEED, read={BG_PALS: 32, TEMP_BG_PALS: 32}),
    ],
    "FadeBGPalIntoTemp2": [
        {"wram": PALETTE_SEED, "read": {BG_PALS: 64, TEMP_BG_PALS: 64}},
        dict(POISON, wram=PALETTE_SEED, read={BG_PALS: 64, TEMP_BG_PALS: 64}),
    ],
    "FadeBGPalIntoTemp3": [
        {"wram": PALETTE_SEED, "read": {BG_PALS: 64, TEMP_BG_PALS: 64}},
        dict(POISON, wram=PALETTE_SEED, read={BG_PALS: 64, TEMP_BG_PALS: 64}),
    ],
    "FadePalIntoAnother.GetFadedColor": [
        {"b": 0, "c": 0, "d": 0, "e": 0}, dict(POISON, b=0, c=0, d=0, e=0),
        {"b": 0x7C, "c": 0x1F, "d": 0x7C, "e": 0x1F},
        {"b": 0, "c": 0, "d": 0x7C, "e": 0xFF},
        {"b": 0x04, "c": 0x21, "d": 0x08, "e": 0xA5},
    ],
    "FadePalIntoAnother.FadeColor": [
        {"a": 0, "hl": 0}, {"a": 31, "hl": 0}, {"a": 0, "hl": 31},
        {"a": 1, "hl": 5}, {"a": 4, "hl": 0}, {"a": 0, "hl": 4},
        {"a": 31, "hl": 27}, dict(POISON, a=0, hl=31),
    ],
    "FlashScreenToWhite": [
        {"c": 1, "wram": {LCDC: b"\x00", **PALETTE_SEED}, "ramg": False, "read": {LCDC: 1, BG_PALS: 64}},
        dict(POISON, c=1, wram={LCDC: b"\x00", **PALETTE_SEED}, ramg=False, read={LCDC: 1, BG_PALS: 64}),
        {"c": 0, "wram": {LCDC: b"\x00", RLCDC: b"\x00", VBLANK: b"\xFE", **PALETTE_SEED},
         "ramg": False, "oracle": False, "why": "Fade-in reaches dissolved VBlank context",
         "expect": {LCDC: b"\x80", RLCDC: b"\x80", VBLANK: b"\x06",
                    BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4",
                    BG_PALS: bytes(range(64)), OBJ_PALS: bytes(range(64, 128)),
                    TEMP_BGP: b"\xE4", TEMP_OBP0: b"\x1B", TEMP_OBP1: b"\xB4",
                    TEMP_BG_PALS: bytes(range(64)), TEMP_OBJ_PALS: bytes(range(64, 128)),
                    0xA000: b"\xFF"},
         "read": {LCDC: 1, RLCDC: 1, VBLANK: 1, BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64,
                  TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1, TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64, 0xA000: 1}},
    ],
    "CopyPalsToSRAMBuffer": [
        {"wram": {0xFF81: b"\x03", **PALETTE_SEED}, "ramg": False,
         "sram": {1: {0xA800: bytes(131)}}, "oracle": False,
         "why": "The 131-byte bank-1 palette save is outside ordinary oracle readback",
         "expect": {0xFF81: b"\x03", 0xA000: b"\xFF"},
         "expect_sram": {1: {0xA800: SRAM_PALETTE}},
         "read": {0xFF81: 1}},
        dict(POISON, wram={0xFF81: b"\x03", **PALETTE_SEED}, ramg=False,
             sram={1: {0xA800: bytes(131)}}, read={0xFF81: 1}),
    ],
    "LoadPalsFromSRAMBuffer": [
        {"wram": {0xFF81: b"\x03", **PALETTE_SEED}, "ramg": False,
         "sram": {1: {0xA800: SRAM_PALETTE}},
         "expect": {BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4"},
         "sread": {1: {0xA000: 1}},
         "read": {BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 128, 0xFF81: 1}},
        dict(POISON, wram={0xFF81: b"\x03", **PALETTE_SEED}, ramg=False,
             sram={1: {0xA800: bytes(reversed(SRAM_PALETTE))}},
             sread={1: {0xA000: 1}},
             read={BGP: 1, BG_PALS: 128, 0xFF81: 1}),
    ],
    "Func_10d74": [
        {"b": 0, "wram": {WD317: b"\x00", **PALETTE_SEED}, "read": {WD317: 1, BG_PALS: 64}},
        {"b": 1, "wram": {WD317: b"\x01", **PALETTE_SEED}, "read": {WD317: 1, BG_PALS: 32}},
        {"b": 2, "wram": {WD317: b"\x02", **PALETTE_SEED}, "read": {WD317: 1, BG_PALS: 32}},
        {"b": 3, "wram": {WD317: b"\x03", **PALETTE_SEED}, "read": {WD317: 1, BG_PALS: 64}},
        {"b": 4, "wram": {WD317: b"\x04", **PALETTE_SEED}, "read": {WD317: 1, BG_PALS: 64}},
        dict(POISON, b=4, wram={WD317: b"\x04", **PALETTE_SEED}, read={WD317: 1, BG_PALS: 64}),
    ],
}

MUTATIONS = {
    "LoadConsolePaletteData": {
        "source_symbol": "LoadConsolePaletteData",
        "before": "gb_write8(wConsolePaletteData_ADDR, 0);",
        "after": "gb_write8(wConsolePaletteData_ADDR, 0xFF);",
        "case_ids": ["LoadConsolePaletteData-0", "LoadConsolePaletteData-1"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

FADE_EVENTS = [{"keys": 0}]
for _i, _rec in enumerate(SCHEMA2_CASES["FadeScreenFromWhite"]):
    _rec["input_events"] = list(FADE_EVENTS)
