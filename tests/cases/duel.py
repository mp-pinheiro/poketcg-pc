POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "CopyPlayerName": ("a", "b", "c", "d", "e", "hl"),
    "CopyOpponentName": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "CopyPlayerName": [
        {"d": 0xC1, "e": 0x00, "sram": {0: {0xA010: b"\x21\x22\x00"}},
         "read": {0xC100: 3}},
        dict(POISON, d=0xC2, e=0x00,
             sram={2: {0xA010: b"\x31\x00"}}, read={0xC200: 2}),
    ],
    "CopyOpponentName": [
        {"d": 0xC1, "e": 0x00, "wram": {0xC500: b"\x41\x42\x00"},
         "read": {0xC100: 3}},
        dict(POISON, d=0xC2, e=0x00, wram={0xC500: b"\x51\x00"},
             read={0xC200: 2}),
    ],
}
