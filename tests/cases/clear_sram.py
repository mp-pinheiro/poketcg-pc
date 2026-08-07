"""Oracle-diff cases for poketcg/src/home/clear_sram.asm.

ValidateSRAM is not registered: both non-matching paths call InitSaveDataAndSetUppercase
(home/init.asm, unported), and the only clean path (signature $04,$21,$05 match) writes
no memory and yields only a carry flag -- not enough coverage to register.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ClearSRAMBank": ("a", "d", "e", "f"),
    "RestartSRAM": ("d", "e"),
}

SIG = b"\x04\x21\x05"

CASES = {
    "ClearSRAMBank": [
        {"a": 1, "sram": {0: {0xA000: b"\x11\x22"}, 1: {0xA000: b"\xaa\xbb\xcc"}}},
        {"a": 2, "sram": {2: {0xA000: b"\xde\xad"}}, "sread": {2: {0xBFFF: 1}}},
        {"a": 1, "sram": {1: {0xA000: b"\x01" * 8}}, "sread": {1: {0xBFFF: 1, 0xA800: 4}}},
        dict(POISON, a=3, sram={3: {0xA000: b"\x99\x88\x77\x66\x55\x44"}}),
    ],
    "RestartSRAM": [
        {"sram": {0: {0xA000: b"\xff" * 8}, 1: {0xA000: b"\xee" * 4},
                  2: {0xA000: b"\x01"}, 3: {0xA000: b"\x02"}},
         "sread": {0: {0xBFFF: 1}, 1: {0xBFFF: 1}, 2: {0xBFFF: 1}, 3: {0xBFFF: 1}}},
        dict(POISON, sram={0: {0xA000: b"\xaa\xbb\xcc"}, 3: {0xBFFF: b"\xff"}}),
    ],
}
