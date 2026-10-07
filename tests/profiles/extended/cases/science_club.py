"""Extended oracle-diff cases for science_club, seeded from tests/cases/science_club.py."""

CONTRACT = {
    'Preload_Joseph': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'ScienceClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'Preload_Joseph': [
        {'wram': {0xD3C6: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C6: b'\x80', 0xD39A: b'\x05'},
            'read': {0xD39A: 0x01, 0xD39C: 0x01}},
        {'wram': {0xD3C6: b'\x80', 0xD39A: b'\xfe'}, 'read': {0xD39A: 0x01, 0xD39C: 0x01}},
    ],
    'ScienceClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'/',
                        0xD337: b'/\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD397: b'\xee',
                        0xD3A3: b'\xaa',
                        0xD321: b'\x01',
                        0xD0AE: b'\x00',
                        0xD0B3: b'\xff\xff',
                        0xD0AC: b'\x00'},
            'expect': {0xD399: b'/', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
}

MUTATIONS = {
    'Preload_Joseph': {   'source_symbol': 'Preload_Joseph',
        'before': '\t\tuint8_t new_x = (uint8_t)(x + 2u);',
        'after': '\t\tuint8_t new_x = (uint8_t)(x + 3u);',
        'case_ids': ['Preload_Joseph-1', 'Preload_Joseph-2'],
        'source': 'src/home/science_club.c'},
    'ScienceClubAfterDuel': {   'source_symbol': 'ScienceClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(ScienceClubAfterDuelTable + 1u));',
        'case_ids': ['ScienceClubAfterDuel-0'],
        'source': 'src/home/science_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
