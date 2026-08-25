"""Oracle-diff cases for poketcg/src/audio/sfx.asm's SFX engine."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SFX_PlaySFX": {"compare": (), "preserve": ()},
    "SFX_UpdateSFX": {"compare": (), "preserve": ()},
}

CASES = {
    "SFX_PlaySFX": [
        {"a": 0, "wram": {0xDE53: b"\x00"},
         "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}},
        dict(POISON, a=0, wram={0xDE53: b"\x00"},
             read={0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}),
        {"a": 96, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
         "wram": {0xDE53: b"\x00"},
         "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}},
        {"a": 1, "wram": {0xDE53: b"\x00"},
         "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1, 0xDE4B: 8, 0xDE2F: 1, 0xDE33: 1}},
    ],
    "SFX_UpdateSFX": [
        {"wram": {0xDD8C: b"\x00", 0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
         "read": {0xDE53: 1, 0xDD83: 1, 0xDD82: 1}},
        dict(POISON, wram={0xDD8C: b"\x00", 0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
             read={0xDE53: 1, 0xDD83: 1, 0xDD82: 1}),
        {"wram": {0xDD8C: b"\x02", 0xDE54: b"\xff", 0xDE53: b"\x01",
                  0xDE33: b"\x02\x00\x00\x00", 0xDE2F: b"\x00\x00\x00",
                  0xDE37: b"\x00\x00\x00\x00\x00\x00"},
         "read": {0xDE33: 1}},
        # Sfx_Cursor_Ch1 (0x44DF): env→pan→duty(0)→freq($7AC)→terminates.
        # wdd85 seeded 0xFF to prove pan preserves other channel bits.
        {"wram": {0xDD8C: b"\x01", 0xDE54: b"\xff", 0xDE53: b"\x01",
                  0xDD85: b"\xFF",
                  0xDE33: b"\x01\x00\x00\x00",
                  0xDE4B: b"\xDF\x44\x00\x00\x00\x00\x00\x00"},
         "read": {0xDD8C: 1, 0xDD85: 1, 0xDE2B: 1, 0xDE37: 2, 0xDE4B: 8}},
        dict(POISON, wram={0xDD8C: b"\x01", 0xDE54: b"\xff", 0xDE53: b"\x01",
                           0xDD85: b"\xFF",
                           0xDE33: b"\x01\x00\x00\x00",
                           0xDE4B: b"\xDF\x44\x00\x00\x00\x00\x00\x00"},
             read={0xDD8C: 1, 0xDD85: 1, 0xDE2B: 1, 0xDE37: 2, 0xDE4B: 8}),
        # sfx_end at ROM 0x4096 ($F0): clears channel bit in wdd8c.
        {"wram": {0xDD8C: b"\x01", 0xDE54: b"\xff", 0xDE53: b"\x01",
                  0xDE33: b"\x01\x00\x00\x00",
                  0xDE4B: b"\x96\x40\x00\x00\x00\x00\x00\x00"},
         "read": {0xDD8C: 1}},
    ],
}
# >>> factory Func_fc105
CONTRACT["Func_fc105"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e")}
CASES["Func_fc105"] = [
    {"wram": {0xDE4B: b"\x00\x00"}, "read": {0xDE4B: 2}},
    {"c": 1, "d": 0x12, "e": 0x34, "wram": {0xDE4D: b"\x00\x00"}, "read": {0xDE4D: 2}},
    {"c": 0x20, "d": 0xFF, "e": 0xFF, "wram": {0xDE8B: b"\x00\x00"}, "read": {0xDE8B: 2}},
    dict(POISON, b=0, c=0x10, wram={0xDE6B: b"\x00\x00"}, read={0xDE6B: 2}),
]
# <<< factory Func_fc105

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
_STACK = [0x2468]
# <<< factory-cases-statics

# >>> factory SFX_end
CONTRACT["SFX_end"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["SFX_end"] = [
    {"b": 0, "c": 0, "wram": {0xDD8C: b"\xFF"}, "stack": _STACK, "read": {0xDD8C: 1}},
    dict(POISON, b=0, c=1, wram={0xDD8C: b"\xFF"}, stack=_STACK, read={0xDD8C: 1}),
    {"b": 0, "c": 3, "wram": {0xDD8C: b"\x01"}, "stack": [0x1357], "read": {0xDD8C: 1}},
    dict(POISON, b=0, c=0xFF, wram={0xDD8C: b"\xFF"}, stack=[0xBEEF], read={0xDD8C: 1})
]
# <<< factory SFX_end

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SFX_PlaySFX": {
        "source_symbol": "SFX_PlaySFX",
        "before": "if (sfx_id >= max_sfx)",
        "after":  "if (sfx_id > max_sfx)",
        "case_ids": ["SFX_PlaySFX-0", "SFX_PlaySFX-1", "SFX_PlaySFX-2", "SFX_PlaySFX-3"],
    },
}
# >>> factory-mutation Func_fc105
MUTATIONS["Func_fc105"] = {
    "source_symbol": "Func_fc105",
    "before": "\tgb_write8(hl, (uint8_t)de);",
    "after": "\tgb_write8(hl, (uint8_t)(de >> 8));",
    "case_ids": ["Func_fc105-1", "Func_fc105-3"],
}
# <<< factory-mutation Func_fc105
# >>> factory-mutation SFX_end
MUTATIONS["SFX_end"] = {
    "source_symbol": "SFX_end",
    "before": "\twdd8c = (uint8_t)(wdd8c & mask);",
    "after": "\twdd8c = (uint8_t)(wdd8c | mask);",
    "case_ids": ["SFX_end-0", "SFX_end-1", "SFX_end-2", "SFX_end-3"]
}
# <<< factory-mutation SFX_end
