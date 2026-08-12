"""Oracle-diff cases for poketcg/src/engine/menus/card_album.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetFirstOwnedCardIndex
OWNED_LIST = 0xCF68
NOT_OWNED = 0x80

CONTRACT["GetFirstOwnedCardIndex"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("c", "d", "e")}
CASES["GetFirstOwnedCardIndex"] = [
    {},
    dict(POISON),
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 3, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 64, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 1, "a": NOT_OWNED},
               {"fn": "FillMemoryWithA", "hl": OWNED_LIST + 1, "b": 0, "c": 1, "a": 0x81}]},
]
# <<< factory GetFirstOwnedCardIndex

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetFirstOwnedCardIndex
MUTATIONS["GetFirstOwnedCardIndex"] = {
    "source_symbol": "GetFirstOwnedCardIndex",
    "before": "index++;",
    "after": "",
    "case_ids": ["GetFirstOwnedCardIndex-2", "GetFirstOwnedCardIndex-3", "GetFirstOwnedCardIndex-4"],
}
# <<< factory-mutation GetFirstOwnedCardIndex
