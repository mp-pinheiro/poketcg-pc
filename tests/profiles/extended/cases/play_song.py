"""Extended oracle-diff cases for play_song, seeded from tests/cases/play_song.py."""

CONTRACT = {
    'ScriptPlaySong': {'compare': ('hl',), 'preserve': ('hl',)},
    'WaitForSongToFinish': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'ScriptPlaySong': [
        {'a': 0x00, 'read': {0xD7A4: 0x01}},
        {'a': 0x1D, 'read': {0xD7A4: 0x01}},
        {'a': 0x1E, 'read': {0xD7A4: 0x01}},
        {   'a': 0x0F,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD7A4: 0x01}},
    ],
    'WaitForSongToFinish': [
        {'wram': {0xD7A4: b'\x80', 0xFF40: b'\x00'}, 'read': {0xD7A4: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD7A4: b'\x80', 0xFF40: b'\x00'},
            'read': {0xD7A4: 0x01}},
    ],
}

MUTATIONS = {
    'ScriptPlaySong': {   'source_symbol': 'ScriptPlaySong',
        'before': '{\n\tPlaySong(a);',
        'after': '{\n\tPlaySong((uint8_t)(a + 1u));',
        'case_ids': [   'ScriptPlaySong-0',
                        'ScriptPlaySong-1',
                        'ScriptPlaySong-2',
                        'ScriptPlaySong-3'],
        'source': 'src/profiles/extended/home/play_song.c'},
    'WaitForSongToFinish': {   'source_symbol': 'WaitForSongToFinish',
        'before': 'void WaitForSongToFinish(void)\n{',
        'after': 'void WaitForSongToFinish(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['WaitForSongToFinish-0'],
        'source': 'src/profiles/extended/home/play_song.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
