"""Extended oracle-diff cases for credits_sequence_commands: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('credits_sequence_commands')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
