POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wActiveGameEvent = 0xD0C2
wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
wLoadNPCXPos = 0xD3AC
wd3d0 = 0xD3D0


def memory(event, x, y, npc_x=0x55, d3d0_value=0x66):
    return {wActiveGameEvent: bytes((event,)),
            wPlayerXCoord: bytes((x,)),
            wPlayerYCoord: bytes((y,)),
            wLoadNPCXPos: bytes((npc_x,)),
            wd3d0: bytes((d3d0_value,))}


CONTRACT = {
    "Preload_Amy": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Preload_Amy": [
        {"wram": memory(0, 0, 0),
         "read": {wActiveGameEvent: 1, wd3d0: 1}},
        dict(POISON,
             wram=memory(0xAA, 0xBB, 0xCC),
             read={wActiveGameEvent: 1, wd3d0: 1}),
        {"wram": memory(1, 0x13, 6),
         "read": {wActiveGameEvent: 1, wPlayerXCoord: 1, wd3d0: 1}},
        dict(POISON,
             wram=memory(1, 0x14, 5),
             read={wActiveGameEvent: 1, wPlayerXCoord: 1, wPlayerYCoord: 1,
                   wd3d0: 1}),
        {"wram": memory(1, 0x14, 6),
         "read": {wActiveGameEvent: 1, wPlayerXCoord: 1, wPlayerYCoord: 1,
                   wLoadNPCXPos: 1, wd3d0: 1}},
    ],
}

# >>> factory WaterClubMovePlayer
CONTRACT["WaterClubMovePlayer"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["WaterClubMovePlayer"] = [
    {"b": 0x12, "c": 0x34, "hl": 0x0000, "wram": {0xD331: b"\x09"}},
    dict(POISON, wram={0xD331: b"\x09"}),
    {"b": 0x56, "c": 0x78, "hl": 0x0000, "wram": {0xD331: b"\x08", 0xD3DD: b"\x20"}},
    {"b": 0x9A, "c": 0xBC, "hl": 0x1234, "wram": {0xD331: b"\x08", 0xD3DD: b"\x00"}},
]
# <<< factory WaterClubMovePlayer

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

# >>> factory WaterClubAfterDuel
CONTRACT["WaterClubAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["WaterClubAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x1f",
        wLoadedNPCs: b"\x1f" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x1f", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory WaterClubAfterDuel

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Preload_Amy": {
        "source_symbol": "Preload_Amy",
        "before": "if (event != 0)",
        "after": "if (event == 0)",
        "case_ids": ["Preload_Amy-0", "Preload_Amy-1", "Preload_Amy-2",
                      "Preload_Amy-3", "Preload_Amy-4"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation WaterClubMovePlayer
MUTATIONS["WaterClubMovePlayer"] = {"source_symbol": "WaterClubMovePlayer", "before": "\tif (y != 8u) {", "after": "\tif (y != 9u) {", "case_ids": ["WaterClubMovePlayer-0", "WaterClubMovePlayer-1"]}
# <<< factory-mutation WaterClubMovePlayer
# >>> factory-mutation WaterClubAfterDuel
MUTATIONS["WaterClubAfterDuel"] = {"source_symbol": "WaterClubAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(WaterClubAfterDuelTable + 1u));", "case_ids": ["WaterClubAfterDuel-0"]}
# <<< factory-mutation WaterClubAfterDuel
