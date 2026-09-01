"""Oracle-diff cases for poketcg/src/home/lcd_enable_frame.asm."""

HRAM = 0xFF8D
JOYP = 0xFF00
RLCDC = 0xFF40

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DoFrameIfLCDEnabled": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")},
}

CASES = {
    "DoFrameIfLCDEnabled": [
        {"setup": [{"fn": "DisableLCD"}], "keys": 0x01,
         "wram": {HRAM: b"\0\0\0\0\0"}, "read": {HRAM: 5}},
        dict(POISON, setup=[{"fn": "DisableLCD"}],
             wram={HRAM: b"\x11\x22\x33\x44\x55"}, read={HRAM: 5}),
        {"oracle": False,
         "why": "EnableLCD turns the LCD on, so a VBlank interrupt fires mid-routine into a zeroed wVBlankFunctionTrampoline and the oracle never returns; the LCD-on branch is verified against the C alone",
         "wram": {RLCDC: b"\x80", HRAM: b"\x11\x22\x33\x44\x55", JOYP: b"\x00"},
         "read": {HRAM: 5, JOYP: 1},
         "expect": {HRAM: b"\x11\x44\x00\x00\x00", JOYP: b"\x30"}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DoFrameIfLCDEnabled": {
        "source_symbol": "DoFrameIfLCDEnabled",
        "before": "if (gb_read8(rLCDC) & LCDC_ON)",
        "after": "if (!(gb_read8(rLCDC) & LCDC_ON))",
        "case_ids": ["DoFrameIfLCDEnabled-0", "DoFrameIfLCDEnabled-1", "DoFrameIfLCDEnabled-2"],
    },
}
