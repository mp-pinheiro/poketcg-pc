"""Oracle-diff cases for poketcg/src/engine/menus/print_stats.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DrawPauseMenuPlayerPortrait
CONTRACT["DrawPauseMenuPlayerPortrait"] = {"compare": (), "preserve": ()}
CASES["DrawPauseMenuPlayerPortrait"] = [
    {"wram": {0xD61E: b"\x00"}, "read": {0xD61E: 1}},
    dict(POISON, wram={0xD61E: b"\xFF"}, read={0xD61E: 1}),
]
# <<< factory DrawPauseMenuPlayerPortrait

# >>> factory-cases-statics
wWhichMedal = 0xD115
wMedalScreenYOffset = 0xD114
wMedalDisplayTimer = 0xD116
wCurTilemap = 0xD131
# <<< factory-cases-statics

# >>> factory FlashReceivedMedal
CONTRACT["FlashReceivedMedal"] = {"compare": (), "preserve": ()}
CASES["FlashReceivedMedal"] = [
    {"wram": {wWhichMedal: b"\x00", wMedalScreenYOffset: b"\x00", wMedalDisplayTimer: b"\x00", wCurTilemap: b"\x00"},
     "read": {0xD291: 1, wCurTilemap: 1}, "vread": {0: {0x9800: 32 * 18}}},
    {"wram": {wWhichMedal: b"\x02", wMedalScreenYOffset: b"\x00", wMedalDisplayTimer: b"\x10", wCurTilemap: b"\x00"},
     "read": {0xD291: 1, wCurTilemap: 1}, "vread": {0: {0x9800: 32 * 18}}},
    dict(POISON, wram={wWhichMedal: b"\x00", wMedalScreenYOffset: b"\x00", wMedalDisplayTimer: b"\x00", wCurTilemap: b"\x00"},
         read={0xD291: 1, wCurTilemap: 1}, vread={0: {0x9800: 32 * 18}}),
]
# <<< factory FlashReceivedMedal

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DrawPauseMenuPlayerPortrait
MUTATIONS["DrawPauseMenuPlayerPortrait"] = {
    "source_symbol": "DrawPauseMenuPlayerPortrait",
    "before": "\tDrawPlayerPortrait();",
    "after": "\t(void)0;",
    "case_ids": ["DrawPauseMenuPlayerPortrait-0", "DrawPauseMenuPlayerPortrait-1"],
}
# <<< factory-mutation DrawPauseMenuPlayerPortrait
# >>> factory-mutation FlashReceivedMedal
MUTATIONS["FlashReceivedMedal"] = {"source_symbol": "FlashReceivedMedal", "before": "\twCurTilemap = tilemap;", "after": "\twCurTilemap = 0u;", "case_ids": ["FlashReceivedMedal-0"]}
# <<< factory-mutation FlashReceivedMedal
