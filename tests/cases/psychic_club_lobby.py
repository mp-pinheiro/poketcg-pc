"""Oracle-diff cases for poketcg/src/scripts/psychic_club_lobby.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory PsychicClubLobbyLoadMap
CONTRACT["PsychicClubLobbyLoadMap"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["PsychicClubLobbyLoadMap"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD34A: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0xD3AA: b'\xEE'}},
    dict(POISON, wram={0xD34A: b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0xD3AA: b'\xEE'}),
]
# <<< factory PsychicClubLobbyLoadMap

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

# >>> factory PsychicClubLobbyAfterDuel
CONTRACT["PsychicClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["PsychicClubLobbyAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x2b",
        wLoadedNPCs: b"\x2b" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x2b", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory PsychicClubLobbyAfterDuel

# >>> factory _Preload_Ronald1InPsychicClubLobby
CONTRACT["_Preload_Ronald1InPsychicClubLobby"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_Preload_Ronald1InPsychicClubLobby"] = [
    {"wram": {0xD3D1: bytes([0xFF]), 0xD3D2: bytes(0x40)}},
    dict(POISON, wram={0xD3D1: bytes([0xFF]), 0xD3D2: bytes(0x40)}),
]
# <<< factory _Preload_Ronald1InPsychicClubLobby

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation PsychicClubLobbyLoadMap
MUTATIONS["PsychicClubLobbyLoadMap"] = {"source_symbol": "PsychicClubLobbyLoadMap", "before": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_ea02_ADDR, hl);", "after": "\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_ea02_ADDR + 1u), hl);", "case_ids": ["PsychicClubLobbyLoadMap-0"]}
# <<< factory-mutation PsychicClubLobbyLoadMap
# >>> factory-mutation PsychicClubLobbyAfterDuel
MUTATIONS["PsychicClubLobbyAfterDuel"] = {"source_symbol": "PsychicClubLobbyAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubLobbyAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(PsychicClubLobbyAfterDuelTable + 1u));", "case_ids": ["PsychicClubLobbyAfterDuel-0"]}
# <<< factory-mutation PsychicClubLobbyAfterDuel
# >>> factory-mutation _Preload_Ronald1InPsychicClubLobby
MUTATIONS["_Preload_Ronald1InPsychicClubLobby"] = {"source_symbol": "_Preload_Ronald1InPsychicClubLobby", "before": "uint8_t f = (medal_count == 0u) ? 0x80u : 0x00u;", "after": "uint8_t f = (medal_count == 0u) ? 0x00u : 0x80u;", "case_ids": ["_Preload_Ronald1InPsychicClubLobby-0"]}
# <<< factory-mutation _Preload_Ronald1InPsychicClubLobby
