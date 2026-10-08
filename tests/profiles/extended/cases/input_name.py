"""Extended oracle-diff cases for input_name: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('input_name', remove=('PlaySFXConfirmOrCancel_Bank6',))
OWN = (
    'PlaySFXConfirmOrCancel_Bank6',
)
CONTRACT.update({
    'PlaySFXConfirmOrCancel_Bank6': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('a', 'f', 'b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    'PlaySFXConfirmOrCancel_Bank6': [
        {'a': 0x00, 'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
        {   'a': 0xFF,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
        {'a': 0x01, 'read': {sym("wCurSfxID"): 0x01, sym("wMusicStereoPanning"): 0x01}},
    ],
})
MUTATIONS.update({
    'PlaySFXConfirmOrCancel_Bank6': {   'source_symbol': 'PlaySFXConfirmOrCancel_Bank6',
        'before': '\tuint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;',
        'after': '\tuint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CONFIRM : SFX_CONFIRM;',
        'case_ids': ['PlaySFXConfirmOrCancel_Bank6-1'],
        'source': 'src/home/input_name.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
