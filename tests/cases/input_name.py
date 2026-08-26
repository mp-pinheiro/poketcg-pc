"""Oracle-diff cases for poketcg/src/engine/input_name.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DeckNamingScreen_GetCharInfoFromPos
CONTRACT["DeckNamingScreen_GetCharInfoFromPos"] = {"compare": ("hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["DeckNamingScreen_GetCharInfoFromPos"] = [
	{},
	{"hl": 0x0001, "wram": {0xCEA9: b"\x05"}},
	{"hl": 0x0100, "wram": {0xCEA9: b"\x06"}},
	{"hl": 0x0105, "wram": {0xCEA9: b"\x05"}},
	{"hl": 0x2A03, "wram": {0xCEA9: b"\x06"}},
	{"hl": 0x3400, "wram": {0xCEA9: b"\x05"}},
	{"hl": 0x34FC, "wram": {0xCEA9: b"\x05"}},
	dict(POISON, hl=0x0203, wram={0xCEA9: b"\x06"}),
]
# <<< factory DeckNamingScreen_GetCharInfoFromPos

# >>> factory ClearMemory_Bank6
CONTRACT["ClearMemory_Bank6"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank6"] = [
    {},  # all-zero entry: a=0 acts as 256 writes at $0000-$00ff (bus drops them)
    {"a": 0, "hl": 0xC100, "wram": {0xC100: b"\xff" * 0x100}},  # count 0 = maximum (256)
    {"a": 1, "hl": 0xC100, "wram": {0xC100: b"\xff" * 0x04}},   # count 1
    {"a": 2, "hl": 0xC100, "wram": {0xC100: b"\xaa" * 0x08}},
    {"a": 0x0C, "hl": 0xC500, "wram": {0xC500: b"\xff" * 0x10}},  # wNameBuffer, MAX_PLAYER_NAME_LENGTH bytes
    dict(POISON, a=5, hl=0xC400, wram={0xC400: b"\x99" * 0x10}),
]
# <<< factory ClearMemory_Bank6

# >>> factory DrawTextboxForKeyboard
CONTRACT["DrawTextboxForKeyboard"] = {"compare": ("hl",), "preserve": ()}
CASES["DrawTextboxForKeyboard"] = [
    {"vread": {0: {0x9800: 0x200, 0x9C00: 0x200}}},  # all-zero entry: a=0, hl=0, text read from ROM $0000
    {"a": 0, "hl": 0xC100, "wram": {0xC100: b"\x50\x00"}, "vread": {0: {0x9800: 0x200, 0x9C00: 0x200}}},
    {"a": 1, "hl": 0xC100, "wram": {0xC100: b"\x41\x42\x43\x50\x00"}, "vread": {0: {0x9800: 0x200, 0x9C00: 0x200}}},
    dict(POISON, a=0, hl=0xC100, wram={0xC100: b"\x00"}, vread={0: {0x9800: 0x200, 0x9C00: 0x200}}),
]
# <<< factory DrawTextboxForKeyboard

# >>> factory TransformCharacter
CONTRACT["TransformCharacter"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["TransformCharacter"] = [
	# wNamingScreenBuffer ($CFE7) and wNamingScreenBufferLength ($CFFF) fall inside the
	# reserved oracle call frame ($CF00-$CFFF) and must not be seeded: the ROM and the C
	# port read the same frame bytes through the bus, so these cases diff faithfully
	# whichever path the frame's length byte selects. Only the hl table (scratch WRAM)
	# is case-controlled; the walk is terminator-driven, so there are no counted-loop
	# boundaries to cover (the len-1 offset wraparound is covered by the C's 8-bit
	# cast, exercised whenever the frame length is 1).
	{"hl": 0xC100},  # all-zero: zero table -> immediate terminator
	{"hl": 0xC100, "wram": {0xC100: bytes([0x41, 0x0E, 0x12, 0x34, 0x00])}},  # match on first entry
	{"hl": 0xC100, "wram": {0xC100: bytes([0x99, 0x88, 0x77, 0x66, 0x05, 0x07, 0xAA, 0xBB, 0x00, 0x00, 0x00, 0x00])}},  # skip one entry, match on second
	{"hl": 0xC100, "wram": {0xC100: bytes([0x05, 0x11, 0x00, 0x00, 0x00])}},  # index matches, set does not -> skip, then terminator
	{"hl": 0xC104, "wram": {0xC100: bytes([0xFF, 0xEE, 0xDD, 0xCC, 0x00, 0x00])}},  # walk starts mid-table, terminator first
	{"hl": 0xC100, "wram": {0xC100: bytes([0x41, 0x00, 0x12, 0x34, 0x00])}},  # matched set byte 0 -> success with Z set
	dict(POISON, hl=0xC100, wram={0xC100: bytes([0x41, 0x0E, 0x12, 0x34, 0x00])}),
]
# <<< factory TransformCharacter

# >>> factory PlayerNamingScreen_GetCharInfoFromPos
CONTRACT["PlayerNamingScreen_GetCharInfoFromPos"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["PlayerNamingScreen_GetCharInfoFromPos"] = [
    {"wram": {0xCEA9: b"\x00"}},
    {"hl": 0x0100, "wram": {0xCEA9: b"\x01"}},
    {"hl": 0x0101, "wram": {0xCEA9: b"\x06"}},
    dict(POISON, hl=0x0203, wram={0xCEA9: b"\x05"}),
    {"hl": 0xFF00, "wram": {0xCEA9: b"\x06"}},
    {"hl": 0xFFFF, "wram": {0xCEA9: b"\x06"}},
]
# <<< factory PlayerNamingScreen_GetCharInfoFromPos

# >>> factory PlaySFXConfirmOrCancel_Bank6
CONTRACT["PlaySFXConfirmOrCancel_Bank6"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")};
CASES["PlaySFXConfirmOrCancel_Bank6"] = [
    {"a": 0, "read": {0xDD82: 1, 0xDD83: 1}},
    dict(POISON, a=0xFF, read={0xDD82: 1, 0xDD83: 1}),
    {"a": 1, "read": {0xDD82: 1, 0xDD83: 1}},
]
# <<< factory PlaySFXConfirmOrCancel_Bank6

# >>> factory PlayerNamingScreen_AdjustCursorPosition
CONTRACT["PlayerNamingScreen_AdjustCursorPosition"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["PlayerNamingScreen_AdjustCursorPosition"] = [
    {"a": 0, "wram": {0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\x00", 0xD004: b"\x02", 0xD007: b"\x00"}, "expect_wram": {0xCA00: b"\x00\x00\x00\x00", 0xCAB5: b"\x00"}},
    {"a": 1, "wram": {0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\xFF", 0xD004: b"\x02", 0xD007: b"\x00"}, "expect_wram": {0xCA00: b"\x08\x18\x00\x00", 0xCAB5: b"\x04"}},
    dict(POISON, wram={0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\xFF", 0xD004: b"\x02", 0xD007: b"\x00"}, expect_wram={0xCA00: b"\x08\x18\x00\x00", 0xCAB5: b"\x04"}),
]
# <<< factory PlayerNamingScreen_AdjustCursorPosition

# >>> factory DeckNamingScreen_AdjustCursorPosition
CONTRACT["DeckNamingScreen_AdjustCursorPosition"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DeckNamingScreen_AdjustCursorPosition"] = [
    {"a": 0, "wram": {0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\x00", 0xD004: b"\x02", 0xD007: b"\x02"}, "expect_wram": {0xCA00: b"\x00\x00\x00\x00", 0xCAB5: b"\x00"}},
    {"a": 1, "wram": {0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\xFF", 0xD004: b"\x02", 0xD007: b"\x02"}, "expect_wram": {0xCA00: b"\x18\x10\x00\x00", 0xCAB5: b"\x04"}},
    dict(POISON, wram={0xCA00: b"\xAA\xBB\xCC\xDD", 0xCAB5: b"\x00", 0xCEAB: b"\xFF", 0xD004: b"\x02", 0xD007: b"\x02"}, expect_wram={0xCA00: b"\x18\x10\x00\x00", 0xCAB5: b"\x04"}),
]
# <<< factory DeckNamingScreen_AdjustCursorPosition

# >>> factory PlayerNamingScreen_DrawCursor
CONTRACT["PlayerNamingScreen_DrawCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["PlayerNamingScreen_DrawCursor"] = [
    {"a": 0x17, "wram": {0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"},
     "expect_regs": {"a": 0x17, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0x00, "e": 0x17, "hl": 0x6BB0}},
    {"a": 0x23, "wram": {0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"},
     "expect_regs": {"a": 0x23, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0x00, "e": 0x23, "hl": 0x6BB0}},
    dict(POISON, a=0x17,
         wram={0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"},
         expect_regs={"a": 0x17, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0xDD, "e": 0x17, "hl": 0x6BB0}),
]
# <<< factory PlayerNamingScreen_DrawCursor

# >>> factory DeckNamingScreen_DrawCursor
CONTRACT["DeckNamingScreen_DrawCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["DeckNamingScreen_DrawCursor"] = [
    {"a": 0x11, "d": 0x22, "wram": {0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x05"},
     "expect_regs": {"a": 0x11, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0x22, "e": 0x11}},
    {"a": 0x37, "d": 0x44, "wram": {0xD006: b"\x01", 0xCEA4: b"\x00", 0xCEA9: b"\x05"},
     "expect_regs": {"a": 0x37, "f": 0x00, "b": 0x01, "c": 0x0E, "d": 0x44, "e": 0x37}},
    dict(POISON, a=0x11,
         wram={0xD006: b"\x00", 0xCEA4: b"\x01", 0xCEA9: b"\x05"},
         expect_regs={"a": 0x11, "f": 0x00, "b": 0x01, "c": 0x06, "d": 0xDD, "e": 0x11}),
]
# <<< factory DeckNamingScreen_DrawCursor

# >>> factory DeckNamingScreen_DrawInvisibleCursor
CONTRACT["DeckNamingScreen_DrawInvisibleCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["DeckNamingScreen_DrawInvisibleCursor"] = [
    {"d": 0x22, "wram": {0xCEAB: b"\x11", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x05"},
     "expect_regs": {"a": 0x11, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0x22, "e": 0x11}},
    dict(POISON, wram={0xCEAB: b"\x37\x44"[:1], 0xD006: b"\x01", 0xCEA4: b"\x00", 0xCEA9: b"\x05"}),
]
# <<< factory DeckNamingScreen_DrawInvisibleCursor

# >>> factory DeckNamingScreen_DrawVisibleCursor
CONTRACT["DeckNamingScreen_DrawVisibleCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["DeckNamingScreen_DrawVisibleCursor"] = [
    {"d": 0x22, "wram": {0xCEAA: b"\x11", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x05"},
     "expect_regs": {"a": 0x11, "f": 0x00, "b": 0x01, "c": 0x04, "d": 0x22, "e": 0x11}},
    dict(POISON, wram={0xCEAA: b"\x37", 0xD006: b"\x01", 0xCEA4: b"\x00", 0xCEA9: b"\x05"}),
]
# <<< factory DeckNamingScreen_DrawVisibleCursor

# >>> factory PlayerNamingScreen_DrawInvisibleCursor
CONTRACT["PlayerNamingScreen_DrawInvisibleCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["PlayerNamingScreen_DrawInvisibleCursor"] = [
    {"wram": {0xCEAB: b"\x17", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"},
     "expect_regs": {"a": 0x17, "f": 0x00, "b": 0x01, "c": 0x04, "e": 0x17, "hl": 0x6BB0}},
    dict(POISON, wram={0xCEAB: b"\x23", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"}),
]
# <<< factory PlayerNamingScreen_DrawInvisibleCursor

# >>> factory PlayerNamingScreen_DrawVisibleCursor
CONTRACT["PlayerNamingScreen_DrawVisibleCursor"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d",)}
CASES["PlayerNamingScreen_DrawVisibleCursor"] = [
    {"wram": {0xCEAA: b"\x17", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"},
     "expect_regs": {"a": 0x17, "f": 0x00, "b": 0x01, "c": 0x04, "e": 0x17, "hl": 0x6BB0}},
    dict(POISON, wram={0xCEAA: b"\x23", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"}),
]
# <<< factory PlayerNamingScreen_DrawVisibleCursor

# >>> factory PlayerNamingScreen_CheckButtonState
CONTRACT["PlayerNamingScreen_CheckButtonState"] = {"compare": ("a",), "preserve": ()}
CASES["PlayerNamingScreen_CheckButtonState"] = [
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x00", 0xCEA3: b"\x00",
              0xCEAA: b"\x17", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"}},
    dict(POISON, wram={0xFF8F: b"\x00", 0xFF91: b"\x00", 0xCEA3: b"\x00",
                       0xCEAA: b"\x17", 0xD006: b"\x00", 0xCEA4: b"\x00", 0xCEA9: b"\x00"}),
]
# <<< factory PlayerNamingScreen_CheckButtonState

# >>> factory PrintPlayerNameFromInput
CONTRACT["PrintPlayerNameFromInput"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintPlayerNameFromInput"] = [
    {"wram": {0xD007: b"\x00\x00", 0xD004: b"\x14"}, "rom_bank": 6,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "vread": {0: {0x9800: 11}}},
    dict(POISON, wram={0xD007: b"\x00\x00", 0xD004: b"\x14"}, rom_bank=6,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         vread={0: {0x9800: 11}}),
]
# <<< factory PrintPlayerNameFromInput

# >>> factory DrawPlayerNamingScreenBG
CONTRACT["DrawPlayerNamingScreenBG"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawPlayerNamingScreenBG"] = [
    {"wram": {0xD002: b"\x00\x00", 0xD007: b"\x00\x00", 0xD004: b"\x14"}, "rom_bank": 6,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "vread": {0: {0x9882: 32}}},
    dict(POISON, wram={0xD002: b"\x00\x00", 0xD007: b"\x00\x00", 0xD004: b"\x14"}, rom_bank=6,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         vread={0: {0x9882: 32}}),
]
# <<< factory DrawPlayerNamingScreenBG

# >>> factory PlayerNamingScreen_ProcessInput
CONTRACT["PlayerNamingScreen_ProcessInput"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PlayerNamingScreen_ProcessInput"] = [
    {"wram": {0xD006: b"\x00", 0xCEA4: b"\x05", 0xCEA9: b"\x06", 0xD009: b"\x00"}, "rom_bank": 6},
    dict(POISON, wram={0xD006: b"\x00", 0xCEA4: b"\x05", 0xCEA9: b"\x06", 0xD009: b"\x00"}, rom_bank=6),
]
# <<< factory PlayerNamingScreen_ProcessInput

# >>> factory LoadTextCursorTile
CONTRACT["LoadTextCursorTile"] = {"compare": (), "preserve": ()}
CASES["LoadTextCursorTile"] = [
    {"vread": {0: {0x8000: 16}}},
    dict(POISON, vread={0: {0x8000: 16}}),
]
# <<< factory LoadTextCursorTile

# >>> factory LoadHalfWidthTextCursorTile
CONTRACT["LoadHalfWidthTextCursorTile"] = {"compare": ("b", "c"), "preserve": ("c",)}
CASES["LoadHalfWidthTextCursorTile"] = [
    {"vread": {0: {0x8000: 16}}},
    dict(POISON, vread={0: {0x8000: 16}}),
]
# <<< factory LoadHalfWidthTextCursorTile

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DeckNamingScreen_GetCharInfoFromPos
MUTATIONS["DeckNamingScreen_GetCharInfoFromPos"] = {
	"source_symbol": "DeckNamingScreen_GetCharInfoFromPos",
	"before": "addr = (uint16_t)(addr + 3u);",
	"after": "addr = (uint16_t)(addr + 2u);",
	"case_ids": ["DeckNamingScreen_GetCharInfoFromPos-1", "DeckNamingScreen_GetCharInfoFromPos-2", "DeckNamingScreen_GetCharInfoFromPos-3", "DeckNamingScreen_GetCharInfoFromPos-4", "DeckNamingScreen_GetCharInfoFromPos-5", "DeckNamingScreen_GetCharInfoFromPos-7"],
}
# <<< factory-mutation DeckNamingScreen_GetCharInfoFromPos
# >>> factory-mutation ClearMemory_Bank6
MUTATIONS["ClearMemory_Bank6"] = {
    "source_symbol": "ClearMemory_Bank6",
    "before": "\tuint32_t n = a ? a : 0x100u;",
    "after": "\tuint32_t n = a ? a : 0xFFu;",
    "case_ids": ["ClearMemory_Bank6-1"],
}
# <<< factory-mutation ClearMemory_Bank6
# >>> factory-mutation DrawTextboxForKeyboard
MUTATIONS["DrawTextboxForKeyboard"] = {
    "source_symbol": "DrawTextboxForKeyboard",
    "before": "\tDrawRegularTextBox(hl, a, 20u, 15u, 0u, 3u);",
    "after": "\tDrawRegularTextBox(hl, a, 19u, 15u, 0u, 3u);",
    "case_ids": ["DrawTextboxForKeyboard-0", "DrawTextboxForKeyboard-1", "DrawTextboxForKeyboard-2", "DrawTextboxForKeyboard-3"],
}
# <<< factory-mutation DrawTextboxForKeyboard
# >>> factory-mutation TransformCharacter
MUTATIONS["TransformCharacter"] = {
	"source_symbol": "TransformCharacter",
	"before": "\tuint8_t len = wNamingScreenBufferLength;\n\tif (len == 0u)",
	"after": "\tuint8_t len = wNamingScreenBufferLength;\n\tif (len != 0u)",
	"case_ids": ["TransformCharacter-0", "TransformCharacter-1", "TransformCharacter-2", "TransformCharacter-3", "TransformCharacter-4", "TransformCharacter-5", "TransformCharacter-6"],
}
# <<< factory-mutation TransformCharacter
# >>> factory-mutation PlayerNamingScreen_GetCharInfoFromPos
MUTATIONS["PlayerNamingScreen_GetCharInfoFromPos"] = {"source_symbol": "PlayerNamingScreen_GetCharInfoFromPos", "before": "\tuint8_t index = (uint8_t)(product + (uint8_t)hl);", "after": "\tuint8_t index = (uint8_t)(product + (uint8_t)hl + 1u);", "case_ids": ["PlayerNamingScreen_GetCharInfoFromPos-0", "PlayerNamingScreen_GetCharInfoFromPos-1", "PlayerNamingScreen_GetCharInfoFromPos-2", "PlayerNamingScreen_GetCharInfoFromPos-3", "PlayerNamingScreen_GetCharInfoFromPos-4", "PlayerNamingScreen_GetCharInfoFromPos-5"]}
# <<< factory-mutation PlayerNamingScreen_GetCharInfoFromPos
# >>> factory-mutation PlaySFXConfirmOrCancel_Bank6
MUTATIONS["PlaySFXConfirmOrCancel_Bank6"] = {
    "source_symbol": "PlaySFXConfirmOrCancel_Bank6",
    "before": "\tuint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;",
    "after": "\tuint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CONFIRM : SFX_CONFIRM;",
    "case_ids": ["PlaySFXConfirmOrCancel_Bank6-1"],
};
# <<< factory-mutation PlaySFXConfirmOrCancel_Bank6
# >>> factory-mutation PlayerNamingScreen_AdjustCursorPosition
MUTATIONS["PlayerNamingScreen_AdjustCursorPosition"] = {"source_symbol": "PlayerNamingScreen_AdjustCursorPosition", "before": "\tuint8_t half_max = (uint8_t)(max_length >> 1);", "after": "\tuint8_t half_max = (uint8_t)(max_length >> 2);", "case_ids": ["PlayerNamingScreen_AdjustCursorPosition-1", "PlayerNamingScreen_AdjustCursorPosition-2"]}
# <<< factory-mutation PlayerNamingScreen_AdjustCursorPosition
# >>> factory-mutation DeckNamingScreen_AdjustCursorPosition
MUTATIONS["DeckNamingScreen_AdjustCursorPosition"] = {"source_symbol": "DeckNamingScreen_AdjustCursorPosition", "before": "\td = (uint8_t)(d + (uint8_t)(name_position << 1));", "after": "\td = (uint8_t)d;", "case_ids": ["DeckNamingScreen_AdjustCursorPosition-1", "DeckNamingScreen_AdjustCursorPosition-2"]}
# <<< factory-mutation DeckNamingScreen_AdjustCursorPosition
# >>> factory-mutation PlayerNamingScreen_DrawCursor
MUTATIONS["PlayerNamingScreen_DrawCursor"] = {"source_symbol": "PlayerNamingScreen_DrawCursor", "before": "uint8_t tile = gb_read8(char_info++);", "after": "uint8_t tile = gb_read8((uint16_t)(char_info + 1u));", "case_ids": ["PlayerNamingScreen_DrawCursor-0"]}
# <<< factory-mutation PlayerNamingScreen_DrawCursor
# >>> factory-mutation DeckNamingScreen_DrawCursor
MUTATIONS["DeckNamingScreen_DrawCursor"] = {"source_symbol": "DeckNamingScreen_DrawCursor", "before": "uint16_t char_info = DeckNamingScreen_GetCharInfoFromPos((uint16_t)((uint16_t)gb_read8(wNamingScreenCursorX_ADDR) << 8 | gb_read8(wNamingScreenCursorY_ADDR)));", "after": "uint16_t char_info = DeckNamingScreen_GetCharInfoFromPos((uint16_t)((uint16_t)gb_read8(wNamingScreenCursorX_ADDR) << 8 | (uint16_t)(gb_read8(wNamingScreenCursorY_ADDR) + 1u)));", "case_ids": ["DeckNamingScreen_DrawCursor-0"]}
# <<< factory-mutation DeckNamingScreen_DrawCursor
# >>> factory-mutation DeckNamingScreen_DrawInvisibleCursor
MUTATIONS["DeckNamingScreen_DrawInvisibleCursor"] = {"source_symbol": "DeckNamingScreen_DrawInvisibleCursor", "before": "uint8_t a = gb_read8(wInvisibleCursorTile_ADDR);", "after": "uint8_t a = (uint8_t)(gb_read8(wInvisibleCursorTile_ADDR) + 1u);", "case_ids": ["DeckNamingScreen_DrawInvisibleCursor-0"]}
# <<< factory-mutation DeckNamingScreen_DrawInvisibleCursor
# >>> factory-mutation DeckNamingScreen_DrawVisibleCursor
MUTATIONS["DeckNamingScreen_DrawVisibleCursor"] = {"source_symbol": "DeckNamingScreen_DrawVisibleCursor", "before": "uint8_t a = gb_read8(wVisibleCursorTile_ADDR);", "after": "uint8_t a = (uint8_t)(gb_read8(wVisibleCursorTile_ADDR) + 1u);", "case_ids": ["DeckNamingScreen_DrawVisibleCursor-0"]}
# <<< factory-mutation DeckNamingScreen_DrawVisibleCursor
# >>> factory-mutation PlayerNamingScreen_DrawInvisibleCursor
MUTATIONS["PlayerNamingScreen_DrawInvisibleCursor"] = {"source_symbol": "PlayerNamingScreen_DrawInvisibleCursor", "before": "uint8_t a = gb_read8(wInvisibleCursorTile_ADDR);\n\treturn PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);", "after": "uint8_t a = (uint8_t)(gb_read8(wInvisibleCursorTile_ADDR) + 1u);\n\treturn PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);", "case_ids": ["PlayerNamingScreen_DrawInvisibleCursor-0"]}
# <<< factory-mutation PlayerNamingScreen_DrawInvisibleCursor
# >>> factory-mutation PlayerNamingScreen_DrawVisibleCursor
MUTATIONS["PlayerNamingScreen_DrawVisibleCursor"] = {"source_symbol": "PlayerNamingScreen_DrawVisibleCursor", "before": "uint8_t a = gb_read8(wVisibleCursorTile_ADDR);\n\treturn PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);", "after": "uint8_t a = (uint8_t)(gb_read8(wVisibleCursorTile_ADDR) + 1u);\n\treturn PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);", "case_ids": ["PlayerNamingScreen_DrawVisibleCursor-0"]}
# <<< factory-mutation PlayerNamingScreen_DrawVisibleCursor
# >>> factory-mutation PlayerNamingScreen_CheckButtonState
MUTATIONS["PlayerNamingScreen_CheckButtonState"] = {"source_symbol": "PlayerNamingScreen_CheckButtonState", "before": "uint8_t vis_tile = gb_read8(wVisibleCursorTile_ADDR);", "after": "uint8_t vis_tile = (uint8_t)(gb_read8(wVisibleCursorTile_ADDR) + 1u);", "case_ids": ["PlayerNamingScreen_CheckButtonState-0"]}
# <<< factory-mutation PlayerNamingScreen_CheckButtonState
# >>> factory-mutation PrintPlayerNameFromInput
MUTATIONS["PrintPlayerNameFromInput"] = {"source_symbol": "PrintPlayerNameFromInput", "before": "uint8_t offset = (uint8_t)(0x15u - max_len);", "after": "uint8_t offset = (uint8_t)(0x16u - max_len);", "case_ids": ["PrintPlayerNameFromInput-0", "PrintPlayerNameFromInput-1"]}
# <<< factory-mutation PrintPlayerNameFromInput
# >>> factory-mutation DrawPlayerNamingScreenBG
MUTATIONS["DrawPlayerNamingScreenBG"] = {"source_symbol": "DrawPlayerNamingScreenBG", "before": "InitTextPrinting(2u, 4u);", "after": "InitTextPrinting(3u, 4u);", "case_ids": ["DrawPlayerNamingScreenBG-0", "DrawPlayerNamingScreenBG-1"]}
# <<< factory-mutation DrawPlayerNamingScreenBG
# >>> factory-mutation PlayerNamingScreen_ProcessInput
MUTATIONS["PlayerNamingScreen_ProcessInput"] = {"source_symbol": "PlayerNamingScreen_ProcessInput", "before": "if (d == 0x09u) {", "after": "if (d == 0x0Au) {", "case_ids": ["PlayerNamingScreen_ProcessInput-0", "PlayerNamingScreen_ProcessInput-1"]}
# <<< factory-mutation PlayerNamingScreen_ProcessInput
# >>> factory-mutation LoadTextCursorTile
MUTATIONS["LoadTextCursorTile"] = {"source_symbol": "LoadTextCursorTile", "before": "for (uint8_t b = 0; b < TILE_SIZE; b++) {", "after": "for (uint8_t b = 0; b < (uint8_t)(TILE_SIZE - 1u); b++) {", "case_ids": ["LoadTextCursorTile-0", "LoadTextCursorTile-1"]}
# <<< factory-mutation LoadTextCursorTile
# >>> factory-mutation LoadHalfWidthTextCursorTile
MUTATIONS["LoadHalfWidthTextCursorTile"] = {
    "source_symbol": "LoadHalfWidthTextCursorTile",
    "before": "LoadHalfWidthTextCursorTileResult LoadHalfWidthTextCursorTile(uint8_t c)\n{\n\tuint16_t hl = V0TILES0_ADDR;",
    "after": "LoadHalfWidthTextCursorTileResult LoadHalfWidthTextCursorTile(uint8_t c)\n{\n\tuint16_t hl = (uint16_t)(V0TILES0_ADDR + 1u);",
    "case_ids": ["LoadHalfWidthTextCursorTile-0", "LoadHalfWidthTextCursorTile-1"],
}
# <<< factory-mutation LoadHalfWidthTextCursorTile
