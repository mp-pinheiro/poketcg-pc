"""Extended oracle-diff cases for default_palettes: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('default_palettes')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'SetDefaultPalettes': {   'source_symbol': 'SetDefaultPalettes',
        'before': 'gb_write8(wOBP1_ADDR, 0xE4u);',
        'after': 'gb_write8(wOBP1_ADDR, 0xE5u);',
        'case_ids': ['SetDefaultPalettes-0', 'SetDefaultPalettes-1', 'SetDefaultPalettes-2'],
        'source': 'src/profiles/extended/home/default_palettes.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
