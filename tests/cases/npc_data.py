"""Oracle-diff cases for poketcg/src/engine/overworld/npc_data.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetNPCHeaderPointer
CONTRACT["GetNPCHeaderPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetNPCHeaderPointer"] = [
    {"a": 0x00},
    {"a": 0x01},
    {"a": 0x7F},
    {"a": 0x80},
    dict(POISON),
]
# <<< factory GetNPCHeaderPointer

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetNPCHeaderPointer
MUTATIONS["GetNPCHeaderPointer"] = {"source_symbol": "GetNPCHeaderPointer", "before": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, table_address);", "after": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, (uint16_t)(table_address + 1u));", "case_ids": ["GetNPCHeaderPointer-0", "GetNPCHeaderPointer-1", "GetNPCHeaderPointer-2", "GetNPCHeaderPointer-3"]}
# <<< factory-mutation GetNPCHeaderPointer
