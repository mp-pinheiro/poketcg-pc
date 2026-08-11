POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

H_KEYS_HELD = 0xFF90
H_SCX = 0xFF92
H_SCY = 0xFF93
W_VBLANK_COUNTER = 0xCAB8
W_RNG1 = 0xCACA
W_D41B = 0xD41B
W_D41C = 0xD41C
SPRITE_BUFFER = 0xD4D0

CONTRACT = {
    "Func_1c865": {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                    "preserve": ("a", "f", "b", "c", "d", "e", "hl")},
    "Func_1c866": {"compare": ("a", "b", "c", "d", "e", "hl"),
                    "preserve": ("d", "e", "hl")},
    "Func_1c890": {"compare": ("a", "b", "c", "d", "e", "hl"),
                    "preserve": ("b", "d", "e")},
}

CASES = {
    "Func_1c865": [
        {"wram": {0xC100: b"\x00"}, "read": {0xC100: 1}},
        dict(POISON, wram={0xC100: b"\x00"}, read={0xC100: 1}),
        {"a": 0, "f": 0xF0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
         "wram": {0xC100: b"\xA5"}, "read": {0xC100: 1}},
    ],
    "Func_1c866": [
        {"wram": {H_KEYS_HELD: b"\x00", H_SCX: b"\x00", H_SCY: b"\x00"}},
        dict(POISON, wram={H_KEYS_HELD: b"\xF0", H_SCX: b"\x11", H_SCY: b"\x22"}),
        {"wram": {H_KEYS_HELD: b"\x02", H_SCX: b"\xFF", H_SCY: b"\x00"}},
        {"keys": 0xF0, "wram": {H_KEYS_HELD: b"\xF0", H_SCX: b"\x80", H_SCY: b"\x80"}},
        {"keys": 0x60, "wram": {H_KEYS_HELD: b"\x60", H_SCX: b"\x01", H_SCY: b"\xFF"}},
    ],
    "Func_1c890": [
        {"wram": {W_VBLANK_COUNTER: b"\x00", W_D41B: b"\x00", W_D41C: b"\x00",
                  W_RNG1: b"\x00\x00\x00", 0xC100: b"\x00"}},
        dict(POISON, wram={W_VBLANK_COUNTER: b"\x00", W_D41B: b"\x0E", W_D41C: b"\x01",
                           W_RNG1: b"\x12\x34\x56", SPRITE_BUFFER: bytes(16),
                           0xC100: b"\x00"}),
        {"wram": {W_VBLANK_COUNTER: b"\x01", W_D41B: b"\x11", W_D41C: b"\x00",
                  W_RNG1: b"\xFF\xFF\xFF", 0xC100: b"\x5A"}},
        {"wram": {W_VBLANK_COUNTER: b"\x00", W_D41B: b"\x11", W_D41C: b"\x00",
                  W_RNG1: b"\xFF\xFF\xFF", SPRITE_BUFFER: bytes(15) + b"\x04",
                  0xC100: b"\x00"}},
        {"wram": {W_VBLANK_COUNTER: b"\x00", W_D41B: b"\x0F", W_D41C: b"\xFF",
                  W_RNG1: b"\x80\x01\xFF", SPRITE_BUFFER: bytes(16),
                  0xC100: b"\x00"}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Func_1c865": {
        "source_symbol": "Func_1c865",
        "before": "void Func_1c865(void)\n{\n}",
        "after": "void Func_1c865(void)\n{\n\tgb_write8(0xC100u, 0x01u);\n}",
        "case_ids": ["Func_1c865-0", "Func_1c865-1", "Func_1c865-2"],
    },
    "Func_1c866": {
        "source_symbol": "Func_1c866",
        "before": "if (keys & PAD_RIGHT)\n\t\tb--;",
        "after": "if (keys & PAD_RIGHT)\n\t\tb++;",
        "case_ids": ["Func_1c866-3", "Func_1c866-4"],
    },
    "Func_1c890": {
        "source_symbol": "Func_1c890",
        "before": "a = (uint8_t)(UpdateRNGSources() & SPRITE_ANIM_FLAG_X_INVERTED);",
        "after": "a = (uint8_t)(UpdateRNGSources() & SPRITE_ANIM_FLAG_CENTERED);",
        "case_ids": ["Func_1c890-1", "Func_1c890-3", "Func_1c890-4"],
    },
}
