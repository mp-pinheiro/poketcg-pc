"""Extended oracle-diff cases for challenge_machine: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('challenge_machine', remove=('ChallengeMachine_GetCurrentOpponent',))
OWN = (
    'ChallengeMachine_GetCurrentOpponent',
    'ChallengeMachine_Start',
)
CONTRACT.update({
    'ChallengeMachine_GetCurrentOpponent': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c')},
    'ChallengeMachine_Start': {'compare': (), 'preserve': ()},
})
CASES.update({
    'ChallengeMachine_GetCurrentOpponent': [
        {   'sram': {0x00: {sym("sChallengeMachineOpponents"): b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n', sym("sChallengeMachineOpponentNumber"): b'\x00'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'sram': {0x00: {sym("sChallengeMachineOpponents"): b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n', sym("sChallengeMachineOpponentNumber"): b'\x03'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
        {   'sram': {0x00: {sym("sChallengeMachineOpponents"): b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99', sym("sChallengeMachineOpponentNumber"): b'\t'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
        {   'sram': {0x00: {sym("sChallengeMachineOpponents"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', sym("sChallengeMachineOpponentNumber"): b'\n'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
        {   'sram': {   0x00: {   sym("sChallengeMachineOpponents"): b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11',
                                  sym("sChallengeMachineOpponentNumber"): b'\xff',
                                  sym("sChallengeMachineEnd") + 0xE1: b'w'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
        {   'ramg': False,
            'sram': {0x00: {sym("sChallengeMachineOpponents"): b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n', sym("sChallengeMachineOpponentNumber"): b'\x02'}},
            'read': {sym("wChallengeMachineOpponent"): 0x01}},
    ],
    'ChallengeMachine_Start': [
        {   'rom_bank': 0x04,
            'sram': {0x00: {sym("sChallengeMachineMagic"): b'\xe3\x95', sym("sChallengeMachineStart"): b'\x00'}},
            'read': {sym("wLineSeparation"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'rom_bank': 0x04,
            'sram': {0x00: {sym("sChallengeMachineMagic"): b'\xe3\x95', sym("sChallengeMachineStart"): b'\x00'}},
            'read': {sym("wLineSeparation"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
})
MUTATIONS.update({
    'ChallengeMachine_GetCurrentOpponent': {   'source_symbol': 'ChallengeMachine_GetCurrentOpponent',
        'before': '\tuint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e);',
        'after': '\tuint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e + 1u);',
        'case_ids': [   'ChallengeMachine_GetCurrentOpponent-0',
                        'ChallengeMachine_GetCurrentOpponent-1',
                        'ChallengeMachine_GetCurrentOpponent-2'],
        'source': 'src/home/challenge_machine.c'},
    'ChallengeMachine_Start': {   'source_symbol': 'ChallengeMachine_Start',
        'before': 'void ChallengeMachine_Start(void)\n{\n\twLineSeparation = DOUBLE_SPACED;',
        'after': 'void ChallengeMachine_Start(void)\n{\n\twLineSeparation = 0x01u;',
        'case_ids': ['ChallengeMachine_Start-0', 'ChallengeMachine_Start-1'],
        'source': 'src/profiles/extended/home/challenge_machine.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _record in SCHEMA2_CASES["ChallengeMachine_Start"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("ChallengeMachine_Start") + 0x1A, "bank": sym_bank("ChallengeMachine_Start")}
