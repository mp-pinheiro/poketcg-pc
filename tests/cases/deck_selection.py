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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetPointerToDeckCards
MUTATIONS["GetPointerToDeckCards"] = {"source_symbol": "GetPointerToDeckCards", "before": "#define DECK_CARD_STRIDE 0x54u", "after": "#define DECK_CARD_STRIDE 0x55u", "case_ids": ["GetPointerToDeckCards-1", "GetPointerToDeckCards-2", "GetPointerToDeckCards-3"]}
# <<< factory-mutation GetPointerToDeckCards
# >>> factory-mutation ResetCheckMenuCursorPositionAndBlink
MUTATIONS["ResetCheckMenuCursorPositionAndBlink"] = {"source_symbol": "ResetCheckMenuCursorPositionAndBlink", "before": "\twCheckMenuCursorYPosition = 0u;", "after": "\twCheckMenuCursorXPosition = 0u;", "case_ids": ["ResetCheckMenuCursorPositionAndBlink-1"]}
# <<< factory-mutation ResetCheckMenuCursorPositionAndBlink
