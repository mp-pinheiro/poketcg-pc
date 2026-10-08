"""Extended oracle-diff cases for duel_init: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('duel_init')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'Duel_Init': {   'source_symbol': 'Duel_Init',
        'before': '\twTextBoxFrameType = 1u;',
        'after': '\twTextBoxFrameType = 0u;',
        'case_ids': ['Duel_Init-0', 'Duel_Init-1', 'Duel_Init-2', 'Duel_Init-3'],
        'source': 'src/profiles/extended/home/duel_init.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
