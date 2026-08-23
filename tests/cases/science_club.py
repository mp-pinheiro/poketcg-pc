"""Oracle-diff cases for poketcg/src/scripts/science_club.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_Joseph
CONTRACT["Preload_Joseph"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Joseph"] = [
    {"wram": {0xD3D7: b"\x00"}},
    dict(POISON, wram={0xD3D7: b"\x80", 0xD3AC: b"\x05"}, read={0xD3AC: 1, 0xD3AE: 1}),
    {"wram": {0xD3D7: b"\x80", 0xD3AC: b"\xFE"}, "read": {0xD3AC: 1, 0xD3AE: 1}},
]
# <<< factory Preload_Joseph

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Preload_Joseph
MUTATIONS["Preload_Joseph"] = {"source_symbol": "Preload_Joseph", "before": "\t\tuint8_t new_x = (uint8_t)(x + 2u);", "after": "\t\tuint8_t new_x = (uint8_t)(x + 3u);", "case_ids": ["Preload_Joseph-1", "Preload_Joseph-2"]}
# <<< factory-mutation Preload_Joseph
