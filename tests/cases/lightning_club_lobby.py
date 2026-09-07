"""Oracle-diff cases for poketcg/src/scripts/lightning_club_lobby.asm."""

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
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x00", 0xD3DD: b"\x08"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x00", 0xD3DD: b"\x0C"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x80", 0xD411: b"\x10", 0xD3DD: b"\x08"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    {"wram": {0xD3D4: b"\x00", 0xD411: b"\x00", 0xD3DD: b"\x08"}, "read": {0xD3D4: 1, 0xD3DD: 1}},
    dict(POISON, wram={0xD3D4: b"\x40", 0xD411: b"\x00", 0xD3DD: b"\x08"}, read={0xD3D4: 1, 0xD3DD: 1}),
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
