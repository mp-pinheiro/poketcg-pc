"""Extended oracle-diff cases for pokemon_dome: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('pokemon_dome')
OWN = (
    'PokemonDomeLoadMap',
)
CONTRACT.update({
    'PokemonDomeLoadMap': {'compare': (), 'preserve': (), 'wram_out': True},
})
CASES.update({
    'PokemonDomeLoadMap': [
        {   'wram': {   sym("wEventVars") + 0x17: b'\x00',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {sym("wPCPacks"): 0x0F, sym("wNextScript"): 0x02, sym("wLoadedEventBits"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wEventVars") + 0x17: b'\x08',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {sym("wPCPacks"): 0x0F, sym("wNextScript"): 0x02, sym("wLoadedEventBits"): 0x01}},
        {   'a': 0x77,
            'f': 0x10,
            'b': 0x98,
            'c': 0x00,
            'd': 0xD3,
            'e': 0x04,
            'hl': 0x7706,
            'wram': {sym("wEventVars") + 0x17: b'\x08',
                     sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {sym("wPCPacks"): 0x0F, sym("wNextScript"): 0x02, sym("wLoadedEventBits"): 0x01},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800},
    ],
})
MUTATIONS.update({
    'PokemonDomeMovePlayer': {   'source_symbol': 'PokemonDomeMovePlayer',
        'before': '\tif (gb_read8(wPlayerYCoord_ADDR) != 0x16u)',
        'after': '\tif (gb_read8(wPlayerYCoord_ADDR) != 0x00u)',
        'case_ids': ['PokemonDomeMovePlayer-0',
                     'PokemonDomeMovePlayer-1',
                     'PokemonDomeMovePlayer-2',
                     'PokemonDomeMovePlayer-3'],
        'source': 'src/profiles/extended/home/pokemon_dome.c'},
    'PokemonDomeLoadMap': {   'source_symbol': 'PokemonDomeLoadMap',
        'before': '\tif (GetEventValue(EVENT_POKEMON_DOME_IN_MENU) == 0u)\n\t\treturn;',
        'after': '\tif ((uint8_t)((gb_read8(0xD3E9u) & 0x08u) >> 3) == 0u)\n\t\treturn;',
        'case_ids': ['PokemonDomeLoadMap-2'],
        'source': 'src/profiles/extended/home/pokemon_dome.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
