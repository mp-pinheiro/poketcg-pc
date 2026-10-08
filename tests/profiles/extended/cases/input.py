"""Extended oracle-diff cases for input: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('input')
OWN = (
    'ReadJoypad',
    'Reset',
)
CONTRACT.update({
    'ReadJoypad': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'Reset': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    'ReadJoypad': [
        {'wram': {sym("hDPadRepeat"): b'\x00\x00\x00\x00\x00'}, 'read': {sym("hDPadRepeat"): 0x05}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hDPadRepeat"): b'\x124Vx\x9a'},
            'read': {sym("hDPadRepeat"): 0x05}},
        {'keys': 0x01, 'wram': {sym("hDPadRepeat"): b'\x00\x00\x00\x00\x00'}, 'read': {sym("hDPadRepeat"): 0x05}},
        {'oracle': False,
         'why': 'The seeded A+B+Start+Select held-button state takes ReadJoypad into the non-returning Reset jump.',
         'wram': {sym("hDPadRepeat"): b'\x00\x00\x00\x0f\x00'},
         'read': {sym("hDPadRepeat"): 0x05},
         'expect': {sym("hDPadRepeat"): b'\x00\x0f\x00\x0f\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'oracle': False,
            'why': 'The poisoned held-button state takes ReadJoypad into the non-returning Reset jump.',
            'wram': {sym("hDPadRepeat"): b'\x00\x00\x00\x0f\x00'},
            'read': {sym("hDPadRepeat"): 0x05},
            'expect': {sym("hDPadRepeat"): b'\x00\x0f\x00\x0f\x00'}},
    ],
    'Reset': [
        {'completion': {'mode': 'entry', 'pc': sym("Start"), 'bank': sym_bank("Start"), 'routine': 'Start'},
         'wram': {sym("wInitialA"): b'7'},
         'read': {sym("wInitialA"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("Start"), 'bank': sym_bank("Start"), 'routine': 'Start'},
            'wram': {sym("wInitialA"): b'\xc3'},
            'read': {sym("wInitialA"): 0x01}},
    ],
})
MUTATIONS.update({
    'ReadJoypad': {'source_symbol': 'ReadJoypad', 'before': '\tgb_write8(hKeysReleased_ADDR, (uint8_t)((held ^ c) & (uint8_t)~c));', 'after': '\tgb_write8(hKeysReleased_ADDR, (uint8_t)(((uint8_t)((held ^ c) & (uint8_t)~c)) ^ 1u));', 'case_ids': ['ReadJoypad-0'], 'source': 'src/profiles/extended/home/input.c'},
    'Reset': {   'source_symbol': 'Reset',
        'before': '\twInitialA = initial_a;',
        'after': '\twInitialA = 0u;',
        'case_ids': ['Reset-0'],
        'source': 'src/profiles/extended/home/input.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
