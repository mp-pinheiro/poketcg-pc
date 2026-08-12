"""Oracle-diff cases for poketcg/src/scripts/mason_laboratory.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wEventVars = 0xD3D2
wLoadNPCXPos = 0xD3AC
wLoadNPCYPos = 0xD3AD
EVENT_MASON_LAB_STATE_BYTE = wEventVars + 0x0D

def npc_pos(state_byte, x=0x55, y=0x66):
    return {EVENT_MASON_LAB_STATE_BYTE: bytes((state_byte,)),
            wLoadNPCXPos: bytes((x,)), wLoadNPCYPos: bytes((y,))}

NPC_POS_READ = {EVENT_MASON_LAB_STATE_BYTE: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1}
# <<< factory-cases-statics

# >>> factory Preload_DrMason
CONTRACT["Preload_DrMason"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["Preload_DrMason"] = [
    {"wram": npc_pos(0x00), "read": NPC_POS_READ},
    dict(POISON, wram=npc_pos(0xFF), read=NPC_POS_READ),
    {"wram": npc_pos(0x02), "read": NPC_POS_READ},
    dict(POISON, wram=npc_pos(0xF2), read=NPC_POS_READ),
    {"wram": npc_pos(0x04), "read": NPC_POS_READ},
]
# <<< factory Preload_DrMason

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Preload_DrMason
MUTATIONS["Preload_DrMason"] = {
    "source_symbol": "Preload_DrMason",
    "before": "if (state == MASON_LAB_IN_PRACTICE_DUEL) {",
    "after": "if (state != MASON_LAB_IN_PRACTICE_DUEL) {",
    "case_ids": ["Preload_DrMason-0", "Preload_DrMason-1", "Preload_DrMason-2",
                 "Preload_DrMason-3", "Preload_DrMason-4"],
}
# <<< factory-mutation Preload_DrMason
