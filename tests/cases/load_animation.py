POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_WHICH_SPRITE = 0xD4CF
SPRITE_BUFFER = 0xD4D0

CONTRACT = {
    "GetFirstSpriteAnimBufferProperty": ("b", "c", "d", "e", "hl"),
    "GetSpriteAnimBufferProperty": ("b", "c", "d", "e", "hl"),
    "GetSpriteAnimBufferProperty_SpriteInA": ("b", "c", "d", "e", "hl"),
    "Func_3ddb": ("b", "c", "d", "e", "hl"),
    "Func_3de7": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "GetFirstSpriteAnimBufferProperty": [
        {"c": 0},
        dict(POISON, c=15),
    ],
    "GetSpriteAnimBufferProperty": [
        {"c": 0, "wram": {W_WHICH_SPRITE: b"\x00"}},
        dict(POISON, c=7, wram={W_WHICH_SPRITE: b"\x03"}),
        {"c": 15, "wram": {W_WHICH_SPRITE: b"\xff"}},
    ],
    "GetSpriteAnimBufferProperty_SpriteInA": [
        {"a": 0, "c": 0},
        dict(POISON, a=3, c=7),
        {"a": 15, "c": 15},
        {"a": 16, "c": 0},
        {"a": 255, "c": 15},
    ],
    "Func_3ddb": [
        {"a": 0, "wram": {SPRITE_BUFFER + 15: b"\xff"},
         "read": {SPRITE_BUFFER + 15: 1}},
        dict(POISON, a=3, wram={SPRITE_BUFFER + 3 * 16 + 15: b"\x04"},
             read={SPRITE_BUFFER + 3 * 16 + 15: 1}),
    ],
    "Func_3de7": [
        {"a": 0, "wram": {SPRITE_BUFFER + 15: b"\x00"},
         "read": {SPRITE_BUFFER + 15: 1}},
        dict(POISON, a=15, wram={SPRITE_BUFFER + 15 * 16 + 15: b"\x01"},
             read={SPRITE_BUFFER + 15 * 16 + 15: 1}),
    ],
# The remaining exports are intentionally unregistered: ClearSpriteAnimations,
# HandleAllSpriteAnimations, DrawSpriteAnimationFrame, GetAnimationFramePointer,
# LoadScene, DrawPlayerPortrait, DrawPortrait, DrawOpponentPortrait, and Func_3e31
# farcall unported engine/gfx/scene code or consume banked animation-frame tables.
# They are not made into no-op adapters.
}
