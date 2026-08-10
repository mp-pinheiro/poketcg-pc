POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
QUEUE = 0xD423
BUFFER = 0xD42C
CONTRACT = {
    "_ResetAnimationQueue": ("b", "c", "hl"),
    "PlayLoadedDuelAnimation": ("b", "c", "d", "e", "hl"),
    "LoadDuelAnimationToBuffer": ("a", "b", "c", "d", "e", "hl"),
    "_UpdateQueuedAnimations": ("a", "b", "c", "d", "e", "hl"),
    "ClearAndDisableQueuedAnimations": ("b", "c", "d", "e", "hl"),
}
CASES = {
    "_ResetAnimationQueue": [
        {"wram": {QUEUE: b"\x00" * 7, 0xD4AC: b"\x7f\x7f\x7f"}},
        dict(POISON, wram={QUEUE: b"\x01" * 7, 0xD4AC: b"\xaa\xbb\xcc"}),
    ],
    "PlayLoadedDuelAnimation": [
        {"wram": {0xCAD3: b"\xC5\x4A", 0xD422: b"\x00", 0xD421: b"\x00", 0xD4AD: b"\x00"}},
        dict(POISON, wram={0xCAD3: b"\xC5\x4A", 0xD422: b"\x01", 0xD421: b"\x00", 0xD4AD: b"\x08"},
             oracle=False, why="animation metadata and sprite/palette/SFX callees are outside this port",
             expect={0xD4BF: b"\x01"}),
        {"wram": {0xCAD3: b"\xC5\x4A", 0xD422: b"\x01", 0xD421: b"\x01", 0xD4AD: b"\x00"},
         "oracle": False, "why": "unskippable animation reaches sprite/palette/SFX callees",
         "expect": {0xD4BF: b"\x01"}},
    ],
    "LoadDuelAnimationToBuffer": [
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x00", 0xD422: b"\x01", 0xD4AE: b"\x02", 0xD4AF: b"\x01", 0xD4B0: b"\x05", 0xD4B1: b"4\x12", 0xD4B3: b"\x03", 0xD4BE: b"\x07"}, "read": {BUFFER: 8}},
        dict(POISON, wram={0xD4AC: b"\x08", 0xD4AD: b"\x78", 0xD422: b"\x02", 0xD4AE: b"\x00", 0xD4AF: b"\x00", 0xD4B0: b"\x00", 0xD4B1: b"\x01\x00", 0xD4B3: b"\x00", 0xD4BE: b"\x00"}, read={BUFFER + 0x78: 8}),
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x08"}, "read": {BUFFER: 8}},
    ],
    "_UpdateQueuedAnimations": [
        {"wram": {0xD42A: b"\xff", 0xD4C0: b"\xff",
                  0xD4DE: b"\xff", QUEUE: b"\x00\x01\x02\x03\x04\x05\x06"},
         "oracle": False,
         "why": "ROM dispatch reaches buffered animation playback and does not return within the oracle frame limit",
         "expect": {0xD4D0: b"\x00", QUEUE: b"\xff\x01\x02\x03\x04\x05\x06"},
         "expect_regs": {"a": 0}},
        dict(POISON, wram={0xD42A: b"\xff", 0xD4C0: b"\x80", 0xD51E: b"\xff",
                           QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             oracle=False,
             why="the $80 branch reaches buffered animation playback and does not return within the oracle frame limit",
             expect={0xD4C0: b"\xff", QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             expect_regs={"a": 0xff}),
    ],
    "ClearAndDisableQueuedAnimations": [
        {"wram": {0xCAD3: b"\xC5\x4A", 0xD42A: b"\xFF", QUEUE: b"\x00" * 7, 0xD4AC: b"\x01\x02"},
         "oracle": False, "why": "queued entries reach DisableCurSpriteAnim",
         "expect": {QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}},
        dict(POISON, wram={0xCAD3: b"\xC5\x4A", 0xD42A: b"\xFF", QUEUE: b"\x01\xff\x02\xff\x03\xff\x04", 0xD4AC: b"\xaa\xbb"},
             oracle=False, why="queued entries reach DisableCurSpriteAnim",
             expect={QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}),
        {"wram": {0xCAD3: b"\x01\x00", 0xD42A: b"\xFF", QUEUE: b"\x01" * 7, 0xD4AC: b"\x01\x02"}},
    ],
}
