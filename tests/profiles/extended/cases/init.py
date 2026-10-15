"""Extended oracle-diff cases for init: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import card_id_bytes, sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('init')
OWN = (
    'InitAITurnVars',
)
CONTRACT.update({
})
CASES.update({
})
MUTATIONS.update({
})
CASES['InitAITurnVars'] = [
    *CASES['InitAITurnVars'],
    {'wram': {sym("hWhoseTurn"): b'\xC3', sym("wPlayerAttackingAttackIndex"): b'\x01',
              sym("wPlayerAttackingCardIndex"): b'\x00', sym("wPlayerDeck"): card_id_bytes(0x019D),
              sym("wAIBarrierFlagCounter"): b'\x00'},
     'read': {sym("wAIBarrierFlagCounter"): 1}},
]
MUTATIONS['InitAITurnVars'] = {
    'source': 'src/home/init.c', 'source_symbol': 'InitAITurnVars',
    'before': 'if (id == MEWTWO_LV53)', 'after': 'if ((uint8_t)id == MEWTWO_LV53)',
    'case_ids': ['InitAITurnVars-1'],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
