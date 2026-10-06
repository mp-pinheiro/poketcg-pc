CONTRACT = {
    'GetAudioCmdAndArgs': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
}

POISON = {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
          'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}

CASES = {
    'GetAudioCmdAndArgs': [
        {'a': 0x00, 'hl': 0xC100, 'wram': {0xC100: b'\x00\x00\x00'},
         'read': {0xD909: 1, 0xD90A: 2}},
        dict(POISON, a=0x42, hl=0xC100,
             wram={0xC100: b'\xD0\x12\x34'},
             read={0xD909: 1, 0xD90A: 2}),
        {'a': 0x01, 'b': 0x01, 'c': 0x02, 'hl': 0xFFFF,
         'wram': {0xFFFF: b'\xFE', 0x0000: b'\xED', 0x0001: b'\xDC'},
         'read': {0xD909: 1, 0xD90A: 2}},
    ],
}

MUTATIONS = {
    'GetAudioCmdAndArgs': {
        'source_symbol': 'GetAudioCmdAndArgs',
        'before': '\tgb_write8(wAudioArg_ADDR, arg0);',
        'after': '\tgb_write8(wAudioArg_ADDR, arg1);',
        'case_ids': ['GetAudioCmdAndArgs-1'],
        'source': 'src/profiles/extended/home/audio.c',
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
