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
