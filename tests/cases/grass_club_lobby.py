"""Oracle-diff cases for poketcg/src/scripts/grass_club_lobby.asm."""
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

# >>> factory GrassClubLobbyAfterDuel
CONTRACT["GrassClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["GrassClubLobbyAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x27",
        wLoadedNPCs: b"\x27" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x27", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory GrassClubLobbyAfterDuel

# >>> factory Preload_Gal2
CONTRACT["Preload_Gal2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Gal2"] = [
    {"wram": {sym("wEventVars") + 6: b"\x00"}},
    {"wram": {sym("wEventVars") + 6: b"\x02"}},
    dict(POISON, wram={sym("wEventVars") + 6: b"\x02"}),
]
# <<< factory Preload_Gal2

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GrassClubLobbyAfterDuel
MUTATIONS["GrassClubLobbyAfterDuel"] = {"source_symbol": "GrassClubLobbyAfterDuel", "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubLobbyAfterDuelTable);", "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(GrassClubLobbyAfterDuelTable + 1u));", "case_ids": ["GrassClubLobbyAfterDuel-0"]}
# <<< factory-mutation GrassClubLobbyAfterDuel
# >>> factory-mutation Preload_Gal2
MUTATIONS["Preload_Gal2"] = {"source_symbol": "Preload_Gal2", "before": "\tif (a < TRUE)\n\t\tf |= 0x10u;", "after": "\tif (a <= TRUE)\n\t\tf |= 0x10u;", "case_ids": ["Preload_Gal2-1"]}
# <<< factory-mutation Preload_Gal2
