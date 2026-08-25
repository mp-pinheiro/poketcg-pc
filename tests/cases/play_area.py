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
