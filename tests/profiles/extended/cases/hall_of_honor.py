"""Extended oracle-diff cases for hall_of_honor, seeded from tests/cases/hall_of_honor.py."""

CONTRACT = {
    'HallOfHonorLoadMap': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
}

CASES = {
    'HallOfHonorLoadMap': [
        {'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
        {'wram': {0xD7A6: b'\xff', 0xD7A7: b'\xff'}, 'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
    ],
}

MUTATIONS = {
    'HallOfHonorLoadMap': {   'source_symbol': 'HallOfHonorLoadMap',
        'before': 'PlaySFX(SFX_LEGENDARY_CARDS)',
        'after': 'PlaySFX(0x11u)',
        'case_ids': ['HallOfHonorLoadMap-0', 'HallOfHonorLoadMap-1', 'HallOfHonorLoadMap-2'],
        'source': 'src/profiles/extended/home/hall_of_honor.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
