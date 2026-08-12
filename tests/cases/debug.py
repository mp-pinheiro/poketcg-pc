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

# >>> factory UnreferencedFillVRAMWithRandomData
CONTRACT["UnreferencedFillVRAMWithRandomData"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("d", "e"),
}
CASES["UnreferencedFillVRAMWithRandomData"] = [
    {"wram": {0xCACA: b"\x00\x00\x00"}, "vread": {0: {0x8000: 0x800}},
     "instruction_budget": 200000, "cycle_budget": 2000000},
    dict(POISON, wram={0xCACA: b"\x12\x34\x56"}, vread={0: {0x8000: 0x800}},
         instruction_budget=200000, cycle_budget=2000000),
    dict(POISON, wram={0xCACA: b"\xff\xff\xff"}, vread={0: {0x8000: 0x800}},
         instruction_budget=200000, cycle_budget=2000000),
]
# <<< factory UnreferencedFillVRAMWithRandomData

# >>> factory _DebugVEffect
CONTRACT["_DebugVEffect"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
}
CASES["_DebugVEffect"] = [
    {"wram": {0xC100: b"\x5a"}, "read": {0xC100: 1}},
    dict(POISON, wram={0xC100: b"\xa5"}, read={0xC100: 1}),
]
# <<< factory _DebugVEffect

# >>> factory Func_80c64
CONTRACT["Func_80c64"] = {"compare": (), "preserve": ()}
CASES["Func_80c64"] = [
    {"wram": {0xCD08: b"\x00", 0xCC16: b"\x00\x00", 0xCC14: b"\x00",
              0xCC18: b"\x00", 0xCC19: b"\x00", 0xCD11: b"\xff" * 8},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCD08: 1, 0xCE3F: 2, 0xCE43: 2, 0xCE45: 2, 0xCD0F: 1,
              0xCD10: 1, 0xCD11: 8, 0xFFB1: 1}},
    dict(POISON, wram={0xCD08: b"\x00", 0xCC16: b"\x00\x00", 0xCC14: b"\x00",
                        0xCC18: b"\x00", 0xCC19: b"\x00", 0xCD11: b"\xff" * 8},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCD08: 1, 0xCE3F: 2, 0xCE43: 2, 0xCE45: 2, 0xCD0F: 1,
               0xCD10: 1, 0xCD11: 8, 0xFFB1: 1}),
    {"wram": {0xCD08: b"\x02", 0xCC16: b"\x12\x34", 0xCC14: b"\x05",
              0xCC18: b"\x07", 0xCC19: b"\x09", 0xCD11: b"\xff" * 8},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCD08: 1, 0xCE3F: 2, 0xCE43: 2, 0xCE45: 2, 0xCD0F: 1,
              0xCD10: 1, 0xCD11: 8, 0xFFB1: 1}},
]
# <<< factory Func_80c64

# >>> factory DebugVEffect
CONTRACT["DebugVEffect"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "b", "c", "d", "e", "hl"),
}
CASES["DebugVEffect"] = [
    {},
    dict(POISON),
]
# <<< factory DebugVEffect

# >>> factory DebugCGBTest
CONTRACT["DebugCGBTest"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "b", "c", "d", "e", "hl"),
}
CASES["DebugCGBTest"] = [
    {},
    dict(POISON),
]
# <<< factory DebugCGBTest

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
# >>> factory-mutation UnreferencedFillVRAMWithRandomData
MUTATIONS["UnreferencedFillVRAMWithRandomData"] = {
    "source_symbol": "UnreferencedFillVRAMWithRandomData",
    "before": "uint32_t n = 0x800u;",
    "after": "uint32_t n = 0x7ffu;",
    "case_ids": ["UnreferencedFillVRAMWithRandomData-0",
                 "UnreferencedFillVRAMWithRandomData-1",
                 "UnreferencedFillVRAMWithRandomData-2"],
}
# <<< factory-mutation UnreferencedFillVRAMWithRandomData
# >>> factory-mutation _DebugVEffect
MUTATIONS["_DebugVEffect"] = {
    "source_symbol": "_DebugVEffect",
    "before": "void _DebugVEffect(void)\n{\n}",
    "after": "void _DebugVEffect(void)\n{\n\tgb_write8(0xC100, 0x01);\n}",
    "case_ids": ["_DebugVEffect-0", "_DebugVEffect-1"],
}
# <<< factory-mutation _DebugVEffect
# >>> factory-mutation Func_80c64
MUTATIONS["Func_80c64"] = {
    "source_symbol": "Func_80c64",
    "before": "for (uint8_t i = 0; i < 8u; i++)",
    "after": "for (uint8_t i = 0; i < 7u; i++)",
    "case_ids": ["Func_80c64-0", "Func_80c64-1", "Func_80c64-2"],
}
# <<< factory-mutation Func_80c64
# >>> factory-mutation DebugVEffect
MUTATIONS["DebugVEffect"] = {
    "source_symbol": "DebugVEffect",
    "before": "f = (uint8_t)((f & 0x80u) | 0x10u);\n\treturn (DebugVEffectResult){a, f, b, c, d, e, hl};",
    "after": "f = (uint8_t)((f & 0x80u) | 0x00u);\n\treturn (DebugVEffectResult){a, f, b, c, d, e, hl};",
    "case_ids": ["DebugVEffect-0", "DebugVEffect-1"],
}
# <<< factory-mutation DebugVEffect
# >>> factory-mutation DebugCGBTest
MUTATIONS["DebugCGBTest"] = {
    "source_symbol": "DebugCGBTest",
    "before": "f = (uint8_t)((f & 0x80u) | 0x10u);\n\treturn (DebugCGBTestResult){a, f, b, c, d, e, hl};",
    "after": "f = (uint8_t)((f & 0x80u) | 0x00u);\n\treturn (DebugCGBTestResult){a, f, b, c, d, e, hl};",
    "case_ids": ["DebugCGBTest-0", "DebugCGBTest-1"],
}
# <<< factory-mutation DebugCGBTest
