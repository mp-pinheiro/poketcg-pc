POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DoAFrames": ("b", "c", "d", "e", "hl"),
    "DoFrame": ("b", "c", "d", "e", "hl"),
    "HandleDPadRepeat": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "DoAFrames": [
        {"a": 0, "wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, a=1, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
    ],
    "DoFrame": [
        {"wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
    ],
    "HandleDPadRepeat": [
        {"wram": {0xFF8D: b"\0\0\0\0\0"}, "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\0\0\0\0\0"}, read={0xFF8D: 5}),
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x01"}, "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\xF0\x00\x00\x00\x00"}, "read": {0xFF8D: 5}},
    ],
}
