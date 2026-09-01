POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadNPCXPos = 0xD3AC
wLoadNPCYPos = 0xD3AD
wLoadNPCDirection = 0xD3AE


CONTRACT = {
    "Func_f762": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "Func_f782": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "PlacePokemonDomeOpponentAtDuelTable": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Func_f762": [
        {"read": {wLoadNPCYPos: 1}},
        dict(POISON, wram={wLoadNPCYPos: b"\xee"},
             read={wLoadNPCYPos: 1}),
        {"f": 0xF0, "wram": {wLoadNPCYPos: b"\xfe"},
         "read": {wLoadNPCYPos: 1}},
        {"f": 0x00, "wram": {wLoadNPCYPos: b"\xff"},
         "read": {wLoadNPCYPos: 1}},
        {"f": 0x80, "wram": {wLoadNPCYPos: b"\x01"},
         "read": {wLoadNPCYPos: 1}},
    ],
    "Func_f782": [
        {"read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1}},
        dict(POISON, b=0xBB, c=0xCC,
             read={wLoadNPCXPos: 1, wLoadNPCYPos: 1}),
        {"b": 0xFF, "c": 0xFE, "f": 0xF0,
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1}},
        {"b": 0x01, "c": 0x00, "f": 0x80,
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1}},
    ],
    "PlacePokemonDomeOpponentAtDuelTable": [
        {"read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
        dict(POISON,
             read={wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}),
        {"f": 0x80,
         "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
    ],
}

# >>> factory Func_f77d
CONTRACT["Func_f77d"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["Func_f77d"] = [
    {"read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
    dict(POISON, b=0xBB, c=0xCC,
         read={wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}),
    {"b": 0xFF, "c": 0xFE, "f": 0xF0,
     "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
    {"b": 0x01, "c": 0x00, "f": 0x80,
     "read": {wLoadNPCXPos: 1, wLoadNPCYPos: 1, wLoadNPCDirection: 1}},
]
# <<< factory Func_f77d

# >>> factory-cases-statics
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wCurTilemap = 0xD131
wConsole = 0xCAB4
wPermissionMap = 0xD133

wPlayerYCoord = 0xD331
wPlayerXCoord = 0xD330
wTempNPC = 0xD3AB
wLoadedNPCs = 0xD34A
wLoadedNPCTempIndex = 0xD3AA
wScriptNPC = 0xD3B6
wPlayerDirection = 0xD334
wOverworldNPCFlags = 0xD0C1
wNextScript = 0xD0C6
wOverworldMode = 0xD0BF
NPC_TABLE = b"\x00" * 96
READ_SPAN = {wTempNPC: 1, wLoadedNPCTempIndex: 1, wScriptNPC: 1, wNextScript: 2}

wEventVarByte_A = 0xD3E9
wPCPacks_A = 0xD11E
wNextScript_A = 0xD0C6
# <<< factory-cases-statics

# >>> factory PokemonDomeCloseTextBox
CONTRACT["PokemonDomeCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["PokemonDomeCloseTextBox"] = [
    {"wram": {wOWMapEvents: b"\x00\xFF\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 3, wPermissionMap: 256}},
    {"wram": {wOWMapEvents: b"\x00\x02\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 3, wPermissionMap: 256}},
    dict(POISON, wram={wOWMapEvents: b"\x00\x03\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents: 3, wPermissionMap: 256}),
]
# <<< factory PokemonDomeCloseTextBox

# >>> factory PokemonDomeMovePlayer
CONTRACT["PokemonDomeMovePlayer"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PokemonDomeMovePlayer"] = [
    {"wram": {wPlayerYCoord: b"\x00", wPlayerXCoord: b"\x0F", wTempNPC: b"\xFF",
              wScriptNPC: b"\xFF", wLoadedNPCTempIndex: b"\xFF", wNextScript: b"\xFF\xFF"},
     "read": READ_SPAN},
    {"wram": {wPlayerYCoord: b"\x16", wPlayerXCoord: b"\x0D", wTempNPC: b"\xFF",
              wScriptNPC: b"\xFF", wLoadedNPCTempIndex: b"\xFF", wNextScript: b"\xFF\xFF"},
     "read": READ_SPAN},
    {"wram": {wPlayerYCoord: b"\x16", wPlayerXCoord: b"\x11", wTempNPC: b"\xFF",
              wScriptNPC: b"\xFF", wLoadedNPCTempIndex: b"\xFF", wNextScript: b"\xFF\xFF"},
     "read": READ_SPAN},
    dict(POISON, wram={wPlayerYCoord: b"\x16", wPlayerXCoord: b"\x0F", wTempNPC: b"\x00",
                       wLoadedNPCs: NPC_TABLE, wLoadedNPCTempIndex: b"\xEE", wScriptNPC: b"\xAA",
                       wPlayerDirection: b"\x01", wOverworldNPCFlags: b"\x00",
                       wNextScript: b"\xFF\xFF", wOverworldMode: b"\x00"},
         read=READ_SPAN),
]
# <<< factory PokemonDomeMovePlayer

# >>> factory PokemonDomeLoadMap
CONTRACT["PokemonDomeLoadMap"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PokemonDomeLoadMap"] = [
    {"wram": {wEventVarByte_A: b"\x00", wPCPacks_A: bytes(15)},
     "read": {wPCPacks_A: 15, wNextScript_A: 2}},
    dict(POISON, wram={wEventVarByte_A: b"\x08", wPCPacks_A: bytes(15)},
         read={wPCPacks_A: 15, wNextScript_A: 2}),
]
# <<< factory PokemonDomeLoadMap

# >>> factory PokemonDomeAfterDuel
CONTRACT["PokemonDomeAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["PokemonDomeAfterDuel"] = [
    {"wram": {0xD0C3: b"\x00", 0xD0C4: b"\x00"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"wram": {0xD0C3: b"\x00", 0xD0C4: b"\x37"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xD0C3: b"\x01", 0xD0C4: b"\x37"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory PokemonDomeAfterDuel

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Func_f762": {
        "source_symbol": "Func_f762",
        "before": "gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 2u",
        "after": "gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 3u",
        "case_ids": ["Func_f762-2", "Func_f762-0", "Func_f762-1",
                     "Func_f762-3", "Func_f762-4"],
    },
    "Func_f782": {
        "source_symbol": "Func_f782",
        "before": "gb_write8(W_LOAD_NPC_X_POS_ADDR, b)",
        "after": "gb_write8(W_LOAD_NPC_X_POS_ADDR, c)",
        "case_ids": ["Func_f782-2", "Func_f782-0", "Func_f782-1", "Func_f782-3"],
    },
    "PlacePokemonDomeOpponentAtDuelTable": {
        "source_symbol": "PlacePokemonDomeOpponentAtDuelTable",
        "before": "gb_write8(W_LOAD_NPC_Y_POS_ADDR, 0x0Eu)",
        "after": "gb_write8(W_LOAD_NPC_Y_POS_ADDR, 0x0Fu)",
        "case_ids": ["PlacePokemonDomeOpponentAtDuelTable-0",
                     "PlacePokemonDomeOpponentAtDuelTable-1",
                     "PlacePokemonDomeOpponentAtDuelTable-2"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation Func_f77d
MUTATIONS["Func_f77d"] = {
    "source_symbol": "Func_f77d",
    "before": "return Func_f782(b, c, f);",
    "after": "return Func_f782(c, b, f);",
    "case_ids": ["Func_f77d-1", "Func_f77d-2", "Func_f77d-3"],
}
# <<< factory-mutation Func_f77d
# >>> factory-mutation PokemonDomeCloseTextBox
MUTATIONS["PokemonDomeCloseTextBox"] = {"source_symbol": "PokemonDomeCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_HALL_OF_HONOR_DOOR);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_HALL_OF_HONOR_DOOR + 1u));", "case_ids": ["PokemonDomeCloseTextBox-0", "PokemonDomeCloseTextBox-1"]}
# <<< factory-mutation PokemonDomeCloseTextBox
# >>> factory-mutation PokemonDomeMovePlayer
MUTATIONS["PokemonDomeMovePlayer"] = {"source_symbol": "PokemonDomeMovePlayer", "before": "gb_write8(0xD3ABu, 0x3Au);", "after": "gb_write8(0xD3ABu, 0x3Bu);", "case_ids": ["PokemonDomeMovePlayer-3"]}
# <<< factory-mutation PokemonDomeMovePlayer
# >>> factory-mutation PokemonDomeLoadMap
MUTATIONS["PokemonDomeLoadMap"] = {"source_symbol": "PokemonDomeLoadMap", "before": "\tSetNextScript(0x780Bu);", "after": "\tSetNextScript(0x780Cu);", "case_ids": ["PokemonDomeLoadMap-1"]}
# <<< factory-mutation PokemonDomeLoadMap
# >>> factory-mutation PokemonDomeAfterDuel
MUTATIONS["PokemonDomeAfterDuel"] = {
    "source_symbol": "PokemonDomeAfterDuel",
    "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(PokemonDomeAfterDuelTable);",
    "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(PokemonDomeAfterDuelTable + 1u));",
    "case_ids": ["PokemonDomeAfterDuel-0", "PokemonDomeAfterDuel-1"]
}
# <<< factory-mutation PokemonDomeAfterDuel
