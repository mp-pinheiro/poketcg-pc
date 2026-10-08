"""Extended oracle-diff cases for fire_club_lobby: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('fire_club_lobby')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'FindExtraInteractableObjects': {'source_symbol': 'FindExtraInteractableObjects', 'before': '\tuint16_t de = 6u;', 'after': '\tuint16_t de = 0x7u;', 'case_ids': ['FindExtraInteractableObjects-0'], 'source': 'src/profiles/extended/home/fire_club_lobby.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
