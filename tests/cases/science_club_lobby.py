"""Oracle-diff cases for poketcg/src/scripts/science_club_lobby.asm."""

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

# >>> factory ScienceClubLobbyAfterDuel
CONTRACT["ScienceClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["ScienceClubLobbyAfterDuel"] = [
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
# <<< factory ScienceClubLobbyAfterDuel

from tests.cases._schema_migration import legacy_to_schema

# >>> factory Script_Specs2
# science_club_lobby.asm:68-81 is 24 bytes of straight-line code with a single
# exit, then `rst $20` at $6BDD begins the script bytecode; completion is
# declared pre-ret there. Running past the rst enters the RST20 bytecode
# interpreter, which needs ambient scene state a probed call cannot supply.
#
# `and %11` indexes the four-entry card-id table at Data_ebe7 (03:6BE7) =
# BD BB 27 2B, so driving the RNG to all four values exercises every entry and
# produces four distinct card names. UpdateRNGSources computes
#   new_r1 = ((ctr ^ r1) << 1) | (((r2 >> 6) ^ r1) & 1)
# hence new_r1 & 3 = feedback | ((ctr ^ r1) & 1) << 1, which the seeds below
# pick directly. Index 0 must be c=3: narrowing `& 0x03` to `& 0x01` is
# invisible at c=0 and c=1.
_SPECS2_TXRAM2 = 0xCE3F
_SPECS2_RNG = 0xCACA  # wRNG1, wRNG2, wRNGCounter
CONTRACT["Script_Specs2"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["Script_Specs2"] = [
    # c=3 -- table entry 0x2B; must be index 0 so the mask mutation reds
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {_SPECS2_TXRAM2: b"\xff\xff\xff", _SPECS2_RNG: b"\x00\x40\x01"},
     "read": {_SPECS2_TXRAM2: 3, _SPECS2_RNG: 3}},
    # c=0 -- table entry 0xBD
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {_SPECS2_TXRAM2: b"\xff\xff\xff", _SPECS2_RNG: b"\x00\x00\x00"},
     "read": {_SPECS2_TXRAM2: 3, _SPECS2_RNG: 3}},
    # c=1 -- table entry 0xBB
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {_SPECS2_TXRAM2: b"\xff\xff\xff", _SPECS2_RNG: b"\x00\x40\x00"},
     "read": {_SPECS2_TXRAM2: 3, _SPECS2_RNG: 3}},
    # c=2 -- table entry 0x27
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {_SPECS2_TXRAM2: b"\xff\xff\xff", _SPECS2_RNG: b"\x00\x00\x01"},
     "read": {_SPECS2_TXRAM2: 3, _SPECS2_RNG: 3}},
    dict(POISON,
         wram={_SPECS2_TXRAM2: b"\xff\xff\xff", _SPECS2_RNG: b"\x00\x40\x01"},
         read={_SPECS2_TXRAM2: 3, _SPECS2_RNG: 3}),
]
# <<< factory Script_Specs2

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion Script_Specs2
# The routine ends at its `rst $20`; legacy_to_schema always emits "return".
for _rec in SCHEMA2_CASES["Script_Specs2"]:
    _rec["completion"] = {"mode": "pre-ret", "pc": 0x6BDD}
# <<< factory-completion Script_Specs2

MUTATIONS = {}
# >>> factory-mutation ScienceClubLobbyAfterDuel
MUTATIONS["ScienceClubLobbyAfterDuel"] = {"source_symbol": "ScienceClubLobbyAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubLobbyAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(ScienceClubLobbyAfterDuelTable + 1u));", "case_ids": ["ScienceClubLobbyAfterDuel-0"]}
# <<< factory-mutation ScienceClubLobbyAfterDuel
# >>> factory-mutation Script_Specs2
MUTATIONS["Script_Specs2"] = {"source_symbol": "Script_Specs2", "before": "\tuint8_t c = (uint8_t)(rng & 0x03u);", "after": "\tuint8_t c = (uint8_t)(rng & 0x01u);", "case_ids": ["Script_Specs2-0", "Script_Specs2-3", "Script_Specs2-4"]}
# <<< factory-mutation Script_Specs2
