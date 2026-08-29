"""Oracle-diff cases for poketcg/src/scripts/challenge_hall_entrance.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_Clerk9
CONTRACT["Preload_Clerk9"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e")}
CASES["Preload_Clerk9"] = [
    {"a": 0x00, "f": 0x00, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x4567, "expect_regs": {"a": 0x00, "f": 0x90, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x4567}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "expect_regs": {"a": 0x00, "f": 0x90, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}},
]
# <<< factory Preload_Clerk9

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Preload_Clerk9
MUTATIONS["Preload_Clerk9"] = {"source_symbol": "Preload_Clerk9", "before": "\tTryGiveMedalPCPacksResult given = TryGiveMedalPCPacks(b, c, d, e, hl);", "after": "\tTryGiveMedalPCPacksResult given = (TryGiveMedalPCPacksResult){0};", "case_ids": ["Preload_Clerk9-0", "Preload_Clerk9-1"]}
# <<< factory-mutation Preload_Clerk9
