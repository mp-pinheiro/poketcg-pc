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
# <<< factory-cases-statics

# >>> factory MainMenu_CardPop
CONTRACT["MainMenu_CardPop"] = {"compare": ("f",), "preserve": ()}
CASES["MainMenu_CardPop"] = [
    dict(oracle=False, evidence="primary", why="The Card Pop! scene is guarded by the seeded non-SGB console path; the routine still starts and then stops the card-pop song, leaving the song ID stopped.", wram=CARD_POP_WRAM, keys=[0x00, 0x01], setup=CARD_POP_SETUP, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=False, evidence="primary", why="The guarded Card Pop! path must stop its temporary music even with poisoned entry registers.", wram=CARD_POP_WRAM, keys=[0x00, 0x01], setup=CARD_POP_SETUP, read={wCurSongID: 1}, expect={wCurSongID: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MainMenu_CardPop

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation MainMenu_CardPop
MUTATIONS["MainMenu_CardPop"] = {"source_symbol": "MainMenu_CardPop", "before": "uint8_t MainMenu_CardPop(void)\n{\n\tPlaySong(MUSIC_CARD_POP);\n\tDoCardPop();\n\tWhiteOutDMGPals();\n\tDoFrameIfLCDEnabled();\n\tPlaySong(MUSIC_STOP);", "after": "uint8_t MainMenu_CardPop(void)\n{\n\tPlaySong(MUSIC_CARD_POP);\n\tDoCardPop();\n\tWhiteOutDMGPals();\n\tDoFrameIfLCDEnabled();\n\tPlaySong(MUSIC_CARD_POP);", "case_ids": ["MainMenu_CardPop-0", "MainMenu_CardPop-1"]}
# <<< factory-mutation MainMenu_CardPop
