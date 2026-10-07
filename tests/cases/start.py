from tests.cases._symbols import sym, sym_bank
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
WCONSOLE = sym("wConsole")

CONTRACT = {
    "ShowCardPopCGBDisclaimer": {"compare": ("f",), "preserve": ()},
}

SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {sym("wc600") + 0x20: 4, sym("wc700") + 0x20: 4, sym("wc800") + 0x20: 4, sym("wc900") + 0x20: 4,
              sym("wCurTextTile"): 2, sym("wFontWidth"): 1, sym("hTextBGMap0Address"): 2, sym("hTextHorizontalAlign"): 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES = {
    # start.asm:399 waits on WaitForButtonAorB, whose RefreshMenuCursor
    # increments wCursorBlinkCounter every frame (menus.asm:173-176). Observing
    # that byte is what distinguishes running the wait from skipping it; the
    # cache and VRAM spans alone do not.
    "ShowCardPopCGBDisclaimer": [
        {"wram": {WCONSOLE: b"\x00", sym("wCursorBlinkCounter"): b"\x00"}, "keys": 0x01,
         "setup": SETUP, "read": {**CACHE_READ, sym("wCursorBlinkCounter"): 1}, "vread": VRAM_READ},
        {"wram": {WCONSOLE: b"\x00", sym("wCursorBlinkCounter"): b"\x00"}, "keys": 0x02,
         "setup": SETUP, "read": {**CACHE_READ, sym("wCursorBlinkCounter"): 1}, "vread": VRAM_READ},
        dict(POISON, wram={WCONSOLE: b"\x00", sym("wCursorBlinkCounter"): b"\x00"}, keys=0x01,
             setup=SETUP, read={**CACHE_READ, sym("wCursorBlinkCounter"): 1}, vread=VRAM_READ),
        {"wram": {WCONSOLE: b"\x02"}},
    ],
}

MUTATIONS = {
    "ShowCardPopCGBDisclaimer": {
        "source_symbol": "ShowCardPopCGBDisclaimer",
        "before": "uint16_t box = 0;\n\tif (wConsole == CONSOLE_CGB)",
        "after": "uint16_t box = 0;\n\tif (wConsole != CONSOLE_CGB)",
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

wCurHighlightedStartMenuItem = sym("wCurHighlightedStartMenuItem")
wCurMenuItem = sym("wCurMenuItem")
wHasSaveData = sym("wHasSaveData")
wCurOverworldMap = sym("wCurOverworldMap")
wMedalCount = sym("wMedalCount")
wTotalNumCardsCollected = sym("wTotalNumCardsCollected")
wTotalNumCardsToCollect = sym("wTotalNumCardsToCollect")
wTxRam2 = sym("wTxRam2")
wTxRam3 = sym("wTxRam3")
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]


wHasSaveData = sym("wHasSaveData")

wLastSelectedStartMenuItem = sym("wLastSelectedStartMenuItem")
wCurSongID = sym("wCurSongID")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory CheckIfHasSaveData
CONTRACT["CheckIfHasSaveData"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["CheckIfHasSaveData"] = [
    {"wram": {sym("hBankSRAM"): b"\x03"}, "ramg": True,
     "sram": {2: {sym("sBackupGeneralSaveData"): _VALID_IMAGE}, 0: {sym("sCurrentDuelType"): b"\x00", sym("sCurrentDuel"): b"\x00" * 0x100}},
     "read": {sym("wHasSaveData"): 1, sym("wHasDuelSaveData"): 1}},
    dict(POISON, wram={sym("hBankSRAM"): b"\x03"}, ramg=True,
         sram={2: {sym("sBackupGeneralSaveData"): _INVALID_IMAGE}},
         read={sym("wHasSaveData"): 1, sym("wHasDuelSaveData"): 1}),
    {"wram": {sym("hBankSRAM"): b"\x03"}, "ramg": True,
     "sram": {2: {sym("sBackupGeneralSaveData"): _INVALID_IMAGE}},
     "read": {sym("wHasSaveData"): 1, sym("wHasDuelSaveData"): 1}},
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
    {"wram": {sym("wHasDuelSaveData"): b"\x00"}, "read": {sym("wHasDuelSaveData"): 1}},
    dict(POISON, wram={sym("wHasDuelSaveData"): b"\x00"}, read={sym("wHasDuelSaveData"): 1}),
]
# <<< factory AskToContinueFromDiaryWithDuelData

# >>> factory HandleStartMenu
CONTRACT["HandleStartMenu"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HandleStartMenu"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x00", sym("wDuelTempList"): b"\xFF", sym("wHasSaveData"): b"\x00", sym("wHasDuelSaveData"): b"\x00", sym("wLastSelectedStartMenuItem"): b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {sym("wLineSeparation"): 1, sym("wHasSaveData"): 1, sym("wHasDuelSaveData"): 1, sym("wCurHighlightedStartMenuItem"): 1, sym("wLastSelectedStartMenuItem"): 1, sym("wStartMenuChoice"): 1, sym("wStartMenuParams"): 17, sym("hCurMenuItem"): 1}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x00", sym("wDuelTempList"): b"\xFF", sym("wHasSaveData"): b"\x00", sym("wHasDuelSaveData"): b"\x00", sym("wLastSelectedStartMenuItem"): b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000, read={sym("wLineSeparation"): 1, sym("wHasSaveData"): 1, sym("wHasDuelSaveData"): 1, sym("wCurHighlightedStartMenuItem"): 1, sym("wLastSelectedStartMenuItem"): 1, sym("wStartMenuChoice"): 1, sym("wStartMenuParams"): 17, sym("hCurMenuItem"): 1}),
]
# <<< factory HandleStartMenu

# >>> factory DrawPlayerPortraitAndPrintNewGameText
CONTRACT["DrawPlayerPortraitAndPrintNewGameText"] = {"compare": (), "preserve": ()}
CASES["DrawPlayerPortraitAndPrintNewGameText"] = [
    {"wram": {sym("wLCDC"): b"\x00", 0xFF40: b"\x00", sym("wConsolePaletteData"): b"\xA5"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "instruction_budget": 60000000, "cycle_budget": 240000000,
     "read": {sym("wConsolePaletteData"): 1}},
    dict(POISON, wram={sym("wLCDC"): b"\x00", 0xFF40: b"\x00", sym("wConsolePaletteData"): b"\x5A"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x01], instruction_budget=60000000, cycle_budget=240000000,
         read={sym("wConsolePaletteData"): 1}),
]
# <<< factory DrawPlayerPortraitAndPrintNewGameText

# >>> factory DeleteSaveDataForNewGame
CONTRACT["DeleteSaveDataForNewGame"] = {"compare": (), "preserve": ()}
CASES["DeleteSaveDataForNewGame"] = [
    {"wram": {wHasSaveData: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={wHasSaveData: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=100000000),
    {"wram": {wHasSaveData: b"\x01", sym("wLCDC"): b"\x00"}, "ramg": True, "sram": {2: {sym("sBackupGeneralSaveData"): b"\x00\x00"}}, "sread": {2: {sym("sBackupGeneralSaveData"): 2}}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={wHasSaveData: b"\x01", sym("wLCDC"): b"\x00"}, ramg=True, sram={2: {sym("sBackupGeneralSaveData"): b"\x00\x00"}}, sread={2: {sym("sBackupGeneralSaveData"): 2}}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000)
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
    dict(oracle=True, evidence="primary", why="The boot prefix initializes RAM, hardware, palettes, timer, serial state, DMA, and SRAM before the non-returning GameLoop jump; the initial byte and tile fill are asserted.", a=0x01, wram={sym("wInitialA"): b"\xff", sym("wTileMapFill"): b"\xff"}, read={sym("wInitialA"): 1, sym("wTileMapFill"): 1}, expect={sym("wInitialA"): b"\x01", sym("wTileMapFill"): b"\x20"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=True, evidence="primary", why="The boot prefix must preserve the incoming A value in wInitialA and initialize the tile fill with poisoned entry registers before the non-returning GameLoop jump.", wram={sym("wInitialA"): b"\xff", sym("wTileMapFill"): b"\xff"}, read={sym("wInitialA"): 1, sym("wTileMapFill"): 1}, expect={sym("wInitialA"): b"\xaa", sym("wTileMapFill"): b"\x20"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Start

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation CheckIfHasSaveData
MUTATIONS["CheckIfHasSaveData"] = {"source_symbol": "CheckIfHasSaveData", "before": "\tuint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;", "after": "\tuint8_t has_save = (first.f & 0x10u) ? FALSE : TRUE;", "case_ids": ["CheckIfHasSaveData-0", "CheckIfHasSaveData-2"]}
# <<< factory-mutation CheckIfHasSaveData
# >>> factory-mutation PrintStartMenuDescriptionText
MUTATIONS["PrintStartMenuDescriptionText"] = {"source_symbol": "PrintStartMenuDescriptionText", "before": "\n\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;", "after": "\n\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0x80u : f;", "case_ids": ["PrintStartMenuDescriptionText-0", "PrintStartMenuDescriptionText-1"]}
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
    _record["completion"] = {"mode": "pre-ret", "pc": sym("HandleTitleScreen.play_opening") + 8, "bank": sym_bank("HandleTitleScreen.play_opening")}
# <<< factory-completion HandleTitleScreen
# >>> factory-mutation Start
MUTATIONS["Start"] = {"source_symbol": "Start", "before": "wInitialA = a;", "after": "wInitialA = 0xFFu;", "case_ids": ["Start-0", "Start-1"]}
# <<< factory-mutation Start
# >>> factory-completion Start
for _record in SCHEMA2_CASES["Start"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("SetupVRAM.loop")}
# <<< factory-completion Start
