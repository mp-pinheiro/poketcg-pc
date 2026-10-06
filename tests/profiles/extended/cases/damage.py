"""Extended oracle-diff cases for damage, seeded from tests/cases/damage.py."""

CONTRACT = {
    'AddToDamage': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'AddToDamage': [
        {'a': 0x00, 'wram': {0xCC64: b'\x00\x00'}},
        {'a': 0x40, 'wram': {0xCC64: b'\xc0\x00'}},
        {'a': 0x10, 'wram': {0xCC64: b'\x05\x01'}},
        {   'a': 0xFF,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCC64: b'\x01\x80'}},
    ],
}

MUTATIONS = {
    'AddToDamage': {   'source_symbol': 'AddToDamage',
        'before': 'uint16_t lo = (uint16_t)((uint16_t)gb_read8(wDamage_ADDR) + a);',
        'after': 'uint16_t lo = (uint16_t)((uint16_t)gb_read8(wDamage_ADDR) + (uint8_t)(a + 1u));',
        'case_ids': ['AddToDamage-zero', 'AddToDamage-boundary'],
        'source': 'src/profiles/extended/home/damage.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
