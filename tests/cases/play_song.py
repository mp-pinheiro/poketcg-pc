POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CUR_SONG_ID = 0xDD80
LCDC = 0xFF40

CONTRACT = {
    "ScriptPlaySong": {"compare": ("hl",), "preserve": ("hl",)},
    "Func_3c87": {"compare": (), "preserve": ()},
    "WaitForSongToFinish": {"compare": ("b", "c", "d", "e", "hl"),
                            "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "ScriptPlaySong": [
        {"a": 0, "read": {CUR_SONG_ID: 1}},
        {"a": 0x1D, "read": {CUR_SONG_ID: 1}},
        {"a": 0x1E, "read": {CUR_SONG_ID: 1}},
        dict(POISON, a=0x0F, read={CUR_SONG_ID: 1}),
    ],
    "Func_3c87": [
        {"a": 0xFF, "wram": {CUR_SONG_ID: b"\x80", LCDC: b"\x00"},
         "read": {CUR_SONG_ID: 1}},
        dict(POISON, a=0xFF,
             wram={CUR_SONG_ID: b"\x80", LCDC: b"\x00"},
             read={CUR_SONG_ID: 1}),
        {"a": 0x1F, "wram": {CUR_SONG_ID: b"\x80", LCDC: b"\x00"},
         "read": {CUR_SONG_ID: 1}},
    ],
    "WaitForSongToFinish": [
        {"wram": {CUR_SONG_ID: b"\x80", LCDC: b"\x00"},
         "read": {CUR_SONG_ID: 1}},
        dict(POISON, wram={CUR_SONG_ID: b"\x80", LCDC: b"\x00"},
             read={CUR_SONG_ID: 1}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "ScriptPlaySong": {
        "source_symbol": "ScriptPlaySong",
        "before": "\tPlaySong(a);",
        "after": "\tPlaySong((uint8_t)(a + 1u));",
        "case_ids": ["ScriptPlaySong-0", "ScriptPlaySong-1", "ScriptPlaySong-2", "ScriptPlaySong-3"],
    },
}
