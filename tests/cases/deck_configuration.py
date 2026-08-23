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

wMenuInputSFX = 0xCFE3
wCheckMenuCursorBlinkCounter = 0xCEA3
wVisibleCursorTile = 0xCEAA
wCardListCursorPos = 0xCEA4
wCardListCursorXPos = 0xCEA5

sCurrentlySelectedDeck = 0xB700

hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
wCardListCursorPos = 0xCEA4
wCardListNumCursorPositions = 0xCEA9
wCheckMenuCursorBlinkCounter = 0xCEA3
wMenuInputSFX = 0xCFE3
hffb3 = 0xFFB3

hDPadHeld = 0xFF8F
wCardListNumCursorPositions = 0xCEA9
wCardListVisibleOffset = 0xCEA1

wDefaultText = 0xC590
sPlayerName = 0xA010
NAME_BUFFER_LENGTH = 0x10
GENERIC_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1, wDefaultText: NAME_BUFFER_LENGTH}
GENERIC_VREAD = {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
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

# >>> factory DrawListCursor
CONTRACT["DrawListCursor"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawListCursor"] = [
    {"a": 0x66,
     "wram": {wCardListCursorPos: b"\x03", wCardListCursorXPos: b"\x04",
              wCardListCursorYPos: b"\x05", wCardListXSpacing: b"\x02",
              0xCEA7: b"\x00"},
     "vread": {0: {0x98AA: 1}}},
    dict(POISON,
         wram={wCardListCursorPos: b"\x04", wCardListCursorXPos: b"\x06",
               wCardListCursorYPos: b"\x07", wCardListXSpacing: b"\x03",
               0xCEA7: b"\x00"},
         vread={0: {0x98F2: 1}}),
]
# <<< factory DrawListCursor

# >>> factory DrawHorizontalListCursor_Invisible
CONTRACT["DrawHorizontalListCursor_Invisible"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawHorizontalListCursor_Invisible"] = [
    {"wram": {0xCEAB: b"\x66", 0xCEA4: b"\x03", 0xCEA5: b"\x04", 0xCEA6: b"\x05", 0xCEA8: b"\x02"},
     "vread": {0: {0x98AA: 1}}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xCEAB: b"\x77", 0xCEA4: b"\x04", 0xCEA5: b"\x06", 0xCEA6: b"\x07", 0xCEA8: b"\x03"},
     "vread": {0: {0x98FA: 1}}},
]
# <<< factory DrawHorizontalListCursor_Invisible

# >>> factory DrawHorizontalListCursor_Visible
CONTRACT["DrawHorizontalListCursor_Visible"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawHorizontalListCursor_Visible"] = [
    {"wram": {0xCEAA: b"\x66", wCardListCursorPos: b"\x03", wCardListCursorXPos: b"\x04",
              wCardListCursorYPos: b"\x05", wCardListXSpacing: b"\x02"},
     "vread": {0: {0x98AA: 1}}},
    dict(POISON,
         wram={0xCEAA: b"\x77", wCardListCursorPos: b"\x04", wCardListCursorXPos: b"\x06",
               wCardListCursorYPos: b"\x07", wCardListXSpacing: b"\x03"},
         vread={0: {0x98FA: 1}}),
]
# <<< factory DrawHorizontalListCursor_Visible

# >>> factory IsCardInAnyDeck
CONTRACT["IsCardInAnyDeck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "c", "d", "e", "hl")}
CASES["IsCardInAnyDeck"] = [
    {"a": 0x01, "f": 0x00, "e": 0x42, "ramg": False, "sram": {0: {0xA218: b"\x00" * 60, 0xA26C: b"\x00" * 60, 0xA2C0: b"\x00\x00\x42" + b"\x00" * 57, 0xA314: b"\x00" * 60}},
     "expect_regs": {"a": 0x01, "f": 0x00, "b": 0x3A, "c": 0x00, "d": 0x00, "e": 0x42, "hl": 0x0000}},
    {"a": 0x00, "f": 0x00, "e": 0x7F, "ramg": False, "sram": {0: {0xA218: b"\x00" * 60, 0xA26C: b"\x00" * 60, 0xA2C0: b"\x00" * 60, 0xA314: b"\x00" * 59 + b"\x7F"}},
     "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x01, "c": 0x00, "d": 0x00, "e": 0x7F, "hl": 0x0000}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "ramg": False, "sram": {0: {0xA218: b"\x00" * 60, 0xA26C: b"\x00" * 60, 0xA2C0: b"\x00" * 60, 0xA314: b"\x00" * 60}},
     "expect_regs": {"a": 0xAA, "f": 0xD0, "b": 0x00, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}},
]
# <<< factory IsCardInAnyDeck

# >>> factory DrawListCursor_Invisible
CONTRACT["DrawListCursor_Invisible"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawListCursor_Invisible"] = [
    {"wram": {0xCEAB: b"\x66", 0xCEA4: b"\x03", 0xCEA5: b"\x04", 0xCEA6: b"\x05", 0xCEA7: b"\x00", 0xCEA8: b"\x02"},
     "vread": {0: {0x98AA: 1}}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xCEAB: b"\x77", 0xCEA4: b"\x04", 0xCEA5: b"\x06", 0xCEA6: b"\x07", 0xCEA7: b"\x00", 0xCEA8: b"\x03"},
     "vread": {0: {0x98F2: 1}}},
]
# <<< factory DrawListCursor_Invisible

# >>> factory DrawListCursor_Visible
CONTRACT["DrawListCursor_Visible"] = {"compare": ("b", "c"), "preserve": ()}
CASES["DrawListCursor_Visible"] = [
    {"wram": {0xCEAA: b"\x66", 0xCEA4: b"\x03", 0xCEA5: b"\x04", 0xCEA6: b"\x05", 0xCEA7: b"\x00", 0xCEA8: b"\x02"},
     "vread": {0: {0x98AA: 1}}},
    dict(POISON,
         wram={0xCEAA: b"\x77", 0xCEA4: b"\x04", 0xCEA5: b"\x06", 0xCEA6: b"\x07", 0xCEA7: b"\x00", 0xCEA8: b"\x03"},
         vread={0: {0x98F2: 1}}),
]
# <<< factory DrawListCursor_Visible

# >>> factory CountNumberOfCardsForEachCardType
CONTRACT["CountNumberOfCardsForEachCardType"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["CountNumberOfCardsForEachCardType"] = [
    {"read": {0xCEBB: 9}},
    dict(POISON, read={0xCEBB: 9}),
]
# <<< factory CountNumberOfCardsForEachCardType

# >>> factory CopyDeckName
CONTRACT["CopyDeckName"] = {"compare": ("hl", "d", "e"), "preserve": (), "wram_out": True}
CASES["CopyDeckName"] = [
    {"hl": 0xA200, "rom_bank": 2, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "sram": {0: {0xA200: b"ABC\x00"}}, "wram": {0xC590: b"\x00" * 16}, "read": {0xC590: 12}},
    dict(POISON, hl=0xA200, rom_bank=2, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], sram={0: {0xA200: b"AB\x00"}}, wram={0xC590: b"\x00" * 16}, read={0xC590: 12}),
]
# <<< factory CopyDeckName

# >>> factory GetOwnedCardCount
CONTRACT["GetOwnedCardCount"] = {"compare": ("a", "d", "e", "hl"), "preserve": ("e", "hl")}
CASES["GetOwnedCardCount"] = [
    {"e": 0x63, "wram": {0xCEDA: b"\x00"}},
    dict(POISON, e=0x63, wram={0xCEDA: b"\x01\x02\x03\x00"}),
    {"e": 0x02, "oracle": False,
     "why": "wOwnedCardsCountList (0xCF68) falls inside $CF00-$CFFF, the oracle's own reserved call frame, so the match branch's real count byte can never be seeded or read live; only the loop index (d) that locates card id 0x02 at position 1 is asserted.",
     "wram": {0xCEDA: b"\x01\x02\x03\x00"},
     "expect_regs": {"d": 0x01}},
]
# <<< factory GetOwnedCardCount

# >>> factory TallyCardsInCardFilterLists
CONTRACT["TallyCardsInCardFilterLists"] = {"compare": ("hl",), "preserve": ()}
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CASES["TallyCardsInCardFilterLists"] = [
    {"wram": {0xCEBB: b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"}, "setup": SETUP_TEXT},
    dict(POISON, wram={0xCEBB: b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"}, setup=SETUP_TEXT),
    {"wram": {0xCEBB: b"\x00\x00\x00\x00\x00\x00\x00\x00\x00"}, "setup": SETUP_TEXT},
]
# <<< factory TallyCardsInCardFilterLists

# >>> factory RemoveCardFromDeck
CONTRACT["RemoveCardFromDeck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["RemoveCardFromDeck"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x01, "hl": 0x4455},
    dict(POISON, e=0x02),
]
# <<< factory RemoveCardFromDeck

# >>> factory CheckIfCurrentDeckWasChanged
CONTRACT["CheckIfCurrentDeckWasChanged"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfCurrentDeckWasChanged"] = [
    {"wram": {0xCECC: b"\x01"}},
    dict(POISON, wram={0xCECC: b"\x01"}),
]
# <<< factory CheckIfCurrentDeckWasChanged

# >>> factory CreateFilteredCardList
CONTRACT["CreateFilteredCardList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CreateFilteredCardList"] = [
    {"a": 0x08, "f": 0x00, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {0xC000: b"\x00" * 240},
     "instruction_budget": 8000000, "cycle_budget": 32000000,
     "read": {0xCEAE: 1}},
    dict(POISON, a=0x08, wram={0xC000: b"\x00" * 240},
         instruction_budget=8000000, cycle_budget=32000000,
         read={0xCEAE: 1}),
]
# <<< factory CreateFilteredCardList

# >>> factory ConfirmSelectionAndReturnCarry
CONTRACT["ConfirmSelectionAndReturnCarry"] = {"compare": ("a", "e"), "preserve": ()}
CASES["ConfirmSelectionAndReturnCarry"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {0xCEA4: b"\x05"},
        "hram": {0xFFB3: b"\x07"},
        "expect_regs": {"a": 0x07, "e": 0x05},
    },
]
# <<< factory ConfirmSelectionAndReturnCarry

# >>> factory AddCardIDToVisibleList
CONTRACT["AddCardIDToVisibleList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl"), "wram_out": True}
CASES["AddCardIDToVisibleList"] = [
    {"b": 2, "e": 0x2A, "wram": {0xCEC4: b"\x00" * 7, 0xCECB: b"\x05"}, "read": {0xCEC4: 7}},
    dict(POISON, b=2, e=0x2A, wram={0xCEC4: b"\x00" * 7, 0xCECB: b"\x05"}, read={0xCEC4: 7}),
]
# <<< factory AddCardIDToVisibleList

# >>> factory HandleCardSelectionCursorBlink
CONTRACT["HandleCardSelectionCursorBlink"] = {"compare": ("b", "c"), "preserve": ()}
CASES["HandleCardSelectionCursorBlink"] = [
    {"wram": {wCheckMenuCursorBlinkCounter: b"\x01"},
     "read": {wCheckMenuCursorBlinkCounter: 1}},
    {"wram": {wCheckMenuCursorBlinkCounter: b"\xF0", wVisibleCursorTile: b"\x77",
              0xCEAB: b"\x66", 0xCEA4: b"\x03", 0xCEA5: b"\x04", 0xCEA6: b"\x05", 0xCEA8: b"\x02"},
     "read": {wCheckMenuCursorBlinkCounter: 1}, "vread": {0: {0x98AA: 1}}},
    dict(POISON, wram={wCheckMenuCursorBlinkCounter: b"\x00", wVisibleCursorTile: b"\x77",
                        0xCEAB: b"\x66", 0xCEA4: b"\x03", 0xCEA5: b"\x04", 0xCEA6: b"\x05", 0xCEA8: b"\x02"},
         read={wCheckMenuCursorBlinkCounter: 1}, vread={0: {0x98AA: 1}}),
]
# <<< factory HandleCardSelectionCursorBlink

# >>> factory DrawHandCardsTileOnCurDeck
CONTRACT["DrawHandCardsTileOnCurDeck"] = {"compare": (), "preserve": ()}
CASES["DrawHandCardsTileOnCurDeck"] = [
    {"sram": {0: {sCurrentlySelectedDeck: b"\x00"}}, "vread": {0: {0x9800: 0x40}}},
    {"sram": {0: {sCurrentlySelectedDeck: b"\x02"}}, "vread": {0: {0x9800: 0x100}}},
    dict(POISON, sram={0: {sCurrentlySelectedDeck: b"\x00"}}, vread={0: {0x9800: 0x40}}),
]
# <<< factory DrawHandCardsTileOnCurDeck

# >>> factory HandleCardSelectionInput
CONTRACT["HandleCardSelectionInput"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HandleCardSelectionInput"] = [
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCardListCursorPos: b"\x02",
              wCardListNumCursorPositions: b"\x04", wCheckMenuCursorBlinkCounter: b"\x01"},
     "read": {hffb3: 1}},
    dict(POISON, wram={hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCardListCursorPos: b"\x03",
                       wCardListNumCursorPositions: b"\x04", wCheckMenuCursorBlinkCounter: b"\x09"},
         read={hffb3: 1}),
]
# <<< factory HandleCardSelectionInput

# >>> factory HandleLeftRightInCardList
CONTRACT["HandleLeftRightInCardList"] = {"compare": ("f",), "preserve": ()}
CASES["HandleLeftRightInCardList"] = [
    {"wram": {hDPadHeld: b"\x00", wCardListNumCursorPositions: b"\x02", wCardListVisibleOffset: b"\x03"}},
    dict(POISON, wram={hDPadHeld: b"\x40", wCardListNumCursorPositions: b"\x02", wCardListVisibleOffset: b"\x03"}),
]
# <<< factory HandleLeftRightInCardList

# >>> factory PrintPlayersCardsText
CONTRACT["PrintPlayersCardsText"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintPlayersCardsText"] = [
    {"wram": {wDefaultText: b"\x00" * NAME_BUFFER_LENGTH},
     "sram": {0: {sPlayerName: bytes([0x81, 0x82, 0x83, 0x00] + [0] * 12)}},
     "setup": SETUP,
     "read": GENERIC_READ, "vread": GENERIC_VREAD},
    dict(POISON, wram={wDefaultText: b"\xFF" * NAME_BUFFER_LENGTH},
         sram={0: {sPlayerName: bytes([0x84, 0x85, 0x00] + [0] * 13)}},
         setup=SETUP,
         read=GENERIC_READ, vread=GENERIC_VREAD),
]
# <<< factory PrintPlayersCardsText

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
# >>> factory-mutation DrawListCursor
MUTATIONS["DrawListCursor"] = {
    "source_symbol": "DrawListCursor",
    "before": "uint8_t x = (uint8_t)((uint8_t)HtimesL(hl) + wCardListCursorXPos);",
    "after": "uint8_t x = (uint8_t)((uint8_t)HtimesL(hl) + wCardListCursorXPos + 1u);",
    "case_ids": ["DrawListCursor-1"],
}
# <<< factory-mutation DrawListCursor
# >>> factory-mutation DrawHorizontalListCursor_Invisible
MUTATIONS["DrawHorizontalListCursor_Invisible"] = {"source_symbol": "DrawHorizontalListCursor_Invisible", "before": "\tuint8_t tile = wInvisibleCursorTile;", "after": "\tuint8_t tile = 0u;", "case_ids": ["DrawHorizontalListCursor_Invisible-0", "DrawHorizontalListCursor_Invisible-1"]}
# <<< factory-mutation DrawHorizontalListCursor_Invisible
# >>> factory-mutation DrawHorizontalListCursor_Visible
MUTATIONS["DrawHorizontalListCursor_Visible"] = {
    "source_symbol": "DrawHorizontalListCursor_Visible",
    "before": "\tuint8_t tile = wVisibleCursorTile;",
    "after": "\tuint8_t tile = 0u;",
    "case_ids": ["DrawHorizontalListCursor_Visible-0", "DrawHorizontalListCursor_Visible-1"],
}
# <<< factory-mutation DrawHorizontalListCursor_Visible
# >>> factory-mutation IsCardInAnyDeck
MUTATIONS["IsCardInAnyDeck"] = {"source_symbol": "IsCardInAnyDeck", "before": "\t\t\tif (card == e) {", "after": "\t\t\tif (card != e) {", "case_ids": ["IsCardInAnyDeck-0", "IsCardInAnyDeck-1", "IsCardInAnyDeck-2"]}
# <<< factory-mutation IsCardInAnyDeck
# >>> factory-mutation DrawListCursor_Invisible
MUTATIONS["DrawListCursor_Invisible"] = {"source_symbol": "DrawListCursor_Invisible", "before": "\tuint8_t tile = wInvisibleCursorTile;\n\treturn DrawListCursor(tile);", "after": "\tuint8_t tile = 0u;\n\treturn DrawListCursor(tile);", "case_ids": ["DrawListCursor_Invisible-0", "DrawListCursor_Invisible-1"]}
# <<< factory-mutation DrawListCursor_Invisible
# >>> factory-mutation DrawListCursor_Visible
MUTATIONS["DrawListCursor_Visible"] = {"source_symbol": "DrawListCursor_Visible", "before": "\tuint8_t tile = wVisibleCursorTile;\n\treturn DrawListCursor(tile);", "after": "\tuint8_t tile = 0u;\n\treturn DrawListCursor(tile);", "case_ids": ["DrawListCursor_Visible-0", "DrawListCursor_Visible-1"]}
# <<< factory-mutation DrawListCursor_Visible
# >>> factory-mutation CountNumberOfCardsForEachCardType
MUTATIONS["CountNumberOfCardsForEachCardType"] = {"source_symbol": "CountNumberOfCardsForEachCardType", "before": "\t\tgb_write8(hl++, CountNumberOfCardsOfType(type));", "after": "\t\tgb_write8(hl++, (uint8_t)(CountNumberOfCardsOfType(type) + 1u));", "case_ids": ["CountNumberOfCardsForEachCardType-0", "CountNumberOfCardsForEachCardType-1"]}
# <<< factory-mutation CountNumberOfCardsForEachCardType
# >>> factory-mutation CopyDeckName
MUTATIONS["CopyDeckName"] = {"source_symbol": "CopyDeckName", "before": "\tuint16_t hl4 = DeckNameSuffix_ADDR;", "after": "\tuint16_t hl4 = (uint16_t)(DeckNameSuffix_ADDR + 1u);", "case_ids": ["CopyDeckName-0", "CopyDeckName-1"]}
# <<< factory-mutation CopyDeckName
# >>> factory-mutation GetOwnedCardCount
MUTATIONS["GetOwnedCardCount"] = {"source_symbol": "GetOwnedCardCount", "before": "\t\tif (a == 0u)\n\t\t\treturn (GetOwnedCardCountResult){0u, d};", "after": "\t\tif (a == 1u)\n\t\t\treturn (GetOwnedCardCountResult){0u, d};", "case_ids": ["GetOwnedCardCount-1"]}
# <<< factory-mutation GetOwnedCardCount
# >>> factory-mutation TallyCardsInCardFilterLists
MUTATIONS["TallyCardsInCardFilterLists"] = {"source_symbol": "TallyCardsInCardFilterLists", "before": "\tif (sum != 0u)", "after": "\tif (sum == 0u)", "case_ids": ["TallyCardsInCardFilterLists-0", "TallyCardsInCardFilterLists-1"]}
# <<< factory-mutation TallyCardsInCardFilterLists
# >>> factory-mutation RemoveCardFromDeck
MUTATIONS["RemoveCardFromDeck"] = {"source_symbol": "RemoveCardFromDeck", "before": "return (RemoveCardFromDeckResult){0u, 0x80u, b, c, d, e, hl};", "after": "return (RemoveCardFromDeckResult){0u, 0x90u, b, c, d, e, hl};", "case_ids": ["RemoveCardFromDeck-0", "RemoveCardFromDeck-1"]}
# <<< factory-mutation RemoveCardFromDeck
# >>> factory-mutation CheckIfCurrentDeckWasChanged
MUTATIONS["CheckIfCurrentDeckWasChanged"] = {"source_symbol": "CheckIfCurrentDeckWasChanged", "before": "return (CheckIfCurrentDeckWasChangedResult){total, 0x10u};", "after": "return (CheckIfCurrentDeckWasChangedResult){total, 0x00u};", "case_ids": ["CheckIfCurrentDeckWasChanged-0", "CheckIfCurrentDeckWasChanged-1"]}
# <<< factory-mutation CheckIfCurrentDeckWasChanged
# >>> factory-mutation CreateFilteredCardList
MUTATIONS["CreateFilteredCardList"] = {"source_symbol": "CreateFilteredCardList", "before": "gb_write8(wNumEntriesInCurFilter_ADDR, (uint8_t)out_index);", "after": "gb_write8(wNumEntriesInCurFilter_ADDR, (uint8_t)(out_index + 1u));", "case_ids": ["CreateFilteredCardList-0", "CreateFilteredCardList-1"]}
# <<< factory-mutation CreateFilteredCardList
# >>> factory-mutation ConfirmSelectionAndReturnCarry
MUTATIONS["ConfirmSelectionAndReturnCarry"] = {
    "source_symbol": "ConfirmSelectionAndReturnCarry",
    "before": "return (ConfirmSelectionAndReturnCarryResult){a, e};",
    "after": "return (ConfirmSelectionAndReturnCarryResult){e, a};",
    "case_ids": ["ConfirmSelectionAndReturnCarry-0"],
}
# <<< factory-mutation ConfirmSelectionAndReturnCarry
# >>> factory-mutation AddCardIDToVisibleList
MUTATIONS["AddCardIDToVisibleList"] = {
    "source_symbol": "AddCardIDToVisibleList",
    "before": "uint8_t offset = (uint8_t)(num_entries - b);",
    "after": "uint8_t offset = (uint8_t)(num_entries + b);",
    "case_ids": ["AddCardIDToVisibleList-0", "AddCardIDToVisibleList-1"],
}
# <<< factory-mutation AddCardIDToVisibleList
# >>> factory-mutation HandleCardSelectionCursorBlink
MUTATIONS["HandleCardSelectionCursorBlink"] = {"source_symbol": "HandleCardSelectionCursorBlink", "before": "\tgb_write8(wCheckMenuCursorBlinkCounter_ADDR, (uint8_t)(counter_old + 1u));", "after": "\tgb_write8(wCheckMenuCursorBlinkCounter_ADDR, counter_old);", "case_ids": ["HandleCardSelectionCursorBlink-0", "HandleCardSelectionCursorBlink-1"]}
# <<< factory-mutation HandleCardSelectionCursorBlink
# >>> factory-mutation DrawHandCardsTileOnCurDeck
MUTATIONS["DrawHandCardsTileOnCurDeck"] = {"source_symbol": "DrawHandCardsTileOnCurDeck", "before": "\tuint8_t e = (uint8_t)((uint8_t)product + 1u);", "after": "\tuint8_t e = (uint8_t)product;", "case_ids": ["DrawHandCardsTileOnCurDeck-0", "DrawHandCardsTileOnCurDeck-1"]}
# <<< factory-mutation DrawHandCardsTileOnCurDeck
# >>> factory-mutation HandleCardSelectionInput
MUTATIONS["HandleCardSelectionInput"] = {"source_symbol": "HandleCardSelectionInput", "before": "\tgb_write8(0xFFB3u, gb_read8(wCardListCursorPos_ADDR));", "after": "\tgb_write8(0xFFB3u, (uint8_t)(gb_read8(wCardListCursorPos_ADDR) + 1u));", "case_ids": ["HandleCardSelectionInput-0", "HandleCardSelectionInput-1"]}
# <<< factory-mutation HandleCardSelectionInput
# >>> factory-mutation HandleLeftRightInCardList
MUTATIONS["HandleLeftRightInCardList"] = {"source_symbol": "HandleLeftRightInCardList", "before": "\t\tuint8_t f = (dpad == 0u) ? 0x80u : 0x00u;", "after": "\t\tuint8_t f = (dpad == 0u) ? 0x00u : 0x80u;", "case_ids": ["HandleLeftRightInCardList-0", "HandleLeftRightInCardList-1"]}
# <<< factory-mutation HandleLeftRightInCardList
# >>> factory-mutation PrintPlayersCardsText
MUTATIONS["PrintPlayersCardsText"] = {"source_symbol": "PrintPlayersCardsText", "before": "InitTextPrinting(1u, 0u);", "after": "InitTextPrinting(2u, 0u);", "case_ids": ["PrintPlayersCardsText-0", "PrintPlayersCardsText-1"]}
# <<< factory-mutation PrintPlayersCardsText
