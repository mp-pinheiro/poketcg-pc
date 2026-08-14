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
