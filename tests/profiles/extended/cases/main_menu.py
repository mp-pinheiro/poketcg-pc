"""Extended oracle-diff cases for main_menu, seeded from tests/cases/main_menu.py."""

CONTRACT = {
    'MainMenu_NewGame': {'compare': (), 'preserve': ()},
    'MainMenu_ContinueFromDiary': {'compare': (), 'preserve': ()},
    'MainMenu_ContinueDuel': {'compare': (), 'preserve': ()},
    '_GameLoop': {'compare': (), 'preserve': ()},
}

CASES = {
    'MainMenu_NewGame': [
        {   'completion': {'mode': 'entry', 'pc': 0x6752, 'bank': 0x04, 'routine': 'DisplayPlayerNamingScreen'},
            'wram': {0xD0A8: b'\xff'},
            'read': {0xD0A8: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': 0x6752, 'bank': 0x04, 'routine': 'DisplayPlayerNamingScreen'},
            'wram': {0xD0A8: b'\xff'},
            'read': {0xD0A8: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'MainMenu_ContinueFromDiary': [
        {   'completion': {'mode': 'entry', 'pc': 0x6699, 'bank': 0x04, 'routine': 'MainMenu_NewGame'},
            'wram': {0xD7A4: b'\x80'},
            'read': {0xD7A4: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': 0x6699, 'bank': 0x04, 'routine': 'MainMenu_NewGame'},
            'wram': {0xD7A4: b'\x80'},
            'read': {0xD7A4: 0x01},
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
        {   'completion': {'mode': 'entry', 'pc': 0x4F8D, 'bank': 0x07, 'routine': 'HandleTitleScreen'},
            'wram': {0xCAC0: b'\x00', 0xD614: b'\x00'},
            'read': {0xCAC0: 0x01, 0xD614: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': 0x4F8D, 'bank': 0x07, 'routine': 'HandleTitleScreen'},
            'wram': {0xCAC0: b'\xff', 0xD614: b'\x00'},
            'read': {0xCAC0: 0x01, 0xD614: 0x01},
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
        'source': 'src/home/main_menu.c'},
    '_GameLoop': {   'source_symbol': '_GameLoop',
        'before': '\t\tZeroObjectPositions();\n'
                  '\t\twVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);',
        'after': '\t\tZeroObjectPositions();\n\t\twVBlankOAMCopyToggle = 0x7Fu;',
        'case_ids': ['_GameLoop-0', '_GameLoop-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record in SCHEMA2_CASES["MainMenu_ContinueDuel"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x66FE, "bank": 4}
for _name, _entries in CASES.items():
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
