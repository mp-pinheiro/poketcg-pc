"""Extended oracle-diff cases for hall_of_honor: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('hall_of_honor', remove=('HallOfHonorLoadMap',))
OWN = ('HallOfHonorLoadMap',)
CONTRACT.update({
    'HallOfHonorLoadMap': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
})
CASES.update({
    'HallOfHonorLoadMap': [
        {'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
        {'wram': {sym("wCurSfxID"): b'\xff', sym("wMusicStereoPanning"): b'\xff'}, 'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
    ],
})
MUTATIONS.update({
    'HallOfHonorLoadMap': {   'source_symbol': 'HallOfHonorLoadMap',
        'before': 'PlaySFX(SFX_LEGENDARY_CARDS)',
        'after': 'PlaySFX(0x11u)',
        'case_ids': ['HallOfHonorLoadMap-0', 'HallOfHonorLoadMap-1', 'HallOfHonorLoadMap-2'],
        'source': 'src/home/hall_of_honor.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
