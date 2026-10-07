"""Oracle-diff cases for poketcg/src/scripts/lightning_club_lobby.asm."""
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

# >>> factory LightningClubLobbyAfterDuel
CONTRACT["LightningClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["LightningClubLobbyAfterDuel"] = [
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
# <<< factory LightningClubLobbyAfterDuel

# EVENT_IMAKUNI_STATE is bits 7-6 of $D3D4, EVENT_TEMP_DUELED_IMAKUNI bit 4 of
# $D411, EVENT_IMAKUNI_ROOM bits 3-2 of $D3DD (scripting.asm EventVarMasks).
# >>> factory Preload_ImakuniInLightningClubLobby
CONTRACT["Preload_ImakuniInLightningClubLobby"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_ImakuniInLightningClubLobby"] = [
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x08"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x0C"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x80", sym("wEventVars") + 0x3F: b"\x10", sym("wEventVars") + 0xB: b"\x08"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    {"wram": {sym("wEventVars") + 2: b"\x00", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x08"}, "read": {sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}},
    dict(POISON, wram={sym("wEventVars") + 2: b"\x40", sym("wEventVars") + 0x3F: b"\x00", sym("wEventVars") + 0xB: b"\x08"}, read={sym("wEventVars") + 2: 1, sym("wEventVars") + 0xB: 1}),
]
# <<< factory Preload_ImakuniInLightningClubLobby

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation LightningClubLobbyAfterDuel
MUTATIONS["LightningClubLobbyAfterDuel"] = {"source_symbol": "LightningClubLobbyAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubLobbyAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(LightningClubLobbyAfterDuelTable + 1u));", "case_ids": ["LightningClubLobbyAfterDuel-0"]}
# <<< factory-mutation LightningClubLobbyAfterDuel
# >>> factory-mutation Preload_ImakuniInLightningClubLobby
MUTATIONS["Preload_ImakuniInLightningClubLobby"] = {"source_symbol": "Preload_ImakuniInLightningClubLobby", "before": "\tif (room != IMAKUNI_LIGHTNING_CLUB)", "after": "\tif (room == IMAKUNI_LIGHTNING_CLUB)", "case_ids": ["Preload_ImakuniInLightningClubLobby-0", "Preload_ImakuniInLightningClubLobby-1"]}
# <<< factory-mutation Preload_ImakuniInLightningClubLobby
