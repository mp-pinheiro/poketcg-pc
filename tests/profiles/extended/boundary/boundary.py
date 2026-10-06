"""Extended boundary fixture cases: the fixture ROM pads CardPointers to $1ff entries."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
PLAYER_TURN = b"\xc2"
COLLECTION = 0xA100
PLAYER_DECK = 0xC400
LOADED_CARD1 = 0xCBCF
LOADED_CARD1_GFX = 0xCBD0
CARD_PALETTE = 0xCDA9
DECOMP_COUNT = 0xCAEF
BOUNDARY_IDS = (0x00FE, 0x00FF, 0x0100, 0x01FF)


def card(card_id, **extra):
    case = {"d": card_id >> 8, "e": card_id & 0xFF}
    case.update(extra)
    return case


def deck_bytes(ids):
    entries = list(ids) + [0x0001] * (60 - len(ids))
    return bytes(sum(([value & 0xFF, value >> 8] for value in entries), []))


CONTRACT = {
    "GetCardPointer": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetCardType": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetCardName": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    "LoadCardDataToBuffer1_FromCardID": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetCardCountInCollection": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "AddCardToCollection": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CompressDeckToSRAM": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "DecompressSRAMDeck": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetCardIDFromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    "LoadLoaded1CardGfx": {"compare": (), "preserve": ()},
}

CASES = {
    "GetCardPointer": [card(card_id) for card_id in BOUNDARY_IDS] + [
        card(0x0200),
        card(0x01FF, **{key: value for key, value in POISON.items() if key not in ("d", "e")}),
        card(0x0200, **{key: value for key, value in POISON.items() if key not in ("d", "e")}),
    ],
    "GetCardType": [card(card_id) for card_id in BOUNDARY_IDS],
    "GetCardName": [card(card_id) for card_id in BOUNDARY_IDS],
    "LoadCardDataToBuffer1_FromCardID": [
        card(card_id, wram={LOADED_CARD1: b"\xaa" * 0x41}, read={LOADED_CARD1: 0x41})
        for card_id in BOUNDARY_IDS
    ],
    "GetCardCountInCollection": [
        card(card_id, sram={0: {COLLECTION: bytes(0x200)}}) for card_id in BOUNDARY_IDS
    ] + [
        card(card_id, sram={0: {COLLECTION: bytes([0x03] * 0x200)}}) for card_id in BOUNDARY_IDS
    ],
    "AddCardToCollection": [
        card(card_id, sram={0: {COLLECTION: bytes(0x200)}}) for card_id in BOUNDARY_IDS
    ] + [
        card(0x01FF, sram={0: {COLLECTION: bytes([0x80] * 0x200)}}),
    ],
    "CompressDeckToSRAM": [
        {"d": 0xC1, "e": 0x00, "hl": 0xC500, "wram": {0xC100: deck_bytes(BOUNDARY_IDS)}, "read": {0xC500: 68}},
        {"d": 0xC1, "e": 0x00, "hl": 0xC500, "wram": {0xC100: deck_bytes([0x01FF] * 60)}, "read": {0xC500: 68}},
    ],
    "DecompressSRAMDeck": [
        {"d": 0xC5, "e": 0x00, "hl": 0xC100, "wram": {0xC500: bytes([0xFF] * 68)}, "read": {0xC100: 120, DECOMP_COUNT: 1}},
        {"d": 0xC5, "e": 0x00, "hl": 0xC100, "wram": {0xC500: bytes([0x80, 0xFF, 0xFE, 0x00, 0xFF] + [0] * 63)},
         "read": {0xC100: 120, DECOMP_COUNT: 1}},
    ],
    "GetCardIDFromDeckIndex": [
        {"a": index, "wram": {0xFF97: PLAYER_TURN, PLAYER_DECK: deck_bytes(BOUNDARY_IDS)}}
        for index in range(len(BOUNDARY_IDS))
    ],
    "LoadLoaded1CardGfx": [
        {"d": 0x88, "e": 0x00, "wram": {LOADED_CARD1_GFX: b"\xa7\x02"},
         "read": {CARD_PALETTE: 0x33}, "vread": {0x00: {0x8800: 0x0300}}},
    ],
}

MUTATIONS = {
    "GetCardPointer": {
        "source_symbol": "get_card_pointer",
        "before": "if (entry >= GETCARDPTR_BOUND)",
        "after": "if (entry > GETCARDPTR_BOUND)",
        "case_ids": ["GetCardPointer-4", "GetCardPointer-6"],
        "source": "src/profiles/extended/home/card_data.c",
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
