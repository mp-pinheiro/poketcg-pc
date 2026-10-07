"""Extended oracle-diff cases for math, seeded from tests/cases/math.py."""

CONTRACT = {
    'ATimes10': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'ATimes10': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x01, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x19, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x1A, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x64, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x80, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x33, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0xFF, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
}

MUTATIONS = {
    'ATimes10': {   'source_symbol': 'ATimes10',
        'before': 'a = (uint8_t)(a + e);',
        'after': 'a = (uint8_t)(a + (uint8_t)(e + 1u));',
        'case_ids': ['ATimes10-zero', 'ATimes10-poison-25', 'ATimes10-wrap'],
        'source': 'src/home/math.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
