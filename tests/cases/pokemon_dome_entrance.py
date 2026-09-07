"""Oracle-diff cases for poketcg/src/scripts/pokemon_dome_entrance.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wCurTilemap = 0xD131
wConsole = 0xCAB4
wPermissionMap = 0xD133
# <<< factory-cases-statics
# >>> factory PokemonDomeEntranceLoadMap
wEventVarByte_Dome = 0xD3E9
wEventVarByte_NPC = 0xD3EA
wReceivedLegendary = 0xD3D8
wEventVarByte_Ronald = 0xD3EB
CONTRACT["PokemonDomeEntranceLoadMap"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["PokemonDomeEntranceLoadMap"] = [
    {"wram": {wEventVarByte_Dome: b"\xFF", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x00"}},
    {"wram": {wEventVarByte_Dome: b"\x08", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x02"}},
    dict(POISON, wram={wEventVarByte_Dome: b"\x00", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x00"}),
]
# <<< factory PokemonDomeEntranceLoadMap

# >>> factory PokemonDomeEntranceCloseTextBox
CONTRACT["PokemonDomeEntranceCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["PokemonDomeEntranceCloseTextBox"] = [
    {"wram": {wOWMapEvents: b"\xFF\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}},
    {"wram": {wOWMapEvents: b"\x02\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}},
    dict(POISON, wram={wOWMapEvents: b"\x03\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}),
]
# <<< factory PokemonDomeEntranceCloseTextBox

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation PokemonDomeEntranceCloseTextBox
MUTATIONS["PokemonDomeEntranceCloseTextBox"] = {"source_symbol": "PokemonDomeEntranceCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_POKEMON_DOME_DOOR);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_POKEMON_DOME_DOOR + 1u));", "case_ids": ["PokemonDomeEntranceCloseTextBox-0", "PokemonDomeEntranceCloseTextBox-1"]}
# <<< factory-mutation PokemonDomeEntranceCloseTextBox
# >>> factory-mutation PokemonDomeEntranceLoadMap
MUTATIONS["PokemonDomeEntranceLoadMap"] = {"source_symbol": "PokemonDomeEntranceLoadMap", "before": "ZeroOutEventValue(EVENT_POKEMON_DOME_STATE", "after": "ZeroOutEventValue(EVENT_HALL_OF_HONOR_DOORS_OPEN", "case_ids": ["PokemonDomeEntranceLoadMap-0"]}
# <<< factory-mutation PokemonDomeEntranceLoadMap
