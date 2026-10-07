"""Extended oracle-diff cases for fire_club, seeded from tests/cases/fire_club.py."""

CONTRACT = {
    'FireClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'FireClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'3',
                        0xD337: b'3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'expect': {0xD399: b'3', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
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
    'FireClubAfterDuel': {   'source_symbol': 'FireClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(FireClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(FireClubAfterDuelTable + 1u));',
        'case_ids': ['FireClubAfterDuel-0'],
        'source': 'src/profiles/extended/home/fire_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
