"""Oracle-diff cases for poketcg/src/scripts/psychic_club_entrance.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory TryFirstRonaldEncounter
CONTRACT["TryFirstRonaldEncounter"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["TryFirstRonaldEncounter"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD34A: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0xD3AA: b'\xEE'}},
    dict(POISON, wram={0xD34A: b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0xD3AA: b'\xEE'}),
]
# <<< factory TryFirstRonaldEncounter

# >>> factory-cases-statics
def _npc_table(ids):
    entries = bytearray()
    for i, npc_id in enumerate(ids):
        entries += bytes([npc_id & 0xFF]) + bytes((i * 7 + k) & 0xFF for k in range(1, 12))
    return bytes(entries)
# <<< factory-cases-statics

# >>> factory TryFirstRonaldDuel
CONTRACT["TryFirstRonaldDuel"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["TryFirstRonaldDuel"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<', 0xD3E5: b"\x00"}},
    dict(POISON, wram={0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}),
    {"b": 0x56, "c": 0x78, "hl": 0x0000, "wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<', 0xD3E5: b"\x20"}},
]
# <<< factory TryFirstRonaldDuel

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation TryFirstRonaldEncounter
MUTATIONS["TryFirstRonaldEncounter"] = {"source_symbol": "TryFirstRonaldEncounter", "before": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldEncounter_ADDR, hl);", "after": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_FirstRonaldEncounter_ADDR + 1u), hl);", "case_ids": ["TryFirstRonaldEncounter-0"]}
# <<< factory-mutation TryFirstRonaldEncounter
# >>> factory-mutation TryFirstRonaldDuel
MUTATIONS["TryFirstRonaldDuel"] = {"source_symbol": "TryFirstRonaldDuel", "before": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldDuel_ADDR, hl);", "after": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_FirstRonaldDuel_ADDR + 1u), hl);", "case_ids": ["TryFirstRonaldDuel-0"]}
# <<< factory-mutation TryFirstRonaldDuel
