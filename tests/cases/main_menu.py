"""Oracle-diff cases for poketcg/src/engine/menus/main_menu.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
wLCDC = 0xCABB
wCurSongID = 0xDD80
CARD_POP_WRAM = {wConsole: b"\x01", wLCDC: b"\x00", wCurSongID: b"\x80"}
CARD_POP_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]

wTempMap = 0xD0BB

wCurSongID = 0xDD80

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wVBlankOAMCopyToggle = 0xCAC0
wLastSelectedStartMenuItem = 0xD627
# <<< factory-cases-statics

# >>> factory MainMenu_CardPop
CONTRACT["MainMenu_CardPop"] = {"compare": ("f",), "preserve": ()}
CASES["MainMenu_CardPop"] = [
    dict(oracle=False, evidence="primary", why="The Card Pop! scene is guarded by the seeded non-SGB console path; the routine still starts and then stops the card-pop song, leaving the song ID stopped.", wram=CARD_POP_WRAM, keys=[0x00, 0x01], setup=CARD_POP_SETUP, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=False, evidence="primary", why="The guarded Card Pop! path must stop its temporary music even with poisoned entry registers.", wram=CARD_POP_WRAM, keys=[0x00, 0x01], setup=CARD_POP_SETUP, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MainMenu_CardPop

# >>> factory MainMenu_NewGame
CONTRACT["MainMenu_NewGame"] = {"compare": (), "preserve": ()}
CASES["MainMenu_NewGame"] = [
    dict(oracle=False, evidence="primary", why="The bounded pre-ret contract stops immediately after the setup callee, before the naming and portrait frame-driven screens; Func_c1b1 still establishes the new-game overworld state.", wram={wTempMap: b"\xFF"}, read={wTempMap: 1}, expect={wTempMap: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=False, evidence="primary", why="The setup prefix must establish the new-game overworld state before the bounded cutpoint even with poisoned entry registers.", wram={wTempMap: b"\xFF"}, read={wTempMap: 1}, expect={wTempMap: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory MainMenu_NewGame

# >>> factory MainMenu_ContinueFromDiary
CONTRACT["MainMenu_ContinueFromDiary"] = {"compare": (), "preserve": ()}
CASES["MainMenu_ContinueFromDiary"] = [
    dict(oracle=False, evidence="primary", why="The bounded prefix ends immediately after the routine stops the current song, before backup validation and the downstream diary transition.", wram={wCurSongID: b"\x80"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=False, evidence="primary", why="The song-stop prefix must write the stopped song ID even with poisoned entry registers.", wram={wCurSongID: b"\x80"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory MainMenu_ContinueFromDiary

# >>> factory MainMenu_ContinueDuel
CONTRACT["MainMenu_ContinueDuel"] = {"compare": (), "preserve": ()}
CASES["MainMenu_ContinueDuel"] = [
    dict(evidence="primary", why="The bounded prefix stops after the ported song stop and event clear, before the unported save and event dispatch calls; PlaySong leaves the current song ID stopped.", wram={wCurSongID: b"\x7f"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, evidence="primary", why="The bounded prefix still stops the song and clears events before the unported save and event dispatch calls, regardless of poisoned entry registers.", wram={wCurSongID: b"\x7f"}, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MainMenu_ContinueDuel

# >>> factory _GameLoop
CONTRACT["_GameLoop"] = {"compare": (), "preserve": ()}
CASES["_GameLoop"] = [
    dict(oracle=False, evidence="primary", why="The bounded opening prefix clears object positions, advances the OAM-copy toggle, and initializes the previous start-menu item before the non-returning title/menu dispatch.", wram={wVBlankOAMCopyToggle: b"\x00", wLastSelectedStartMenuItem: b"\x00"}, read={wVBlankOAMCopyToggle: 1, wLastSelectedStartMenuItem: 1}, expect={wVBlankOAMCopyToggle: b"\x01", wLastSelectedStartMenuItem: b"\xff"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=False, evidence="primary", why="The bounded opening prefix performs the same state initialization with poisoned entry registers before the game-loop dispatch.", wram={wVBlankOAMCopyToggle: b"\xff", wLastSelectedStartMenuItem: b"\x00"}, read={wVBlankOAMCopyToggle: 1, wLastSelectedStartMenuItem: 1}, expect={wVBlankOAMCopyToggle: b"\x00", wLastSelectedStartMenuItem: b"\xff"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory _GameLoop

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation MainMenu_CardPop
MUTATIONS["MainMenu_CardPop"] = {"source_symbol": "MainMenu_CardPop", "before": "uint8_t MainMenu_CardPop(void)\n{\n\tPlaySong(MUSIC_CARD_POP);\n\tDoCardPop();\n\tWhiteOutDMGPals();\n\tDoFrameIfLCDEnabled();\n\tPlaySong(MUSIC_STOP);", "after": "uint8_t MainMenu_CardPop(void)\n{\n\tPlaySong(MUSIC_CARD_POP);\n\tDoCardPop();\n\tWhiteOutDMGPals();\n\tDoFrameIfLCDEnabled();\n\tPlaySong(MUSIC_CARD_POP);", "case_ids": ["MainMenu_CardPop-0", "MainMenu_CardPop-1"]}
# <<< factory-mutation MainMenu_CardPop
# >>> factory-mutation MainMenu_NewGame
MUTATIONS["MainMenu_NewGame"] = {"source_symbol": "MainMenu_NewGame", "before": "void MainMenu_NewGame(void)\n{\n\tFunc_c1b1();", "after": "void MainMenu_NewGame(void)\n{\n\t(void)0;", "case_ids": ["MainMenu_NewGame-0", "MainMenu_NewGame-1"]}
# <<< factory-mutation MainMenu_NewGame
# >>> factory-completion MainMenu_NewGame
for _record in SCHEMA2_CASES["MainMenu_NewGame"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6708, "bank": 4}
# <<< factory-completion MainMenu_NewGame
# >>> factory-mutation MainMenu_ContinueFromDiary
MUTATIONS["MainMenu_ContinueFromDiary"] = {"source_symbol": "MainMenu_ContinueFromDiary", "before": "void MainMenu_ContinueFromDiary(void)\n{\n\tPlaySong(MUSIC_STOP);", "after": "void MainMenu_ContinueFromDiary(void)\n{\n\tPlaySong(MUSIC_CARD_POP);", "case_ids": ["MainMenu_ContinueFromDiary-0", "MainMenu_ContinueFromDiary-1"]}
# <<< factory-mutation MainMenu_ContinueFromDiary
# >>> factory-completion MainMenu_ContinueFromDiary
for _record in SCHEMA2_CASES["MainMenu_ContinueFromDiary"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6746, "bank": 4}
# <<< factory-completion MainMenu_ContinueFromDiary
# >>> factory-mutation MainMenu_ContinueDuel
MUTATIONS["MainMenu_ContinueDuel"] = {"source_symbol": "MainMenu_ContinueDuel", "before": "void MainMenu_ContinueDuel(void)\n{\n\tPlaySong(MUSIC_STOP);", "after": "void MainMenu_ContinueDuel(void)\n{\n\tPlaySong(0x01u);", "case_ids": ["MainMenu_ContinueDuel-0", "MainMenu_ContinueDuel-1"]}
# <<< factory-mutation MainMenu_ContinueDuel
# >>> factory-completion MainMenu_ContinueDuel
# MainMenu_ContinueDuel reaches the unported LoadGeneralSaveData farcall after PlaySong and ClearEvents.
for _record in SCHEMA2_CASES["MainMenu_ContinueDuel"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6787, "bank": 4}
# <<< factory-completion MainMenu_ContinueDuel
# >>> factory-mutation _GameLoop
MUTATIONS["_GameLoop"] = {"source_symbol": "_GameLoop", "before": "void _GameLoop(void)\n{\n\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);\n\t/* SetIntroSGBBorder is scope-excluded; stop before the main-menu dispatch. */\n\twLastSelectedStartMenuItem = 0xFFu;", "after": "void _GameLoop(void)\n{\n\tZeroObjectPositions();\n\twVBlankOAMCopyToggle = 0x7Fu;\n\t/* SetIntroSGBBorder is scope-excluded; stop before the main-menu dispatch. */\n\twLastSelectedStartMenuItem = 0xFFu;", "case_ids": ["_GameLoop-0", "_GameLoop-1"]}
# <<< factory-mutation _GameLoop
# >>> factory-completion _GameLoop
for _record in SCHEMA2_CASES["_GameLoop"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x66E1, "bank": 4}
# <<< factory-completion _GameLoop
