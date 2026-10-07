"""Extended oracle-diff cases for fighting_club, seeded from tests/cases/fighting_club.py."""

CONTRACT = {
    'FightingClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_ChrisInFightingClub': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_MichaelInFightingClub': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_JessicaInFightingClub': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'FightingClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'\x17',
                        0xD337: b'\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'expect': {0xD399: b'\x17', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Preload_ChrisInFightingClub': [
        {'wram': {0xD3C4: b'\x00'}},
        {'wram': {0xD3C4: b'\x80'}},
        {'wram': {0xD3C4: b'p'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C4: b'\x90'}},
    ],
    'Preload_MichaelInFightingClub': [
        {'wram': {0xD3C2: b'\x00'}},
        {'wram': {0xD3C2: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C2: b'p'}},
    ],
    'Preload_JessicaInFightingClub': [
        {'wram': {0xD3C7: b'\x00'}},
        {'wram': {0xD3C7: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'p'}},
    ],
}

MUTATIONS = {
    'FightingClubAfterDuel': {   'source_symbol': 'FightingClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(FightingClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(FightingClubAfterDuelTable + 1u));',
        'case_ids': ['FightingClubAfterDuel-0'],
        'source': 'src/profiles/extended/home/fighting_club.c'},
    'Preload_ChrisInFightingClub': {   'source_symbol': 'Preload_ChrisInFightingClub',
        'before': '\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);',
        'after': '\treturn preload_pupil(EVENT_PUPIL_MICHAEL_STATE);',
        'case_ids': ['Preload_ChrisInFightingClub-1'],
        'source': 'src/profiles/extended/home/fighting_club.c'},
    'Preload_MichaelInFightingClub': {   'source_symbol': 'Preload_MichaelInFightingClub',
        'before': '\treturn preload_pupil(EVENT_PUPIL_MICHAEL_STATE);',
        'after': '\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);',
        'case_ids': ['Preload_MichaelInFightingClub-1'],
        'source': 'src/profiles/extended/home/fighting_club.c'},
    'Preload_JessicaInFightingClub': {   'source_symbol': 'Preload_JessicaInFightingClub',
        'before': '\treturn preload_pupil(EVENT_PUPIL_JESSICA_STATE);',
        'after': '\treturn preload_pupil(EVENT_PUPIL_CHRIS_STATE);',
        'case_ids': ['Preload_JessicaInFightingClub-1'],
        'source': 'src/profiles/extended/home/fighting_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
