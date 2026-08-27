"""Oracle-diff cases for poketcg/src/engine/menus/deck_machine.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory CheckIfSelectedDeckMachineEntryIsEmpty
CONTRACT["CheckIfSelectedDeckMachineEntryIsEmpty"] = {"compare": ("d", "e", "f"), "preserve": ("d", "e")}
CASES["CheckIfSelectedDeckMachineEntryIsEmpty"] = [
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x50\xa3"}, "sram": {0: {0xA367: b"\x7f\x00"}}, "ramg": False},
    dict(POISON, wram={0xD088: b"\x01", 0xD00D: b"\x00\x00\x80\xa3"}, sram={0: {0xA397: b"\x00\x7f"}}, ramg=False),
]
# <<< factory CheckIfSelectedDeckMachineEntryIsEmpty

# >>> factory SafelySwitchToSRAM1
CONTRACT["SafelySwitchToSRAM1"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToSRAM1"] = [
    {"read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON, wram={0xFF81: b"\x01", 0xD0A4: b"\x55"}),
    {"wram": {0xFF81: b"\x02", 0xD0A4: b"\x09"}},
]
# <<< factory SafelySwitchToSRAM1

# >>> factory SafelySwitchToTempSRAMBank
CONTRACT["SafelySwitchToTempSRAMBank"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToTempSRAMBank"] = [
    {"read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON, wram={0xFF81: b"\x02", 0xD0A4: b"\x01"}),
    {"wram": {0xFF81: b"\x03", 0xD0A4: b"\x03"}},
]
# <<< factory SafelySwitchToTempSRAMBank

# >>> factory CheckIfHasEnoughCardsToBuildDeck
CONTRACT["CheckIfHasEnoughCardsToBuildDeck"] = {"compare": ("a", "f", "c", "hl"), "preserve": ("c",)}
CASES["CheckIfHasEnoughCardsToBuildDeck"] = [
    {"hl": 0xC100,
     "wram": {0xC000: b"\x00", 0xC100: b"\x00"},
     "read": {0xC000: 1}},
    dict(POISON, hl=0xC100,
         wram={0xC000: b"\x3c", 0xC100: b"\x00" * 60},
         read={0xC000: 1, 0xC100: 60}),
    {"hl": 0xC100,
     "wram": {0xC000: b"\x01", 0xC100: b"\x00\x00"},
     "read": {0xC000: 1, 0xC100: 2}},
    {"hl": 0xC100,
     "wram": {0xC000: b"\x00\x00\x00\x00\x00\x80", 0xC100: b"\x05"},
     "read": {0xC005: 1}},
    {"hl": 0xC100,
     "wram": {0xC000: b"\x01" * 60, 0xC100: bytes(range(60))},
     "read": {0xC000: 60, 0xC100: 60}},
]
# <<< factory CheckIfHasEnoughCardsToBuildDeck

# >>> factory GetSavedDeckPointers
wMachineDeckPtrs = 0xD00D
CONTRACT["GetSavedDeckPointers"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["GetSavedDeckPointers"] = [
	{"wram": {wMachineDeckPtrs: b"\xaa" * 0x78}},  # 0x78 = 2 bytes * NUM_DECK_SAVE_MACHINE_SLOTS
	dict(POISON, wram={wMachineDeckPtrs: b"\x55" * 0x78}),
]
# <<< factory GetSavedDeckPointers

# >>> factory GetSavedDeckCount
CONTRACT["GetSavedDeckCount"] = {"compare": (), "preserve": ()}
CASES["GetSavedDeckCount"] = [
    {"sram": {0: {0xA350: bytes(0x54 * 0x3C)}}, "read": {0xD085: 1}},
    dict(POISON,
         sram={0: {0xA350: bytes(1 if i in (0, 0x54, 0xA8) else 0
                              for i in range(0x54 * 0x3C))}},
         read={0xD085: 1}),
    {"sram": {0: {0xA350: bytes(1 if i == 0 else 0
                              for i in range(0x54 * 0x3C))}},
     "read": {0xD085: 1}},
    {"sram": {0: {0xA350: bytes(1 if i == 0x54 else 0
                              for i in range(0x54 * 0x3C))}},
     "read": {0xD085: 1}},
    {"sram": {0: {0xA350: b"\x01" * (0x54 * 0x3C)}},
     "read": {0xD085: 1}},
]
# <<< factory GetSavedDeckCount

# >>> factory GetSelectedSavedDeckPtr
CONTRACT["GetSelectedSavedDeckPtr"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "hl")}
CASES["GetSelectedSavedDeckPtr"] = [
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x34\x12"}},
    dict(POISON,
         wram={0xD088: b"\x01", 0xD00D: b"\x78\x56\xBC\x9A"}),
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x00\x00"}},
    {"wram": {0xD088: b"\x01", 0xD00D: b"\x00\x00\x78\x56"}},
    {"wram": {0xD088: b"\xFF",
              0xD00D: bytes(0x1FE) + b"\xEF\xBE\x00\x00"}},
]
# <<< factory GetSelectedSavedDeckPtr

# >>> factory SafelySwitchToSRAM0
CONTRACT["SafelySwitchToSRAM0"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToSRAM0"] = [
    {"wram": {0xFF81: b"\x00", 0xD0A4: b"\x00"}, "read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON,
         wram={0xFF81: b"\x02", 0xD0A4: b"\xEE"},
         read={0xFF81: 1, 0xD0A4: 1}),
    {"wram": {0xFF81: b"\x01", 0xD0A4: b"\x00"}, "read": {0xFF81: 1, 0xD0A4: 1}},
    {"wram": {0xFF81: b"\x03", 0xD0A4: b"\xFF"}, "read": {0xFF81: 1, 0xD0A4: 1}},
]
# <<< factory SafelySwitchToSRAM0

# >>> factory-cases-statics
wCardListVisibleOffset = 0xCEA1
wNumDeckMachineEntries = 0xD0A5
wUnableToScrollDown = 0xCECD
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wConsole = 0xCAB4
wLCDC = 0xCABB

wConsole = 0xCAB4
wLCDC = 0xCABB
wNameBuffer = 0xC500
wDefaultText = 0xC590
wTxRam2 = 0xCE3F

hBankSRAM = 0xFF81
wTempBankSRAM = 0xD0A4
wMachineDeckPtrs = 0xD00D

wMachineDeckPtrs = 0xD00D
wDefaultText = 0xC590

wNameBuffer = 0xC500
wDefaultText = 0xC590
wTxRam2 = 0xCE3F
hffb0 = 0xFFB0

wDuelTempList = 0xC510
wTempCardCollection = 0xC000
wFilteredCardList = 0xCEDA
wNumEntriesInCurFilter = 0xCEAE
wNumVisibleCardListEntries = 0xCECB
wCardListCoords = 0xCED0
wCursorAlternateTile = 0xCFDE
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCardListCursorPos = 0xCEA4
wDefaultYesOrNo = 0xCD9A

def menu_state(counter=0, item=0, xoff=0, yoff=0, ysep=0, vis=0, invis=0):
    return {0xCD0F: bytes([counter]), 0xCD10: bytes([item]), 0xCD11: bytes([xoff]),
            0xCD12: bytes([yoff]), 0xCD13: bytes([ysep]), 0xCD15: bytes([vis]),
            0xCD16: bytes([invis])}

SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1, 0xFFAE: 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 192}, 1: {0x9980: 192}}
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# HandleDeckMissingCardsList (deck_machine.asm:6): one saved-deck struct in
# SRAM -- the name, then the 60 card ids at offset $18 -- is the whole input.
HDMC_NAME_SRAM = 0xA800
HDMC_CARDS_SRAM = 0xA818
# Seeds every case shares. A seed address is compared as well as written, so
# this lists only bytes the reference and the port both leave identical: the
# state the body reads, plus the buffers it overwrites end to end (pre-zeroed,
# so no byte the routine never writes can differ). wLCDC ($CABB) is absent on
# purpose -- the body calls EnableLCD and the reference VBlank handler then
# keeps mirroring it, which makes it uncomparable.
HDMC_SEEDS = {
    0xCAB4: b"\x00",       # wConsole = CONSOLE_DMG
    0xCAD0: b"\xc9",       # wVBlankFunctionTrampoline: a bare `ret`, which the
                           # reference VBlank handler calls every frame
    0xCFDA: b"\x6f\x02",   # wCardConfirmationText = TheseCardsAreNeededToBuildThisDeckText
    0xCEA5: b"\x00" * 9,   # wCardListCursorXPos..wCardListHandlerFunction, filled from $6E91
    0xCEBB: b"\x00" * 9,   # wCardFilterCounts
    0xCECE: b"\x00\x00",   # wCardListUpdateFunction
    0xCED0: b"\x00\x00",   # wCardListCoords
    0xCED2: b"\x00",       # wced2
    0xCF17: b"\x00" * 61,  # wCurDeckCards and its terminator
    0xCF68: b"\x00" * 8,   # wUniqueDeckCardList
    0xCFB9: b"\x00" * 8,   # wCurDeckName
}
# Everything else this routine's own asm writes. Nothing the reference VBlank
# handler touches (hSCX/hSCY/hWX/hWY, wLCDC, wFlushPaletteFlags,
# wVBlankOAMCopyToggle) and no VRAM: the LCD is on for the second half of the
# body, so PPU-timed VRAM writes are not comparable.
HDMC_READ = {
    0xCEA1: 1,  # wCardListVisibleOffset
    0xCEA4: 1,  # wCardListCursorPos
    0xCECB: 1,  # wNumVisibleCardListEntries
    0xCECC: 1,  # wTotalCardCount
    0xCFE6: 1,  # wNumCardListEntries
    0xFF8F: 1,  # hDPadHeld
    0xFFB3: 1,  # hffb3
}
# The body reaches DoFrame with the LCD on, so real frames elapse: the reference
# needs the game's DMA routine installed (EmptyScreenAndLoadFontDuelAndHandCards
# Icons sets wVBlankOAMCopyToggle, and VBlankHandler then calls hDMAFunction)
# and a text setup before any glyph is cached.
HDMC_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# Frame one presses nothing, frame two presses B, and both sides cycle the pair,
# so the edge-triggered hKeysPressed read inside HandleDeckCardSelectionList
# always catches a fresh B press: that is the MENU_CANCEL write to hffb3 the
# `ret z` in .selection_made returns through. A (0x01) instead falls into
# .open_card_pge and loops back to .loop forever.
HDMC_KEYS = [0x00, 0x02]

wCardListVisibleOffset = 0xCEA1

wTileMapFill = 0xCAB6
wVBlankOAMCopyToggle = 0xCAC0
wDeckMachineTitleText = 0xD0A2

wDeckMachineText = 0xD0A7
wMachineDeckPtrs = 0xD00D

wCardListVisibleOffset = 0xCEA1
wCardListCursorPos = 0xCEA4
wMachineDeckPtrs = 0xD00D
wTempCardListVisibleOffset = 0xD087
wTempDeckMachineCursorPos = 0xD086
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory DrawListScrollArrows
CONTRACT["DrawListScrollArrows"] = {"compare": (), "preserve": ()}
CASES["DrawListScrollArrows"] = [
    {"wram": {wCardListVisibleOffset: b"\x00", wNumDeckMachineEntries: b"\x00", wUnableToScrollDown: b"\xAA"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
    dict(POISON, wram={wCardListVisibleOffset: b"\x01", wNumDeckMachineEntries: b"\x07", wUnableToScrollDown: b"\xAA"},
         read={wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
         vread={0: {0x9833: 1, 0x9953: 1}}),
    {"wram": {wCardListVisibleOffset: b"\x05", wNumDeckMachineEntries: b"\x0A", wUnableToScrollDown: b"\x00"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
    {"wram": {wCardListVisibleOffset: b"\xFA", wNumDeckMachineEntries: b"\x00", wUnableToScrollDown: b"\xFF"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
]
# <<< factory DrawListScrollArrows

# >>> factory SetDeckMachineTitleText
CONTRACT["SetDeckMachineTitleText"] = {"compare": ("hl",), "preserve": ()}
CASES["SetDeckMachineTitleText"] = [
    {"wram": {0xD0A2: b"\x00\x00", 0xCABB: b"\x00"}, "read": {0xFFAD: 1}},
    dict(POISON, wram={0xD0A2: b"\x00\x00", 0xCABB: b"\x00"}, read={0xFFAD: 1}),
]
# <<< factory SetDeckMachineTitleText

# >>> factory FindFirstEmptyDeckSlot
CONTRACT["FindFirstEmptyDeckSlot"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["FindFirstEmptyDeckSlot"] = [
    {"ramg": True, "sram": {0: {0xA218: b"\x00"}}},
    dict(POISON, ramg=True, sram={0: {0xA218: b"\x01", 0xA26C: b"\x00"}}),
    {"ramg": True, "sram": {0: {0xA218: b"\x01", 0xA26C: b"\x02", 0xA2C0: b"\x03", 0xA314: b"\x04"}}},
]
# <<< factory FindFirstEmptyDeckSlot

# >>> factory EmptyScreenAndDrawTextBox
CONTRACT["EmptyScreenAndDrawTextBox"] = {"compare": (), "preserve": ()}
CASES["EmptyScreenAndDrawTextBox"] = [
    {"wram": {wConsole: b"\x00", wLCDC: b"\x00"},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}},
    dict(POISON, wram={wConsole: b"\x00", wLCDC: b"\x00"},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}),
]
# <<< factory EmptyScreenAndDrawTextBox

# >>> factory PrintCardToSendText
CONTRACT["PrintCardToSendText"] = {"compare": (), "preserve": ()}
CASES["PrintCardToSendText"] = [
    {"wram": {wConsole: b"\x00", wLCDC: b"\x00"},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}},
    dict(POISON, wram={wConsole: b"\x00", wLCDC: b"\x00"},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}),
]
# <<< factory PrintCardToSendText

# >>> factory PrintReceivedTheseCardsText
CONTRACT["PrintReceivedTheseCardsText"] = {"compare": (), "preserve": ()}
CASES["PrintReceivedTheseCardsText"] = [
    {"wram": {wConsole: b"\x00", wLCDC: b"\x00", wNameBuffer: b"\x05\x08\x00"},
     "read": {wDefaultText: 3, wTxRam2: 2},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}},
    dict(POISON, wram={wConsole: b"\x00", wLCDC: b"\x00", wNameBuffer: b"\x05\x08\x00"},
         read={wDefaultText: 3, wTxRam2: 2},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}),
]
# <<< factory PrintReceivedTheseCardsText

# >>> factory PrintNumSavedDecks
CONTRACT["PrintNumSavedDecks"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintNumSavedDecks"] = [
    {"wram": {0xD085: b"\x05"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC590: 9}},
    dict(POISON, wram={0xD085: b"\x05"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC590: 9}),
]
# <<< factory PrintNumSavedDecks

# >>> factory Func_b568
CONTRACT["Func_b568"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_b568"] = [
    {"wram": {0xCEA4: b"\x02", 0xCEA1: b"\x01", 0xD085: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC590: 9}},
    dict(POISON, wram={0xCEA4: b"\x02", 0xCEA1: b"\x01", 0xD085: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC590: 9}),
]
# <<< factory Func_b568

# >>> factory CheckIfCanBuildSavedDeck
CONTRACT["CheckIfCanBuildSavedDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfCanBuildSavedDeck"] = [
    {"a": 0x00, "b": 0x00, "wram": {hBankSRAM: b"\x00", wTempBankSRAM: b"\x00", wMachineDeckPtrs: b"\xE8\xC0", 0xC000: b"\x00", 0xC100: b"\x00"},
     "sram": {0: {}}},
    dict(POISON, a=0x00, b=0x00, wram={hBankSRAM: b"\x00", wTempBankSRAM: b"\x00", wMachineDeckPtrs: b"\xE8\xC0", 0xC000: b"\x00", 0xC100: b"\x00"},
         sram={0: {}}),
]
# <<< factory CheckIfCanBuildSavedDeck

# >>> factory PrintDeckMachineEntry
CONTRACT["PrintDeckMachineEntry"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PrintDeckMachineEntry"] = [
    {"a": 0x00, "d": 0x01, "e": 0x0E,
     "wram": {wDefaultText: b"\x00" * 8, wMachineDeckPtrs: b"\x00\xA2"},
     "ramg": False,
     "sram": {0: {0xA200: b"\x00"}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, a=0x00, d=0x01, e=0x0E,
         wram={wDefaultText: b"\xFF" * 8, wMachineDeckPtrs: b"\x00\xA2"},
         ramg=False,
         sram={0: {0xA200: b"\xFF"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintDeckMachineEntry

# >>> factory ShowReceivedCardsList
CONTRACT["ShowReceivedCardsList"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ShowReceivedCardsList"] = [
    {"a": 0x00, "f": 0x00, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {wNameBuffer: b"\x00", wTxRam2: b"\xFF\xFF"},
     "read": {hffb0: 1, wTxRam2: 2}},
    dict(POISON, wram={wNameBuffer: b"\x00", wTxRam2: b"\xFF\xFF"},
         read={hffb0: 1, wTxRam2: 2}),
]
# <<< factory ShowReceivedCardsList

# >>> factory Func_b088
CONTRACT["Func_b088"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_b088"] = [
    {"wram": {wDuelTempList: b"\x00", wTempCardCollection: bytes(0x100)},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={wDuelTempList: b"\x00", wTempCardCollection: bytes(0x100)},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_b088

# >>> factory TryDeleteSavedDeck
CONTRACT["TryDeleteSavedDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TryDeleteSavedDeck"] = [
    {"keys": 0x01, "setup": SETUP,
     "wram": {**menu_state(counter=5, item=1, xoff=2, invis=0x22),
              wDefaultYesOrNo: b"\x00", wCardListCursorPos: b"\x03", 0xCABB: b"\x00"},
     "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ,
     "expect_regs": {"a": 0x03, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=0x01, setup=SETUP,
         wram={**menu_state(counter=5, item=1, xoff=2, invis=0x22),
               wDefaultYesOrNo: b"\x00", wCardListCursorPos: b"\xAA", 0xCABB: b"\x00"},
         read={**CACHE_READ, **PLACEMENT_READ}, vread=VRAM_READ,
         expect_regs={"a": 0xAA, "f": 0x90},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory TryDeleteSavedDeck

# >>> factory HandleDeckMissingCardsList
CONTRACT["HandleDeckMissingCardsList"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
# rom_bank 2 is mandatory, not decoration: the routine reads
# .DeckConfirmationCardSelectionParams ($6E91) and DeckNameSuffix ($52A7) out of
# its own bank, and with bank 1 mapped the params become garbage,
# wCardListHandlerFunction turns non-zero and the run falls into
# OpenCardPageFromCardList forever.
CASES["HandleDeckMissingCardsList"] = [
    # Empty deck name: .PrintDeckIndexAndName takes its `ret z` exit, so the
    # title is skipped and only the confirmation list is printed.
    {"hl": HDMC_NAME_SRAM, "d": HDMC_CARDS_SRAM >> 8, "e": HDMC_CARDS_SRAM & 0xFF,
     "keys": HDMC_KEYS, "rom_bank": 2, "ramg": True,
     "wram": {**HDMC_SEEDS, 0xCEB1: b"\x00"},
     "sram": {0: {HDMC_NAME_SRAM: b"\x00", HDMC_CARDS_SRAM: b"\x01" * 60}},
     "read": dict(HDMC_READ), "setup": HDMC_SETUP,
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    # Named deck: the full "X.<NAME> deck" path runs, so wCurDeck feeds
    # ConvertToNumericalDigits and DeckNameSuffix is appended past the name.
    {"hl": HDMC_NAME_SRAM, "d": HDMC_CARDS_SRAM >> 8, "e": HDMC_CARDS_SRAM & 0xFF,
     "keys": HDMC_KEYS, "rom_bank": 2, "ramg": True,
     "wram": {**HDMC_SEEDS, 0xCEB1: b"\x02"},
     "sram": {0: {HDMC_NAME_SRAM: b"ABC\x00", HDMC_CARDS_SRAM: b"\x01" * 60}},
     "read": dict(HDMC_READ), "setup": HDMC_SETUP,
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    # Poisoned a/f/b/c (d/e/hl carry the SRAM pointers the routine dereferences)
    # over a two-id deck, so the sort reorders it and wNumUniqueCards is 2.
    dict(POISON, hl=HDMC_NAME_SRAM, d=HDMC_CARDS_SRAM >> 8, e=HDMC_CARDS_SRAM & 0xFF,
         keys=HDMC_KEYS, rom_bank=2, ramg=True,
         wram={**HDMC_SEEDS, 0xCEB1: b"\x09"},
         sram={0: {HDMC_NAME_SRAM: b"DECK\x00",
                   HDMC_CARDS_SRAM: b"\x0a" * 30 + b"\x05" * 30}},
         read=dict(HDMC_READ), setup=HDMC_SETUP,
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandleDeckMissingCardsList

# >>> factory HandleDismantleDeckToMakeSpace
CONTRACT["HandleDismantleDeckToMakeSpace"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleDismantleDeckToMakeSpace"] = [
    {"keys": [0x00, 0x02],
     "ramg": True,
     "sram": {0: {}},
     "wram": {0xCABB: b"\x00", 0xFF81: b"\x00", 0xD0A4: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         ramg=True, sram={0: {}},
         wram={0xCABB: b"\x00", 0xFF81: b"\x00", 0xD0A4: b"\x00"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandleDismantleDeckToMakeSpace

# >>> factory PrintVisibleDeckMachineEntries
CONTRACT["PrintVisibleDeckMachineEntries"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PrintVisibleDeckMachineEntries"] = [
    {"f": 0x10, "wram": {wCardListVisibleOffset: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    {"f": 0x11, "wram": {wCardListVisibleOffset: b"\xE4"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, wram={wCardListVisibleOffset: b"\x01"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintVisibleDeckMachineEntries

# >>> factory ClearScreenAndDrawDeckMachineScreen
CONTRACT["ClearScreenAndDrawDeckMachineScreen"] = {"compare": (), "preserve": ()}
CASES["ClearScreenAndDrawDeckMachineScreen"] = [
    {"wram": {0xD0A2: b"\x00\x00", 0xCAB6: b"\xff", 0xCAC0: b"\x00"}, "read": {0xCAB6: 1, 0xCAC0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xD0A2: b"\x00\x00", 0xCAB6: b"\xaa", 0xCAC0: b"\x55"}, read={0xCAB6: 1, 0xCAC0: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ClearScreenAndDrawDeckMachineScreen

# >>> factory DrawDeckMachineScreen
CONTRACT["DrawDeckMachineScreen"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawDeckMachineScreen"] = [
    {"wram": {wDeckMachineText: b"\x00\x00", wMachineDeckPtrs: b"\x50\xA3" * 5}, "sram": {0: {0xA368: b"\x01"}}, "read": {0xFFB0: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={wDeckMachineText: b"\x00\x00", wMachineDeckPtrs: b"\x50\xA3" * 5}, sram={0: {0xA368: b"\x01"}}, read={0xFFB0: 1}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DrawDeckMachineScreen

# >>> factory HandleDeckMachineSelection
CONTRACT["HandleDeckMachineSelection"] = {"compare": ("f",), "preserve": ()}
CASES["HandleDeckMachineSelection"] = [
    {"wram": {0xCABB: b"\x00", 0xCEA1: b"\x03", 0xCEA4: b"\x00", 0xD087: b"\x00", 0xD086: b"\x00", 0xD00D: b"\x00\xC0", 0xFFB3: b"\x00"}, "sram": {0: {}}, "keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xCEA1: 1, 0xCEA4: 1, 0xD087: 1, 0xD086: 1, 0xCEB1: 1, 0xFFB3: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xCABB: b"\x00", 0xCEA1: b"\x03", 0xCEA4: b"\x00", 0xD087: b"\x00", 0xD086: b"\x00", 0xD00D: b"\x00\xC0", 0xFFB3: b"\x00"}, sram={0: {}}, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xCEA1: 1, 0xCEA4: 1, 0xD087: 1, 0xD086: 1, 0xCEB1: 1, 0xFFB3: 1}, instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory HandleDeckMachineSelection

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
MUTATIONS["CheckIfSelectedDeckMachineEntryIsEmpty"] = {"source_symbol": "CheckIfSelectedDeckMachineEntryIsEmpty", "before": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);", "after": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE - 1u);", "case_ids": ["CheckIfSelectedDeckMachineEntryIsEmpty-0", "CheckIfSelectedDeckMachineEntryIsEmpty-1"]}
# <<< factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
# >>> factory-mutation SafelySwitchToSRAM1
MUTATIONS["SafelySwitchToSRAM1"] = {"source_symbol": "SafelySwitchToSRAM1", "before": "if (hBankSRAM != 1u)", "after": "if (hBankSRAM == 1u)", "case_ids": ["SafelySwitchToSRAM1-0", "SafelySwitchToSRAM1-2"]}
# <<< factory-mutation SafelySwitchToSRAM1
# >>> factory-mutation SafelySwitchToTempSRAMBank
MUTATIONS["SafelySwitchToTempSRAMBank"] = {"source_symbol": "SafelySwitchToTempSRAMBank", "before": "if (hBankSRAM != wTempBankSRAM)", "after": "if (hBankSRAM != (uint8_t)(wTempBankSRAM + 1u))", "case_ids": ["SafelySwitchToTempSRAMBank-1"]}
# <<< factory-mutation SafelySwitchToTempSRAMBank
# >>> factory-mutation CheckIfHasEnoughCardsToBuildDeck
MUTATIONS["CheckIfHasEnoughCardsToBuildDeck"] = {"source_symbol": "CheckIfHasEnoughCardsToBuildDeck", "before": "if (count == 0u || count == CARD_NOT_OWNED)", "after": "if (count == 0u && count == CARD_NOT_OWNED)", "case_ids": ["CheckIfHasEnoughCardsToBuildDeck-0", "CheckIfHasEnoughCardsToBuildDeck-2", "CheckIfHasEnoughCardsToBuildDeck-3"]}
# <<< factory-mutation CheckIfHasEnoughCardsToBuildDeck
# >>> factory-mutation GetSavedDeckPointers
MUTATIONS["GetSavedDeckPointers"] = {
	"source_symbol": "GetSavedDeckPointers",
	"before": "gb_write8(d++, (uint8_t)h);\n\t\tgb_write8(d++, (uint8_t)(h >> 8));",
	"after": "gb_write8(d++, (uint8_t)(h >> 8));\n\t\tgb_write8(d++, (uint8_t)h);",
	"case_ids": ["GetSavedDeckPointers-0", "GetSavedDeckPointers-1"],
}
# <<< factory-mutation GetSavedDeckPointers
# >>> factory-mutation GetSavedDeckCount
MUTATIONS["GetSavedDeckCount"] = {"source_symbol": "GetSavedDeckCount", "before": "i * DECK_STRUCT_SIZE", "after": "i * (DECK_STRUCT_SIZE - 1u)", "case_ids": ["GetSavedDeckCount-1", "GetSavedDeckCount-3", "GetSavedDeckCount-4"]}
# <<< factory-mutation GetSavedDeckCount
# >>> factory-mutation GetSelectedSavedDeckPtr
MUTATIONS["GetSelectedSavedDeckPtr"] = {"source_symbol": "GetSelectedSavedDeckPtr", "before": "(uint8_t)(index << 1)", "after": "index", "case_ids": ["GetSelectedSavedDeckPtr-1", "GetSelectedSavedDeckPtr-3", "GetSelectedSavedDeckPtr-4"]}
# <<< factory-mutation GetSelectedSavedDeckPtr
# >>> factory-mutation SafelySwitchToSRAM0
MUTATIONS["SafelySwitchToSRAM0"] = {"source_symbol": "SafelySwitchToSRAM0", "before": "if (bank != 0u)", "after": "if (bank == 0u)", "case_ids": ["SafelySwitchToSRAM0-1", "SafelySwitchToSRAM0-2", "SafelySwitchToSRAM0-3"]}
# <<< factory-mutation SafelySwitchToSRAM0
# >>> factory-mutation DrawListScrollArrows
MUTATIONS["DrawListScrollArrows"] = {
    "source_symbol": "DrawListScrollArrows",
    "before": "WriteByteToBGMap0(tile, 19u, 1u);",
    "after": "WriteByteToBGMap0(tile, 19u, 11u);",
    "case_ids": ["DrawListScrollArrows-0", "DrawListScrollArrows-1", "DrawListScrollArrows-2", "DrawListScrollArrows-3"],
}
# <<< factory-mutation DrawListScrollArrows
# >>> factory-mutation SetDeckMachineTitleText
MUTATIONS["SetDeckMachineTitleText"] = {"source_symbol": "SetDeckMachineTitleText", "before": "\tInitTextPrinting(1u, 0u);", "after": "\tInitTextPrinting(0u, 0u);", "case_ids": ["SetDeckMachineTitleText-0", "SetDeckMachineTitleText-1"]}
# <<< factory-mutation SetDeckMachineTitleText
# >>> factory-mutation FindFirstEmptyDeckSlot
MUTATIONS["FindFirstEmptyDeckSlot"] = {"source_symbol": "FindFirstEmptyDeckSlot", "before": "\treturn (FindFirstEmptyDeckSlotResult){0u, 0x80u, hl};", "after": "\treturn (FindFirstEmptyDeckSlotResult){1u, 0x80u, hl};", "case_ids": ["FindFirstEmptyDeckSlot-0"]}
# <<< factory-mutation FindFirstEmptyDeckSlot
# >>> factory-mutation EmptyScreenAndDrawTextBox
MUTATIONS["EmptyScreenAndDrawTextBox"] = {"source_symbol": "EmptyScreenAndDrawTextBox", "before": "\tDrawRegularTextBox(&hl, 0u, 20u, 13u, 0u, 0u);", "after": "\tDrawRegularTextBox(&hl, 0u, 19u, 13u, 0u, 0u);", "case_ids": ["EmptyScreenAndDrawTextBox-0", "EmptyScreenAndDrawTextBox-1"]}
# <<< factory-mutation EmptyScreenAndDrawTextBox
# >>> factory-mutation PrintCardToSendText
MUTATIONS["PrintCardToSendText"] = {"source_symbol": "PrintCardToSendText", "before": "\tProcessTextFromID(CardToSendText);", "after": "\tProcessTextFromID(0u);", "case_ids": ["PrintCardToSendText-0", "PrintCardToSendText-1"]}
# <<< factory-mutation PrintCardToSendText
# >>> factory-mutation PrintReceivedTheseCardsText
MUTATIONS["PrintReceivedTheseCardsText"] = {"source_symbol": "PrintReceivedTheseCardsText", "before": "\tCopyListFromHLToDE(&hl, &de);", "after": "\t(void)hl; (void)de;", "case_ids": ["PrintReceivedTheseCardsText-0", "PrintReceivedTheseCardsText-1"]}
# <<< factory-mutation PrintReceivedTheseCardsText
# >>> factory-mutation PrintNumSavedDecks
MUTATIONS["PrintNumSavedDecks"] = {"source_symbol": "PrintNumSavedDecks", "before": "gb_write8(hl, SYM_SLASH);", "after": "gb_write8(hl, TX_SYMBOL);", "case_ids": ["PrintNumSavedDecks-0", "PrintNumSavedDecks-1"]}
# <<< factory-mutation PrintNumSavedDecks
# >>> factory-mutation Func_b568
MUTATIONS["Func_b568"] = {"source_symbol": "Func_b568", "before": "\tuint8_t b = wCardListCursorPos;\n\tuint8_t a = (uint8_t)(wCardListVisibleOffset + b + 1u);", "after": "\tuint8_t b = wCardListCursorPos;\n\tuint8_t a = (uint8_t)(wCardListVisibleOffset + b);", "case_ids": ["Func_b568-0", "Func_b568-1"]}
# <<< factory-mutation Func_b568
# >>> factory-mutation CheckIfCanBuildSavedDeck
MUTATIONS["CheckIfCanBuildSavedDeck"] = {
    "source_symbol": "CheckIfCanBuildSavedDeck",
    "before": "\tDeckBuildCheckResult r = CheckIfHasEnoughCardsToBuildDeck(&ptr);\n\treturn r;",
    "after": "\tDeckBuildCheckResult r = CheckIfHasEnoughCardsToBuildDeck(&ptr);\n\tr.a = (uint8_t)(r.a + 1u);\n\treturn r;",
    "case_ids": ["CheckIfCanBuildSavedDeck-0", "CheckIfCanBuildSavedDeck-1"],
}
# <<< factory-mutation CheckIfCanBuildSavedDeck
# >>> factory-mutation PrintDeckMachineEntry
MUTATIONS["PrintDeckMachineEntry"] = {
    "source_symbol": "PrintDeckMachineEntry",
    "before": "if (af_result & 0x10u) {",
    "after": "if (af_result & 0x20u) {",
    "case_ids": ["PrintDeckMachineEntry-0", "PrintDeckMachineEntry-1"],
}
# <<< factory-mutation PrintDeckMachineEntry
# >>> factory-mutation ShowReceivedCardsList
MUTATIONS["ShowReceivedCardsList"] = {"source_symbol": "ShowReceivedCardsList", "before": "gb_write8(wTxRam2_ADDR, 0x00u);", "after": "gb_write8(wTxRam2_ADDR, 0x01u);", "case_ids": ["ShowReceivedCardsList-0", "ShowReceivedCardsList-1"]}
# <<< factory-mutation ShowReceivedCardsList
# >>> factory-mutation Func_b088
MUTATIONS["Func_b088"] = {
    "source_symbol": "Func_b088",
    "before": "\tuint8_t f = 0x40u;\n\treturn (Func_b088Result){a, f};",
    "after": "\tuint8_t f = 0x00u;\n\treturn (Func_b088Result){a, f};",
    "case_ids": ["Func_b088-0", "Func_b088-1"],
}
# <<< factory-mutation Func_b088
# >>> factory-mutation TryDeleteSavedDeck
MUTATIONS["TryDeleteSavedDeck"] = {
    "source_symbol": "TryDeleteSavedDeck",
    "before": "TryDeleteSavedDeckResult TryDeleteSavedDeck(void)\n{\n\tHandleYesOrNoMenuResult choice = YesOrNoMenuWithText(DoYouReallyWishToDeleteText);\n\tif (choice.f & 0x10u) {\n\t\tuint8_t cursor = wCardListCursorPos;",
    "after": "TryDeleteSavedDeckResult TryDeleteSavedDeck(void)\n{\n\tHandleYesOrNoMenuResult choice = YesOrNoMenuWithText(DoYouReallyWishToDeleteText);\n\tif (choice.f & 0x10u) {\n\t\tuint8_t cursor = (uint8_t)(wCardListCursorPos + 1u);",
    "case_ids": ["TryDeleteSavedDeck-0", "TryDeleteSavedDeck-1"],
}
# <<< factory-mutation TryDeleteSavedDeck
# >>> factory-mutation HandleDeckMissingCardsList
MUTATIONS["HandleDeckMissingCardsList"] = {
    "source_symbol": "HandleDeckMissingCardsList",
    # wCardListUpdateFunction ($CECE) is seeded, so both of its bytes are
    # compared: corrupting the low half of the stored $6E9A is visible to every
    # case, and no sibling in deck_machine.c names this constant.
    "before": "gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)CARD_LIST_UPDATE_FUNCTION_ADDR);",
    "after": "gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)(CARD_LIST_UPDATE_FUNCTION_ADDR + 1u));",
    "case_ids": [
        "HandleDeckMissingCardsList-0",
        "HandleDeckMissingCardsList-1",
        "HandleDeckMissingCardsList-2",
    ],
}
# <<< factory-mutation HandleDeckMissingCardsList
# >>> factory-mutation HandleDismantleDeckToMakeSpace
MUTATIONS["HandleDismantleDeckToMakeSpace"] = {
    "source_symbol": "HandleDismantleDeckToMakeSpace",
    "before": "\t\t\t\treturn (HandleDismantleDeckToMakeSpaceResult){hCurMenuItem, 0x90u};",
    "after": "\t\t\t\treturn (HandleDismantleDeckToMakeSpaceResult){0u, 0x90u};",
    "case_ids": ["HandleDismantleDeckToMakeSpace-0", "HandleDismantleDeckToMakeSpace-1"],
}
# <<< factory-mutation HandleDismantleDeckToMakeSpace
# >>> factory-mutation PrintVisibleDeckMachineEntries
MUTATIONS["PrintVisibleDeckMachineEntries"] = {"source_symbol": "PrintVisibleDeckMachineEntries", "before": "\tuint8_t a = wCardListVisibleOffset;", "after": "\tuint8_t a = (uint8_t)(wCardListVisibleOffset + 1u);", "case_ids": ["PrintVisibleDeckMachineEntries-0", "PrintVisibleDeckMachineEntries-1", "PrintVisibleDeckMachineEntries-2"]}
# <<< factory-mutation PrintVisibleDeckMachineEntries
# >>> factory-mutation ClearScreenAndDrawDeckMachineScreen
MUTATIONS["ClearScreenAndDrawDeckMachineScreen"] = {"source_symbol": "ClearScreenAndDrawDeckMachineScreen", "before": "\twTileMapFill = 0u;", "after": "\twTileMapFill = 1u;", "case_ids": ["ClearScreenAndDrawDeckMachineScreen-0", "ClearScreenAndDrawDeckMachineScreen-1"]}
# <<< factory-mutation ClearScreenAndDrawDeckMachineScreen
# >>> factory-mutation DrawDeckMachineScreen
MUTATIONS["DrawDeckMachineScreen"] = {"source_symbol": "DrawDeckMachineScreen", "before": "\thffb0 = 0x00u;", "after": "\thffb0 = 0x01u;", "case_ids": ["DrawDeckMachineScreen-0", "DrawDeckMachineScreen-1"]}
# <<< factory-mutation DrawDeckMachineScreen
# >>> factory-mutation HandleDeckMachineSelection
MUTATIONS["HandleDeckMachineSelection"] = {"source_symbol": "HandleDeckMachineSelection", "before": "\t\t\tDrawListCursor_Visible();\n\t\t\twTempCardListVisibleOffset = wCardListVisibleOffset;", "after": "\t\t\tDrawListCursor_Visible();\n\t\t\twTempCardListVisibleOffset = 0u;", "case_ids": ["HandleDeckMachineSelection-0", "HandleDeckMachineSelection-1"]}
# <<< factory-mutation HandleDeckMachineSelection
