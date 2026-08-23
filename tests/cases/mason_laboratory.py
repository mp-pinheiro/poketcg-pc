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

wDuelResult = 0xD0C3
wNPCDuelist = 0xD0C4
wTempNPC = 0xD3AB
wLoadedNPCs = 0xD34A
wLoadedNPCTempIndex = 0xD3AA
wScriptNPC = 0xD3B6
wPlayerDirection = 0xD334
wOverworldNPCFlags = 0xD0C1
wNextScript = 0xD0C6
wOverworldMode = 0xD0BF

wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wCurTilemap = 0xD131
wConsole = 0xCAB4
wPermissionMap = 0xD133
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

# >>> factory MasonLaboratoryAfterDuel
CONTRACT["MasonLaboratoryAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["MasonLaboratoryAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x07",
        wLoadedNPCs: b"\x07" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x07", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory MasonLaboratoryAfterDuel

# >>> factory MasonLabCloseTextBox
CONTRACT["MasonLabCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["MasonLabCloseTextBox"] = [
    {"wram": {wOWMapEvents + 9: b"\x00\x01\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}},
    {"wram": {wOWMapEvents + 9: b"\x00\x02\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}},
    dict(POISON, wram={wOWMapEvents + 9: b"\x00\x03\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}),
]
# <<< factory MasonLabCloseTextBox

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
# >>> factory-mutation MasonLaboratoryAfterDuel
MUTATIONS["MasonLaboratoryAfterDuel"] = {"source_symbol": "MasonLaboratoryAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(MasonLaboratoryAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(MasonLaboratoryAfterDuelTable + 1u));", "case_ids": ["MasonLaboratoryAfterDuel-0"]}
# <<< factory-mutation MasonLaboratoryAfterDuel
# >>> factory-mutation MasonLabCloseTextBox
MUTATIONS["MasonLabCloseTextBox"] = {"source_symbol": "MasonLabCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_CHALLENGE_MACHINE);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_CHALLENGE_MACHINE + 1u));", "case_ids": ["MasonLabCloseTextBox-0", "MasonLabCloseTextBox-1"]}
# <<< factory-mutation MasonLabCloseTextBox
