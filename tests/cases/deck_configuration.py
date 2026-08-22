"""Oracle-diff cases for poketcg/src/engine/menus/deck_configuration.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DecrementDeckCardsInCollection
CONTRACT["DecrementDeckCardsInCollection"] = {"compare": ("hl",), "preserve": ()}
sCardCollection = 0xA100
CASES["DecrementDeckCardsInCollection"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00"}, "sram": {0: {sCardCollection: b"\x00" * 4}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x02\x00"}, "sram": {0: {sCardCollection: b"\x05\x05\x05"}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01" * 60}, "sram": {0: {sCardCollection + 1: b"\x63"}}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE}, hl=0xC100, wram={0xC100: b"\x00"}, sram={0: {sCardCollection: b"\x00" * 4}}),
]
# <<< factory DecrementDeckCardsInCollection


# >>> factory AddDeckToCollection
CONTRACT["AddDeckToCollection"] = {"compare": ("hl",), "preserve": ()}
sCardCollection2 = 0xA100
CASES["AddDeckToCollection"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00"}, "sram": {0: {sCardCollection2: b"\x00" * 4}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x02\x00"}, "sram": {0: {sCardCollection2: b"\x05\x05\x05"}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01" * 60}, "sram": {0: {sCardCollection2 + 1: b"\x62"}}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE}, hl=0xC100, wram={0xC100: b"\x00"}, sram={0: {sCardCollection2: b"\x00" * 4}}),
]
# <<< factory AddDeckToCollection


# >>> factory CopyListFromHLToDE
CONTRACT["CopyListFromHLToDE"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["CopyListFromHLToDE"] = [
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\x00"}, "read": {0xC200: 1}},
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\x01\x02\x00"}, "read": {0xC200: 3}},
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\xFF" * 5 + b"\x00"}, "read": {0xC200: 6}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC}, hl=0xC100, d=0xC2, e=0x00, wram={0xC100: b"\x00"}, read={0xC200: 1}),
]
# <<< factory CopyListFromHLToDE


# >>> factory CalculateOnesAndTensDigits
CONTRACT["CalculateOnesAndTensDigits"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CalculateOnesAndTensDigits"] = [
    {"a": 0, "wram": {0xCEB6: b"\xFF\xFF"}},
    dict(POISON, wram={0xCEB6: b"\xFF\xFF"}),
    {"a": 1, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 9, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 10, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 19, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 99, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 255, "wram": {0xCEB6: b"\xFF\xFF"}},
]
# <<< factory CalculateOnesAndTensDigits




# >>> factory InitCardSelectionParams
CONTRACT["InitCardSelectionParams"] = {"compare": ("a", "c", "hl"), "preserve": ("c",)}
CASES["InitCardSelectionParams"] = [
    {"a": 0x00, "hl": 0xC100, "wram": {0xC100: b"\x00" * 9}, "read": {0xCEA3: 12, 0xFFB3: 1}},
    dict(POISON, a=0x5A, hl=0xC100, wram={0xC100: bytes(range(1, 10))},
         read={0xCEA3: 12, 0xFFB3: 1}),
    {"a": 0xFF, "hl": 0xC1F8, "wram": {0xC1F8: b"\x11\x22\x33\x44\x55\x66\x77\x88\x99"},
     "read": {0xCEA3: 12, 0xFFB3: 1}},
]
# <<< factory InitCardSelectionParams


# >>> factory ClearMemory_Bank2
CONTRACT["ClearMemory_Bank2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank2"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\xAA" * 0x100}},
    dict(POISON, a=1, hl=0xC200, wram={0xC200: b"\xAA"}),
    {"a": 1, "hl": 0xC300, "wram": {0xC300: b"\xAA"}},
    {"a": 0xFF, "hl": 0xC400, "wram": {0xC400: b"\xAA" * 0xFF}},
]
# <<< factory ClearMemory_Bank2

# >>> factory CheckIfHasOtherValidDecks
CONTRACT["CheckIfHasOtherValidDecks"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfHasOtherValidDecks"] = [
    {"wram": {0xCEB2: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xCEB2: b"\x01\x01\x00\x00"}),
    {"wram": {0xCEB2: b"\x01\x00\x00\x00"}},
    {"wram": {0xCEB2: b"\x00\x01\x00\x00"}},
    {"wram": {0xCEB2: b"\x01\x00\x01\x00"}},
    {"wram": {0xCEB2: b"\x00\x00\x01\x01"}},
]
# <<< factory CheckIfHasOtherValidDecks

# >>> factory FillDEWithA
CONTRACT["FillDEWithA"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "c", "d", "e", "hl")}
CASES["FillDEWithA"] = [
    {"a": 0x00, "b": 0x01, "d": 0xC1, "e": 0x00, "hl": 0xC200, "wram": {0xC100: b"\xFF"}, "read": {0xC100: 1}},
    {"a": 0x7E, "b": 0x00, "d": 0xC2, "e": 0x00, "hl": 0xC300, "wram": {0xC200: b"\xFF" * 0x100}, "read": {0xC200: 0x100}},
    {"a": 0xA5, "b": 0x05, "d": 0xC3, "e": 0x00, "hl": 0xC400, "wram": {0xC300: b"\x00" * 5}, "read": {0xC300: 5}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, wram={0xDDEE: b"\x00" * 0xBB}, read={0xDDEE: 0xBB}),
]
# <<< factory FillDEWithA

# >>> factory DrawHandCardsTileAtDE
CONTRACT["DrawHandCardsTileAtDE"] = {"compare": ("d", "e"), "preserve": ("d", "e")}
CASES["DrawHandCardsTileAtDE"] = [
    {"d": 0x00, "e": 0x00, "vread": {0: {0x9800: 0x40}}},
    {"d": 0x01, "e": 0x02, "vread": {0: {0x9841: 2, 0x9861: 2}}},
    dict(POISON, d=0x02, e=0x03, vread={0: {0x9862: 2, 0x9882: 2}}),
]
# <<< factory DrawHandCardsTileAtDE

# >>> factory CountNumberOfCardsOfType
CONTRACT["CountNumberOfCardsOfType"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["CountNumberOfCardsOfType"] = [
    {},
    {"a": 0x08},
    dict(POISON),
]
# <<< factory CountNumberOfCardsOfType

# >>> factory CopyNBytesFromHLToDE
CONTRACT["CopyNBytesFromHLToDE"] = {"compare": ("d", "e", "hl"), "preserve": ()}
CASES["CopyNBytesFromHLToDE"] = [
    {"b": 1, "hl": 0xC100, "d": 0xC5, "e": 0x00, "wram": {0xC100: b"\x42"}, "read": {0xC500: 1}},
    {"b": 3, "hl": 0xC100, "d": 0xC5, "e": 0x00, "wram": {0xC100: b"\x01\x02\x03"}, "read": {0xC500: 3}},
    {"b": 0, "hl": 0xC100, "d": 0xC5, "e": 0x00, "wram": {0xC100: bytes(range(256))}, "read": {0xC500: 256}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, hl=0xC100, wram={0xC100: bytes(range(187))}, read={0xDDEE: 187}),
]
# <<< factory CopyNBytesFromHLToDE

# >>> factory-cases-statics
wTempCardCollection = 0xC000

sCardCollection = 0xA100
sDeck1Cards = 0xA218
sDeck2Cards = 0xA26C
sDeck3Cards = 0xA2C0
sDeck4Cards = 0xA314
wTempCardCollection = 0xC000

wCardListCursorPos = 0xCEA4
wVisibleListCardIDs = 0xCEC4
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCardListCursorPos = 0xCEA4
wCardListCursorXPos = 0xCEA5
wCardListCursorYPos = 0xCEA6
wCardListXSpacing = 0xCEA8

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory IncrementDeckCardsInTempCollection
CONTRACT["IncrementDeckCardsInTempCollection"] = {"compare": (), "preserve": ()}
CASES["IncrementDeckCardsInTempCollection"] = [
    {"d": 0xC2, "e": 0x00, "wram": {0xC200: b"\x01\x02\x01\x00"}, "read": {0xC001: 2, 0xC002: 1}},
    {"d": 0xC2, "e": 0x10, "wram": {0xC210: b"\x00"}, "read": {}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xDDEE: b"\xBB" * 60}, "read": {0xC0BB: 60}},
]
# <<< factory IncrementDeckCardsInTempCollection

# >>> factory CreateCardCollectionListWithDeckCards
CONTRACT["CreateCardCollectionListWithDeckCards"] = {"compare": (), "preserve": ()}
CASES["CreateCardCollectionListWithDeckCards"] = [
    {"a": 0x00, "sram": {0: {sCardCollection: b"\x00" * 255}}, "read": {wTempCardCollection: 255}},
    {"a": 0x05, "sram": {0: {sCardCollection + 1: b"\x05\x06", sDeck1Cards: b"\x01\x02\x00", sDeck3Cards: b"\x02\x01\x00"}}, "read": {wTempCardCollection + 1: 6, wTempCardCollection + 2: 8}},
    {"a": 0x0A, "sram": {0: {sDeck2Cards: b"\x01\x00", sDeck4Cards: b"\x01\x00"}}, "read": {wTempCardCollection + 1: 2}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, sram={0: {sDeck2Cards: b"\x01\x00", sDeck4Cards: b"\x01\x00"}}, read={wTempCardCollection + 1: 2}),
]
# <<< factory CreateCardCollectionListWithDeckCards

# >>> factory GetSelectedVisibleCardID
CONTRACT["GetSelectedVisibleCardID"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["GetSelectedVisibleCardID"] = [
    {"wram": {wCardListCursorPos: b"\x00", wVisibleListCardIDs: b"\x2A"}, "expect_regs": {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x2A, "hl": 0xCEC4}},
    {"wram": {wCardListCursorPos: b"\x01", wVisibleListCardIDs: b"\x00\x7F"}, "expect_regs": {"a": 0x01, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x7F, "hl": 0xCEC5}},
    dict(POISON, wram={wCardListCursorPos: b"\x02", wVisibleListCardIDs: b"\x00\x00\xEE"}, expect_regs={"a": 0x02, "f": 0x80, "b": 0xBB, "c": 0xCC, "d": 0x00, "e": 0xEE, "hl": 0xCEC6}),
]
# <<< factory GetSelectedVisibleCardID

# >>> factory CheckIfDeckHasCards
CONTRACT["CheckIfDeckHasCards"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfDeckHasCards"] = [
    {"hl": 0xA200, "ramg": False, "sram": {0: {0xA218: b"\x00"}}},
    {"hl": 0xA200, "ramg": False, "sram": {0: {0xA218: b"\x01"}}},
    dict(POISON, hl=0xA200, ramg=False, sram={0: {0xA218: b"\x00"}}),
    {"hl": 0xA200, "sram": {0: {0xA218: b"\xFF"}}},
]
# <<< factory CheckIfDeckHasCards

# >>> factory FillBGMapLineWithA
CONTRACT["FillBGMapLineWithA"] = {"compare": (), "preserve": ()}
CASES["FillBGMapLineWithA"] = [
    {"a": 0x11, "b": 0x00, "c": 0x00, "wram": {0xCAB4: b"\x00"}, "vread": {0: {0x9800: 20}}},
    {"a": 0x22, "b": 0x01, "c": 0x02, "wram": {0xCAB4: b"\x02"}, "vread": {0: {0x9841: 20}, 1: {0x9841: 20}}},
    dict(POISON, a=0xAA, f=0xF0, b=0x03, c=0x04, d=0xDD, e=0xEE, hl=0x1234, wram={0xCAB4: b"\x02"}, vread={0: {0x9883: 20}, 1: {0x9883: 20}}),
]
# <<< factory FillBGMapLineWithA

# >>> factory OpenDeckConfigurationMenu
CONTRACT["OpenDeckConfigurationMenu"] = {"compare": (), "preserve": ()};
CASES["OpenDeckConfigurationMenu"] = [
    {"wram": {0xCE52: b"\xFF", 0xCEA3: b"\xFF"}, "read": {0xCE52: 1, 0xCE53: 2, 0xCE55: 1, 0xCEA3: 1}},
    {"wram": {0xCE52: b"\x01", 0xCEA3: b"\x7F"}, "read": {0xCE52: 1, 0xCE53: 2, 0xCE55: 1, 0xCEA3: 1}},
    dict(POISON, wram={0xCE52: b"\xA5", 0xCEA3: b"\x12"}, read={0xCE52: 1, 0xCE53: 2, 0xCE55: 1, 0xCEA3: 1}),
]
# <<< factory OpenDeckConfigurationMenu

# >>> factory PrintTotalNumberOfCardsInCollection
CONTRACT["PrintTotalNumberOfCardsInCollection"] = {"compare": (), "preserve": ()}
CASES["PrintTotalNumberOfCardsInCollection"] = [
    {"sram": {0: {0xA100: b"\x00" * 255}}, "read": {0xC000: 12, 0xCEB6: 5}},
    {"sram": {0: {0xA100: b"\x00\x01" + b"\x00" * 253}}, "read": {0xC000: 12, 0xCEB6: 5}},
    {"sram": {0: {0xA100: b"\x00\xff" + b"\x00" * 253}}, "read": {0xC000: 12, 0xCEB6: 5}},
    dict(POISON, sram={0: {0xA100: b"\x00\x7f" + b"\x00" * 253}}, read={0xC000: 12, 0xCEB6: 5}),
]
# <<< factory PrintTotalNumberOfCardsInCollection

# >>> factory DrawHorizontalListCursor
CONTRACT["DrawHorizontalListCursor"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawHorizontalListCursor"] = [
    {"a": 0x66,
     "wram": {wCardListCursorPos: b"\x03", wCardListCursorXPos: b"\x04",
              wCardListCursorYPos: b"\x05", wCardListXSpacing: b"\x02"},
     "vread": {0: {0x98AA: 1}}},
    dict(POISON,
         wram={wCardListCursorPos: b"\x04", wCardListCursorXPos: b"\x06",
               wCardListCursorYPos: b"\x07", wCardListXSpacing: b"\x03"},
         vread={0: {0x98FA: 1}}),
]
# <<< factory DrawHorizontalListCursor

# >>> factory GetCountOfCardInCurDeck
CONTRACT["GetCountOfCardInCurDeck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "e", "hl")}
CASES["GetCountOfCardInCurDeck"] = [
    {},
    dict(POISON),
]
# <<< factory GetCountOfCardInCurDeck

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DecrementDeckCardsInCollection
MUTATIONS["DecrementDeckCardsInCollection"] = {
    "source_symbol": "DecrementDeckCardsInCollection",
    "before": "gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));",
    "after": "gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));",
    "case_ids": ["DecrementDeckCardsInCollection-1"],
}
# <<< factory-mutation DecrementDeckCardsInCollection
# >>> factory-mutation AddDeckToCollection
MUTATIONS["AddDeckToCollection"] = {
    "source_symbol": "AddDeckToCollection",
    "before": "gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));",
    "after": "gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));",
    "case_ids": ["AddDeckToCollection-1"],
}
# <<< factory-mutation AddDeckToCollection
# >>> factory-mutation CopyListFromHLToDE
MUTATIONS["CopyListFromHLToDE"] = {
    "source_symbol": "CopyListFromHLToDE",
    "before": "if (a == 0)\n\t\t\tbreak;\n\t\td++;",
    "after": "if (a == 0)\n\t\t\tbreak;\n\t\td += 2u;",
    "case_ids": ["CopyListFromHLToDE-1"],
}
# <<< factory-mutation CopyListFromHLToDE
# >>> factory-mutation CalculateOnesAndTensDigits
MUTATIONS["CalculateOnesAndTensDigits"] = {"source_symbol": "CalculateOnesAndTensDigits", "before": "if (tens != 0u)", "after": "if (tens > 1u)", "case_ids": ["CalculateOnesAndTensDigits-4", "CalculateOnesAndTensDigits-5"]}
# <<< factory-mutation CalculateOnesAndTensDigits
# >>> factory-mutation InitCardSelectionParams
MUTATIONS["InitCardSelectionParams"] = {
    "source_symbol": "InitCardSelectionParams",
    "before": "for (uint8_t i = 0; i < 9u; i++)",
    "after": "for (uint8_t i = 0; i < 8u; i++)",
    "case_ids": ["InitCardSelectionParams-1", "InitCardSelectionParams-2"],
}
# <<< factory-mutation InitCardSelectionParams
# >>> factory-mutation ClearMemory_Bank2
MUTATIONS["ClearMemory_Bank2"] = {"source_symbol": "ClearMemory_Bank2", "before": "uint32_t n = count ? count : 0x100u;", "after": "uint32_t n = count ? count : 0xFFu;", "case_ids": ["ClearMemory_Bank2-0", "ClearMemory_Bank2-1"]}
# <<< factory-mutation ClearMemory_Bank2
# >>> factory-mutation CheckIfHasOtherValidDecks
MUTATIONS["CheckIfHasOtherValidDecks"] = {
    "source_symbol": "CheckIfHasOtherValidDecks",
    "before": "if (gb_read8(hl) == 0)",
    "after": "if (gb_read8(hl) != 0)",
    "case_ids": ["CheckIfHasOtherValidDecks-0", "CheckIfHasOtherValidDecks-1", "CheckIfHasOtherValidDecks-2", "CheckIfHasOtherValidDecks-3"],
}
# <<< factory-mutation CheckIfHasOtherValidDecks
# >>> factory-mutation FillDEWithA
MUTATIONS["FillDEWithA"] = {"source_symbol": "FillDEWithA", "before": "do {\n\t\tgb_write8(address++, a);\n\t} while (--count);", "after": "do {\n\t\tgb_write8(address++, a);\n\t} while (--count > 1u);", "case_ids": ["FillDEWithA-1", "FillDEWithA-3"]}
# <<< factory-mutation FillDEWithA
# >>> factory-mutation DrawHandCardsTileAtDE
MUTATIONS["DrawHandCardsTileAtDE"] = {"source_symbol": "DrawHandCardsTileAtDE", "before": "FillRectangle(0x38u, 2u, 2u, de, 0x0102u);", "after": "FillRectangle(0x39u, 2u, 2u, de, 0x0102u);", "case_ids": ["DrawHandCardsTileAtDE-0", "DrawHandCardsTileAtDE-1", "DrawHandCardsTileAtDE-2"]}
# <<< factory-mutation DrawHandCardsTileAtDE
# >>> factory-mutation CountNumberOfCardsOfType
MUTATIONS["CountNumberOfCardsOfType"] = {
    "source_symbol": "CountNumberOfCardsOfType",
    "before": "uint8_t count = 0;",
    "after": "uint8_t count = 1;",
    "case_ids": ["CountNumberOfCardsOfType-2"],
}
# <<< factory-mutation CountNumberOfCardsOfType
# >>> factory-mutation CopyNBytesFromHLToDE
MUTATIONS["CopyNBytesFromHLToDE"] = {"source_symbol": "CopyNBytesFromHLToDE", "before": "\t\tgb_write8(dst++, gb_read8(src++));", "after": "\t\tgb_write8(dst++, (uint8_t)(gb_read8(src++) + 1u));", "case_ids": ["CopyNBytesFromHLToDE-0", "CopyNBytesFromHLToDE-1", "CopyNBytesFromHLToDE-2", "CopyNBytesFromHLToDE-3"]}
# <<< factory-mutation CopyNBytesFromHLToDE
# >>> factory-mutation IncrementDeckCardsInTempCollection
MUTATIONS["IncrementDeckCardsInTempCollection"] = {"source_symbol": "IncrementDeckCardsInTempCollection", "before": "uint16_t slot = (uint16_t)(bc + card);", "after": "uint16_t slot = (uint16_t)(bc + (uint8_t)(card + 1u));", "case_ids": ["IncrementDeckCardsInTempCollection-0", "IncrementDeckCardsInTempCollection-1", "IncrementDeckCardsInTempCollection-2"]}
# <<< factory-mutation IncrementDeckCardsInTempCollection
# >>> factory-mutation CreateCardCollectionListWithDeckCards
MUTATIONS["CreateCardCollectionListWithDeckCards"] = {"source_symbol": "CreateCardCollectionListWithDeckCards", "before": "IncrementDeckCardsInTempCollection(sDeck1Cards_ADDR);", "after": "IncrementDeckCardsInTempCollection(sDeck2Cards_ADDR);", "case_ids": ["CreateCardCollectionListWithDeckCards-1"]}
# <<< factory-mutation CreateCardCollectionListWithDeckCards
# >>> factory-mutation GetSelectedVisibleCardID
MUTATIONS["GetSelectedVisibleCardID"] = {"source_symbol": "GetSelectedVisibleCardID", "before": "\treturn gb_read8((uint16_t)(wVisibleListCardIDs_ADDR + cursor));", "after": "\treturn gb_read8((uint16_t)(wVisibleListCardIDs_ADDR + cursor + 1u));", "case_ids": ["GetSelectedVisibleCardID-0", "GetSelectedVisibleCardID-1", "GetSelectedVisibleCardID-2"]}
# <<< factory-mutation GetSelectedVisibleCardID
# >>> factory-mutation CheckIfDeckHasCards
MUTATIONS["CheckIfDeckHasCards"] = {"source_symbol": "CheckIfDeckHasCards", "before": "return value == 0u ? 0x90u : 0x00u;", "after": "return value != 0u ? 0x90u : 0x00u;", "case_ids": ["CheckIfDeckHasCards-0", "CheckIfDeckHasCards-1", "CheckIfDeckHasCards-2", "CheckIfDeckHasCards-3"]}
# <<< factory-mutation CheckIfDeckHasCards
# >>> factory-mutation FillBGMapLineWithA
MUTATIONS["FillBGMapLineWithA"] = {"source_symbol": "FillBGMapLineWithA", "before": "	FillDEWithA(0x04u, 20u, de);", "after": "	FillDEWithA(0x05u, 20u, de);", "case_ids": ["FillBGMapLineWithA-1", "FillBGMapLineWithA-2"]}
# <<< factory-mutation FillBGMapLineWithA
# >>> factory-mutation OpenDeckConfigurationMenu
MUTATIONS["OpenDeckConfigurationMenu"] = {"source_symbol": "OpenDeckConfigurationMenu", "before": "gb_write8(wDuelInitialPrizesUpperBitsSet_ADDR, 0xffu);", "after": "gb_write8(wDuelInitialPrizesUpperBitsSet_ADDR, 0xfeu);", "case_ids": ["OpenDeckConfigurationMenu-0"]};
# <<< factory-mutation OpenDeckConfigurationMenu
# >>> factory-mutation PrintTotalNumberOfCardsInCollection
MUTATIONS["PrintTotalNumberOfCardsInCollection"] = {"source_symbol": "PrintTotalNumberOfCardsInCollection", "before": "uint8_t digit = 0u;", "after": "uint8_t digit = 1u;", "case_ids": ["PrintTotalNumberOfCardsInCollection-1", "PrintTotalNumberOfCardsInCollection-3"]}
# <<< factory-mutation PrintTotalNumberOfCardsInCollection
# >>> factory-mutation DrawHorizontalListCursor
MUTATIONS["DrawHorizontalListCursor"] = {
    "source_symbol": "DrawHorizontalListCursor",
    "before": "WriteByteToBGMap0(a, x, y);",
    "after": "WriteByteToBGMap0(a, y, x);",
    "case_ids": ["DrawHorizontalListCursor-0", "DrawHorizontalListCursor-1"],
}
# <<< factory-mutation DrawHorizontalListCursor
# >>> factory-mutation GetCountOfCardInCurDeck
MUTATIONS["GetCountOfCardInCurDeck"] = {"source_symbol": "GetCountOfCardInCurDeck", "before": "\tuint8_t count = 0u;", "after": "\tuint8_t count = 1u;", "case_ids": ["GetCountOfCardInCurDeck-0", "GetCountOfCardInCurDeck-1"]}
# <<< factory-mutation GetCountOfCardInCurDeck
