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

# >>> factory PokemonDomeLoadMap
CONTRACT["PokemonDomeLoadMap"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PokemonDomeLoadMap"] = [
    {"wram": {wEventVarByte_A: b"\x00", wPCPacks_A: bytes(15)},
     "read": {wPCPacks_A: 15, wNextScript_A: 2}},
    dict(POISON, wram={wEventVarByte_A: b"\x08", wPCPacks_A: bytes(15)},
         read={wPCPacks_A: 15, wNextScript_A: 2}),
]
# <<< factory PokemonDomeLoadMap

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Func_f762": {
        "source_symbol": "Func_f762",
        "before": "gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 2u",
        "after": "gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 3u",
        "case_ids": ["Func_f762-0", "Func_f762-1", "Func_f762-2",
                     "Func_f762-3", "Func_f762-4"],
    },
    "Func_f782": {
        "source_symbol": "Func_f782",
        "before": "gb_write8(W_LOAD_NPC_X_POS_ADDR, b)",
        "after": "gb_write8(W_LOAD_NPC_X_POS_ADDR, c)",
        "case_ids": ["Func_f782-0", "Func_f782-1", "Func_f782-2", "Func_f782-3"],
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
# >>> factory-mutation PokemonDomeLoadMap
MUTATIONS["PokemonDomeLoadMap"] = {"source_symbol": "PokemonDomeLoadMap", "before": "\tSetNextScript(0x780Bu);", "after": "\tSetNextScript(0x780Cu);", "case_ids": ["PokemonDomeLoadMap-1"]}
# <<< factory-mutation PokemonDomeLoadMap
