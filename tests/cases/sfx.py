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

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
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

# >>> factory SFX_frequency
CONTRACT["SFX_frequency"] = {"compare": (), "preserve": ()}
CASES["SFX_frequency"] = [
    {"stack": [0], "wram": {0xDE37: b"\x00\x00", 0xDE2B: b"\x00"}, "hram": {0xFF11: b"\x00"}, "read": {0xDE4B: 2}},
    {"a": 0x12, "c": 0, "stack": [0xC500], "wram": {0xC500: b"\x34", 0xDE37: b"\x78\x56", 0xDE2B: b"\x20"}, "hram": {0xFF11: b"\xC0"}, "read": {0xDE4B: 2}},
    {"a": 0xAB, "c": 3, "stack": [0xC510], "wram": {0xC510: b"\x41", 0xDE3D: b"\x49\x00", 0xDE2E: b"\x10"}, "hram": {0xFF20: b"\x80"}, "read": {0xDE4B: 2}},
    dict(POISON, stack=[0x1234], read={0xDE4B: 2})
]
# <<< factory SFX_frequency

# >>> factory ExecuteNextSFXCommand
CONTRACT["ExecuteNextSFXCommand"] = {"compare": (), "preserve": ()}
CASES["ExecuteNextSFXCommand"] = [
    {"hl": 0xC100, "c": 0, "wram": {0xC100: b"\xF0", 0xDD8C: b"\xFF"},
     "read": {0xDD8C: 1}, "hram": {0xFF12: b"\x00", 0xFF14: b"\x00"}},
    dict(POISON, b=0, c=1, hl=0xC100, wram={0xC100: b"\xF0", 0xDD8C: b"\xFF"},
         read={0xDD8C: 1}, hram={0xFF17: b"\x00", 0xFF19: b"\x00"}),
    {"hl": 0xC100, "c": 0,
     "wram": {0xC100: b"\x01\x23", 0xDE37: b"\x00\x00", 0xDE2B: b"\x20"},
     "read": {0xDE4B: 2, 0xDE37: 2, 0xDE2B: 1},
     "hram": {0xFF11: b"\xC0", 0xFF13: b"\x00", 0xFF14: b"\x00"}},
    {"hl": 0xC100, "c": 1, "wram": {0xC100: b"\x27\xF0", 0xDD8C: b"\xFF"},
     "read": {0xDD8C: 1},
     "hram": {0xFF16: b"\x00", 0xFF17: b"\x00", 0xFF19: b"\x00"}},
    {"hl": 0xC100, "c": 3,
     "wram": {0xC100: b"\x08\x88", 0xDE3D: b"\x00\x00", 0xDE2E: b"\x00"},
     "read": {0xDE51: 2, 0xDE3D: 2, 0xDE2E: 1},
     "hram": {0xFF20: b"\x00", 0xFF22: b"\x00", 0xFF23: b"\x00"}},
    {"hl": 0xC100, "c": 2,
     "wram": {0xC100: b"\x10\xAB\xF0", 0xDD8C: b"\xFF"},
     "read": {0xDE2D: 1, 0xDD8C: 1},
     "hram": {0xFF1C: b"\x00", 0xFF1E: b"\x00"}},
]
# <<< factory ExecuteNextSFXCommand

# >>> factory SFX_loop
CONTRACT["SFX_loop"] = {"compare": (), "preserve": ()}
CASES["SFX_loop"] = [
    {"b": 0, "c": 0, "stack": [0xC400], "wram": {0xC400: b"\x12\xF0"}, "read": {0xDE43: 2, 0xDE3F: 1}},
    {"b": 0, "c": 1, "stack": [0xC400], "wram": {0xC400: b"\x34\xF0"}, "read": {0xDE45: 2, 0xDE40: 1}},
    {"b": 0, "c": 3, "stack": [0xC400], "wram": {0xC400: b"\x56\xF0"}, "read": {0xDE49: 2, 0xDE42: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "stack": [0xC400], "wram": {0xC400: b"\x78\xF0"}, "read": {0xDE43: 2, 0xDE3F: 1}},
]
# <<< factory SFX_loop

# >>> factory SFX_pan
CONTRACT["SFX_pan"] = {"compare": (), "preserve": ()}
CASES["SFX_pan"] = [
    {"b": 0, "c": 0, "stack": [0xC100], "wram": {0xC100: b"\xF0", 0xDD85: b"\xFF", 0xDD8C: b"\xFF"}, "read": {0xDD85: 1, 0xDD8C: 1}},
    {"b": 0, "c": 1, "stack": [0xC200], "wram": {0xC200: b"\xF0", 0xDD85: b"\xFF", 0xDD8C: b"\xFF"}, "read": {0xDD85: 1, 0xDD8C: 1}},
    {"b": 0, "c": 3, "stack": [0xC300], "wram": {0xC300: b"\xF0", 0xDD85: b"\xFF", 0xDD8C: b"\xFF"}, "read": {0xDD85: 1, 0xDD8C: 1}},
    dict(POISON, b=0, c=2, stack=[0xC400], wram={0xC400: b"\xF0", 0xDD85: b"\xFF", 0xDD8C: b"\xFF"}, read={0xDD85: 1, 0xDD8C: 1}),
]
# <<< factory SFX_pan

# >>> factory SFX_unused
CONTRACT["SFX_unused"] = {"compare": (), "preserve": ()}
CASES["SFX_unused"] = [
    {"c": 0, "hl": 0xC100, "wram": {0xC100: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    {"c": 1, "hl": 0xC100, "wram": {0xC100: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    {"c": 3, "hl": 0xC100, "wram": {0xC100: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    dict(POISON, b=0, c=2, hl=0xC100, wram={0xC100: b"\xF0", 0xDD8C: b"\xFF"}, read={0xDD8C: 1}),
]
# <<< factory SFX_unused

# >>> factory SFX_pitch_offset
CONTRACT["SFX_pitch_offset"] = {"compare": (), "preserve": ()}
CASES["SFX_pitch_offset"] = [
    {"b": 0, "c": 0, "stack": [0xC100], "wram": {0xC100: b"\x12\xF0"}, "read": {0xDE2F: 1}},
    {"b": 0, "c": 1, "stack": [0xC200], "wram": {0xC200: b"\x34\xF0"}, "read": {0xDE30: 1}},
    dict(POISON, b=0, c=2, stack=[0xC300], wram={0xC300: b"\x56\xF0"}, read={0xDE31: 1}),
]
# <<< factory SFX_pitch_offset

# >>> factory SFX_wave
CONTRACT["SFX_wave"] = {"compare": (), "preserve": ()}
CASES["SFX_wave"] = [
    {"a": 0, "b": 0, "c": 0, "stack": [0xC100], "wram": {0xC100: b"\xF0"}, "read": {0xDD8B: 1}},
    {"a": 1, "b": 0, "c": 0, "stack": [0xC200], "wram": {0xC200: b"\xF0"}, "read": {0xDD8B: 1}},
    dict(POISON, b=0, c=0, stack=[0xC300], wram={0xC300: b"\xF0"}, read={0xDD8B: 1}),
]
# <<< factory SFX_wave

# >>> factory SFX_duty
CONTRACT["SFX_duty"] = {"compare": (), "preserve": ()}
CASES["SFX_duty"] = [
    {"a": 0x12, "c": 0, "stack": [0xC100], "wram": {0xC100: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    {"a": 0xAB, "c": 1, "stack": [0xC200], "wram": {0xC200: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    {"a": 0x5E, "c": 3, "stack": [0xC400], "wram": {0xC400: b"\xF0", 0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    dict(POISON, stack=[0xC300], wram={0xC300: b"\xF0", 0xDD8C: b"\xFF"}, read={0xDD8C: 1}),
]
# <<< factory SFX_duty

# >>> factory SFX_envelope
CONTRACT["SFX_envelope"] = {"compare": (), "preserve": ()}
CASES["SFX_envelope"] = [
    {"b": 0x00, "c": 0x00, "stack": [0xC100], "wram": {0xC100: b"\x40\xF0"}, "read": {0xDE2B: 1}},
    {"b": 0x00, "c": 0x01, "stack": [0xC200], "wram": {0xC200: b"\x55\xF0"}, "read": {0xDE2C: 1}},
    {"b": 0x00, "c": 0x03, "stack": [0xC300], "wram": {0xC300: b"\xA5\xF0"}, "read": {0xDE2E: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "stack": [0xC400], "wram": {0xC400: b"\xF0\xF0"}, "read": {0xDEF7: 1}}
]
# <<< factory SFX_envelope

# >>> factory SFX_endloop
CONTRACT["SFX_endloop"] = {"compare": (), "preserve": ()}
CASES["SFX_endloop"] = [
    {"b": 0, "c": 0, "stack": [0xC100], "wram": {0xC100: b"\xF0", 0xDE3F: b"\x01"}, "read": {0xDE3F: 1}},
    {"b": 0, "c": 1, "stack": [0xC100], "wram": {0xC100: b"\xF0", 0xDE40: b"\x02", 0xDE45: b"\x00\xC2", 0xC200: b"\xF0"}, "read": {0xDE40: 1}},
    dict(POISON, b=0, c=0, stack=[0xC300], wram={0xC300: b"\xF0", 0xDE3F: b"\x01"}, read={0xDE3F: 1}),
]
# <<< factory SFX_endloop

# >>> factory SFX_Play
# `SFX_PlaySFX: jp SFX_Play`, so the body is entered identically and these
# mirror the trampoline's cases.
CONTRACT["SFX_Play"] = {"compare": (), "preserve": ()}
CASES["SFX_Play"] = [
    {"a": 0, "wram": {0xDE53: b"\x00"},
     "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}},
    dict(POISON, a=0, wram={0xDE53: b"\x00"},
         read={0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}),
    {"a": 96, "wram": {0xDE53: b"\x00"},
     "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1}},
    {"a": 1, "wram": {0xDE53: b"\x00"},
     "read": {0xDE53: 1, 0xDD8C: 1, 0xDE54: 1, 0xDE4B: 8, 0xDE2F: 1, 0xDE33: 1}},
]
# <<< factory SFX_Play

# >>> factory SFX_Update
CONTRACT["SFX_Update"] = {"compare": (), "preserve": ()}
CASES["SFX_Update"] = [
    {"wram": {0xDD8C: b"\x00", 0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
     "read": {0xDE53: 1, 0xDD83: 1, 0xDD82: 1}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
         read={0xDE53: 1, 0xDD83: 1, 0xDD82: 1}),
    {"wram": {0xDD8C: b"\x01", 0xDE54: b"\xff", 0xDE53: b"\x01",
              0xDD85: b"\xFF",
              0xDE33: b"\x01\x00\x00\x00",
              0xDE4B: b"\xDF\x44\x00\x00\x00\x00\x00\x00"},
     "read": {0xDD8C: 1, 0xDD85: 1, 0xDE2B: 1, 0xDE37: 2, 0xDE4B: 8}},
    {"wram": {0xDD8C: b"\x01", 0xDE54: b"\xff", 0xDE53: b"\x01",
              0xDE33: b"\x01\x00\x00\x00",
              0xDE4B: b"\x96\x40\x00\x00\x00\x00\x00\x00"},
     "read": {0xDD8C: 1}},
]
# <<< factory SFX_Update

# >>> factory Func_fc26c
CONTRACT["Func_fc26c"] = {"compare": (), "preserve": ()}
CASES["Func_fc26c"] = [
    {"wram": {0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
     "read": {0xDE53: 1, 0xDD83: 1, 0xDD82: 1}},
    {"wram": {0xDE53: b"\xFF", 0xDD83: b"\xFF", 0xDD82: b"\xFF"},
     "read": {0xDE53: 1, 0xDD83: 1, 0xDD82: 1}},
    dict(POISON, wram={0xDE53: b"\x01", 0xDD83: b"\x05", 0xDD82: b"\x04"},
         read={0xDE53: 1, 0xDD83: 1, 0xDD82: 1}),
]
# <<< factory Func_fc26c

# >>> factory Func_fc279
# The asm's register loads are a documented ROM bug (reads, not writes), so
# clearing wdd8c is the only surviving effect.
CONTRACT["Func_fc279"] = {"compare": (), "preserve": ()}
CASES["Func_fc279"] = [
    {"wram": {0xDD8C: b"\x01"}, "read": {0xDD8C: 1}},
    {"wram": {0xDD8C: b"\xFF"}, "read": {0xDD8C: 1}},
    dict(POISON, wram={0xDD8C: b"\x0F"}, read={0xDD8C: 1}),
]
# <<< factory Func_fc279

# >>> factory SFX_wait
CONTRACT["SFX_wait"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c")}
CASES["SFX_wait"] = [
    {"stack": [0xC100], "wram": {0xC100: b"\x42", 0xDE33: b"\x00"}, "read": {0xDE33: 1, 0xDE4B: 2}},
    {"c": 1, "stack": [0xC110], "wram": {0xC110: b"\x37", 0xDE34: b"\x00"}, "read": {0xDE34: 1, 0xDE4D: 2}},
    {"c": 3, "stack": [0xC120], "wram": {0xC120: b"\x7E", 0xDE32: b"\x00", 0xDE36: b"\x00"}, "read": {0xDE36: 1, 0xDE51: 2}},
    dict(POISON, stack=[0xC130], wram={0xC130: b"\x55"}),
]
# <<< factory SFX_wait

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
# >>> factory-mutation SFX_frequency
MUTATIONS["SFX_frequency"] = {"source_symbol": "SFX_frequency", "before": "\tuint16_t de = caller_hl;", "after": "\tuint16_t de = (uint16_t)(caller_hl + 2u);", "case_ids": ["SFX_frequency-0", "SFX_frequency-1", "SFX_frequency-2"]}
# <<< factory-mutation SFX_frequency
# >>> factory-mutation ExecuteNextSFXCommand
MUTATIONS["ExecuteNextSFXCommand"] = {
    "source_symbol": "ExecuteNextSFXCommand",
    "before": "\t\tcase 15u:",
    "after": "\t\tcase 14u:",
    "case_ids": ["ExecuteNextSFXCommand-0", "ExecuteNextSFXCommand-1",
                 "ExecuteNextSFXCommand-3"],
}
# <<< factory-mutation ExecuteNextSFXCommand
# >>> factory-mutation SFX_loop
MUTATIONS["SFX_loop"] = {"source_symbol": "SFX_loop", "before": "void SFX_loop(uint16_t bc, uint16_t caller_de)\n{\n\tuint16_t store_addr = (uint16_t)(wde43_ADDR + bc + bc);", "after": "void SFX_loop(uint16_t bc, uint16_t caller_de)\n{\n\tuint16_t store_addr = (uint16_t)(wde43_ADDR + bc + bc + 1u);", "case_ids": ["SFX_loop-0", "SFX_loop-1", "SFX_loop-2"]}
# <<< factory-mutation SFX_loop
# >>> factory-mutation SFX_pan
MUTATIONS["SFX_pan"] = {"source_symbol": "SFX_pan", "before": "void SFX_pan(uint16_t bc, uint16_t caller_hl)\n{\n\tuint8_t pan_val = gb_read8(caller_hl);", "after": "void SFX_pan(uint16_t bc, uint16_t caller_hl)\n{\n\tuint8_t pan_val = 0u;", "case_ids": ["SFX_pan-0", "SFX_pan-1", "SFX_pan-2", "SFX_pan-3"]}
# <<< factory-mutation SFX_pan
# >>> factory-mutation SFX_unused
MUTATIONS["SFX_unused"] = {"source_symbol": "SFX_unused", "before": "void SFX_unused(uint16_t hl, uint16_t bc)\n{\n\tExecuteNextSFXCommand(hl, bc);", "after": "void SFX_unused(uint16_t hl, uint16_t bc)\n{\n\tExecuteNextSFXCommand(hl, (uint16_t)(bc + 1u));", "case_ids": ["SFX_unused-0", "SFX_unused-1", "SFX_unused-2", "SFX_unused-3"]}
# <<< factory-mutation SFX_unused
# >>> factory-mutation SFX_pitch_offset
MUTATIONS["SFX_pitch_offset"] = {"source_symbol": "SFX_pitch_offset", "before": "\tgb_write8((uint16_t)(wSFXPitchOffsets_ADDR + bc), gb_read8(caller_hl));", "after": "\tgb_write8((uint16_t)(wSFXPitchOffsets_ADDR + bc), 0u);", "case_ids": ["SFX_pitch_offset-0", "SFX_pitch_offset-1", "SFX_pitch_offset-2"]}
# <<< factory-mutation SFX_pitch_offset
# >>> factory-mutation SFX_wave
MUTATIONS["SFX_wave"] = {"source_symbol": "SFX_wave", "before": "void SFX_wave(uint8_t a, uint16_t bc, uint16_t caller_hl)\n{\n\tuint16_t table_addr = (uint16_t)(SFX_WaveInstruments_ADDR + (uint16_t)a * 2u);\n\tconst uint8_t *table = rom_ptr(SFX_BANK, table_addr);\n\tuint16_t wave_addr = (uint16_t)table[0] | (uint16_t)((uint16_t)table[1] << 8u);\n\tconst uint8_t *wave = rom_ptr(SFX_BANK, wave_addr);\n\tgb_write8(0xFF1Au, 0u);\n\tfor (uint8_t i = 0u; i < AUD3WAVE_SIZE; i++)\n\t\tgb_write8((uint16_t)(AUD3WAVERAM + i), wave[i]);\n\twMusicWaveChange = 1u;", "after": "void SFX_wave(uint8_t a, uint16_t bc, uint16_t caller_hl)\n{\n\tuint16_t table_addr = (uint16_t)(SFX_WaveInstruments_ADDR + (uint16_t)a * 2u);\n\tconst uint8_t *table = rom_ptr(SFX_BANK, table_addr);\n\tuint16_t wave_addr = (uint16_t)table[0] | (uint16_t)((uint16_t)table[1] << 8u);\n\tconst uint8_t *wave = rom_ptr(SFX_BANK, wave_addr);\n\tgb_write8(0xFF1Au, 0u);\n\tfor (uint8_t i = 0u; i < AUD3WAVE_SIZE; i++)\n\t\tgb_write8((uint16_t)(AUD3WAVERAM + i), wave[i]);\n\twMusicWaveChange = 0u;", "case_ids": ["SFX_wave-0", "SFX_wave-1", "SFX_wave-2"]}
# <<< factory-mutation SFX_wave
# >>> factory-mutation SFX_duty
MUTATIONS["SFX_duty"] = {"source_symbol": "SFX_duty", "before": "void SFX_duty(uint8_t a, uint16_t bc, uint16_t caller_hl)\n{\n\tSFX_Duty((uint8_t)bc, a);\n\tExecuteNextSFXCommand(caller_hl, bc);", "after": "void SFX_duty(uint8_t a, uint16_t bc, uint16_t caller_hl)\n{\n\tSFX_Duty((uint8_t)bc, a);\n\tExecuteNextSFXCommand(caller_hl, (uint16_t)(bc + 1u));", "case_ids": ["SFX_duty-0", "SFX_duty-1", "SFX_duty-2", "SFX_duty-3"]}
# <<< factory-mutation SFX_duty
# >>> factory-mutation SFX_envelope
MUTATIONS["SFX_envelope"] = {"source_symbol": "SFX_envelope", "before": "void SFX_envelope(uint16_t bc, uint16_t caller_hl)\n{\n\tuint16_t store_addr = (uint16_t)(wde2b_ADDR + bc);", "after": "void SFX_envelope(uint16_t bc, uint16_t caller_hl)\n{\n\tuint16_t store_addr = (uint16_t)(wde2b_ADDR + bc + 1u);", "case_ids": ["SFX_envelope-0", "SFX_envelope-1", "SFX_envelope-2", "SFX_envelope-3"]}
# <<< factory-mutation SFX_envelope
# >>> factory-mutation SFX_endloop
MUTATIONS["SFX_endloop"] = {"source_symbol": "SFX_endloop", "before": "void SFX_endloop(uint16_t bc, uint16_t caller_word)\n{\n\tuint8_t count = gb_read8((uint16_t)(wde3f_ADDR + bc));\n\tcount = (uint8_t)(count - 1u);", "after": "void SFX_endloop(uint16_t bc, uint16_t caller_word)\n{\n\tuint8_t count = gb_read8((uint16_t)(wde3f_ADDR + bc));\n\tcount = (uint8_t)(count - 2u);", "case_ids": ["SFX_endloop-0", "SFX_endloop-1", "SFX_endloop-2"]}
# <<< factory-mutation SFX_endloop
# >>> factory-mutation SFX_Play
MUTATIONS["SFX_Play"] = {"source_symbol": "SFX_Play", "before": "\tuint16_t offset = (uint16_t)sfx_id * 2u;", "after": "\tuint16_t offset = (uint16_t)sfx_id * 3u;", "case_ids": ["SFX_Play-3"]}
# <<< factory-mutation SFX_Play
# >>> factory-mutation SFX_Update
MUTATIONS["SFX_Update"] = {"source_symbol": "SFX_Update", "before": "\twde54 = wdd8c;", "after": "\twde54 = (uint8_t)(wdd8c ^ 1u);", "case_ids": ["SFX_Update-2", "SFX_Update-3"]}
# <<< factory-mutation SFX_Update
# >>> factory-mutation Func_fc26c
MUTATIONS["Func_fc26c"] = {"source_symbol": "Func_fc26c", "before": "\twCurSfxID = 0x80;", "after": "\twCurSfxID = 0x81;", "case_ids": ["Func_fc26c-0", "Func_fc26c-1"]}
# <<< factory-mutation Func_fc26c
# >>> factory-mutation Func_fc279
MUTATIONS["Func_fc279"] = {"source_symbol": "Func_fc279", "before": "\tgb_read8(rAUD4GO);\n\twdd8c = 0;", "after": "\tgb_read8(rAUD4GO);\n\twdd8c = 1;", "case_ids": ["Func_fc279-0", "Func_fc279-1"]}
# <<< factory-mutation Func_fc279
# >>> factory-mutation SFX_wait
MUTATIONS["SFX_wait"] = {"source_symbol": "SFX_wait", "before": "\tgb_write8((uint16_t)(wde33_ADDR + bc), wait_val);", "after": "\tgb_write8((uint16_t)(wde33_ADDR + bc + 1u), wait_val);", "case_ids": ["SFX_wait-0", "SFX_wait-1", "SFX_wait-2"]}
# <<< factory-mutation SFX_wait
