"""Extended oracle-diff cases for water_club, seeded from tests/cases/water_club.py."""

CONTRACT = {
    'Preload_Amy': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'WaterClubMovePlayer': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ()},
    'WaterClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'Preload_Amy': [
        {   'wram': {0xD0AF: b'\x00', 0xD31D: b'\x00', 0xD31E: b'\x00', 0xD39A: b'U', 0xD3BF: b'f'},
            'read': {0xD0AF: 0x01, 0xD3BF: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0AF: b'\xaa', 0xD31D: b'\xbb', 0xD31E: b'\xcc', 0xD39A: b'U', 0xD3BF: b'f'},
            'read': {0xD0AF: 0x01, 0xD3BF: 0x01}},
        {   'wram': {0xD0AF: b'\x01', 0xD31D: b'\x13', 0xD31E: b'\x06', 0xD39A: b'U', 0xD3BF: b'f'},
            'read': {0xD0AF: 0x01, 0xD31D: 0x01, 0xD3BF: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0AF: b'\x01', 0xD31D: b'\x14', 0xD31E: b'\x05', 0xD39A: b'U', 0xD3BF: b'f'},
            'read': {0xD0AF: 0x01, 0xD31D: 0x01, 0xD31E: 0x01, 0xD3BF: 0x01}},
        {   'wram': {0xD0AF: b'\x01', 0xD31D: b'\x14', 0xD31E: b'\x06', 0xD39A: b'U', 0xD3BF: b'f'},
            'read': {0xD0AF: 0x01, 0xD31D: 0x01, 0xD31E: 0x01, 0xD39A: 0x01, 0xD3BF: 0x01}},
    ],
    'WaterClubMovePlayer': [
        {'b': 0x12, 'c': 0x34, 'hl': 0x00, 'wram': {0xD31E: b'\t'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31E: b'\t'}},
        {'b': 0x56, 'c': 0x78, 'hl': 0x00, 'wram': {0xD31E: b'\x08', 0xD3CC: b' '}},
        {'b': 0x9A, 'c': 0xBC, 'hl': 0x1234, 'wram': {0xD31E: b'\x08', 0xD3CC: b'\x00'}},
    ],
    'WaterClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'\x1f',
                        0xD337: b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'expect': {0xD399: b'\x1f', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
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
    'Preload_Amy': {   'source_symbol': 'Preload_Amy',
        'before': 'if (event != 0)',
        'after': 'if (event == 0)',
        'case_ids': [   'Preload_Amy-0',
                        'Preload_Amy-1',
                        'Preload_Amy-2',
                        'Preload_Amy-3',
                        'Preload_Amy-4'],
        'source': 'src/home/water_club.c'},
    'WaterClubMovePlayer': {   'source_symbol': 'WaterClubMovePlayer',
        'before': '\tif (y != 8u) {',
        'after': '\tif (y != 9u) {',
        'case_ids': ['WaterClubMovePlayer-0', 'WaterClubMovePlayer-1'],
        'source': 'src/home/water_club.c'},
    'WaterClubAfterDuel': {   'source_symbol': 'WaterClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(WaterClubAfterDuelTable + 1u));',
        'case_ids': ['WaterClubAfterDuel-0'],
        'source': 'src/home/water_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
