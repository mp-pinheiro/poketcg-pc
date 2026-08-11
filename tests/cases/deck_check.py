POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CURSOR_X = 0xCEAF
CURSOR_Y = 0xCEB0
SFX_ID = 0xDD82
SFX_PRIORITY = 0xDD83

CONTRACT = {
    "DrawCheckMenuCursor": {"compare": ("d",), "preserve": ("d",)},
    "PlaySFXConfirmOrCancel": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "DrawCheckMenuCursor": [
        {"read": {0x99C1: 1}, "wram": {CURSOR_X: b"\x00", CURSOR_Y: b"\x00"}},
        dict(POISON, wram={CURSOR_X: b"\x00", CURSOR_Y: b"\x00"}, read={0x99C1: 1}),
        {"a": 0x5A, "wram": {CURSOR_X: b"\x01", CURSOR_Y: b"\x01"},
         "read": {0x9A0B: 1}},
        {"a": 0xFF, "wram": {CURSOR_X: b"\xFF", CURSOR_Y: b"\x0F"},
         "read": {0x9E77: 1}},
    ],
    "PlaySFXConfirmOrCancel": [
        {"a": 0, "read": {SFX_ID: 1, SFX_PRIORITY: 1}},
        dict(POISON, a=0xFF, read={SFX_ID: 1, SFX_PRIORITY: 1}),
        {"a": 1, "read": {SFX_ID: 1, SFX_PRIORITY: 1}},
        {"a": 0xFF, "read": {SFX_ID: 1, SFX_PRIORITY: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawCheckMenuCursor": {
        "source_symbol": "DrawCheckMenuCursor",
        "before": "uint8_t x = (uint8_t)(product + 1u);",
        "after": "uint8_t x = (uint8_t)(product + 2u);",
        "case_ids": ["DrawCheckMenuCursor-2", "DrawCheckMenuCursor-3"],
    },
    "PlaySFXConfirmOrCancel": {
        "source_symbol": "PlaySFXConfirmOrCancel",
        "before": "if (a == 0xFFu)",
        "after": "if (a == 0xFEu)",
        "case_ids": ["PlaySFXConfirmOrCancel-1", "PlaySFXConfirmOrCancel-3"],
    },
}
