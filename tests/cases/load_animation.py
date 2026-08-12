POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_WHICH_SPRITE = 0xD4CF
SPRITE_BUFFER = 0xD4D0

hBankROM = 0xFF80
wCurrSpriteAttributes = 0xD5D0
wCurrSpriteXPos = 0xD5D1
wCurrSpriteYPos = 0xD5D2
wCurrSpriteTileID = 0xD5D3
wCurrSpriteRightEdgeCheck = 0xD5D4
wCurrSpriteFrameBank = 0xD5D6
wOAM = 0xCA00
wOAMOffset = 0xCAB5
wWhichAnimationFrame = 0xD4CA
wTempPointer = 0xD4C4


def wtemp_seed(bank, addr, tail=b""):
    """wTempPointer/+1 (addr) + wTempPointerBank (bank), contiguous in WRAM."""
    return bytes([addr & 0xFF, addr >> 8, bank]) + tail


CONTRACT = {
    "GetFirstSpriteAnimBufferProperty": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetSpriteAnimBufferProperty": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetSpriteAnimBufferProperty_SpriteInA": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "Func_3ddb": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "Func_3de7": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    # Final pop af restores flags; BankswitchROM then leaves A as the restored bank.
    "DrawSpriteAnimationFrame": {"compare": ("f", "hl"), "preserve": ("f",)},
    # The routine restores AF and HL; its final bank switch makes A scratch.
    "GetAnimationFramePointer": {"compare": ("f", "hl"), "preserve": ("f", "hl")},
}

CASES = {
    "GetFirstSpriteAnimBufferProperty": [
        {"c": 0, "wram": {W_WHICH_SPRITE: b"\x00"}},
        dict(POISON, c=15, wram={W_WHICH_SPRITE: b"\x0f"}),
        {"wram": {W_WHICH_SPRITE: b"\x10"}},
        dict(POISON, wram={W_WHICH_SPRITE: b"\xff"}),
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
    "DrawSpriteAnimationFrame": [
        # Baseline: no flip, no edge clipping, single record.
        {"hl": 0xC100, "wram": {
            wCurrSpriteFrameBank: b"\x00", wCurrSpriteXPos: b"\x50", wCurrSpriteYPos: b"\x60",
            wCurrSpriteAttributes: b"\x00", wCurrSpriteTileID: b"\x10", wOAMOffset: b"\x00",
            0xC100: bytes((1, 0x05, 0x08, 0x02, 0x00))},
         "read": {wOAM: 4, wOAMOffset: 1, wCurrSpriteRightEdgeCheck: 2}},
        # Poison hl (the only field this routine consumes) to a controlled address;
        # count=0 exits immediately, but the edge checks still run unconditionally.
        dict(POISON, hl=0xC300, wram={
            hBankROM: b"\x0A", wCurrSpriteFrameBank: b"\x01",
            wCurrSpriteXPos: b"\xF5", wCurrSpriteYPos: b"\x10", 0xC300: b"\x00"},
             read={wCurrSpriteRightEdgeCheck: 2}),
        # Both Y and X flip, with a palette/flip-bit attribute delta.
        {"hl": 0xC100, "wram": {
            wCurrSpriteFrameBank: b"\x00", wCurrSpriteXPos: b"\x50", wCurrSpriteYPos: b"\x60",
            wCurrSpriteAttributes: b"\x60", wCurrSpriteTileID: b"\x20", wOAMOffset: b"\x00",
            0xC100: bytes((1, 0x05, 0x03, 0x0A, 0x11))},
         "read": {wOAM: 4, wOAMOffset: 1}},
        # Y offset carries a non-edge sprite past the 256 boundary: clipped, so
        # wOAM/wOAMOffset must stay untouched even though hl still advances.
        {"hl": 0xC200, "wram": {
            wCurrSpriteFrameBank: b"\x00", wCurrSpriteXPos: b"\x10", wCurrSpriteYPos: b"\x90",
            wCurrSpriteAttributes: b"\x00", wCurrSpriteTileID: b"\x00", wOAMOffset: b"\x08",
            wOAM + 8: bytes((0x11, 0x22, 0x33, 0x44)),
            0xC200: bytes((1, 0x7F, 0x00, 0x00, 0x00))},
         "read": {wOAM + 8: 4, wOAMOffset: 1}},
        # Three records in one frame: hl advances 1 + 4*3 and wOAMOffset by 12.
        {"hl": 0xC400, "wram": {
            wCurrSpriteFrameBank: b"\x00", wCurrSpriteXPos: b"\x10", wCurrSpriteYPos: b"\x10",
            wCurrSpriteAttributes: b"\x00", wCurrSpriteTileID: b"\x00", wOAMOffset: b"\x00",
            0xC400: bytes((3, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 0))},
         "read": {wOAM: 12, wOAMOffset: 1}},
        # Real bank switch: frame data comes from bank 3's actual ROM image.
        {"hl": 0x4000, "wram": {
            wCurrSpriteFrameBank: b"\x03", wCurrSpriteXPos: b"\x10", wCurrSpriteYPos: b"\x10",
            wCurrSpriteAttributes: b"\x00", wCurrSpriteTileID: b"\x00", wOAMOffset: b"\x00",
            hBankROM: b"\x00"},
         "read": {hBankROM: 1}},
    ],
    "GetAnimationFramePointer": [
        # wWhichAnimationFrame == $FF: the SpriteNullAnimationPointer branch,
        # a real, fixed ROM address and bank.
        {"hl": 0xC500, "wram": {wWhichAnimationFrame: b"\xFF"}, "read": {0xC50B: 3}},
        # Ordinary table lookup, frame index 3.
        {"hl": 0xC500, "wram": {
            wWhichAnimationFrame: b"\x03", wTempPointer: wtemp_seed(0x02, 0xC300),
            0xC300: bytes((0x02, 0x00, 0xC3)), 0xC306: bytes((0x78, 0x56))},
         "read": {0xC50B: 3}},
        # Poison hl (the only field this routine consumes); frame index 0 exercises
        # the rotate(0)==0 boundary.
        dict(POISON, hl=0xC600, wram={
            hBankROM: b"\x09", wWhichAnimationFrame: b"\x00",
            wTempPointer: wtemp_seed(0x00, 0xC300),
            0xC300: bytes((0x00, 0x80, 0xC3)), 0xC380: bytes((0xAB, 0xCD))},
             read={0xC60B: 3, hBankROM: 1}),
        # frame index $FE: rotate($FE) == $FD, carries into the high byte.
        {"hl": 0xC500, "wram": {
            wWhichAnimationFrame: b"\xFE", wTempPointer: wtemp_seed(0x01, 0xC700),
            0xC700: bytes((0x01, 0x80, 0xC7)), 0xC87D: bytes((0x11, 0x22))},
         "read": {0xC50B: 3}},
    ],
}
# >>> factory-cases-statics
wAllSpriteAnimationsDisabled = 0xD5D7
wVBlankOAMCopyToggle = 0xCAC0
# <<< factory-cases-statics

# >>> factory ClearSpriteAnimations
CONTRACT["ClearSpriteAnimations"] = {
    "compare": ("f", "b", "c", "d", "e", "hl"),
    "preserve": ("f", "b", "c", "d", "e", "hl"),
}
CASES["ClearSpriteAnimations"] = [
    {"read": {SPRITE_BUFFER: 256, wOAM: 160, wOAMOffset: 1,
              wVBlankOAMCopyToggle: 1, W_WHICH_SPRITE: 1}},
    dict(POISON, wram={SPRITE_BUFFER: b"\xff" * 256},
         read={SPRITE_BUFFER: 256, wOAM: 160, wOAMOffset: 1,
               wVBlankOAMCopyToggle: 1}),
    {"wram": {wAllSpriteAnimationsDisabled: b"\x01", SPRITE_BUFFER: b"\xaa" * 256},
     "read": {SPRITE_BUFFER: 256, wVBlankOAMCopyToggle: 1}},
]
# <<< factory ClearSpriteAnimations

# >>> factory HandleAllSpriteAnimations
CONTRACT["HandleAllSpriteAnimations"] = {
    "compare": ("f", "b", "c", "d", "e", "hl"),
    "preserve": ("f", "b", "c", "d", "e", "hl"),
}
CASES["HandleAllSpriteAnimations"] = [
    {"wram": {SPRITE_BUFFER: b"\x00" * 256},
     "read": {SPRITE_BUFFER: 256, wOAM: 160, wOAMOffset: 1,
              wVBlankOAMCopyToggle: 1, W_WHICH_SPRITE: 1}},
    dict(POISON, wram={SPRITE_BUFFER: b"\x00" * 256},
         read={SPRITE_BUFFER: 256, wOAM: 160, wOAMOffset: 1,
               wVBlankOAMCopyToggle: 1}),
    {"wram": {wAllSpriteAnimationsDisabled: b"\x01", SPRITE_BUFFER: b"\x11" * 256},
     "read": {SPRITE_BUFFER: 256, wVBlankOAMCopyToggle: 1}},
]
# <<< factory HandleAllSpriteAnimations

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "DrawSpriteAnimationFrame": {
        "source_symbol": "DrawSpriteAnimationFrame",
        "before": "wCurrSpriteRightEdgeCheck = (wCurrSpriteXPos >= 0xF0u) ? 0xFFu : 0x00u;",
        "after": "wCurrSpriteRightEdgeCheck = (wCurrSpriteXPos >= 0x80u) ? 0xFFu : 0x00u;",
        "case_ids": ["DrawSpriteAnimationFrame-0", "DrawSpriteAnimationFrame-1", "DrawSpriteAnimationFrame-2", "DrawSpriteAnimationFrame-3", "DrawSpriteAnimationFrame-4", "DrawSpriteAnimationFrame-5"],
    },
}
# >>> factory-mutation ClearSpriteAnimations
MUTATIONS["ClearSpriteAnimations"] = {
    "source_symbol": "ClearSpriteAnimations",
    "before": "_ClearSpriteAnimations();",
    "after": "(void)0;",
    "case_ids": ["ClearSpriteAnimations-0", "ClearSpriteAnimations-1"],
}
# <<< factory-mutation ClearSpriteAnimations
# >>> factory-mutation HandleAllSpriteAnimations
MUTATIONS["HandleAllSpriteAnimations"] = {
    "source_symbol": "HandleAllSpriteAnimations",
    "before": "_HandleAllSpriteAnimations();",
    "after": "(void)0;",
    "case_ids": ["HandleAllSpriteAnimations-0", "HandleAllSpriteAnimations-1"],
}
# <<< factory-mutation HandleAllSpriteAnimations
