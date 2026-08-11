POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

W_CONSOLE = 0xCAB4
W_DEFAULT_SONG = 0xD111
W_CUR_TILEMAP = 0xD131
W_CUR_MAP_SGB_PALS = 0xD132
W_CUR_MAP_INITIAL_PALETTE = 0xD28F
W_CUR_MAP_PALETTE = 0xD290
W_CUR_MAP = 0xD32F

CONTRACT = {
    "LoadMapHeader": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "LoadMapHeader": [
        {"wram": {
            W_CONSOLE: b"\x00",
            W_CUR_MAP: b"\x00",
            W_CUR_TILEMAP: b"\x00",
            W_CUR_MAP_SGB_PALS: b"\x00",
            W_CUR_MAP_INITIAL_PALETTE: b"\x00",
            W_CUR_MAP_PALETTE: b"\x00",
            W_DEFAULT_SONG: b"\x00",
        }},
        dict(POISON, wram={
            W_CONSOLE: b"\x00",
            W_CUR_MAP: b"\x01",
            W_CUR_TILEMAP: b"\xAA",
            W_CUR_MAP_SGB_PALS: b"\xAA",
            W_CUR_MAP_INITIAL_PALETTE: b"\xAA",
            W_CUR_MAP_PALETTE: b"\xAA",
            W_DEFAULT_SONG: b"\xAA",
        }),
        {"wram": {
            W_CONSOLE: b"\x02",
            W_CUR_MAP: b"\x00",
            W_CUR_TILEMAP: b"\xAA",
            W_CUR_MAP_SGB_PALS: b"\xAA",
            W_CUR_MAP_INITIAL_PALETTE: b"\xAA",
            W_CUR_MAP_PALETTE: b"\xAA",
            W_DEFAULT_SONG: b"\xAA",
        }},
        dict(POISON, wram={
            W_CONSOLE: b"\x02",
            W_CUR_MAP: b"\x23",
            W_CUR_TILEMAP: b"\xAA",
            W_CUR_MAP_SGB_PALS: b"\xAA",
            W_CUR_MAP_INITIAL_PALETTE: b"\xAA",
            W_CUR_MAP_PALETTE: b"\xAA",
            W_DEFAULT_SONG: b"\xAA",
        }),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "LoadMapHeader": {
        "source_symbol": "LoadMapHeader",
        "before": "cgb_tilemap != 0",
        "after": "cgb_tilemap == 0",
        "case_ids": ["LoadMapHeader-0", "LoadMapHeader-1", "LoadMapHeader-2", "LoadMapHeader-3"],
    },
}
