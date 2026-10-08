"""Extended oracle-diff cases for deck_check: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('deck_check', remove=('PlaySFXConfirmOrCancel',))
OWN = (
    'PlaySFXConfirmOrCancel',
)
CONTRACT.update({
    'PlaySFXConfirmOrCancel': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('a', 'f', 'b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    'PlaySFXConfirmOrCancel': [
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
    'PlaySFXConfirmOrCancel': {   'source_symbol': 'PlaySFXConfirmOrCancel',
        'before': 'uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;',
        'after': 'uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CONFIRM : SFX_CONFIRM;',
        'case_ids': ['PlaySFXConfirmOrCancel-1'],
        'source': 'src/home/deck_check.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
