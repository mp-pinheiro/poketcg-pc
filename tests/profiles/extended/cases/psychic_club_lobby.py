"""Extended oracle-diff cases for psychic_club_lobby, seeded from tests/cases/psychic_club_lobby.py."""

CONTRACT = {
    'PsychicClubLobbyLoadMap': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ()},
    'PsychicClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    '_Preload_Ronald1InPsychicClubLobby': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_Ronald1InPsychicClubLobby': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'PsychicClubLobbyLoadMap': [
        {   'b': 0x12,
            'c': 0x34,
            'hl': 0x00,
            'wram': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD397: b'\xee'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD397: b'\xee'}},
    ],
    'PsychicClubLobbyAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'+',
                        0xD337: b'+\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'expect': {0xD399: b'+', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    '_Preload_Ronald1InPsychicClubLobby': [
        {   'wram': {   0xD3C0: b'\xff',
                        0xD3C1: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD3C0: b'\xff',
                        0xD3C1: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
    ],
    'Preload_Ronald1InPsychicClubLobby': [
        {   'wram': {   0xD3C0: b'\xff',
                        0xD3C1: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD3C0: b'\xff',
                        0xD3C1: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
    ],
}

MUTATIONS = {
    'PsychicClubLobbyLoadMap': {   'source_symbol': 'PsychicClubLobbyLoadMap',
        'before': '\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_ea02_ADDR, hl);',
        'after': '\tSetNextNPCAndScriptResult r2 = SetNextNPCAndScript((uint16_t)(Script_ea02_ADDR '
                 '+ 1u), hl);',
        'case_ids': ['PsychicClubLobbyLoadMap-0'],
        'source': 'src/home/psychic_club_lobby.c'},
    'PsychicClubLobbyAfterDuel': {   'source_symbol': 'PsychicClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(PsychicClubLobbyAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(PsychicClubLobbyAfterDuelTable + 1u));',
        'case_ids': ['PsychicClubLobbyAfterDuel-0'],
        'source': 'src/home/psychic_club_lobby.c'},
    '_Preload_Ronald1InPsychicClubLobby': {   'source_symbol': '_Preload_Ronald1InPsychicClubLobby',
        'before': 'uint8_t f = (medal_count == 0u) ? 0x80u : 0x00u;',
        'after': 'uint8_t f = (medal_count == 0u) ? 0x00u : 0x80u;',
        'case_ids': ['_Preload_Ronald1InPsychicClubLobby-0'],
        'source': 'src/home/psychic_club_lobby.c'},
    'Preload_Ronald1InPsychicClubLobby': {   'source_symbol': 'Preload_Ronald1InPsychicClubLobby',
        'before': '\t\treturn (Preload_Ronald1InPsychicClubLobbyResult){r.a, r.f, b, c, d, e, hl};',
        'after': '\t\treturn (Preload_Ronald1InPsychicClubLobbyResult){r.a, r.f, c, c, d, e, hl};',
        'case_ids': ['Preload_Ronald1InPsychicClubLobby-1'],
        'source': 'src/home/psychic_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
