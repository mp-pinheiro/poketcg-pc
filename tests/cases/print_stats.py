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

SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
wd291 = 0xD291
event_flags = 0xD3D2
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

# >>> factory ConvertWordToNumericalDigits
CONTRACT["ConvertWordToNumericalDigits"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["ConvertWordToNumericalDigits"] = [
    {"hl": 257, "wram": {0xD4B4: b"\x00\x00\x00"}, "expect": {0xD4B4: b"\x22\x25\x27"}},
    {"hl": 5, "wram": {0xD4B4: b"\x00\x00\x00"}, "expect": {0xD4B4: b"\x00\x00\x25"}},
    dict(POISON, hl=0x1234, wram={0xD4B4: b"\x00\x00\x00"}),
]
# <<< factory ConvertWordToNumericalDigits

# >>> factory PrintAlbumProgress_SkipGetProgress
CONTRACT["PrintAlbumProgress_SkipGetProgress"] = {"compare": (), "preserve": ()}
CASES["PrintAlbumProgress_SkipGetProgress"] = [
    {"b": 0, "c": 0, "d": 5, "e": 10, "read": {0xD4B4: 3}, "vread": {0: {0x9800: 3, 0x9804: 3}}},
    dict(POISON, read={0xD4B4: 3}, vread={0: {0x9800: 3}}),
]
# <<< factory PrintAlbumProgress_SkipGetProgress

# >>> factory PrintPlayTime_SkipUpdateTime
CONTRACT["PrintPlayTime_SkipUpdateTime"] = {"compare": (), "preserve": ()}
CASES["PrintPlayTime_SkipUpdateTime"] = [
    {"b": 0, "c": 0, "wram": {0xD3C8: b"\x1E\x05\x00"},
     "read": {0xD4B4: 3}, "vread": {0: {0x9800: 3, 0x9804: 2}}},
    dict(POISON, wram={0xD3C8: b"\x1E\x05\x00"},
         read={0xD4B4: 3}, vread={0: {0x9800: 3}}),
]
# <<< factory PrintPlayTime_SkipUpdateTime

# >>> factory PrintAlbumProgress
CONTRACT["PrintAlbumProgress"] = {"compare": (), "preserve": ()}
CASES["PrintAlbumProgress"] = [
    {"b": 0, "c": 0, "sram": {0: {0xA100: bytes(256)}}, "read": {0xD4B4: 3},
     "vread": {0: {0x9800: 3, 0x9804: 3}}},
    dict(POISON, sram={0: {0xA100: bytes(256)}}, read={0xD4B4: 3}),
]
# <<< factory PrintAlbumProgress

# >>> factory PrintPlayTime
CONTRACT["PrintPlayTime"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintPlayTime"] = [
    {"b": 0x02, "c": 0x02, "wram": {0xCAC7: b"\x1E", 0xCAC8: b"\x05", 0xCAC9: b"\x00"},
     "vread": {0: {0x9842: 5}}},
    dict(POISON, b=0x02, c=0x02, wram={0xCAC7: b"\x1E", 0xCAC8: b"\x05", 0xCAC9: b"\x00"},
         vread={0: {0x9842: 5}}),
]
# <<< factory PrintPlayTime

# >>> factory PrintMedalCount
CONTRACT["PrintMedalCount"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintMedalCount"] = [
    {"b": 0x02, "c": 0x02, "wram": {0xD3D1: bytes([0xFF] * 24), 0xD3D2: bytes([0xFF] * 24), 0xD3DC: b"\x20"},
     "vread": {0: {0x9842: 1}}},
    dict(POISON, b=0x02, c=0x02, wram={0xD3D1: bytes([0xFF] * 24), 0xD3D2: bytes([0xFF] * 24), 0xD3DC: b"\x20"},
         vread={0: {0x9842: 1}}),
]
# <<< factory PrintMedalCount

# >>> factory DrawCollectedMedals
CONTRACT["DrawCollectedMedals"] = {"compare": (), "preserve": ()}
CASES["DrawCollectedMedals"] = [
    {"wram": {event_flags: b"\x00", wMedalScreenYOffset: b"\x00", wCurTilemap: b"\x00", wd291: b"\x55"}, "setup": SETUP_TEXT, "read": {wd291: 1, wMedalScreenYOffset: 1, wCurTilemap: 1}},
    {"wram": {event_flags: b"\x00", wMedalScreenYOffset: b"\x03", wCurTilemap: b"\x77", wd291: b"\xAA"}, "setup": SETUP_TEXT, "read": {wd291: 1, wMedalScreenYOffset: 1, wCurTilemap: 1}},
    dict(POISON, wram={event_flags: b"\x00", wMedalScreenYOffset: b"\x05", wCurTilemap: b"\x99", wd291: b"\xCC"}, setup=SETUP_TEXT, read={wd291: 1, wMedalScreenYOffset: 1, wCurTilemap: 1}),
]
# <<< factory DrawCollectedMedals

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
# >>> factory-mutation ConvertWordToNumericalDigits
MUTATIONS["ConvertWordToNumericalDigits"] = {"source_symbol": "ConvertWordToNumericalDigits", "before": "uint8_t a = (uint8_t)((uint8_t)hl + SYM_0);", "after": "uint8_t a = (uint8_t)((uint8_t)hl + SYM_0 + 1u);", "case_ids": ["ConvertWordToNumericalDigits-0", "ConvertWordToNumericalDigits-1"]}
# <<< factory-mutation ConvertWordToNumericalDigits
# >>> factory-mutation PrintAlbumProgress_SkipGetProgress
MUTATIONS["PrintAlbumProgress_SkipGetProgress"] = {"source_symbol": "PrintAlbumProgress_SkipGetProgress", "before": "uint8_t b2 = (uint8_t)(b + 4u);", "after": "uint8_t b2 = (uint8_t)(b + 5u);", "case_ids": ["PrintAlbumProgress_SkipGetProgress-0"]}
# <<< factory-mutation PrintAlbumProgress_SkipGetProgress
# >>> factory-mutation PrintPlayTime_SkipUpdateTime
MUTATIONS["PrintPlayTime_SkipUpdateTime"] = {"source_symbol": "PrintPlayTime_SkipUpdateTime", "before": "uint16_t sum = (uint16_t)((uint16_t)minutes + 100u);", "after": "uint16_t sum = (uint16_t)((uint16_t)minutes + 99u);", "case_ids": ["PrintPlayTime_SkipUpdateTime-0"]}
# <<< factory-mutation PrintPlayTime_SkipUpdateTime
# >>> factory-mutation PrintAlbumProgress
MUTATIONS["PrintAlbumProgress"] = {"source_symbol": "PrintAlbumProgress", "before": "PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e);", "after": "PrintAlbumProgress_SkipGetProgress(b, c, (uint8_t)(prog.d + 1u), prog.e);", "case_ids": ["PrintAlbumProgress-0"]}
# <<< factory-mutation PrintAlbumProgress
# >>> factory-mutation PrintPlayTime
MUTATIONS["PrintPlayTime"] = {"source_symbol": "PrintPlayTime", "before": "gb_write8(wPlayTimeHourMinutes_ADDR, gb_read8((uint16_t)(wPlayTimeCounter_ADDR + 2u)));", "after": "gb_write8(wPlayTimeHourMinutes_ADDR, gb_read8((uint16_t)(wPlayTimeCounter_ADDR + 3u)));", "case_ids": ["PrintPlayTime-0", "PrintPlayTime-1"]}
# <<< factory-mutation PrintPlayTime
# >>> factory-mutation PrintMedalCount
MUTATIONS["PrintMedalCount"] = {"source_symbol": "PrintMedalCount", "before": "uint16_t src = (uint16_t)(wDecimalChars_ADDR + 2u);", "after": "uint16_t src = (uint16_t)(wDecimalChars_ADDR + 1u);", "case_ids": ["PrintMedalCount-0", "PrintMedalCount-1"]}
# <<< factory-mutation PrintMedalCount
# >>> factory-mutation DrawCollectedMedals
MUTATIONS["DrawCollectedMedals"] = {"source_symbol": "DrawCollectedMedals", "before": "void DrawCollectedMedals(void)\n{\n\twd291 = 0u;", "after": "void DrawCollectedMedals(void)\n{\n\twd291 = 1u;", "case_ids": ["DrawCollectedMedals-0"]}
# <<< factory-mutation DrawCollectedMedals
