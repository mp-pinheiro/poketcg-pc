"""Oracle-diff cases for poketcg/src/engine/menus/config.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DrawConfigMenuCursor": {
        "compare": ("a", "d", "e", "f"),
        "preserve": ("a", "d", "e", "f"),
    },
}

CASES = {
    "DrawConfigMenuCursor": [
        {"a": 0, "c": 0, "read": {0x9800 + 6 * 32 + 5: 1}},
        dict(POISON, a=0x5A, c=1, wram={0xD119: b"\x02"},
             read={0x9800 + 12 * 32 + 15: 1}),
        {"a": 0x33, "c": 0, "wram": {0xD118: b"\x01"},
         "read": {0x9800 + 6 * 32 + 7: 1}},
        {"a": 0x44, "c": 0, "wram": {0xD118: b"\x04"},
         "read": {0x9800 + 6 * 32 + 13: 1}},
        {"a": 0x66, "c": 1, "wram": {0xD119: b"\x00"},
         "read": {0x9800 + 12 * 32 + 1: 1}},
        {"a": 0x77, "c": 1, "wram": {0xD119: b"\x01"},
         "read": {0x9800 + 12 * 32 + 7: 1}},
        {"a": 0x88, "c": 1, "wram": {0xD119: b"\x02"},
         "read": {0x9800 + 12 * 32 + 15: 1}},
        {"a": 0x99, "c": 2, "read": {0x9800 + 16 * 32 + 1: 1}},
    ],
}

# >>> factory GetConfigCursorPositions
CONTRACT["GetConfigCursorPositions"] = {"compare": ("d", "e"), "preserve": ("d", "e")}
CASES["GetConfigCursorPositions"] = [
    # All-zero: sTextSpeed 0 walks the whole table and stops at c==4.
    {"sram": {0: {0xA006: b"\x00", 0xA007: b"\x00", 0xA009: b"\x00"}},
     "wram": {0xD421: b"\x00"},
     "read": {0xD118: 1, 0xD119: 1}},
    # Poisoned entry registers: the routine takes no arguments; d/e must survive.
    dict(POISON,
         sram={0: {0xA006: b"\x06", 0xA007: b"\x00", 0xA009: b"\x01"}},
         wram={0xD421: b"\x01"},
         read={0xD118: 1, 0xD119: 1}),
    # sTextSpeed == TEXT_SPEED_1 (6): first compare already takes the match branch.
    {"sram": {0: {0xA006: b"\x06", 0xA009: b"\x00"}},
     "wram": {0xD421: b"\x00"}, "read": {0xD118: 1, 0xD119: 1}},
    # 5: above table[1]=4, below table[0]=6 -> c==1.
    {"sram": {0: {0xA006: b"\x05", 0xA009: b"\x00"}},
     "wram": {0xD421: b"\x00"}, "read": {0xD118: 1, 0xD119: 1}},
    # 4 -> c==1 exactly at the boundary (cp is >=).
    {"sram": {0: {0xA006: b"\x04", 0xA009: b"\x01"}},
     "wram": {0xD421: b"\x00"}, "read": {0xD118: 1, 0xD119: 1}},
    # 2 -> c==2, skip allowed + animations disabled -> index 3 -> setting 2.
    {"sram": {0: {0xA006: b"\x02", 0xA009: b"\x01"}},
     "wram": {0xD421: b"\x01"}, "read": {0xD118: 1, 0xD119: 1}},
    # 1 -> c==3, skip disallowed but animations disabled -> index 1 -> setting 0.
    {"sram": {0: {0xA006: b"\x01", 0xA009: b"\x00"}},
     "wram": {0xD421: b"\x01"}, "read": {0xD118: 1, 0xD119: 1}},
    # Only bit 0 of each flag counts: 0xFE has bit0 clear, 0xFF set.
    {"sram": {0: {0xA006: b"\xFF", 0xA009: b"\xFE"}},
     "wram": {0xD421: b"\xFF"}, "read": {0xD118: 1, 0xD119: 1}},
    # ramg False after seeding: only the routine's own EnableSRAM makes the
    # seeded SRAM bytes visible instead of open-bus $FF.
    {"ramg": False,
     "sram": {0: {0xA006: b"\x00", 0xA009: b"\x01"}},
     "wram": {0xD421: b"\x00"}, "read": {0xD118: 1, 0xD119: 1}},
]
# <<< factory GetConfigCursorPositions

# >>> factory SaveConfigSettings
CONTRACT["SaveConfigSettings"] = {"compare": ("d", "e"), "preserve": ("d", "e")}
CASES["SaveConfigSettings"] = [
    # All-zero: show-all animations, slowest text speed.
    {"wram": {0xD118: b"\x00", 0xD119: b"\x00", 0xD421: b"\x00", 0xCE47: b"\x00"},
     "sram": {0: {0xA006: b"\x00", 0xA007: b"\x00", 0xA009: b"\x00"}},
     "sread": {0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}},
    # Poisoned entry registers; cursor 1 = skip some, message speed index 4.
    dict(POISON,
         wram={0xD118: b"\x04", 0xD119: b"\x01", 0xD421: b"\xFF", 0xCE47: b"\xFF"},
         sram={0: {0xA006: b"\xFF", 0xA007: b"\xFF", 0xA009: b"\xFF"}},
         sread={0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}),
    # Cursor 2 = none: animations disabled TRUE and skip delay TRUE.
    {"wram": {0xD118: b"\x02", 0xD119: b"\x02", 0xD421: b"\x00", 0xCE47: b"\x00"},
     "sram": {0: {0xA006: b"\x00", 0xA007: b"\x00", 0xA009: b"\x00"}},
     "sread": {0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}},
    # Cursor 3 = unused entry: both FALSE.
    {"wram": {0xD118: b"\x03", 0xD119: b"\x03", 0xD421: b"\x01", 0xCE47: b"\x01"},
     "sram": {0: {0xA006: b"\x11", 0xA007: b"\x11", 0xA009: b"\x11"}},
     "sread": {0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}},
    # Only the low two bits of the animation cursor are used: 0xFE -> entry 2.
    {"wram": {0xD118: b"\x01", 0xD119: b"\xFE", 0xD421: b"\x00", 0xCE47: b"\x00"},
     "sram": {0: {0xA006: b"\x00", 0xA007: b"\x00", 0xA009: b"\x00"}},
     "sread": {0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}},
    # ramg False after seeding: only the routine's EnableSRAM lets the writes land.
    {"ramg": False,
     "wram": {0xD118: b"\x02", 0xD119: b"\x01", 0xD421: b"\x00", 0xCE47: b"\x00"},
     "sram": {0: {0xA006: b"\x00", 0xA007: b"\x00", 0xA009: b"\x00"}},
     "sread": {0: {0xA006: 1, 0xA007: 1, 0xA009: 1}}},
]
# <<< factory SaveConfigSettings

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawConfigMenuCursor": {
        "source_symbol": "DrawConfigMenuCursor",
        "before": "x = (uint8_t)(5u + (uint8_t)(cursor << 1));",
        "after": "x = (uint8_t)(5u + (uint8_t)(cursor << 1) + 1u);",
        "case_ids": ["DrawConfigMenuCursor-2", "DrawConfigMenuCursor-3"],
    },
}
# >>> factory-mutation GetConfigCursorPositions
MUTATIONS["GetConfigCursorPositions"] = {
    "source_symbol": "GetConfigCursorPositions",
    "before": "\t\tif (c >= 4u)",
    "after": "\t\tif (c >= 3u)",
    "case_ids": ["GetConfigCursorPositions-0", "GetConfigCursorPositions-8"],
}
# <<< factory-mutation GetConfigCursorPositions
# >>> factory-mutation SaveConfigSettings
MUTATIONS["SaveConfigSettings"] = {
    "source_symbol": "SaveConfigSettings",
    "before": "\tuint8_t c = (uint8_t)((wConfigDuelAnimationCursorPos & 0x03u) << 1);",
    "after": "\tuint8_t c = (uint8_t)((wConfigDuelAnimationCursorPos & 0x01u) << 1);",
    "case_ids": ["SaveConfigSettings-2", "SaveConfigSettings-4"],
}
# <<< factory-mutation SaveConfigSettings
