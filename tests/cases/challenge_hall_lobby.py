POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wEventVars = 0xD3D2
wLoadedEventBits = 0xD3D1
wDefaultSong = 0xD111
EVENT_BYTE = wEventVars + 0x10
MUSIC_CHALLENGE_HALL = 0x0B


def event_vars(value):
    data = bytearray(64)
    data[0x10] = value
    return bytes(data)


CONTRACT = {
    "Preload_ChallengeHallNPCs2": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Preload_ChallengeHallNPCs2": [
        {"wram": {wEventVars: bytes(64), wDefaultSong: b"\x55"},
         "read": {wEventVars: 64, wLoadedEventBits: 1, wDefaultSong: 1}},
        dict(POISON,
             wram={wEventVars: event_vars(0), wDefaultSong: b"\x55"},
             read={wEventVars: 64, wLoadedEventBits: 1, wDefaultSong: 1}),
        {"wram": {wEventVars: event_vars(0x7F), wDefaultSong: b"\x55"},
         "read": {EVENT_BYTE: 1, wLoadedEventBits: 1, wDefaultSong: 1}},
        dict(POISON,
             wram={wEventVars: event_vars(0xFF), wDefaultSong: b"\x55"},
             read={EVENT_BYTE: 1, wLoadedEventBits: 1, wDefaultSong: 1}),
    ],
}

# >>> factory-cases-statics
TABLE_ADDR = 0xC500
def table_row(state, result, event, convo):
    return bytes([state, result, event, convo])
# <<< factory-cases-statics

# >>> factory SetRonaldChallengeHallLobbyState
CONTRACT["SetRonaldChallengeHallLobbyState"] = {"compare": ("a", "f", "hl"), "preserve": (), "wram_out": True}
CASES["SetRonaldChallengeHallLobbyState"] = [
    {"hl": TABLE_ADDR, "d": 0x00, "e": 0x01,
     "wram": {TABLE_ADDR: table_row(0x01, 0x00, 0x50, 0x01) + table_row(0x03, 0x03, 0x51, 0x02)
              + table_row(0x00, 0x00, 0x52, 0x03) + table_row(0x07, 0x00, 0x53, 0x04),
              0xD3E6: b"\x00", 0xD3E7: b"\x00"},
     "read": {0xD3E6: 1, 0xD3E7: 1}},
    dict(POISON, hl=TABLE_ADDR, d=0xFF, e=0xFF,
         wram={TABLE_ADDR: table_row(0x01, 0x00, 0x50, 0x01) + table_row(0x03, 0x03, 0x51, 0x02)
               + table_row(0x00, 0x00, 0x52, 0x03) + table_row(0x07, 0x00, 0x53, 0x04),
               0xD3E6: b"\x00", 0xD3E7: b"\x00"},
         read={0xD3E6: 1, 0xD3E7: 1}),
]
# <<< factory SetRonaldChallengeHallLobbyState

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Preload_ChallengeHallNPCs2": {
        "source_symbol": "Preload_ChallengeHallNPCs2",
        "before": "if ((event_byte & EVENT_CHALLENGE_CUP_STARTING_MASK) == 0)",
        "after": "if ((event_byte & EVENT_CHALLENGE_CUP_STARTING_MASK) != 0)",
        "case_ids": ["Preload_ChallengeHallNPCs2-0", "Preload_ChallengeHallNPCs2-1",
                     "Preload_ChallengeHallNPCs2-2", "Preload_ChallengeHallNPCs2-3"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation SetRonaldChallengeHallLobbyState
MUTATIONS["SetRonaldChallengeHallLobbyState"] = {"source_symbol": "SetRonaldChallengeHallLobbyState", "before": "if (a != e) {", "after": "if (a != d) {", "case_ids": ["SetRonaldChallengeHallLobbyState-0"]}
# <<< factory-mutation SetRonaldChallengeHallLobbyState
