"""Extended oracle-diff cases for mail: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('mail')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'GetPCPackNameTextID': {   'source_symbol': 'GetPCPackNameTextID',
        'before': 'uint16_t GetPCPackNameTextID(uint8_t a)\n'
                  '{\n'
                  '\treturn kPCPackNameTextIDs[a];\n'
                  '}',
        'after': 'uint16_t GetPCPackNameTextID(uint8_t a)\n'
                 '{\n'
                 '\treturn kPCPackNameTextIDs[(uint8_t)(a + 1u)];\n'
                 '}',
        'case_ids': ['GetPCPackNameTextID-0', 'GetPCPackNameTextID-1', 'GetPCPackNameTextID-2'],
        'source': 'src/profiles/extended/home/mail.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
