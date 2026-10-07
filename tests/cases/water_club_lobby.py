"""Oracle-diff cases for poketcg/src/scripts/water_club_lobby.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wDuelResult = sym("wDuelResult")
wNPCDuelist = sym("wNPCDuelist")
wTempNPC = sym("wTempNPC")
wLoadedNPCs = sym("wLoadedNPCs")
wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
wScriptNPC = sym("wScriptNPC")
wPlayerDirection = sym("wPlayerDirection")
wOverworldNPCFlags = sym("wOverworldNPCFlags")
wNextScript = sym("wNextScript")
wOverworldMode = sym("wOverworldMode")
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
    {"wram": {sym("wEventVars") + 0xB: b"\x00"}},
    {"wram": {sym("wEventVars") + 0xB: b"\x20"}},
    dict(POISON, wram={sym("wEventVars") + 0xB: b"\x30"}),
]
# <<< factory Preload_Man2

# EVENT_IMAKUNI_STATE is bits 7-6 of $D3D4, EVENT_TEMP_DUELED_IMAKUNI bit 4 of
# $D411, EVENT_IMAKUNI_ROOM bits 3-2 of $D3DD (scripting.asm EventVarMasks).
# >>> factory Preload_ImakuniInWaterClubLobby
CONTRACT["Preload_ImakuniInWaterClubLobby"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_ImakuniInWaterClubLobby"] = [
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x0C"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x00"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x10", sym("wEventVars") + 0xB: b"\x0C"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x00", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x0C"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    dict(POISON, wram={sym("wEventVars") + 2: b"\x40", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x0C"}, read={sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}),
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
