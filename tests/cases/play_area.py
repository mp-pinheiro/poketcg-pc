from tests.cases._symbols import sym
from tests.cases._fixtures import in_play_area_b_exit_fixture as _in_play_area_b_exit_fixture, IN_PLAY_AREA_B_EXIT_REGS as _IN_PLAY_AREA_B_EXIT_REGS
wOAM = sym("wOAM")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")
OAM_SIZE = 160

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "d", "e"),
    },
}

OAM = bytes((0x10, 0x20, 0x30, 0x40)) * 40

CASES = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": [
        {"wram": {wOAM: b"\x00" * OAM_SIZE,
                  wVBlankOAMCopyToggle: b"\x00"},
         "read": {wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}},
        dict(POISON, wram={wOAM: OAM,
                           wVBlankOAMCopyToggle: b"\xFF"},
             read={wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}),
        {"wram": {wOAM: OAM,
                  wVBlankOAMCopyToggle: b"\x00"},
         "read": {wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}},
    ],
}

MUTATIONS = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": {
        "source_symbol": "ZeroObjectPositionsAndToggleOAMCopy_Bank6",
        "before": "gb_write8(wVBlankOAMCopyToggle_ADDR, 1);",
        "after": "gb_write8(wVBlankOAMCopyToggle_ADDR, 0);",
        "case_ids": ["ZeroObjectPositionsAndToggleOAMCopy_Bank6-0",
                     "ZeroObjectPositionsAndToggleOAMCopy_Bank6-1",
                     "ZeroObjectPositionsAndToggleOAMCopy_Bank6-2"],
    },
}

# >>> factory OpenInPlayAreaScreen_HandleInput
CONTRACT["OpenInPlayAreaScreen_HandleInput"] = {"compare": ("a", "f"), "preserve": ()}
# The routine reads the joypad snapshot without polling, so the frame's B press
# (hDPadHeld, hKeysHeld, hKeysPressed) is seeded here; the fixture leaves it out.
_B_EXIT = _in_play_area_b_exit_fixture(bank=6)
_B_EXIT["wram"] = {**_B_EXIT["wram"], sym("hDPadHeld"): b"\x02", sym("hKeysHeld"): b"\x02", sym("hKeysPressed"): b"\x02"}
_B_EXIT["read"] = {**_B_EXIT["read"], sym("wCheckMenuCursorBlinkCounter"): 1}
CASES["OpenInPlayAreaScreen_HandleInput"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            sym("wCheckMenuCursorBlinkCounter"): b"\x01",   # wCheckMenuCursorBlinkCounter = 1
        },
        "hram": {sym("hDPadHeld"): b"\x00", sym("hKeysPressed"): b"\x00"},   # hDPadHeld=0, hKeysPressed=0
        "expect_regs": {"a": 0x01, "f": 0x20},
    },
    dict(_B_EXIT, **_IN_PLAY_AREA_B_EXIT_REGS),
]
# <<< factory OpenInPlayAreaScreen_HandleInput

# >>> factory OpenInPlayAreaScreen_TurnHolderPlayArea
CONTRACT["OpenInPlayAreaScreen_TurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_TurnHolderPlayArea"] = [
    {"wram": {sym("wInPlayAreaCurPosition"): b"\x05", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {sym("wCurPlayAreaSlot"): 1}, "expect": {sym("wCurPlayAreaSlot"): b"\x00"}},
    {"wram": {sym("wInPlayAreaCurPosition"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {sym("wCurPlayAreaSlot"): 1}, "expect": {sym("wCurPlayAreaSlot"): b"\x01"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wInPlayAreaCurPosition"): b"\x05", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {sym("wCurPlayAreaSlot"): 1}, "expect": {sym("wCurPlayAreaSlot"): b"\x00"}}]
# <<< factory OpenInPlayAreaScreen_TurnHolderPlayArea

# >>> factory-cases-statics
wInPlayAreaCurPosition = sym("wInPlayAreaCurPosition")
wCurPlayAreaSlot = sym("wCurPlayAreaSlot")
wCurPlayAreaY = sym("wCurPlayAreaY")

hBankROM = sym("hBankROM")
hDPadHeld = sym("hDPadHeld")
hWhoseTurn = sym("hWhoseTurn")
wDefaultText = sym("wDefaultText")
wInPlayAreaCurPosition = sym("wInPlayAreaCurPosition")
wInPlayAreaFromSelectButton = sym("wInPlayAreaFromSelectButton")
wMenuInputTablePointer = sym("wMenuInputTablePointer")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")
# <<< factory-cases-statics

# >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderPlayArea"] = [
    {"wram": {wInPlayAreaCurPosition: b"\x08", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00"}},
    {"wram": {wInPlayAreaCurPosition: b"\x0B", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x01", wCurPlayAreaY: b"\x00"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wInPlayAreaCurPosition: b"\x08", sym("wLCDC"): b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00"}}]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderPlayArea

# >>> factory OpenInPlayAreaScreen_TurnHolderDiscardPile
CONTRACT["OpenInPlayAreaScreen_TurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_TurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, "read": {sym("wDuelTempList"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02", sym("wPlayerDeckCards"): b"\x11\x22", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00", sym("wDuelTempList"): b"\xFF", sym("wNoItemSelectionMenuKeys"): b"\x00"}, "read": {sym("wNoItemSelectionMenuKeys"): 1, sym("wDuelTempList"): 3}, "expect": {sym("wNoItemSelectionMenuKeys"): b"\x09"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, read={sym("wDuelTempList"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenInPlayAreaScreen_TurnHolderDiscardPile

# >>> factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wDecompressionSecondaryBufferStart") + 0xFE: b"\x00", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFE: b"\x00", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC1"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wDecompressionSecondaryBufferStart") + 0xFE: b"\x00", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, read={sym("hWhoseTurn"): 1}, expect={sym("hWhoseTurn"): b"\xC2"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile

# >>> factory OpenInPlayAreaScreen_NonTurnHolderHand
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderHand"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderHand"] = [
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wOpponentNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wOpponentNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}}
]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderHand

# >>> factory OpenInPlayAreaScreen_TurnHolderHand
CONTRACT["OpenInPlayAreaScreen_TurnHolderHand"] = {"compare": ("a", "f"), "preserve": ("f",)}
CASES["OpenInPlayAreaScreen_TurnHolderHand"] = [
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC1", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC1"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, read={sym("hWhoseTurn"): 1}, expect={sym("hWhoseTurn"): b"\xC2"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenInPlayAreaScreen_TurnHolderHand

# >>> factory OpenInPlayAreaScreen
# play_area.asm:62-78. The carry is the screen's only output: set when B
# backs out, clear on the Select-button skip.
CONTRACT["OpenInPlayAreaScreen"] = {"compare": ("f",), "preserve": ()}
CASES["OpenInPlayAreaScreen"] = [
    {"keys": [0x00, 0x02], "hram": {hBankROM: b"\x01"}, "wram": {wInPlayAreaFromSelectButton: b"\x00", wInPlayAreaCurPosition: b"\xAA"}, "expect": {hBankROM: b"\x06", wInPlayAreaCurPosition: b"\x05"}, "read": {hBankROM: 1, wInPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x04], hram={hBankROM: b"\x01"}, wram={wInPlayAreaFromSelectButton: b"\x01", wInPlayAreaCurPosition: b"\xAA"}, expect={hBankROM: b"\x06", wInPlayAreaCurPosition: b"\x05"}, read={hBankROM: 1, wInPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory OpenInPlayAreaScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation OpenInPlayAreaScreen_HandleInput
MUTATIONS["OpenInPlayAreaScreen_HandleInput"] = {
    "source_symbol": "OpenInPlayAreaScreen_HandleInput",
    "before": "if (masked != 0u)\n\t\treturn (OpenInPlayAreaScreenHandleInputResult){masked, 0x20u};",
    "after": "if (masked != 0u)\n\t\treturn (OpenInPlayAreaScreenHandleInputResult){0u, 0x20u};",
    "case_ids": ["OpenInPlayAreaScreen_HandleInput-0"],
}
# <<< factory-mutation OpenInPlayAreaScreen_HandleInput
# >>> factory-mutation OpenInPlayAreaScreen_TurnHolderPlayArea
MUTATIONS["OpenInPlayAreaScreen_TurnHolderPlayArea"] = {"source_symbol": "OpenInPlayAreaScreen_TurnHolderPlayArea", "before": "void OpenInPlayAreaScreen_TurnHolderPlayArea(void)\n{\n\tuint8_t slot = (uint8_t)(wInPlayAreaCurPosition + 1u);", "after": "void OpenInPlayAreaScreen_TurnHolderPlayArea(void)\n{\n\tuint8_t slot = (uint8_t)(wInPlayAreaCurPosition + 2u);", "case_ids": ["OpenInPlayAreaScreen_TurnHolderPlayArea-0", "OpenInPlayAreaScreen_TurnHolderPlayArea-1", "OpenInPlayAreaScreen_TurnHolderPlayArea-2"]}
# <<< factory-mutation OpenInPlayAreaScreen_TurnHolderPlayArea
# >>> factory-mutation OpenInPlayAreaScreen_NonTurnHolderPlayArea
MUTATIONS["OpenInPlayAreaScreen_NonTurnHolderPlayArea"] = {"source_symbol": "OpenInPlayAreaScreen_NonTurnHolderPlayArea", "before": "void OpenInPlayAreaScreen_NonTurnHolderPlayArea(void)\n{\n\tuint8_t slot = (uint8_t)(wInPlayAreaCurPosition - INPLAYAREA_OPP_ACTIVE);", "after": "void OpenInPlayAreaScreen_NonTurnHolderPlayArea(void)\n{\n\tuint8_t slot = (uint8_t)(wInPlayAreaCurPosition - INPLAYAREA_OPP_ACTIVE - 1u);", "case_ids": ["OpenInPlayAreaScreen_NonTurnHolderPlayArea-0", "OpenInPlayAreaScreen_NonTurnHolderPlayArea-1", "OpenInPlayAreaScreen_NonTurnHolderPlayArea-2"]}
# <<< factory-mutation OpenInPlayAreaScreen_NonTurnHolderPlayArea
# >>> factory-mutation OpenInPlayAreaScreen_TurnHolderDiscardPile
MUTATIONS["OpenInPlayAreaScreen_TurnHolderDiscardPile"] = {"source_symbol": "OpenInPlayAreaScreen_TurnHolderDiscardPile", "before": "void OpenInPlayAreaScreen_TurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;\n\t(void)OpenTurnHolderDiscardPileScreen(c);", "after": "void OpenInPlayAreaScreen_TurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;\n\t(void)0;", "case_ids": ["OpenInPlayAreaScreen_TurnHolderDiscardPile-0", "OpenInPlayAreaScreen_TurnHolderDiscardPile-1", "OpenInPlayAreaScreen_TurnHolderDiscardPile-2"]}
# <<< factory-mutation OpenInPlayAreaScreen_TurnHolderDiscardPile
# >>> factory-mutation OpenInPlayAreaScreen_NonTurnHolderDiscardPile
MUTATIONS["OpenInPlayAreaScreen_NonTurnHolderDiscardPile"] = {"source_symbol": "OpenInPlayAreaScreen_NonTurnHolderDiscardPile", "before": "void OpenInPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "void OpenInPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenInPlayAreaScreen_NonTurnHolderDiscardPile-0", "OpenInPlayAreaScreen_NonTurnHolderDiscardPile-1", "OpenInPlayAreaScreen_NonTurnHolderDiscardPile-2"]}
# <<< factory-mutation OpenInPlayAreaScreen_NonTurnHolderDiscardPile
# >>> factory-mutation OpenInPlayAreaScreen_NonTurnHolderHand
MUTATIONS["OpenInPlayAreaScreen_NonTurnHolderHand"] = {"source_symbol": "OpenInPlayAreaScreen_NonTurnHolderHand", "before": "void OpenInPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "void OpenInPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenInPlayAreaScreen_NonTurnHolderHand-0", "OpenInPlayAreaScreen_NonTurnHolderHand-1"]}
# <<< factory-mutation OpenInPlayAreaScreen_NonTurnHolderHand
# >>> factory-mutation OpenInPlayAreaScreen_TurnHolderHand
MUTATIONS["OpenInPlayAreaScreen_TurnHolderHand"] = {"source_symbol": "OpenInPlayAreaScreen_TurnHolderHand", "before": "uint8_t OpenInPlayAreaScreen_TurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "uint8_t OpenInPlayAreaScreen_TurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenInPlayAreaScreen_TurnHolderHand-0", "OpenInPlayAreaScreen_TurnHolderHand-1", "OpenInPlayAreaScreen_TurnHolderHand-2"]}
# <<< factory-mutation OpenInPlayAreaScreen_TurnHolderHand
# >>> factory-mutation OpenInPlayAreaScreen
MUTATIONS["OpenInPlayAreaScreen"] = {"source_symbol": "OpenInPlayAreaScreen", "before": "\twInPlayAreaCurPosition = INPLAYAREA_PLAYER_ACTIVE;", "after": "\twInPlayAreaCurPosition = INPLAYAREA_PLAYER_HAND;", "case_ids": ["OpenInPlayAreaScreen-0", "OpenInPlayAreaScreen-1"]}
# <<< factory-mutation OpenInPlayAreaScreen
