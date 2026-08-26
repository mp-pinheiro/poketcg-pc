"""Oracle-diff cases for poketcg/src/scripts/grass_club.asm."""

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

# >>> factory GrassClubAfterDuel
CONTRACT["GrassClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["GrassClubAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x28",
        wLoadedNPCs: b"\x28" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x28", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory GrassClubAfterDuel

from tests.cases._schema_migration import legacy_to_schema

# >>> factory Script_Nikki
# grass_club.asm:95-98 is 8 bytes of code:
#   ld a, [wCurMap] / cp ISHIHARAS_HOUSE / jp z, Script_NikkiInIshiharasHouse
# BOTH exits enter script bytecode via a `rst $20`, so this routine has TWO
# completion points and each case declares the one its seed reaches:
#   wCurMap != 3 -> falls through to the `start_script` rst at $67A6
#   wCurMap == 3 -> jumps to Script_NikkiInIshiharasHouse, whose first byte is
#                   the rst at $5AE9
# The routine's only real effect is choosing between them, which a per-routine
# port cannot express as control flow, so the decision rides in `f`: Z set means
# taken. Comparing `f` is what verifies the branch. The map values below cover
# Z set (3), the half-carry borrow (1 and 2 -> H and C set) and no borrow
# (4 -> H and C clear), so all four cp flag bits are exercised.
# Index 0 must be wCurMap == 3, the only value where retargeting the compare
# constant changes the result.
_NIKKI_CURMAP = 0xD32F
_NIKKI_MAPS = (0x03, 0x01, 0x02, 0x04)
_NIKKI_RST = {True: 0x5AE9, False: 0x67A6}  # keyed by "jump taken"
CONTRACT["Script_Nikki"] = {"compare": ("a", "f"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Script_Nikki"] = [
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {_NIKKI_CURMAP: bytes((_m,))}, "read": {_NIKKI_CURMAP: 1}}
    for _m in _NIKKI_MAPS
]
CASES["Script_Nikki"].append(
    dict(POISON, wram={_NIKKI_CURMAP: b"\x03"}, read={_NIKKI_CURMAP: 1}))
# <<< factory Script_Nikki

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion Script_Nikki
# One completion pc per case, derived from that case's own seeded wCurMap so the
# two can never drift apart. The POISON case appended last also seeds 3.
_NIKKI_SEEDS = list(_NIKKI_MAPS) + [0x03]
for _rec, _m in zip(SCHEMA2_CASES["Script_Nikki"], _NIKKI_SEEDS):
    _rec["completion"] = {"mode": "pre-ret", "pc": _NIKKI_RST[_m == 0x03]}
# <<< factory-completion Script_Nikki

MUTATIONS = {}
# >>> factory-mutation GrassClubAfterDuel
MUTATIONS["GrassClubAfterDuel"] = {"source_symbol": "GrassClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(GrassClubAfterDuelTable + 1u));", "case_ids": ["GrassClubAfterDuel-0"]}
# <<< factory-mutation GrassClubAfterDuel
# >>> factory-mutation Script_Nikki
MUTATIONS["Script_Nikki"] = {"source_symbol": "Script_Nikki", "before": "\treturn (ScriptNikkiResult){map, nikki_cp_flags(map, ISHIHARAS_HOUSE)};", "after": "\treturn (ScriptNikkiResult){map, nikki_cp_flags(map, 0x04u)};", "case_ids": ["Script_Nikki-0", "Script_Nikki-4"]}
# <<< factory-mutation Script_Nikki
