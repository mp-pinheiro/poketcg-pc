"""Oracle-diff cases for poketcg/src/engine/menus/deck_selection.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetPointerToDeckCards
CONTRACT["GetPointerToDeckCards"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["GetPointerToDeckCards"] = [
	{},
	{"wram": {sym("wCurDeck"): b"\x01"}},
	{"wram": {sym("wCurDeck"): b"\xFF"}},
	dict(POISON, wram={sym("wCurDeck"): b"\x02"}),
]
# <<< factory GetPointerToDeckCards

# >>> factory ResetCheckMenuCursorPositionAndBlink
CONTRACT["ResetCheckMenuCursorPositionAndBlink"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ResetCheckMenuCursorPositionAndBlink"] = [
	{"wram": {sym("wCheckMenuCursorBlinkCounter"): b"\x00", sym("wCheckMenuCursorXPosition"): b"\x00", sym("wCheckMenuCursorYPosition"): b"\x00"}},
	dict(POISON, wram={sym("wCheckMenuCursorBlinkCounter"): b"\x11", sym("wCheckMenuCursorXPosition"): b"\x22", sym("wCheckMenuCursorYPosition"): b"\x33"}),
]
# <<< factory ResetCheckMenuCursorPositionAndBlink

# >>> factory-cases-statics
wCurDeck = sym("wCurDeck")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sHasPromotionalCards = sym("sHasPromotionalCards")
sUnnamedDeckCounter = sym("sUnnamedDeckCounter")

wConsole = sym("wConsole")
wTileMapFill = sym("wTileMapFill")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")
wLCDC = sym("wLCDC")

wCurDeck = sym("wCurDeck")

# OpenDeckConfirmationMenu (deck_selection.asm:188). The body fills
# wCurDeckName and wCurDeckCards from the SRAM deck its de/hl point at,
# zeroes wCardFilterCounts, stores DECK_SIZE in two places, then hands off
# to HandleDeckConfirmationMenu, whose landed case this environment mirrors.
sDeck1Name = sym("sDeck1Name")
sDeck1Cards = sym("sDeck1Cards")
sCurrentlySelectedDeck = sym("sCurrentlySelectedDeck")
wCurDeckCards = sym("wCurDeckCards")
wCurDeckName = sym("wCurDeckName")
wCardFilterCounts = sym("wCardFilterCounts")
wTotalCardCount = sym("wTotalCardCount")
wUniqueDeckCardList = sym("wUniqueDeckCardList")
wNumUniqueCards = sym("wNumUniqueCards")
wCardListVisibleOffset = sym("wCardListVisibleOffset")
wCardListCursorPos = sym("wCardListCursorPos")
wCardListNumCursorPositions = sym("wCardListNumCursorPositions")
wNumVisibleCardListEntries = sym("wNumVisibleCardListEntries")
wced2 = sym("wced2")
wCardListUpdateFunction = sym("wCardListUpdateFunction")
wNumCardListEntries = sym("wNumCardListEntries")
wOpponentDeck = sym("wOpponentDeck")
wDuelTempList = sym("wDuelTempList")
hWhoseTurn = sym("hWhoseTurn")
hDPadHeld = sym("hDPadHeld")
hffb3 = sym("hffb3")

ODCM_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# Frame one idles, frame two presses B: HandleDeckConfirmationMenu's
# MENU_CANCEL exit, the same bounded cancel the landed case takes.
ODCM_KEYS = [0x00, 0x02]
# Only bytes both sides leave identical: the landed HandleDeckConfirmationMenu
# menu-path seeds, plus wUniqueDeckCardList and wNumUniqueCards poisoned so
# the empty-deck tail a wTotalCardCount mutation takes -- which writes
# neither -- stays visible against the menu path that overwrites both.
ODCM_WRAM = {
    wLCDC: b"\x00",
    hWhoseTurn: b"\xC2",
    wOpponentDeck: b"\x99\x00",
    wDuelTempList: b"\xFF",
    wUniqueDeckCardList: b"\x77\x77",
    wNumUniqueCards: b"\x09",
    wCardListUpdateFunction: b"\x00\x00",
}
ODCM_READ = {
    wCurDeckCards: 61,
    wCurDeckName: 1,
    wCardFilterCounts: 9,
    wTotalCardCount: 1,
    wUniqueDeckCardList: 2,
    wNumUniqueCards: 1,
    wCardListVisibleOffset: 1,
    wCardListCursorPos: 1,
    wCardListNumCursorPositions: 1,
    wNumVisibleCardListEntries: 1,
    wNumCardListEntries: 1,
    wced2: 1,
    wCardListUpdateFunction: 2,
    hWhoseTurn: 1,
    hDPadHeld: 1,
    hffb3: 1,
}

hDPadHeld = sym("hDPadHeld")
wCurDeck = sym("wCurDeck")
wCurMenuItem = sym("wCurMenuItem")

ICDN_PARK = bytes([0x18, 0xFE, 0x00]) * 4
ICDN_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
ICDN_READ = {sym("wTileMapFill"): 1, sym("wCardListCursorPos"): 1, sym("wCardListNumCursorPositions"): 1, sym("wVisibleCursorTile"): 2, sym("wNamingScreenBuffer"): 9, sym("wNamingScreenBufferLength"): 1, sym("wNamingScreenDestPointer"): 10, wCurDeckName: 21, sym("wCurDeckCardChanges"): 6}
# <<< factory-cases-statics

# >>> factory GetPointerToDeckName
CONTRACT["GetPointerToDeckName"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetPointerToDeckName"] = [
    {"wram": {wCurDeck: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "hl": sym("sBuiltDecks")}},
    dict(POISON, wram={wCurDeck: b"\x01"}, expect_regs={"a": 0x00, "f": 0x80, "hl": sym("sDeck2")}),
]
# <<< factory GetPointerToDeckName

# >>> factory InitDeckBuildingParams
CONTRACT["InitDeckBuildingParams"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c",)}
CASES["InitDeckBuildingParams"] = [
    {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x50\x04\x01\x34\x12\x78\x56"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 7}},
    dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01\x23\x45\x67\x89\xAB\xCD"}, read={sym("wDecompressionSecondaryBufferStart") + 0x11: 7}),
    {"a": 0xFF, "f": 0x01, "c": 0x7E, "d": 0x11, "e": 0x22, "hl": sym("wDecompressionSecondaryBufferStart") + 0x109,
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x109: b"\xFF\x00\x80\x7F\xAA\x55\x33"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x109: 7}},
]
# <<< factory InitDeckBuildingParams

# >>> factory CheckIfCurDeckIsValid
CONTRACT["CheckIfCurDeckIsValid"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["CheckIfCurDeckIsValid"] = [
    {"wram": {sym("wCurDeck"): b"\x00", sym("wDeck1Valid"): b"\x00"}},
    {"wram": {sym("wCurDeck"): b"\x02", sym("wDeck1Valid"): b"\x00\x00\x01"}},
    dict(POISON, wram={sym("wCurDeck"): b"\x01", sym("wDeck1Valid"): b"\x00\x00"}, expect_regs={"a": 0x00, "f": 0x90, "b": 0x00, "c": 0x01, "d": 0xDD, "e": 0xEE, "hl": sym("wDeck2Valid")}),
]
# <<< factory CheckIfCurDeckIsValid

# >>> factory CancelDeckSelectionSubMenu
CONTRACT["CancelDeckSelectionSubMenu"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CancelDeckSelectionSubMenu"] = [
	{"wram": {sym("wCurDeck"): b"\x00"}},
	dict(POISON, wram={sym("wCurDeck"): b"\x7F"}),
]
# <<< factory CancelDeckSelectionSubMenu

# >>> factory CopyDeckFromSRAM
CONTRACT["CopyDeckFromSRAM"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": ()}
CASES["CopyDeckFromSRAM"] = [
    {"d": 0xA0, "e": 0x00, "hl": sym("wNameBuffer"), "sram": {0: {sym("s0a000"): bytes(range(60))}}, "wram": {sym("wNameBuffer"): bytes(61)}, "read": {sym("wNameBuffer"): 61}},
    dict(POISON, d=0xA0, e=0x00, hl=sym("wNameBuffer"), sram={0: {sym("s0a000"): bytes(range(60))}}, wram={sym("wNameBuffer"): bytes(61)}, read={sym("wNameBuffer"): 61}),
]
# <<< factory CopyDeckFromSRAM

# >>> factory Func_9001
CONTRACT["Func_9001"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["Func_9001"] = [
    {"hl": 257, "read": {sym("wd009") + 1: 3}},
    dict(POISON, hl=257, read={sym("wd009") + 1: 3}),
    {"hl": 999, "read": {sym("wd009") + 1: 3}},
    {"hl": 5, "read": {sym("wd009") + 1: 3}},
]
# <<< factory Func_9001

# >>> factory LoadHandCardsIcon
CONTRACT["LoadHandCardsIcon"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["LoadHandCardsIcon"] = [
    {"vread": {0: {0x9380: 32}}},
    dict(POISON),
]
# <<< factory LoadHandCardsIcon

# >>> factory InitPromotionalCardAndDeckCounterSaveData
CONTRACT["InitPromotionalCardAndDeckCounterSaveData"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["InitPromotionalCardAndDeckCounterSaveData"] = [
    {"sram": {0: {sHasPromotionalCards: b"\xFF\xFF\xFF\xFF", sUnnamedDeckCounter: b"\xFF"}},
     "vread": {0: {0x9380: 32}}, "sread": {0: {sHasPromotionalCards: 4, sUnnamedDeckCounter: 1}}},
    dict(POISON, sram={0: {sHasPromotionalCards: b"\x00\x00\x00\x00", sUnnamedDeckCounter: b"\x00"}},
         vread={0: {0x9380: 32}}, sread={0: {sHasPromotionalCards: 4, sUnnamedDeckCounter: 1}}),
]
# <<< factory InitPromotionalCardAndDeckCounterSaveData

# >>> factory PrepareMenuGraphics
CONTRACT["PrepareMenuGraphics"] = {"compare": (), "preserve": ()}
CASES["PrepareMenuGraphics"] = [
    {"wram": {wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
     "read": {wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32}}},
    dict(POISON, wram={wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
         read={wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32}}),
]
# <<< factory PrepareMenuGraphics

# >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons
CONTRACT["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = {"compare": (), "preserve": ()}
CASES["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = [
    {"wram": {wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
     "read": {wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "vread": {0: {0x8D00: 768, 0x9000: 896, 0x9380: 32}}},
    dict(POISON, wram={wConsole: b"\x00", wTileMapFill: b"\xFF", wVBlankOAMCopyToggle: b"\x00", wLCDC: b"\x00"},
         read={wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         vread={0: {0x8D00: 768, 0x9000: 896, 0x9380: 32}}),
]
# <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons

# >>> factory PrintThereIsNoDeckHereText
CONTRACT["PrintThereIsNoDeckHereText"] = {"compare": ("a",), "preserve": ()}
CASES["PrintThereIsNoDeckHereText"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "keys": 0x01, "wram": {wCurDeck: b"\x02"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         keys=0x01, wram={wCurDeck: b"\x03"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintThereIsNoDeckHereText

# >>> factory WriteCardListsTerminatorBytes
CONTRACT["WriteCardListsTerminatorBytes"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["WriteCardListsTerminatorBytes"] = [
    {"wram": {sym("wFilteredCardList") + 0x3C: b"\xAA", sym("wCurDeckCards") + 0x50: b"\xBB"}, "read": {sym("wFilteredCardList") + 0x3C: 1, sym("wCurDeckCards") + 0x50: 1}},
    dict(POISON, wram={sym("wFilteredCardList") + 0x3C: b"\x11", sym("wCurDeckCards") + 0x50: b"\x22"}, read={sym("wFilteredCardList") + 0x3C: 1, sym("wCurDeckCards") + 0x50: 1}),
]
# <<< factory WriteCardListsTerminatorBytes

# >>> factory OpenDeckConfirmationMenu
CONTRACT["OpenDeckConfirmationMenu"] = {"compare": (), "preserve": ()}
CASES["OpenDeckConfirmationMenu"] = [
    # sixty copies of card 1: the sort leaves the deck list alone, the
    # unique list holds one card, and B cancels the confirmation menu on
    # frame two
    {"d": 0xA2, "e": 0x18, "hl": sDeck1Name, "wram": dict(ODCM_WRAM),
     "sram": {0: {sDeck1Name: b"\x00", sDeck1Cards: b"\x01" * 60}},
     "keys": ODCM_KEYS, "rom_bank": 2, "setup": ODCM_SETUP,
     "read": dict(ODCM_READ), "vread": {0: {0x9821: 4}},
     "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, d=0xA2, e=0x18, hl=sDeck1Name, wram=dict(ODCM_WRAM),
         sram={0: {sDeck1Name: b"\x00", sDeck1Cards: b"\x01" * 60}},
         keys=ODCM_KEYS, rom_bank=2, setup=ODCM_SETUP,
         read=dict(ODCM_READ), vread={0: {0x9821: 4}},
         instruction_budget=20000000, cycle_budget=100000000),
    # a shuffled two-card deck (30x card 2 then 30x card 1) makes the sort
    # reorder the list, and a non-empty deck name takes ShowDeckInfoHeader
    # through PrintCurDeckNumberAndName with the wCurDeck and
    # sCurrentlySelectedDeck seeds the landed
    # ShowDeckInfoHeaderAndWaitForBButton case uses for that path
    {"d": 0xA2, "e": 0x18, "hl": sDeck1Name,
     "wram": {**ODCM_WRAM, wCurDeck: b"\x00"},
     "sram": {0: {sDeck1Name: b"\x01\x00",
                  sDeck1Cards: bytes([2] * 30 + [1] * 30),
                  sCurrentlySelectedDeck: b"\x00"}},
     "keys": ODCM_KEYS, "rom_bank": 2, "setup": ODCM_SETUP,
     "read": {**ODCM_READ, wCurDeckName: 2, wUniqueDeckCardList: 3},
     "vread": {0: {0x9821: 4}},
     "instruction_budget": 20000000, "cycle_budget": 100000000},
]
# <<< factory OpenDeckConfirmationMenu

# >>> factory HandleStartButtonInDeckSelectionMenu
CONTRACT["HandleStartButtonInDeckSelectionMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleStartButtonInDeckSelectionMenu"] = [
    {"wram": {hDPadHeld: b"\x00", wCurDeck: b"\x42"}, "read": {wCurDeck: 1}},
    {"wram": {hDPadHeld: b"\x08", wCurMenuItem: b"\x00", wCurDeck: b"\x42", sym("wDeck1Valid"): b"\x00", sym("wDeck2Valid"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {wCurDeck: 1}},
    dict(POISON, wram={hDPadHeld: b"\x00", wCurDeck: b"\x42"}, read={wCurDeck: 1}),
]
# <<< factory HandleStartButtonInDeckSelectionMenu

# >>> factory InputCurDeckName
CONTRACT["InputCurDeckName"] = {"compare": (), "preserve": (), "wram_out": True, "sram_out": True}
CASES["InputCurDeckName"] = [
    {"wram": {wCurDeck: bytes([0x00]), wCurDeckName: bytes([0x06, 0x61]) + bytes(19), sym("wCurDeckCardChanges"): bytes(6), sym("hKeysHeld"): bytes([0x00]), sym("wd009") + 1: ICDN_PARK},
     "sram": {0: {sUnnamedDeckCounter: bytes([0x01, 0x00])}},
     "rom_bank": 6, "keys": 0x41, "setup": ICDN_SETUP,
     "read": ICDN_READ, "sread": {0: {sUnnamedDeckCounter: 2}},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={wCurDeck: bytes([0x02]), wCurDeckName: bytes([0x06, 0x61]) + bytes(19), sym("wCurDeckCardChanges"): bytes(6), sym("hKeysHeld"): bytes([0x00]), sym("wd009") + 1: ICDN_PARK},
         sram={0: {sUnnamedDeckCounter: bytes([0xE7, 0x03])}},
         rom_bank=6, keys=0x41, setup=ICDN_SETUP, read=ICDN_READ,
         sread={0: {sUnnamedDeckCounter: 2}},
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, wram={wCurDeck: bytes([0x01]), wCurDeckName: bytes([0x06, 0x62]) + bytes(19), sym("wCurDeckCardChanges"): bytes(6), sym("hKeysHeld"): bytes([0x00]), sym("wd009") + 1: ICDN_PARK},
         sram={0: {sUnnamedDeckCounter: bytes([0x01, 0x00])}},
         rom_bank=6, keys=0x41, setup=ICDN_SETUP, read=ICDN_READ,
         sread={0: {sUnnamedDeckCounter: 2}},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory InputCurDeckName

# >>> factory DeckSelectionMenu
CONTRACT["DeckSelectionMenu"] = {"compare": (), "preserve": ()}
CASES["DeckSelectionMenu"] = [
    {"keys": [0x00, 0x02],
     "wram": {sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"},
     "read": {sym("wCurDeck"): 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         wram={sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"}, read={sym("wCurDeck"): 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory DeckSelectionMenu

# >>> factory DeckSelectionSubMenu
CONTRACT["DeckSelectionSubMenu"] = {"compare": (), "preserve": ()}
CASES["DeckSelectionSubMenu"] = [
    {"keys": [0x00, 0x02, 0x02],
     "wram": {sym("wCheckMenuCursorXPosition"): b"\xAA", sym("wCheckMenuCursorYPosition"): b"\x00", sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"},
     "read": {sym("wCheckMenuCursorXPosition"): 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02, 0x02],
         wram={sym("wCheckMenuCursorXPosition"): b"\xAA", sym("wCheckMenuCursorYPosition"): b"\x00", sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"}, read={sym("wCheckMenuCursorXPosition"): 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"keys": [0x00, 0x80, 0x00, 0x01, 0x00, 0x08, 0x00, 0x01, 0x00, 0x02], "rom_bank": 2, "wram": {sym("wCurDeck"): b"\x00", sym("wDeck1Valid"): b"\x01", sym("wLCDC"): b"\x00", sym("wTextSpeed"): b"\x00"}, "sram": {0: {sDeck1Name: bytes(24), sDeck1Cards: bytes([0x08]) * 60, sCurrentlySelectedDeck: b"\x00", sUnnamedDeckCounter: b"\x01\x00"}}, "read": {wCurDeckName: 10}, "sread": {0: {sDeck1Name: 10, sUnnamedDeckCounter: 2}}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory DeckSelectionSubMenu

# >>> factory DeckSelectionSubMenu_SelectOrCancel
CONTRACT["DeckSelectionSubMenu_SelectOrCancel"] = {"compare": (), "preserve": ()}
CASES["DeckSelectionSubMenu_SelectOrCancel"] = [
    {"wram": {sym("wCheckMenuCursorYPosition"): b"\x01"}, "read": {sym("wCheckMenuCursorYPosition"): 1}},
    dict(POISON, wram={sym("wCheckMenuCursorYPosition"): b"\x01"}, read={sym("wCheckMenuCursorYPosition"): 1})]
# <<< factory DeckSelectionSubMenu_SelectOrCancel

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetPointerToDeckCards
MUTATIONS["GetPointerToDeckCards"] = {"source_symbol": "GetPointerToDeckCards", "before": "#define DECK_CARD_STRIDE 0x54u", "after": "#define DECK_CARD_STRIDE 0x55u", "case_ids": ["GetPointerToDeckCards-1", "GetPointerToDeckCards-2", "GetPointerToDeckCards-3"]}
# <<< factory-mutation GetPointerToDeckCards
# >>> factory-mutation ResetCheckMenuCursorPositionAndBlink
MUTATIONS["ResetCheckMenuCursorPositionAndBlink"] = {"source_symbol": "ResetCheckMenuCursorPositionAndBlink", "before": "\twCheckMenuCursorYPosition = 0u;", "after": "\twCheckMenuCursorXPosition = 0u;", "case_ids": ["ResetCheckMenuCursorPositionAndBlink-1"]}
# <<< factory-mutation ResetCheckMenuCursorPositionAndBlink
# >>> factory-mutation GetPointerToDeckName
MUTATIONS["GetPointerToDeckName"] = {"source_symbol": "GetPointerToDeckName", "before": "\treturn (uint16_t)(sDeck1Name_ADDR + offset);", "after": "\treturn (uint16_t)(sDeck1Name_ADDR + offset + 1u);", "case_ids": ["GetPointerToDeckName-0", "GetPointerToDeckName-1"]}
# <<< factory-mutation GetPointerToDeckName
# >>> factory-mutation InitDeckBuildingParams
MUTATIONS["InitDeckBuildingParams"] = {"source_symbol": "InitDeckBuildingParams", "before": "for (uint8_t i = 0; i < 7u; i++)", "after": "for (uint8_t i = 0; i < 6u; i++)", "case_ids": ["InitDeckBuildingParams-0", "InitDeckBuildingParams-1", "InitDeckBuildingParams-2"]}
# <<< factory-mutation InitDeckBuildingParams
# >>> factory-mutation CheckIfCurDeckIsValid
MUTATIONS["CheckIfCurDeckIsValid"] = {"source_symbol": "CheckIfCurDeckIsValid", "before": "\tuint8_t value = gb_read8(hl);", "after": "\tuint8_t value = (uint8_t)(gb_read8(hl) ^ 1u);", "case_ids": ["CheckIfCurDeckIsValid-0", "CheckIfCurDeckIsValid-1", "CheckIfCurDeckIsValid-2"]}
# <<< factory-mutation CheckIfCurDeckIsValid
# >>> factory-mutation CancelDeckSelectionSubMenu
MUTATIONS["CancelDeckSelectionSubMenu"] = {"source_symbol": "CancelDeckSelectionSubMenu", "before": "\treturn;", "after": "\tgb_write8(wCurDeck_ADDR, (uint8_t)(gb_read8(wCurDeck_ADDR) + 1u));", "case_ids": ["CancelDeckSelectionSubMenu-0", "CancelDeckSelectionSubMenu-1"]}
# <<< factory-mutation CancelDeckSelectionSubMenu
# >>> factory-mutation CopyDeckFromSRAM
MUTATIONS["CopyDeckFromSRAM"] = {"source_symbol": "CopyDeckFromSRAM", "before": "\tfor (uint8_t i = 0; i < DECK_SIZE; i++) {", "after": "\tfor (uint8_t i = 0; i < (uint8_t)(DECK_SIZE - 1u); i++) {", "case_ids": ["CopyDeckFromSRAM-0", "CopyDeckFromSRAM-1"]}
# <<< factory-mutation CopyDeckFromSRAM
# >>> factory-mutation Func_9001
MUTATIONS["Func_9001"] = {"source_symbol": "Func_9001", "before": "\tstatic const uint16_t steps[3] = {(uint16_t)-100, (uint16_t)-10, (uint16_t)-1};", "after": "\tstatic const uint16_t steps[3] = {(uint16_t)-100, (uint16_t)-10, (uint16_t)-2};", "case_ids": ["Func_9001-0", "Func_9001-2"]}
# <<< factory-mutation Func_9001
# >>> factory-mutation LoadHandCardsIcon
MUTATIONS["LoadHandCardsIcon"] = {"source_symbol": "LoadHandCardsIcon", "before": "\tuint16_t de = v0Tiles2_dest;", "after": "\tuint16_t de = (uint16_t)(v0Tiles2_dest + 1u);", "case_ids": ["LoadHandCardsIcon-0"]}
# <<< factory-mutation LoadHandCardsIcon
# >>> factory-mutation InitPromotionalCardAndDeckCounterSaveData
MUTATIONS["InitPromotionalCardAndDeckCounterSaveData"] = {"source_symbol": "InitPromotionalCardAndDeckCounterSaveData", "before": "\tgb_write8(sUnnamedDeckCounter_ADDR, 1u);", "after": "\tgb_write8(sUnnamedDeckCounter_ADDR, 0u);", "case_ids": ["InitPromotionalCardAndDeckCounterSaveData-0", "InitPromotionalCardAndDeckCounterSaveData-1"]}
# <<< factory-mutation InitPromotionalCardAndDeckCounterSaveData
# >>> factory-mutation PrepareMenuGraphics
MUTATIONS["PrepareMenuGraphics"] = {"source_symbol": "PrepareMenuGraphics", "before": "\twVBlankOAMCopyToggle = TRUE;", "after": "\twVBlankOAMCopyToggle = 0u;", "case_ids": ["PrepareMenuGraphics-0", "PrepareMenuGraphics-1"]}
# <<< factory-mutation PrepareMenuGraphics
# >>> factory-mutation EmptyScreenAndLoadFontDuelAndHandCardsIcons
MUTATIONS["EmptyScreenAndLoadFontDuelAndHandCardsIcons"] = {"source_symbol": "EmptyScreenAndLoadFontDuelAndHandCardsIcons", "before": "\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = TRUE;", "after": "\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = 0u;", "case_ids": ["EmptyScreenAndLoadFontDuelAndHandCardsIcons-0", "EmptyScreenAndLoadFontDuelAndHandCardsIcons-1"]}
# <<< factory-mutation EmptyScreenAndLoadFontDuelAndHandCardsIcons
# >>> factory-mutation PrintThereIsNoDeckHereText
MUTATIONS["PrintThereIsNoDeckHereText"] = {"source_symbol": "PrintThereIsNoDeckHereText", "before": "\treturn wCurDeck;", "after": "\treturn (uint8_t)(wCurDeck + 1u);", "case_ids": ["PrintThereIsNoDeckHereText-0", "PrintThereIsNoDeckHereText-1"]}
# <<< factory-mutation PrintThereIsNoDeckHereText
# >>> factory-mutation WriteCardListsTerminatorBytes
MUTATIONS["WriteCardListsTerminatorBytes"] = {"source_symbol": "WriteCardListsTerminatorBytes", "before": "\tuint16_t filtered_terminator = (uint16_t)(wFilteredCardList_ADDR + DECK_SIZE);", "after": "\tuint16_t filtered_terminator = (uint16_t)(wFilteredCardList_ADDR + (DECK_SIZE - 1u));", "case_ids": ["WriteCardListsTerminatorBytes-0", "WriteCardListsTerminatorBytes-1"]}
# <<< factory-mutation WriteCardListsTerminatorBytes
# >>> factory-mutation OpenDeckConfirmationMenu
MUTATIONS["OpenDeckConfirmationMenu"] = {"source_symbol": "OpenDeckConfirmationMenu", "before": "\twTotalCardCount = DECK_SIZE;", "after": "\twTotalCardCount = 0u;", "case_ids": ["OpenDeckConfirmationMenu-0", "OpenDeckConfirmationMenu-1", "OpenDeckConfirmationMenu-2"]}
# <<< factory-mutation OpenDeckConfirmationMenu
# >>> factory-mutation HandleStartButtonInDeckSelectionMenu
MUTATIONS["HandleStartButtonInDeckSelectionMenu"] = {"source_symbol": "HandleStartButtonInDeckSelectionMenu", "before": "\twCurDeck = wCurMenuItem;", "after": "\twCurDeck = 0x01u;", "case_ids": ["HandleStartButtonInDeckSelectionMenu-1"]}
# <<< factory-mutation HandleStartButtonInDeckSelectionMenu
# >>> factory-mutation InputCurDeckName
MUTATIONS["InputCurDeckName"] = {"source_symbol": "InputCurDeckName", "before": "\telse if (deck == 2u)\n\t\tquestion = INPUT_CUR_DECK_DECK3_DATA;", "after": "\telse if (deck == 2u)\n\t\tquestion = INPUT_CUR_DECK_DECK1_DATA;", "case_ids": ["InputCurDeckName-1"]}
# <<< factory-mutation InputCurDeckName
# >>> factory-mutation DeckSelectionMenu
MUTATIONS["DeckSelectionMenu"] = {"source_symbol": "DeckSelectionMenu", "before": "\tDrawDecksScreen(ALL_DECKS);", "after": "\tDrawDecksScreen(ALL_DECKS);\n\twCurDeck = 1u;", "case_ids": ["DeckSelectionMenu-0", "DeckSelectionMenu-1"]}
# <<< factory-mutation DeckSelectionMenu
# >>> factory-mutation DeckSelectionSubMenu
MUTATIONS["DeckSelectionSubMenu"] = {"source_symbol": "DeckSelectionSubMenu", "before": "\t(void)ResetCheckMenuCursorPositionAndBlink();", "after": "\t(void)ResetCheckMenuCursorPositionAndBlink();\n\twCheckMenuCursorXPosition = 1u;", "case_ids": ["DeckSelectionSubMenu-0", "DeckSelectionSubMenu-1"]}
# <<< factory-mutation DeckSelectionSubMenu
# >>> factory-mutation DeckSelectionSubMenu_SelectOrCancel
MUTATIONS["DeckSelectionSubMenu_SelectOrCancel"] = {"source_symbol": "DeckSelectionSubMenu_SelectOrCancel", "before": "\tif (wCheckMenuCursorYPosition != 0u) {\n\t\tCancelDeckSelectionSubMenu();", "after": "\tif (wCheckMenuCursorYPosition != 0u) {\n\t\twCheckMenuCursorYPosition = 0u;\n\t\tCancelDeckSelectionSubMenu();", "case_ids": ["DeckSelectionSubMenu_SelectOrCancel-0", "DeckSelectionSubMenu_SelectOrCancel-1"]}
# <<< factory-mutation DeckSelectionSubMenu_SelectOrCancel
