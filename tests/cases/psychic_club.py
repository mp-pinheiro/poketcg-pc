"""Oracle-diff cases for poketcg/src/scripts/psychic_club.asm."""
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

# >>> factory PsychicClubAfterDuel
CONTRACT["PsychicClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["PsychicClubAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x2c",
        wLoadedNPCs: b"\x2c" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x2c", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory PsychicClubAfterDuel

# >>> factory Preload_Murray2
CONTRACT["Preload_Murray2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Murray2"] = [
    {"wram": {sym("wLoadedEventBits"): bytes([0xFF]), sym("wEventVars"): bytes(0x40)}},
    dict(POISON, wram={sym("wLoadedEventBits"): bytes([0xFF]), sym("wEventVars"): bytes(0x40)}),
]
# <<< factory Preload_Murray2

# >>> factory Preload_Murray1
CONTRACT["Preload_Murray1"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Murray1"] = [
    {"wram": {sym("wLoadedEventBits"): bytes([0xFF]), sym("wEventVars"): bytes(0x40)}},
    dict(POISON, wram={sym("wLoadedEventBits"): bytes([0xFF]), sym("wEventVars"): bytes(0x40)}),
]
# <<< factory Preload_Murray1

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation PsychicClubAfterDuel
MUTATIONS["PsychicClubAfterDuel"] = {"source_symbol": "PsychicClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(PsychicClubAfterDuelTable + 1u));", "case_ids": ["PsychicClubAfterDuel-0"]}
# <<< factory-mutation PsychicClubAfterDuel
# >>> factory-mutation Preload_Murray2
MUTATIONS["Preload_Murray2"] = {"source_symbol": "Preload_Murray2", "before": "uint8_t f = 0x40u;", "after": "uint8_t f = 0x00u;", "case_ids": ["Preload_Murray2-0"]}
# <<< factory-mutation Preload_Murray2
# >>> factory-mutation Preload_Murray1
MUTATIONS["Preload_Murray1"] = {"source_symbol": "Preload_Murray1", "before": "uint8_t old_c = (uint8_t)(r.f & 0x10u);", "after": "uint8_t old_c = 0u;", "case_ids": ["Preload_Murray1-0"]}
# <<< factory-mutation Preload_Murray1
