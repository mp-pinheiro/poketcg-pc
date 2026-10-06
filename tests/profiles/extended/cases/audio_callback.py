"""Extended oracle-diff cases for audio_callback, seeded from tests/cases/audio_callback.py."""

CONTRACT = {
    'Bankswitch3dTo3f': {'compare': (), 'preserve': ()},
}

CASES = {
    'Bankswitch3dTo3f': [
        {   'oracle': False,
            'why': 'The zero-register call has no valid caller callback; verify its bank-3d tail '
                   'directly.',
            'expect': {0xFF80: b'='}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': False,
            'why': 'The standalone poisoned call has no valid caller callback; verify its bank-3d tail '
                   'directly.',
            'expect': {0xFF80: b'='}},
        {'hl': 0x3FEE, 'read': {0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x3FEE,
            'read': {0xFF80: 0x01}},
    ],
}

MUTATIONS = {
    'Bankswitch3dTo3f': {   'source_symbol': 'Bankswitch3dTo3f',
        'before': 'BankswitchROM(0x3Du);',
        'after': 'BankswitchROM(0x3Eu);',
        'case_ids': ['Bankswitch3dTo3f-2', 'Bankswitch3dTo3f-3'],
        'source': 'src/profiles/extended/home/audio_callback.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
