"""Oracle-diff cases for poketcg/src/scripts/grass_club_entrance.asm."""
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
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
# >>> factory FindEndOfDuelScript
CONTRACT["FindEndOfDuelScript"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["FindEndOfDuelScript"] = [{"hl": 0xC600, "wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99", 0xC600: b"\x00"}}, dict(POISON, hl=0xC600, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99", 0xC600: b"\x00"})]
# <<< factory FindEndOfDuelScript
# >>> factory GrassClubEntranceAfterDuel
CONTRACT["GrassClubEntranceAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["GrassClubEntranceAfterDuel"] = [{"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}}, dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"})]
# <<< factory GrassClubEntranceAfterDuel
# >>> factory Preload_MichaelInGrassClubEntrance
CONTRACT["Preload_MichaelInGrassClubEntrance"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_MichaelInGrassClubEntrance"] = [{"wram": {0xD3D3: b"\x00"}}, {"wram": {0xD3D3: b"\x80"}}, dict(POISON, wram={0xD3D3: b"\x10"})]
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
MUTATIONS["Preload_MichaelInGrassClubEntrance"] = {"source_symbol": "Preload_MichaelInGrassClubEntrance", "before": "\tuint8_t a = GetEventValue(0x11u);", "after": "\tuint8_t a = GetEventValue(0x20u);", "case_ids": ["Preload_MichaelInGrassClubEntrance-1"]}
# <<< factory-mutation Preload_MichaelInGrassClubEntrance
