"""Extended oracle-diff cases for pokemon_dome_entrance, seeded from tests/cases/pokemon_dome_entrance.py."""

CONTRACT = {
    'PokemonDomeEntranceLoadMap': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'PokemonDomeEntranceCloseTextBox': {'compare': (), 'preserve': ()},
    'Script_f631.ows_f63c': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Script_f631': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('a', 'f', 'b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'PokemonDomeEntranceLoadMap': [
        {'wram': {0xD3D8: b'\xff', 0xD3D9: b'\xff', 0xD3DA: b'\xff', 0xD3C7: b'\x00'}},
        {'wram': {0xD3D8: b'\x08', 0xD3D9: b'\xff', 0xD3DA: b'\xff', 0xD3C7: b'\x02'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3D8: b'\x00', 0xD3D9: b'\xff', 0xD3DA: b'\xff', 0xD3C7: b'\x00'}},
    ],
    'PokemonDomeEntranceCloseTextBox': [
        {   'wram': {0xD310: b'\xff\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD310: 0x02, 0xD120: 0x0100}},
        {   'wram': {0xD310: b'\x02\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD310: 0x02, 0xD120: 0x0100}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD310: b'\x03\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD310: 0x02, 0xD120: 0x0100}},
    ],
    'Script_f631.ows_f63c': [
        {'wram': {0xD3CB: b'\x00'}, 'read': {0xD3CB: 0x01, 0xCE09: 0x02, 0xCE0B: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xD3CB: 0x01, 0xCE09: 0x02, 0xCE0B: 0x02}},
        {   'a': 0x3C,
            'f': 0x00,
            'b': 0x76,
            'c': 0x3B,
            'd': 0x1E,
            'e': 0x11,
            'hl': 0x763C,
            'read': {0xD3CB: 0x01, 0xCE09: 0x02, 0xCE0B: 0x02}},
    ],
    'Script_f631': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'read': {0xCE09: 0x04}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xCE09: 0x04}},
    ],
}

MUTATIONS = {
    'PokemonDomeEntranceLoadMap': {   'source_symbol': 'PokemonDomeEntranceLoadMap',
        'before': 'ZeroOutEventValue(EVENT_POKEMON_DOME_STATE',
        'after': 'ZeroOutEventValue(EVENT_HALL_OF_HONOR_DOORS_OPEN',
        'case_ids': ['PokemonDomeEntranceLoadMap-0'],
        'source': 'src/home/pokemon_dome_entrance.c'},
    'PokemonDomeEntranceCloseTextBox': {   'source_symbol': 'PokemonDomeEntranceCloseTextBox',
        'before': '\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_POKEMON_DOME_DOOR);',
        'after': '\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_POKEMON_DOME_DOOR + 1u));',
        'case_ids': ['PokemonDomeEntranceCloseTextBox-0', 'PokemonDomeEntranceCloseTextBox-1'],
        'source': 'src/home/pokemon_dome_entrance.c'},
    'Script_f631.ows_f63c': {   'source_symbol': 'Script_f631_ows_f63c',
        'before': '\twTxRam3_b = (uint8_t)(count + 1u);',
        'after': '\twTxRam3_b = count;',
        'case_ids': ['Script_f631.ows_f63c-0', 'Script_f631.ows_f63c-1', 'Script_f631.ows_f63c-2'],
        'source': 'src/home/pokemon_dome_entrance.c'},
    'Script_f631': {   'source_symbol': 'Script_f631',
        'before': 'void Script_f631(void)\n{\n}',
        'after': 'void Script_f631(void)\n{\n\twTxRam3 = 1u;\n}',
        'case_ids': ['Script_f631-0', 'Script_f631-1'],
        'source': 'src/home/pokemon_dome_entrance.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record in SCHEMA2_CASES["Script_f631"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x7499, "bank": 3}
for _record in SCHEMA2_CASES["Script_f631.ows_f63c"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x74B9, "bank": 3}
