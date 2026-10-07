"""Extended oracle-diff cases for sound, seeded from tests/cases/sound.py."""

CONTRACT = {
    'SetupSound': {'compare': (), 'preserve': ()},
    'PlaySong': {'compare': ('hl',), 'preserve': ('hl',)},
    'AssertSongFinished': {'compare': ('a',), 'preserve': ()},
    'AssertSFXFinished': {'compare': ('a',), 'preserve': ()},
    'PlaySFX_InvalidChoice': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'PlaySFX': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'PauseSong': {'compare': (), 'preserve': ()},
    'ResumeSong': {'compare': (), 'preserve': ()},
}

CASES = {
    'SetupSound': [
        {'read': {0xD7A4: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD7A4: 0x01}},
    ],
    'PlaySong': [
        {'a': 0x00, 'read': {0xD7A4: 0x01}},
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
    'AssertSongFinished': [
        {'wram': {0xD7A4: b'\x80'}},
        {'wram': {0xD7A4: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD7A4: b'\x80'}},
    ],
    'AssertSFXFinished': [
        {'wram': {0xD7A6: b'\x80'}},
        {'wram': {0xD7A6: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD7A6: b'\x80'}},
    ],
    'PlaySFX_InvalidChoice': [
        {'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
    ],
    'PlaySFX': [
        {'a': 0x00, 'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
        {'a': 0x01, 'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
        {   'a': 0x05,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD7A6: 0x01, 0xD7A7: 0x01}},
    ],
    'PauseSong': [
        {'wram': {0xD7A4: b'\x01'}, 'read': {0xD7A4: 0x01}},
    ],
    'ResumeSong': [
        {'wram': {0xD7A4: b'\x01'}, 'read': {0xD7A4: 0x01}},
    ],
}

MUTATIONS = {
    'SetupSound': {
        'source_symbol': 'SetupSound',
        'before': '\t_SetupSound();',
        'after': '\t_PauseSong();',
        'case_ids': ['SetupSound-0'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'PlaySong': {
        'source_symbol': 'PlaySong',
        'before': '\t_PlaySong(a);',
        'after': '\t_PlaySong(0u);',
        'case_ids': ['PlaySong-1'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'AssertSongFinished': {
        'source_symbol': 'AssertSongFinished',
        'before': '\tuint8_t result = _AssertSongFinished();',
        'after': '\tuint8_t result = _AssertSFXFinished();',
        'case_ids': ['AssertSongFinished-0'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'AssertSFXFinished': {
        'source_symbol': 'AssertSFXFinished',
        'before': '\tuint8_t result = _AssertSFXFinished();',
        'after': '\tuint8_t result = _AssertSongFinished();',
        'case_ids': ['AssertSFXFinished-0'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'PlaySFX_InvalidChoice': {
        'source_symbol': 'PlaySFX_InvalidChoice',
        'before': '\tPlaySFX(SFX_DENIED);',
        'after': '\tPlaySFX(0u);',
        'case_ids': ['PlaySFX_InvalidChoice-0'],
        'source': 'src/home/sound.c',
    },
    'PlaySFX': {
        'source_symbol': 'PlaySFX',
        'before': '\t_PlaySFX(a);',
        'after': '\t_PlaySFX(0u);',
        'case_ids': ['PlaySFX-1'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'PauseSong': {
        'source_symbol': 'PauseSong',
        'before': '\t_PauseSong();',
        'after': '\t_ResumeSong();',
        'case_ids': ['PauseSong-0'],
        'source': 'src/profiles/extended/home/sound.c',
    },
    'ResumeSong': {
        'source_symbol': 'ResumeSong',
        'before': '\t_ResumeSong();',
        'after': '\t_PauseSong();',
        'case_ids': ['ResumeSong-0'],
        'source': 'src/profiles/extended/home/sound.c',
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
