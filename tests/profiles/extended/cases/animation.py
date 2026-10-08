"""Extended oracle-diff cases for animation: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('animation')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'DoMapOWFrame': {   'source_symbol': 'DoMapOWFrame',
        'before': '\tuint8_t c = (uint8_t)(map * 2u);',
        'after': '\tuint8_t c = (uint8_t)(map * 2u + 1u);',
        'case_ids': ['DoMapOWFrame-0', 'DoMapOWFrame-1'],
        'source': 'src/profiles/extended/home/animation.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
