POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPCPackSelection = 0xD11D
wPCPacks = 0xD11E

CONTRACT = {
    "GePCPackSelectionCoordinates": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "TryGivePCPack": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "GePCPackSelectionCoordinates": [
        {"wram": {wPCPackSelection: b"\x00"}},
        {"wram": {wPCPackSelection: b"\x0e"}},
        dict(POISON, wram={wPCPackSelection: b"\x0e"}),
    ],
    "TryGivePCPack": [
        {"wram": {wPCPacks: bytes(15)}},
        {"a": 1, "wram": {wPCPacks: bytes(15)}, "read": {wPCPacks: 15}},
        {"a": 15, "wram": {wPCPacks: bytes(14) + b"\x01"}, "read": {wPCPacks: 15}},
        dict(POISON, a=10, wram={wPCPacks: b"\x81\x02" + bytes(13)}, read={wPCPacks: 15}),
        {"a": 0x7f, "wram": {wPCPacks: bytes([1] * 15)}, "read": {wPCPacks: 15}},
    ],
}

# >>> factory InitPCPacks

CONTRACT["InitPCPacks"] = {"compare": (), "preserve": ()}
CASES["InitPCPacks"] = [
	{"wram": {wPCPacks: bytes(15), wPCPackSelection: b"\x05"},
	 "read": {wPCPacks: 15}},
	dict(POISON, wram={wPCPacks: bytes([0xff] * 15), wPCPackSelection: b"\x0e"},
	     read={wPCPacks: 15}),
]
# <<< factory InitPCPacks

# >>> factory DrawMailMenuCursor

CONTRACT["DrawMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["DrawMailMenuCursor"] = [
	{"a": 0x3f, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"a": 1, "wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, a=2, wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory DrawMailMenuCursor

# >>> factory GetPCPackCoordinates

CONTRACT["GetPCPackCoordinates"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetPCPackCoordinates"] = [
	{"a": 0, "wram": {wPCPackSelection: b"\x00"}},
	{"a": 14, "wram": {wPCPackSelection: b"\x00"}},
	dict(POISON, a=7, wram={wPCPackSelection: b"\x03"}),
]
# <<< factory GetPCPackCoordinates

# >>> factory ShowMailMenuCursor
CONTRACT["ShowMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["ShowMailMenuCursor"] = [
	{"wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory ShowMailMenuCursor

# >>> factory HideMailMenuCursor
CONTRACT["HideMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["HideMailMenuCursor"] = [
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, setup=[{"fn": "ShowMailMenuCursor"}], wram={wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory HideMailMenuCursor

# >>> factory PrintEmptyPCPackName
CONTRACT["PrintEmptyPCPackName"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PrintEmptyPCPackName"] = [
	{"setup": [{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 2, "c": 2}],
	 "a": 0, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x9842: 1}}},
	{"setup": [{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 14, "c": 10}],
	 "a": 14, "wram": {wPCPackSelection: b"\x00"}, "vread": {0: {0x994e: 1}}},
	dict(POISON, setup=[{"fn": "WriteByteToBGMap0", "a": 0x0F, "b": 8, "c": 6}],
	     a=7, wram={wPCPackSelection: b"\x03"}, vread={0: {0x98c8: 1}}),
]
# <<< factory PrintEmptyPCPackName

# >>> factory-cases-statics
wCursorBlinkTimer = 0xD11C

hDPadHeld = 0xFF8F
wPCLastDirectionPressed = 0xD12D

CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wPCPacks = 0xD11E
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# mail.asm:263 (TryOpenPCMailBoosterPack).
wAnotherBoosterPack = 0xD117
wSelectedPCPack = 0xD12E
MAIL_wLCDC = 0xCABB
MAIL_wTxRam2 = 0xCE3F
MAIL_wTxRam3 = 0xCE43

# wLCDC clear on entry keeps InitMenuScreen's screen off (it never calls
# EnableLCD), every WaitForVBlank behind the scrollable text a no-op, and the
# trailing DisableLCD on its early return, so no VBlank-mutated byte is ever
# involved. CopyDMAFunction is still installed because InitMenuScreen sets
# wVBlankOAMCopyToggle, and SetupText warms the glyph cache the text page walks.
MAIL_TEXT_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# B, cycled: PrintScrollableText_NoTextBoxLabel waits on edge-triggered
# hKeysPressed, and with the LCD off runner.c still advances the input timeline
# every 70224 cycles, so a tapped button lands an edge inside the wait.
MAIL_TEXT_KEYS = [0x00, 0x02]
# A menu screen load plus a full page of letter-delayed scrollable text.
MAIL_TEXT_INSTRUCTIONS = 60000000
MAIL_TEXT_CYCLES = 240000000

# mail.asm:136 (PCMailHandleAInput).
hKeysPressed = 0xFF91
hBankROM = 0xFF80
# PlaySFX, one printed pack name and the cursor write together sit well above
# legacy_to_schema's 100000/400000 fallback defaults, so both budgets are
# declared explicitly; every case here stops before any text page or DoFrame.
MAIL_A_INSTRUCTIONS = 20000000
MAIL_A_CYCLES = 80000000
# <<< factory-cases-statics

# >>> factory UpdateMailMenuCursor
CONTRACT["UpdateMailMenuCursor"] = {"compare": (), "preserve": ()}
CASES["UpdateMailMenuCursor"] = [
	{"wram": {0xD11C: b"\x00", wPCPackSelection: b"\x00"}, "vread": {0: {0x9841: 1}, 1: {0x9841: 1}}},
	{"setup": [{"fn": "ShowMailMenuCursor"}], "wram": {0xD11C: b"\x10", wPCPackSelection: b"\x0e"}, "vread": {0: {0x994d: 1}, 1: {0x994d: 1}}},
	dict(POISON, wram={0xD11C: b"\x0f", wPCPackSelection: b"\x07"}, vread={0: {0x98c7: 1}, 1: {0x98c7: 1}}),
]
# <<< factory UpdateMailMenuCursor

# >>> factory PCMailHandleDPadInput
CONTRACT["PCMailHandleDPadInput"] = {"compare": (), "preserve": ()}
CASES["PCMailHandleDPadInput"] = [
    {"hDPadHeld": 0, "wram": {hDPadHeld: b"\x00", wPCPackSelection: b"\x00", wCursorBlinkTimer: b"\xAA"}, "read": {wPCPackSelection: 1, wCursorBlinkTimer: 1}},
    {"hDPadHeld": 0x10, "wram": {hDPadHeld: b"\x10", wPCPackSelection: b"\x00", wPCPacks: bytes([1] * 15), wCursorBlinkTimer: b"\xAA"}, "read": {wPCLastDirectionPressed: 1, wPCPackSelection: 1, wCursorBlinkTimer: 1}, "vread": {0: {0x9841: 1, 0x9847: 1}, 1: {0x9841: 1, 0x9847: 1}}},
    dict(POISON, hDPadHeld=0x40, wram={hDPadHeld: b"\x40", wPCPackSelection: b"\x0E", wPCPacks: bytes([1] * 15), wCursorBlinkTimer: b"\xAA"}, read={wPCLastDirectionPressed: 0, wPCPackSelection: 11, wCursorBlinkTimer: 1}, vread={0: {0x994D: 1, 0x9901: 1}, 1: {0x994D: 1, 0x9901: 1}}),
]
# <<< factory PCMailHandleDPadInput

# >>> factory GetPCPackNameTextID
CONTRACT["GetPCPackNameTextID"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")}
CASES["GetPCPackNameTextID"] = [
    {"a": 0, "expect_regs": {"b": 0, "c": 0, "d": 0x03, "e": 0x5D, "hl": 0}},
    {"a": 0x0E, "expect_regs": {"b": 0, "c": 0, "d": 0x03, "e": 0x6B, "hl": 0}},
    dict(POISON, a=1, expect_regs={"b": 0xBB, "c": 0xCC, "d": 0x03, "e": 0x5E, "hl": 0x1234}),
]
# <<< factory GetPCPackNameTextID

# >>> factory PrintPCPackName
CONTRACT["PrintPCPackName"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PrintPCPackName"] = [
    {"a": 0, "wram": {0xFF80: b"\x04", 0xCABB: b"\x00"}, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": {0: {0x9842: 6}}},
    {"a": 14, "wram": {0xFF80: b"\x04", 0xCABB: b"\x00"}, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": {0: {0x994E: 6}}},
    dict(POISON, a=1, wram={0xFF80: b"\x04", 0xCABB: b"\x00"}, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ}, vread={0: {0x9848: 6}}),
]
# <<< factory PrintPCPackName

# >>> factory PrintObtainedPCPacks
CONTRACT["PrintObtainedPCPacks"] = {"compare": (), "preserve": ()}
CASES["PrintObtainedPCPacks"] = [
    {"wram": {wPCPacks: bytes(15)}},
    {"wram": {wPCPacks: b"\x01" + bytes(14), 0xFF80: b"\x04", 0xCABB: b"\x00"}, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": {0: {0x9842: 6}}},
    dict(POISON, wram={wPCPacks: bytes(14) + b"\x01", 0xFF80: b"\x04", 0xCABB: b"\x00"}, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ}, vread={0: {0x994E: 6}}),
]
# <<< factory PrintObtainedPCPacks

# >>> factory BlinkUnopenedPCPacks
CONTRACT["BlinkUnopenedPCPacks"] = {"compare": (), "preserve": ()}
CASES["BlinkUnopenedPCPacks"] = [
    {"wram": {wPCPacks: bytes(15), wCursorBlinkTimer: b"\x00"}},
    {"wram": {wPCPacks: b"\x80" + bytes(14), wCursorBlinkTimer: b"\x00", 0xFF80: b"\x04", 0xCABB: b"\x00"}, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": {0: {0x9842: 6}}},
    {"wram": {wPCPacks: bytes(14) + b"\x80", wCursorBlinkTimer: b"\x0c", 0xFF80: b"\x04", 0xCABB: b"\x00"}, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": {0: {0x994e: 1}}},
    {"wram": {wPCPacks: b"\x80" + bytes(14), wCursorBlinkTimer: b"\x04"}},
    dict(POISON, wram={wPCPacks: b"\x80" + bytes(14), wCursorBlinkTimer: b"\x00", 0xFF80: b"\x04", 0xCABB: b"\x00"}, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ}, vread={0: {0x9842: 6}}),
]
# <<< factory BlinkUnopenedPCPacks

# >>> factory TryOpenPCMailBoosterPack
CONTRACT["TryOpenPCMailBoosterPack"] = {"compare": (), "preserve": ()}
CASES["TryOpenPCMailBoosterPack"] = [
    # PACK_UNOPENED_F clear: the pack is already open, so the routine prints
    # MailBoosterPackAlreadyOpenedText and both sides return through DisableLCD.
    # wAnotherBoosterPack is seeded non-zero and must come back cleared.
    {"wram": {wSelectedPCPack: b"\x00", wAnotherBoosterPack: b"\xff", MAIL_wLCDC: b"\x00"},
     "keys": MAIL_TEXT_KEYS, "setup": MAIL_TEXT_SETUP,
     "read": {wAnotherBoosterPack: 1},
     "instruction_budget": MAIL_TEXT_INSTRUCTIONS, "cycle_budget": MAIL_TEXT_CYCLES},
    # A pack id that would select a real two-booster row if bit 7 were set, so
    # only the branch bit decides; wAnotherBoosterPack starts at the value the
    # opened path would have left.
    {"wram": {wSelectedPCPack: b"\x0a", wAnotherBoosterPack: b"\x01", MAIL_wLCDC: b"\x00"},
     "keys": MAIL_TEXT_KEYS, "setup": MAIL_TEXT_SETUP,
     "read": {wAnotherBoosterPack: 1},
     "instruction_budget": MAIL_TEXT_INSTRUCTIONS, "cycle_budget": MAIL_TEXT_CYCLES},
    # Poisoned entry registers: `xor a` kills a and f immediately and no other
    # register is an input. $7F is the largest id with the unopened bit clear.
    dict(POISON, wram={wSelectedPCPack: b"\x7f", wAnotherBoosterPack: b"\xff", MAIL_wLCDC: b"\x00"},
         keys=MAIL_TEXT_KEYS, setup=MAIL_TEXT_SETUP,
         read={wAnotherBoosterPack: 1},
         instruction_budget=MAIL_TEXT_INSTRUCTIONS, cycle_budget=MAIL_TEXT_CYCLES),
    # Unopened pack, native only. The reference never returns from
    # GiveBoosterPack -- it spins in WaitForSongToFinish, which is why that
    # routine itself landed with a pre-ret cutpoint at AssertSongFinished -- so
    # this branch cannot be measured end to end against the real ROM. Mail 10
    # ($8A) is the only row whose second id is non-zero, so the second call
    # re-writes the TxRam pair with BOOSTER_EVOLUTION_NEUTRAL's scene
    # (SCENE_EVOLUTION_BOOSTER $02) and EvolutionBoosterText ($03A9), which
    # proves both the row lookup and the `or a` continuation.
    {"oracle": False,
     "why": "The reference ROM cannot return from this branch: GiveBoosterPack spins in WaitForSongToFinish and is itself ported only up to a pre-ret cutpoint, so the unopened path is native-only evidence.",
     "wram": {wSelectedPCPack: b"\x8a", MAIL_wLCDC: b"\x00"},
     "expect": {wAnotherBoosterPack: b"\x01", MAIL_wTxRam2: b"\xa9\x03", MAIL_wTxRam3: b"\x02\x00"},
     "instruction_budget": MAIL_TEXT_INSTRUCTIONS, "cycle_budget": MAIL_TEXT_CYCLES},
]
# <<< factory TryOpenPCMailBoosterPack

# >>> factory PCMailHandleAInput
CONTRACT["PCMailHandleAInput"] = {"compare": (), "preserve": ()}
CASES["PCMailHandleAInput"] = [
    # All-zero entry: `ldh a, [hKeysPressed] / and PAD_A / ret z` leaves before
    # the SFX, so wSelectedPCPack keeps the byte it was seeded with.
    {"wram": {hKeysPressed: b"\x00", wPCPackSelection: b"\x00", wPCPacks: bytes(15),
              wSelectedPCPack: b"\xff"},
     "read": {wSelectedPCPack: 1, wPCPacks: 15}},
    # A pressed on an empty slot: PlaySFX, PrintObtainedPCPacks (nothing to
    # print) and ShowMailMenuCursor all run, then `ld [wSelectedPCPack], a /
    # and $7f / or a / ret z` exits with the zero pack byte stored.
    {"wram": {hKeysPressed: b"\x01", wPCPackSelection: b"\x00", wPCPacks: bytes(15),
              wSelectedPCPack: b"\xff"},
     "read": {wSelectedPCPack: 1, wPCPacks: 15},
     "vread": {0: {0x9841: 1}, 1: {0x9841: 1}},
     "instruction_budget": MAIL_A_INSTRUCTIONS, "cycle_budget": MAIL_A_CYCLES},
    # Unopened mail id 0 ($80): wSelectedPCPack keeps the whole flag byte, the
    # slot is written back masked to 0, and `or a / ret z` then exits, so the
    # text pages are never entered. The non-zero slot makes PrintObtainedPCPacks
    # print pack 0's name at $9842, with the cursor at $9841 on top of it, which
    # is why SetupText warms the glyph cache and wLCDC is cleared.
    {"wram": {hKeysPressed: b"\x01", wPCPackSelection: b"\x00",
              wPCPacks: b"\x80" + bytes(14), wSelectedPCPack: b"\x00",
              hBankROM: b"\x04", MAIL_wLCDC: b"\x00"},
     "setup": SETUP,
     "read": {wSelectedPCPack: 1, wPCPacks: 15, **CACHE_READ, **PLACEMENT_READ},
     "vread": {0: {0x9841: 7}},
     "instruction_budget": MAIL_A_INSTRUCTIONS, "cycle_budget": MAIL_A_CYCLES},
    # Poisoned entry registers on the last slot: the routine reads no register
    # input at all (hKeysPressed comes from HRAM), so every poisoned byte is
    # simply unused, and slot 14 is the index boundary of wPCPacks.
    dict(POISON,
         wram={hKeysPressed: b"\x01", wPCPackSelection: b"\x0e",
               wPCPacks: bytes(14) + b"\x80", wSelectedPCPack: b"\x00",
               hBankROM: b"\x04", MAIL_wLCDC: b"\x00"},
         setup=SETUP,
         read={wSelectedPCPack: 1, wPCPacks: 15, **CACHE_READ, **PLACEMENT_READ},
         vread={0: {0x994D: 7}},
         instruction_budget=MAIL_A_INSTRUCTIONS, cycle_budget=MAIL_A_CYCLES),
]
# <<< factory PCMailHandleAInput

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GePCPackSelectionCoordinates": {
        "source_symbol": "GePCPackSelectionCoordinates",
        "before": "pc_mail_coordinates[selection][0],",
        "after": "pc_mail_coordinates[selection][1],",
        "case_ids": ["GePCPackSelectionCoordinates-0", "GePCPackSelectionCoordinates-1", "GePCPackSelectionCoordinates-2"],
    },
    "TryGivePCPack": {
        "source_symbol": "TryGivePCPack",
        "before": "if ((uint8_t)(gb_read8(slot) & 0x7f) == 0)",
        "after": "if ((uint8_t)(gb_read8(slot) & 0x7f) != 0)",
        "case_ids": ["TryGivePCPack-0", "TryGivePCPack-1", "TryGivePCPack-3", "TryGivePCPack-4"],
    },
}
# >>> factory-mutation InitPCPacks

MUTATIONS["InitPCPacks"] = {
	"source_symbol": "InitPCPacks",
	"before": "TryGivePCPack(1u);",
	"after": "TryGivePCPack(0u);",
	"case_ids": ["InitPCPacks-0", "InitPCPacks-1"],
}
# <<< factory-mutation InitPCPacks
# >>> factory-mutation DrawMailMenuCursor

MUTATIONS["DrawMailMenuCursor"] = {
	"source_symbol": "DrawMailMenuCursor",
	"before": "WriteByteToBGMap0(symbol, coords.b, coords.c);",
	"after": "WriteByteToBGMap0(symbol, coords.c, coords.b);",
	"case_ids": ["DrawMailMenuCursor-0", "DrawMailMenuCursor-1", "DrawMailMenuCursor-2"],
}
# <<< factory-mutation DrawMailMenuCursor
# >>> factory-mutation GetPCPackCoordinates

MUTATIONS["GetPCPackCoordinates"] = {
	"source_symbol": "GetPCPackCoordinates",
	"before": "coords.b++;",
	"after": "coords.b--;",
	"case_ids": ["GetPCPackCoordinates-0", "GetPCPackCoordinates-1", "GetPCPackCoordinates-2"],
}
# <<< factory-mutation GetPCPackCoordinates
# >>> factory-mutation ShowMailMenuCursor
MUTATIONS["ShowMailMenuCursor"] = {
	"source_symbol": "ShowMailMenuCursor",
	"before": "void ShowMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_CURSOR_R);\n}",
	"after": "void ShowMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_SPACE);\n}",
	"case_ids": ["ShowMailMenuCursor-0", "ShowMailMenuCursor-1", "ShowMailMenuCursor-2"],
}
# <<< factory-mutation ShowMailMenuCursor
# >>> factory-mutation HideMailMenuCursor
MUTATIONS["HideMailMenuCursor"] = {
	"source_symbol": "HideMailMenuCursor",
	"before": "void HideMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_SPACE);\n}",
	"after": "void HideMailMenuCursor(void)\n{\n\tDrawMailMenuCursor(SYM_CURSOR_R);\n}",
	"case_ids": ["HideMailMenuCursor-0", "HideMailMenuCursor-1", "HideMailMenuCursor-2"],
}
# <<< factory-mutation HideMailMenuCursor
# >>> factory-mutation PrintEmptyPCPackName
MUTATIONS["PrintEmptyPCPackName"] = {
	"source_symbol": "PrintEmptyPCPackName",
	"before": "InitTextPrinting(coords.b, coords.c);",
	"after": "InitTextPrinting(coords.c, coords.b);",
	"case_ids": ["PrintEmptyPCPackName-1", "PrintEmptyPCPackName-2"],
}
# <<< factory-mutation PrintEmptyPCPackName
# >>> factory-mutation UpdateMailMenuCursor
MUTATIONS["UpdateMailMenuCursor"] = {
	"source_symbol": "UpdateMailMenuCursor",
	"before": "if ((wCursorBlinkTimer & 0x10u) == 0u)",
	"after": "if ((wCursorBlinkTimer & 0x10u) != 0u)",
	"case_ids": ["UpdateMailMenuCursor-1", "UpdateMailMenuCursor-0", "UpdateMailMenuCursor-2"],
}
# <<< factory-mutation UpdateMailMenuCursor
# >>> factory-mutation PCMailHandleDPadInput
MUTATIONS["PCMailHandleDPadInput"] = {"source_symbol": "PCMailHandleDPadInput", "before": "if ((gb_read8(hDPadHeld_ADDR) & PAD_CTRL_PAD) == 0u)", "after": "if ((gb_read8(hDPadHeld_ADDR) & 0x00u) == 0u)", "case_ids": ["PCMailHandleDPadInput-1", "PCMailHandleDPadInput-2"]}
# <<< factory-mutation PCMailHandleDPadInput
# >>> factory-mutation GetPCPackNameTextID
MUTATIONS["GetPCPackNameTextID"] = {"source_symbol": "GetPCPackNameTextID", "before": "uint16_t GetPCPackNameTextID(uint8_t a)\n{\n\treturn (uint16_t)(0x035Du + (uint16_t)a);\n}", "after": "uint16_t GetPCPackNameTextID(uint8_t a)\n{\n\treturn (uint16_t)(0x035Eu + (uint16_t)a);\n}", "case_ids": ["GetPCPackNameTextID-0", "GetPCPackNameTextID-1", "GetPCPackNameTextID-2"]}
# <<< factory-mutation GetPCPackNameTextID
# >>> factory-mutation PrintPCPackName
MUTATIONS["PrintPCPackName"] = {"source_symbol": "PrintPCPackName", "before": "PrintPCPackNameResult PrintPCPackName(uint8_t a)\n{\n\tuint16_t text_id = GetPCPackNameTextID(a);", "after": "PrintPCPackNameResult PrintPCPackName(uint8_t a)\n{\n\tuint16_t text_id = (uint16_t)(GetPCPackNameTextID(a) + 1u);", "case_ids": ["PrintPCPackName-0", "PrintPCPackName-1", "PrintPCPackName-2"]}
# <<< factory-mutation PrintPCPackName
# >>> factory-mutation PrintObtainedPCPacks
MUTATIONS["PrintObtainedPCPacks"] = {"source_symbol": "PrintObtainedPCPacks", "before": "\t\t\t(void)PrintPCPackName(index);", "after": "\t\t\t(void)PrintPCPackName(0u);", "case_ids": ["PrintObtainedPCPacks-2"]}
# <<< factory-mutation PrintObtainedPCPacks
# >>> factory-mutation BlinkUnopenedPCPacks
MUTATIONS["BlinkUnopenedPCPacks"] = {"source_symbol": "BlinkUnopenedPCPacks", "before": "\t\tif ((pack & (uint8_t)(1u << PACK_UNOPENED_F)) == 0u)", "after": "\t\tif ((pack & (uint8_t)(1u << PACK_UNOPENED_F)) != 0u)", "case_ids": ["BlinkUnopenedPCPacks-1", "BlinkUnopenedPCPacks-2", "BlinkUnopenedPCPacks-4"]}
# <<< factory-mutation BlinkUnopenedPCPacks
# >>> factory-mutation TryOpenPCMailBoosterPack
MUTATIONS["TryOpenPCMailBoosterPack"] = {
	"source_symbol": "TryOpenPCMailBoosterPack",
	"before": "\twAnotherBoosterPack = 0u;\n\tuint8_t pack = wSelectedPCPack;",
	"after": "\twAnotherBoosterPack = 1u;\n\tuint8_t pack = wSelectedPCPack;",
	"case_ids": ["TryOpenPCMailBoosterPack-0", "TryOpenPCMailBoosterPack-1", "TryOpenPCMailBoosterPack-2"],
}
# <<< factory-mutation TryOpenPCMailBoosterPack
# >>> factory-mutation PCMailHandleAInput
MUTATIONS["PCMailHandleAInput"] = {
	"source_symbol": "PCMailHandleAInput",
	"before": "\tuint8_t pack = gb_read8(slot);\n\twSelectedPCPack = pack;",
	"after": "\tuint8_t pack = gb_read8(slot);\n\twSelectedPCPack = 0u;",
	"case_ids": ["PCMailHandleAInput-2", "PCMailHandleAInput-3"],
}
# <<< factory-mutation PCMailHandleAInput
