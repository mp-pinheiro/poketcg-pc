"""Extended oracle-diff cases for damage_calculation: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import WRAMX_START, sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('damage_calculation')
OWN = (
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
    'CalculateDamage_FromDefendingPokemon': {   'source_symbol': 'CalculateDamage_FromDefendingPokemon',
        'before': '    if (damage & (1u << (UNAFFECTED_BY_WEAKNESS_RESISTANCE_F + 8u))) {\n'
                  '        damage = (uint16_t)(damage & ~(uint16_t)(1u << '
                  '(UNAFFECTED_BY_WEAKNESS_RESISTANCE_F + 8u)));',
        'after': '    if (damage & (1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)) {\n'
                 '        damage = (uint16_t)(damage & ~(uint16_t)(1u << '
                 'UNAFFECTED_BY_WEAKNESS_RESISTANCE_F));',
        'case_ids': ['CalculateDamage_FromDefendingPokemon-2'],
        'source': 'src/profiles/extended/home/damage_calculation.c'},
    'EstimateDamage_VersusDefendingCard': {   'source_symbol': 'EstimateDamage_VersusDefendingCard',
        'before': '\tgb_write8(wAIMinDamage_ADDR, damage);\n'
                  '\tgb_write8(wAIMaxDamage_ADDR, damage);\n'
                  '\t(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);',
        'after': '\tgb_write8(wAIMinDamage_ADDR, (uint8_t)(damage + 1u));\n'
                 '\tgb_write8(wAIMaxDamage_ADDR, damage);\n'
                 '\t(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);',
        'case_ids': [   'EstimateDamage_VersusDefendingCard-0',
                        'EstimateDamage_VersusDefendingCard-1',
                        'EstimateDamage_VersusDefendingCard-3'],
        'source': 'src/home/damage_calculation.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _records in ((_fn, SCHEMA2_CASES[_fn]) for _fn in OWN):
    for _index, _record in enumerate(_records):
        if isinstance(_record.get("completion"), dict) and _record["completion"].get("mode") == "entry":
            CASES[_name][_index]["completion"] = _record["completion"]
        if "compare" in _record and _record["compare"] != CONTRACT[_name]["compare"]:
            CASES[_name][_index]["compare"] = _record["compare"]
