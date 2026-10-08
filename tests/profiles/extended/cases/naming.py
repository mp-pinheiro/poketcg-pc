"""Extended oracle-diff cases for naming: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('naming')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'DisplayPlayerNamingScreen': {   'source_symbol': 'DisplayPlayerNamingScreen',
        'before': '\tif (gb_read8(hl) == 0u)',
        'after': '\tif (gb_read8(hl) != 0u)',
        'case_ids': ['DisplayPlayerNamingScreen-0', 'DisplayPlayerNamingScreen-1'],
        'source': 'src/profiles/extended/home/naming.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
