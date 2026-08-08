"""Oracle-diff cases for poketcg/src/home/card_data.asm.

CopyFontsOrDuelGraphicsTiles2 (card_data.asm:208) is excluded: zero callsites
anywhere in poketcg/src (only the definition itself; grep confirmed no `call`,
`jp`, or pointer-table reference exists) -- dead code.

LoadCardDataToHL_FromCardID is excluded: it is a fallthrough continuation of
LoadCardDataToBuffer1_FromCardID/_2, not an independent entry point. Those two
wrappers `push hl` before falling/jumping in, and LoadCardDataToHL_FromCardID's
tail does one `pop hl` more than this routine itself pushes -- balanced only by
that wrapper push. Called directly (`call LoadCardDataToHL_FromCardID`), the
extra pop consumes the return address itself and `ret` jumps to garbage. Its
behavior is already covered transitively by the two wrappers below.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadedCard1 = 0xCC24
wLoadedCard2 = 0xCC65
CARD_LEN = 0x41

CONTRACT = {
    "GetCardType": ("a", "b", "c", "d", "e", "hl"),
    "GetCardName": ("b", "c", "d", "e", "hl"),
    "GetCardTypeRarityAndSet": ("a", "b", "c", "d", "e", "hl"),
    "LoadCardDataToBuffer1_FromCardID": ("b", "c", "d", "e", "hl"),
    "LoadCardDataToBuffer2_FromCardID": ("b", "c", "d", "e", "hl"),
    "LoadCardDataToBuffer1_FromName": (),
    "LoadCardGfx": (),
    "GetCardPointer": ("f", "b", "c", "d", "e", "hl"),
}
CASES = {
    "GetCardType": [
        {"e": 1}, {"e": 8}, {"e": 0x40}, {"e": 0x80}, {"e": 0xE4},
        dict(POISON, e=0x20),
    ],
    "GetCardName": [
        {"e": 1}, {"e": 8}, {"e": 0x40}, {"e": 0xE4},
        dict(POISON, e=0x60),
    ],
    "GetCardTypeRarityAndSet": [
        {"a": 1}, {"a": 8}, {"a": 0x40}, {"a": 0xE4},
        dict(POISON, a=0x30),
    ],
    "LoadCardDataToBuffer1_FromCardID": [
        {"e": 8, "wram": {wLoadedCard1: b"\xaa" * CARD_LEN}, "read": {wLoadedCard1: CARD_LEN}},
        {"e": 0x80, "read": {wLoadedCard1: CARD_LEN}},
        dict(POISON, e=0xE4, wram={wLoadedCard1: b"\xaa" * CARD_LEN}, read={wLoadedCard1: CARD_LEN}),
    ],
    "LoadCardDataToBuffer2_FromCardID": [
        {"e": 8, "wram": {wLoadedCard2: b"\xaa" * CARD_LEN}, "read": {wLoadedCard2: CARD_LEN}},
        {"e": 0xE4, "read": {wLoadedCard2: CARD_LEN}},
        dict(POISON, e=0x40, wram={wLoadedCard2: b"\xaa" * CARD_LEN}, read={wLoadedCard2: CARD_LEN}),
    ],
    "LoadCardDataToBuffer1_FromName": [
        {"d": 0x08, "e": 0x0A, "read": {wLoadedCard1: CARD_LEN}},
        {"d": 0x09, "e": 0x1C, "read": {wLoadedCard1: CARD_LEN}},
        {"d": 0xFF, "e": 0xFF, "wram": {wLoadedCard1: b"\xaa" * CARD_LEN}, "read": {wLoadedCard1: CARD_LEN}},
    ],
    "LoadCardGfx": [
        {"hl": 0x02A7, "d": 0x88, "e": 0x00, "b": 0x30, "c": 0x10, "vread": {0: {0x8800: 0x300}}},
        {"hl": 0x1800, "d": 0x90, "e": 0x00, "b": 0x30, "c": 0x10, "vread": {0: {0x9000: 0x300}}},
    ],
    "GetCardPointer": [
        {"e": 0},
        {"e": 228},  # last valid index (0xE4 == NUM_CARDS)
        {"e": 229},  # first out-of-bounds index, lands exactly on the boundary
        {"e": 230},  # out of bounds, past the boundary
        {"e": 255},
        dict(POISON, e=8),
        dict(POISON, e=229),
    ],
}
