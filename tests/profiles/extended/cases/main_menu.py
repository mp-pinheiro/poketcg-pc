"""Extended oracle-diff cases for main_menu: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('main_menu', remove=('MainMenu_CardPop',))
OWN = (
    'MainMenu_ContinueFromDiary',
    'MainMenu_NewGame',
    '_GameLoop',
)
CONTRACT.update({
    'MainMenu_NewGame': {'compare': (), 'preserve': ()},
    'MainMenu_ContinueFromDiary': {'compare': (), 'preserve': ()},
    '_GameLoop': {'compare': (), 'preserve': ()},
})
CASES.update({
    'MainMenu_NewGame': [
        {   'completion': {'mode': 'entry', 'pc': sym("DisplayPlayerNamingScreen"), 'bank': sym_bank("DisplayPlayerNamingScreen"), 'routine': 'DisplayPlayerNamingScreen'},
            'wram': {sym("wTempMap"): b'\xff'},
            'read': {sym("wTempMap"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("DisplayPlayerNamingScreen"), 'bank': sym_bank("DisplayPlayerNamingScreen"), 'routine': 'DisplayPlayerNamingScreen'},
            'wram': {sym("wTempMap"): b'\xff'},
            'read': {sym("wTempMap"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'MainMenu_ContinueFromDiary': [
        {   'completion': {'mode': 'entry', 'pc': sym("MainMenu_NewGame"), 'bank': sym_bank("MainMenu_NewGame"), 'routine': 'MainMenu_NewGame'},
            'wram': {sym("wCurSongID"): b'\x80'},
            'read': {sym("wCurSongID"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("MainMenu_NewGame"), 'bank': sym_bank("MainMenu_NewGame"), 'routine': 'MainMenu_NewGame'},
            'wram': {sym("wCurSongID"): b'\x80'},
            'read': {sym("wCurSongID"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    '_GameLoop': [
        {   'completion': {'mode': 'entry', 'pc': sym("HandleTitleScreen"), 'bank': sym_bank("HandleTitleScreen"), 'routine': 'HandleTitleScreen'},
            'wram': {sym("wVBlankOAMCopyToggle"): b'\x00', sym("wLastSelectedStartMenuItem"): b'\x00'},
            'read': {sym("wVBlankOAMCopyToggle"): 0x01, sym("wLastSelectedStartMenuItem"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("HandleTitleScreen"), 'bank': sym_bank("HandleTitleScreen"), 'routine': 'HandleTitleScreen'},
            'wram': {sym("wVBlankOAMCopyToggle"): b'\xff', sym("wLastSelectedStartMenuItem"): b'\x00'},
            'read': {sym("wVBlankOAMCopyToggle"): 0x01, sym("wLastSelectedStartMenuItem"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
})
MUTATIONS.update({
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
    '_GameLoop': {   'source_symbol': '_GameLoop',
        'before': '\t\tZeroObjectPositions();\n'
                  '\t\twVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);',
        'after': '\t\tZeroObjectPositions();\n\t\twVBlankOAMCopyToggle = 0x7Fu;',
        'case_ids': ['_GameLoop-0', '_GameLoop-1'],
        'source': 'src/profiles/extended/home/main_menu.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _record in SCHEMA2_CASES["MainMenu_ContinueDuel"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("MainMenu_ContinueDuel") + 9, "bank": sym_bank("MainMenu_ContinueDuel")}
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
