"""Extended oracle-diff cases for fighting_club_lobby, seeded from tests/cases/fighting_club_lobby.py."""

CONTRACT = {
    'FightingClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Granny1': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_ImakuniInFightingClubLobby': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'FightingClubLobbyAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'\x04',
                        0xD337: b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'expect': {0xD399: b'\x04', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Preload_Granny1': [
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
    'Preload_ImakuniInFightingClubLobby': [
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x00'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x04'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x10', 0xD3CC: b'\x00'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x00', 0xD400: b'\x00', 0xD3CC: b'\x00'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C3: b'@', 0xD400: b'\x00', 0xD3CC: b'\x00'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
    ],
}

MUTATIONS = {
    'FightingClubLobbyAfterDuel': {   'source_symbol': 'FightingClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(FightingClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(FightingClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['FightingClubLobbyAfterDuel-0'],
        'source': 'src/home/fighting_club_lobby.c'},
    'Preload_Granny1': {   'source_symbol': 'Preload_Granny1',
        'before': '\tif (a < TRUE)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= TRUE)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Granny1-1'],
        'source': 'src/home/fighting_club_lobby.c'},
    'Preload_ImakuniInFightingClubLobby': {   'source_symbol': 'Preload_ImakuniInFightingClubLobby',
        'before': '\tif (room != IMAKUNI_FIGHTING_CLUB)',
        'after': '\tif (room == IMAKUNI_FIGHTING_CLUB)',
        'case_ids': [   'Preload_ImakuniInFightingClubLobby-0',
                        'Preload_ImakuniInFightingClubLobby-1'],
        'source': 'src/home/fighting_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
