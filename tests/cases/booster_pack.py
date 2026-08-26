"""Oracle-diff cases for poketcg/src/engine/menus/booster_pack.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wBoosterCardsDrawn = 0xC400
wDuelTempList = 0xC510
wNoItemSelectionMenuKeys = 0xCBD6
wPlayerDuelVariables = 0xC200
# <<< factory-cases-statics

# >>> factory _OpenBoosterPack
CONTRACT["_OpenBoosterPack"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["_OpenBoosterPack"] = [
    {"wram": {0xC200: b"\xAA" * 0x3C, 0xC400: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x02], "read": {0xFF97: 1, 0xC200: 0x3C, 0xC510: 1, 0xCBD6: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xC200: b"\xAA" * 0x3C, 0xC400: b"\x00", 0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x02], read={0xFF97: 1, 0xC200: 0x3C, 0xC510: 1, 0xCBD6: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _OpenBoosterPack

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _OpenBoosterPack
MUTATIONS["_OpenBoosterPack"] = {"source_symbol": "_OpenBoosterPack", "before": "void _OpenBoosterPack(void)\n{\n\thWhoseTurn = PLAYER_TURN;", "after": "void _OpenBoosterPack(void)\n{\n\thWhoseTurn = (uint8_t)(PLAYER_TURN + 1u);", "case_ids": ["_OpenBoosterPack-0", "_OpenBoosterPack-1"]}
# <<< factory-mutation _OpenBoosterPack
