"""Extended oracle-diff cases for booster_packs: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_pointer
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('booster_packs')
OWN = (
    'GenerateBoosterEnergies',
    'GenerateFightingEnergy',
    'GenerateFireEnergy',
    'GenerateGrassEnergy',
    'GenerateLightningEnergy',
    'GeneratePsychicEnergy',
    'GenerateWaterEnergy',
)
CONTRACT.update({
    'GenerateTwoTypesEnergyBooster': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GenerateRandomEnergy': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'hl'),
    'wram_out': True},
    'GenerateRandomEnergyBooster': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'hl'),
    'wram_out': True},
    'GenerateFightingEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateFireEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateGrassEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateLightningEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GeneratePsychicEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateWaterEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateBoosterEnergies': {'compare': (), 'preserve': ()},
})
_BOOSTER_ENERGY_STATE = {sym("wTempCardCollection"): b'\x00' * 0x10, sym("wBoosterTempEnergiesDrawn"): b'\x00' * 0x16,
                         sym("wBoosterCurrentCard"): b'\x00\x00'}
_BOOSTER_ENERGY_READ = {sym("wTempCardCollection"): 0x10, sym("wBoosterTempEnergiesDrawn"): 0x16, sym("wBoosterCurrentCard"): 2}
CASES.update({
    'GenerateBoosterEnergies': [
        {'wram': {**_BOOSTER_ENERGY_STATE, sym("wBoosterData_EnergyFunctionPointer"): sym_pointer("GenerateGrassEnergy")},
         'read': dict(_BOOSTER_ENERGY_READ)},
        {'wram': {**_BOOSTER_ENERGY_STATE, sym("wBoosterData_EnergyFunctionPointer"): sym_pointer("GenerateEnergyBoosterLightningFire")},
         'read': dict(_BOOSTER_ENERGY_READ)},
        {'wram': {**_BOOSTER_ENERGY_STATE, sym("wBoosterData_EnergyFunctionPointer"): b'\x00\x00'},
         'read': dict(_BOOSTER_ENERGY_READ)},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {**_BOOSTER_ENERGY_STATE, sym("wBoosterData_EnergyFunctionPointer"): sym_pointer("GenerateRandomEnergy")},
         'read': dict(_BOOSTER_ENERGY_READ)},
    ],
})
CASES.update({
    'GenerateFightingEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE,
         'hl': 0x1234, 'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
    'GenerateFireEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
    'GenerateGrassEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
    'GenerateLightningEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
    'GeneratePsychicEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
    'GenerateWaterEnergy': [
        {'wram': {sym("wDeckToBuild"): b'\x00', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
        {'wram': {sym("wDeckToBuild"): b'\xff', sym("wBoosterTempEnergiesDrawn"): b'\x00'}},
    ],
})
MUTATIONS.update({
    'AppendCurrentCardToHL': {   'source_symbol': 'AppendCurrentCardToHL',
        'before': 'if (card == 0u)\n\t\t\tbreak;',
        'after': 'if (card != 0u)\n\t\t\tbreak;',
        'case_ids': [   'AppendCurrentCardToHL-0',
                        'AppendCurrentCardToHL-1',
                        'AppendCurrentCardToHL-2',
                        'AppendCurrentCardToHL-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterCardToTempCardCollection': {'source_symbol': 'AddBoosterCardToTempCardCollection', 'before': 'uint8_t value = (uint8_t)(old + 1u);', 'after': 'uint8_t value = (uint8_t)(old + 2u);', 'case_ids': ['AddBoosterCardToTempCardCollection-0', 'AddBoosterCardToTempCardCollection-1', 'AddBoosterCardToTempCardCollection-2', 'AddBoosterCardToTempCardCollection-3'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterEnergyToDrawnEnergies': {'source_symbol': 'AddBoosterEnergyToDrawnEnergies', 'before': 'card_id_write(&current, a);', 'after': 'card_id_write(&current, (CardId)(a + 1u));', 'case_ids': ['AddBoosterEnergyToDrawnEnergies-0', 'AddBoosterEnergyToDrawnEnergies-1', 'AddBoosterEnergyToDrawnEnergies-2', 'AddBoosterEnergyToDrawnEnergies-3'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateRandomEnergy': {'source_symbol': 'GenerateRandomEnergy', 'before': 'return AddBoosterEnergyToDrawnEnergies((CardId)(random + 1u));', 'after': 'return AddBoosterEnergyToDrawnEnergies((CardId)(random + 2u));', 'case_ids': ['GenerateRandomEnergy-0', 'GenerateRandomEnergy-1', 'GenerateRandomEnergy-2', 'GenerateRandomEnergy-3'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'PutEnergiesAndNonEnergiesTogether': {'source_symbol': 'PutEnergiesAndNonEnergiesTogether', 'before': 'if (card == 0u)', 'after': 'if (card != 0u)', 'case_ids': ['PutEnergiesAndNonEnergiesTogether-0', 'PutEnergiesAndNonEnergiesTogether-1', 'PutEnergiesAndNonEnergiesTogether-2', 'PutEnergiesAndNonEnergiesTogether-3'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateBoosterEnergies': {'source_symbol': 'GenerateBoosterEnergies', 'before': '\tuint8_t hi = gb_read8((uint16_t)(ptr_addr + 1u));', 'after': '\tuint8_t hi = gb_read8((uint16_t)(ptr_addr + 0x0u));', 'case_ids': ['GenerateBoosterEnergies-0'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'CheckCardAlreadyDrawn': {'source_symbol': 'CheckCardAlreadyDrawn', 'before': 'uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);', 'after': 'uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card + 1u);', 'case_ids': ['CheckCardAlreadyDrawn-1', 'CheckCardAlreadyDrawn-2'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'FindCardsInSetAndRarity': {'source_symbol': 'FindCardsInSetAndRarity', 'before': 'for (CardId card_id = 1u; card_id <= NUM_CARDS; card_id++) {', 'after': 'for (CardId card_id = 1u; card_id < NUM_CARDS; card_id++) {', 'case_ids': ['FindCardsInSetAndRarity-0', 'FindCardsInSetAndRarity-1'], 'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateFightingEnergy': {'source_symbol': 'GenerateFightingEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(FIGHTING_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(FIRE_ENERGY);',
        'case_ids': ['GenerateFightingEnergy-0', 'GenerateFightingEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateFireEnergy': {'source_symbol': 'GenerateFireEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(FIRE_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(GRASS_ENERGY);',
        'case_ids': ['GenerateFireEnergy-0', 'GenerateFireEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateGrassEnergy': {'source_symbol': 'GenerateGrassEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(GRASS_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(LIGHTNING_ENERGY);',
        'case_ids': ['GenerateGrassEnergy-0', 'GenerateGrassEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateLightningEnergy': {'source_symbol': 'GenerateLightningEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(LIGHTNING_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(PSYCHIC_ENERGY);',
        'case_ids': ['GenerateLightningEnergy-0', 'GenerateLightningEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GeneratePsychicEnergy': {'source_symbol': 'GeneratePsychicEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(PSYCHIC_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(WATER_ENERGY);',
        'case_ids': ['GeneratePsychicEnergy-0', 'GeneratePsychicEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateWaterEnergy': {'source_symbol': 'GenerateWaterEnergy',
        'before': '\treturn AddBoosterEnergyToDrawnEnergies(WATER_ENERGY);',
        'after': '\treturn AddBoosterEnergyToDrawnEnergies(FIGHTING_ENERGY);',
        'case_ids': ['GenerateWaterEnergy-0', 'GenerateWaterEnergy-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
MUTATIONS['AddBoosterCardToDrawnEnergies'] = {'source_symbol': 'AddBoosterCardToDrawnEnergies', 'before': '\treturn (AddBoosterCardToDrawnEnergiesResult){result.a, result.f};', 'after': '\treturn (AddBoosterCardToDrawnEnergiesResult){(uint8_t)((result.a) ^ 1u), result.f};', 'case_ids': ['AddBoosterCardToDrawnEnergies-0'], 'source': 'src/profiles/extended/home/booster_packs.c'}
MUTATIONS['CheckCardInSetAndRarity'] = {'source_symbol': 'CheckCardInSetAndRarity', 'before': '\t\treturn (CheckCardInSetAndRarityResult){\n\t\t\twBoosterCurrentRarity, 0x10u, b, c, d, e, hl};', 'after': '\t\treturn (CheckCardInSetAndRarityResult){(uint8_t)((wBoosterCurrentRarity) ^ 1u), 0x10u, b, c, d, e, hl};', 'case_ids': ['CheckCardInSetAndRarity-0'], 'source': 'src/profiles/extended/home/booster_packs.c'}
MUTATIONS['GenerateRandomEnergyBooster'] = {'source_symbol': 'GenerateRandomEnergyBooster', 'before': '\treturn (AddBoosterEnergyToDrawnEnergiesResult){0u, 0x80u, last.d, last.e};', 'after': '\treturn (AddBoosterEnergyToDrawnEnergiesResult){(uint8_t)((0u) ^ 1u), 0x80u, last.d, last.e};', 'case_ids': ['GenerateRandomEnergyBooster-0'], 'source': 'src/profiles/extended/home/booster_packs.c'}
