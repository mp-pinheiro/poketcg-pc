"""Extended oracle-diff cases for time: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('time')
OWN = (
    'SwitchToCGBDoubleSpeed',
)
CONTRACT.update({
    'SwitchToCGBDoubleSpeed': {'compare': (), 'preserve': (), 'wram_out': True},
})
CASES.update({
    'SwitchToCGBDoubleSpeed': [
        {   'wram': {sym("wConsole"): b'\x00',
                     0xFF4D: b'\x7e', 0xFFFF: b'\x05',
                     0xFF06: b'\x00', 0xFF07: b'\x00',
                     0xFF0F: b'\x00', 0xFF00: b'\x00'},
            'read': {0xFF4D: 1, 0xFF06: 1, 0xFF07: 1, 0xFF0F: 1, 0xFF00: 1, 0xFFFF: 1},
        },
    ],
})
MUTATIONS.update({
    'SwitchToCGBDoubleSpeed': {
        'source_symbol': 'SwitchToCGBDoubleSpeed',
        'before': 'void SwitchToCGBDoubleSpeed(void)\n{',
        'after': 'void SwitchToCGBDoubleSpeed(void)\n{\n\tif ((CheckForCGB() & 0x10u) != 0u) return;',
        'case_ids': ['SwitchToCGBDoubleSpeed-0'],
        'source': 'src/home/time.c',
    },
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
