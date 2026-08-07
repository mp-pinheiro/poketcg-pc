SRC = 0xC100
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "InitTextFormat": ("b", "c", "d", "e", "hl"),
    "CaseHalfWidthLetter": ("a", "b", "c", "d", "e", "hl"),
    # Carry is the real output (callers branch on it); exit a is path-dependent
    # residue no caller reads, so f is in and a is out.
    "ClassifyTextCharacterPair": ("f", "b", "c", "d", "e", "hl"),
    "GetTextLengthInHalfTiles": ("a", "b", "c", "d", "e", "hl"),
    "GetTextLengthInTiles": ("a", "b", "c", "d", "e", "hl"),
    "GetFullWidthFontTileOffset": ("a", "b", "c", "d", "e", "hl"),
    "ConvertTileNumberToTileDataAddress": ("a", "b", "c", "d", "e", "hl"),
    "CopyHalfWidthCharacterToDE": ("a", "d", "e", "hl"),
    "CreateHalfWidthFontTile": ("a", "b", "c", "d", "e", "hl"),
    "CreateFullWidthFontTile": ("a", "b", "d", "e", "hl"),
    "CreateFullWidthFontTile_ConvertToTileDataAddress": ("a", "b", "c", "d", "e", "hl"),
    "GenerateTextTile": ("a", "b", "c", "d", "e", "hl"),
    "TwoByteNumberToTxSymbol_PadSpace": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "InitTextFormat": [{}, dict(POISON)],
    "CaseHalfWidthLetter": [{"e": 0x61}, dict(POISON, e=0x7A)],
    # All four exit paths: swap (e < TX_CTRL_START, carry set), half-width, katakana,
    # and not-katakana. Previously both cases used e=0x01 and drove only the swap.
    "ClassifyTextCharacterPair": [
        {"d": 0x20, "e": 0x01},
        dict(POISON, d=0x22, e=0x01),
        {"d": 0x20, "e": 0x08},
        {"d": 0x20, "e": 0x20, "wram": {0xFFAF: b"\x0f"}},
        {"d": 0x20, "e": 0x20, "wram": {0xFFAF: b"\x0e"}},
        {"d": 0x20, "e": 0x70, "wram": {0xFFAF: b"\x0f"}},
        {"d": 0x20, "e": 0x01, "wram": {0xCD0A: b"\x01"}},
        {"d": 0x20, "e": 0x20, "wram": {0xCD0A: b"\x01", 0xFFAF: b"\x0f"}},
    ],
    "GetTextLengthInHalfTiles": [
        {"hl": SRC, "wram": {SRC: b"\x00"}},
        {"hl": SRC, "wram": {SRC: b"\x01\x02\x00"}},
        {"hl": SRC, "wram": {SRC: b"\x05\x01\x05\x02\x00"}},
        dict(POISON, hl=SRC, wram={SRC: b"\x01\x02\x03\x04\x00"}),
    ],
    "GetTextLengthInTiles": [
        {"hl": SRC, "wram": {SRC: b"\x00"}},
        {"hl": SRC, "wram": {SRC: b"\x06\x01\x02\x03\x00"}},
        dict(POISON, hl=SRC, wram={SRC: b"\x01\x02\x03\x00"}),
    ],
    "GetFullWidthFontTileOffset": [{"d": 0, "e": 1}, {"d": 0x0F, "e": 0x20}, dict(POISON, d=0x0E, e=0x20)],
    "ConvertTileNumberToTileDataAddress": [{"b": 0}, {"b": 1}, dict(POISON, b=0x80)],
    "CopyHalfWidthCharacterToDE": [{"a": 0x20, "d": 0xC1, "e": 0}, dict(POISON, a=0x41, d=0xC1, e=0)],
    "CreateHalfWidthFontTile": [{"d": 0x20, "e": 0x20}, dict(POISON, d=0x41, e=0x42)],
    "CreateFullWidthFontTile": [{"hl": 0x4000}, dict(POISON, hl=0x4000)],
    "CreateFullWidthFontTile_ConvertToTileDataAddress": [{"d": 0, "e": 1}, dict(POISON, d=0x0F, e=0x20)],
    "GenerateTextTile": [{"b": 0, "d": 0x20, "e": 0x20}, {"b": 1, "d": 0x20, "e": 0x20}],
    "TwoByteNumberToTxSymbol_PadSpace": [{"hl": 0}, {"hl": 1}, {"hl": 0xFFFF}, dict(POISON, hl=12345)],
}

CONTRACT.update({
    "ProcessText": ("hl",),
    "InitTextPrinting_ProcessText": ("hl",),
    "SetupText": ("b", "c", "d", "e", "hl"),
    "InitTextPrinting": ("b", "c", "hl"),
    "InitTextPrintingInTextbox": ("b", "c", "hl"),
    "PlaceNextTextTile": ("a", "b", "c", "d", "e", "hl"),
    "ProcessSpecialTextCharacter": ("a", "hl"),
    "TerminateHalfWidthText": ("a", "d", "e", "hl"),
    "Func_235e": ("a", "d", "e", "f"),
    "Func_2325": ("a", "d", "e", "f"),
    "Func_22ca": ("b", "c", "d", "e", "hl"),
    "CopyTextData": ("a", "d", "e", "hl"),
})

CASES.update({
    "ProcessText": [{"hl": SRC, "wram": {SRC: b"\x00"}},
                     dict(POISON, hl=SRC, wram={SRC: b"\x00"})],
    "InitTextPrinting_ProcessText": [{"hl": SRC, "wram": {SRC: b"\x00\x00\x00"}},
                                      dict(POISON, hl=SRC, wram={SRC: b"\x00\x00\x00"})],
    "SetupText": [{"d": 1, "e": 2, "read": {0xc600: 256}},
                   dict(POISON, d=3, e=4, read={0xc600: 256})],
    "InitTextPrinting": [{"d": 0, "e": 0}, dict(POISON, d=3, e=4)],
    "InitTextPrintingInTextbox": [{"a": 1, "d": 0, "e": 0},
                                   dict(POISON, a=2, d=3, e=4)],
    "PlaceNextTextTile": [{"a": 0, "wram": {0xffaa: b"\x00", 0xffab: b"\xc0",
                                               0xcd05: b"\x22", 0xc000: b"\x00"}},
                           dict(POISON, a=0x44, wram={0xffaa: b"\x00", 0xffab: b"\xc0",
                                                      0xcd05: b"\x33", 0xc000: b"\x00"})],
    "ProcessSpecialTextCharacter": [{"a": 0, "hl": SRC},
                                     dict(POISON, a=0, hl=SRC)],
    "TerminateHalfWidthText": [{}, dict(POISON)],
    # Both maintain the generated-tile cache as a linked list over $C6 key1,
    # $C7 key2, $C8 next and $C9 prev, with index 0 reserved as the terminator.
    # Without reading those pages back the list surgery is invisible, so each
    # case warms the cache with SetupText and then diffs all four pages.
    "Func_235e": [
        {}, dict(POISON),
        {"d": 0x41, "e": 0x42,
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "read": {0xC600: 4, 0xC700: 4, 0xC800: 4, 0xC900: 4, 0xFFA9: 1}},
    ],
    "Func_2325": [
        {}, dict(POISON),
        # one miss allocates the first node past the reserved index 0
        {"d": 0x41, "e": 0x42,
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "read": {0xC620: 2, 0xC720: 2, 0xC820: 2, 0xC920: 2, 0xFFA9: 1,
                  0xCD04: 1}},
        # a second distinct pair allocates again and relinks the head
        {"d": 0x43, "e": 0x44,
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40},
                   {"fn": "Func_2325", "d": 0x41, "e": 0x42}],
         "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xFFA9: 1,
                  0xCD04: 1}},
        # repeating the first pair must hit the cache and hoist it, not allocate
        {"d": 0x41, "e": 0x42,
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40},
                   {"fn": "Func_2325", "d": 0x41, "e": 0x42},
                   {"fn": "Func_2325", "d": 0x43, "e": 0x44}],
         "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xFFA9: 1,
                  0xCD04: 1}},
    ],
    # The zero-length path alone leaves the whole copy loop unexercised, so these
    # also drive: the early-TX_END fill, truncation at the budget, and a plain
    # control character (>= TX_CTRL_START, < TX_CTRL_END), which the asm copies
    # without counting it in e or spending budget.
    "CopyTextData": [
        {"a": 1, "hl": SRC, "d": 0xc2, "e": 0, "wram": {SRC: b"\x00"}},
        dict(POISON, a=1, hl=SRC, d=0xc2, e=1, wram={SRC: b"\x00"}),
        # full-width source, ends before the budget: pads with the $70 space tile
        {"a": 4, "hl": SRC, "d": 0xc2, "e": 0,
         "wram": {SRC: b"\x41\x42\x00"}, "read": {0xC200: 8}},
        # half-width source ($06 lead byte) doubles the budget and pads with $20
        {"a": 2, "hl": SRC, "d": 0xc2, "e": 0,
         "wram": {SRC: b"\x06\x41\x42\x00"}, "read": {0xC200: 8}},
        # more characters than the budget allows: truncates and sets carry
        {"a": 2, "hl": SRC, "d": 0xc2, "e": 0,
         "wram": {SRC: b"\x41\x42\x43\x44\x45\x00"}, "read": {0xC200: 8}},
        # a plain control character is copied but must not consume budget
        {"a": 3, "hl": SRC, "d": 0xc2, "e": 0,
         "wram": {SRC: b"\x07\x41\x42\x00"}, "read": {0xC200: 8}},
    ],
    # Every CONTRACT field is push/pop-preserved, so the only observable effect is what
    # the dispatched callees write: wCurTextTile ($CD05), the tile at
    # hTextBGMap0Address ($FFAA, pointed into VRAM here), and the advanced
    # hTextBGMap0Address / hTextLineCurPos ($FFAC). Without reading those back the
    # cases cannot fail -- stubbing the body left them green.
    # hffb0 ($FFB0) selects the branch: bit0 set -> Func_235e; bit0 clear -> the
    # Func_2325 / GenerateTextTile path, with bit1 gating PlaceNextTextTile.
    "Func_22ca": [
        {"d": 1, "e": 2,
         "wram": {0xffb0: b"\x01", 0xffa9: b"\x2a", 0xffaa: b"\x00\x98", 0xffac: b"\x00"},
         "read": {0xCD05: 1, 0xFFAA: 2, 0xFFAC: 1, 0x9800: 4}},
        dict(POISON, d=3, e=4,
             wram={0xffb0: b"\x01", 0xffa9: b"\x2a", 0xffaa: b"\x00\x98", 0xffac: b"\x00"},
             read={0xCD05: 1, 0xFFAA: 2, 0xFFAC: 1, 0x9800: 4}),
        {"d": 1, "e": 2,
         "wram": {0xffb0: b"\x00", 0xffa9: b"\x2a", 0xffaa: b"\x00\x98", 0xffac: b"\x00"},
         "read": {0xCD05: 1, 0xFFAA: 2, 0xFFAC: 1, 0x9800: 4}},
        {"d": 1, "e": 2,
         "wram": {0xffb0: b"\x02", 0xffa9: b"\x2a", 0xffaa: b"\x00\x98", 0xffac: b"\x00"},
         "read": {0xCD05: 1, 0xFFAA: 2, 0xFFAC: 1, 0x9800: 4}},
    ],
})
