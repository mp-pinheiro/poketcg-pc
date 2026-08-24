"""Oracle-diff cases for poketcg/src/scripts/psychic_club.asm."""

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
    {"wram": {0xD3D1: bytes([0xFF]), 0xD3D2: bytes(0x40)}},
    dict(POISON, wram={0xD3D1: bytes([0xFF]), 0xD3D2: bytes(0x40)}),
]
# <<< factory Preload_Murray2

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation PsychicClubAfterDuel
MUTATIONS["PsychicClubAfterDuel"] = {"source_symbol": "PsychicClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(PsychicClubAfterDuelTable + 1u));", "case_ids": ["PsychicClubAfterDuel-0"]}
# <<< factory-mutation PsychicClubAfterDuel
# >>> factory-mutation Preload_Murray2
MUTATIONS["Preload_Murray2"] = {"source_symbol": "Preload_Murray2", "before": "uint8_t f = 0x40u;", "after": "uint8_t f = 0x00u;", "case_ids": ["Preload_Murray2-0"]}
# <<< factory-mutation Preload_Murray2
