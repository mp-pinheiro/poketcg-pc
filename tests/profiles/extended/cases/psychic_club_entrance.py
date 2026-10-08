"""Extended oracle-diff cases for psychic_club_entrance: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('psychic_club_entrance', remove=('TryFirstRonaldEncounter',))
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'LoadClubEntrance': {   'source_symbol': 'LoadClubEntrance',
        'before': '\twTempNPC = NPC_RONALD1;',
        'after': '\twTempNPC = NPC_RONALD2;',
        'case_ids': ['LoadClubEntrance-0', 'LoadClubEntrance-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
