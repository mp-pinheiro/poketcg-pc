SRC = 0xC100
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "InitializeCardListParameters": ("b", "c", "d", "e", "hl"),
    "InitializeMenuParameters": ("c", "hl"),
    "SetMenuItem": ("b", "c", "d", "e", "hl"),
    "OneByteNumberToTxSymbol": ("b", "c", "d", "hl"),
    "OneByteNumberToTxSymbol_PadSpace": ("b", "c", "d", "hl"),
    "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign": ("b", "c", "d", "hl"),
    "CardTypeToSymbolID": ("b", "c", "d", "e", "hl"),
    "GetCardSymbolData": ("d", "e", "hl"),
}

PARAMS8 = bytes(range(8))
PARAMS9 = bytes(range(9))
CASES = {
    "InitializeCardListParameters": [
        {"hl": SRC, "wram": {SRC: PARAMS9}},
        dict(POISON, a=7, d=3, e=2, hl=SRC, wram={SRC: PARAMS9}),
    ],
    "InitializeMenuParameters": [
        {"hl": SRC, "wram": {SRC: PARAMS8}},
        dict(POISON, a=4, hl=SRC, wram={SRC: PARAMS8}),
    ],
    "SetMenuItem": [
        {},
        dict(POISON, a=5),
    ],
    "OneByteNumberToTxSymbol": [
        {"read": {0xC590: 3}},
        dict(POISON, a=9, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "OneByteNumberToTxSymbol_PadSpace": [
        {"read": {0xC590: 3}},
        {"a": 9, "read": {0xC590: 3}},
        dict(POISON, a=42, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign": [
        {"read": {0xC590: 3}},
        {"a": 9, "read": {0xC590: 3}},
        dict(POISON, a=7, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "CardTypeToSymbolID": [
        {"wram": {0xCC24: b"\x00"}},
        dict(POISON, wram={0xCC24: b"\x07"}),
        {"wram": {0xCC24: b"\x08"}},
        {"wram": {0xCC24: b"\x0f"}},
        {"wram": {0xCC24: b"\x10", 0xCC2D: b"\x03"}},
    ],
    "GetCardSymbolData": [
        {"wram": {0xCC24: b"\x00", 0xCC2D: b"\x00"}},
        dict(POISON, wram={0xCC24: b"\x10", 0xCC2D: b"\x02"}),
        {"wram": {0xCC24: b"\x08"}},
    ],
}
