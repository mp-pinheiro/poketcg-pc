"""Extended oracle-diff cases for fire_club_lobby, seeded from tests/cases/fire_club_lobby.py."""

CONTRACT = {
    'FindExtraInteractableObjects': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'FireClubPressedA': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'FireClubLobbyAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Lad2': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_JessicaInFireClubLobby': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'FindExtraInteractableObjects': [
        {'hl': 0xC4F0, 'wram': {0xC4F0: b'\x00'}},
        {   'hl': 0xC4F0,
            'wram': {   0xC4F0: b'\xaa\x00\x00\x00\x00\x05\x06\x00\xbc\x9a\x00',
                        0xD31D: b'\x05',
                        0xD31E: b'\x06',
                        0xD321: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31D: b'\x05', 0xD31E: b'\x06', 0xD321: b'\x00'}},
    ],
    'FireClubPressedA': [
        {'wram': {0xD31D: b'\x10', 0xD31E: b'\x02', 0xD321: b'\x00'}, 'rom_bank': 0x03},
        {'wram': {0xD31D: b'c', 0xD31E: b'\x02', 0xD321: b'\x00'}, 'rom_bank': 0x03},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31D: b'\x10', 0xD31E: b'\x02', 0xD321: b'\x00'},
            'rom_bank': 0x03},
    ],
    'FireClubLobbyAfterDuel': [
        {'wram': {0xD0B0: b'\x00', 0xD0B1: b'\x19'}, 'rom_bank': 0x03},
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x19'}, 'rom_bank': 0x03},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x00', 0xD0B1: b'\x19'},
            'rom_bank': 0x03},
    ],
    'Preload_Lad2': [
        {'wram': {0xD3C7: b'\x00'}},
        {'wram': {0xD3C7: b'\x04'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\x08'}},
    ],
    'Preload_JessicaInFireClubLobby': [
        {'wram': {0xD3C7: b'\x00'}},
        {'wram': {0xD3C7: b'\x10'}},
        {'wram': {0xD3C7: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\x90'}},
    ],
}

MUTATIONS = {
    'FindExtraInteractableObjects': {   'source_symbol': 'FindExtraInteractableObjects',
        'before': 'if (gb_read8(wPlayerXCoord_ADDR) == gb_read8(cursor)) {',
        'after': 'if (gb_read8(wPlayerXCoord_ADDR) != gb_read8(cursor)) {',
        'case_ids': ['FindExtraInteractableObjects-1'],
        'source': 'src/profiles/extended/home/fire_club_lobby.c'},
    'FireClubPressedA': {   'source_symbol': 'FireClubPressedA',
        'before': 'FindExtraInteractableObjectsResult r = '
                  'FindExtraInteractableObjects(SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520);',
        'after': 'FindExtraInteractableObjectsResult r = '
                 'FindExtraInteractableObjects((uint16_t)(SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520 '
                 '+ 5u));',
        'case_ids': ['FireClubPressedA-0', 'FireClubPressedA-1'],
        'source': 'src/home/fire_club_lobby.c'},
    'FireClubLobbyAfterDuel': {   'source_symbol': 'FireClubLobbyAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(AFTER_DUEL_TABLE_830);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(AFTER_DUEL_TABLE_830 + 1u));',
        'case_ids': ['FireClubLobbyAfterDuel-0'],
        'source': 'src/home/fire_club_lobby.c'},
    'Preload_Lad2': {   'source_symbol': 'Preload_Lad2',
        'before': '\tif (a < LAD2_SLOWPOKE_AVAILABLE)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= LAD2_SLOWPOKE_AVAILABLE)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Lad2-1'],
        'source': 'src/home/fire_club_lobby.c'},
    'Preload_JessicaInFireClubLobby': {   'source_symbol': 'Preload_JessicaInFireClubLobby',
        'before': '\tif (a < PUPIL_DEFEATED)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= PUPIL_DEFEATED)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_JessicaInFireClubLobby-2'],
        'source': 'src/home/fire_club_lobby.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
