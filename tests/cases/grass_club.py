"""Oracle-diff cases for poketcg/src/scripts/grass_club.asm."""
from tests.cases._symbols import sym
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
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
# >>> factory GrassClubAfterDuel
CONTRACT["GrassClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["GrassClubAfterDuel"] = [{"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}}, dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"})]
# <<< factory GrassClubAfterDuel
# >>> factory Script_Nikki
CONTRACT["Script_Nikki"] = {"compare": ("a", "f"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Script_Nikki"] = [{"wram": {sym("wCurMap"): b"\x03"}}, {"wram": {sym("wCurMap"): b"\x01"}}, dict(POISON, wram={sym("wCurMap"): b"\x03"})]
# <<< factory Script_Nikki
# >>> factory Preload_NikkiInGrassClub
CONTRACT["Preload_NikkiInGrassClub"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_NikkiInGrassClub"] = [{"wram": {sym("wEventVars") + 0xB: b"\x00"}}, {"wram": {sym("wEventVars") + 0xB: b"\x02"}}, dict(POISON, wram={sym("wEventVars") + 0xB: b"\x02"})]
# <<< factory Preload_NikkiInGrassClub
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion Script_Nikki
_NIKKI_RST = {True: sym("Script_NikkiInIshiharasHouse"), False: sym("Script_Nikki") + 8}
_NIKKI_SEEDS = [0x03, 0x01, 0x03]
for _rec, _m in zip(SCHEMA2_CASES["Script_Nikki"], _NIKKI_SEEDS):
    _rec["completion"] = {"mode": "pre-ret", "pc": _NIKKI_RST[_m == 0x03]}
# <<< factory-completion Script_Nikki
MUTATIONS = {}
# >>> factory-mutation GrassClubAfterDuel
MUTATIONS["GrassClubAfterDuel"] = {"source_symbol": "GrassClubAfterDuel", "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubAfterDuelTable);", "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(GrassClubAfterDuelTable + 1u));", "case_ids": ["GrassClubAfterDuel-0"]}
# <<< factory-mutation GrassClubAfterDuel
# >>> factory-mutation Script_Nikki
MUTATIONS["Script_Nikki"] = {"source_symbol": "Script_Nikki", "before": "return (ScriptNikkiResult){map, nikki_cp_flags(map, ISHIHARAS_HOUSE),", "after": "return (ScriptNikkiResult){map, nikki_cp_flags(map, 0x04u),", "case_ids": ["Script_Nikki-0"]}
# <<< factory-mutation Script_Nikki
# >>> factory-mutation Preload_NikkiInGrassClub
MUTATIONS["Preload_NikkiInGrassClub"] = {"source_symbol": "Preload_NikkiInGrassClub", "before": "uint8_t a = GetEventValue(EVENT_NIKKI_STATE);", "after": "uint8_t a = GetEventValue(0x11u);", "case_ids": ["Preload_NikkiInGrassClub-1"]}
# <<< factory-mutation Preload_NikkiInGrassClub
