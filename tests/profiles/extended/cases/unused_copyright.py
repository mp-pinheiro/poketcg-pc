"""Extended oracle-diff cases for unused_copyright, seeded from tests/cases/unused_copyright.py."""

CONTRACT = {
}

CASES = {
}

MUTATIONS = {
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
