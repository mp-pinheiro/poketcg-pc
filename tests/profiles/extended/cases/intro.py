"""Extended oracle-diff cases for intro: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('intro')
OWN = (
    'PlayIntroSequence',
)
CONTRACT.update({
    'PlayIntroSequence': {'compare': (), 'preserve': ()},
})
CASES.update({
    'PlayIntroSequence': [
        {   'completion': {'mode': 'entry', 'pc': sym("DoFrameIfLCDEnabled"), 'bank': sym_bank("DoFrameIfLCDEnabled"), 'routine': 'DoFrameIfLCDEnabled'},
            'wram': {sym("wSequenceCmdPtr"): b'\x00\x00', sym("wd317"): b'\xff', sym("wIntroSequencePalsNeedUpdate"): b'\xff', sym("wSequenceDelay"): b'\xff'},
            'read': {sym("wSequenceCmdPtr"): 0x02, sym("wd317"): 0x01, sym("wIntroSequencePalsNeedUpdate"): 0x01, sym("wSequenceDelay"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': sym("DoFrameIfLCDEnabled"), 'bank': sym_bank("DoFrameIfLCDEnabled"), 'routine': 'DoFrameIfLCDEnabled'},
            'wram': {sym("wSequenceCmdPtr"): b'\x00\x00', sym("wd317"): b'\xff', sym("wIntroSequencePalsNeedUpdate"): b'\xff', sym("wSequenceDelay"): b'\xff'},
            'read': {sym("wSequenceCmdPtr"): 0x02, sym("wd317"): 0x01, sym("wIntroSequencePalsNeedUpdate"): 0x01, sym("wSequenceDelay"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
})
MUTATIONS.update({
    'PlayIntroSequence': {   'source_symbol': 'PlayIntroSequence',
        'before': '\twd317 = 0u;',
        'after': '\twd317 = 0xFFu;',
        'case_ids': ['PlayIntroSequence-0', 'PlayIntroSequence-1'],
        'source': 'src/profiles/extended/home/intro.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
