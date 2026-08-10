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
        {"wram": {0xCABB: b"\0", 0xCABF: b"\0"},
         "read": {0xCABB: 1, 0xCABF: 1, 0xFF40: 1}},
        dict(POISON, wram={0xCABB: b"\x04", 0xCABF: b"\x55"},
             read={0xCABB: 1, 0xCABF: 1, 0xFF40: 1}),
    ],
    "DisableLCD": [
        {"wram": {0xCABB: b"\x80", 0xCAB7: b"\xFF", 0xFF40: b"\x80", 0xFFFF: b"\xFF"},
         "read": {0xCABB: 1, 0xCAB7: 1, 0xFF40: 1, 0xFFFF: 1,
                  0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
        dict(POISON, wram={0xCABB: b"\0", 0xCAB7: b"\xA5", 0xFF40: b"\0", 0xFFFF: b"\xA5"},
             read={0xCABB: 1, 0xCAB7: 1}),
    ],
    "Set_OBJ_8x8": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "Set_OBJ_8x16": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x80"}, read={0xCABB: 1})],
    "SetWindowOn": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "SetWindowOff": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x20"}, read={0xCABB: 1})],
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
