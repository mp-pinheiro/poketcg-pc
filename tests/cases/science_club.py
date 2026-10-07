"""Oracle-diff cases for poketcg/src/scripts/science_club.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_Joseph
CONTRACT["Preload_Joseph"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Joseph"] = [
    {"wram": {sym("wEventVars") + 5: b"\x00"}},
    dict(POISON, wram={sym("wEventVars") + 5: b"\x80", sym("wLoadNPCXPos"): b"\x05"}, read={sym("wLoadNPCXPos"): 1, sym("wLoadNPCDirection"): 1}),
    {"wram": {sym("wEventVars") + 5: b"\x80", sym("wLoadNPCXPos"): b"\xFE"}, "read": {sym("wLoadNPCXPos"): 1, sym("wLoadNPCDirection"): 1}},
]
# <<< factory Preload_Joseph

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

# >>> factory ScienceClubAfterDuel
CONTRACT["ScienceClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["ScienceClubAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x2f",
        wLoadedNPCs: b"\x2f" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x2f", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory ScienceClubAfterDuel

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Preload_Joseph
MUTATIONS["Preload_Joseph"] = {"source_symbol": "Preload_Joseph", "before": "\t\tuint8_t new_x = (uint8_t)(x + 2u);", "after": "\t\tuint8_t new_x = (uint8_t)(x + 3u);", "case_ids": ["Preload_Joseph-1", "Preload_Joseph-2"]}
# <<< factory-mutation Preload_Joseph
# >>> factory-mutation ScienceClubAfterDuel
MUTATIONS["ScienceClubAfterDuel"] = {"source_symbol": "ScienceClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(ScienceClubAfterDuelTable + 1u));", "case_ids": ["ScienceClubAfterDuel-0"]}
# <<< factory-mutation ScienceClubAfterDuel
