"""Extended oracle-diff cases for text_box: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('text_box', remove=(
    'ContinueDrawingTextBoxDMGorSGB',
    'DrawRegularTextBoxDMG',
))
OWN = (
    'ContinueDrawingTextBoxDMG',
)
CONTRACT.update({
    'ContinueDrawingTextBoxDMG': {'compare': ('b', 'hl'), 'preserve': ('b',)},
})
CASES.update({
    'ContinueDrawingTextBoxDMG': [
        {'b': 0x04, 'c': 0x03, 'hl': 0x9800, 'read': {0x9800: 0x40}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0x04, 'c': 0x04, 'd': 0xDD, 'e': 0xEE,
         'hl': 0x9800, 'read': {0x9800: 0x60}},
    ],
})
MUTATIONS.update({
    'DrawRegularTextBox': {   'source_symbol': 'DrawRegularTextBox',
        'before': '\tdraw_line(hl, SYM_BOX_TOP, SYM_BOX_TOP_L, SYM_BOX_TOP_R, b);',
        'after': '\tdraw_line(hl, SYM_BOX_TOP, SYM_BOX_TOP_L, SYM_BOX_TOP_L, b);',
        'case_ids': ['DrawRegularTextBox-0'],
        'source': 'src/profiles/extended/home/text_box.c'},
    'ContinueDrawingTextBoxDMG': {   'source_symbol': 'ContinueDrawingTextBoxDMG',
        'before': '\tdraw_line(hl, 0x1du, 0x1au, 0x1bu, b);',
        'after': '\tdraw_line(hl, 0x1eu, 0x1au, 0x1bu, b);',
        'case_ids': ['ContinueDrawingTextBoxDMG-0'],
        'source': 'src/profiles/extended/home/text_box.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
