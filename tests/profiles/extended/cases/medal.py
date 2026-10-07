"""Extended oracle-diff cases for medal, seeded from tests/cases/medal.py."""

CONTRACT = {
    'ShowMedalReceivedScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    'ShowMedalReceivedScreen': [
        {   'oracle': False,
            'why': 'Extended medal screen waits for song and frame-driven animation completion outside the isolated oracle.',
            'a': 0x08,
            'expect': {0xD101: b'\xfa', 0xD102: b'\x00', 0xD103: b'\xe0', 0xD11E: b'\x1e'}},
        {   'oracle': False,
            'why': 'Extended medal screen waits for song and frame-driven animation completion outside the isolated oracle.',
            'a': 0x0F,
            'expect': {0xD101: b'\xfa', 0xD102: b'\x07', 0xD103: b'\xe0', 0xD11E: b'\x23'}},
        {   'oracle': False,
            'why': 'Extended medal screen waits for song and frame-driven animation completion outside the isolated oracle.',
            'a': 0x0A,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'expect': {0xD101: b'\xfa', 0xD102: b'\x02', 0xD103: b'\xe0', 0xD11E: b'\x20'}},
    ],
}

MUTATIONS = {
    'ShowMedalReceivedScreen': {   'source_symbol': 'ShowMedalReceivedScreen',
        'before': '\twMedalScreenYOffset = (uint8_t)-6;',
        'after': '\twMedalScreenYOffset = (uint8_t)-5;',
        'case_ids': [   'ShowMedalReceivedScreen-0',
                        'ShowMedalReceivedScreen-1',
                        'ShowMedalReceivedScreen-2'],
        'source': 'src/profiles/extended/home/medal.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
