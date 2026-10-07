"""Extended oracle-diff cases for water_club_lobby, seeded from tests/cases/water_club_lobby.py."""

CONTRACT = {
    'WaterClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Man2': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_ImakuniInWaterClubLobby': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'WaterClubLobbyAfterDuel': [
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
    'Preload_Man2': [
        {'wram': {0xD3CC: b'\x00'}},
        {'wram': {0xD3CC: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CC: b'0'}},
    ],
    'Preload_ImakuniInWaterClubLobby': [
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x0c'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x00'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x10', 0xD3CC: b'\x0c'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x00', 0xD400: b'\x00', 0xD3CC: b'\x0c'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C3: b'@', 0xD400: b'\x00', 0xD3CC: b'\x0c'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
    ],
}

MUTATIONS = {
    'WaterClubLobbyAfterDuel': {   'source_symbol': 'WaterClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(WaterClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(WaterClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['WaterClubLobbyAfterDuel-0'],
        'source': 'src/profiles/extended/home/water_club_lobby.c'},
    'Preload_Man2': {   'source_symbol': 'Preload_Man2',
        'before': '\tif (a < JOSHUA_DEFEATED)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= JOSHUA_DEFEATED)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Man2-1'],
        'source': 'src/profiles/extended/home/water_club_lobby.c'},
    'Preload_ImakuniInWaterClubLobby': {   'source_symbol': 'Preload_ImakuniInWaterClubLobby',
        'before': '\tif (room != IMAKUNI_WATER_CLUB)',
        'after': '\tif (room == IMAKUNI_WATER_CLUB)',
        'case_ids': ['Preload_ImakuniInWaterClubLobby-0', 'Preload_ImakuniInWaterClubLobby-1'],
        'source': 'src/profiles/extended/home/water_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
