"""Oracle-diff cases for poketcg/src/engine/duel/ai/trainer_cards.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory RemoveCardFromList
CONTRACT["RemoveCardFromList"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["RemoveCardFromList"] = [
    {"hl": 0xC101, "wram": {0xC100: b"\xaa\xff"}},
    {"hl": 0xC101, "wram": {0xC100: b"\xaa\x01\x02\xff\x55"}},
    dict(POISON, hl=0xC102, wram={0xC100: b"\x10\x11\x12\x13\xff"}),
]
# <<< factory RemoveCardFromList

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation RemoveCardFromList
MUTATIONS["RemoveCardFromList"] = {
    "source_symbol": "RemoveCardFromList",
    "before": "\t*hl = (uint16_t)(*hl - 1u);",
    "after": "\t*hl = (uint16_t)(*hl - 2u);",
    "case_ids": ["RemoveCardFromList-0", "RemoveCardFromList-1", "RemoveCardFromList-2"],
}
# <<< factory-mutation RemoveCardFromList
