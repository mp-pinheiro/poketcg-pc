"""Oracle-diff cases for poketcg/src/engine/menus/deck_selection.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetPointerToDeckCards
CONTRACT["GetPointerToDeckCards"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["GetPointerToDeckCards"] = [
	{},
	{"wram": {0xCEB1: b"\x01"}},
	{"wram": {0xCEB1: b"\xFF"}},
	dict(POISON, wram={0xCEB1: b"\x02"}),
]
# <<< factory GetPointerToDeckCards

# >>> factory ResetCheckMenuCursorPositionAndBlink
CONTRACT["ResetCheckMenuCursorPositionAndBlink"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ResetCheckMenuCursorPositionAndBlink"] = [
	{"wram": {0xCEA3: b"\x00", 0xCEAF: b"\x00", 0xCEB0: b"\x00"}},
	dict(POISON, wram={0xCEA3: b"\x11", 0xCEAF: b"\x22", 0xCEB0: b"\x33"}),
]
# <<< factory ResetCheckMenuCursorPositionAndBlink

# >>> factory-cases-statics
wCurDeck = 0xCEB1
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory GetPointerToDeckName
CONTRACT["GetPointerToDeckName"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetPointerToDeckName"] = [
    {"wram": {wCurDeck: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "hl": 0xA200}},
    dict(POISON, wram={wCurDeck: b"\x01"}, expect_regs={"a": 0x00, "f": 0x80, "hl": 0xA254}),
]
# <<< factory GetPointerToDeckName

# >>> factory InitDeckBuildingParams
CONTRACT["InitDeckBuildingParams"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c",)}
CASES["InitDeckBuildingParams"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x50\x04\x01\x34\x12\x78\x56"}, "read": {0xC100: 7}},
    dict(POISON, hl=0xC100, wram={0xC100: b"\x01\x23\x45\x67\x89\xAB\xCD"}, read={0xC100: 7}),
    {"a": 0xFF, "f": 0x01, "c": 0x7E, "d": 0x11, "e": 0x22, "hl": 0xC1F8,
     "wram": {0xC1F8: b"\xFF\x00\x80\x7F\xAA\x55\x33"}, "read": {0xC1F8: 7}},
]
# <<< factory InitDeckBuildingParams

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
