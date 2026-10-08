"""Extended oracle-diff cases for grass_club: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('grass_club')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'Preload_NikkiInGrassClub': {   'source_symbol': 'Preload_NikkiInGrassClub',
        'before': 'if (a == NIKKI_IN_GRASS_CLUB)',
        'after': 'if (a != NIKKI_IN_GRASS_CLUB)',
        'case_ids': ['Preload_NikkiInGrassClub-0',
                     'Preload_NikkiInGrassClub-1',
                     'Preload_NikkiInGrassClub-2'],
        'source': 'src/profiles/extended/home/grass_club.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
