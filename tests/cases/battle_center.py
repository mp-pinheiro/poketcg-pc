"""Oracle-diff cases for poketcg/src/scripts/battle_center.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wDuelResult = 0xD0C3
wCurrentNPCNameTx = 0xD0C8
wNextScript = 0xD0C6
# <<< factory-cases-statics

# >>> factory Func_fc2b
CONTRACT["Func_fc2b"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_fc2b"] = [
    {"wram": {wDuelResult: b"\x00"}, "read": {wCurrentNPCNameTx: 2, wNextScript: 2}},
    dict(POISON, wram={wDuelResult: b"\x01"}, read={wCurrentNPCNameTx: 2, wNextScript: 2}),
    {"wram": {wDuelResult: b"\xFF"}, "read": {wCurrentNPCNameTx: 2, wNextScript: 2}},
]
# <<< factory Func_fc2b

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_fc2b
MUTATIONS["Func_fc2b"] = {"source_symbol": "Func_fc2b", "before": "bc = 0x7C64u;", "after": "bc = 0x7C60u;", "case_ids": ["Func_fc2b-0"]}
# <<< factory-mutation Func_fc2b
