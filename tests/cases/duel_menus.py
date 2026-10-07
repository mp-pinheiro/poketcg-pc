"""Oracle-diff cases for poketcg/src/home/duel_menus.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
hBankROM_A = sym("hBankROM")
wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
wTileMapFill = sym("wUnavailableAlbumCardSets") + 3
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hBankROM_B = sym("hBankROM")
hWhoseTurn_B = sym("hWhoseTurn")
wCheckMenuPlayAreaWhichDuelist_B = sym("wCheckMenuPlayAreaWhichDuelist")
wCheckMenuPlayAreaWhichLayout_B = sym("wCheckMenuPlayAreaWhichLayout")
wDefaultText_B = sym("wCurDeckCardChanges")

hBankROM = sym("hBankROM")
hWhoseTurn = sym("hWhoseTurn")
wDefaultText = sym("wDefaultText")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")
wYourOrOppPlayAreaCurPosition = sym("wYourOrOppPlayAreaCurPosition")
wMenuInputTablePointer = sym("wMenuInputTablePointer")
wIsSwapTurnPending = sym("wIsSwapTurnPending")

wNumberOfPrizeCardsToSelect = sym("wNumberOfPrizeCardsToSelect")

hBankROM = sym("hBankROM")
_hps_wram = {
    sym("hWhoseTurn"): b"\xC2",
    sym("wPlayerPrizeCards"): b"\x00",
    sym("wPlayerPrizes"): b"\x3F",
    sym("wBoosterCardsDrawn"): b"\x08",
    sym("wLCDC"): b"\x00",
}
_hps_read = {sym("hBankROM"): 1, sym("wInPlayAreaCurPosition"): 1, sym("wMenuInputTablePointer"): 2, sym("wIsSwapTurnPending"): 1, sym("wce5c"): 1}
_hps_setup = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory DrawPlayersPrizeAndBenchCards
CONTRACT["DrawPlayersPrizeAndBenchCards"] = {"compare": (), "preserve": ()}
CASES["DrawPlayersPrizeAndBenchCards"] = [
    {"wram": {hBankROM_A: b"\x01"}, "instruction_budget": 1000000, "cycle_budget": 4000000,
     "read": {hBankROM_A: 1, wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "expect": {hBankROM_A: b"\x01", wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}},
    dict(POISON, wram={hBankROM_A: b"\x01"}, instruction_budget=1000000, cycle_budget=4000000,
         read={hBankROM_A: 1, wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         expect={hBankROM_A: b"\x01", wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}),
]
# <<< factory DrawPlayersPrizeAndBenchCards

# >>> factory DrawPlayAreaToPlacePrizeCards
CONTRACT["DrawPlayAreaToPlacePrizeCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawPlayAreaToPlacePrizeCards"] = [
    {"instruction_budget": 2000000, "cycle_budget": 8000000,
     "hram": {sym("hBankROM"): b"\x01", sym("hWhoseTurn"): b"\xC2"},
     "wram": {sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
     "read": {sym("hBankROM"): 1, sym("wCheckMenuPlayAreaWhichLayout"): 1, sym("wIsSwapTurnPending"): 1},
     "expect": {sym("hBankROM"): b"\x01"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=2000000, cycle_budget=8000000,
         hram={sym("hBankROM"): b"\x37", sym("hWhoseTurn"): b"\xC2"},
         wram={sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
         read={sym("hBankROM"): 1, sym("wCheckMenuPlayAreaWhichLayout"): 1, sym("wIsSwapTurnPending"): 1},
         expect={sym("hBankROM"): b"\x37"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawPlayAreaToPlacePrizeCards

# >>> factory DrawYourOrOppPlayAreaScreen_Bank0
CONTRACT["DrawYourOrOppPlayAreaScreen_Bank0"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayAreaScreen_Bank0"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM_B: b"\x01", hWhoseTurn_B: b"\xC2"},
     "wram": {wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText_B: b"\x00" * 16},
     "read": {hBankROM_B: 1, wCheckMenuPlayAreaWhichDuelist_B: 1, wCheckMenuPlayAreaWhichLayout_B: 1},
     "expect": {hBankROM_B: b"\x01", wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "hl": sym("wPlayerArenaCardFlags")},
    dict(POISON, hl=sym("wPlayerArenaCardFlags"), instruction_budget=20000000, cycle_budget=80000000,
         hram={hBankROM_B: b"\x37", hWhoseTurn_B: b"\xC2"},
         wram={wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText_B: b"\x00" * 16},
         read={hBankROM_B: 1, wCheckMenuPlayAreaWhichDuelist_B: 1, wCheckMenuPlayAreaWhichLayout_B: 1},
         expect={hBankROM_B: b"\x37", wCheckMenuPlayAreaWhichDuelist_B: b"\xC2", wCheckMenuPlayAreaWhichLayout_B: b"\xC2"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayAreaScreen_Bank0

# >>> factory DrawAIPeekScreen
CONTRACT["DrawAIPeekScreen"] = {"compare": ("a", "f"), "preserve": ("f",)}
CASES["DrawAIPeekScreen"] = [
    {"keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM: b"\x01", hWhoseTurn: b"\xC2"},
     "wram": {sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
     "read": {hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         hram={hBankROM: b"\x37", hWhoseTurn: b"\xC2"},
         wram={sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
         read={hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
         vread={0: {0x9800: 32, 0x9C00: 32}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
    {"a": 0xFF, "f": 0x00, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {hBankROM: b"\x02", hWhoseTurn: b"\xC2"},
     "wram": {sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
     "read": {hBankROM: 1, wIsSwapTurnPending: 1, wMenuInputTablePointer: 2,
               wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]}]
# <<< factory DrawAIPeekScreen

# >>> factory SelectPrizeCards
CONTRACT["SelectPrizeCards"] = {"compare": (), "preserve": ()}
CASES["SelectPrizeCards"] = [
    {"a": 0x00, "f": 0x00, "wram": {wNumberOfPrizeCardsToSelect: b"\x00", hBankROM: b"\x01", sym("hWhoseTurn"): b"\xC2", sym("wPlayerPrizes"): b"\x00"}, "instruction_budget": 2000000, "cycle_budget": 8000000, "read": {wNumberOfPrizeCardsToSelect: 1, hBankROM: 1, sym("wInPlayAreaCurPosition"): 1, sym("wSelectedPrizeCardListPtr"): 2, sym("hTempList"): 1, sym("hAIPkmnPowerEffectParam"): 1}},
    dict(POISON, a=0x00, wram={wNumberOfPrizeCardsToSelect: b"\x00", hBankROM: b"\x37", sym("hWhoseTurn"): b"\xC2", sym("wPlayerPrizes"): b"\x00"}, instruction_budget=2000000, cycle_budget=8000000, read={wNumberOfPrizeCardsToSelect: 1, hBankROM: 1, sym("wInPlayAreaCurPosition"): 1, sym("wSelectedPrizeCardListPtr"): 2, sym("hTempList"): 1, sym("hAIPkmnPowerEffectParam"): 1})
]
# <<< factory SelectPrizeCards

# >>> factory HandlePeekSelection
CONTRACT["HandlePeekSelection"] = {"compare": ("a", "f"), "preserve": ("f",), "wram_out": True}
CASES["HandlePeekSelection"] = [
    {"f": 0x00, "keys": [0x00, 0x01], "wram": {**_hps_wram, hBankROM: b"\x01"}, "read": dict(_hps_read), "setup": _hps_setup, "instruction_budget": 30000000, "cycle_budget": 120000000},
    dict(POISON, keys=[0x00, 0x01], wram={**_hps_wram, hBankROM: b"\x01"}, read=dict(_hps_read), setup=_hps_setup, instruction_budget=30000000, cycle_budget=120000000),
]
# <<< factory HandlePeekSelection

# >>> factory OpenDuelCheckMenu
CONTRACT["OpenDuelCheckMenu"] = {"compare": (), "preserve": ()}
CASES["OpenDuelCheckMenu"] = [
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("hBankROM"): b"\x01"}, "read": {sym("hBankROM"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("hBankROM"): b"\x01"}, read={sym("hBankROM"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenDuelCheckMenu

# >>> factory OpenInPlayAreaScreen_FromSelectButton
# `f` is a real output: the screen's exits are `scf; ret` and `or a; ret`
# (play_area.asm:73-81) over SetupText's a=0/Z=1/H=1 return, giving $90 and
# $80. BankswitchROM sets no flags, so the wrapper passes it through.
CONTRACT["OpenInPlayAreaScreen_FromSelectButton"] = {"compare": ("f",), "preserve": ()}
CASES["OpenInPlayAreaScreen_FromSelectButton"] = [
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("hBankROM"): b"\x01"}, "read": {sym("hBankROM"): 1, sym("wInPlayAreaFromSelectButton"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("hBankROM"): b"\x01"}, read={sym("hBankROM"): 1, sym("wInPlayAreaFromSelectButton"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenInPlayAreaScreen_FromSelectButton

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DrawPlayersPrizeAndBenchCards
MUTATIONS["DrawPlayersPrizeAndBenchCards"] = {"source_symbol": "DrawPlayersPrizeAndBenchCards", "before": "\tBankswitchROM(saved_bank);", "after": "\tBankswitchROM(0u);", "case_ids": ["DrawPlayersPrizeAndBenchCards-0", "DrawPlayersPrizeAndBenchCards-1"]}
# <<< factory-mutation DrawPlayersPrizeAndBenchCards
# >>> factory-mutation DrawPlayAreaToPlacePrizeCards
MUTATIONS["DrawPlayAreaToPlacePrizeCards"] = {
    "source_symbol": "DrawPlayAreaToPlacePrizeCards",
    "before": "\t_DrawPlayAreaToPlacePrizeCards();\n\tBankswitchROM(saved_bank);",
    "after": "\t_DrawPlayAreaToPlacePrizeCards();\n\tBankswitchROM((uint8_t)(saved_bank ^ 1u));",
    "case_ids": ["DrawPlayAreaToPlacePrizeCards-0", "DrawPlayAreaToPlacePrizeCards-1"],
}
# <<< factory-mutation DrawPlayAreaToPlacePrizeCards
# >>> factory-mutation DrawYourOrOppPlayAreaScreen_Bank0
MUTATIONS["DrawYourOrOppPlayAreaScreen_Bank0"] = {"source_symbol": "DrawYourOrOppPlayAreaScreen_Bank0", "before": "\t(void)DrawWideTextBox();\n\tBankswitchROM(saved_bank);", "after": "\t(void)DrawWideTextBox();\n\tBankswitchROM(0u);", "case_ids": ["DrawYourOrOppPlayAreaScreen_Bank0-0", "DrawYourOrOppPlayAreaScreen_Bank0-1"]}
# <<< factory-mutation DrawYourOrOppPlayAreaScreen_Bank0
# >>> factory-mutation DrawAIPeekScreen
MUTATIONS["DrawAIPeekScreen"] = {"source_symbol": "DrawAIPeekScreen", "before": "\tBankswitchROM(saved_bank);\n\treturn (DrawAIPeekScreenResult){saved_bank, f};", "after": "\tBankswitchROM((uint8_t)(saved_bank ^ 1u));\n\treturn (DrawAIPeekScreenResult){saved_bank, f};", "case_ids": ["DrawAIPeekScreen-0", "DrawAIPeekScreen-1"]}
# <<< factory-mutation DrawAIPeekScreen
# >>> factory-mutation SelectPrizeCards
MUTATIONS["SelectPrizeCards"] = {"source_symbol": "SelectPrizeCards", "before": "\t_SelectPrizeCards();\n\tBankswitchROM(saved_bank);", "after": "\t_SelectPrizeCards();\n\tBankswitchROM((uint8_t)(saved_bank ^ 1u));", "case_ids": ["SelectPrizeCards-0", "SelectPrizeCards-1"]}
# <<< factory-mutation SelectPrizeCards
# >>> factory-mutation HandlePeekSelection
MUTATIONS["HandlePeekSelection"] = {
    "source_symbol": "HandlePeekSelection",
    "before": "\tHandlePeekSelectionResult inner = _HandlePeekSelection();\n\tBankswitchROM(saved_bank);",
    "after": "\tHandlePeekSelectionResult inner = _HandlePeekSelection();\n\tBankswitchROM((uint8_t)(saved_bank ^ 1u));",
    "case_ids": ["HandlePeekSelection-0", "HandlePeekSelection-1"],
}
# <<< factory-mutation HandlePeekSelection
# >>> factory-mutation OpenDuelCheckMenu
MUTATIONS["OpenDuelCheckMenu"] = {"source_symbol": "OpenDuelCheckMenu", "before": "\tBankswitchROM(saved_bank);", "after": "\tBankswitchROM((uint8_t)(saved_bank ^ 1u));", "case_ids": ["OpenDuelCheckMenu-0", "OpenDuelCheckMenu-1"]}
# <<< factory-mutation OpenDuelCheckMenu
# >>> factory-mutation OpenInPlayAreaScreen_FromSelectButton
MUTATIONS["OpenInPlayAreaScreen_FromSelectButton"] = {"source_symbol": "OpenInPlayAreaScreen_FromSelectButton", "before": "\twInPlayAreaFromSelectButton = 1u;", "after": "\twInPlayAreaFromSelectButton = 2u;", "case_ids": ["OpenInPlayAreaScreen_FromSelectButton-0", "OpenInPlayAreaScreen_FromSelectButton-1"]}
# <<< factory-mutation OpenInPlayAreaScreen_FromSelectButton
