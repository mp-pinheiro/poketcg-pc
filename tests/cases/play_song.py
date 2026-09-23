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
        "before": "{\n\tPlaySong(a);",
        "after": "{\n\tPlaySong((uint8_t)(a + 1u));",
        "case_ids": ["ScriptPlaySong-0", "ScriptPlaySong-1", "ScriptPlaySong-2", "ScriptPlaySong-3"],
    },
}
for _rec in SCHEMA2_CASES["WaitForSongToFinish"]:
    _rec.setdefault("bus", {}).update({0xDD80: 0x165})
MUTATIONS["Func_3c87"] = {
    "source_symbol": "Func_3c87",
    "before": "\tPauseSong();",
    "after": "\t;",
    "case_ids": ["Func_3c87-0"],
}
for _rec in SCHEMA2_CASES["WaitForSongToFinish"]:
    _rec.setdefault("bus", {}).update({0xdff0: 1})
MUTATIONS["WaitForSongToFinish"] = {
    "source_symbol": "WaitForSongToFinish",
    "before": "void WaitForSongToFinish(void)\n{",
    "after": "void WaitForSongToFinish(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["WaitForSongToFinish-0"],
}
