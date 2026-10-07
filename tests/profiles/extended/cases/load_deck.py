"""Extended oracle-diff cases for load_deck, seeded from tests/cases/load_deck.py."""

CONTRACT = {
    'LoadDeck': {'compare': ('f', 'hl'), 'preserve': ('hl',)},
}

CASES = {
    'LoadDeck': [
        {'a': 0x37, 'wram': {0xFF97: b'\xc2'}},
        {'a': 0x01, 'wram': {0xFF97: b'\xc2'}, 'read': {0xC400: 0x3C, 0xCC97: 0x02}},
        {'a': 0x08, 'wram': {0xFF97: b'\xc3'}, 'read': {0xC478: 0x3C, 0xCC97: 0x02}},
        {   'a': 0x02,
            'wram': {0xFF97: b'\xc2', 0xC400: b'\xff\xff\xff\xff\xff\xff\xff\xff'},
            'read': {0xC400: 0x3C, 0xCC97: 0x02}},
        {   'a': 0x37,
            'wram': {   0xFF97: b'\xc2',
                        0xC400: b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'},
            'read': {0xC400: 0x3C}},
        {   'a': 0x37,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC400: b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'
                                b'\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee\xee'},
            'read': {0xC400: 0x3C}},
        {   'a': 0x03,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2'},
            'read': {0xC400: 0x3C, 0xCC97: 0x02}},
    ],
}
DECK_ENTRIES = bytes(sum(([index & 0xFF, 1 if index % 3 == 0 else 0] for index in range(1, 61)), []))
COMPRESSED = bytes([0x92, 1, 2, 3, 4, 5, 6, 7, 8, 0x49, 9, 10, 11, 12, 13, 14, 15, 16,
                    0x24, 17, 18, 19, 20, 21, 22, 23, 24, 0x92, 25, 26, 27, 28, 29, 30, 31, 32,
                    0x49, 33, 34, 35, 36, 37, 38, 39, 40, 0x24, 41, 42, 43, 44, 45, 46, 47, 48,
                    0x92, 49, 50, 51, 52, 53, 54, 55, 56, 0x40, 57, 58, 59, 60])

CONTRACT['CompressDeckToSRAM'] = {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')}
CASES['CompressDeckToSRAM'] = [
    {'d': 0xC1, 'e': 0x00, 'hl': 0xC500, 'wram': {0xC100: bytes(120)}, 'read': {0xC500: 68}},
    {'d': 0xC1, 'e': 0x00, 'hl': 0xC500, 'wram': {0xC100: DECK_ENTRIES}, 'read': {0xC500: 68}},
    {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xC1, 'e': 0x00, 'hl': 0xC500,
     'wram': {0xC100: bytes([0xFF, 0x01] * 60)}, 'read': {0xC500: 68}},
]

CONTRACT['DecompressSRAMDeck'] = {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')}
CASES['DecompressSRAMDeck'] = [
    {'d': 0xC5, 'e': 0x00, 'hl': 0xC100, 'wram': {0xC500: bytes(68)}, 'read': {0xC100: 120, 0xCAEF: 1}},
    {'d': 0xC5, 'e': 0x00, 'hl': 0xC100, 'wram': {0xC500: COMPRESSED}, 'read': {0xC100: 120, 0xCAEF: 1}},
    {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xC5, 'e': 0x00, 'hl': 0xC100,
     'wram': {0xC500: bytes([0xFF] * 68)}, 'read': {0xC100: 120, 0xCAEF: 1}},
]

MUTATIONS = {
    'LoadDeck': {   'source_symbol': 'LoadDeck',
        'before': 'uint8_t carry = 1;',
        'after': 'uint8_t carry = 0;',
        'case_ids': [   'LoadDeck-0',
                        'LoadDeck-1',
                        'LoadDeck-2',
                        'LoadDeck-3',
                        'LoadDeck-4',
                        'LoadDeck-5'],
        'source': 'src/home/load_deck.c'},
    'CompressDeckToSRAM': {'source_symbol': 'CompressDeckToSRAM',
        'before': 'gb_write8(destination++, (uint8_t)(command << 4));',
        'after': 'gb_write8(destination++, command);',
        'case_ids': ['CompressDeckToSRAM-1', 'CompressDeckToSRAM-2'],
        'source': 'src/profiles/extended/home/load_deck.c'},
    'DecompressSRAMDeck': {'source_symbol': 'DecompressSRAMDeck',
        'before': 'gb_write8(destination++, (uint8_t)(command >> 7));',
        'after': 'gb_write8(destination++, (uint8_t)(command & 0x01u));',
        'case_ids': ['DecompressSRAMDeck-1', 'DecompressSRAMDeck-2'],
        'source': 'src/profiles/extended/home/load_deck.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
