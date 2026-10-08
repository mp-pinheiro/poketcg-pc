"""Extended oracle-diff cases for game_loop: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('game_loop')
OWN = (
    'GameLoop',
)
CONTRACT.update({
    'GameLoop': {'compare': (), 'preserve': ()},
})
CASES.update({
    'GameLoop': [
        {   'completion': {'mode': 'entry', 'pc': sym("_GameLoop"), 'bank': sym_bank("_GameLoop"), 'routine': '_GameLoop'},
            'wram': {sym("wConsole"): b'\x02', sym("hKeysHeld"): b'\x00', sym("wTextSpeed"): b'\xff', sym("wSkipDelayAllowed"): b'\xff', sym("wUppercaseHalfWidthLetters"): b'\xff'},
            'sram': {0x00: {sym("sTextSpeed"): b'\x02', sym("sSkipDelayAllowed"): b'\x01'}},
            'read': {sym("wTextSpeed"): 0x01, sym("wSkipDelayAllowed"): 0x01, sym("wUppercaseHalfWidthLetters"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("_GameLoop"), 'bank': sym_bank("_GameLoop"), 'routine': '_GameLoop'},
            'wram': {sym("wConsole"): b'\x02', sym("hKeysHeld"): b'\x00', sym("wTextSpeed"): b'\xff', sym("wSkipDelayAllowed"): b'\xff', sym("wUppercaseHalfWidthLetters"): b'\xff'},
            'sram': {0x00: {sym("sTextSpeed"): b'\x06', sym("sSkipDelayAllowed"): b'\x00'}},
            'read': {sym("wTextSpeed"): 0x01, sym("wSkipDelayAllowed"): 0x01, sym("wUppercaseHalfWidthLetters"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
})
MUTATIONS.update({
    'GameLoop': {   'source_symbol': 'GameLoop',
        'before': '\twUppercaseHalfWidthLetters = 1u;',
        'after': '\twUppercaseHalfWidthLetters = 0u;',
        'case_ids': ['GameLoop-0', 'GameLoop-1'],
        'source': 'src/profiles/extended/home/game_loop.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
