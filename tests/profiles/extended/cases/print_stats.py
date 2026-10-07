"""Extended oracle-diff cases for print_stats, seeded from tests/cases/print_stats.py."""

CONTRACT = {
    'DrawPauseMenuPlayerPortrait': {'compare': (), 'preserve': ()},
    'FlashReceivedMedal': {'compare': (), 'preserve': ()},
    'ConvertWordToNumericalDigits': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'PrintAlbumProgress_SkipGetProgress': {'compare': (), 'preserve': ()},
    'PrintPlayTime_SkipUpdateTime': {'compare': (), 'preserve': ()},
    'PrintAlbumProgress': {'compare': (), 'preserve': ()},
    'PrintPlayTime': {'compare': (), 'preserve': (), 'wram_out': True},
    'PrintMedalCount': {'compare': (), 'preserve': (), 'wram_out': True},
}

CASES = {
    'DrawPauseMenuPlayerPortrait': [
        {'wram': {0xD60B: b'\xff'}, 'read': {0xD60B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD60B: b'\xff'},
            'read': {0xD60B: 0x01}},
    ],
    'FlashReceivedMedal': [
        {   'wram': {0xD102: b'\x00', 0xD101: b'\x00', 0xD103: b'\x00', 0xD11E: b'\x00'},
            'read': {0xD27E: 0x01, 0xD11E: 0x01},
            'vread': {0x00: {0x9800: 0x0240}}},
        {   'wram': {0xD102: b'\x02', 0xD101: b'\x00', 0xD103: b'\x10', 0xD11E: b'\x00'},
            'read': {0xD27E: 0x01, 0xD11E: 0x01},
            'vread': {0x00: {0x9800: 0x0240}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD102: b'\x00', 0xD101: b'\x00', 0xD103: b'\x00', 0xD11E: b'\x00'},
            'read': {0xD27E: 0x01, 0xD11E: 0x01},
            'vread': {0x00: {0x9800: 0x0240}}},
    ],
    'ConvertWordToNumericalDigits': [
        {'hl': 0x0101, 'wram': {0xD4A1: b'\x00\x00\x00'}, 'expect': {0xD4A1: b'"%\''}},
        {'hl': 0x05, 'wram': {0xD4A1: b'\x00\x00\x00'}, 'expect': {0xD4A1: b'\x00\x00%'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4A1: b'\x00\x00\x00'}},
    ],
    'PrintAlbumProgress_SkipGetProgress': [
        {   'b': 0x00,
            'c': 0x00,
            'd': 0x05,
            'e': 0x0A,
            'read': {0xD4A1: 0x03},
            'vread': {0x00: {0x9800: 0x03, 0x9804: 0x03}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD4A1: 0x03},
            'vread': {0x00: {0x9800: 0x03}}},
    ],
    'PrintPlayTime_SkipUpdateTime': [
        {   'b': 0x00,
            'c': 0x00,
            'wram': {0xD3B5: b'\x1e\x05\x00'},
            'read': {0xD4A1: 0x03},
            'vread': {0x00: {0x9800: 0x03, 0x9804: 0x02}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3B5: b'\x1e\x05\x00'},
            'read': {0xD4A1: 0x03},
            'vread': {0x00: {0x9800: 0x03}}},
    ],
    'PrintAlbumProgress': [
        {   'b': 0x00,
            'c': 0x00,
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD4A1: 0x03},
            'vread': {0x00: {0x9800: 0x03, 0x9804: 0x03}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD4A1: 0x03}},
    ],
    'PrintPlayTime': [
        {   'b': 0x02,
            'c': 0x02,
            'wram': {0xCAC7: b'\x1e', 0xCAC8: b'\x05', 0xCAC9: b'\x00'},
            'vread': {0x00: {0x9842: 0x05}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x02,
            'c': 0x02,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAC7: b'\x1e', 0xCAC8: b'\x05', 0xCAC9: b'\x00'},
            'vread': {0x00: {0x9842: 0x05}}},
    ],
    'PrintMedalCount': [
        {   'b': 0x02,
            'c': 0x02,
            'wram': {   0xD3C0: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD3C1: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD3CB: b' '},
            'vread': {0x00: {0x9842: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x02,
            'c': 0x02,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD3C0: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD3C1: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD3CB: b' '},
            'vread': {0x00: {0x9842: 0x01}}},
    ],
}

MUTATIONS = {
    'DrawPauseMenuPlayerPortrait': {   'source_symbol': 'DrawPauseMenuPlayerPortrait',
        'before': '\tDrawPlayerPortrait(b, c);',
        'after': '\t(void)b;\n\t(void)c;',
        'case_ids': ['DrawPauseMenuPlayerPortrait-0', 'DrawPauseMenuPlayerPortrait-1'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'FlashReceivedMedal': {   'source_symbol': 'FlashReceivedMedal',
        'before': '\twCurTilemap = tilemap;',
        'after': '\twCurTilemap = 0u;',
        'case_ids': ['FlashReceivedMedal-0'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'ConvertWordToNumericalDigits': {   'source_symbol': 'ConvertWordToNumericalDigits',
        'before': 'uint8_t a = (uint8_t)((uint8_t)hl + SYM_0);',
        'after': 'uint8_t a = (uint8_t)((uint8_t)hl + SYM_0 + 1u);',
        'case_ids': ['ConvertWordToNumericalDigits-0', 'ConvertWordToNumericalDigits-1'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'PrintAlbumProgress_SkipGetProgress': {   'source_symbol': 'PrintAlbumProgress_SkipGetProgress',
        'before': 'uint8_t b2 = (uint8_t)(b + 4u);',
        'after': 'uint8_t b2 = (uint8_t)(b + 5u);',
        'case_ids': ['PrintAlbumProgress_SkipGetProgress-0'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'PrintPlayTime_SkipUpdateTime': {   'source_symbol': 'PrintPlayTime_SkipUpdateTime',
        'before': 'uint16_t sum = (uint16_t)((uint16_t)minutes + 100u);',
        'after': 'uint16_t sum = (uint16_t)((uint16_t)minutes + 99u);',
        'case_ids': ['PrintPlayTime_SkipUpdateTime-0'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'PrintAlbumProgress': {   'source_symbol': 'PrintAlbumProgress',
        'before': 'PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e,\n'
                  '\t\t(uint16_t)(((uint16_t)prog.b << 8) | prog.c));',
        'after': 'PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e,\n'
                 '\t\t(uint16_t)(((uint16_t)(prog.b + 1u) << 8) | prog.c));',
        'case_ids': ['PrintAlbumProgress-0'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'PrintPlayTime': {   'source_symbol': 'PrintPlayTime',
        'before': 'gb_write8(wPlayTimeHourMinutes_ADDR, gb_read8((uint16_t)(wPlayTimeCounter_ADDR '
                  '+ 2u)));',
        'after': 'gb_write8(wPlayTimeHourMinutes_ADDR, gb_read8((uint16_t)(wPlayTimeCounter_ADDR + '
                 '3u)));',
        'case_ids': ['PrintPlayTime-0', 'PrintPlayTime-1'],
        'source': 'src/profiles/extended/home/print_stats.c'},
    'PrintMedalCount': {   'source_symbol': 'PrintMedalCount',
        'before': 'uint16_t src = (uint16_t)(wDecimalChars_ADDR + 2u);',
        'after': 'uint16_t src = (uint16_t)(wDecimalChars_ADDR + 1u);',
        'case_ids': ['PrintMedalCount-0', 'PrintMedalCount-1'],
        'source': 'src/profiles/extended/home/print_stats.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
