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

# >>> factory-cases-statics
DEBUG_CREATE_WLCDC = 0xCABB
DEBUG_CREATE_RLCDC = 0xFF40
DEBUG_CREATE_DPAD = 0xFF8F
DEBUG_CREATE_KEYS = 0xFF91
DEBUG_CREATE_MENU_ITEM = 0xCD10
DEBUG_CREATE_SELECTION = 0xD41A
DEBUG_CREATE_CUR_MENU = 0xFFB1

wLoadedNPCTempIndex = 0xD3AA

DEBUG_DUEL_MENU_ITEM = 0xFFB1
DEBUG_DUEL_MODE = 0xBA41
# <<< factory-cases-statics

# >>> factory DebugCreateBoosterPack
CONTRACT["DebugCreateBoosterPack"] = {"compare": ("f",), "preserve": ()}
CASES["DebugCreateBoosterPack"] = [
    {"rom_bank": 0x04,
     "wram": {DEBUG_CREATE_WLCDC: b"\x00", DEBUG_CREATE_RLCDC: b"\x00",
               DEBUG_CREATE_DPAD: b"\x00", DEBUG_CREATE_KEYS: b"\x02",
               DEBUG_CREATE_SELECTION: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {DEBUG_CREATE_MENU_ITEM: 1, DEBUG_CREATE_CUR_MENU: 1,
               DEBUG_CREATE_SELECTION: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"rom_bank": 0x04,
     "wram": {DEBUG_CREATE_WLCDC: b"\x00", DEBUG_CREATE_RLCDC: b"\x00",
               DEBUG_CREATE_DPAD: b"\x00", DEBUG_CREATE_KEYS: b"\x02",
               DEBUG_CREATE_SELECTION: b"\x02"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {DEBUG_CREATE_MENU_ITEM: 1, DEBUG_CREATE_CUR_MENU: 1,
               DEBUG_CREATE_SELECTION: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, rom_bank=0x04,
         wram={DEBUG_CREATE_WLCDC: b"\x00", DEBUG_CREATE_RLCDC: b"\x00",
               DEBUG_CREATE_DPAD: b"\x00", DEBUG_CREATE_KEYS: b"\x02",
               DEBUG_CREATE_SELECTION: b"\x03"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={DEBUG_CREATE_MENU_ITEM: 1, DEBUG_CREATE_CUR_MENU: 1,
               DEBUG_CREATE_SELECTION: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DebugCreateBoosterPack

# >>> factory DebugCredits
CONTRACT["DebugCredits"] = {"compare": (), "preserve": ()}
CASES["DebugCredits"] = [
    dict(oracle=False, evidence="primary", why="The bounded debug wrapper stops at the nested credits routine entry; no wrapper state changes occur before that farcall.", wram={0xDD80: b"\x7F"}, read={0xDD80: 1}, expect={0xDD80: b"\x7F"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=False, evidence="primary", why="The wrapper has no pre-call state effects and remains unchanged with poisoned entry registers.", wram={0xDD80: b"\x7F"}, read={0xDD80: 1}, expect={0xDD80: b"\x7F"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DebugCredits

# >>> factory _DebugLookAtSprite
CONTRACT["_DebugLookAtSprite"] = {
    "compare": (),
    "preserve": (),
}
CASES["_DebugLookAtSprite"] = [
    dict(keys=[0x00, 0x04], read={wLoadedNPCTempIndex: 1}, setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}], instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x04], read={wLoadedNPCTempIndex: 1}, setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _DebugLookAtSprite

# >>> factory DebugLookAtSprite
CONTRACT["DebugLookAtSprite"] = {
    "compare": (),
    "preserve": (),
}
CASES["DebugLookAtSprite"] = [
    {"keys": [0x00, 0x04],
     "read": {0xD3AA: 1},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x04],
         read={0xD3AA: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DebugLookAtSprite

# >>> factory DebugDuelMode
CONTRACT["DebugDuelMode"] = {
    "compare": ("a", "f"),
    "preserve": (),
}
CASES["DebugDuelMode"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xCABB: b"\x80", 0xFF40: b"\x80", DEBUG_DUEL_MENU_ITEM: b"\x00"},
     "sram": {0: {DEBUG_DUEL_MODE: b"\x00"}},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {DEBUG_DUEL_MENU_ITEM: 1},
     "sread": {0: {DEBUG_DUEL_MODE: 1}},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCABB: b"\x80", 0xFF40: b"\x80", DEBUG_DUEL_MENU_ITEM: b"\x01"},
         sram={0: {DEBUG_DUEL_MODE: b"\x01"}},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={DEBUG_DUEL_MENU_ITEM: 1},
         sread={0: {DEBUG_DUEL_MODE: 1}},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DebugDuelMode

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
        "before": "\treturn (DebugQuitResult){a, (uint8_t)(a == 0",
        "after": "\treturn (DebugQuitResult){a, (uint8_t)(a != 0",
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
# >>> factory-mutation DebugCreateBoosterPack
MUTATIONS["DebugCreateBoosterPack"] = {"source_symbol": "DebugCreateBoosterPack", "before": "\tuint8_t selected = wDebugBoosterSelection;", "after": "\tuint8_t selected = (uint8_t)(wDebugBoosterSelection + 1u);", "case_ids": ["DebugCreateBoosterPack-0", "DebugCreateBoosterPack-1", "DebugCreateBoosterPack-2"]}
# <<< factory-mutation DebugCreateBoosterPack
# >>> factory-mutation DebugCredits
MUTATIONS["DebugCredits"] = {"source_symbol": "DebugCredits", "before": "void DebugCredits(void)\n{\n}", "after": "void DebugCredits(void)\n{\n\tPlaySong(0u);\n}", "case_ids": ["DebugCredits-0", "DebugCredits-1"]}
# <<< factory-mutation DebugCredits
# >>> factory-completion DebugCredits
for _record in SCHEMA2_CASES["DebugCredits"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x56AD, "bank": 7}
# <<< factory-completion DebugCredits
# >>> factory-mutation _DebugLookAtSprite
MUTATIONS["_DebugLookAtSprite"] = {
    "source_symbol": "_DebugLookAtSprite",
    "before": "wLoadedNPCTempIndex = 0x01u;",
    "after": "wLoadedNPCTempIndex = 0x02u;",
    "case_ids": ["_DebugLookAtSprite-0", "_DebugLookAtSprite-1"],
}
# <<< factory-mutation _DebugLookAtSprite
# >>> factory-completion _DebugLookAtSprite
for _rec in SCHEMA2_CASES["_DebugLookAtSprite"]:
    _rec["completion"] = {"mode": "event", "predicate": "mem:0xd3aa==0x1&0xff"}
# <<< factory-completion _DebugLookAtSprite
# >>> factory-mutation DebugLookAtSprite
MUTATIONS["DebugLookAtSprite"] = {
    "source_symbol": "DebugLookAtSprite",
    "before": "\t_DebugLookAtSprite();",
    "after": "\tgb_write8(0xD3AAu, 0x02u);",
    "case_ids": ["DebugLookAtSprite-0", "DebugLookAtSprite-1"],
}
# <<< factory-mutation DebugLookAtSprite
# >>> factory-completion DebugLookAtSprite
for _rec in SCHEMA2_CASES["DebugLookAtSprite"]:
    _rec["completion"] = {"mode": "event", "predicate": "mem:0xd3aa==0x1&0xff"}
# <<< factory-completion DebugLookAtSprite
# >>> factory-mutation DebugDuelMode
MUTATIONS["DebugDuelMode"] = {
    "source_symbol": "DebugDuelMode",
    "before": "DebugDuelModeResult DebugDuelMode(void)\n{\n\tEnableSRAM();\n\tuint8_t selected = (uint8_t)(sDebugDuelMode & 0x01u);\n\tsDebugDuelMode = selected;\n\tInitAndPrintMenu(DEBUG_DUEL_MENU_PARAMS, selected);\n\n\tfor (;;) {\n\t\tDoFrameIfLCDEnabled();\n\t\tHandleMenuInputResult input = HandleMenuInput();\n\t\tif ((input.f & 0x10u) == 0u)\n\t\t\tcontinue;\n\t\tuint8_t item = hCurMenuItem;\n\t\tif (item != input.e)\n\t\t\tcontinue;\n\t\tuint8_t final = (uint8_t)(item & 0x01u);\n\t\tsDebugDuelMode = final;",
    "after": "DebugDuelModeResult DebugDuelMode(void)\n{\n\tEnableSRAM();\n\tuint8_t selected = (uint8_t)(sDebugDuelMode & 0x01u);\n\tsDebugDuelMode = selected;\n\tInitAndPrintMenu(DEBUG_DUEL_MENU_PARAMS, selected);\n\n\tfor (;;) {\n\t\tDoFrameIfLCDEnabled();\n\t\tHandleMenuInputResult input = HandleMenuInput();\n\t\tif ((input.f & 0x10u) == 0u)\n\t\t\tcontinue;\n\t\tuint8_t item = hCurMenuItem;\n\t\tif (item != input.e)\n\t\t\tcontinue;\n\t\tuint8_t final = (uint8_t)(item & 0x01u);\n\t\tsDebugDuelMode = (uint8_t)(final ^ 0x01u);",
    "case_ids": ["DebugDuelMode-0", "DebugDuelMode-1"],
}
# <<< factory-mutation DebugDuelMode
