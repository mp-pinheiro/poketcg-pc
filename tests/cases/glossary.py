"""Oracle-diff cases for poketcg/src/engine/menus/glossary.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory OpenGlossaryScreen
CONTRACT["OpenGlossaryScreen"] = {"compare": (), "preserve": ()}
CASES["OpenGlossaryScreen"] = [
    {"keys": [0x00, 0x02], "wram": {0xCE62: b"\x00", 0xCE52: b"\x00", 0xCE55: b"\xFF", 0xCEA3: b"\x00", 0xCAB6: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x02], "wram": {0xCE62: b"\x01", 0xCE52: b"\x00", 0xCE55: b"\xFF", 0xCEA3: b"\x00", 0xCAB6: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={0xCE62: b"\x00", 0xCE52: b"\x00", 0xCE55: b"\xFF", 0xCEA3: b"\x00", 0xCAB6: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenGlossaryScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation OpenGlossaryScreen
MUTATIONS["OpenGlossaryScreen"] = {"source_symbol": "OpenGlossaryScreen", "before": "if ((uint8_t)(item + 1u) == 0u)", "after": "if ((uint8_t)(item + 2u) == 0u)", "case_ids": ["OpenGlossaryScreen-0", "OpenGlossaryScreen-1"]}
# <<< factory-mutation OpenGlossaryScreen
