"""Oracle-diff cases for poketcg/src/engine/menus/card_album.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetFirstOwnedCardIndex
OWNED_LIST = 0xCF68
NOT_OWNED = 0x80

CONTRACT["GetFirstOwnedCardIndex"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("c", "d", "e")}
CASES["GetFirstOwnedCardIndex"] = [
    {},
    dict(POISON),
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 3, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 64, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 1, "a": NOT_OWNED},
               {"fn": "FillMemoryWithA", "hl": OWNED_LIST + 1, "b": 0, "c": 1, "a": 0x81}]},
]
# <<< factory GetFirstOwnedCardIndex

# >>> factory-cases-statics
wCardListCoords = 0xCED0
wCardListVisibleOffset = 0xCEA1
wFilteredCardList = 0xCEDA
wNumVisibleCardListEntries = 0xCECB
wUnableToScrollDown = 0xCECD
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory PrintCardSetListEntries
CONTRACT["PrintCardSetListEntries"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintCardSetListEntries"] = [
    {"wram": {wCardListCoords: b"\x10\x08", wCardListVisibleOffset: b"\x00", wNumVisibleCardListEntries: b"\x00", wFilteredCardList: b"\x00\x00"}, "read": {wUnableToScrollDown: 1, wFilteredCardList: 2}},
    dict(POISON, wram={wCardListCoords: b"\x10\x08", wCardListVisibleOffset: b"\x00", wNumVisibleCardListEntries: b"\x00", wFilteredCardList: b"\x00\x00"}, read={wUnableToScrollDown: 1, wFilteredCardList: 2}),
]
# <<< factory PrintCardSetListEntries

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetFirstOwnedCardIndex
MUTATIONS["GetFirstOwnedCardIndex"] = {
    "source_symbol": "GetFirstOwnedCardIndex",
    "before": "index++;",
    "after": "",
    "case_ids": ["GetFirstOwnedCardIndex-2", "GetFirstOwnedCardIndex-3", "GetFirstOwnedCardIndex-4"],
}
# <<< factory-mutation GetFirstOwnedCardIndex
# >>> factory-mutation PrintCardSetListEntries
MUTATIONS["PrintCardSetListEntries"] = {"source_symbol": "PrintCardSetListEntries", "before": "gb_write8(wUnableToScrollDown_ADDR, TRUE);", "after": "gb_write8(wUnableToScrollDown_ADDR, FALSE);", "case_ids": ["PrintCardSetListEntries-0", "PrintCardSetListEntries-1"]}
# <<< factory-mutation PrintCardSetListEntries
