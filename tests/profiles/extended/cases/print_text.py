"""Extended oracle-diff cases for print_text: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._fixtures import SCROLL_LABEL_REGS, scroll_label_fixture
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('print_text')

OWN = (
    'PrintScrollableText_WithTextBoxLabel',
)
CASES["PrintScrollableText_WithTextBoxLabel"].append(
    dict(scroll_label_fixture(vram=False), **SCROLL_LABEL_REGS, keys=[0x00, 0x01])
)
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
