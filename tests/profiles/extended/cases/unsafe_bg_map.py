"""Extended oracle-diff cases for unsafe_bg_map, seeded from tests/cases/unsafe_bg_map.py."""

CONTRACT = {
}

CASES = {
}

MUTATIONS = {
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
