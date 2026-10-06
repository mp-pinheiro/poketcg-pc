"""Extended oracle-diff cases for main_menu, seeded from tests/cases/main_menu.py."""

CONTRACT = {
    'MainMenu_NewGame': {'compare': (), 'preserve': ()},
    'MainMenu_ContinueFromDiary': {'compare': (), 'preserve': ()},
    'MainMenu_ContinueDuel': {'compare': (), 'preserve': ()},
    '_GameLoop': {'compare': (), 'preserve': ()},
}

CASES = {
    'MainMenu_NewGame': [
        {   'oracle': False,
            'evidence': 'primary',
            'why': 'The bounded pre-ret contract stops immediately after the setup callee, before the '
                   'naming and portrait frame-driven screens; Func_c1b1 still establishes the new-game '
                   'overworld state.',
            'wram': {0xD0A8: b'\xff'},
            'read': {0xD0A8: 0x01},
            'expect': {0xD0A8: b'\x00'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': False,
            'evidence': 'primary',
            'why': 'The setup prefix must establish the new-game overworld state before the bounded '
                   'cutpoint even with poisoned entry registers.',
            'wram': {0xD0A8: b'\xff'},
            'read': {0xD0A8: 0x01},
            'expect': {0xD0A8: b'\x00'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'MainMenu_ContinueFromDiary': [
        {   'oracle': False,
            'evidence': 'primary',
            'why': 'The bounded prefix ends immediately after the routine stops the current song, '
                   'before backup validation and the downstream diary transition.',
            'wram': {0xD7A4: b'\x80'},
            'read': {0xD7A4: 0x01},
            'expect': {0xD7A4: b'\x00'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': False,
            'evidence': 'primary',
            'why': 'The song-stop prefix must write the stopped song ID even with poisoned entry '
                   'registers.',
            'wram': {0xD7A4: b'\x80'},
            'read': {0xD7A4: 0x01},
            'expect': {0xD7A4: b'\x00'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'MainMenu_ContinueDuel': [
        {   'evidence': 'primary',
            'why': 'The bounded prefix stops after the ported song stop and event clear, before the '
                   'unported save and event dispatch calls; PlaySong leaves the current song ID '
                   'stopped.',
            'wram': {0xD7A4: b'\x7f'},
            'read': {0xD7A4: 0x01},
            'expect': {0xD7A4: b'\x00'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'evidence': 'primary',
            'why': 'The bounded prefix still stops the song and clears events before the unported save '
                   'and event dispatch calls, regardless of poisoned entry registers.',
            'wram': {0xD7A4: b'\x7f'},
            'read': {0xD7A4: 0x01},
            'expect': {0xD7A4: b'\x00'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    '_GameLoop': [
        {   'oracle': False,
            'evidence': 'primary',
            'why': 'The bounded opening prefix clears object positions, advances the OAM-copy toggle, '
                   'and initializes the previous start-menu item before the non-returning title/menu '
                   'dispatch.',
            'wram': {0xCAC0: b'\x00', 0xD614: b'\x00'},
            'read': {0xCAC0: 0x01, 0xD614: 0x01},
            'expect': {0xCAC0: b'\x01', 0xD614: b'\xff'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': False,
            'evidence': 'primary',
            'why': 'The bounded opening prefix performs the same state initialization with poisoned '
                   'entry registers before the game-loop dispatch.',
            'wram': {0xCAC0: b'\xff', 0xD614: b'\x00'},
            'read': {0xCAC0: 0x01, 0xD614: 0x01},
            'expect': {0xCAC0: b'\x00', 0xD614: b'\xff'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
}

MUTATIONS = {
    'MainMenu_NewGame': {   'source_symbol': 'MainMenu_NewGame',
        'before': '\tFunc_c1b1();\n\tif (!frame_boundary_is_installed()) {',
        'after': '\t(void)0;\n\tif (!frame_boundary_is_installed()) {',
        'case_ids': ['MainMenu_NewGame-0', 'MainMenu_NewGame-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
    'MainMenu_ContinueFromDiary': {   'source_symbol': 'MainMenu_ContinueFromDiary',
        'before': 'uint8_t MainMenu_ContinueFromDiary(void)\n{\n\tPlaySong(MUSIC_STOP);',
        'after': 'uint8_t MainMenu_ContinueFromDiary(void)\n{\n\tPlaySong(MUSIC_CARD_POP);',
        'case_ids': ['MainMenu_ContinueFromDiary-0', 'MainMenu_ContinueFromDiary-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
    'MainMenu_ContinueDuel': {   'source_symbol': 'MainMenu_ContinueDuel',
        'before': 'uint8_t MainMenu_ContinueDuel(void)\n{\n\tPlaySong(MUSIC_STOP);',
        'after': 'uint8_t MainMenu_ContinueDuel(void)\n{\n\tPlaySong(0x01u);',
        'case_ids': ['MainMenu_ContinueDuel-0', 'MainMenu_ContinueDuel-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
    '_GameLoop': {   'source_symbol': '_GameLoop',
        'before': '\t\tZeroObjectPositions();\n'
                  '\t\twVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);',
        'after': '\t\tZeroObjectPositions();\n\t\twVBlankOAMCopyToggle = 0x7Fu;',
        'case_ids': ['_GameLoop-0', '_GameLoop-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
