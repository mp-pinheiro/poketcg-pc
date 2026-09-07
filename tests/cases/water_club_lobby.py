"""Oracle-diff cases for poketcg/src/scripts/water_club_lobby.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
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
# <<< factory-cases-statics

# >>> factory WaterClubLobbyAfterDuel
CONTRACT["WaterClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["WaterClubLobbyAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x04",
        wLoadedNPCs: b"\x04" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x04", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory WaterClubLobbyAfterDuel

# >>> factory Preload_Man2
CONTRACT["Preload_Man2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Man2"] = [
    {"wram": {0xD3DD: b"\x00"}},
    {"wram": {0xD3DD: b"\x20"}},
    dict(POISON, wram={0xD3DD: b"\x30"}),
]
# <<< factory Preload_Man2

# EVENT_IMAKUNI_STATE is bits 7-6 of $D3D4, EVENT_TEMP_DUELED_IMAKUNI bit 4 of
# $D411, EVENT_IMAKUNI_ROOM bits 3-2 of $D3DD (scripting.asm EventVarMasks).
# >>> factory Preload_ImakuniInWaterClubLobby
CONTRACT["Preload_ImakuniInWaterClubLobby"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_ImakuniInWaterClubLobby"] = [
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x00", 0xD3DD: b"\x0C"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x00", 0xD3DD: b"\x00"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x10", 0xD3DD: b"\x0C"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x00", 0xD411: b"\x00", 0xD3DD: b"\x0C"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    dict(POISON, wram={0xD3D4: b"\x40", 0xD411: b"\x00", 0xD3DD: b"\x0C"}, read={0xD3D4: 1, 0xD3DD: 1}),
]
# <<< factory Preload_ImakuniInWaterClubLobby

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation WaterClubLobbyAfterDuel
MUTATIONS["WaterClubLobbyAfterDuel"] = {"source_symbol": "WaterClubLobbyAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubLobbyAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(WaterClubLobbyAfterDuelTable + 1u));", "case_ids": ["WaterClubLobbyAfterDuel-0"]}
# <<< factory-mutation WaterClubLobbyAfterDuel
# >>> factory-mutation Preload_Man2
MUTATIONS["Preload_Man2"] = {"source_symbol": "Preload_Man2", "before": "\tif (a < JOSHUA_DEFEATED)\n\t\tf |= 0x10u;", "after": "\tif (a <= JOSHUA_DEFEATED)\n\t\tf |= 0x10u;", "case_ids": ["Preload_Man2-1"]}
# <<< factory-mutation Preload_Man2
# >>> factory-mutation Preload_ImakuniInWaterClubLobby
MUTATIONS["Preload_ImakuniInWaterClubLobby"] = {"source_symbol": "Preload_ImakuniInWaterClubLobby", "before": "\tif (room != IMAKUNI_WATER_CLUB)", "after": "\tif (room == IMAKUNI_WATER_CLUB)", "case_ids": ["Preload_ImakuniInWaterClubLobby-0", "Preload_ImakuniInWaterClubLobby-1"]}
# <<< factory-mutation Preload_ImakuniInWaterClubLobby
