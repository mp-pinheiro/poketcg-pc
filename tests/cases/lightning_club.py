"""Oracle-diff cases for poketcg/src/scripts/lightning_club.asm."""
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
# >>> factory LightningClubAfterDuel
CONTRACT["LightningClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["LightningClubAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {wDuelResult: b"\x00", wNPCDuelist: b"\x23", wLoadedNPCs: b"\x23" + b"\x00" * 95, wLoadedNPCTempIndex: b"\xEE", wScriptNPC: b"\xAA", wPlayerDirection: b"\x01", wOverworldNPCFlags: b"\x00", wNextScript: b"\xFF\xFF", wOverworldMode: b"\x00"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory LightningClubAfterDuel
# >>> factory Preload_Isaac
CONTRACT["Preload_Isaac"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Isaac"] = [
    {"wram": {sym("wEventVars") + 7: b"\x00"}},
    {"wram": {sym("wEventVars") + 7: b"\x38"}, "read": {sym("wEventVars") + 7: 1}},
    dict(POISON, wram={sym("wEventVars") + 7: b"\x38"}),
]
# <<< factory Preload_Isaac
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {}
# >>> factory-mutation LightningClubAfterDuel
MUTATIONS["LightningClubAfterDuel"] = {"source_symbol": "LightningClubAfterDuel", "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubAfterDuelTable);", "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(LightningClubAfterDuelTable + 1u));", "case_ids": ["LightningClubAfterDuel-0"]}
# <<< factory-mutation LightningClubAfterDuel
# >>> factory-mutation Preload_Isaac
MUTATIONS["Preload_Isaac"] = {"source_symbol": "Preload_Isaac", "before": "\ta = SOUTH;", "after": "\ta = 0u;", "case_ids": ["Preload_Isaac-1", "Preload_Isaac-2"]}
# <<< factory-mutation Preload_Isaac
