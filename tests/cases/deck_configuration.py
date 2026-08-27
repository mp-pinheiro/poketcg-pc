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

sCardCollection = 0xA100
wTempCardCollection = 0xC000

wCardFilterCounts = 0xCEBB
wDefaultText = 0xC590
wTotalCardCount = 0xCECC
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wCardCollection = 0xA100
wCardListCoords = 0xCED0
wNumVisibleCardListEntries = 0xCECB

F9_wVisibleListCardIDs = 0xCEC4
F9_wCardListCursorPos = 0xCEA4
F9_wVBlankOAMCopyToggle = 0xCAC0
F9_wLCDC = 0xCABB
F9_rLCDC = 0xFF40
F9_wLoadedCard1 = 0xCC24

wCardListCursorPos = 0xCEA4
wCardListVisibleOffset = 0xCEA1
wMenuInputSFX = 0xCFE3
wTempCardListCursorPos = 0xCED4

hWhoseTurn = 0xFF97
wCurDeckCards = 0xCF17
wDuelTempList = 0xC510
wOpponentDeck = 0xC480
hTempListPtr_ff99 = 0xFF99

wConsole = 0xCAB4
V0_ROW2 = 0x9841
V0_ROW3 = 0x9861
V1_ROW2 = 0x9841
V1_ROW3 = 0x9861
ICON_ROW0 = bytes([0xE4, 0xE5, 0xE0, 0xE1, 0xEC, 0xED, 0xE8, 0xE9, 0xF0, 0xF1, 0xF4, 0xF5, 0xF8, 0xF9, 0xDC, 0xDD, 0xFC, 0xFD])
ICON_ROW1 = bytes([0xE6, 0xE7, 0xE2, 0xE3, 0xEE, 0xEF, 0xEA, 0xEB, 0xF2, 0xF3, 0xF6, 0xF7, 0xFA, 0xFB, 0xDE, 0xDF, 0xFE, 0xFF])
ATTR_ROW = bytes([2, 2, 1, 1, 2, 2, 1, 1, 3, 3, 3, 3, 0, 0, 2, 2, 2, 2])

wCurDeckCards = 0xCF17
wUniqueDeckCardList = 0xCF68
wNumUniqueCards = 0xCED9

wMaxNumCardsAllowed = 0xCFD1

hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
hffb3 = 0xFFB3
wCardListCursorPos = 0xCEA4
wCardListNumCursorPositions = 0xCEA9
wCardListVisibleOffset = 0xCEA1
wCheckMenuCursorBlinkCounter = 0xCEA3
wCardListHandlerFunction = 0xCEAC
wCardListUpdateFunction = 0xCECE
wUnableToScrollDown = 0xCECD
wced2 = 0xCED2
wVisibleCursorTile = 0xCEAA
wMenuInputSFX = 0xCFE3

wCurDeck_PCD = 0xCEB1
wCurDeckName_PCD = 0xCFB9
wDefaultText_PCD = 0xC590
SETUP_PCD = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wNumCardListEntries = 0xCFE6

# HandleDeckConfirmationMenu (deck_configuration.asm:2364). A seed address is
# compared as well as written, so this lists only bytes the reference and the
# port both leave identical: state the body reads, plus buffers it overwrites
# end to end. Nothing the reference VBlank handler touches once EnableLCD
# raises wLCDC ($CABB, seeded 0, raised to $80 on both sides) is seeded or
# read: wVBlankOAMCopyToggle, wFlushPaletteFlags, wVBlankCounter. rom_bank 2
# is the bank the params table ($5EAF) lives in.
HDCM_SEEDS = {
    wTotalCardCount: b"\x01",  # nonzero: takes the menu path, not the empty-deck tail
    0xCFB9: b"\x00",  # wCurDeckName empty skips the deck-name print
    0xCABB: b"\x00",
    hWhoseTurn: b"\xC2",  # saved and restored around SortCurDeckCardsByID
    wCurDeckCards: b"\x01\x00",  # rewritten in place by the sort
    wOpponentDeck: b"\x99\x00",  # sort scratch, overwritten end to end
    wDuelTempList: b"\xFF",
    wCardFilterCounts: b"\x00" * 9,  # PrintTotalCardCount rewrites wTotalCardCount to 0
    wCardListUpdateFunction: b"\x00\x00",
}
HDCM_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# Frame one idles, frame two presses B: the MENU_CANCEL write to hffb3 that
# the `ret z` in .selection_made returns through. A (0x01) instead falls into
# .selected_card and re-enters .init_params forever.
HDCM_KEYS = [0x00, 0x02]
HDCM_READ = {
    wCardListVisibleOffset: 1,  # cleared before .init_params; the re-entry must not clear it again
    wCardListCursorPos: 1,
    wCardListNumCursorPositions: 1,  # clamped to 7 by the .no_cap branch
    hDPadHeld: 1,  # B is still held on the frame the ret fires on
    hffb3: 1,  # MENU_CANCEL at the ret
    wNumVisibleCardListEntries: 1,  # clamped to 7 by the .no_cap branch
    wced2: 1,
    wNumUniqueCards: 1,
    wCardListUpdateFunction: 2,  # $5E31 parked for CallIndirect
    wNumCardListEntries: 1,  # the uncapped unique count
    hWhoseTurn: 1,
}

wTotalCardCount = 0xCECC
wConsole = 0xCAB4
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

# >>> factory AddGiftCenterDeckCardsToCollection
CONTRACT["AddGiftCenterDeckCardsToCollection"] = {"compare": (), "preserve": ()}
CASES["AddGiftCenterDeckCardsToCollection"] = [
    {"hl": 0xC300, "wram": {0xC300: b"\x05\x00"},
     "sram": {0: {sCardCollection: b"\x00" * 255}},
     "read": {sCardCollection + 5: 1, wTempCardCollection + 5: 1}},
    dict(POISON, hl=0xC300, wram={0xC300: b"\x05\x00"},
         sram={0: {sCardCollection: b"\x00" * 255}},
         read={sCardCollection + 5: 1, wTempCardCollection + 5: 1}),
]
# <<< factory AddGiftCenterDeckCardsToCollection

# >>> factory ConvertToNumericalDigits
CONTRACT["ConvertToNumericalDigits"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "c", "d", "e")}
CASES["ConvertToNumericalDigits"] = [
    {"a": 0x2A, "hl": 0xC500, "wram": {0xC500: b"\x00\x00\x00\x00"},
     "expect": {0xC500: b"\x05\x24\x05\x22"}},
    {"a": 17, "hl": 0xC500, "wram": {0xC500: b"\x00\x00\x00\x00"},
     "expect": {0xC500: b"\x05\x21\x05\x27"}},
    dict(POISON, a=17),
]
# <<< factory ConvertToNumericalDigits

# >>> factory CopyListFromHLToDEInSRAM
CONTRACT["CopyListFromHLToDEInSRAM"] = {"compare": ("f", "d", "e", "hl"), "preserve": ()}
CASES["CopyListFromHLToDEInSRAM"] = [
    {"hl": 0xC500, "d": 0xC6, "e": 0x00, "wram": {0xC500: b"\x41\x42\x00", 0xC600: b"\x00\x00\x00"},
     "expect": {0xC600: b"\x41\x42\x00"}, "expect_regs": {"hl": 0xC503, "d": 0xC6, "e": 0x02}},
    dict(POISON, hl=0xC500, d=0xC6, e=0x00, wram={0xC500: b"\x41\x42\x00", 0xC600: b"\x00\x00\x00"}),
]
# <<< factory CopyListFromHLToDEInSRAM

# >>> factory PrintDeckName
CONTRACT["PrintDeckName"] = {"compare": (), "preserve": ()}
CASES["PrintDeckName"] = [
    {"hl": 0xA200, "d": 0x01, "e": 0x08, "sram": {0: {0xA218: b"\x00"}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    {"hl": 0xA200, "d": 0x01, "e": 0x08, "sram": {0: {0xA200: b"AB\x00", 0xA218: b"\x01"}},
     "wram": {0xC590: b"\x00" * 16},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "rom_bank": 2, "read": {0xC590: 8}},
    dict(POISON, hl=0xA200, sram={0: {0xA218: b"\x00"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintDeckName

# >>> factory AppendOwnedCardCountNumber
CONTRACT["AppendOwnedCardCountNumber"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["AppendOwnedCardCountNumber"] = [
    {"hl": 0xC500, "e": 0x63, "wram": {0xC500: b"AB\x00\x00\x00\x00\x00", 0xCEDA: b"\x01\x02\x03\x00"},
     "read": {0xC500: 7}},
    dict(POISON, hl=0xC500, e=0x63, wram={0xC500: b"AB\x00\x00\x00\x00\x00", 0xCEDA: b"\x01\x02\x03\x00"},
         read={0xC500: 7}),
]
# <<< factory AppendOwnedCardCountNumber

# >>> factory PrintNumberValueInCursorYPos
CONTRACT["PrintNumberValueInCursorYPos"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintNumberValueInCursorYPos"] = [
    {"a": 0x05, "wram": {0xCEA7: b"\x01", 0xCEA4: b"\x02", 0xCEA6: b"\x08"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC590: 5},
     "vread": {0: {0x994E: 5}}},
    dict(POISON, a=0x05, wram={0xCEA7: b"\x01", 0xCEA4: b"\x02", 0xCEA6: b"\x08"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC590: 5},
         vread={0: {0x994E: 5}}),
]
# <<< factory PrintNumberValueInCursorYPos

# >>> factory AppendOwnedCardCountAndStorageCountNumbers
CONTRACT["AppendOwnedCardCountAndStorageCountNumbers"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["AppendOwnedCardCountAndStorageCountNumbers"] = [
    {"hl": 0xC500, "e": 0x63, "wram": {0xC500: b"AB\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xCEDA: b"\x01\x02\x03\x00"},
     "read": {0xC500: 12}},
    dict(POISON, hl=0xC500, e=0x63, wram={0xC500: b"AB\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0xCEDA: b"\x01\x02\x03\x00"},
         read={0xC500: 12}),
]
# <<< factory AppendOwnedCardCountAndStorageCountNumbers

# >>> factory PrintCardTypeCounts
CONTRACT["PrintCardTypeCounts"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintCardTypeCounts"] = [
    {"wram": {0xCEBB: bytes([1, 2, 3, 4, 5, 6, 7, 8, 9])},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC590: 37}},
    dict(POISON, wram={0xCEBB: bytes([1, 2, 3, 4, 5, 6, 7, 8, 9])},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC590: 37}),
]
# <<< factory PrintCardTypeCounts

# >>> factory AppendDeckName
CONTRACT["AppendDeckName"] = {"compare": ("f",), "preserve": ()}
CASES["AppendDeckName"] = [
    {"hl": 0xA200, "ramg": False, "sram": {0: {0xA218: b"\x00"}}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0xA200, ramg=False, sram={0: {0xA218: b"\x00"}}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory AppendDeckName

# >>> factory DrawDecksScreen
CONTRACT["DrawDecksScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawDecksScreen"] = [
    {"a": 0x00, "sram": {0: {0xA218: b"\x00", 0xA26C: b"\x00", 0xA2C0: b"\x00", 0xA314: b"\x00", 0xB700: b"\x00"}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "rom_bank": 2,
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "read": {0xCEB2: 4}},
    dict(POISON, a=0x00, sram={0: {0xA218: b"\x00", 0xA26C: b"\x00", 0xA2C0: b"\x00", 0xA314: b"\x00", 0xB700: b"\x00"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], rom_bank=2,
         instruction_budget=2000000, cycle_budget=8000000,
         read={0xCEB2: 4}),
]
# <<< factory DrawDecksScreen

# >>> factory PrintTotalCardCount
CONTRACT["PrintTotalCardCount"] = {"compare": ("d", "e"), "preserve": ("d", "e"), "wram_out": True}
CASES["PrintTotalCardCount"] = [
    {"d": 0x20, "e": 0x40,
     "wram": {wCardFilterCounts: b"\x01\x02\x00\x00\x00\x00\x00\x00\x00", wDefaultText: b"\x00" * 16},
     "setup": SETUP_TEXT, "read": {wTotalCardCount: 1, wDefaultText: 5}},
    dict(POISON, d=0x20, e=0x40,
         wram={wCardFilterCounts: b"\x09\x00\x00\x00\x00\x00\x00\x00\x00", wDefaultText: b"\x00" * 16},
         setup=SETUP_TEXT, read={wTotalCardCount: 1, wDefaultText: 5}),
]
# <<< factory PrintTotalCardCount

# >>> factory RemoveCardFromDeckAndUpdateCount
CONTRACT["RemoveCardFromDeckAndUpdateCount"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["RemoveCardFromDeckAndUpdateCount"] = [
    {"e": 0x01},
    dict(POISON, e=0x02),
]
# <<< factory RemoveCardFromDeckAndUpdateCount

# >>> factory PrintCardSelectionList
CONTRACT["PrintCardSelectionList"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintCardSelectionList"] = [
    {"wram": {0xCED0: b"\x03\x04", 0xCEA1: b"\x00", 0xCECB: b"\x00", 0xCEDA: b"\x00"}, "read": {0xCECD: 1}, "vread": {0: {0x9833: 1, 0x9873: 1}}},
    {"wram": {0xCED0: b"\x03\x04", 0xCEA1: b"\x01", 0xCECB: b"\x00", 0xCEDA: b"\x00\x01"}, "read": {0xCECD: 1}, "vread": {0: {0x9833: 1, 0x9873: 1}}},
    dict(POISON, wram={0xCED0: b"\x03\x04", 0xCEA1: b"\x01", 0xCECB: b"\x00", 0xCEDA: b"\x00\x01"}, read={0xCECD: 1}, vread={0: {0x9833: 1, 0x9873: 1}}),
]
# <<< factory PrintCardSelectionList

# >>> factory PrintFilteredCardSelectionList
CONTRACT["PrintFilteredCardSelectionList"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["PrintFilteredCardSelectionList"] = [
    {"a": 0x00, "f": 0x00, "wram": {0xC000: b"\x00" * 240, 0xCECB: b"\x00"}, "read": {0xCECB: 1}, "instruction_budget": 8000000, "cycle_budget": 32000000},
    dict(POISON, a=0x00, wram={0xC000: b"\x00" * 240, 0xCECB: b"\x00"}, read={0xCECB: 1}, instruction_budget=8000000, cycle_budget=32000000),
    {"a": 0x08, "f": 0x80, "wram": {0xC000: b"\x00" * 240, 0xCECB: b"\x00"}, "read": {0xCECB: 1}, "instruction_budget": 8000000, "cycle_budget": 32000000},
]
# <<< factory PrintFilteredCardSelectionList

# >>> factory PrintDeckBuildingCardList
CONTRACT["PrintDeckBuildingCardList"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintDeckBuildingCardList"] = [
    {"wram": {0xCED0: b"\x03\x04", 0xCEA1: b"\x00", 0xCECB: b"\x00", 0xCEDA: b"\x00"}, "read": {0xCECD: 1}, "vread": {0: {0x9853: 0, 0x9833: 0}}},
    {"wram": {0xCED0: b"\x03\x04", 0xCEA1: b"\x01", 0xCECB: b"\x00", 0xCEDA: b"\x00"}, "read": {0xCECD: 1}, "vread": {0: {0x9853: 0x0C, 0x9833: 0}}},
    dict(POISON, wram={0xCED0: b"\x03\x04", 0xCEA1: b"\x01", 0xCECB: b"\x00", 0xCEDA: b"\x00"}, read={0xCECD: 1}, vread={0: {0x9853: 0x0C, 0x9833: 0}}),
]
# <<< factory PrintDeckBuildingCardList

# >>> factory PrintFilteredCardList
CONTRACT["PrintFilteredCardList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f")}
CASES["PrintFilteredCardList"] = [
    {"a": 0x00, "wram": {0xC000: b"\x00", 0xCECB: b"\x00", 0xCED0: b"\x00\x00"}, "sram": {0: {0xA100: b"\x00" * 0xFF}}, "read": {0xCECB: 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, a=0x00, wram={0xC000: b"\x00", 0xCECB: b"\x00", 0xCED0: b"\x00\x00"}, sram={0: {0xA100: b"\x00" * 0xFF}}, read={0xCECB: 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory PrintFilteredCardList

# >>> factory Func_9ced
CONTRACT["Func_9ced"] = {"compare": (), "preserve": ()}
CASES["Func_9ced"] = [
    # B is the card page's exit key (wCardPageExitKeys), read through hDPadHeld.
    # The card page selects OBJ 8x16, which only touches the wLCDC shadow; the
    # reference's VBlank ISR then mirrors it into rLCDC, so both start at $84.
    {"keys": [0x00, 0x02],
     "wram": {F9_wLCDC: b"\x84", F9_rLCDC: b"\x84",
      F9_wCardListCursorPos: b"\x00",
      F9_wVisibleListCardIDs: b"\x08\x00",
      F9_wVBlankOAMCopyToggle: b"\x00",
      F9_wLoadedCard1: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {F9_wVBlankOAMCopyToggle: 1, F9_wLoadedCard1: 64},
     "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, keys=[0x00, 0x02],
         wram={F9_wLCDC: b"\x84", F9_rLCDC: b"\x84",
         F9_wCardListCursorPos: b"\x00",
         F9_wVisibleListCardIDs: b"\x20\x00",
         F9_wVBlankOAMCopyToggle: b"\x00",
         F9_wLoadedCard1: b"\x00"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={F9_wVBlankOAMCopyToggle: 1, F9_wLoadedCard1: 64},
         instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory Func_9ced

# >>> factory OpenCardPageFromCardList
CONTRACT["OpenCardPageFromCardList"] = {"compare": (), "preserve": ()}
CASES["OpenCardPageFromCardList"] = [
    {"wram": {wCardListCursorPos: b"\x01", wCardListVisibleOffset: b"\x00", wCardListNumCursorPositions: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wTempCardListCursorPos: 1}, "expect": {wTempCardListCursorPos: b"\x01"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wCardListCursorPos: b"\x01", wCardListVisibleOffset: b"\x00", wCardListNumCursorPositions: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wTempCardListCursorPos: 1}, "expect": {wTempCardListCursorPos: b"\x01"}}]
# <<< factory OpenCardPageFromCardList

# >>> factory CheckIfThereAreAnyBasicCardsInDeck
CONTRACT["CheckIfThereAreAnyBasicCardsInDeck"] = {"compare": ("a", "f", "e", "hl"), "preserve": ()}
CASES["CheckIfThereAreAnyBasicCardsInDeck"] = [
    {"wram": {0xCF17: b"\x00"}, "read": {0xCF17: 1}, "expect_regs": {"a": 0x00, "f": 0x80, "e": 0x00, "hl": 0xCF18}},
    {"wram": {0xCF17: b"\x08\x00"}, "read": {0xCF17: 2}, "expect_regs": {"a": 0x00, "f": 0x90, "e": 0x08, "hl": 0xCF18}},
    {"wram": {0xCF17: b"\x01\x00"}, "read": {0xCF17: 2}, "expect_regs": {"a": 0x00, "f": 0x80, "e": 0x00, "hl": 0xCF19}},
    {"wram": {0xCF17: b"\x09\x00"}, "read": {0xCF17: 2}, "expect_regs": {"a": 0x00, "f": 0x80, "e": 0x00, "hl": 0xCF19}},
    dict(POISON, wram={0xCF17: b"\x08\x00"}, read={0xCF17: 2}, expect_regs={"a": 0x00, "f": 0x90, "e": 0x08, "hl": 0xCF18}),
]
# <<< factory CheckIfThereAreAnyBasicCardsInDeck

# >>> factory SortCurDeckCardsByID
CONTRACT["SortCurDeckCardsByID"] = {"compare": ("e",), "preserve": ()}
CASES["SortCurDeckCardsByID"] = [
    {"wram": {hWhoseTurn: b"\xC2", wCurDeckCards: b"\x03\x01\x02\x00", wOpponentDeck: b"\x99\x98\x97\x00", wDuelTempList: b"\xFF"},
     "read": {hWhoseTurn: 1, wCurDeckCards: 4, wOpponentDeck: 4, wDuelTempList: 4, hTempListPtr_ff99: 2}},
    {"wram": {hWhoseTurn: b"\xC3", wCurDeckCards: b"\x04\x00", wOpponentDeck: b"\xA0\x00", wDuelTempList: b"\xFF"},
     "read": {hWhoseTurn: 1, wCurDeckCards: 2, wOpponentDeck: 2, wDuelTempList: 2, hTempListPtr_ff99: 2}},
    {"wram": {hWhoseTurn: b"\xC2", wCurDeckCards: b"\x00", wOpponentDeck: b"\x55\x00", wDuelTempList: b"\xFF"},
     "read": {hWhoseTurn: 1, wCurDeckCards: 1, wOpponentDeck: 2, wDuelTempList: 1, hTempListPtr_ff99: 2}},
    dict(POISON, wram={hWhoseTurn: b"\xC3", wCurDeckCards: b"\x02\x03\x01\x00", wOpponentDeck: b"\xA0\xA1\xA2\x00", wDuelTempList: b"\xFF"},
         read={hWhoseTurn: 1, wCurDeckCards: 4, wOpponentDeck: 4, wDuelTempList: 4, hTempListPtr_ff99: 2}),
]
# <<< factory SortCurDeckCardsByID

# >>> factory GetCardTypeIconPalette
CONTRACT["GetCardTypeIconPalette"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")}
CASES["GetCardTypeIconPalette"] = [
    {"a": 0xe0, "f": 0x00, "b": 0x12, "c": 0x34, "d": 0x56, "e": 0x78, "hl": 0xc100, "expect_regs": {"a": 0x01, "f": 0xc0, "b": 0x12, "c": 0x34, "d": 0x56, "e": 0x78, "hl": 0xc100}},
    {"a": 0xf8, "f": 0xf0, "b": 0xaa, "c": 0xbb, "d": 0xcc, "e": 0xdd, "hl": 0xc200, "expect_regs": {"a": 0x00, "f": 0xc0, "b": 0xaa, "c": 0xbb, "d": 0xcc, "e": 0xdd, "hl": 0xc200}},
    {"a": 0x01, "f": 0x10, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0xc300, "expect_regs": {"a": 0xff, "f": 0x80, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0xc300}},
    {"a": 0x00, "f": 0xff, "b": 0x01, "c": 0x02, "d": 0x03, "e": 0x04, "hl": 0xc400, "expect_regs": {"a": 0xff, "f": 0x80, "b": 0x01, "c": 0x02, "d": 0x03, "e": 0x04, "hl": 0xc400}},
    dict(POISON, expect_regs={"a": 0xff, "f": 0x80, "b": 0xbb, "c": 0xcc, "d": 0xdd, "e": 0xee, "hl": 0x1234}),
]
# <<< factory GetCardTypeIconPalette

# >>> factory DrawCardTypeIcons
CONTRACT["DrawCardTypeIcons"] = {"compare": (), "preserve": ()}
CASES["DrawCardTypeIcons"] = [
    {"wram": {wConsole: b"\x00"},
     "vram": {0: {V0_ROW2: bytes(18), V0_ROW3: bytes(18)}},
     "expect_vram": {0: {V0_ROW2: ICON_ROW0, V0_ROW3: ICON_ROW1}},
     "instruction_budget": 100000, "cycle_budget": 400000},
    dict(POISON, wram={wConsole: b"\x02"},
         vram={0: {V0_ROW2: bytes(18), V0_ROW3: bytes(18)}, 1: {V1_ROW2: bytes(18), V1_ROW3: bytes(18)}},
         expect_vram={0: {V0_ROW2: ICON_ROW0, V0_ROW3: ICON_ROW1}, 1: {V1_ROW2: ATTR_ROW, V1_ROW3: ATTR_ROW}},
         instruction_budget=100000, cycle_budget=400000),
]
# <<< factory DrawCardTypeIcons

# >>> factory PrintPlayersCardsHeaderInfo
CONTRACT["PrintPlayersCardsHeaderInfo"] = {"compare": (), "preserve": ()}
CASES["PrintPlayersCardsHeaderInfo"] = [
    {"wram": {0xCAB4: b"\x00", 0xCAB6: b"\xFF", 0xCAC0: b"\x00", 0xCABB: b"\x00"},
     "sram": {0: {0xA100: b"\x00" * 255, 0xA010: bytes([0x81, 0x82, 0x00] + [0] * 13)}},
     "read": {0xCAB6: 1, 0xCAC0: 1, 0xCABB: 1},
     "vread": {0: {0x9880: 20}}},
    dict(POISON, wram={0xCAB4: b"\x00", 0xCAB6: b"\xFF", 0xCAC0: b"\x00", 0xCABB: b"\x00"},
         sram={0: {0xA100: b"\x00\x01" + b"\x00" * 253, 0xA010: bytes([0x84, 0x85, 0x00] + [0] * 13)}},
         read={0xCAB6: 1, 0xCAC0: 1, 0xCABB: 1},
         vread={0: {0x9880: 20}}),
]
# <<< factory PrintPlayersCardsHeaderInfo

# >>> factory PrintConfirmationCardList
CONTRACT["PrintConfirmationCardList"] = {"compare": (), "preserve": ()}
CASES["PrintConfirmationCardList"] = [
    {"a": 0x00, "d": 0x00, "e": 0x00, "hl": 0xC100, "wram": {0xCECB: b"\x00", 0xCED0: b"\x05\x02"}, "read": {0xCECD: 1}, "expect": {0xCECD: b"\x01"}},
    dict(POISON, wram={0xCECB: b"\x00", 0xCED0: b"\x05\x02"}, read={0xCECD: 1}, expect={0xCECD: b"\x01"}),
]
# <<< factory PrintConfirmationCardList

# >>> factory CreateCurDeckUniqueCardList
CONTRACT["CreateCurDeckUniqueCardList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["CreateCurDeckUniqueCardList"] = [
    {"wram": {wCurDeckCards: b"\x01\x00"}, "read": {wCurDeckCards: 2, wUniqueDeckCardList: 2, wNumUniqueCards: 1}},
    {"wram": {wCurDeckCards: b"\x01\x01\x02\x02\x00"}, "read": {wCurDeckCards: 5, wUniqueDeckCardList: 3, wNumUniqueCards: 1}},
    {"wram": {wCurDeckCards: b"\xE4\xE4\x03\x00"}, "read": {wCurDeckCards: 4, wUniqueDeckCardList: 3, wNumUniqueCards: 1}},
    dict(POISON, wram={wCurDeckCards: b"\x05\x05\x07\x05\x00"}, read={wCurDeckCards: 5, wUniqueDeckCardList: 4, wNumUniqueCards: 1}),
]
# <<< factory CreateCurDeckUniqueCardList

# >>> factory TryAddCardToDeck
CONTRACT["TryAddCardToDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TryAddCardToDeck"] = [
    {"wram": {0xCECC: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x90}},
    {"e": 0x01, "wram": {0xCECC: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x90}},
    dict(POISON, e=0xE4, wram={0xCECC: b"\x00"}, expect_regs={"a": 0x00, "f": 0x90}),
]
# <<< factory TryAddCardToDeck

# >>> factory AddCardToDeckAndUpdateCount
CONTRACT["AddCardToDeckAndUpdateCount"] = {"compare": ("a", "f", "e"), "preserve": ("e",)}
CASES["AddCardToDeckAndUpdateCount"] = [
    {"e": 0x01, "wram": {0xCECC: b"\x00", 0xCFD1: b"\x00"}},
    dict(POISON, e=0x01, wram={0xCECC: b"\x00", 0xCFD1: b"\x00"}),
]
# <<< factory AddCardToDeckAndUpdateCount

# >>> factory HandleDeckCardSelectionList
CONTRACT["HandleDeckCardSelectionList"] = {"compare": (), "preserve": ()}
CASES["HandleDeckCardSelectionList"] = [
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCardListCursorPos: b"\x02", wCardListHandlerFunction: b"\x00", wCheckMenuCursorBlinkCounter: b"\x01"}, "read": {hffb3: 1}},
    {"wram": {hDPadHeld: b"\x40", hKeysPressed: b"\x00", wCardListCursorPos: b"\x02", wCardListNumCursorPositions: b"\x04", wCardListVisibleOffset: b"\x01", wCardListHandlerFunction: b"\x00", wCheckMenuCursorBlinkCounter: b"\x01"}, "read": {hffb3: 1}},
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x01", wCardListCursorPos: b"\x03", wCardListHandlerFunction: b"\x00", wCheckMenuCursorBlinkCounter: b"\x01"}, "read": {hffb3: 1}},
    dict(POISON, wram={hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCardListCursorPos: b"\x03", wCardListHandlerFunction: b"\x00", wCheckMenuCursorBlinkCounter: b"\x09"}, read={hffb3: 1}),
]
# <<< factory HandleDeckCardSelectionList

# >>> factory PrintCurDeckNumberAndName
CONTRACT["PrintCurDeckNumberAndName"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintCurDeckNumberAndName"] = [
    {"rom_bank": 2, "wram": {wCurDeck_PCD: b"\xFF", wCurDeckName_PCD: b"\x00", wDefaultText_PCD: b"\x00" * 16},
     "setup": SETUP_PCD, "read": {wDefaultText_PCD: 1}},
    {"rom_bank": 2, "wram": {wCurDeck_PCD: b"\x00", wCurDeckName_PCD: b"AB\x00", wDefaultText_PCD: b"\x00" * 16},
     "setup": SETUP_PCD, "read": {wDefaultText_PCD: 8}},
    {"rom_bank": 2, "wram": {wCurDeck_PCD: b"\x80", wCurDeckName_PCD: b"CDE\x00", wDefaultText_PCD: b"\x00" * 16},
     "setup": SETUP_PCD, "read": {wDefaultText_PCD: 9}},
    dict(POISON, rom_bank=2, wram={wCurDeck_PCD: b"\x01", wCurDeckName_PCD: b"XY\x00", wDefaultText_PCD: b"\x00" * 16},
         setup=SETUP_PCD, read={wDefaultText_PCD: 8}),
]
# <<< factory PrintCurDeckNumberAndName

# >>> factory UpdateConfirmationCardScreen
CONTRACT["UpdateConfirmationCardScreen"] = {"compare": (), "preserve": ()}
CASES["UpdateConfirmationCardScreen"] = [
    {"rom_bank": 2, "wram": {0xCEB1: b"\xFF", 0xCFB9: b"\x00", 0xC590: b"\x00" * 16, 0xCECB: b"\x00", 0xCED0: b"\x05\x02"}, "setup": SETUP_PCD, "read": {0xC590: 1, 0xCECD: 1, 0xFFB0: 1}},
    {"rom_bank": 2, "wram": {0xCEB1: b"\x00", 0xCFB9: b"AB\x00", 0xC590: b"\x00" * 16, 0xCECB: b"\x00", 0xCED0: b"\x05\x02"}, "setup": SETUP_PCD, "read": {0xC590: 8, 0xCECD: 1, 0xFFB0: 1}},
    dict(POISON, rom_bank=2, wram={0xCEB1: b"\xFF", 0xCFB9: b"\x00", 0xC590: b"\x00" * 16, 0xCECB: b"\x00", 0xCED0: b"\x05\x02"}, setup=SETUP_PCD, read={0xC590: 1, 0xCECD: 1, 0xFFB0: 1}),
]
# <<< factory UpdateConfirmationCardScreen

# >>> factory PrintSlashSixty
CONTRACT["PrintSlashSixty"] = {"compare": (), "preserve": ()}
CASES["PrintSlashSixty"] = [
    {"d": 17, "e": 0, "read": {0xC590: 7}, "vread": {0: {0x9811: 3}},
     "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}]},
    {"d": 16, "e": 1, "read": {0xC590: 7}, "vread": {0: {0x9830: 3}},
     "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}]},
    dict(POISON, d=17, e=0, read={0xC590: 7}, vread={0: {0x9811: 3}},
         setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}]),
]
# <<< factory PrintSlashSixty

# >>> factory ShowDeckInfoHeader
CONTRACT["ShowDeckInfoHeader"] = {"compare": (), "preserve": ()}
CASES["ShowDeckInfoHeader"] = [
    {"wram": {0xCFB9: b"\x00", 0xCABB: b"\x00"},
     "sram": {0: {}}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "vread": {0: {0x9821: 4}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xCFB9: b"\x01\x00", 0xCEB1: b"\x00", 0xCABB: b"\x00"},
         sram={0: {0xB700: b"\x00"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         vread={0: {0x9821: 4}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory ShowDeckInfoHeader

# >>> factory DrawCardTypeIconsAndPrintCardCounts
CONTRACT["DrawCardTypeIconsAndPrintCardCounts"] = {"compare": (), "preserve": ()}
CASES["DrawCardTypeIconsAndPrintCardCounts"] = [
    {"wram": {wConsole: b"\x00"}, "setup": SETUP_TEXT, "vread": {0: {0x98A0: 20}}, "instruction_budget": 100000, "cycle_budget": 400000},
    dict(POISON, wram={wConsole: b"\x00"}, setup=SETUP_TEXT, vread={0: {0x98A0: 20}}, instruction_budget=100000, cycle_budget=400000),
]
# <<< factory DrawCardTypeIconsAndPrintCardCounts

# >>> factory ShowConfirmationCardScreen
CONTRACT["ShowConfirmationCardScreen"] = {"compare": (), "preserve": ()}
CASES["ShowConfirmationCardScreen"] = [
    {"rom_bank": 2, "wram": {0xCFB9: b"\x00", 0xCABB: b"\x00", 0xCECB: b"\x00", 0xCED0: b"\x00\x00"}, "sram": {0: {}}, "setup": SETUP_PCD, "read": {0xCED0: 2}, "expect": {0xCED0: b"\x05\x03"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "rom_bank": 2, "wram": {0xCFB9: b"\x00", 0xCABB: b"\x00", 0xCECB: b"\x00", 0xCED0: b"\x00\x00"}, "sram": {0: {}}, "setup": SETUP_PCD, "read": {0xCED0: 2}, "expect": {0xCED0: b"\x05\x03"}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory ShowConfirmationCardScreen

# >>> factory ShowDeckInfoHeaderAndWaitForBButton
CONTRACT["ShowDeckInfoHeaderAndWaitForBButton"] = {"compare": (), "preserve": ()}
CASES["ShowDeckInfoHeaderAndWaitForBButton"] = [
    {"wram": {0xCFB9: b"\x00", 0xCABB: b"\x00"},
     "sram": {0: {}},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x02],
     "vread": {0: {0x9821: 4}},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCFB9: b"\x01\x00", 0xCEB1: b"\x00", 0xCABB: b"\x00"},
         sram={0: {0xB700: b"\x00"}},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x02],
         vread={0: {0x9821: 4}},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ShowDeckInfoHeaderAndWaitForBButton

# >>> factory HandleDeckConfirmationMenu
CONTRACT["HandleDeckConfirmationMenu"] = {"compare": (), "preserve": ()}
CASES["HandleDeckConfirmationMenu"] = [
    # Empty deck: the `jp z` hands the whole body to
    # ShowDeckInfoHeaderAndWaitForBButton, whose callee-`ret` returns straight
    # to this routine's caller.
    {"wram": {wTotalCardCount: b"\x00", 0xCFB9: b"\x00", 0xCABB: b"\x00"},
     "sram": {0: {}}, "keys": HDCM_KEYS, "rom_bank": 2, "setup": HDCM_SETUP,
     "vread": {0: {0x9821: 4}},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    # One-card deck: sort + unique list + one visible entry; B cancels on
    # frame two and the `ret z` fires with hffb3 = MENU_CANCEL.
    {"wram": {**HDCM_SEEDS}, "sram": {0: {}}, "keys": HDCM_KEYS, "rom_bank": 2,
     "setup": HDCM_SETUP,
     "read": {**HDCM_READ, wCurDeckCards: 2, wUniqueDeckCardList: 2},
     "vread": {0: {0x9821: 4}},
     "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={**HDCM_SEEDS}, sram={0: {}}, keys=HDCM_KEYS, rom_bank=2,
         setup=HDCM_SETUP,
         read={**HDCM_READ, wCurDeckCards: 2, wUniqueDeckCardList: 2},
         vread={0: {0x9821: 4}},
         instruction_budget=20000000, cycle_budget=100000000),
    # Eight unique cards: wNumUniqueCards ($08) crosses
    # NUM_DECK_CONFIRMATION_VISIBLE_CARDS, so .no_cap is skipped, both cursor
    # byte stores clamp to 7 while wNumCardListEntries keeps the raw 8.
    {"wram": {**HDCM_SEEDS, wCurDeckCards: bytes([8, 1, 2, 3, 4, 5, 6, 7, 0])},
     "sram": {0: {}}, "keys": HDCM_KEYS, "rom_bank": 2, "setup": HDCM_SETUP,
     "read": {**HDCM_READ, wCurDeckCards: 9, wUniqueDeckCardList: 9},
     "instruction_budget": 20000000, "cycle_budget": 100000000},
]
# <<< factory HandleDeckConfirmationMenu

# >>> factory ConfirmDeckConfiguration
CONTRACT["ConfirmDeckConfiguration"] = {"compare": (), "preserve": ()}
CASES["ConfirmDeckConfiguration"] = [
    {"a": 0x00, "f": 0x00, "wram": {0xCECC: b"\x00", 0xCFB9: b"\x00", 0xCABB: b"\x00", 0xCEA1: b"\x33", 0xCAB4: b"\x00"}, "sram": {0: {}}, "keys": [0x00, 0x02], "rom_bank": 2, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xCEA1: 1, 0xCED8: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={0xCECC: b"\x00", 0xCFB9: b"\x00", 0xCABB: b"\x00", 0xCEA1: b"\x33", 0xCAB4: b"\x00"}, sram={0: {}}, keys=[0x00, 0x02], rom_bank=2, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xCEA1: 1, 0xCED8: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory ConfirmDeckConfiguration

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
# >>> factory-mutation AddGiftCenterDeckCardsToCollection
MUTATIONS["AddGiftCenterDeckCardsToCollection"] = {"source_symbol": "AddGiftCenterDeckCardsToCollection", "before": "uint16_t addr = (uint16_t)(sCardCollection_ADDR + card);\n\t\tuint8_t owned = gb_read8(addr);\n\t\tif (owned == CARD_NOT_OWNED)\n\t\t\tgb_write8(addr, 0u);\n\t\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));", "after": "uint16_t addr = (uint16_t)(sCardCollection_ADDR + card);\n\t\tuint8_t owned = gb_read8(addr);\n\t\tif (owned == CARD_NOT_OWNED)\n\t\t\tgb_write8(addr, 0u);\n\t\tgb_write8(addr, gb_read8(addr));", "case_ids": ["AddGiftCenterDeckCardsToCollection-0", "AddGiftCenterDeckCardsToCollection-1"]}
# <<< factory-mutation AddGiftCenterDeckCardsToCollection
# >>> factory-mutation ConvertToNumericalDigits
MUTATIONS["ConvertToNumericalDigits"] = {"source_symbol": "ConvertToNumericalDigits", "before": "gb_write8(hl, tens);", "after": "gb_write8(hl, ones);", "case_ids": ["ConvertToNumericalDigits-0", "ConvertToNumericalDigits-1"]}
# <<< factory-mutation ConvertToNumericalDigits
# >>> factory-mutation CopyListFromHLToDEInSRAM
MUTATIONS["CopyListFromHLToDEInSRAM"] = {"source_symbol": "CopyListFromHLToDEInSRAM", "before": "EnableSRAM();\n\tCopyListFromHLToDE(&hl, &de);", "after": "EnableSRAM();\n\tCopyListFromHLToDE(&de, &hl);", "case_ids": ["CopyListFromHLToDEInSRAM-0"]}
# <<< factory-mutation CopyListFromHLToDEInSRAM
# >>> factory-mutation PrintDeckName
MUTATIONS["PrintDeckName"] = {"source_symbol": "PrintDeckName", "before": "uint16_t suffix_dst = (uint16_t)(wDefaultText_ADDR + len.c);", "after": "uint16_t suffix_dst = (uint16_t)(wDefaultText_ADDR + len.c + 1u);", "case_ids": ["PrintDeckName-1"]}
# <<< factory-mutation PrintDeckName
# >>> factory-mutation AppendOwnedCardCountNumber
MUTATIONS["AppendOwnedCardCountNumber"] = {"source_symbol": "AppendOwnedCardCountNumber", "before": "\twhile (gb_read8(walk) != 0u) {", "after": "\twhile (gb_read8(walk) != 1u) {", "case_ids": ["AppendOwnedCardCountNumber-0", "AppendOwnedCardCountNumber-1"]}
# <<< factory-mutation AppendOwnedCardCountNumber
# >>> factory-mutation PrintNumberValueInCursorYPos
MUTATIONS["PrintNumberValueInCursorYPos"] = {"source_symbol": "PrintNumberValueInCursorYPos", "before": "\tuint8_t e = (uint8_t)(lo + cursor_y);", "after": "\tuint8_t e = (uint8_t)(lo + cursor_y + 1u);", "case_ids": ["PrintNumberValueInCursorYPos-0", "PrintNumberValueInCursorYPos-1"]}
# <<< factory-mutation PrintNumberValueInCursorYPos
# >>> factory-mutation AppendOwnedCardCountAndStorageCountNumbers
MUTATIONS["AppendOwnedCardCountAndStorageCountNumbers"] = {"source_symbol": "AppendOwnedCardCountAndStorageCountNumbers", "before": "gb_write8(walk, SYM_SLASH);", "after": "gb_write8(walk, TX_SYMBOL);", "case_ids": ["AppendOwnedCardCountAndStorageCountNumbers-0", "AppendOwnedCardCountAndStorageCountNumbers-1"]}
# <<< factory-mutation AppendOwnedCardCountAndStorageCountNumbers
# >>> factory-mutation PrintCardTypeCounts
MUTATIONS["PrintCardTypeCounts"] = {"source_symbol": "PrintCardTypeCounts", "before": "\t\tuint8_t count = gb_read8((uint16_t)(wCardFilterCounts_ADDR + c));", "after": "\t\tuint8_t count = gb_read8((uint16_t)(wCardFilterCounts_ADDR + c + 1u));", "case_ids": ["PrintCardTypeCounts-0", "PrintCardTypeCounts-1"]}
# <<< factory-mutation PrintCardTypeCounts
# >>> factory-mutation AppendDeckName
MUTATIONS["AppendDeckName"] = {"source_symbol": "AppendDeckName", "before": "\tif (no_cards & 0x10u) {", "after": "\tif (no_cards & 0x20u) {", "case_ids": ["AppendDeckName-0", "AppendDeckName-1"]}
# <<< factory-mutation AppendDeckName
# >>> factory-mutation DrawDecksScreen
MUTATIONS["DrawDecksScreen"] = {"source_symbol": "DrawDecksScreen", "before": "\tif (!(nc1 & 0x10u)) {\n\t\twDeck1Valid = TRUE;", "after": "\tif ((nc1 & 0x10u)) {\n\t\twDeck1Valid = TRUE;", "case_ids": ["DrawDecksScreen-0", "DrawDecksScreen-1"]}
# <<< factory-mutation DrawDecksScreen
# >>> factory-mutation PrintTotalCardCount
MUTATIONS["PrintTotalCardCount"] = {"source_symbol": "PrintTotalCardCount", "before": "uint8_t value = gb_read8(hl);\n\t\tsum = (uint8_t)(value + sum);", "after": "uint8_t value = gb_read8((uint16_t)(hl + 1u));\n\t\tsum = (uint8_t)(value + sum);", "case_ids": ["PrintTotalCardCount-0", "PrintTotalCardCount-1"]}
# <<< factory-mutation PrintTotalCardCount
# >>> factory-mutation RemoveCardFromDeckAndUpdateCount
MUTATIONS["RemoveCardFromDeckAndUpdateCount"] = {"source_symbol": "RemoveCardFromDeckAndUpdateCount", "before": "\t\treturn (RemoveCardFromDeckAndUpdateCountResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};", "after": "\t\treturn (RemoveCardFromDeckAndUpdateCountResult){r.a, r.f, r.b, r.c, r.c, r.e, r.hl};", "case_ids": ["RemoveCardFromDeckAndUpdateCount-1"]}
# <<< factory-mutation RemoveCardFromDeckAndUpdateCount
# >>> factory-mutation PrintCardSelectionList
MUTATIONS["PrintCardSelectionList"] = {
    "source_symbol": "PrintCardSelectionList",
    "before": "\t\ttile = SYM_CURSOR_U;",
    "after": "\t\ttile = SYM_CURSOR_D;",
    "case_ids": ["PrintCardSelectionList-1", "PrintCardSelectionList-2"],
}
# <<< factory-mutation PrintCardSelectionList
# >>> factory-mutation PrintFilteredCardSelectionList
MUTATIONS["PrintFilteredCardSelectionList"] = {"source_symbol": "PrintFilteredCardSelectionList", "before": "\tgb_write8(wNumVisibleCardListEntries_ADDR, NUM_DECK_CONFIRMATION_VISIBLE_CARDS);", "after": "\tgb_write8(wNumVisibleCardListEntries_ADDR, 0x06u);", "case_ids": ["PrintFilteredCardSelectionList-0", "PrintFilteredCardSelectionList-1"]}
# <<< factory-mutation PrintFilteredCardSelectionList
# >>> factory-mutation PrintDeckBuildingCardList
MUTATIONS["PrintDeckBuildingCardList"] = {
    "source_symbol": "PrintDeckBuildingCardList",
    "before": "\tuint8_t tile = (wCardListVisibleOffset != 0u) ? SYM_CURSOR_U : SYM_SPACE;",
    "after": "\tuint8_t tile = (wCardListVisibleOffset != 0u) ? SYM_CURSOR_D : SYM_SPACE;",
    "case_ids": ["PrintDeckBuildingCardList-1", "PrintDeckBuildingCardList-2"],
}
# <<< factory-mutation PrintDeckBuildingCardList
# >>> factory-mutation PrintFilteredCardList
MUTATIONS["PrintFilteredCardList"] = {
    "source_symbol": "PrintFilteredCardList",
    "before": "\tgb_write8(wNumVisibleCardListEntries_ADDR, NUM_FILTERED_LIST_VISIBLE_CARDS);",
    "after": "\tgb_write8(wNumVisibleCardListEntries_ADDR, 0x00u);",
    "case_ids": ["PrintFilteredCardList-0", "PrintFilteredCardList-1"],
}
# <<< factory-mutation PrintFilteredCardList
# >>> factory-mutation Func_9ced
MUTATIONS["Func_9ced"] = {
 "source_symbol": "Func_9ced",
 "before": "\tLoadCardDataToBuffer1_FromCardID(e);",
 "after": "\tLoadCardDataToBuffer1_FromCardID((uint8_t)(e + 1u));",
 "case_ids": ["Func_9ced-0", "Func_9ced-1"],
}
# <<< factory-mutation Func_9ced
# >>> factory-mutation OpenCardPageFromCardList
MUTATIONS["OpenCardPageFromCardList"] = {"source_symbol": "OpenCardPageFromCardList", "before": "\twTempCardListCursorPos = cursor;", "after": "\twTempCardListCursorPos = 0u;", "case_ids": ["OpenCardPageFromCardList-0", "OpenCardPageFromCardList-1"]}
# <<< factory-mutation OpenCardPageFromCardList
# >>> factory-mutation CheckIfThereAreAnyBasicCardsInDeck
MUTATIONS["CheckIfThereAreAnyBasicCardsInDeck"] = {"source_symbol": "CheckIfThereAreAnyBasicCardsInDeck", "before": "CheckIfThereAreAnyBasicCardsInDeck(void)\n{\n\tuint16_t hl = wCurDeckCards_ADDR;\n\tfor (;;) {\n\t\tuint8_t card = gb_read8(hl++);\n\t\tif (card == 0u)", "after": "CheckIfThereAreAnyBasicCardsInDeck(void)\n{\n\tuint16_t hl = wCurDeckCards_ADDR;\n\tfor (;;) {\n\t\tuint8_t card = gb_read8(hl++);\n\t\tif (card == 8u)", "case_ids": ["CheckIfThereAreAnyBasicCardsInDeck-1", "CheckIfThereAreAnyBasicCardsInDeck-4"]}
# <<< factory-mutation CheckIfThereAreAnyBasicCardsInDeck
# >>> factory-mutation SortCurDeckCardsByID
MUTATIONS["SortCurDeckCardsByID"] = {"source_symbol": "SortCurDeckCardsByID", "before": "SortCurDeckCardsByIDResult SortCurDeckCardsByID(void)\n{\n\tuint16_t src = wCurDeckCards_ADDR;", "after": "SortCurDeckCardsByIDResult SortCurDeckCardsByID(void)\n{\n\tuint16_t src = wOpponentDeck_ADDR;", "case_ids": ["SortCurDeckCardsByID-0", "SortCurDeckCardsByID-1", "SortCurDeckCardsByID-2", "SortCurDeckCardsByID-3"]}
# <<< factory-mutation SortCurDeckCardsByID
# >>> factory-mutation GetCardTypeIconPalette
MUTATIONS["GetCardTypeIconPalette"] = {"source_symbol": "GetCardTypeIconPalette", "before": "\tuint8_t palette = 0xffu;", "after": "\tuint8_t palette = 0x00u;", "case_ids": ["GetCardTypeIconPalette-2", "GetCardTypeIconPalette-4"]}
# <<< factory-mutation GetCardTypeIconPalette
# >>> factory-mutation DrawCardTypeIcons
MUTATIONS["DrawCardTypeIcons"] = {
    "source_symbol": "DrawCardTypeIcons",
    "before": "\t\tuint8_t tile = icons[i];",
    "after": "\t\tuint8_t tile = icons[(uint8_t)(i + 1u)];",
    "case_ids": ["DrawCardTypeIcons-1"],
}
# <<< factory-mutation DrawCardTypeIcons
# >>> factory-mutation PrintPlayersCardsHeaderInfo
MUTATIONS["PrintPlayersCardsHeaderInfo"] = {"source_symbol": "PrintPlayersCardsHeaderInfo", "before": "\tFillBGMapLineWithA(0x1Cu, 0u, 4u);", "after": "\tFillBGMapLineWithA(0x1Du, 0u, 4u);", "case_ids": ["PrintPlayersCardsHeaderInfo-0", "PrintPlayersCardsHeaderInfo-1"]}
# <<< factory-mutation PrintPlayersCardsHeaderInfo
# >>> factory-mutation PrintConfirmationCardList
MUTATIONS["PrintConfirmationCardList"] = {"source_symbol": "PrintConfirmationCardList", "before": "/* PrintConfirmationCardList: set scroll guard */\n\t\twUnableToScrollDown = 1u;", "after": "/* PrintConfirmationCardList: set scroll guard */\n\t\twUnableToScrollDown = 0u;", "case_ids": ["PrintConfirmationCardList-0", "PrintConfirmationCardList-1"]}
# <<< factory-mutation PrintConfirmationCardList
# >>> factory-mutation CreateCurDeckUniqueCardList
MUTATIONS["CreateCurDeckUniqueCardList"] = {"source_symbol": "CreateCurDeckUniqueCardList", "before": "CreateCurDeckUniqueCardListResult CreateCurDeckUniqueCardList(void)\n{\n\tuint8_t count = 0u;", "after": "CreateCurDeckUniqueCardListResult CreateCurDeckUniqueCardList(void)\n{\n\tuint8_t count = 1u;", "case_ids": ["CreateCurDeckUniqueCardList-0", "CreateCurDeckUniqueCardList-1"]}
# <<< factory-mutation CreateCurDeckUniqueCardList
# >>> factory-mutation TryAddCardToDeck
MUTATIONS["TryAddCardToDeck"] = {"source_symbol": "TryAddCardToDeck", "before": "\treturn (TryAddCardToDeckResult){0u, 0x90u};", "after": "\treturn (TryAddCardToDeckResult){0u, 0u};", "case_ids": ["TryAddCardToDeck-0", "TryAddCardToDeck-1", "TryAddCardToDeck-2"]}
# <<< factory-mutation TryAddCardToDeck
# >>> factory-mutation AddCardToDeckAndUpdateCount
MUTATIONS["AddCardToDeckAndUpdateCount"] = {"source_symbol": "AddCardToDeckAndUpdateCount", "before": "\t\treturn (AddCardToDeckAndUpdateCountResult){r.a, r.f, e};", "after": "\t\treturn (AddCardToDeckAndUpdateCountResult){r.a, r.f, r.a};", "case_ids": ["AddCardToDeckAndUpdateCount-0", "AddCardToDeckAndUpdateCount-1"]}
# <<< factory-mutation AddCardToDeckAndUpdateCount
# >>> factory-mutation HandleDeckCardSelectionList
MUTATIONS["HandleDeckCardSelectionList"] = {"source_symbol": "HandleDeckCardSelectionList", "before": "HandleDeckCardSelectionListResult HandleDeckCardSelectionList(void)\n{\n\twMenuInputSFX = FALSE;", "after": "HandleDeckCardSelectionListResult HandleDeckCardSelectionList(void)\n{\n\twMenuInputSFX = FALSE;\n\twCardListCursorPos = 0x40u;", "case_ids": ["HandleDeckCardSelectionList-0", "HandleDeckCardSelectionList-2", "HandleDeckCardSelectionList-3"]}
# <<< factory-mutation HandleDeckCardSelectionList
# >>> factory-mutation PrintCurDeckNumberAndName
MUTATIONS["PrintCurDeckNumberAndName"] = {
    "source_symbol": "PrintCurDeckNumberAndName",
    "before": "\tTextLength name_length = GetTextLengthInTiles(wDefaultText_ADDR);\n\tuint16_t suffix_base = wDefaultText_ADDR;\n\tuint16_t suffix_destination = (uint16_t)(suffix_base + name_length.c);",
    "after": "\tTextLength name_length = GetTextLengthInTiles(wDefaultText_ADDR);\n\tuint16_t suffix_base = wDefaultText_ADDR;\n\tuint16_t suffix_destination = (uint16_t)(suffix_base + name_length.c + 1u);",
    "case_ids": ["PrintCurDeckNumberAndName-1", "PrintCurDeckNumberAndName-2", "PrintCurDeckNumberAndName-3"],
}
# <<< factory-mutation PrintCurDeckNumberAndName
# >>> factory-mutation UpdateConfirmationCardScreen
MUTATIONS["UpdateConfirmationCardScreen"] = {"source_symbol": "UpdateConfirmationCardScreen", "before": "\tPrintCurDeckNumberAndName();\n\n\thffb0 = 0u;", "after": "\tPrintCurDeckNumberAndName();\n\n\thffb0 = 1u;", "case_ids": ["UpdateConfirmationCardScreen-0", "UpdateConfirmationCardScreen-1", "UpdateConfirmationCardScreen-2"]}
# <<< factory-mutation UpdateConfirmationCardScreen
# >>> factory-mutation PrintSlashSixty
MUTATIONS["PrintSlashSixty"] = {"source_symbol": "PrintSlashSixty", "before": "\tgb_write8(text++, (uint8_t)(SYM_0 + 6u));", "after": "\tgb_write8(text++, (uint8_t)(SYM_0 + 5u));", "case_ids": ["PrintSlashSixty-0", "PrintSlashSixty-1", "PrintSlashSixty-2"]}
# <<< factory-mutation PrintSlashSixty
# >>> factory-mutation ShowDeckInfoHeader
MUTATIONS["ShowDeckInfoHeader"] = {
    "source_symbol": "ShowDeckInfoHeader",
    "before": "ShowDeckInfoHeader(void)\n{\n\tEmptyScreenAndLoadFontDuelAndHandCardsIcons();\n\tuint16_t box = 0u;\n\tDrawRegularTextBox(&box, 0u, 20u, 4u, 0u, 0u);\n\tif (wCurDeckName != 0u) {",
    "after": "ShowDeckInfoHeader(void)\n{\n\tEmptyScreenAndLoadFontDuelAndHandCardsIcons();\n\tuint16_t box = 0u;\n\tDrawRegularTextBox(&box, 0u, 20u, 4u, 0u, 0u);\n\tif (wCurDeckName == 0u) {",
    "case_ids": ["ShowDeckInfoHeader-0", "ShowDeckInfoHeader-1"],
}
# <<< factory-mutation ShowDeckInfoHeader
# >>> factory-mutation DrawCardTypeIconsAndPrintCardCounts
MUTATIONS["DrawCardTypeIconsAndPrintCardCounts"] = {"source_symbol": "DrawCardTypeIconsAndPrintCardCounts", "before": "\tFillBGMapLineWithA(SYM_BOX_TOP, 0u, 5u);", "after": "\tFillBGMapLineWithA(0x1Du, 0u, 5u);", "case_ids": ["DrawCardTypeIconsAndPrintCardCounts-0", "DrawCardTypeIconsAndPrintCardCounts-1"]}
# <<< factory-mutation DrawCardTypeIconsAndPrintCardCounts
# >>> factory-mutation ShowConfirmationCardScreen
MUTATIONS["ShowConfirmationCardScreen"] = {"source_symbol": "ShowConfirmationCardScreen", "before": "ShowConfirmationCardScreen(void)\n{\n\tShowDeckInfoHeader();\n\twCardListCoords = 5u;", "after": "ShowConfirmationCardScreen(void)\n{\n\tShowDeckInfoHeader();\n\twCardListCoords = 4u;", "case_ids": ["ShowConfirmationCardScreen-0", "ShowConfirmationCardScreen-1"]}
# <<< factory-mutation ShowConfirmationCardScreen
# >>> factory-mutation ShowDeckInfoHeaderAndWaitForBButton
MUTATIONS["ShowDeckInfoHeaderAndWaitForBButton"] = {"source_symbol": "ShowDeckInfoHeaderAndWaitForBButton", "before": "void ShowDeckInfoHeaderAndWaitForBButton(void)\n{\n\tShowDeckInfoHeader();", "after": "void ShowDeckInfoHeaderAndWaitForBButton(void)\n{\n\t(void)0;", "case_ids": ["ShowDeckInfoHeaderAndWaitForBButton-0", "ShowDeckInfoHeaderAndWaitForBButton-1"]}
# <<< factory-mutation ShowDeckInfoHeaderAndWaitForBButton
# >>> factory-mutation HandleDeckConfirmationMenu
MUTATIONS["HandleDeckConfirmationMenu"] = {"source_symbol": "HandleDeckConfirmationMenu", "before": "\tgb_write8(wCardListUpdateFunction_ADDR, (uint8_t)UPDATE_CONFIRMATION_CARD_SCREEN_ADDR);", "after": "\tgb_write8(wCardListUpdateFunction_ADDR, (uint8_t)(UPDATE_CONFIRMATION_CARD_SCREEN_ADDR + 1u));", "case_ids": ["HandleDeckConfirmationMenu-1", "HandleDeckConfirmationMenu-2", "HandleDeckConfirmationMenu-3"]}
# <<< factory-mutation HandleDeckConfirmationMenu
# >>> factory-mutation ConfirmDeckConfiguration
MUTATIONS["ConfirmDeckConfiguration"] = {"source_symbol": "ConfirmDeckConfiguration", "before": "ConfirmDeckConfiguration(void)\n{\n\tuint8_t visible_offset = wCardListVisibleOffset;", "after": "ConfirmDeckConfiguration(void)\n{\n\tuint8_t visible_offset = 0u;", "case_ids": ["ConfirmDeckConfiguration-0", "ConfirmDeckConfiguration-1"]}
# <<< factory-mutation ConfirmDeckConfiguration
