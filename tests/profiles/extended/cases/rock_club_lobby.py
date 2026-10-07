"""Extended oracle-diff cases for rock_club_lobby, seeded from tests/cases/rock_club_lobby.py."""

CONTRACT = {
    'RockClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Lass3': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_ChrisInRockClubLobby': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'RockClubLobbyAfterDuel': [
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
    'Preload_Lass3': [
        {'wram': {0xD3C7: b'\x00'}},
        {'wram': {0xD3C7: b'\x02'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\x02'}},
    ],
    'Preload_ChrisInRockClubLobby': [
        {'wram': {0xD3C4: b'\x00'}},
        {'wram': {0xD3C4: b'\x10'}},
        {'wram': {0xD3C4: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C4: b'\x90'}},
    ],
}

MUTATIONS = {
    'RockClubLobbyAfterDuel': {   'source_symbol': 'RockClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(RockClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(RockClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['RockClubLobbyAfterDuel-0'],
        'source': 'src/profiles/extended/home/rock_club_lobby.c'},
    'Preload_Lass3': {   'source_symbol': 'Preload_Lass3',
        'before': '\tif (a < TRUE)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= TRUE)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Lass3-1'],
        'source': 'src/profiles/extended/home/rock_club_lobby.c'},
    'Preload_ChrisInRockClubLobby': {   'source_symbol': 'Preload_ChrisInRockClubLobby',
        'before': '\tif (a < PUPIL_DEFEATED)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= PUPIL_DEFEATED)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_ChrisInRockClubLobby-2'],
        'source': 'src/profiles/extended/home/rock_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
