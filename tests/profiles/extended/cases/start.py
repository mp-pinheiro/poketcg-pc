"""Extended oracle-diff cases for start: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import VRAM_START, sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('start', remove=(
    'CheckIfHasSaveData',
    'DrawPlayerPortraitAndPrintNewGameText',
    'ShowCardPopCGBDisclaimer',
))
OWN = (
    'CheckIfHasSaveData',
    'DrawPlayerPortraitAndPrintNewGameText',
    'HandleTitleScreen',
    'Start',
)
CONTRACT.update({
    'CheckIfHasSaveData': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'DrawPlayerPortraitAndPrintNewGameText': {'compare': (), 'preserve': ()},
    'HandleTitleScreen': {'compare': (), 'preserve': ()},
    'Start': {'compare': (), 'preserve': ()},
})
CASES.update({
    'CheckIfHasSaveData': [
        {   'wram': {sym("hBankSRAM"): b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   sym("sBackupGeneralSaveData"): b'\x08\x00\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00'},
                        0x00: {   sym("sChallengeMachineEnd") + 0x19A: b'\x00',
                                  sym("sChallengeMachineEnd") + 0x197: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'read': {sym("wHasSaveData"): 0x01, sym("wHasDuelSaveData"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankSRAM"): b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   sym("sBackupGeneralSaveData"): b'\xf7\xff\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {sym("wHasSaveData"): 0x01, sym("wHasDuelSaveData"): 0x01}},
        {   'wram': {sym("hBankSRAM"): b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   sym("sBackupGeneralSaveData"): b'\xf7\xff\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {sym("wHasSaveData"): 0x01, sym("wHasDuelSaveData"): 0x01}},
    ],
    'DrawPlayerPortraitAndPrintNewGameText': [
        {   'wram': {sym("wLCDC"): b'\x00', 0xFF40: b'\x00', sym("wWriteBGMapToSRAM") + 1: b'\xa5'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00,
            'read': {sym("wWriteBGMapToSRAM") + 1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wLCDC"): b'\x00', 0xFF40: b'\x00', sym("wWriteBGMapToSRAM") + 1: b'Z'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00,
            'read': {sym("wWriteBGMapToSRAM") + 1: 0x01}},
    ],
    'HandleTitleScreen': [
        {   'completion': {'mode': 'entry', 'pc': sym("PlayIntroSequence"), 'bank': sym_bank("PlayIntroSequence"), 'routine': 'PlayIntroSequence'},
            'wram': {sym("wLastSelectedStartMenuItem"): b'\x01', sym("wCurSongID"): b'\x7f'},
            'read': {sym("wCurSongID"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("PlayIntroSequence"), 'bank': sym_bank("PlayIntroSequence"), 'routine': 'PlayIntroSequence'},
            'wram': {sym("wLastSelectedStartMenuItem"): b'\x01', sym("wCurSongID"): b'\x7f'},
            'read': {sym("wCurSongID"): 0x01}},
    ],
    'Start': [
        {   'a': 0x01,
            'completion': {'mode': 'entry', 'pc': sym("GameLoop"), 'bank': sym_bank("GameLoop"), 'routine': 'GameLoop'},
            'wram': {sym("wInitialA"): b'\xff', sym("wTileMapFill"): b'\xff'},
            'read': {sym("wInitialA"): 0x01, sym("wTileMapFill"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("GameLoop"), 'bank': sym_bank("GameLoop"), 'routine': 'GameLoop'},
            'wram': {sym("wInitialA"): b'\xff', sym("wTileMapFill"): b'\xff'},
            'read': {sym("wInitialA"): 0x01, sym("wTileMapFill"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
})
MUTATIONS.update({
    'CheckIfHasSaveData': {   'source_symbol': 'CheckIfHasSaveData',
        'before': '\tuint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;',
        'after': '\tuint8_t has_save = (first.f & 0x10u) ? FALSE : TRUE;',
        'case_ids': ['CheckIfHasSaveData-0', 'CheckIfHasSaveData-2'],
        'source': 'src/profiles/extended/home/start.c'},
    'DrawPlayerPortraitAndPrintNewGameText': {'source_symbol': 'DrawPlayerPortraitAndPrintNewGameText', 'before': '\tDrawPlayerPortrait(7u, 3u); /* menus/start.asm:410 lb bc, 7, 3 */', 'after': '\tDrawPlayerPortrait(0x6u, 3u); /* menus/start.asm:410 lb bc, 7, 3 */', 'case_ids': ['DrawPlayerPortraitAndPrintNewGameText-0'], 'source': 'src/profiles/extended/home/start.c'},
    'HandleTitleScreen': {   'source_symbol': 'HandleTitleScreen',
        'before': '\t\tPlaySong(MUSIC_STOP);\n\t\tEnableAndClearSpriteAnimations();\n\t\tPlayIntroSequence();\n\t\treturn;',
        'after': '\t\tPlaySong(0x01u);\n\t\tEnableAndClearSpriteAnimations();\n\t\tPlayIntroSequence();\n\t\treturn;',
        'case_ids': ['HandleTitleScreen-0', 'HandleTitleScreen-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'Start': {   'source_symbol': 'Start',
        'before': 'wInitialA = a;',
        'after': 'wInitialA = 0xFFu;',
        'case_ids': ['Start-0', 'Start-1'],
        'source': 'src/profiles/extended/home/start.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
for _record in SCHEMA2_CASES["DrawPlayerPortraitAndPrintNewGameText"]:
    _record.setdefault("bus", {}).update({VRAM_START: 0x2000})
