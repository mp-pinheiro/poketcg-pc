POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SPRITE_BUFFER = 0xD4D0
CACHE = 0xD5D8
CACHE_SIZE = 0xD618
W_WHICH_SPRITE = 0xD4CF
OAM = 0xCA00
OAM_OFFSET = 0xCAB5
OAM_TOGGLE = 0xCAC0
H_BANK = 0xFF80
CUR_ATTR = 0xD5D0
CUR_X = 0xD5D1
CUR_Y = 0xD5D2
CUR_TILE = 0xD5D3
CUR_EDGE = 0xD5D4
CUR_FRAME_BANK = 0xD5D6
WHICH_FRAME = 0xD4CA
TEMP_POINTER = 0xD4C4
TEMP_BANK = 0xD4C6
LOADED_FRAME = 0xD23E

CONTRACT = {
    "_ClearSpriteAnimations": ("b", "c", "d", "e", "hl"),
    "CreateSpriteAndAnimBufferEntry": ("f", "b", "c", "d", "e", "hl"),
    "FillNewSpriteAnimBufferEntry": ("b", "c", "d", "e", "hl"),
    "DisableCurSpriteAnim": ("b", "c", "d", "e", "hl"),
    "DisableSpriteAnim": ("b", "c", "d", "e", "hl"),
    "GetSpriteAnimCounter": ("a", "b", "c", "d", "e", "hl"),
    "_HandleAllSpriteAnimations": ("a", "f", "b", "c", "d", "e", "hl"),
    "LoadSpriteDataForAnimationFrame": ("b", "c", "hl"),
    "TryHandleSpriteAnimationFrame": ("b", "c", "d", "e", "hl"),
    "StartNewSpriteAnimation": ("b", "d", "e", "hl"),
    "StartSpriteAnimation": ("b", "c", "d", "e", "hl"),
    "Func_12ac9": ("b", "c", "d", "e", "hl"),
    "LoadSpriteAnimPointers": ("b", "c", "d", "e", "hl"),
    "HandleAnimationFrame": ("b", "c", "d", "e", "hl"),
    "GetAnimFramePointerFromOffset": ("b", "c", "d", "e", "hl"),
    "SetAnimationCounterAndLoop": ("f", "b", "c", "d", "e", "hl"),
    "Func_12ba7": ("b", "c", "d", "e", "hl"),
    "Func_12bcd": ("b", "c", "d", "e", "hl"),
    "ClearSpriteVRAMBuffer": ("b", "c", "d", "e", "hl"),
    "Func_12c05": ("a", "f", "b", "c", "d", "e", "hl"),
    "Func_12c4f": ("a", "b", "c", "d", "e", "hl"),
    "Func_12c5e": ("b", "c", "d", "e", "hl"),
}


def entry(base, enabled=1, anim=0, counter=1, frame_bank=0, frame_ptr=0,
          flags=0, x=0, y=0, tile=0, bank=4, anim_ptr=0xC200,
          offset_ptr=0xC300):
    data = bytearray(16)
    data[0] = enabled
    data[1] = 0
    data[2] = x
    data[3] = y
    data[4] = tile
    data[5] = anim
    data[6] = bank
    data[7:9] = anim_ptr.to_bytes(2, "little")
    data[9:11] = offset_ptr.to_bytes(2, "little")
    data[11] = frame_bank
    data[12:14] = frame_ptr.to_bytes(2, "little")
    data[14] = counter
    data[15] = flags
    return {base: bytes(data)}
def frame_fixture(base=0xC100, entry_base=SPRITE_BUFFER, frame_ptr=0xC300,
                   frame=(0, 1, 2, 3), flags=0, counter=1):
    state = entry(entry_base, counter=counter, flags=flags, offset_ptr=frame_ptr)
    state.update({base: bytes(frame), 0xC200: bytes((0, 0, 0)) + b"\x00" * 29,
                  0xC220: frame_ptr.to_bytes(2, "little"),
                  frame_ptr: bytes(frame),
                  H_BANK: b"\x04"})
    return state


CASES = {
    "_ClearSpriteAnimations": [
        {"wram": {SPRITE_BUFFER: b"\xff" * 256, CACHE: b"\xff" * 64,
                   CACHE_SIZE: b"\xff"}, "read": {SPRITE_BUFFER: 256, CACHE: 64,
                   CACHE_SIZE: 1, W_WHICH_SPRITE: 1, OAM: 160, OAM_OFFSET: 1,
                   OAM_TOGGLE: 1}},
        dict(POISON, wram={SPRITE_BUFFER: b"\xa5" * 256, CACHE: b"\xa5" * 64,
                           CACHE_SIZE: b"\xa5", 0xD5D7: b"\x01"},
             read={SPRITE_BUFFER: 256, CACHE: 64, CACHE_SIZE: 1, OAM: 160,
                   OAM_OFFSET: 1, OAM_TOGGLE: 1}),
        {"wram": {0xD5D7: b"\x01", SPRITE_BUFFER: b"\xaa" * 256,
                   CACHE: b"\xaa" * 64, CACHE_SIZE: b"\xaa"},
         "read": {SPRITE_BUFFER: 256, CACHE: 64, CACHE_SIZE: 1}},
    ],
    "CreateSpriteAndAnimBufferEntry": [
        {"a": 1, "f": 0, "wram": {H_BANK: b"\x04", CACHE_SIZE: b"\x00"},
         "read": {SPRITE_BUFFER: 16, CACHE_SIZE: 1}},
        dict(POISON, a=7, f=0, wram={H_BANK: b"\x04", CACHE_SIZE: b"\x00"},
             read={SPRITE_BUFFER: 16, CACHE_SIZE: 1}),
        {"a": 1, "f": 0xF0, "wram": {0xD5D7: b"\x01"}},
    ],
    "FillNewSpriteAnimBufferEntry": [
        {"hl": 0xC100, "wram": {0xC100: b"\xaa" * 16, CUR_TILE: b"\x12"},
         "read": {0xC0FF: 1, 0xC100: 16, 0xC110: 1}},
        dict(POISON, hl=0xC1F8, wram={0xC1F8: b"\x55" * 16, CUR_TILE: b"\x34"},
             read={0xC1F0: 8, 0xC1F8: 16, 0xC208: 1}),
    ],
    "DisableCurSpriteAnim": [
        {"wram": {W_WHICH_SPRITE: b"\x00", SPRITE_BUFFER: b"\x01"},
         "read": {SPRITE_BUFFER: 1}},
        dict(POISON, wram={W_WHICH_SPRITE: b"\xff", SPRITE_BUFFER + 15 * 16: b"\x01"},
             read={SPRITE_BUFFER + 15 * 16: 1}),
    ],
    "DisableSpriteAnim": [
        {"a": 0, "wram": {SPRITE_BUFFER: b"\x01"}, "read": {SPRITE_BUFFER: 1}},
        dict(POISON, a=0xff, wram={SPRITE_BUFFER + 15 * 16: b"\x01"},
             read={SPRITE_BUFFER + 15 * 16: 1}),
        {"a": 3, "wram": {0xD5D7: b"\x01", SPRITE_BUFFER + 48: b"\x01"},
         "read": {SPRITE_BUFFER + 48: 1}},
    ],
    "GetSpriteAnimCounter": [
        {"wram": {W_WHICH_SPRITE: b"\x00", SPRITE_BUFFER + 14: b"\x12"}},
        dict(POISON, wram={W_WHICH_SPRITE: b"\xff", SPRITE_BUFFER + 15 * 16 + 14: b"\x34"}),
    ],
    "_HandleAllSpriteAnimations": [
        {"wram": {SPRITE_BUFFER: b"\x00" * 256}, "read": {SPRITE_BUFFER: 256,
         OAM: 160, OAM_OFFSET: 1, OAM_TOGGLE: 1}},
        dict(POISON, wram={SPRITE_BUFFER: b"\x00" * 256},
             read={SPRITE_BUFFER: 256, OAM: 160, OAM_OFFSET: 1, OAM_TOGGLE: 1}),
        {"wram": {0xD5D7: b"\x01", SPRITE_BUFFER: b"\x11" * 256},
         "read": {SPRITE_BUFFER: 256, OAM_TOGGLE: 1}},
    ],
    "LoadSpriteDataForAnimationFrame": [
        {"hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, frame_bank=0, x=2, y=3, tile=4)}},
        dict(POISON, hl=SPRITE_BUFFER, wram={**entry(SPRITE_BUFFER, frame_bank=0, x=0xff, y=0, tile=9)}),
        {"hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, frame_bank=1, frame_ptr=0xC300),
         H_BANK: b"\x04", 0xC300: b"\x01\x00\x00\x01"},
         "read": {OAM: 160, OAM_OFFSET: 1, CUR_ATTR: 1, CUR_X: 1, CUR_Y: 1,
                  CUR_TILE: 1, CUR_FRAME_BANK: 1}},
    ],
    "TryHandleSpriteAnimationFrame": [
        {"hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, counter=0xff)},
         "read": {SPRITE_BUFFER + 14: 1}},
        {"hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, counter=1), **frame_fixture()},
         "read": {SPRITE_BUFFER: 16, LOADED_FRAME: 4}},
        dict(POISON, hl=SPRITE_BUFFER,
             wram={**entry(SPRITE_BUFFER, counter=2, flags=4), **frame_fixture()},
             read={SPRITE_BUFFER: 16, LOADED_FRAME: 4}),
    ],
    "StartNewSpriteAnimation": [
        {"a": 0, "wram": {SPRITE_BUFFER: bytes((1, 0)) + b"\x00" * 14}},
        dict(POISON, a=7, wram={SPRITE_BUFFER: bytes((1, 0)) + b"\x00" * 14,
             H_BANK: b"\x04", 0xC200: b"\x00" * 35, 0xC300: b"\x00\x01\x00\x00"},
             read={SPRITE_BUFFER: 16}),
    ],
    "StartSpriteAnimation": [
        {"a": 0, "wram": {H_BANK: b"\x04", SPRITE_BUFFER: bytes(16),
         0xC200: b"\x00" * 35, 0xC300: b"\x00\x01\x00\x00"}, "read": {SPRITE_BUFFER: 16}},
        dict(POISON, a=7, wram={H_BANK: b"\x04", SPRITE_BUFFER: bytes(16),
             0xC200: b"\x00" * 35, 0xC300: b"\x00\x01\xff\x01"}, read={SPRITE_BUFFER: 16}),
    ],
    "Func_12ac9": [
        {"a": 0, "c": 0, "wram": {H_BANK: b"\x04", SPRITE_BUFFER: bytes(16),
         0xC200: b"\x00" * 35, 0xC300: b"\x00\x01\x00\x00"}},
        dict(POISON, a=7, c=1, wram={H_BANK: b"\x04", SPRITE_BUFFER: bytes(16),
             0xC200: b"\x00" * 35, 0xC300: b"\xff\x01\x00\x00"}, read={SPRITE_BUFFER: 16}),
    ],
    "LoadSpriteAnimPointers": [
        {"a": 0, "wram": {H_BANK: b"\x04", W_WHICH_SPRITE: b"\x00"}, "read": {SPRITE_BUFFER: 16}},
        dict(POISON, a=7, wram={H_BANK: b"\x04", W_WHICH_SPRITE: b"\xff"},
             read={SPRITE_BUFFER + 15 * 16: 16, TEMP_POINTER: 3}),
    ],
    "HandleAnimationFrame": [
        {"hl": SPRITE_BUFFER, "wram": {**frame_fixture(), 0xC300: b"\x00\x01\x02\x03",
         0xC220: b"\x00\xC3"}, "read": {SPRITE_BUFFER: 16, LOADED_FRAME: 4, H_BANK: 1}},
        dict(POISON, hl=SPRITE_BUFFER, wram={**frame_fixture(frame=(0, 2, 0xff, 1), flags=3, counter=1),
             0xC300: b"\x00\x01\xff\x01", 0xC220: b"\x00\xC3"},
             read={SPRITE_BUFFER: 16, LOADED_FRAME: 4, H_BANK: 1}),
    ],
    "GetAnimFramePointerFromOffset": [
        {"a": 0, "hl": SPRITE_BUFFER,
         "wram": {**entry(SPRITE_BUFFER, bank=1, anim_ptr=0xC300),
                  H_BANK: b"\x04", 0xC300: bytes((0, 0x80, 0xC3)),
                  0xC380: b"\xab\xcd"},
         "read": {WHICH_FRAME: 1, TEMP_POINTER: 3, SPRITE_BUFFER + 11: 3}},
        dict(POISON, a=0xff, hl=SPRITE_BUFFER + 15 * 16,
             wram={**entry(SPRITE_BUFFER + 15 * 16, bank=1, anim_ptr=0xC300),
                   H_BANK: b"\x04", 0xC300: bytes((0, 0x80, 0xC3)), 0xC380: b"\x11\x22"},
             read={WHICH_FRAME: 1, SPRITE_BUFFER + 15 * 16 + 11: 3}),
    ],
    "SetAnimationCounterAndLoop": [
        {"a": 0, "hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, counter=0, anim_ptr=0xC2FD)},
         "read": {SPRITE_BUFFER + 9: 2, SPRITE_BUFFER + 14: 1}},
        dict(POISON, a=1, hl=SPRITE_BUFFER + 15 * 16, wram={**entry(SPRITE_BUFFER + 15 * 16, counter=0)},
             read={SPRITE_BUFFER + 15 * 16 + 14: 1}),
        {"a": 0xff, "hl": SPRITE_BUFFER, "wram": {**entry(SPRITE_BUFFER, counter=0)}},
    ],
    "Func_12ba7": [
        {"ramg": False, "wram": {SPRITE_BUFFER: bytes(range(256)), CACHE: bytes(range(64)), CACHE_SIZE: b"\x10"},
         "sread": {0: {0xB900: 321}}},
        dict(POISON, ramg=False, wram={SPRITE_BUFFER: b"\xa5" * 256, CACHE: b"\x5a" * 64,
             CACHE_SIZE: b"\xff"}, sread={2: {0xB900: 321}}),
    ],
    "Func_12bcd": [
        {"ramg": False, "sram": {0: {0xB900: bytes(range(256)) + bytes(range(64)) + b"\x10"}},
         "read": {SPRITE_BUFFER: 256, CACHE: 64, CACHE_SIZE: 1}},
        dict(POISON, ramg=False, sram={1: {0xB900: b"\x5a" * 321}},
             read={SPRITE_BUFFER: 256, CACHE: 64, CACHE_SIZE: 1}),
    ],
    "ClearSpriteVRAMBuffer": [
        {"wram": {CACHE: b"\xff" * 64, CACHE_SIZE: b"\xff"}, "read": {CACHE: 64, CACHE_SIZE: 1}},
        dict(POISON, wram={CACHE: b"\xaa" * 64, CACHE_SIZE: b"\xaa"}, read={CACHE: 64, CACHE_SIZE: 1}),
    ],
    "Func_12c05": [
        {"a": 0, "wram": {CACHE_SIZE: b"\x00", H_BANK: b"\x04"},
         "read": {CACHE: 64, CACHE_SIZE: 1}},
        {"a": 7, "wram": {H_BANK: b"\x04", CACHE_SIZE: b"\x01",
         CACHE: bytes((1, 7, 0, 2)) + b"\x00" * 60},
         "read": {CACHE: 64, CACHE_SIZE: 1}},
        dict(POISON, a=7, wram={H_BANK: b"\x04", CACHE_SIZE: b"\x01",
             CACHE: bytes((0xff, 7, 0, 2)) + b"\x00" * 60},
             read={CACHE: 4, CACHE_SIZE: 1}),
        {"a": 7, "wram": {H_BANK: b"\x04", CACHE_SIZE: b"\x10",
         CACHE: b"\x00" * 64}, "read": {CACHE_SIZE: 1}},
    ],
    "Func_12c4f": [
        {"a": 0, "d": 0, "wram": {H_BANK: b"\x04"}, "read": {H_BANK: 1}},
        dict(POISON, a=7, d=0x7f, wram={H_BANK: b"\x04"}, read={H_BANK: 1}),
        {"a": 0, "d": 0x80, "wram": {H_BANK: b"\x04"}, "read": {H_BANK: 1}},
    ],
    "Func_12c5e": [
        {"wram": {H_BANK: b"\x04", CACHE: bytes((1, 0, 0, 1)) + b"\x00" * 60},
         "read": {CACHE: 64, H_BANK: 1}, "vread": {0: {0x8000: 16}}},
        dict(POISON, wram={H_BANK: b"\x04", CACHE: b"\x00" * 60 + bytes((1, 7, 0x7f, 1))},
             read={CACHE: 64, H_BANK: 1}, vread={1: {0x87f0: 16}}),
    ],
}
