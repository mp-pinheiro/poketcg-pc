from tests.cases._symbols import sym
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "EnableLCD": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "DisableLCD": {"compare": ("b",), "preserve": ("b",)},
    "Set_OBJ_8x8": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "Set_OBJ_8x16": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetWindowOn": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetWindowOff": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    # Oracle-run: $FF00-$FF7F is captured, so rLCDC is diffed against the ROM.
    # rIE ($FFFF) is HRAM and was already observable.
    "EnableLCD": [
        {"wram": {sym("wLCDC"): b"\0", sym("wFlushPaletteFlags"): b"\0"},
         "read": {sym("wLCDC"): 1, sym("wFlushPaletteFlags"): 1, 0xFF40: 1}},
        dict(POISON, wram={sym("wLCDC"): b"\x04", sym("wFlushPaletteFlags"): b"\x55"},
             read={sym("wLCDC"): 1, sym("wFlushPaletteFlags"): 1, 0xFF40: 1}),
    ],
    "DisableLCD": [
        {"wram": {sym("wLCDC"): b"\x80", sym("wIE"): b"\xFF", 0xFF40: b"\x80", 0xFFFF: b"\xFF"},
         "read": {sym("wLCDC"): 1, sym("wIE"): 1, 0xFF40: 1, 0xFFFF: 1,
                  0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
        dict(POISON, wram={sym("wLCDC"): b"\0", sym("wIE"): b"\xA5", 0xFF40: b"\0", 0xFFFF: b"\xA5"},
             read={sym("wLCDC"): 1, sym("wIE"): 1}),
    ],
    "Set_OBJ_8x8": [{"wram": {sym("wLCDC"): b"\xFF"}, "read": {sym("wLCDC"): 1}}, dict(POISON, wram={sym("wLCDC"): b"\x04"}, read={sym("wLCDC"): 1})],
    "Set_OBJ_8x16": [{"wram": {sym("wLCDC"): b"\0"}, "read": {sym("wLCDC"): 1}}, dict(POISON, wram={sym("wLCDC"): b"\x80"}, read={sym("wLCDC"): 1})],
    "SetWindowOn": [{"wram": {sym("wLCDC"): b"\0"}, "read": {sym("wLCDC"): 1}}, dict(POISON, wram={sym("wLCDC"): b"\x04"}, read={sym("wLCDC"): 1})],
    "SetWindowOff": [{"wram": {sym("wLCDC"): b"\xFF"}, "read": {sym("wLCDC"): 1}}, dict(POISON, wram={sym("wLCDC"): b"\x20"}, read={sym("wLCDC"): 1})],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "EnableLCD": {
        "source_symbol": "EnableLCD",
        "before": "if (value & LCDC_ON)",
        "after": "if (value | LCDC_ON)",
        "case_ids": ["EnableLCD-0", "EnableLCD-1"],
    },
}
MUTATIONS["DisableLCD"] = {
    "source_symbol": "DisableLCD",
    "before": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_ON));",
    "after": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | (uint8_t)~LCDC_ON));",
    "case_ids": ["DisableLCD-0"],
}
MUTATIONS["SetWindowOff"] = {
    "source_symbol": "SetWindowOff",
    "before": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_WIN_ON));",
    "after": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | (uint8_t)~LCDC_WIN_ON));",
    "case_ids": ["SetWindowOff-0"],
}
MUTATIONS["SetWindowOn"] = {
    "source_symbol": "SetWindowOn",
    "before": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | LCDC_WIN_ON));",
    "after": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & LCDC_WIN_ON));",
    "case_ids": ["SetWindowOn-0"],
}
MUTATIONS["Set_OBJ_8x16"] = {
    "source_symbol": "Set_OBJ_8x16",
    "before": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | LCDC_OBJ_16));",
    "after": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & LCDC_OBJ_16));",
    "case_ids": ["Set_OBJ_8x16-0"],
}
MUTATIONS["Set_OBJ_8x8"] = {
    "source_symbol": "Set_OBJ_8x8",
    "before": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_OBJ_16));",
    "after": "\tgb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | (uint8_t)~LCDC_OBJ_16));",
    "case_ids": ["Set_OBJ_8x8-0"],
}
