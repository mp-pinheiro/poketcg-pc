"""Oracle-diff cases for poketcg/src/scripts/grass_club_entrance.asm."""
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
# >>> factory FindEndOfDuelScript
CONTRACT["FindEndOfDuelScript"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["FindEndOfDuelScript"] = [{"hl": sym("wc600"), "wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99", sym("wc600"): b"\x00"}}, dict(POISON, hl=sym("wc600"), wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99", sym("wc600"): b"\x00"})]
# <<< factory FindEndOfDuelScript
# >>> factory GrassClubEntranceAfterDuel
CONTRACT["GrassClubEntranceAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["GrassClubEntranceAfterDuel"] = [{"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}}, dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"})]
# <<< factory GrassClubEntranceAfterDuel
# >>> factory Preload_MichaelInGrassClubEntrance
CONTRACT["Preload_MichaelInGrassClubEntrance"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_MichaelInGrassClubEntrance"] = [{"wram": {sym("wEventVars") + 1: b"\x00"}}, {"wram": {sym("wEventVars") + 1: b"\x80"}}, dict(POISON, wram={sym("wEventVars") + 1: b"\x10"})]
# <<< factory Preload_MichaelInGrassClubEntrance
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {}
# >>> factory-mutation FindEndOfDuelScript
MUTATIONS["FindEndOfDuelScript"] = {"source_symbol": "FindEndOfDuelScript", "before": "\thl = (uint16_t)(hl + c);", "after": "\thl = (uint16_t)(hl + c + 1u);", "case_ids": ["FindEndOfDuelScript-0"]}
# <<< factory-mutation FindEndOfDuelScript
# >>> factory-mutation GrassClubEntranceAfterDuel
MUTATIONS["GrassClubEntranceAfterDuel"] = {"source_symbol": "GrassClubEntranceAfterDuel", "before": "\treturn FindEndOfDuelScript(GrassClubEntranceAfterDuelTable);", "after": "\treturn FindEndOfDuelScript((uint16_t)(GrassClubEntranceAfterDuelTable + 1u));", "case_ids": ["GrassClubEntranceAfterDuel-0"]}
# <<< factory-mutation GrassClubEntranceAfterDuel
# >>> factory-mutation Preload_MichaelInGrassClubEntrance
MUTATIONS["Preload_MichaelInGrassClubEntrance"] = {"source_symbol": "Preload_MichaelInGrassClubEntrance", "before": "\tuint8_t a = GetEventValue(EVENT_PUPIL_MICHAEL_STATE);", "after": "\tuint8_t a = GetEventValue(0x20u);", "case_ids": ["Preload_MichaelInGrassClubEntrance-1"]}
# <<< factory-mutation Preload_MichaelInGrassClubEntrance
