POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_CONSOLE = 0xCAB4
W_GIFT_CENTER_CHOICE = 0xD10E
W_LOAD_NPC_DIRECTION = 0xD3AE
W_LOADED_EVENT_BITS = 0xD3D1
W_EVENT_VARS = 0xD3D2
EVENT_CHOICE = W_EVENT_VARS + 0x1A

CONTRACT = {
    "Func_fcad": {"compare": (), "preserve": ()},
    "Preload_GiftCenterClerk": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Func_fcad": [
        {"wram": {W_GIFT_CENTER_CHOICE: b"\x00", W_EVENT_VARS: bytes(64)},
         "read": {EVENT_CHOICE: 1, W_LOADED_EVENT_BITS: 1}},
        dict(POISON,
             wram={W_GIFT_CENTER_CHOICE: b"\x04", W_EVENT_VARS: bytes(0x1A) + b"\x03" + bytes(64 - 0x1B)},
             read={EVENT_CHOICE: 1, W_LOADED_EVENT_BITS: 1}),
        {"wram": {W_GIFT_CENTER_CHOICE: b"\x01", W_EVENT_VARS: bytes(64)},
         "read": {EVENT_CHOICE: 1, W_LOADED_EVENT_BITS: 1}},
        {"wram": {W_GIFT_CENTER_CHOICE: b"\x04", W_EVENT_VARS: bytes(64)},
         "read": {EVENT_CHOICE: 1, W_LOADED_EVENT_BITS: 1}},
        {"wram": {W_GIFT_CENTER_CHOICE: b"\xFF", W_EVENT_VARS: bytes(64)},
         "read": {EVENT_CHOICE: 1, W_LOADED_EVENT_BITS: 1}},
    ],
    "Preload_GiftCenterClerk": [
        {"wram": {W_CONSOLE: b"\x00", W_LOAD_NPC_DIRECTION: b"\xFF"},
         "read": {W_LOAD_NPC_DIRECTION: 1}},
        dict(POISON,
             wram={W_CONSOLE: b"\x00", W_LOAD_NPC_DIRECTION: b"\xAA"},
             read={W_LOAD_NPC_DIRECTION: 1}),
        {"wram": {W_CONSOLE: b"\x02", W_LOAD_NPC_DIRECTION: b"\xFF"},
         "read": {W_LOAD_NPC_DIRECTION: 1}},
        dict(POISON,
             wram={W_CONSOLE: b"\x02", W_LOAD_NPC_DIRECTION: b"\xAA"},
             read={W_LOAD_NPC_DIRECTION: 1}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Func_fcad": {
        "source_symbol": "Func_fcad",
        "before": "uint8_t encoded = (uint8_t)((value << 2) & EVENT_GIFT_CENTER_MENU_CHOICE_MASK);",
        "after": "uint8_t encoded = (uint8_t)((value << 1) & EVENT_GIFT_CENTER_MENU_CHOICE_MASK);",
        "case_ids": ["Func_fcad-0", "Func_fcad-1", "Func_fcad-2", "Func_fcad-3", "Func_fcad-4"],
    },
    "Preload_GiftCenterClerk": {
        "source_symbol": "Preload_GiftCenterClerk",
        "before": "if (console != CONSOLE_CGB) {",
        "after": "if (console == CONSOLE_CGB) {",
        "case_ids": ["Preload_GiftCenterClerk-0", "Preload_GiftCenterClerk-1", "Preload_GiftCenterClerk-2", "Preload_GiftCenterClerk-3"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
