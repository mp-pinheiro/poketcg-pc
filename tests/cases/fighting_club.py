"""Oracle-diff cases for poketcg/src/scripts/fighting_club.asm."""

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

# >>> factory FightingClubAfterDuel
CONTRACT["FightingClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["FightingClubAfterDuel"] = [
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
# <<< factory FightingClubAfterDuel

# The pupil states are the high nibbles of wEventVars bytes $01, $03 and $06
# ($D3D3 Michael, $D3D5 Chris, $D3D8 Jessica; scripting.asm:407-422);
# PUPIL_DEFEATED is 8.
# >>> factory Preload_ChrisInFightingClub
CONTRACT["Preload_ChrisInFightingClub"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_ChrisInFightingClub"] = [
    {"wram": {0xD3D5: b"\x00"}},
    {"wram": {0xD3D5: b"\x80"}},
    {"wram": {0xD3D5: b"\x70"}},
    dict(POISON, wram={0xD3D5: b"\x90"}),
]
# <<< factory Preload_ChrisInFightingClub

# >>> factory Preload_MichaelInFightingClub
CONTRACT["Preload_MichaelInFightingClub"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_MichaelInFightingClub"] = [
    {"wram": {0xD3D3: b"\x00"}},
    {"wram": {0xD3D3: b"\x80"}},
    dict(POISON, wram={0xD3D3: b"\x70"}),
]
# <<< factory Preload_MichaelInFightingClub

# >>> factory Preload_JessicaInFightingClub
CONTRACT["Preload_JessicaInFightingClub"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_JessicaInFightingClub"] = [
    {"wram": {0xD3D8: b"\x00"}},
    {"wram": {0xD3D8: b"\x80"}},
    dict(POISON, wram={0xD3D8: b"\x70"}),
]
# <<< factory Preload_JessicaInFightingClub

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation FightingClubAfterDuel
MUTATIONS["FightingClubAfterDuel"] = {"source_symbol": "FightingClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FightingClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(FightingClubAfterDuelTable + 1u));", "case_ids": ["FightingClubAfterDuel-0"]}
# <<< factory-mutation FightingClubAfterDuel
# >>> factory-mutation Preload_ChrisInFightingClub
MUTATIONS["Preload_ChrisInFightingClub"] = {"source_symbol": "Preload_ChrisInFightingClub", "before": "\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);", "after": "\treturn preload_pupil(EVENT_PUPIL_MICHAEL_STATE);", "case_ids": ["Preload_ChrisInFightingClub-1"]}
# <<< factory-mutation Preload_ChrisInFightingClub
# >>> factory-mutation Preload_MichaelInFightingClub
MUTATIONS["Preload_MichaelInFightingClub"] = {"source_symbol": "Preload_MichaelInFightingClub", "before": "\treturn preload_pupil(EVENT_PUPIL_MICHAEL_STATE);", "after": "\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);", "case_ids": ["Preload_MichaelInFightingClub-1"]}
# <<< factory-mutation Preload_MichaelInFightingClub
# >>> factory-mutation Preload_JessicaInFightingClub
MUTATIONS["Preload_JessicaInFightingClub"] = {"source_symbol": "Preload_JessicaInFightingClub", "before": "\treturn preload_pupil(EVENT_PUPIL_JESSICA_STATE);", "after": "\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);", "case_ids": ["Preload_JessicaInFightingClub-1"]}
# <<< factory-mutation Preload_JessicaInFightingClub
