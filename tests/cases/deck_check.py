POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

X_POSITION = 0xCEAF
Y_POSITION = 0xCEB0

CONTRACT = {
    "DrawCheckMenuCursor": {
        "compare": ("a", "d", "e", "f"),
        "preserve": ("d",),
    },
    "PlaySFXConfirmOrCancel": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "DrawCheckMenuCursor": [
        {"read": {0x9800 + 14 * 32 + 1: 1}},
        dict(POISON, a=0x5A, wram={X_POSITION: b"\x01", Y_POSITION: b"\x01"},
             read={0x9800 + 16 * 32 + 11: 1}),
        {"a": 0x33, "wram": {X_POSITION: b"\xFF", Y_POSITION: b"\xFF"},
         "read": {0x9800 + 12 * 32 + 247: 1}},
    ],
    "PlaySFXConfirmOrCancel": [
        {"a": 0, "read": {0xDD82: 1, 0xDD83: 1}},
        dict(POISON, a=0xFF, read={0xDD82: 1, 0xDD83: 1}),
        {"a": 1, "read": {0xDD82: 1, 0xDD83: 1}},
    ],
}

# >>> factory EraseCheckMenuCursor
CONTRACT["EraseCheckMenuCursor"] = {"compare": ("a", "d", "e", "f"), "preserve": ("d",)}
CASES["EraseCheckMenuCursor"] = [
    {"read": {0x9800 + 14 * 32 + 1: 1}},
    dict(POISON, wram={X_POSITION: b"\x01", Y_POSITION: b"\x01"},
         read={0x9800 + 16 * 32 + 11: 1}),
    {"wram": {X_POSITION: b"\xFF", Y_POSITION: b"\xFF"},
     "read": {0x9800 + 12 * 32 + 247: 1}},
]
# <<< factory EraseCheckMenuCursor

# >>> factory DisplayCheckMenuCursor
CONTRACT["DisplayCheckMenuCursor"] = {"compare": ("a", "d", "e", "f"), "preserve": ("d",)}
CASES["DisplayCheckMenuCursor"] = [
    {"read": {0x9800 + 14 * 32 + 1: 1}},
    dict(POISON, wram={X_POSITION: b"\x01", Y_POSITION: b"\x01"},
         read={0x9800 + 16 * 32 + 11: 1}),
    {"wram": {X_POSITION: b"\xFF", Y_POSITION: b"\xFF"},
     "read": {0x9800 + 12 * 32 + 247: 1}},
]
# <<< factory DisplayCheckMenuCursor

# >>> factory-cases-statics
wMenuInputSFX = 0xCFE3
hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
wCheckMenuCursorXPosition = 0xCEAF
wCheckMenuCursorYPosition = 0xCEB0
wCheckMenuCursorBlinkCounter = 0xCEA3
# <<< factory-cases-statics

# >>> factory HandleCheckMenuInput
CONTRACT["HandleCheckMenuInput"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["HandleCheckMenuInput"] = [
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x02",
              wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03"}},
    dict(POISON, wram={hDPadHeld: b"\x00", hKeysPressed: b"\x03",
                       wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03"}),
    {"wram": {hDPadHeld: b"\x20", hKeysPressed: b"\x00",
              wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03",
              wCheckMenuCursorBlinkCounter: b"\x01"}},
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00",
              wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03",
              wCheckMenuCursorBlinkCounter: b"\x05"}},
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00",
              wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03",
              wCheckMenuCursorBlinkCounter: b"\x00"}},
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00",
              wCheckMenuCursorXPosition: b"\x05", wCheckMenuCursorYPosition: b"\x03",
              wCheckMenuCursorBlinkCounter: b"\x10"}},
]
# <<< factory HandleCheckMenuInput

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawCheckMenuCursor": {
        "source_symbol": "DrawCheckMenuCursor",
        "before": "uint8_t b = (uint8_t)(product + 1u);",
        "after": "uint8_t b = (uint8_t)(product + 2u);",
        "case_ids": ["DrawCheckMenuCursor-1", "DrawCheckMenuCursor-2"],
    },
    "PlaySFXConfirmOrCancel": {
        "source_symbol": "PlaySFXConfirmOrCancel",
        "before": "uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;",
        "after": "uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CONFIRM : SFX_CONFIRM;",
        "case_ids": ["PlaySFXConfirmOrCancel-1"],
    },
}
# >>> factory-mutation EraseCheckMenuCursor
MUTATIONS["EraseCheckMenuCursor"] = {
    "source_symbol": "EraseCheckMenuCursor",
    "before": "DrawCheckMenuCursorResult EraseCheckMenuCursor(void)\n{\n\treturn DrawCheckMenuCursor(SYM_SPACE);\n}",
    "after": "DrawCheckMenuCursorResult EraseCheckMenuCursor(void)\n{\n\treturn DrawCheckMenuCursor(SYM_CURSOR_R);\n}",
    "case_ids": ["EraseCheckMenuCursor-0", "EraseCheckMenuCursor-1", "EraseCheckMenuCursor-2"],
}
# <<< factory-mutation EraseCheckMenuCursor
# >>> factory-mutation DisplayCheckMenuCursor
MUTATIONS["DisplayCheckMenuCursor"] = {
    "source_symbol": "DisplayCheckMenuCursor",
    "before": "DrawCheckMenuCursorResult DisplayCheckMenuCursor(void)\n{\n\treturn DrawCheckMenuCursor(SYM_CURSOR_R);\n}",
    "after": "DrawCheckMenuCursorResult DisplayCheckMenuCursor(void)\n{\n\treturn DrawCheckMenuCursor(SYM_SPACE);\n}",
    "case_ids": ["DisplayCheckMenuCursor-0", "DisplayCheckMenuCursor-1", "DisplayCheckMenuCursor-2"],
}
# <<< factory-mutation DisplayCheckMenuCursor
# >>> factory-mutation HandleCheckMenuInput
MUTATIONS["HandleCheckMenuInput"] = {"source_symbol": "HandleCheckMenuInput", "before": "return (HandleCheckMenuInputResult){MENU_CONFIRM, 0x10u};", "after": "return (HandleCheckMenuInputResult){MENU_CANCEL, 0x10u};", "case_ids": ["HandleCheckMenuInput-1"]}
# <<< factory-mutation HandleCheckMenuInput
