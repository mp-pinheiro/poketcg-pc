"""Extended oracle-diff cases for grass_club_lobby, seeded from tests/cases/grass_club_lobby.py."""

CONTRACT = {
    'GrassClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Gal2': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'GrassClubLobbyAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b"'",
                        0xD337: b"'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
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
            'expect': {0xD399: b"'", 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Preload_Gal2': [
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
}

MUTATIONS = {
    'GrassClubLobbyAfterDuel': {   'source_symbol': 'GrassClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(GrassClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(GrassClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['GrassClubLobbyAfterDuel-0'],
        'source': 'src/profiles/extended/home/grass_club_lobby.c'},
    'Preload_Gal2': {   'source_symbol': 'Preload_Gal2',
        'before': '\tif (a < TRUE)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= TRUE)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Gal2-1'],
        'source': 'src/profiles/extended/home/grass_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
