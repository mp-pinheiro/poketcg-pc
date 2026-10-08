"""Extended oracle-diff cases for print_stats: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('print_stats', remove=('DrawCollectedMedals',))
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'PrintAlbumProgress': {   'source_symbol': 'PrintAlbumProgress',
        'before': 'PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e,\n'
                  '\t\t(uint16_t)(((uint16_t)prog.b << 8) | prog.c));',
        'after': 'PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e,\n'
                 '\t\t(uint16_t)(((uint16_t)(prog.b + 1u) << 8) | prog.c));',
        'case_ids': ['PrintAlbumProgress-0'],
        'source': 'src/profiles/extended/home/print_stats.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
