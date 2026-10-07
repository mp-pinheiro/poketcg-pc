"""Extended oracle-diff cases for medal, seeded from tests/cases/medal.py."""

CONTRACT = {
    'ShowMedalReceivedScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    'ShowMedalReceivedScreen': [
        {   'a': 0x08,
            'keys': [0x00, 0x01],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD101: 0x03, 0xCE05: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x0F,
            'keys': [0x00, 0x01],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD101: 0x03, 0xCE05: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x0A,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD101: 0x03, 0xCE05: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
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
for _record in SCHEMA2_CASES["ShowMedalReceivedScreen"]:
    _record["completion"] = {"mode": "entry", "pc": 0x2DFC, "bank": 0, "routine": "AssertSongFinished"}
