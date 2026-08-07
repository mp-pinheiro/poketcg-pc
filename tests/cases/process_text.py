SRC = 0xC100
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "InitTextFormat": ("b", "c", "d", "e", "hl"),
    "CaseHalfWidthLetter": ("a", "b", "c", "d", "e", "hl"),
    "ClassifyTextCharacterPair": ("a", "b", "c", "d", "e", "hl"),
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
    "ClassifyTextCharacterPair": [{"d": 0x20, "e": 0x01}, dict(POISON, d=0x22, e=0x01)],
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
