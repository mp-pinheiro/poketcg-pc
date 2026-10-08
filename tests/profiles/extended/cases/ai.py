"""Extended oracle-diff cases for ai: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from pathlib import Path
from tests.cases._fixtures import Fixture
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_AIDO = Fixture("ai-duel-fire-charge-aidoaction-entry", directory=_FIXTURES)
_AIDO_START = Fixture("ai-duel-fire-charge-aidoaction-startduel-entry", directory=_FIXTURES)
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('ai')
OWN = (
    'AIDoAction',
    'AIDoAction_StartDuel',
)
CONTRACT.update({
    'AIDoAction': {'compare': ('a',), 'preserve': ()},
})
CASES['AIDoAction_StartDuel'].append(dict(_AIDO_START.case(vram=False), **_AIDO_START.regs))
CASES['AIDoAction'] = [
    dict(_AIDO.case(vram=False), **_AIDO.regs)
]
MUTATIONS.update({
    'AIDoAction': {   'source_symbol': 'AIDoAction',
        'before': '\t\tcase AIACTION_DO_TURN:\n'
                  '\t\t\tif (sam && sam_scripted())\n'
                  '\t\t\t\t(void)AIPerformScriptedTurn(0u, 0u, 0u, 0u, 0u, 0u, 0u);',
        'after': '\t\tcase AIACTION_DO_TURN:\n'
                 '\t\t\tif (sam && sam_scripted())\n'
                 '\t\t\t\t(void)AIMainTurnLogic(0u, 0u, 0u, 0u, 0u, 0u, 0u);',
        'case_ids': ['AIDoAction-0'],
        'source': 'src/profiles/extended/home/ai.c'},
    'AIDoAction_StartDuel': {   'source_symbol': 'AIDoAction_StartDuel',
        'before': 'uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x02u);',
        'after': 'uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x01u);',
        'case_ids': ['AIDoAction_StartDuel-0'],
        'source': 'src/home/ai.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _records in ((_fn, SCHEMA2_CASES[_fn]) for _fn in OWN):
    for _index, _record in enumerate(_records):
        if isinstance(_record.get("completion"), dict) and _record["completion"].get("mode") == "entry":
            CASES[_name][_index]["completion"] = _record["completion"]
        if "compare" in _record and _record["compare"] != CONTRACT[_name]["compare"]:
            CASES[_name][_index]["compare"] = _record["compare"]
