"""Oracle-diff cases for poketcg/src/audio/sfx.asm's SFX engine."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SFX_PlaySFX": (),
    "SFX_UpdateSFX": (),
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
