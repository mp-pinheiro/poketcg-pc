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
    "GetCardType": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetCardName": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    "GetCardTypeRarityAndSet": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "LoadCardDataToBuffer1_FromCardID": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadCardDataToBuffer2_FromCardID": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadCardDataToBuffer1_FromName": {"compare": (), "preserve": ()},
    "LoadCardGfx": {"compare": (), "preserve": ()},
    "GetCardPointer": {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
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
# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CARD_DATA_LENGTH = 0x41

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory LoadCardDataToHL_FromCardID
CONTRACT["LoadCardDataToHL_FromCardID"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LoadCardDataToHL_FromCardID"] = [
    {"stack": [0]},
    {"e": 1, "hl": 0xC100, "stack": [0xC100], "wram": {0xC100: b"\xAA" * CARD_DATA_LENGTH}, "read": {0xC100: 0x41}},
    {"e": 0xE4, "hl": 0xC200, "stack": [0xC200], "wram": {0xC200: b"\xAA" * CARD_DATA_LENGTH}, "read": {0xC200: 0x41}},
    dict(POISON, stack=[0x1234]),
    dict(POISON, e=1, hl=0xC300, stack=[0xC300], wram={0xC300: b"\xAA" * CARD_DATA_LENGTH}, read={0xC300: 0x41}),
]
# <<< factory LoadCardDataToHL_FromCardID

# >>> factory CopyFontsOrDuelGraphicsTiles2
CONTRACT["CopyFontsOrDuelGraphicsTiles2"] = {"compare": (), "preserve": ()}
CASES["CopyFontsOrDuelGraphicsTiles2"] = [
    {},
    {"b": 1, "hl": 0x4000, "d": 0xC5, "e": 0x00, "wram": {0xC500: b"\xAA" * 16}, "read": {0xC500: 16, 0xFF80: 1}},
    dict(POISON, b=1, hl=0x4000, wram={0xDDEE: b"\x55" * 16}, read={0xDDEE: 16, 0xFF80: 1}),
    {"b": 1, "hl": 0x4000, "d": 0xC5, "e": 0x20, "wram": {0xC520: b"\x33" * 16}, "read": {0xC520: 16, 0xFF80: 1}}
]
# <<< factory CopyFontsOrDuelGraphicsTiles2

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GetCardType": {
        "source_symbol": "GetCardType",
        "before": "\treturn card_data(e)[CARD_DATA_TYPE];",
        "after": "\treturn card_data(e)[CARD_DATA_RARITY];",
        "case_ids": ["GetCardType-0", "GetCardType-1", "GetCardType-2", "GetCardType-3", "GetCardType-4", "GetCardType-5"],
    },
}
# >>> factory-mutation LoadCardDataToHL_FromCardID
MUTATIONS["LoadCardDataToHL_FromCardID"] = {"source_symbol": "LoadCardDataToHL_FromCardID", "before": "\tuint8_t copy_length = PKMN_CARD_DATA_LENGTH;", "after": "\tuint8_t copy_length = 0x40u;", "case_ids": ["LoadCardDataToHL_FromCardID-1", "LoadCardDataToHL_FromCardID-2", "LoadCardDataToHL_FromCardID-4"]}
# <<< factory-mutation LoadCardDataToHL_FromCardID
# >>> factory-mutation CopyFontsOrDuelGraphicsTiles2
MUTATIONS["CopyFontsOrDuelGraphicsTiles2"] = {"source_symbol": "CopyFontsOrDuelGraphicsTiles2", "before": "\tuint8_t copy_length = 0x10u;", "after": "\tuint8_t copy_length = 0x08u;", "case_ids": ["CopyFontsOrDuelGraphicsTiles2-1", "CopyFontsOrDuelGraphicsTiles2-2", "CopyFontsOrDuelGraphicsTiles2-3"]}
# <<< factory-mutation CopyFontsOrDuelGraphicsTiles2
