POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

DEBUG_BORDER = 0xD419
CONSOLE = 0xCAB4
LCDC_STATE = 0xCABB
LCDC_WORK = 0xCAB7
KEYS_PRESSED = 0xFF91

CONTRACT = {
    "DebugSGBFrame": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "DebugStandardBGCharacter": {
        "compare": ("a", "f", "d", "e"),
        "preserve": (),
    },
    "DebugQuit": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "DebugSGBFrame": [
        {"wram": {DEBUG_BORDER: b"\x00", CONSOLE: b"\x00", LCDC_STATE: b"\x80",
                   LCDC_WORK: b"\xff", 0xFFFF: b"\xff"},
         "read": {DEBUG_BORDER: 1, CONSOLE: 1, LCDC_STATE: 1, LCDC_WORK: 1,
                   0xFF40: 1, 0xFFFF: 1}},
        dict(POISON, wram={DEBUG_BORDER: b"\x02", CONSOLE: b"\x00",
                           LCDC_STATE: b"\x00", LCDC_WORK: b"\xa5"},
             read={DEBUG_BORDER: 1, CONSOLE: 1, LCDC_STATE: 1, LCDC_WORK: 1}),
        {"wram": {DEBUG_BORDER: b"\x03", CONSOLE: b"\x00", LCDC_STATE: b"\x80",
                   LCDC_WORK: b"\xff", 0xFFFF: b"\xff"},
         "read": {DEBUG_BORDER: 1, CONSOLE: 1, LCDC_STATE: 1, LCDC_WORK: 1,
                   0xFF40: 1, 0xFFFF: 1}},
    ],
    "DebugStandardBGCharacter": [
        {"keys": 0xFF, "setup": [{"fn": "DisableLCD"}],
         "wram": {KEYS_PRESSED: b"\xff"},
         "read": {KEYS_PRESSED: 1},
         "vread": {0: {0x9800: 256}}},
        dict(POISON, keys=0xFF, setup=[{"fn": "DisableLCD"}],
             wram={KEYS_PRESSED: b"\xff"}, read={KEYS_PRESSED: 1},
             vread={0: {0x9800: 256}}),
    ],
    "DebugQuit": [
        {"a": 0, "f": 0},
        dict(POISON),
        {"a": 0, "f": 0x10},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DebugSGBFrame": {
        "source_symbol": "DebugSGBFrame",
        "before": "if (next >= 4u)",
        "after": "if (next > 4u)",
        "case_ids": ["DebugSGBFrame-0", "DebugSGBFrame-1", "DebugSGBFrame-2"],
    },
    "DebugStandardBGCharacter": {
        "source_symbol": "DebugStandardBGCharacter",
        "before": "FillRectangle(0x80u, 16u, 16u, 0, 0x0110u)",
        "after": "FillRectangle(0x81u, 16u, 16u, 0, 0x0110u)",
        "case_ids": ["DebugStandardBGCharacter-0", "DebugStandardBGCharacter-1"],
    },
    "DebugQuit": {
        "source_symbol": "DebugQuit",
        "before": "a == 0",
        "after": "a != 0",
        "case_ids": ["DebugQuit-0", "DebugQuit-1", "DebugQuit-2"],
    },
}
