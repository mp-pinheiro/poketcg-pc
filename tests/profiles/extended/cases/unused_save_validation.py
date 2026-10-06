"""Extended oracle-diff cases for unused_save_validation, seeded from tests/cases/unused_save_validation.py."""

CONTRACT = {
}

CASES = {
}

MUTATIONS = {
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
