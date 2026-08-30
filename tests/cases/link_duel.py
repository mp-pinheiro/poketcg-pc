"""Oracle-diff cases for poketcg/src/engine/link/link_duel.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wDuelResult = 0xD0C3
WRAM_LCD_SHADOW = 0xCABB
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory _SetUpAndStartLinkDuel
CONTRACT["_SetUpAndStartLinkDuel"] = {"compare": (), "preserve": ()}
CASES["_SetUpAndStartLinkDuel"] = [
    {"keys": [0x00, 0x02], "wram": {wDuelResult: b"\x00", WRAM_LCD_SHADOW: b"\x00"}, "setup": SETUP, "read": {wDuelResult: 1}, "expect": {wDuelResult: b"\xFF"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={wDuelResult: b"\xAB", WRAM_LCD_SHADOW: b"\x00"}, setup=SETUP, read={wDuelResult: 1}, expect={wDuelResult: b"\xFF"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _SetUpAndStartLinkDuel

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _SetUpAndStartLinkDuel
MUTATIONS["_SetUpAndStartLinkDuel"] = {"source_symbol": "_SetUpAndStartLinkDuel", "before": "wDuelResult = 0xFFu;", "after": "wDuelResult = 0x00u;", "case_ids": ["_SetUpAndStartLinkDuel-0", "_SetUpAndStartLinkDuel-1"]}
# <<< factory-mutation _SetUpAndStartLinkDuel
