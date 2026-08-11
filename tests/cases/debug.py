POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

W_DEBUG_SGB_BORDER = 0xD419
H_KEYS_PRESSED = 0xFF91

CONTRACT = {
    "DebugSGBFrame": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "DebugStandardBGCharacter": {
        "compare": ("a", "f"),
    },
    "DebugQuit": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "DebugSGBFrame": [
        {"setup": [{"fn": "DisableLCD"}],
         "wram": {W_DEBUG_SGB_BORDER: b"\x00"},
         "read": {W_DEBUG_SGB_BORDER: 1}},
        dict(POISON, setup=[{"fn": "DisableLCD"}],
             wram={W_DEBUG_SGB_BORDER: b"\x00"},
             read={W_DEBUG_SGB_BORDER: 1}),
        {"setup": [{"fn": "DisableLCD"}],
         "wram": {W_DEBUG_SGB_BORDER: b"\x02"},
         "read": {W_DEBUG_SGB_BORDER: 1}},
        {"setup": [{"fn": "DisableLCD"}],
         "wram": {W_DEBUG_SGB_BORDER: b"\x03"},
         "read": {W_DEBUG_SGB_BORDER: 1}},
    ],
    "DebugStandardBGCharacter": [
        {"setup": [{"fn": "DisableLCD"}],
         "wram": {H_KEYS_PRESSED: b"\x01"},
         "keys": 0xFF,
         "vread": {0: {0x9800: 0x400}}},
        dict(POISON, setup=[{"fn": "DisableLCD"}],
             wram={H_KEYS_PRESSED: b"\x80"}, keys=0xFF,
             vread={0: {0x9800: 0x400}}),
    ],
    "DebugQuit": [
        {"a": 0},
        dict(POISON, a=0),
        {"a": 1},
        dict(POISON, a=0xFF),
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DebugSGBFrame": {
        "source_symbol": "DebugSGBFrame",
        "before": "if (border >= 4)",
        "after": "if (border > 4)",
        "case_ids": ["DebugSGBFrame-0", "DebugSGBFrame-1", "DebugSGBFrame-2", "DebugSGBFrame-3"],
    },
    "DebugStandardBGCharacter": {
        "source_symbol": "DebugStandardBGCharacter",
        "before": "FillRectangle(0x80, 16, 16, 0, 0x0110);",
        "after": "FillRectangle(0x00, 16, 16, 0, 0x0110);",
        "case_ids": ["DebugStandardBGCharacter-0", "DebugStandardBGCharacter-1"],
    },
    "DebugQuit": {
        "source_symbol": "DebugQuit",
        "before": "return (DebugResult){a, a ? 0 : 0x80};",
        "after": "return (DebugResult){a, a ? 0x80 : 0x80};",
        "case_ids": ["DebugQuit-0", "DebugQuit-1", "DebugQuit-2", "DebugQuit-3"],
    },
}
