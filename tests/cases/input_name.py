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
