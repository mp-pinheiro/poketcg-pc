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

wTempNPC = 0xD3AB

wDuelResult = 0xD0C3
wNPCDuelist = 0xD0C4
# <<< factory-cases-statics

# >>> factory TryFirstRonaldDuel
CONTRACT["TryFirstRonaldDuel"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["TryFirstRonaldDuel"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<', 0xD3E5: b"\x00"}},
    dict(POISON, wram={0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}),
    {"b": 0x56, "c": 0x78, "hl": 0x0000, "wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<', 0xD3E5: b"\x20"}},
]
# <<< factory TryFirstRonaldDuel

# >>> factory TrySecondRonaldDuel
CONTRACT["TrySecondRonaldDuel"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["TrySecondRonaldDuel"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}},
    dict(POISON, wram={0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}),
]
# <<< factory TrySecondRonaldDuel

# >>> factory LoadClubEntrance
CONTRACT["LoadClubEntrance"] = {"compare": (), "preserve": ()}
CASES["LoadClubEntrance"] = [
    {"wram": {0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}, "read": {wTempNPC: 1}},
    dict(POISON, wram={0xD34A: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x0723456789:;<'}, read={wTempNPC: 1}),
]
# <<< factory LoadClubEntrance

# >>> factory ClubEntranceAfterDuel
CONTRACT["ClubEntranceAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["ClubEntranceAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x71"}},
    {"wram": {wDuelResult: b"\x00", wNPCDuelist: b"\x72"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x71"}),
]
# <<< factory ClubEntranceAfterDuel

# >>> factory Func_e8a0
CONTRACT["Func_e8a0"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Func_e8a0"] = [
    {"a": 0x01, "read": {0xD3AC: 1, 0xD3AD: 1}},
    {"a": 0x02},
    dict(POISON, a=0x02),
]
# <<< factory Func_e8a0

# Event var byte $13 (wEventVars + $13 = $D3E5): bit 7 EVENT_RONALD_FIRST_CLUB_ENTRANCE_ENCOUNTER,
# bits 6-5 EVENT_RONALD_FIRST_DUEL_STATE, bits 4-3 EVENT_RONALD_SECOND_DUEL_STATE
# (scripting.asm:465-467). TryGiveMedalPCPacks recounts EVENT_MEDAL_COUNT from the
# medal flags in byte $00 ($D3D2), one bit per club master (scripting.asm:355-363).
# >>> factory Preload_Ronald1InClubEntrance
CONTRACT["Preload_Ronald1InClubEntrance"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Ronald1InClubEntrance"] = [
    {"wram": {0xD3E5: b"\x00"}},
    {"wram": {0xD3E5: b"\x80"}},
    dict(POISON, wram={0xD3E5: b"\x7F"}),
]
# <<< factory Preload_Ronald1InClubEntrance

# >>> factory Preload_Ronald2InClubEntrance
CONTRACT["Preload_Ronald2InClubEntrance"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Ronald2InClubEntrance"] = [
    {"wram": {0xD3E5: b"\x00", 0xD3D2: b"\x00"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    {"wram": {0xD3E5: b"\x00", 0xD3D2: b"\xC0"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    {"wram": {0xD3E5: b"\x20"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    dict(POISON, wram={0xD3E5: b"\x40"}, read={0xD3AC: 1, 0xD3AD: 1}),
]
# <<< factory Preload_Ronald2InClubEntrance

# >>> factory Preload_Ronald3InClubEntrance
CONTRACT["Preload_Ronald3InClubEntrance"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Ronald3InClubEntrance"] = [
    {"wram": {0xD3E5: b"\x00", 0xD3D2: b"\x00"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    {"wram": {0xD3E5: b"\x00", 0xD3D2: b"\xF8"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    {"wram": {0xD3E5: b"\x08"}, "read": {0xD3AC: 1, 0xD3AD: 1}},
    dict(POISON, wram={0xD3E5: b"\x10"}, read={0xD3AC: 1, 0xD3AD: 1}),
]
# <<< factory Preload_Ronald3InClubEntrance

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation TryFirstRonaldEncounter
MUTATIONS["TryFirstRonaldEncounter"] = {"source_symbol": "TryFirstRonaldEncounter", "before": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldEncounter_ADDR, hl);", "after": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_FirstRonaldEncounter_ADDR + 1u), hl);", "case_ids": ["TryFirstRonaldEncounter-0"]}
# <<< factory-mutation TryFirstRonaldEncounter
# >>> factory-mutation TryFirstRonaldDuel
MUTATIONS["TryFirstRonaldDuel"] = {"source_symbol": "TryFirstRonaldDuel", "before": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldDuel_ADDR, hl);", "after": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_FirstRonaldDuel_ADDR + 1u), hl);", "case_ids": ["TryFirstRonaldDuel-0"]}
# <<< factory-mutation TryFirstRonaldDuel
# >>> factory-mutation TrySecondRonaldDuel
MUTATIONS["TrySecondRonaldDuel"] = {"source_symbol": "TrySecondRonaldDuel", "before": "return (TrySecondRonaldDuelResult){r.a, r.f, b, c, hl};", "after": "return (TrySecondRonaldDuelResult){0u, r.f, b, c, hl};", "case_ids": ["TrySecondRonaldDuel-0", "TrySecondRonaldDuel-1"]}
# <<< factory-mutation TrySecondRonaldDuel
# >>> factory-mutation LoadClubEntrance
MUTATIONS["LoadClubEntrance"] = {"source_symbol": "LoadClubEntrance", "before": "TryFirstRonaldEncounterResult r3 = TryFirstRonaldEncounter(r2.b, r2.c, r2.hl);", "after": "TryFirstRonaldEncounterResult r3 = {0};", "case_ids": ["LoadClubEntrance-0", "LoadClubEntrance-1"]}
# <<< factory-mutation LoadClubEntrance
# >>> factory-mutation ClubEntranceAfterDuel
MUTATIONS["ClubEntranceAfterDuel"] = {"source_symbol": "ClubEntranceAfterDuel", "before": "FindEndOfDuelScriptResult r = FindEndOfDuelScript(ClubEntranceAfterDuelTable);", "after": "FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(ClubEntranceAfterDuelTable + 1u));", "case_ids": ["ClubEntranceAfterDuel-0", "ClubEntranceAfterDuel-1"]}
# <<< factory-mutation ClubEntranceAfterDuel
# >>> factory-mutation Func_e8a0
MUTATIONS["Func_e8a0"] = {"source_symbol": "Func_e8a0", "before": "\t\twLoadNPCXPos = 0x08u;", "after": "\t\twLoadNPCXPos = 0x09u;", "case_ids": ["Func_e8a0-0"]}
# <<< factory-mutation Func_e8a0
# >>> factory-mutation Preload_Ronald1InClubEntrance
MUTATIONS["Preload_Ronald1InClubEntrance"] = {"source_symbol": "Preload_Ronald1InClubEntrance", "before": "\tif (a < TRUE)\n\t\tf |= 0x10u;", "after": "\tif (a <= TRUE)\n\t\tf |= 0x10u;", "case_ids": ["Preload_Ronald1InClubEntrance-1"]}
# <<< factory-mutation Preload_Ronald1InClubEntrance
# >>> factory-mutation Preload_Ronald2InClubEntrance
MUTATIONS["Preload_Ronald2InClubEntrance"] = {"source_symbol": "Preload_Ronald2InClubEntrance", "before": "GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE), b, c, d, 2u, hl);", "after": "GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE), b, c, d, 3u, hl);", "case_ids": ["Preload_Ronald2InClubEntrance-1"]}
# <<< factory-mutation Preload_Ronald2InClubEntrance
# >>> factory-mutation Preload_Ronald3InClubEntrance
MUTATIONS["Preload_Ronald3InClubEntrance"] = {"source_symbol": "Preload_Ronald3InClubEntrance", "before": "GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE), b, c, d, 5u, hl);", "after": "GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE), b, c, d, 4u, hl);", "case_ids": ["Preload_Ronald3InClubEntrance-1"]}
# <<< factory-mutation Preload_Ronald3InClubEntrance
