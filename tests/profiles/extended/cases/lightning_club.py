"""Extended oracle-diff cases for lightning_club, seeded from tests/cases/lightning_club.py."""

CONTRACT = {
    'LightningClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Preload_Isaac': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'LightningClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'#',
                        0xD337: b'#\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                        0xD0AC: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Preload_Isaac': [
        {'wram': {0xD3C8: b'\x00'}},
        {'wram': {0xD3C8: b'8'}, 'read': {0xD3C8: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C8: b'8'}},
    ],
}

MUTATIONS = {
    'LightningClubAfterDuel': {   'source_symbol': 'LightningClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(LightningClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(LightningClubAfterDuelTable + 1u));',
        'case_ids': ['LightningClubAfterDuel-0'],
        'source': 'src/home/lightning_club.c'},
    'Preload_Isaac': {   'source_symbol': 'Preload_Isaac',
        'before': '\ta = SOUTH;',
        'after': '\ta = 0u;',
        'case_ids': ['Preload_Isaac-1', 'Preload_Isaac-2'],
        'source': 'src/home/lightning_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
