"""Extended oracle-diff cases for start, seeded from tests/cases/start.py."""

CONTRACT = {
    'CheckIfHasSaveData': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'PrintStartMenuDescriptionText': {'compare': ('a', 'f', 'b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'AskToContinueFromDiaryWithDuelData': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleStartMenu': {'compare': (), 'preserve': (), 'wram_out': True},
    'DrawPlayerPortraitAndPrintNewGameText': {'compare': (), 'preserve': ()},
    'DeleteSaveDataForNewGame': {'compare': (), 'preserve': ()},
    'HandleTitleScreen': {'compare': (), 'preserve': ()},
    'Start': {'compare': (), 'preserve': ()},
}

CASES = {
    'CheckIfHasSaveData': [
        {   'wram': {0xFF81: b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   0xB800: b'\x08\x00\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                        0x00: {   0xBC03: b'\x00',
                                  0xBC00: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD611: 0x01, 0xD612: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF81: b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   0xB800: b'\xf7\xff\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD611: 0x01, 0xD612: 0x01}},
        {   'wram': {0xFF81: b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   0xB800: b'\xf7\xff\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD611: 0x01, 0xD612: 0x01}},
    ],
    'PrintStartMenuDescriptionText': [
        {'wram': {0xCCBE: b'\x02', 0xD613: b'\x02', 0xD611: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCCBE: b'\x03', 0xD613: b'\x03', 0xD611: b'\x00'}},
    ],
    'AskToContinueFromDiaryWithDuelData': [
        {'wram': {0xD612: b'\x00'}, 'read': {0xD612: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD612: b'\x00'},
            'read': {0xD612: 0x01}},
    ],
    'HandleStartMenu': [
        {   'wram': {   0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff',
                        0xD611: b'\x00',
                        0xD612: b'\x00',
                        0xD614: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100,
            'read': {   0xCCB6: 0x01,
                        0xD611: 0x01,
                        0xD612: 0x01,
                        0xD613: 0x01,
                        0xD614: 0x01,
                        0xD615: 0x01,
                        0xD623: 0x11,
                        0xFFB1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff',
                        0xD611: b'\x00',
                        0xD612: b'\x00',
                        0xD614: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100,
            'read': {   0xCCB6: 0x01,
                        0xD611: 0x01,
                        0xD612: 0x01,
                        0xD613: 0x01,
                        0xD614: 0x01,
                        0xD615: 0x01,
                        0xD623: 0x11,
                        0xFFB1: 0x01}},
    ],
    'DrawPlayerPortraitAndPrintNewGameText': [
        {   'wram': {0xCABB: b'\x00', 0xFF40: b'\x00', 0xD280: b'\xa5'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00,
            'read': {0xD280: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCABB: b'\x00', 0xFF40: b'\x00', 0xD280: b'Z'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00,
            'read': {0xD280: 0x01}},
    ],
    'DeleteSaveDataForNewGame': [
        {   'wram': {0xD611: b'\x00'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD611: b'\x00'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
        {   'wram': {0xD611: b'\x01', 0xCABB: b'\x00'},
            'ramg': True,
            'sram': {0x02: {0xB800: b'\x00\x00'}},
            'sread': {0x02: {0xB800: 0x02}},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD611: b'\x01', 0xCABB: b'\x00'},
            'ramg': True,
            'sram': {0x02: {0xB800: b'\x00\x00'}},
            'sread': {0x02: {0xB800: 0x02}},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
    ],
    'HandleTitleScreen': [
        {   'oracle': False,
            'evidence': 'primary',
            'why': "The bounded opening prefix stops before PlayIntroSequence's frame-driven intro, "
                   'after stopping music and enabling sprite animations.',
            'wram': {0xD614: b'\x01', 0xD7A4: b'\x7f'},
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
            'why': 'The opening setup is independent of poisoned entry registers and still stops the '
                   'current song before the intro call.',
            'wram': {0xD614: b'\x01', 0xD7A4: b'\x7f'},
            'read': {0xD7A4: 0x01},
            'expect': {0xD7A4: b'\x00'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'Start': [
        {   'oracle': True,
            'evidence': 'primary',
            'why': 'The boot prefix initializes RAM, hardware, palettes, timer, serial state, DMA, and '
                   'SRAM before the non-returning GameLoop jump; the initial byte and tile fill are '
                   'asserted.',
            'a': 0x01,
            'wram': {0xCAB3: b'\xff', 0xCAB6: b'\xff'},
            'read': {0xCAB3: 0x01, 0xCAB6: 0x01},
            'expect': {0xCAB3: b'\x01', 0xCAB6: b' '},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': True,
            'evidence': 'primary',
            'why': 'The boot prefix must preserve the incoming A value in wInitialA and initialize the '
                   'tile fill with poisoned entry registers before the non-returning GameLoop jump.',
            'wram': {0xCAB3: b'\xff', 0xCAB6: b'\xff'},
            'read': {0xCAB3: 0x01, 0xCAB6: 0x01},
            'expect': {0xCAB3: b'\xaa', 0xCAB6: b' '},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'CheckIfHasSaveData': {   'source_symbol': 'CheckIfHasSaveData',
        'before': '\tuint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;',
        'after': '\tuint8_t has_save = (first.f & 0x10u) ? FALSE : TRUE;',
        'case_ids': ['CheckIfHasSaveData-0', 'CheckIfHasSaveData-2'],
        'source': 'src/profiles/extended/home/start.c'},
    'PrintStartMenuDescriptionText': {   'source_symbol': 'PrintStartMenuDescriptionText',
        'before': '\n\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;',
        'after': '\n\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0x80u : f;',
        'case_ids': ['PrintStartMenuDescriptionText-0', 'PrintStartMenuDescriptionText-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'AskToContinueFromDiaryWithDuelData': {   'source_symbol': 'AskToContinueFromDiaryWithDuelData',
        'before': '\t\treturn (AskToContinueFromDiaryWithDuelDataResult){a, 0x80u};',
        'after': '\t\treturn (AskToContinueFromDiaryWithDuelDataResult){0xFFu, 0x80u};',
        'case_ids': [   'AskToContinueFromDiaryWithDuelData-0',
                        'AskToContinueFromDiaryWithDuelData-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'HandleStartMenu': {   'source_symbol': 'HandleStartMenu',
        'before': '\t\twLastSelectedStartMenuItem = hCurMenuItem;',
        'after': '\t\twLastSelectedStartMenuItem = (uint8_t)(hCurMenuItem ^ 1u);',
        'case_ids': ['HandleStartMenu-0', 'HandleStartMenu-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'DrawPlayerPortraitAndPrintNewGameText': {   'source_symbol': 'DrawPlayerPortraitAndPrintNewGameText',
        'before': '\t(void)InitMenuScreen();',
        'after': '\t(void)InitMenuScreen();\n\t(void)0;',
        'case_ids': [   'DrawPlayerPortraitAndPrintNewGameText-0',
                        'DrawPlayerPortraitAndPrintNewGameText-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'DeleteSaveDataForNewGame': {   'source_symbol': 'DeleteSaveDataForNewGame',
        'before': 'uint8_t DeleteSaveDataForNewGame(void)\n{\n\tif (wHasSaveData == 0u)\n',
        'after': 'uint8_t DeleteSaveDataForNewGame(void)\n{\n\tif (wHasSaveData != 0u)\n',
        'case_ids': ['DeleteSaveDataForNewGame-2'],
        'source': 'src/profiles/extended/home/start.c'},
    'HandleTitleScreen': {   'source_symbol': 'HandleTitleScreen',
        'before': '\t\tPlaySong(MUSIC_STOP);\n\t\tEnableAndClearSpriteAnimations();\n\t\treturn;',
        'after': '\t\tPlaySong(0x01u);\n\t\tEnableAndClearSpriteAnimations();\n\t\treturn;',
        'case_ids': ['HandleTitleScreen-0', 'HandleTitleScreen-1'],
        'source': 'src/profiles/extended/home/start.c'},
    'Start': {   'source_symbol': 'Start',
        'before': 'wInitialA = a;',
        'after': 'wInitialA = 0xFFu;',
        'case_ids': ['Start-0', 'Start-1'],
        'source': 'src/profiles/extended/home/start.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
