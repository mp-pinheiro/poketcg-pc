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
