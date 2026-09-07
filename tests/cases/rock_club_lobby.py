"""Oracle-diff cases for poketcg/src/scripts/rock_club_lobby.asm."""

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

# >>> factory RockClubLobbyAfterDuel
CONTRACT["RockClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["RockClubLobbyAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x17",
        wLoadedNPCs: b"\x17" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x17", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory RockClubLobbyAfterDuel

# >>> factory Preload_Lass3
CONTRACT["Preload_Lass3"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Lass3"] = [
    {"wram": {0xD3D8: b"\x00"}},
    {"wram": {0xD3D8: b"\x02"}},
    dict(POISON, wram={0xD3D8: b"\x02"}),
]
# <<< factory Preload_Lass3

# >>> factory Preload_ChrisInRockClubLobby
CONTRACT["Preload_ChrisInRockClubLobby"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_ChrisInRockClubLobby"] = [
    {"wram": {0xD3D5: b"\x00"}},
    {"wram": {0xD3D5: b"\x10"}},
    {"wram": {0xD3D5: b"\x80"}},
    dict(POISON, wram={0xD3D5: b"\x90"}),
]
# <<< factory Preload_ChrisInRockClubLobby

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation RockClubLobbyAfterDuel
MUTATIONS["RockClubLobbyAfterDuel"] = {"source_symbol": "RockClubLobbyAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(RockClubLobbyAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(RockClubLobbyAfterDuelTable + 1u));", "case_ids": ["RockClubLobbyAfterDuel-0"]}
# <<< factory-mutation RockClubLobbyAfterDuel
# >>> factory-mutation Preload_Lass3
MUTATIONS["Preload_Lass3"] = {"source_symbol": "Preload_Lass3", "before": "\tif (a < TRUE)\n\t\tf |= 0x10u;", "after": "\tif (a <= TRUE)\n\t\tf |= 0x10u;", "case_ids": ["Preload_Lass3-1"]}
# <<< factory-mutation Preload_Lass3
# >>> factory-mutation Preload_ChrisInRockClubLobby
MUTATIONS["Preload_ChrisInRockClubLobby"] = {"source_symbol": "Preload_ChrisInRockClubLobby", "before": "\tif (a < PUPIL_DEFEATED)\n\t\tf |= 0x10u;", "after": "\tif (a <= PUPIL_DEFEATED)\n\t\tf |= 0x10u;", "case_ids": ["Preload_ChrisInRockClubLobby-2"]}
# <<< factory-mutation Preload_ChrisInRockClubLobby
