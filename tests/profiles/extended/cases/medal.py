"""Extended oracle-diff cases for medal: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('medal')
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
for _record in SCHEMA2_CASES["ShowMedalReceivedScreen"]:
    _record["completion"] = {"mode": "entry", "pc": sym("AssertSongFinished"), "bank": sym_bank("AssertSongFinished"), "routine": "AssertSongFinished"}
