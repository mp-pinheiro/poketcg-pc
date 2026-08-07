POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "EnableLCD": ("b", "c", "d", "e", "hl"),
    "DisableLCD": ("b", "c", "d", "e", "hl"),
    "Set_OBJ_8x8": ("b", "c", "d", "e", "hl"),
    "Set_OBJ_8x16": ("b", "c", "d", "e", "hl"),
    "SetWindowOn": ("b", "c", "d", "e", "hl"),
    "SetWindowOff": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "EnableLCD": [
        {"wram": {0xCABB: b"\0", 0xCABF: b"\0"}, "oracle": False,
         "why": "LCD registers are hardware IO outside the oracle snapshot",
         "expect": {0xCABB: b"\x80", 0xCABF: b"\xC0", 0xFF40: b"\x80"}},
        dict(POISON, wram={0xCABB: b"\x04", 0xCABF: b"\x55"}, oracle=False,
             why="LCD registers are hardware IO outside the oracle snapshot",
             expect={0xCABB: b"\x84", 0xCABF: b"\xC0", 0xFF40: b"\x84"}),
    ],
    "DisableLCD": [
        {"wram": {0xCABB: b"\x80", 0xCAB7: b"\xFF", 0xFF40: b"\x80", 0xFFFF: b"\xFF"}, "oracle": False,
         "why": "LCD registers are hardware IO outside the oracle snapshot",
         "expect": {0xCABB: b"\0", 0xCAB7: b"\xFF", 0xFF40: b"\0", 0xFFFF: b"\xFF", 0xFF47: b"\0", 0xFF48: b"\0", 0xFF49: b"\0"}},
        dict(POISON, wram={0xCABB: b"\0", 0xCAB7: b"\xA5", 0xFF40: b"\0", 0xFFFF: b"\xA5"}, oracle=False,
             why="LCD registers are hardware IO outside the oracle snapshot",
             expect={0xCABB: b"\0", 0xCAB7: b"\xA5"}),
    ],
    "Set_OBJ_8x8": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "Set_OBJ_8x16": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x80"}, read={0xCABB: 1})],
    "SetWindowOn": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "SetWindowOff": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x20"}, read={0xCABB: 1})],
}
