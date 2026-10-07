"""Extended oracle-diff cases for ai, seeded from tests/cases/ai.py."""
from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_AIDO = Fixture("ai-duel-fire-charge-aidoaction-entry", directory=_FIXTURES)
_AIDO_START = Fixture("ai-duel-fire-charge-aidoaction-startduel-entry", directory=_FIXTURES)
_AIDO_TURN = Fixture("ai-duel-fire-charge-aidoaction-turn-entry", directory=_FIXTURES)
from tests.profiles.extended.cases.overworld import CASES as _OVERWORLD_CASES

def _extended_ai_wram():
    source = _OVERWORLD_CASES['Func_c17a'][2]['wram']
    clipped = {}
    for address, data in source.items():
        if address == 0xCE4E:
            clipped[address] = data[:0xB2]
            clipped[0xD000] = data[0xB2:]
        elif address == 0xD001:
            clipped[address] = data[:0xC2F]
        elif address == 0xDCEE:
            clipped[0xDD00] = data[0x12:]
        else:
            clipped[address] = data
    clipped[0xCAD3] = b'\x00\x00'
    return clipped

_AI_WIDE_WRAM = _extended_ai_wram()

CONTRACT = {
    'LoadOpponentDeck': {'compare': ('a', 'hl'), 'preserve': ()},
    'AIDoAction': {'compare': ('a',), 'preserve': ()},
    'AIDoAction_ForcedSwitch': {'compare': ('a',), 'preserve': ()},
    'AIDoAction_KOSwitch': {'compare': ('a',), 'preserve': ()},
    'AIDoAction_StartDuel': {'compare': ('a',), 'preserve': ()},
    'AIDoAction_TakePrize': {'compare': ('a',), 'preserve': ()},
    'AIDoAction_Turn': {'compare': ('a',), 'preserve': ()},
}

CASES = {
    'LoadOpponentDeck': [
        {   'wram': {0xFF97: b'\xc2', 0xCBB8: b'\x02'},
            'read': {   0xCBBE: 0x01,
                        0xCBB8: 0x01,
                        0xCACA: 0x01,
                        0xCACB: 0x01,
                        0xCACC: 0x01,
                        0xC478: 0x3C,
                        0xC400: 0x3C,
                        0xCC97: 0x02,
                        0xC2F1: 0x01}},
        {   'wram': {0xFF97: b'\xc3', 0xCBB8: b'\x00'},
            'read': {   0xCBBE: 0x01,
                        0xCBB8: 0x01,
                        0xCACA: 0x01,
                        0xCACB: 0x01,
                        0xCACC: 0x01,
                        0xC478: 0x3C,
                        0xC400: 0x3C,
                        0xCC97: 0x02,
                        0xC3F1: 0x01}},
        {   'wram': {0xFF97: b'\xc2', 0xCBB8: b'\x05'},
            'read': {0xCBBE: 0x01, 0xCBB8: 0x01, 0xC400: 0x3C, 0xCC97: 0x02, 0xC2F1: 0x01}},
        {'wram': {0xFF97: b'\xc3', 0xCBB8: b'5'}, 'read': {0xCBB8: 0x01, 0xC3F1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xCBB8: b'\t'},
            'read': {0xCBBE: 0x01, 0xCBB8: 0x01, 0xC400: 0x3C, 0xCC97: 0x02, 0xC2F1: 0x01}},
        {   'oracle': False,
            'why': 'deck_id=54 clamp forces a LoadDeck(56) read of raw code as deck data '
                   '(DeckPointers[56]=$0614, fixed bank 0) -- an unbounded copy loop that would '
                   'corrupt WRAM broadly on real hardware too, not something safe to run through the '
                   'oracle.',
            'wram': {0xFF97: b'\xc2', 0xCBB8: b'6'},
            'expect': {0xCBB8: b'\x01', 0xC2F1: b'\x81'},
            'expect_regs': {'a': 0x81}},
    ],
    'AIDoAction': [
        {'a': 0x01, 'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
        {'a': 0x04, 'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
        {'a': 0x05, 'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
        {'a': 0x03, 'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
    ],
    'AIDoAction_ForcedSwitch': [
        {'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2'}, 'read': {0xFF9D: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2'},
            'read': {0xFF9D: 0x01}},
    ],
    'AIDoAction_KOSwitch': [
        {'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2'}, 'read': {0xFFA0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2'},
            'read': {0xFFA0: 0x01}},
    ],
    'AIDoAction_StartDuel': [
        {'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2', 0xC2BA: b'\x00'}, 'expect_regs': {'a': 0xFF}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBB8: b'\x01', 0xFF97: b'\xc2', 0xC2BA: b'\x00'},
            'expect_regs': {'a': 0xFF}},
    ],
    'AIDoAction_TakePrize': [
        {   'wram': {   0xFF97: b'\xc3',
                        0xCC76: b'\x01',
                        0xC3EC: b'?',
                        0xC3EE: b'\x00',
                        0xC33C: b'\x00\x00\x00\x00\x00\x00',
                        0xCBB8: b'\x01'},
            'read': {0xC3EC: 0x01, 0xC3EE: 0x01, 0xC342: 0x01},
            'expect_regs': {'a': 0x05},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc3',
                        0xCC76: b'\x01',
                        0xC3EC: b'?',
                        0xC3EE: b'\x00',
                        0xC33C: b'\x00\x00\x00\x00\x00\x00',
                        0xCBB8: b'\x01'},
            'read': {0xC3EC: 0x01, 0xC3EE: 0x01, 0xC342: 0x01},
            'expect_regs': {'a': 0x05},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'AIDoAction_Turn': [
        {'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': _AI_WIDE_WRAM, 'keys': [0x00, 0x01]},
    ],
}
CASES['AIDoAction'].append(dict(_AIDO.case(vram=False), **_AIDO.regs))
CASES['AIDoAction_StartDuel'].append(dict(_AIDO_START.case(vram=False), **_AIDO_START.regs))
CASES['AIDoAction_Turn'].append(dict(_AIDO_TURN.case(vram=False), **_AIDO_TURN.regs))
CASES['AIDoAction'] = [
    dict(_AIDO.case(vram=False), **_AIDO.regs)
]
CASES['AIDoAction_Turn'] = [
    dict(_AIDO_TURN.case(vram=False), **_AIDO_TURN.regs)
]

MUTATIONS = {
    'LoadOpponentDeck': {   'source_symbol': 'LoadOpponentDeck',
        'before': '\t\t\twIsPracticeDuel = 1;',
        'after': '\t\t\twIsPracticeDuel = 0;',
        'case_ids': ['LoadOpponentDeck-1', 'LoadOpponentDeck-4'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction': {   'source_symbol': 'AIDoAction',
        'before': '\t\tcase AIACTION_DO_TURN:\n'
                  '\t\t\tif (sam && sam_scripted())\n'
                  '\t\t\t\t(void)AIPerformScriptedTurn(0u, 0u, 0u, 0u, 0u, 0u, 0u);',
        'after': '\t\tcase AIACTION_DO_TURN:\n'
                 '\t\t\tif (sam && sam_scripted())\n'
                 '\t\t\t\t(void)AIMainTurnLogic(0u, 0u, 0u, 0u, 0u, 0u, 0u);',
        'case_ids': ['AIDoAction-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_ForcedSwitch': {   'source_symbol': 'AIDoAction_ForcedSwitch',
        'before': 'uint8_t AIDoAction_ForcedSwitch(void)\n'
                  '{\n'
                  '\tuint8_t result = AIDoAction(0x03u);\n'
                  '\thTempPlayAreaLocation_ff9d = result;',
        'after': 'uint8_t AIDoAction_ForcedSwitch(void)\n'
                 '{\n'
                 '\tuint8_t result = AIDoAction(0x03u);\n'
                 '\thTempPlayAreaLocation_ff9d = (uint8_t)(result ^ 0xFFu);',
        'case_ids': ['AIDoAction_ForcedSwitch-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_KOSwitch': {   'source_symbol': 'AIDoAction_KOSwitch',
        'before': 'uint8_t AIDoAction_KOSwitch(void)\n'
                  '{\n'
                  '\tuint8_t result = AIDoAction(AIACTION_KO_SWITCH);\n'
                  '\thTemp_ffa0 = result;',
        'after': 'uint8_t AIDoAction_KOSwitch(void)\n'
                 '{\n'
                 '\tuint8_t result = AIDoAction(AIACTION_KO_SWITCH);\n'
                 '\thTemp_ffa0 = (uint8_t)(result ^ 0xFFu);',
        'case_ids': ['AIDoAction_KOSwitch-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_StartDuel': {   'source_symbol': 'AIDoAction_StartDuel',
        'before': 'uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x02u);',
        'after': 'uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x01u);',
        'case_ids': ['AIDoAction_StartDuel-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_TakePrize': {   'source_symbol': 'AIDoAction_TakePrize',
        'before': 'uint8_t AIDoAction_TakePrize(void)\n'
                  '{\n'
                  '\treturn AIDoAction(AIACTION_TAKE_PRIZE);',
        'after': 'uint8_t AIDoAction_TakePrize(void)\n{\n\treturn AIDoAction(0x03u);',
        'case_ids': ['AIDoAction_TakePrize-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_Turn': {   'source_symbol': 'AIDoAction_Turn',
        'before': 'uint8_t AIDoAction_Turn(void)\n{\n\treturn AIDoAction(AIACTION_DO_TURN);',
        'after': 'uint8_t AIDoAction_Turn(void)\n{\n\treturn AIDoAction(AIACTION_KO_SWITCH);',
        'case_ids': ['AIDoAction_Turn-0'],
        'source': 'src/profiles/extended/home/ai.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
SCHEMA2_CASES["AIDoAction_Turn"][0]["completion"] = {
    "mode": "entry",
    "pc": 0x466F,
    "bank": 5,
    "routine": "AIProcessHandTrainerCards",
}
SCHEMA2_CASES["AIDoAction_Turn"][0]["compare"] = ()
for _name, _records in SCHEMA2_CASES.items():
    for _index, _record in enumerate(_records):
        if isinstance(_record.get("completion"), dict) and _record["completion"].get("mode") == "entry":
            CASES[_name][_index]["completion"] = _record["completion"]
        if "compare" in _record and _record["compare"] != CONTRACT[_name]["compare"]:
            CASES[_name][_index]["compare"] = _record["compare"]
