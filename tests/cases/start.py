POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
WCONSOLE = 0xCAB4

CONTRACT = {
    "ShowCardPopCGBDisclaimer": {"compare": ("f",), "preserve": ()},
}

SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4,
              0xCD05: 2, 0xCD0A: 1, 0xFFAA: 2, 0xFFAD: 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES = {
    "ShowCardPopCGBDisclaimer": [
        {"wram": {WCONSOLE: b"\x02"}},
        {"wram": {WCONSOLE: b"\x00"}, "keys": 0x01,
         "setup": SETUP, "read": CACHE_READ, "vread": VRAM_READ},
        {"wram": {WCONSOLE: b"\x00"}, "keys": 0x02,
         "setup": SETUP, "read": CACHE_READ, "vread": VRAM_READ},
        dict(POISON, wram={WCONSOLE: b"\x00"}, keys=0x01,
             setup=SETUP, read=CACHE_READ, vread=VRAM_READ),
    ],
}

MUTATIONS = {
    "ShowCardPopCGBDisclaimer": {
        "source_symbol": "ShowCardPopCGBDisclaimer",
        "before": "if (wConsole == CONSOLE_CGB)",
        "after": "if (wConsole != CONSOLE_CGB)",
        "case_ids": [
            "ShowCardPopCGBDisclaimer-0",
            "ShowCardPopCGBDisclaimer-1",
            "ShowCardPopCGBDisclaimer-2",
            "ShowCardPopCGBDisclaimer-3",
        ],
    },
}

# >>> factory-cases-statics
def _header_for(payload):
    checksum = sum(payload) & 0xFFFF
    return bytes([0x08, 0x00, len(payload) & 0xFF, len(payload) >> 8,
                  checksum & 0xFF, checksum >> 8])

def _build_image(payload):
    return _header_for(payload) + b"\x00\x00" + payload

_VALID_PAYLOAD = bytes(179)
_VALID_IMAGE = _build_image(_VALID_PAYLOAD)
_INVALID_IMAGE = (bytes([0x08 ^ 0xFF, 0x00 ^ 0xFF]) + _header_for(_VALID_PAYLOAD)[2:]
                  + b"\x00\x00" + _VALID_PAYLOAD)

wCurHighlightedStartMenuItem = 0xD626
wCurMenuItem = 0xCD10
wHasSaveData = 0xD624
wCurOverworldMap = 0xD3CB
wMedalCount = 0xD3CC
wTotalNumCardsCollected = 0xD3CD
wTotalNumCardsToCollect = 0xD3CE
wTxRam2 = 0xCE3F
wTxRam3 = 0xCE43
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wHasDuelSaveData = 0xD625

wHasSaveData = 0xD624

wLastSelectedStartMenuItem = 0xD627
wCurSongID = 0xDD80
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory CheckIfHasSaveData
CONTRACT["CheckIfHasSaveData"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["CheckIfHasSaveData"] = [
    {"wram": {0xFF81: b"\x03"}, "ramg": True,
     "sram": {2: {0xB800: _VALID_IMAGE}, 0: {0xBC03: b"\x00", 0xBC00: b"\x00" * 0x100}},
     "read": {0xD624: 1, 0xD625: 1}},
    dict(POISON, wram={0xFF81: b"\x03"}, ramg=True,
         sram={2: {0xB800: _INVALID_IMAGE}},
         read={0xD624: 1, 0xD625: 1}),
    {"wram": {0xFF81: b"\x03"}, "ramg": True,
     "sram": {2: {0xB800: _INVALID_IMAGE}},
     "read": {0xD624: 1, 0xD625: 1}},
]
# <<< factory CheckIfHasSaveData

# >>> factory PrintStartMenuDescriptionText
CONTRACT["PrintStartMenuDescriptionText"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["PrintStartMenuDescriptionText"] = [
    {"wram": {wCurMenuItem: b"\x02", wCurHighlightedStartMenuItem: b"\x02", wHasSaveData: b"\x01"}},
    dict(POISON, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234,
         wram={wCurMenuItem: b"\x03", wCurHighlightedStartMenuItem: b"\x03", wHasSaveData: b"\x00"})
]
# <<< factory PrintStartMenuDescriptionText

# >>> factory AskToContinueFromDiaryWithDuelData
CONTRACT["AskToContinueFromDiaryWithDuelData"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AskToContinueFromDiaryWithDuelData"] = [
    {"wram": {0xD625: b"\x00"}, "read": {0xD625: 1}},
    dict(POISON, wram={0xD625: b"\x00"}, read={0xD625: 1}),
]
# <<< factory AskToContinueFromDiaryWithDuelData

# >>> factory HandleStartMenu
CONTRACT["HandleStartMenu"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HandleStartMenu"] = [
    {"wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF", 0xD624: b"\x00", 0xD625: b"\x00", 0xD627: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {0xCD08: 1, 0xD624: 1, 0xD625: 1, 0xD626: 1, 0xD627: 1, 0xD628: 1, 0xD636: 17, 0xFFB1: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF", 0xD624: b"\x00", 0xD625: b"\x00", 0xD627: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000, read={0xCD08: 1, 0xD624: 1, 0xD625: 1, 0xD626: 1, 0xD627: 1, 0xD628: 1, 0xD636: 17, 0xFFB1: 1}),
]
# <<< factory HandleStartMenu

# >>> factory DrawPlayerPortraitAndPrintNewGameText
CONTRACT["DrawPlayerPortraitAndPrintNewGameText"] = {"compare": (), "preserve": ()}
CASES["DrawPlayerPortraitAndPrintNewGameText"] = [
    {"wram": {0xCABB: b"\x00", 0xFF40: b"\x00", 0xD293: b"\xA5"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "instruction_budget": 60000000, "cycle_budget": 240000000,
     "read": {0xD293: 1}},
    dict(POISON, wram={0xCABB: b"\x00", 0xFF40: b"\x00", 0xD293: b"\x5A"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x01], instruction_budget=60000000, cycle_budget=240000000,
         read={0xD293: 1}),
]
# <<< factory DrawPlayerPortraitAndPrintNewGameText

# >>> factory DeleteSaveDataForNewGame
CONTRACT["DeleteSaveDataForNewGame"] = {"compare": (), "preserve": ()}
CASES["DeleteSaveDataForNewGame"] = [
    {"wram": {wHasSaveData: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={wHasSaveData: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=100000000),
    {"wram": {wHasSaveData: b"\x01", 0xCABB: b"\x00"}, "ramg": True, "sram": {2: {0xB800: b"\x00\x00"}}, "sread": {2: {0xB800: 2}}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={wHasSaveData: b"\x01", 0xCABB: b"\x00"}, ramg=True, sram={2: {0xB800: b"\x00\x00"}}, sread={2: {0xB800: 2}}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000)
]
# <<< factory DeleteSaveDataForNewGame

# >>> factory HandleTitleScreen
CONTRACT["HandleTitleScreen"] = {"compare": (), "preserve": ()}
CASES["HandleTitleScreen"] = [
    dict(oracle=False, evidence="primary", why="The bounded opening prefix stops before PlayIntroSequence's frame-driven intro, after stopping music and enabling sprite animations.", wram={wLastSelectedStartMenuItem: b"\x01", wCurSongID: b"\x7f"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=False, evidence="primary", why="The opening setup is independent of poisoned entry registers and still stops the current song before the intro call.", wram={wLastSelectedStartMenuItem: b"\x01", wCurSongID: b"\x7f"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory HandleTitleScreen

# >>> factory Start
CONTRACT["Start"] = {"compare": (), "preserve": ()}
CASES["Start"] = [
    dict(oracle=True, evidence="primary", why="The boot prefix initializes RAM, hardware, palettes, timer, serial state, DMA, and SRAM before the non-returning GameLoop jump; the initial byte and tile fill are asserted.", a=0x01, wram={0xCAB3: b"\xff", 0xCAB6: b"\xff"}, read={0xCAB3: 1, 0xCAB6: 1}, expect={0xCAB3: b"\x01", 0xCAB6: b"\x20"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=True, evidence="primary", why="The boot prefix must preserve the incoming A value in wInitialA and initialize the tile fill with poisoned entry registers before the non-returning GameLoop jump.", wram={0xCAB3: b"\xff", 0xCAB6: b"\xff"}, read={0xCAB3: 1, 0xCAB6: 1}, expect={0xCAB3: b"\xaa", 0xCAB6: b"\x20"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Start

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation CheckIfHasSaveData
MUTATIONS["CheckIfHasSaveData"] = {"source_symbol": "CheckIfHasSaveData", "before": "\tuint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;", "after": "\tuint8_t has_save = (first.f & 0x10u) ? FALSE : TRUE;", "case_ids": ["CheckIfHasSaveData-0", "CheckIfHasSaveData-2"]}
# <<< factory-mutation CheckIfHasSaveData
# >>> factory-mutation PrintStartMenuDescriptionText
MUTATIONS["PrintStartMenuDescriptionText"] = {"source_symbol": "PrintStartMenuDescriptionText", "before": "\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;", "after": "\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0x80u : f;", "case_ids": ["PrintStartMenuDescriptionText-0", "PrintStartMenuDescriptionText-1"]}
# <<< factory-mutation PrintStartMenuDescriptionText
# >>> factory-mutation AskToContinueFromDiaryWithDuelData
MUTATIONS["AskToContinueFromDiaryWithDuelData"] = {"source_symbol": "AskToContinueFromDiaryWithDuelData", "before": "\t\treturn (AskToContinueFromDiaryWithDuelDataResult){a, 0x80u};", "after": "\t\treturn (AskToContinueFromDiaryWithDuelDataResult){0xFFu, 0x80u};", "case_ids": ["AskToContinueFromDiaryWithDuelData-0", "AskToContinueFromDiaryWithDuelData-1"]}
# <<< factory-mutation AskToContinueFromDiaryWithDuelData
# >>> factory-mutation HandleStartMenu
MUTATIONS["HandleStartMenu"] = {"source_symbol": "HandleStartMenu", "before": "\t\twLastSelectedStartMenuItem = hCurMenuItem;", "after": "\t\twLastSelectedStartMenuItem = (uint8_t)(hCurMenuItem ^ 1u);", "case_ids": ["HandleStartMenu-0", "HandleStartMenu-1"]}
# <<< factory-mutation HandleStartMenu
# >>> factory-mutation DrawPlayerPortraitAndPrintNewGameText
MUTATIONS["DrawPlayerPortraitAndPrintNewGameText"] = {"source_symbol": "DrawPlayerPortraitAndPrintNewGameText", "before": "\tLoadConsolePaletteData();", "after": "\t(void)0;", "case_ids": ["DrawPlayerPortraitAndPrintNewGameText-0", "DrawPlayerPortraitAndPrintNewGameText-1"]}
# <<< factory-mutation DrawPlayerPortraitAndPrintNewGameText
# >>> factory-mutation DeleteSaveDataForNewGame
MUTATIONS["DeleteSaveDataForNewGame"] = {"source_symbol": "DeleteSaveDataForNewGame", "before": "uint8_t DeleteSaveDataForNewGame(void)\n{\n\tif (wHasSaveData == 0u)\n", "after": "uint8_t DeleteSaveDataForNewGame(void)\n{\n\tif (wHasSaveData != 0u)\n", "case_ids": ["DeleteSaveDataForNewGame-2"]}
# <<< factory-mutation DeleteSaveDataForNewGame
# >>> factory-mutation HandleTitleScreen
MUTATIONS["HandleTitleScreen"] = {"source_symbol": "HandleTitleScreen", "before": "\t\tPlaySong(MUSIC_STOP);\n\t\tEnableAndClearSpriteAnimations();\n\t\treturn;", "after": "\t\tPlaySong(0x01u);\n\t\tEnableAndClearSpriteAnimations();\n\t\treturn;", "case_ids": ["HandleTitleScreen-0", "HandleTitleScreen-1"]}
# <<< factory-mutation HandleTitleScreen
# >>> factory-completion HandleTitleScreen
for _record in SCHEMA2_CASES["HandleTitleScreen"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x5086, "bank": 7}
# <<< factory-completion HandleTitleScreen
# >>> factory-mutation Start
MUTATIONS["Start"] = {"source_symbol": "Start", "before": "wInitialA = a;", "after": "wInitialA = 0xFFu;", "case_ids": ["Start-0", "Start-1"]}
# <<< factory-mutation Start
# >>> factory-completion Start
for _record in SCHEMA2_CASES["Start"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x03B8}
# <<< factory-completion Start
