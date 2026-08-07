SRC = 0xC100
CURSOR_STATE = 0xCD0F

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
    "SetCursorParametersForTextBox": ("b", "c", "d", "e", "hl"),
    "SetCursorParametersForTextBox_Default": ("b", "c", "d", "e", "hl"),
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
    "SetCursorParametersForTextBox": [
        {"d": 3, "e": 4, "b": 0x12, "c": 0x34},
        dict(POISON, d=7, e=8, b=0x56, c=0x78),
        {"d": 3, "e": 4, "b": 0x12, "c": 0x34, "oracle": False,
         "why": "cursor state is inside the synthesized frame",
		"expect": {CURSOR_STATE: bytes([0, 0, 3, 4, 0, 1, 0x12, 0x34])}},
    ],
    # The label intentionally falls through into WaitForButtonAorB after the
    # setup call (menus.asm:709-716), so a standalone oracle invocation waits
    # forever. SYM_CURSOR_R is resolved from charmaps.asm:444 as $0F.
    "SetCursorParametersForTextBox_Default": [
        {"d": 2, "e": 5, "oracle": False,
         "why": "intentional fallthrough into the genuine A/B input wait; SYM_CURSOR_R=$0F from charmaps.asm:444",
         "expect": {CURSOR_STATE: bytes([0, 0, 2, 5, 0, 1, 0x0F, 0])},
         "expect_regs": {"b": 0x0F, "c": 0, "hl": 0xCD16}},
        dict(POISON, d=9, e=1, oracle=False,
             why="intentional fallthrough into the genuine A/B input wait; SYM_CURSOR_R=$0F from charmaps.asm:444",
             expect={CURSOR_STATE: bytes([0, 0, 9, 1, 0, 1, 0x0F, 0])},
             expect_regs={"b": 0x0F, "c": 0, "hl": 0xCD16}),
    ],
}
