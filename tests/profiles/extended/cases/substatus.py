"""Extended oracle-diff cases for substatus, seeded from tests/cases/substatus.py."""

CONTRACT = {
    'CheckSandAttackOrSmokescreenSubstatus': {'compare': ('a', 'b', 'c', 'd', 'e', 'f', 'hl'), 'preserve': ('b', 'c')},
    'CountTurnDuelistPokemonWithActivePkmnPower': {'compare': ('a', 'b', 'c', 'd', 'e', 'f', 'hl'), 'preserve': ()},
    'CountPokemonWithActivePkmnPowerInBothPlayAreas': {'compare': ('a', 'b', 'c', 'd', 'e', 'f', 'hl'), 'preserve': ()},
    'CheckIsIncapableOfUsingPkmnPower': {'compare': ('a', 'f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ()},
    'CheckIsIncapableOfUsingPkmnPower_ArenaCard': {'compare': ('a', 'f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ()},
    'HandleDoubleDamageSubstatus': {'compare': ('b', 'c', 'd', 'e'), 'preserve': ('b', 'c')},
    'HandleDamageReductionExceptSubstatus2': {'compare': ('d', 'e'), 'preserve': ()},
    'HandleDamageReduction': {'compare': ('d', 'e'), 'preserve': ()},
    'HandleCantAttackSubstatus': {'compare': ('f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'HandleAmnesiaSubstatus': {'compare': ('f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'HandleNoDamageOrEffectSubstatus': {'compare': ('f', 'd', 'e', 'hl', 'b', 'c'), 'preserve': ()},
    'CheckNoDamageOrEffect': {'compare': ('f', 'hl', 'b', 'c'), 'preserve': ('b', 'c')},
    'IsClairvoyanceActive': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'GetLoadedCard1RetreatCost': {'compare': ('a',), 'preserve': ()},
    'CheckUnableToRetreatDueToEffect': {'compare': ('f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'CheckCantUseTrainerDueToEffect': {'compare': ('f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'IsPrehistoricPowerActive': {'compare': ('a', 'f', 'hl', 'b', 'c', 'd', 'e'), 'preserve': ()},
    'ClearDamageReductionSubstatus2': {'compare': (), 'preserve': ()},
    'UpdateSubstatusConditions_StartOfTurn': {'compare': (), 'preserve': ()},
    'UpdateSubstatusConditions_EndOfTurn': {'compare': (), 'preserve': ()},
    'IsRainDanceActive': {'compare': ('a', 'f', 'b', 'c', 'd', 'e'), 'preserve': ()},
    'ClearChangedTypesIfMuk': {'compare': (), 'preserve': ()},
    'CheckRainDanceScenario': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleStrikesBack_AgainstDamagingAttack': {'compare': ('a', 'b', 'c', 'd', 'e', 'f', 'hl'), 'preserve': ()},
    'ApplyStrikesBack_AgainstResidualAttack': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleStrikesBack_AgainstResidualAttack': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleDestinyBondSubstatus': {'compare': ('a', 'f', 'hl'), 'preserve': ()},
    'HandleNShieldAndTransparency': {'compare': ('d', 'e', 'f'), 'preserve': ('d', 'e')},
    'HandleTransparency': {'compare': ('a', 'f', 'hl'), 'preserve': ('hl',)},
    'HandleDamageReductionOrNoDamageFromPkmnPowerEffects': {'compare': ('f', 'd', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'HandleSandAttackOrSmokescreenSubstatus': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
}

CASES = {
    'CheckSandAttackOrSmokescreenSubstatus': [
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x02', 0xCBB4: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x02', 0xCBB4: b'\x01'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01', 0xCBB4: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01', 0xCBB4: b'\x01'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc3', 0xC3E8: b'\x00'}},
    ],
    'CountTurnDuelistPokemonWithActivePkmnPower': [
        {'d': 0x00, 'e': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x01', 0xC2BC: b'\xff'}},
        {   'd': 0x00,
            'e': 0x01,
            'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x01', 0xC2BC: b'\x00\x00\xff'},
            'read': {0xCE36: 0x01}},
        {   'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\x00',
                        0xC2F0: b'\x01',
                        0xC400: b'\x01',
                        0xC2BC: b'\xff'}},
        {   'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\x00',
                        0xC2F0: b'\x08',
                        0xC400: b'\x01',
                        0xC2BC: b'\xff'}},
        {'d': 0x00, 'e': 0x02, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x01', 0xC2BC: b'\xff'}},
    ],
    'CountPokemonWithActivePkmnPowerInBothPlayAreas': [
        {   'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\x00',
                        0xC400: b'\x01',
                        0xC2BC: b'\xff',
                        0xC478: b'\x01',
                        0xC3BC: b'\xff'}},
        {   'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\xff',
                        0xC400: b'\x01',
                        0xC2BC: b'\xff',
                        0xC478: b'\x01',
                        0xC3BC: b'\xff'},
            'read': {0xCE36: 0x01}},
        {   'd': 0x00,
            'e': 0x02,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\xff',
                        0xC3BB: b'\xff',
                        0xC400: b'\x01',
                        0xC2BC: b'\xff',
                        0xC478: b'\x01',
                        0xC3BC: b'\xff'},
            'read': {0xCE36: 0x01}},
    ],
    'CheckIsIncapableOfUsingPkmnPower': [
        {'a': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x01'}},
        {'a': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x00'}},
        {   'a': 0x00,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2BB: b'\x00', 0xC400: b"'"}},
        {'a': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x01'}},
        {   'a': 0x01,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3BB: b'\x00', 0xC478: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'CheckIsIncapableOfUsingPkmnPower_ArenaCard': [
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x08'}},
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'HandleDoubleDamageSubstatus': [
        {'d': 0x00, 'e': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x01'}},
        {'d': 0x12, 'e': 0x34, 'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x01'}},
        {'d': 0x12, 'e': 0x34, 'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x00'}},
        {'d': 0x80, 'e': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x01'}},
    ],
    'HandleDamageReductionExceptSubstatus2': [
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC75: b'\x01'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x0f'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x1e'}},
        {   'd': 0x00,
            'e': 0x05,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x1e'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x13'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x0e'}},
        {   'd': 0x00,
            'e': 0x27,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x0e'}},
        {   'd': 0x00,
            'e': 0x28,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x0e'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x15'}},
        {   'd': 0x00,
            'e': 0x02,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x15'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x01'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC5C: b'\x04'}},
        {   'd': 0x00,
            'e': 0x0A,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x9b'}},
        {   'd': 0x00,
            'e': 0x1E,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x9b'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x8b'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'HandleDamageReduction': [
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3E8: b'\x00'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3E8: b'\x03'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3E8: b'\x07'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3E8: b'\x12'}},
        {   'd': 0x00,
            'e': 0x64,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3E8: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'HandleCantAttackSubstatus': [
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x05'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x06'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x0b'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2'}},
    ],
    'HandleAmnesiaSubstatus': [
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x04', 0xC2F2: b'\x02', 0xCC74: b'\x02'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x04', 0xC2F2: b'\x02', 0xCC74: b'\x00'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x04', 0xC2F2: b'\x02', 0xCC74: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2'}},
    ],
    'HandleNoDamageOrEffectSubstatus': [
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xCC5C: b'\x04',
                        0xCC75: b'\x03'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\r'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x14'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2E7: b'\x0c'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2F0: b'\x01'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x00'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x01'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xCC71: b'\xa0',
                        0xCC94: b'\x01'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\xa0', 0xCC6F: b'&'}},
        {   'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\xa0', 0xCC6F: b"'"}},
        {   'd': 0x5A,
            'e': 0x99,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\xa0', 0xCC6F: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'CheckNoDamageOrEffect': [
        {'hl': 0x1234, 'wram': {0xCC75: b'\x00'}},
        {'hl': 0x1234, 'wram': {0xCC75: b'\x81'}},
        {'hl': 0x1234, 'wram': {0xCC75: b'\x01'}},
        {'hl': 0x1234, 'wram': {0xCC75: b'\x05'}},
        {'hl': 0x1234, 'wram': {0xCC75: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCC75: b'\x02'}},
    ],
    'IsClairvoyanceActive': [
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2BB: b'\x00', 0xC400: b'\\'}},
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC3BB: b'\x00', 0xC478: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'GetLoadedCard1RetreatCost': [
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC02: b'\x03'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\x00\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb6',
                        0xCC02: b'\x03'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\x00\x00\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb6',
                        0xCC02: b'\x03'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\x00\x00\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb6',
                        0xCC02: b'\x01'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\x00\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb6',
                        0xCC02: b'\x03',
                        0xC3BB: b'\x00',
                        0xC478: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC02: b'\x05'}},
    ],
    'CheckUnableToRetreatDueToEffect': [
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\t'}},
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2'}},
    ],
    'CheckCantUseTrainerDueToEffect': [
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x02'}},
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2'}},
    ],
    'IsPrehistoricPowerActive': [
        {'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
        {   'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC2BB: b'\x00',
                        0xC400: b'\x8d'}},
        {   'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC2BB: b'\x00',
                        0xC400: b'\x8d',
                        0xC3BB: b'\x00',
                        0xC478: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'ClearDamageReductionSubstatus2': [
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x03'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x05'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x06'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x07'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x12'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x01'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x05'}},
    ],
    'UpdateSubstatusConditions_StartOfTurn': [
        {'wram': {0xFF97: b'\xc2', 0xC2E7: b'\x19', 0xC2EB: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E7: b'\x0c', 0xC2EB: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E7: b'\x00', 0xC2EB: b'\x02'}},
        {'wram': {0xFF97: b'\xc2', 0xC2E7: b'\x19', 0xC2EB: b'\x02'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2E7: b'\x19', 0xC2EB: b'\x00'}},
    ],
    'UpdateSubstatusConditions_EndOfTurn': [
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x03', 0xC2E8: b'\x05', 0xC2E7: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x03', 0xC2E8: b'\x05', 0xC2E7: b'\x19'}},
        {'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x00', 0xC2E8: b'\x00', 0xC2E7: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2EB: b'\x03', 0xC2E8: b'\x05', 0xC2E7: b'\x00'}},
    ],
    'IsRainDanceActive': [
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
        {'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xC2BB: b'\x00', 0xC400: b'C'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC2BB: b'\x00',
                        0xC400: b'C',
                        0xC3BB: b'\x00',
                        0xC478: b"'"}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff'}},
    ],
    'ClearChangedTypesIfMuk': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC400: b"'",
                        0xC2D4: b'\x01\x02\x03\x04\x05\x06',
                        0xC3D4: b'\x07\x08\t\n\x0b\x0c'}},
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC400: b'\x01',
                        0xC2D4: b'\x01\x02\x03\x04\x05\x06',
                        0xC3D4: b'\x07\x08\t\n\x0b\x0c'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC400: b"'",
                        0xC2D4: b'\x01\x02\x03\x04\x05\x06',
                        0xC3D4: b'\x07\x08\t\n\x0b\x0c'}},
    ],
    'CheckRainDanceScenario': [
        {   'wram': {   0xFF97: b'\xc2',
                        0xFF98: b'\x00',
                        0xC400: b'\x08',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x00',
                        0xC2D4: b'\x00'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xFF98: b'\x00',
                        0xC400: b'\x03',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x01',
                        0xC401: b'\x08',
                        0xC2D4: b'\x00'}},
        {   'wram': {   0xFF97: b'\xc2',
                        0xFF98: b'\x00',
                        0xC400: b'\x03',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x01',
                        0xC401: b'C',
                        0xC2D4: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xFF98: b'\x00',
                        0xC400: b'\x03',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x01',
                        0xC401: b'C',
                        0xC2D4: b'\x00'}},
    ],
    'HandleStrikesBack_AgainstDamagingAttack': [
        {   'd': 0x00,
            'e': 0x00,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x7f'}},
        {   'd': 0x00,
            'e': 0x0A,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xCC71: b'\x7f',
                        0xCC94: b'\x01'}},
        {'d': 0x00, 'e': 0x0A, 'wram': {0xFF97: b'\xc2', 0xCC71: b'\x01'}},
        {   'd': 0x00,
            'e': 0x0A,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xCC71: b'\x7f',
                        0xCC5C: b'\x04'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BC: b'\xff', 0xC3BC: b'\xff', 0xCC71: b'\x7f'}},
    ],
    'ApplyStrikesBack_AgainstResidualAttack': [
        {   'hl': 0x00,
            'wram': {0xFF97: b'\xc2', 0xCC6F: b'\x01'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {0xCC13: 0x02}},
        {   'hl': 0x00,
            'wram': {0xFF97: b'\xc2', 0xCC6F: b'\xe4'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {0xCC13: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x00,
            'wram': {0xFF97: b'\xc2', 0xCC6F: b'\x01'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {0xCC13: 0x02}},
    ],
    'HandleStrikesBack_AgainstResidualAttack': [
        {   'wram': {   0xC000: b'\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0'
                                b'\xc1\xc2\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0'
                                b'\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x08\x00\x00\x00\x00\x00'
                                b'\x01\x00\x00\x00\x08\x00\x00\x00\x00\x08\x01\x00\x08\x00\x01\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
                                b'\x00\x00\x00\x00\x00\x00\x00\x08\x01\x01\x08\x00:\x19\x1c\x14'
                                b'\n7\x1e\x109\x1a\x078/\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x109\x1a\x078/:\x19\x1c'
                                b'\x14\n7.\x00,\x03%\x13\x1f&#\x01\x08+\x1d\x042-!\x0b\x16"1\x0f*)0'
                                b"\x17$\x18 3\x06\x1b4(\x15\x12;\t\x026\x05'5\x0e\x11\r\x0c\r/"
                                b'\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'?\x00\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00'
                                b'\x00\x00\x00\x00\x00\x08\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00'
                                b'\x00\x00\x12\x00\x08\x08\x00\x00\x11\x00\x00\x10\x08\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x08'
                                b' (;\x11!\x006\x07\t\x17\x17\x17\t\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x146'
                                b'\x07\x1e$\'\t (;\x11!\x00\x17\x02\x03\x13\x1f\x1b09,%#.\n8*\x18"'
                                b'&)\r\x064\x152\x16\x0c\x19/1\x1d\x0b\x1a\x1c\x0f\x0e\x10:+3\x08\x05'
                                b"\x01\x04\x125-7\x0e'$\x1e\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00"
                                b'\n2d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00?\x00\x04\x03\x00\x9b\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x04\x04\x04\x04\x04\x04\x04\x04\x05\x05\x05\x05\x05\x050012'
                                b'66899;``giikuyyz}~\xa7\xa7\xa8\xb1\xc3\xc5\xc5\xd2\xd6\xd8'
                                b'\xdd\xdd\xdf\xdf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x07\x07\x07\x07=@@Z'
                                b'_rv\xb9\xb9\xbc\xbc\xbc\xbc\xbf\xbf\xbf\xbf\xc0\xc0\xc0'
                                b'\xc1\xc1\xc3\xc5\xc5\xc5\xc9\xca\xca\xd0\xd0\xd0\xd5\xd5\xd5\xe3'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00'
                                b'\x17\t\x076\xff\xff\xff\xff\xff\xff/\x1e8\xff;$\xff\x18\xff\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x17\x17\x16'
                                b'\x00\x00\x00\x00\x00\x00\x00\x000\x00                              '
                                b'                     \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00O,0MEHPATAOO PG HA D'
                                b"KHD.MS N.(' EKSESATNO-RV.O@LESSOOL   AC  OALRIIADELO NADD R SOCWLTRG"
                                b' 0R YPVUN NTII !\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00 RNLLGNAP)3AWC L EHCGUAET REO  E@EOAM NISAUD'RTOTTDL"
                                b'RLKPNSODORL.THN)ARNB  KZPPA FUTNLSUDIM  IAEN91AKGAAOEYIOTNND'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x008120456\\E\x93N\x9e\x82d>\x83\x92\x8aG\x86a;w\x85i<=`sLFRm9X'
                                b'STk\x9aBgn\x80\x87O]P\x9fD\x90W[CZ\x95Yh|U@e\x8c\x8fVA\x88r^\x9du\x97'
                                b'I\x84H\x96{J}~\x7f8:qvy\x9boxf_j\x8bb\x98ztc\x99l\x8epMKQ?\x8d\x00'
                                b'\x94\x9c\x89\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x0042395678\x81R\x82FJK?\x99lqXea9OCzx}\x97N\x96;]'
                                b'_\x98PTUkpcShfd8^t\x8aLE\x8d\x91>m\x89YiI\x8bV\x93QZ\x87\x95\x83sM'
                                b'\x90v\x84G\x88\x85\x8f|j~\x7f\x80[\x9f=@yHD\\r\x9eB\x8cn\x9a\x94o'
                                b'b\x00A:\x9cg{w\x8e\x92W\x86\x9du<`\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00\x14\x00'
                                b'\x00\x00\x11\x00\x00\x00\x12\x00\x00\x00\x0f \x00\x00\x11 '
                                b'\x00\x00\x0f@\x00\x00\x10@\x00\x00\x0f`\x00\x00\x11 \x00\x00\x0f@'
                                b'\x00\x00\x10@\x00\x00\x0f`\x00\x00\x01@\x00\x00\x02@\x00\x00\x03@'
                                b'\x00\x00f\x00\x00\x00g\x00\x00\x00h\x00\x00\x00i\x00\x00\x00\t\x00'
                                b'\x00\x00\x08\x00\x00\x00\x18\x00\x00\x00\x19\x00\x00\x00\x04\x00'
                                b'\x00\x00\x14\x00\x00\x00$\x00\x00\x00\x05\x00\x00\x00\x15\x00'
                                b'\x00\x00%\x00\x00\x005\x00\x00\x004\x00\x00\x00(\x00\x00\x00&\x00'
                                b'\x00\x00\x16\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x17\x00'
                                b"\x00\x00'\x00\x00\x00)\x0000010\x00d\x00\x030\x030\x00\x00\x00\x00"
                                b'\x00\x00\x00\x11\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xd2\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x00\x01&\x01\t\x05;\x03\x00/<\r\xc3\xa6>\xc3H\x03\xa2;\x00\x13t\x05'
                                b'\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9cc\xbe\x03~'
                                b'\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb\x0c\x00\x00\x9c'
                                b'cZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xffk\xac~\x08'
                                b'A\x00\x10\xffk\x08\x02\x95@\x00\x10\x00\x00\xff\x7f\xef=\x00\x00\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\x00\x00\x11\xc5\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01'
                                b'\x03\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x08\x02\x00'
                                b'\x00o\x00\xa7\x00\x01\x00\x00\x00\x00\x00\x00\xe8\xdf\x00\x01'
                                b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x04\x01\x04\x00\x0e;S\x00\x00\xc3\x00\x00\x06'
                                b'\x9b\x00\x01\x00\x9b\x1b\xff\xff\xff`\x00\x02\x02\xad\x03\x06'
                                b'\x1b\x04\x00\x00\x00\x00\x00\x00\x02\x00\x02\x06aH[\x0b\x01 \xbf('
                                b'\x00\x00\x00\x00\x00\x00\x10\xad\n\x00\x00\x00\x00\n\x00\x00'
                                b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x04t\t\x93\x00'
                                b'\n\x05\x0bF\x00\\\x0b\x12\x06aH[\x0b\x01 \xbf(\x00\x00\x00'
                                b'\x00\x00\x00\x10\xad\n\x00\x00\x00\x00\n\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x01\x00\x04t\t\x93\x00\n\x05\x0bF\x00\\\x0b'
                                b'\x12\x00\x00\x00\x10\xad\n\x00\x00\x00\x00\n\x00\x00\x00\x00'
                                b'\x00\x00\x00\x01\n\x00\n\n\x00\x00\n\x00\x00\xbf\xbf\xa7'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3\xf0\x03\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\xf5\x01\x00\x00\x002\x00\x00\x00\x00\x04\x00'
                                b'\x00\xc4\xc4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa0\xa0\xc4\xc4\x9f'
                                b'\x91\x88\x80\x00\x00\x01\x00\n\x01\x00',
                        0xCCBE: b'\x00\x12\x11\x01\x01/\x1d\x00\x00\x00\x04\x06\x0e\x19W\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00 \x01\x00\x00\x01'
                                b'\x00\x00\x00\x00\x00\xff\x06\x00\xd3T\x9cT\xa3T\xa7T\x00\x00\xb1T'
                                b'\x00\x00\x00\x00\x03Y\x0b\x00\x00\x00\x00Q\x8a\x80\x95\x88'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x08\x04\x06\x06'
                                b'@\x01\x01\x00\x00\x00\x81\x01\x00Q\x8a\x84\x8b\x82\x00}'
                                b'\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x1e6'
                                b'\x01\x00\x00\x00\x00v\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x04\x00\x07\x00\x00\x00\x00\x00\x00\x1e\xff\x00\x00\x00'
                                b'\x00\x00\xff\xd8\x0e\x1e\x01\x05\xff\x00\x00\x00\x00\x00\x0b\xff'
                                b'k\xac~\x08A\x00\x10\x0f\x01\r\x93f\x0f\x01\r\xa5\xca\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xad\n\n\x00\x06\x00\x02'
                                b'\x00\x01\x01\x00\xd7\x03\x00\x00\xc3\xc2\x03[K\xff\x01\x00'
                                b'\x00\x00\xa2\xff\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00'\x00\x01\n\x00\x00\x80\xc3\xa7\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x17\t\x076\xff\xff\xff0\xff\xff-69\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x17\t\x076\xff\xff\xff0\xff\xff-69\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x00\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b"\x00\x00\x00\x00\n\xc3\xff\x18\xc5\xcd\x00\x00\n'\x00\x00"
                                b'\x05\xff\x00\x00\x00\x00\x9f\x91\x14\x98\x06\x0e\x00\x0f\x00\x00'
                                b'\x01\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFCE,
            'rom_bank': 0x00,
            'read': {0xCC71: 0x01},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0xA7,
            'b': 0x0B,
            'c': 0x04,
            'd': 0x98,
            'e': 0x69,
            'f': 0x00,
            'hl': 0x00},
        {'wram': {0xCC71: b'\x01'}},
        {'wram': {0xCC71: b'\x7f', 0xCC5C: b'\x80'}},
        {'wram': {0xCC71: b'\x7f', 0xCC5C: b'\x00', 0xCC6A: b'\x00'}},
        {'wram': {0xCC71: b'\x01', 0xCC5C: b'\x80', 0xCC6A: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCC71: b'\x01'}},
    ],
    'HandleDestinyBondSubstatus': [
        {'wram': {0xFF97: b'\xc2', 0xC3E7: b'\x00', 0xC3C8: b'\x00'}},
        {'wram': {0xFF97: b'\xc2', 0xC3E7: b'\x16', 0xC3BB: b'\xff'}},
        {'wram': {0xFF97: b'\xc2', 0xC3E7: b'\x16', 0xC3BB: b'\x00', 0xC3C8: b'\n'}},
        {'wram': {0xFF97: b'\xc2', 0xC3E7: b'\x16', 0xC3BB: b'\x00', 0xC3C8: b'\x00', 0xC2C8: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc3', 0xC2E7: b' ', 0xC2C8: b'\x00'}},
    ],
    'HandleNShieldAndTransparency': [
        {   'e': 0x00,
            'd': 0x12,
            'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x01', 0xC401: b'\x01', 0xCC75: b'\x00'},
            'read': {0xCC75: 0x01}},
        {   'e': 0x00,
            'd': 0x12,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BB: b'\x01',
                        0xC401: b'\xa0',
                        0xC3CE: b'\x01',
                        0xCC75: b'\x00',
                        0xCABB: b'\x00',
                        0xC500: b'\xff'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400,
            'read': {0xCC75: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x01', 0xC401: b'\x01', 0xCC75: b'\x00'},
            'read': {0xCC75: 0x01}},
    ],
    'HandleTransparency': [
        {'wram': {0xCC71: b'\x00'}, 'hl': 0x4567},
        {'wram': {0xCC71: b'\x96', 0xCC5C: b'\x04'}, 'hl': 0xC100},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC200,
            'wram': {0xCC71: b'\x96', 0xCC5C: b'\x04'}},
    ],
    'HandleDamageReductionOrNoDamageFromPkmnPowerEffects': [
        {'d': 0x12, 'e': 0x34, 'hl': 0x4567, 'wram': {0xCC5C: b'\x04'}},
        {'d': 0x80, 'e': 0x00, 'hl': 0x00, 'wram': {0xCC5C: b'\x04'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCC5C: b'\x04'}},
        {   'wram': {   0xC000: b'\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0'
                                b'\xc1\xc2\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0'
                                b'\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x10\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00\x00\x00\x00'
                                b'\x02\x00\x01\x00\x00\x01\x00\x00\x00\x11\x01\x00\x00\x00\x01\x08'
                                b'\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00\x00\x08\x00\x00\x00\x00'
                                b'\x00\x10\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f+(\x0b'
                                b'\x00\x00\x1a8\x12\x15\t\x1e\x1e\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10&'
                                b'\x1a\x00\x10\x01&\x1f+(\x0b8\x12\x15\t\x1e\x1d,\x0f\x1c\x0e7'
                                b'/\x11\x08\x05\x17\x13\x04\n.\x1b9\x185\r!6\x062\'0\x07#4"\x16;\x03)'
                                b':\x02-3%*\x0c$ \x14\x101\x19\xff\xff\xff\xff\xff\x80\x80'
                                b'\x80\x00\x00\x00(2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x02\x06\x02\x00\x00\x00\n'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x13'
                                b'\x01\x11\x13\x00\x00\x00\x11\x00\x00\x00\x00\x00\x01\x00\x00\x10'
                                b'\x00\x00\x11\x00\x00\x13\x00\x00\x00\x10\x00\x00\x12\x00\x00\x00'
                                b'\x01\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x08\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x002\x10\x02'\x00\x00$\x04\x10\x101 "
                                b'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x001$\x04\x16\x05\x1d\n2\x10\x02'\x03 \x19"
                                b'\x061/:!\x1f(&"\x070%),\x0f.\x12\t\x18#9+7\x01\x00\x1a\x1c\x15'
                                b'-4\x0b\x1e35\x1b;8\x17\r\x116\x0e\x0c\x08\x14*\x10\x1d\x16 \x19\xff'
                                b'\xff\xff\x80\x80\x80\x80\x00\x00\x1e(2<\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x01\x03\x04'
                                b'\x00\xa5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x04\x04\x04\x04\x04\x04'
                                b'\x04\x04\x05\x05\x05\x05\x05\x05001266899;``giikuyyz}~\xa7\xa7'
                                b'\xa8\xb1\xc3\xc5\xc5\xd2\xd6\xd8\xdd\xdd\xdf\xdf\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x03\x03\x03\x03\x03\x03\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
                                b'\x04\x04\x04\x04\x04\x04`abcddddeeffgghh\xc5\xc5\xc5\xc5\xd2\xd2'
                                b'\xd2\xd2\xd4\xd4\xd4\xd4\xdd\xdd\xdd\xdd\xde\xde\xdf\xdf\xdf\xdf'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00'
                                b'1\x00\x15\x128\x01\x1a\xff\xff\xff+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x16\x16\x16'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00chu Lv12\x00                       '
                                b'                     \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00G N1ROHPRWOKCSET!H1D'
                                b" 0IN.EAIA OALG  )TEUDYNN R.G EKM VNO Y.R O CIAWKRKOLLU4H'0AETL CC(FS"
                                b'CMNDEA5E IW.FRH \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00LGTIGCU NTI ERC UAYIN N HTVEM1NOEJMTHUT FAH4SW HNAAM'
                                b"2ADR5RCA LEP.GNDSEKAFCEOIPDPEPVG4\x03EMA Y RD 'E N DT4SEYOHIT D"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x000123456\x99y\x8cAc\\`8G\x9c\x94?\x81\x97~PD\x9a\x89l={\x96SYreo'
                                b'\x9bBqz[kFI\x8duxwT\x7f\x9e}Ja\x00^\x82v\x95\x93R:\x98\x83\x80n@U'
                                b'\x84\x91\x90COtsf\x8ej<\x8aE9N\x9fZp\x9dH\x86_g;W\x8bK\x85>VQML\x88mh'
                                b'|X\x87]\x92i\x8fb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x0012345678?\x81m\x8b~L\x90Cr;UwH\x80Z@\x87[d\x8e'
                                b'\x94\x93\x82xG\x92lO`s\x91\x8c\x99P\x84X=\x9bg\x89>e\x9f<\x00R{\x8a'
                                b'\x97\x9d}YK\x96qS\x85VQzy]i_^9WM\x98cFapDhot\x8f\x88\x9a\x95J\x7f\x8d'
                                b':\\|\x9evu\x9ckBjNEn8ITA\x86b\x83\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00'
                                b'\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x00 \x00\x00\x01 '
                                b'\x00\x00\x02 \x00\x00\x03 \x00\x00\x00`\x00\x00\x01`\x00\x00\x02`'
                                b'\x00\x00\x03`\x00\x00\x00@\x00\x00\x01@\x00\x00\x02@\x00\x00\x03@'
                                b'\x00\x000@\x00\x001@\x00\x000@\x00\x001@\x00\x003@\x00\x004@'
                                b'\x00\x003@\x00\x004@\x00\x00\x04\x00\x00\x00\x14\x00\x00\x00$\x00'
                                b'\x00\x00\x05\x00\x00\x00\x15\x00\x00\x00%\x00\x00\x005\x00'
                                b'\x00\x004\x00\x00\x00(\x00\x00\x00&\x00\x00\x00\x16\x00'
                                b"\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x17\x00\x00\x00'\x00"
                                b'\x00\x00)\x00\x00\x00\x00! \x00\x030\x030\x030\x00\x00\x00\x00'
                                b'\x00\x00\x00\x11\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xd2\xe4',
                        0xCAC0: b'',
                        0xCAC1: b"\x00\x01\x10\x01'6\x11\x01\x00\x9d\n\xde\xc3\x00\x00\xc3H\x03\xa2;"
                                b'\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9c'
                                b'c\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb'
                                b'\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xbf\x02\x002\x9a\x00\x00\x00\xffk\xbf\x02\x15'
                                b'\x11\x00\x00\x00\x00\xff\x1f\x1f\x1bk\x00\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\x00\x00\x12\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02\x03\x01\x00\x00'
                                b'\x00\x00\x00\x01\x00\x00\x01\x00\x00\x08\x02\x00\x00\xaa\x00\xa7'
                                b'\x00\x01\x00\x00\x01\x00\x00\x00\xe8\xdf\x00\x01\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04'
                                b'\x01\x07\x00\x0e;S\x00\x00\xc2\t\x00\x04\xa5\x00\x01\x00\x00%\xff\x00'
                                b'1\xb1\x00#&\xc0\x03\x04%\x02\x00\x00\x01\x00\x00\x00\x00\x00\x01\x02'
                                b'\xaf%\xc2\t\xffHd(\x00\x00\x00\x00\x10\x00\x00\xc0\t"\x08\x00'
                                b'\x00\n\x00\x88L\x04\x00\x00\x00\x06\x00\x00\x000\xc3\t\xc4\t\x00\x00'
                                b'\x1e\x00\x8cL\x00\x04\x00\x00Q\x01\x00\x08\xb9\t\x19\x00'
                                b'\x0c\x01\x04\x82\x00\xc5\t\x03\x02\xaf%\xc2\t\xffHd(\x00\x00\x00'
                                b'\x00\x10\x00\x00\xc0\t"\x08\x00\x00\n\x00\x88L\x04\x00'
                                b'\x00\x00\x06\x00\x00\x000\xc3\t\xc4\t\x00\x00\x1e\x00\x8c'
                                b'L\x00\x04\x00\x00Q\x01\x00\x08\xb9\t\x19\x00\x0c\x01\x04'
                                b'\x82\x00\xc5\t\x03\x00\x00\x00 \x14\x0b\x15\x0b\x00\x00\x00\x80MN '
                                b'@\x00\x02\x83\x00\x00\n\n\x00\x00\x00\x00\x00\xb1\xb1f'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc2\xf0\x03\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x05\x02\x02\x01\x00!\x00\x00\x00\x00\x04\x00'
                                b'\x00\xa4\xa4\xa4\xa4\xa4\xa4\xe4\xe4\xa4\xa4\xa0\xa0\xa4\xa4\x9f'
                                b'd\x88\x80\x00\x00\x01\x00\n\x01\x00',
                        0xCCBE: b'\x00\x12\x11\x01\x01/\x1d\x00\x00\x01\x04\x07\x0e\x19W\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00 \x01\x00\xa5\x01'
                                b'\x00\x00\x00\x00\x00\xff\n\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x016\x08\x00\x00\x00\x00R'
                                b'\x85\x85\x89\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
                                b'\x08\x04\x04\x03\x04\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01$\x01\x00\x00\x00\x00y\x00\x01\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x0e\x00\x19\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\xff\xd8\x0e\x17\t\x00\x00\x00\x00\x00'
                                b'\x00\x00\x0b\xbf\x02\x002\x9a\x00\x00\x00\x0f\x01\r\xe0e'
                                b'\x0f\x01\x18\x86b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x14\x0b\x01\x00\x00\x00\x02\x00\x02\x00\x00\xc0\x03\x00\x00'
                                b'\xc3\xc2\x00[K\xcf\x01\x00\x00\x00\xa2\xff\x00\x00\x00\x00'
                                b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x01\x00"
                                b'\x00\x00\x80\xc2d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x10\x04$\xff\xff\xff\xff&\xff\xff+$5\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x10\x04$\xff\xff\xff\xff&\xff\xff+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x0b\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x00\x00\x00\x00\n\xc31\x14\xc5\xc3\x00\x00\n1\x01\x00'
                                b'\xff\xff\x00\x00\x00\x00\x9fd\x14\x98\n\n\x00\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFD2,
            'rom_bank': 0x0B,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x02,
            'b': 0x12,
            'c': 0x04,
            'd': 0x00,
            'e': 0x14,
            'f': 0xA0,
            'hl': 0x00},
    ],
    'HandleSandAttackOrSmokescreenSubstatus': [
        {'d': 0x12, 'e': 0x34, 'hl': 0x4567, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {'d': 0xAD, 'e': 0xB5, 'hl': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {   'a': 0x01,
            'f': 0x10,
            'b': 0x22,
            'c': 0x33,
            'd': 0x80,
            'e': 0x01,
            'hl': 0xC000,
            'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2E8: b'\x00'}},
        {   'wram': {   0xC000: b'\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0'
                                b'\xc1\xc2\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0'
                                b'\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
                                b'\x00\x00\x00\x00\x01\x00\x00\x10\x00\x00\x08\x01\x11\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x08\x00\x00\x00\x00'
                                b'\x00\x00\x00\x08\x00\x00\x01\x00\x00\x00\x00\x013+\x1a\x00'
                                b'\x00\x00\r\x1b;6\x14\x146\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x1c)\x1b\x17;63+\x1a'
                                b'\x14\x075\x05\x194\x08\x0c(\t/-\x02\x12!,&\x04\x06#\x15\x1d:\x00'
                                b'21\x1e\x03\x10\n9\'\x16\x0e\x18\x11%\x0f$0\x0b\x13\x1f78. "\x01*\x0b)'
                                b'\x1c\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x14<\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00'
                                b'\x07\x00\x05\x02\x00\x00\x00\n\x00\x00\x02\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x08\x00\x00\x00\x01'
                                b'\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x08\x02\x00'
                                b'\x02\x00\x00\x08\x00\x10\x00\x00\x00\x00\x01\x13\x11\x00\x00\x00'
                                b'\x00\x00\x00\x01\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x19\x1f\x07\x00\x00\x00\x06\x12\x0b&/\x04'\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x1a\x1c13(\x1a!\x19\x1f\x07\x0e\x06\x12\x0b&/\x04';5\x16\x15"
                                b'\x1b%6.\x18\x012\x02\x1e+\x149\r\x03\x13\x0c#\x00,$)\x100-\t4:\x0f'
                                b'\n\x11"\x088\x05*7\x1d \x12!(\x17\'\xff\xff\xff\x00\x00'
                                b'\x00\x00\x00\x00((\x1e(\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x04\x06\x04\x00\x9f\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x02\x02'
                                b'\x02\x02\x02\x02\x02\x02\x04\x04\x04\x04\x04\x04\x04\x04\x05\x05'
                                b'\x05\x05\x05\x05001266899;``giikuyyz}~\xa7\xa7\xa8\xb1\xc3\xc5'
                                b'\xc5\xd2\xd6\xd8\xdd\xdd\xdf\xdf\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x05\x05\x05'
                                b'\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x03\x03\x03\x03\x03'
                                b'\x03\x03\x03MMMN\\\\\\]]wwwwxx\x84\x84\x84\x86\x88\x88'
                                b'\x88\x8b\x8b\x8c\x8d\x8d\xc3\xc3\xc5\xc5\xca\xca\xcc\xcc\xcc\xcc'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00'
                                b')\x00)\x01\x1b\r\xff\xff\x11#+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x16\x16\x16'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00v12\x00                            '
                                b'                     \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000)NLHPETE.OO E HT2AK'
                                b'ON6I T1DMP    C OU ITGYRN LIEA 0C GWYTANSSL.OCKGGRKNRVUHATDLZCEY( I!'
                                b'PTFRL RAHIHDRWWE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00RC LBMME\x03SALC N RETRMDETE1ECCI7DGO NAA8DUTRHYMLH'
                                b"HRRAEYPTSHK1E.IEGAT ' SNDAOANTPMELF -T GI  AD LKMU GEWUSSFGEDAOL"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x000123456\x94\x8c\x83\x82S\x7fxAj{p9CDG\x8e\x87\x81}ro`c>Os\x9di'
                                b'kvH]\\J\x91ZEP;Q\x92\x8aw\x88Ma:\x9aNIlz<\x85\x86\x9cdYq\x008hW\x96'
                                b'\x80\x84\x8fTg@K~\x9e\x95[t_\x9fBmeR|f\x89F\x93yL\x90\x9b\x8bu\x98?V'
                                b'\x97^\x99\x8dXb=n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x0012345678tCf^l\x9eO\x96}?\x86DE\\\x8dFViY~\x90dhP'
                                b']_\x89<{s\x97v\x9cq[\x82XW\x99\x84Me\x9dNp\x88\x8b|uS@Tj\x87\x9fLBrKQ'
                                b'\x83\x94Ub>\x8fkA\x8aJ\x7f=xI;:ymnHc\x8ca\x939\x9bGz\x91Z`\x8e'
                                b'8\x81w\x98\x95\x9ag\x92oR\x80\x85\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00'
                                b'\x00\x00\x03\x00\x00\x00\x03 \x00\x00/\x00\x00\x000\x00\x00\x000 '
                                b'\x00\x00/ \x00\x000`\x00\x00/`\x00\x00-`\x00\x002\x00\x00\x003\x00'
                                b'\x00\x005\x00\x00\x006\x00\x00\x002\x00\x00\x00\x0b\x00'
                                b'\x00\x00\x0c\x00\x00\x00\x10 \x00\x00\x11 \x00\x00\x0b\x00'
                                b'\x00\x00\x0c\x00\x00\x00\x10 \x00\x00\x11 \x00\x00\x0b \x00\x00\x0c '
                                b'\x00\x00\x10\x00\x00\x00\x11\x00\x00\x00\x0b \x00\x00\x0c '
                                b'\x00\x00\x10\x00\x00\x00\x11\x00\x00\x00\x0e\x00\x00\x00\x10\x00'
                                b'\x00\x00\x11\x00\x00\x00\x0b \x00\x00\x0c \x00\x00\x0e\x00'
                                b'\x00\x00\x10 \x00\x00\x11 \x00\x00\x00# \x00\x030\x030\x030'
                                b'\x00\x00\x00\x00\x00\x00\x00\x11\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xe6\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x0f\x01\xef\x01/*5\x00\x00\xb7Cy\xc3\x00\x00\xc3H\x03\x00\x00'
                                b'\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9c'
                                b'c\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb'
                                b'\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xffC\xff\x13\x90\x01\x04\x00\xffC\xbf\x12\x9a'
                                b'\x11\x04\x00\x9cc\xb5BJ!\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00'
                                b'\x00\x12\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x01\x00\x02\x03\x01\x00\x00\x00\x01\x00\x00'
                                b'\x00\x00\x01\x00\x00\x08\x02\x00\x00\xaa\x00\xa7\x00\x01\x00\x00'
                                b'\x01\x00\x00\x00\xe8\xdf\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x07\x00\x0e'
                                b';S\x00\x00\xc2\x01\x00\x03\x9f\x00\x01\x00\x00\x1f\xff\x00)y\x00\x1c'
                                b'\x1b\xb9\x03\x03\x1f\x02\x00\x00\x00\x00\x01\x00\x00\x00\x01\x04'
                                b'\xaf-\x0f\n\x00\x00y\x1e\x00\x00\x00\x00\x00\x10\x00\x10'
                                b'\n\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
                                b' \x00\x11\n\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x01\x00@ '
                                b'\x12\n2\x00\x08\x00\x08\x14\x00\x13\n\x13\x04\xaf-\x0f\n\x00\x00y'
                                b'\x1e\x00\x00\x00\x00\x00\x10\x00\x10\n\x00\x00\x00\x00\n\x00'
                                b'\x00\x00\x00\x00\x00\x00\x01\x00\x00 \x00\x11\n\x00\x00\x00'
                                b'\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x01\x00@ \x12\n2\x00\x08\x00\x08'
                                b'\x14\x00\x13\n\x13\x00\x00\x10\x00\x10\n\x00\x00\x00\x00\n'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\n\x00\n\n\x00\x00\x00\x00\x00yyw'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3\xf0\x03\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\xfc\x01\x00\x01\x00\x14\x00\x00\x00\x00\x04\x00'
                                b'\x00NN\xaa\xaa\xaa\xaa\xea\xea\xae\xae\xa8\xa8\xa8\xa8\x9f'
                                b'U\x88\x80\x00\x00\x01\x00\n\x01\x00',
                        0xCCBE: b'\x00\x01\r\x02\x02\x0f\x00\x00\x00\x00\x04\x06\x0e\x19W\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00 \x01\x00\x00\x01'
                                b'\x00\x00\x00\x00\x00\xff\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x02\x04\x02\x01\xa8\x0e\x00\x00\x00\x00R'
                                b'\x8b\x80\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08'
                                b'@ \x03\x03\xcc\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x17\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x0e\x00'\x00\x00\x00\x00\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\xff\xd8\x0ex"\x00\x00\x00\x00\x00'
                                b'\x04\x00\x0b\xffC\xff\x13\x90\x01\x04\x00\x0f\x01\r\xb6j'
                                b'\x0f\x01\x17\x87f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04'
                                b'\x08\x0f\n\x01\x00\x00\x00\x02\x00\x02\x00\x00\xb9\x03\x00\x00'
                                b'\xc3\xc2\x00[K\xcf\x01\x00\x00\x00\xa2\xff\x00\x00\x00\x00'
                                b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x01\n"
                                b'\x00\x00\x80\xc3y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x04/&\x0b\x12\x06\xff\xff\x11#+$5\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x04/&\x0b\x12\x06\xff\xff\x11#+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x01\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x00\x00\x00\x00\n\xc2)\x14\xc5\xc3\x00\x00\x08)\x17\x00'
                                b'\xff\xff\x00\x00\x00\x00\x9fU\xeb\x99\x04\x07\x00\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFE2,
            'rom_bank': 0x01,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x17,
            'b': 0x01,
            'c': 0x01,
            'd': 0x00,
            'e': 0xDE,
            'f': 0x80,
            'hl': 0xC2E8},
    ],
}

MUTATIONS = {
    'CheckSandAttackOrSmokescreenSubstatus': {   'source_symbol': 'CheckSandAttackOrSmokescreenSubstatus',
        'before': '\tif (status.a == 0)',
        'after': '\tif (status.a != 0)',
        'case_ids': ['CheckSandAttackOrSmokescreenSubstatus-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CountTurnDuelistPokemonWithActivePkmnPower': {   'source_symbol': 'CountTurnDuelistPokemonWithActivePkmnPower',
        'before': '\tif (arena != 0xFF) {',
        'after': '\tif (arena == 0xFF) {',
        'case_ids': ['CountTurnDuelistPokemonWithActivePkmnPower-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CountPokemonWithActivePkmnPowerInBothPlayAreas': {   'source_symbol': 'CountPokemonWithActivePkmnPowerInBothPlayAreas',
        'before': '	uint8_t count = (uint8_t)(turn.a + other.a);',
        'after': '	uint8_t count = (uint8_t)(turn.a - other.a);',
        'case_ids': ['CountPokemonWithActivePkmnPowerInBothPlayAreas-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckIsIncapableOfUsingPkmnPower': {   'source_symbol': 'CheckIsIncapableOfUsingPkmnPower',
        'before': '\tif (a == PLAY_AREA_ARENA) {',
        'after': '\tif (a != PLAY_AREA_ARENA) {',
        'case_ids': ['CheckIsIncapableOfUsingPkmnPower-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckIsIncapableOfUsingPkmnPower_ArenaCard': {   'source_symbol': 'CheckIsIncapableOfUsingPkmnPower_ArenaCard',
        'before': '\treturn CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_ARENA);',
        'after': '\treturn CheckIsIncapableOfUsingPkmnPower((PLAY_AREA_ARENA + 1u));',
        'case_ids': ['CheckIsIncapableOfUsingPkmnPower_ArenaCard-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleDoubleDamageSubstatus': {   'source_symbol': 'HandleDoubleDamageSubstatus',
        'before': 'de = (uint16_t)(de << 1);',
        'after': 'de = (uint16_t)(de >> 1);',
        'case_ids': [   'HandleDoubleDamageSubstatus-1',
                        'HandleDoubleDamageSubstatus-0',
                        'HandleDoubleDamageSubstatus-2',
                        'HandleDoubleDamageSubstatus-3',
                        'HandleDoubleDamageSubstatus-4'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleDamageReductionExceptSubstatus2': {   'source_symbol': 'HandleDamageReductionExceptSubstatus2',
        'before': '\tif (gb_read8(wNoDamageOrEffect_ADDR) != 0)',
        'after': '\tif (gb_read8(wNoDamageOrEffect_ADDR) == 0)',
        'case_ids': ['HandleDamageReductionExceptSubstatus2-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleDamageReduction': {   'source_symbol': 'HandleDamageReduction',
        'before': '\tif (sub2.a == SUBSTATUS2_REDUCE_BY_20)',
        'after': '\tif (sub2.a != SUBSTATUS2_REDUCE_BY_20)',
        'case_ids': ['HandleDamageReduction-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleCantAttackSubstatus': {   'source_symbol': 'HandleCantAttackSubstatus',
        'before': '\tif (sub2.a == SUBSTATUS2_TAIL_WAG)',
        'after': '\tif (sub2.a != SUBSTATUS2_TAIL_WAG)',
        'case_ids': ['HandleCantAttackSubstatus-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleAmnesiaSubstatus': {   'source_symbol': 'HandleAmnesiaSubstatus',
        'before': '\tif (sub2.a != SUBSTATUS2_AMNESIA)',
        'after': '\tif (sub2.a == SUBSTATUS2_AMNESIA)',
        'case_ids': ['HandleAmnesiaSubstatus-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleNoDamageOrEffectSubstatus': {   'source_symbol': 'HandleNoDamageOrEffectSubstatus_PkmnPower',
        'before': '\te = gb_read8(wTempTurnDuelistCardID_ADDR);\n'
                  '\td = 0u;\n'
                  '\tLoadCardDataToBuffer2_FromCardID(e);',
        'after': '\te = gb_read8(wTempTurnDuelistCardID_ADDR);\n'
                 '\tLoadCardDataToBuffer2_FromCardID(e);',
        'case_ids': ['HandleNoDamageOrEffectSubstatus-10'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckNoDamageOrEffect': {   'source_symbol': 'CheckNoDamageOrEffect',
        'before': '\tif (val == 0)',
        'after': '\tif (val != 0)',
        'case_ids': ['CheckNoDamageOrEffect-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'IsClairvoyanceActive': {   'source_symbol': 'IsClairvoyanceActive',
        'before': '\t\treturn (PkmnPowerCountResult){muk.a, 0x00u, muk.de};',
        'after': '\t\treturn (PkmnPowerCountResult){muk.a, 0x01u, muk.de};',
        'case_ids': ['IsClairvoyanceActive-2'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'GetLoadedCard1RetreatCost': {   'source_symbol': 'GetLoadedCard1RetreatCost',
        'before': '\twhile (gb_read8(bench) != 0xFFu) {',
        'after': '\twhile (gb_read8(bench) == 0xFFu) {',
        'case_ids': ['GetLoadedCard1RetreatCost-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckUnableToRetreatDueToEffect': {   'source_symbol': 'CheckUnableToRetreatDueToEffect',
        'before': '\tif (sub2.a != SUBSTATUS2_ACID)',
        'after': '\tif (sub2.a == SUBSTATUS2_ACID)',
        'case_ids': ['CheckUnableToRetreatDueToEffect-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckCantUseTrainerDueToEffect': {   'source_symbol': 'CheckCantUseTrainerDueToEffect',
        'before': '\t\treturn (TrainerEffectResult){0xA0u, sub3.hl};',
        'after': '\t\treturn (TrainerEffectResult){0xA1u, sub3.hl};',
        'case_ids': ['CheckCantUseTrainerDueToEffect-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'IsPrehistoricPowerActive': {   'source_symbol': 'IsPrehistoricPowerActive',
        'before': '\tif (!(aero.f & 0x10u))',
        'after': '\tif (!(aero.f | 0x10u))',
        'case_ids': ['IsPrehistoricPowerActive-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'ClearDamageReductionSubstatus2': {   'source_symbol': 'ClearDamageReductionSubstatus2',
        'before': '\tif (sub2.a == SUBSTATUS2_REDUCE_BY_20 || sub2.a == SUBSTATUS2_POUNCE ||',
        'after': '\tif (sub2.a != SUBSTATUS2_REDUCE_BY_20 || sub2.a == SUBSTATUS2_POUNCE ||',
        'case_ids': ['ClearDamageReductionSubstatus2-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'UpdateSubstatusConditions_StartOfTurn': {   'source_symbol': 'UpdateSubstatusConditions_StartOfTurn',
        'before': '\tif (sub1.a != SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)',
        'after': '\tif (sub1.a == SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)',
        'case_ids': ['UpdateSubstatusConditions_StartOfTurn-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'UpdateSubstatusConditions_EndOfTurn': {   'source_symbol': 'UpdateSubstatusConditions_EndOfTurn',
        'before': '\tif (sub1.a == SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)',
        'after': '\tif (sub1.a != SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)',
        'case_ids': ['UpdateSubstatusConditions_EndOfTurn-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'IsRainDanceActive': {   'source_symbol': 'IsRainDanceActive',
        'before': '\tif (!(blastoise.f & 0x10u))',
        'after': '\tif (!(blastoise.f | 0x10u))',
        'case_ids': ['IsRainDanceActive-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'ClearChangedTypesIfMuk': {   'source_symbol': 'ClearChangedTypesIfMuk',
        'before': '\tif ((uint8_t)id != MUK)',
        'after': '\tif ((uint8_t)id == MUK)',
        'case_ids': ['ClearChangedTypesIfMuk-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'CheckRainDanceScenario': {   'source_symbol': 'CheckRainDanceScenario',
        'before': '\tif (card_type != TYPE_ENERGY_WATER)',
        'after': '\tif (card_type == TYPE_ENERGY_WATER)',
        'case_ids': ['CheckRainDanceScenario-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleStrikesBack_AgainstDamagingAttack': {   'source_symbol': 'HandleStrikesBack_AgainstDamagingAttack',
        'before': '\t\treturn (StrikesBackResult){a, f_cp(a, 0x04u)};',
        'after': '\t\treturn (StrikesBackResult){a, f_cp(a, 0x05u)};',
        'case_ids': ['HandleStrikesBack_AgainstDamagingAttack-3'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'ApplyStrikesBack_AgainstResidualAttack': {   'source_symbol': 'ApplyStrikesBack_AgainstResidualAttack',
        'before': '\tuint8_t card_id = wTempTurnDuelistCardID;',
        'after': '\tuint8_t card_id = 0;',
        'case_ids': [   'ApplyStrikesBack_AgainstResidualAttack-0',
                        'ApplyStrikesBack_AgainstResidualAttack-1',
                        'ApplyStrikesBack_AgainstResidualAttack-2'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleStrikesBack_AgainstResidualAttack': {   'source_symbol': 'HandleStrikesBack_AgainstResidualAttack',
        'before': '\t\tuint8_t f = 0x40u;\n\t\tif ((card_id & 0x0Fu) < (MACHAMP & 0x0Fu))',
        'after': '\t\tuint8_t f = 0x50u;\n\t\tif ((card_id & 0x0Fu) < (MACHAMP & 0x0Fu))',
        'case_ids': ['HandleStrikesBack_AgainstResidualAttack-0'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleDestinyBondSubstatus': {   'source_symbol': 'HandleDestinyBondSubstatus',
        'before': 'DestinyBondResult HandleDestinyBondSubstatus(void)\n'
                  '{\n'
                  '\tDuelistVarResult substatus = '
                  'GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);',
        'after': 'DestinyBondResult HandleDestinyBondSubstatus(void)\n'
                 '{\n'
                 '\tDuelistVarResult substatus = '
                 'GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);',
        'case_ids': ['HandleDestinyBondSubstatus-0', 'HandleDestinyBondSubstatus-4'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleNShieldAndTransparency': {   'source_symbol': 'HandleNShieldAndTransparency',
        'before': '\t\t\tgb_write8(wNoDamageOrEffect_ADDR, NO_DAMAGE_OR_EFFECT_NSHIELD);',
        'after': '\t\t\tgb_write8(wNoDamageOrEffect_ADDR, 0x40u);',
        'case_ids': ['HandleNShieldAndTransparency-1'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleTransparency': {   'source_symbol': 'HandleTransparency',
        'before': '\tif (category == POKEMON_POWER) {\n'
                  '\t\treturn (HandleTransparencyResult){category, category ? 0u : 0x80u, hl};',
        'after': '\tif (category == POKEMON_POWER) {\n'
                 '\t\treturn (HandleTransparencyResult){0x05u, category ? 0u : 0x80u, hl};',
        'case_ids': ['HandleTransparency-1', 'HandleTransparency-2'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleDamageReductionOrNoDamageFromPkmnPowerEffects': {   'source_symbol': 'HandleDamageReductionOrNoDamageFromPkmnPowerEffects',
        'before': '\tNoDamageOrEffectResult no_damage = '
                  'HandleNoDamageOrEffectSubstatus_PkmnPower((uint8_t)(de >> 8), location, hl);',
        'after': '\tNoDamageOrEffectResult no_damage = '
                 'HandleNoDamageOrEffectSubstatus((uint8_t)(de >> 8), location, hl);',
        'case_ids': ['HandleDamageReductionOrNoDamageFromPkmnPowerEffects-3'],
        'source': 'src/profiles/extended/home/substatus.c'},
    'HandleSandAttackOrSmokescreenSubstatus': {   'source_symbol': 'HandleSandAttackOrSmokescreenSubstatus',
        'before': '\t\t(uint16_t)((uint16_t)wait.d << 8 | wait.e), wait.hl,',
        'after': '\t\tAttackUnsuccessfulText, wait.hl,',
        'case_ids': ['HandleSandAttackOrSmokescreenSubstatus-4'],
        'source': 'src/profiles/extended/home/substatus.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
