"""Extended oracle-diff cases for science_club_lobby, seeded from tests/cases/science_club_lobby.py."""

CONTRACT = {
    'ScienceClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_ImakuniInScienceClubLobby': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'Script_Specs2': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
}

CASES = {
    'ScienceClubLobbyAfterDuel': [
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
    'Preload_ImakuniInScienceClubLobby': [
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x04'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x00', 0xD3CC: b'\x08'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x80', 0xD400: b'\x10', 0xD3CC: b'\x04'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'wram': {0xD3C3: b'\x00', 0xD400: b'\x00', 0xD3CC: b'\x04'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C3: b'@', 0xD400: b'\x00', 0xD3CC: b'\x04'},
            'read': {0xD3C3: 0x01, 0xD3CC: 0x01}},
    ],
    'Script_Specs2': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {0xCE05: b'\xff\xff\xff', 0xCACA: b'\x00@\x01'},
            'read': {0xCE05: 0x03, 0xCACA: 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {0xCE05: b'\xff\xff\xff', 0xCACA: b'\x00\x00\x00'},
            'read': {0xCE05: 0x03, 0xCACA: 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {0xCE05: b'\xff\xff\xff', 0xCACA: b'\x00@\x00'},
            'read': {0xCE05: 0x03, 0xCACA: 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {0xCE05: b'\xff\xff\xff', 0xCACA: b'\x00\x00\x01'},
            'read': {0xCE05: 0x03, 0xCACA: 0x03}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCE05: b'\xff\xff\xff', 0xCACA: b'\x00@\x01'},
            'read': {0xCE05: 0x03, 0xCACA: 0x03}},
    ],
}

MUTATIONS = {
    'ScienceClubLobbyAfterDuel': {   'source_symbol': 'ScienceClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(ScienceClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(ScienceClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['ScienceClubLobbyAfterDuel-0'],
        'source': 'src/home/science_club_lobby.c'},
    'Preload_ImakuniInScienceClubLobby': {   'source_symbol': 'Preload_ImakuniInScienceClubLobby',
        'before': '\tif (room != IMAKUNI_SCIENCE_CLUB)',
        'after': '\tif (room == IMAKUNI_SCIENCE_CLUB)',
        'case_ids': ['Preload_ImakuniInScienceClubLobby-0', 'Preload_ImakuniInScienceClubLobby-1'],
        'source': 'src/home/science_club_lobby.c'},
    'Script_Specs2': {   'source_symbol': 'Script_Specs2',
        'before': '\tuint16_t hl = (uint16_t)(DATA_EBE7 + c);',
        'after': '\tuint16_t hl = (uint16_t)(DATA_EBE7 + c + 2u);',
        'case_ids': ['Script_Specs2-0', 'Script_Specs2-2', 'Script_Specs2-3', 'Script_Specs2-4'],
        'source': 'src/profiles/extended/home/science_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record in SCHEMA2_CASES["Script_Specs2"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6A43, "bank": 3}
