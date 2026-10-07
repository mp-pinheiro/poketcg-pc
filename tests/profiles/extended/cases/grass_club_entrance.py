"""Extended oracle-diff cases for grass_club_entrance, seeded from tests/cases/grass_club_entrance.py."""

CONTRACT = {
    'FindEndOfDuelScript': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GrassClubEntranceAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_MichaelInGrassClubEntrance': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'FindEndOfDuelScript': [
        {'hl': 0xC600, 'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99', 0xC600: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC600,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99', 0xC600: b'\x00'}},
        {   'hl': 0xC600,
            'wram': {   0xD0B0: b'\x01',
                        0xD0B1: b'\x99',
                        0xD0B5: b'\x03',
                        0xC600: b'\x05\x00\x00\x00\x00\x00\x99\x42\x11\x22\x33\x44\x00'},
            'read': {0xD0B3: 0x03, 0xD399: 0x01}},
    ],
    'GrassClubEntranceAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Preload_MichaelInGrassClubEntrance': [
        {'wram': {0xD3C2: b'\x00'}},
        {'wram': {0xD3C2: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C2: b'\x10'}},
    ],
}

MUTATIONS = {
    'FindEndOfDuelScript': {   'source_symbol': 'FindEndOfDuelScript',
        'before': '\thl = (uint16_t)(hl + c);',
        'after': '\thl = (uint16_t)(hl + c + 1u);',
        'case_ids': ['FindEndOfDuelScript-2'],
        'source': 'src/home/grass_club_entrance.c'},
    'GrassClubEntranceAfterDuel': {   'source_symbol': 'GrassClubEntranceAfterDuel',
        'before': '\treturn FindEndOfDuelScript(GrassClubEntranceAfterDuelTable);',
        'after': '\treturn FindEndOfDuelScript((uint16_t)(GrassClubEntranceAfterDuelTable + 1u));',
        'case_ids': ['GrassClubEntranceAfterDuel-0'],
        'source': 'src/home/grass_club_entrance.c'},
    'Preload_MichaelInGrassClubEntrance': {   'source_symbol': 'Preload_MichaelInGrassClubEntrance',
        'before': '\tuint8_t a = GetEventValue(0x11u);',
        'after': '\tuint8_t a = GetEventValue(0x20u);',
        'case_ids': ['Preload_MichaelInGrassClubEntrance-1'],
        'source': 'src/home/grass_club_entrance.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
