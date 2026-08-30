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
