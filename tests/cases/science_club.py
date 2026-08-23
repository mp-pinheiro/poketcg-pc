"""Oracle-diff cases for poketcg/src/scripts/science_club.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_Joseph
CONTRACT["Preload_Joseph"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Preload_Joseph"] = [
    {"wram": {0xD3D7: b"\x00"}},
    dict(POISON, wram={0xD3D7: b"\x80", 0xD3AC: b"\x05"}, read={0xD3AC: 1, 0xD3AE: 1}),
    {"wram": {0xD3D7: b"\x80", 0xD3AC: b"\xFE"}, "read": {0xD3AC: 1, 0xD3AE: 1}},
]
# <<< factory Preload_Joseph

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
