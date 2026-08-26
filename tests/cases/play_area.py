wOAM = 0xCA00
wVBlankOAMCopyToggle = 0xCAC0
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
CASES["OpenInPlayAreaScreen_HandleInput"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            0xCEA3: b"\x01",   # wCheckMenuCursorBlinkCounter = 1
        },
        "hram": {0xFF8F: b"\x00", 0xFF91: b"\x00"},   # hDPadHeld=0, hKeysPressed=0
        "expect_regs": {"a": 0x01, "f": 0x20},
    },
]
# <<< factory OpenInPlayAreaScreen_HandleInput

# >>> factory OpenInPlayAreaScreen_TurnHolderPlayArea
CONTRACT["OpenInPlayAreaScreen_TurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_TurnHolderPlayArea"] = [
    {"wram": {0xCE52: b"\x05", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {0xCBC9: 1}, "expect": {0xCBC9: b"\x00"}},
    {"wram": {0xCE52: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {0xCBC9: 1}, "expect": {0xCBC9: b"\x01"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCE52: b"\x05", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {0xCBC9: 1}, "expect": {0xCBC9: b"\x00"}}]
# <<< factory OpenInPlayAreaScreen_TurnHolderPlayArea

# >>> factory-cases-statics
wInPlayAreaCurPosition = 0xCE52
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
# <<< factory-cases-statics

# >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderPlayArea"] = [
    {"wram": {wInPlayAreaCurPosition: b"\x08", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00"}},
    {"wram": {wInPlayAreaCurPosition: b"\x0B", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x01", wCurPlayAreaY: b"\x00"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wInPlayAreaCurPosition: b"\x08", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}, "expect": {wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00"}}]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderPlayArea

# >>> factory OpenInPlayAreaScreen_TurnHolderDiscardPile
CONTRACT["OpenInPlayAreaScreen_TurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_TurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC2ED: b"\x00", 0xCABB: b"\x00", 0xC590: b"\x00"}, "read": {0xC510: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xC2ED: b"\x02", 0xC27E: b"\x11\x22", 0xCABB: b"\x00", 0xC590: b"\x00", 0xC510: b"\xFF", 0xCBD6: b"\x00"}, "read": {0xCBD6: 1, 0xC510: 3}, "expect": {0xCBD6: b"\x09"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC2ED: b"\x00", 0xCABB: b"\x00", 0xC590: b"\x00"}, read={0xC510: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenInPlayAreaScreen_TurnHolderDiscardPile

# >>> factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC1ED: b"\x00", 0xC2ED: b"\x00", 0xCABB: b"\x00", 0xC590: b"\x00"}, "read": {0xFF97: 1}, "expect": {0xFF97: b"\xC2"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC1", 0xC1ED: b"\x00", 0xC2ED: b"\x00", 0xCABB: b"\x00", 0xC590: b"\x00"}, "read": {0xFF97: 1}, "expect": {0xFF97: b"\xC1"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC1ED: b"\x00", 0xC2ED: b"\x00", 0xCABB: b"\x00", 0xC590: b"\x00"}, read={0xFF97: 1}, expect={0xFF97: b"\xC2"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile

# >>> factory OpenInPlayAreaScreen_NonTurnHolderHand
# >>> factory OpenInPlayAreaScreen_NonTurnHolderHand
CONTRACT["OpenInPlayAreaScreen_NonTurnHolderHand"] = {"compare": (), "preserve": ()}
CASES["OpenInPlayAreaScreen_NonTurnHolderHand"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC3EE: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {0xFF97: 1}, "expect": {0xFF97: b"\xC2"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC3EE: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {0xFF97: 1}, "expect": {0xFF97: b"\xC2"}}
]
# <<< factory OpenInPlayAreaScreen_NonTurnHolderHand

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
# >>> factory-mutation OpenInPlayAreaScreen_NonTurnHolderHand
MUTATIONS["OpenInPlayAreaScreen_NonTurnHolderHand"] = {"source_symbol": "OpenInPlayAreaScreen_NonTurnHolderHand", "before": "void OpenInPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "void OpenInPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenInPlayAreaScreen_NonTurnHolderHand-0", "OpenInPlayAreaScreen_NonTurnHolderHand-1"]}
# <<< factory-mutation OpenInPlayAreaScreen_NonTurnHolderHand
