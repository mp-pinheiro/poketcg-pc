"""Extended oracle-diff cases for booster_packs, seeded from tests/cases/booster_packs.py."""

CONTRACT = {
    'GetCurrentRarityAmount': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetBoosterCardType': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CalculateTypeChances': {'compare': ('a', 'd', 'e'), 'preserve': ('d', 'e')},
    'UpdateBoosterCardTypesChanceByte': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'AppendCurrentCardToHL': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e'),
    'wram_out': True},
    'AddBoosterCardToTempCardCollection': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'AddBoosterCardToDrawnEnergies': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'AddBoosterEnergyToDrawnEnergies': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'ZeroBoosterRarityData': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'GenerateTwoTypesEnergyBooster': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GenerateRandomEnergy': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'hl'),
    'wram_out': True},
    'GenerateEnergyBoosterGrassPsychic': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GenerateEnergyBoosterLightningFire': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GenerateEnergyBoosterWaterFighting': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'GenerateRandomEnergyBooster': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'hl'),
    'wram_out': True},
    'PutEnergiesAndNonEnergiesTogether': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'LoadRarityAmountsToWram': {'compare': (), 'preserve': ()},
    'DetermineBoosterCardType': {'compare': ('a',), 'preserve': ()},
    'FindBoosterDataPointer': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'AddBoosterCardToDrawnNonEnergies': {'compare': (), 'preserve': (), 'wram_out': True},
    'AddBoosterCardsToCollection': {'compare': ('a', 'f', 'hl'), 'preserve': ('hl',), 'wram_out': True},
    'GenerateBoosterEnergies': {'compare': (), 'preserve': (), 'wram_out': True},
    'DetermineBoosterCard': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('d', 'e')},
    'CheckCardInSetAndRarity': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CheckCardAlreadyDrawn': {'compare': ('a', 'f'), 'preserve': ()},
    'FindCardsInSetAndRarity': {'compare': ('a', 'f', 'd', 'e'), 'preserve': (), 'wram_out': True},
    'GenerateBoosterNonEnergies': {'compare': ('a', 'f'), 'preserve': ()},
    'InitBoosterData': {'compare': (), 'preserve': (), 'wram_out': True, 'sram_out': True},
    'GenerateBoosterPack': {'compare': (), 'preserve': (), 'wram_out': True, 'sram_out': True},
    'GenerateFightingEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateFireEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateGrassEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateLightningEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GeneratePsychicEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'GenerateWaterEnergy': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'GetCurrentRarityAmount': [
        {'wram': {0xD65A: b'\x00'}},
        {'wram': {0xD65A: b'\x01'}},
        {'wram': {0xD65A: b'\x02'}},
        {'wram': {0xD65A: b'\xff'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD65A: b'\x03'}},
    ],
    'GetBoosterCardType': [
        {'a': 0x00},
        {'a': 0x01},
        {'a': 0x07},
        {'a': 0x08},
        {'a': 0x0F},
        {'a': 0x10},
        {'a': 0x11},
        {'a': 0xFF},
        {'a': 0x05, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x11, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'CalculateTypeChances': [
        {   'wram': {   0xD65F: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD677: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD668: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD4B7: b'\x00'}},
        {   'wram': {   0xD65F: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xD677: b'\x02\x02\x02\x02\x02\x02\x02\x02\x02',
                        0xD668: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD4B7: b'\xff'}},
        {   'wram': {   0xD65F: b'\x01\x00\x01\x00\x01\x00\x01\x00\x01',
                        0xD677: b'\n\n\x00\n\x14\x00\x05\n\x1e',
                        0xD668: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xD4B7: b'\xaa'}},
        {   'wram': {   0xD65F: b'\x00\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xD677: b'\xff@@@@\x00\x00\x00\x00',
                        0xD668: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11',
                        0xD4B7: b'\x11'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD65F: b'\x02\x02\x02\x02\x02\x02\x02\x02\x02',
                        0xD677: b'\x03\x03\x03\x03\x03\x03\x03\x03\x03',
                        0xD668: b'\xee\xee\xee\xee\xee\xee\xee\xee\xee',
                        0xD4B7: b'\xee'}},
    ],
    'UpdateBoosterCardTypesChanceByte': [
        {   'wram': {0xD659: b'\x00', 0xD65B: b'\x00', 0xD677: b'\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xD677: 0x08}},
        {   'wram': {0xD659: b'\x01', 0xD65B: b'\x02', 0xD677: b'\t\x05\x07\x05\x00\x00\x00\x00'},
            'read': {0xD677: 0x08}},
        {   'wram': {0xD659: b'\x03', 0xD65B: b'\x05', 0xD677: b'\t\x05\x07\x05\x00\x00\x00\x00'},
            'read': {0xD677: 0x08}},
        {   'wram': {0xD659: b'\x02', 0xD65B: b'@', 0xD677: b'\x01\x02\x01\x04\x00\x00\x00\x00'},
            'read': {0xD677: 0x08}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD659: b'\x04', 0xD65B: b'\x03', 0xD677: b'\t\x05\x07\x05\x03\x00\x00\x00'},
            'read': {0xD677: 0x08}},
    ],
    'AppendCurrentCardToHL': [
        {'hl': 0xC4F0, 'wram': {0xC4F0: b'\x00', 0xD657: b'\x12'}, 'read': {0xC4F0: 0x02}},
        {'hl': 0xC500, 'wram': {0xC500: b'\x01\x02\x00', 0xD657: b'4'}, 'read': {0xC500: 0x04}},
        {'hl': 0xC510, 'wram': {0xC510: b'\xaa\xbb\xcc\x00', 0xD657: b'~'}, 'read': {0xC510: 0x05}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC520,
            'wram': {0xC520: b'\x00', 0xD657: b'\xff'},
            'read': {0xC520: 0x02}},
    ],
    'AddBoosterCardToTempCardCollection': [
        {   'wram': {0xD657: b'\x00', 0xC000: b'\x00'},
            'expect': {0xC000: b'\x01'},
            'expect_regs': {'a': 0x00, 'f': 0x00, 'hl': 0x00}},
        {   'wram': {0xD657: b'*', 0xC02A: b'\x0f'},
            'expect': {0xC02A: b'\x10'},
            'expect_regs': {'a': 0x2A, 'f': 0x20, 'hl': 0x00}},
        {   'wram': {0xD657: b'\xff', 0xC0FF: b'\xff'},
            'expect': {0xC0FF: b'\x00'},
            'expect_regs': {'a': 0xFF, 'f': 0xA0, 'hl': 0x00}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD657: b'\x80', 0xC080: b'\xfe'},
            'expect': {0xC080: b'\xff'},
            'expect_regs': {   'a': 0x80,
                               'f': 0x10,
                               'b': 0xBB,
                               'c': 0xCC,
                               'd': 0xDD,
                               'e': 0xEE,
                               'hl': 0x1234}},
    ],
    'AddBoosterCardToDrawnEnergies': [
        {   'wram': {0xD657: b'\x12', 0xC416: b'\x00', 0xC012: b'\x00'},
            'read': {0xC416: 0x02, 0xC012: 0x01}},
        {   'wram': {0xD657: b'\xff', 0xC416: b'\x01\x02\x00', 0xC0FF: b'\x0f'},
            'read': {0xC416: 0x04, 0xC0FF: 0x01}},
        {   'wram': {0xD657: b'\x00', 0xC416: b'\xaa\x00', 0xC000: b'\xff'},
            'read': {0xC416: 0x03, 0xC000: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD657: b'~', 0xC416: b'\x00', 0xC07E: b'\xff'},
            'read': {0xC416: 0x02, 0xC07E: 0x01}},
    ],
    'AddBoosterEnergyToDrawnEnergies': [
        {   'a': 0x12,
            'wram': {0xC416: b'\x00', 0xD657: b'\x00', 0xC012: b'\x00'},
            'expect': {0xC416: b'\x12\x00', 0xD657: b'\x12', 0xC012: b'\x01'},
            'expect_regs': {'a': 0x12, 'f': 0x00, 'hl': 0x00}},
        {   'a': 0x2A,
            'hl': 0x4567,
            'wram': {0xC416: b'\x01\x02\x00', 0xD657: b'\x00', 0xC02A: b'\x0f'},
            'expect': {0xC416: b'\x01\x02*\x00', 0xD657: b'*', 0xC02A: b'\x10'},
            'expect_regs': {'a': 0x2A, 'f': 0x20, 'hl': 0x4567}},
        {   'a': 0xFF,
            'wram': {0xC416: b'\xaa\xbb\x00', 0xD657: b'\x00', 0xC0FF: b'\xff'},
            'expect': {0xC416: b'\xaa\xbb\xff\x00', 0xD657: b'\xff', 0xC0FF: b'\x00'},
            'expect_regs': {'a': 0xFF, 'f': 0x80, 'hl': 0x00}},
        {   'a': 0x80,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC416: b'\x00', 0xD657: b'\x00', 0xC080: b'\xfe'},
            'expect': {0xC416: b'\x80\x00', 0xD657: b'\x80', 0xC080: b'\xff'},
            'expect_regs': {   'a': 0x80,
                               'f': 0x00,
                               'b': 0xBB,
                               'c': 0xCC,
                               'd': 0xDD,
                               'e': 0xEE,
                               'hl': 0x1234}},
    ],
    'ZeroBoosterRarityData': [
        {   'wram': {0xD65C: b'\x01', 0xD65D: b'\x02', 0xD65E: b'\x03'},
            'expect': {0xD65C: b'\x00', 0xD65D: b'\x00', 0xD65E: b'\x00'}},
        {   'wram': {0xD65C: b'\xff', 0xD65D: b'\x80', 0xD65E: b'\x7f'},
            'expect': {0xD65C: b'\x00', 0xD65D: b'\x00', 0xD65E: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD65C: b'\xaa', 0xD65D: b'\xbb', 0xD65E: b'\xcc'},
            'expect': {0xD65C: b'\x00', 0xD65D: b'\x00', 0xD65E: b'\x00'}},
    ],
    'GenerateTwoTypesEnergyBooster': [
        {   'hl': 0xC4F0,
            'wram': {   0xC4F0: b'\x12*',
                        0xC416: b'\x00',
                        0xC012: b'\x00',
                        0xC02A: b'\x00',
                        0xD65C: b'\x01',
                        0xD65D: b'\x02',
                        0xD65E: b'\x03'},
            'expect': {   0xC416: b'\x12\x12\x12\x12\x12*****\x00',
                          0xD657: b'*',
                          0xC012: b'\x05',
                          0xC02A: b'\x05',
                          0xD65C: b'\x00',
                          0xD65D: b'\x00',
                          0xD65E: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0x80, 'b': 0x00, 'c': 0x00, 'hl': 0xC502}},
        {   'hl': 0xC500,
            'wram': {   0xC500: b'\x03~',
                        0xC416: b'\x00',
                        0xC003: b'\x00',
                        0xC07E: b'\x00',
                        0xD65C: b'\xff',
                        0xD65D: b'\xff',
                        0xD65E: b'\xff'},
            'expect': {   0xC416: b'\x03\x03\x03\x03\x03~~~~~\x00',
                          0xD657: b'~',
                          0xC003: b'\x05',
                          0xC07E: b'\x05',
                          0xD65C: b'\x00',
                          0xD65D: b'\x00',
                          0xD65E: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0x80, 'b': 0x00, 'c': 0x00, 'hl': 0xC512}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC520,
            'wram': {   0xC520: b'\x80\xff',
                        0xC416: b'\x00',
                        0xC080: b'\x00',
                        0xC0FF: b'\x00',
                        0xD65C: b'\xaa',
                        0xD65D: b'\xbb',
                        0xD65E: b'\xcc'},
            'expect': {   0xC416: b'\x80\x80\x80\x80\x80\xff\xff\xff\xff\xff\x00',
                          0xD657: b'\xff',
                          0xC080: b'\x05',
                          0xC0FF: b'\x05',
                          0xD65C: b'\x00',
                          0xD65D: b'\x00',
                          0xD65E: b'\x00'},
            'expect_regs': {   'a': 0x00,
                               'f': 0x80,
                               'b': 0x00,
                               'c': 0x00,
                               'd': 0xDD,
                               'e': 0xEE,
                               'hl': 0xC532}},
    ],
    'GenerateRandomEnergy': [
        {   'wram': {   0xCACA: b'\x00\x00\x00',
                        0xC416: b'\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'wram': {   0xCACA: b'\x124V',
                        0xC416: b'\x01\x02\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'wram': {   0xCACA: b'\xde\xad\xbe',
                        0xC416: b'\xaa\xbb\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCACA: b'\x01\x00\x80',
                        0xC416: b'\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
    ],
    'GenerateEnergyBoosterGrassPsychic': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'GenerateEnergyBoosterLightningFire': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'GenerateEnergyBoosterWaterFighting': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'GenerateRandomEnergyBooster': [
        {   'wram': {   0xCACA: b'\x00\x00\x00',
                        0xC416: b'\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'wram': {   0xCACA: b'\x124V',
                        0xC416: b'\x01\x02\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'wram': {   0xCACA: b'\xde\xad\xbe',
                        0xC416: b'\xaa\xbb\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCACA: b'\x01\x00\x80',
                        0xC416: b'\x00',
                        0xC000: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
    ],
    'PutEnergiesAndNonEnergiesTogether': [
        {   'a': 0x11,
            'f': 0x00,
            'b': 0x22,
            'c': 0x33,
            'd': 0x44,
            'e': 0x55,
            'hl': 0x2468,
            'wram': {0xC416: b'\x00', 0xC400: b'\x00', 0xD657: b'w'},
            'expect': {0xC400: b'\x00', 0xD657: b'w'}},
        {   'a': 0x66,
            'f': 0x10,
            'b': 0x77,
            'c': 0x88,
            'd': 0x99,
            'e': 0xAA,
            'hl': 0x1357,
            'wram': {0xC416: b'\x12\x00', 0xC400: b'\x00', 0xD657: b'\x00'},
            'expect': {0xC400: b'\x12\x00', 0xD657: b'\x12'}},
        {   'a': 0x01,
            'f': 0x20,
            'b': 0x02,
            'c': 0x03,
            'd': 0x04,
            'e': 0x05,
            'hl': 0x3456,
            'wram': {0xC416: b'\x12*\x00', 0xC400: b'\x99\x00', 0xD657: b'\x00'},
            'expect': {0xC400: b'\x99\x12*\x00', 0xD657: b'*'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC416: b'\x80\xff\x00', 0xC400: b'\xaa\x00', 0xD657: b'\xcc'},
            'expect': {0xC400: b'\xaa\x80\xff\x00', 0xD657: b'\xff'}},
    ],
    'LoadRarityAmountsToWram': [
        {'wram': {0xD674: b'\x00'}, 'read': {0xD65C: 0x01, 0xD65D: 0x01, 0xD65E: 0x01}},
        {'wram': {0xD674: b'\x01'}, 'read': {0xD65C: 0x01, 0xD65D: 0x01, 0xD65E: 0x01}},
        {'wram': {0xD674: b'\x02'}, 'read': {0xD65C: 0x01, 0xD65D: 0x01, 0xD65E: 0x01}},
        {'wram': {0xD674: b'\x03'}, 'read': {0xD65C: 0x01, 0xD65D: 0x01, 0xD65E: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD674: b'\x00'},
            'read': {0xD65C: 0x01, 0xD65D: 0x01, 0xD65E: 0x01}},
    ],
    'DetermineBoosterCardType': [
        {   'a': 0x00,
            'wram': {0xD668: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0xD659: b'\xff', 0xD4B7: b'\xff'},
            'read': {0xD659: 0x01, 0xD4B7: 0x01}},
        {   'a': 0x00,
            'wram': {0xD668: b'\x01\x00\x00\x00\x00\x00\x00\x00\x00', 0xD659: b'\xff'},
            'read': {0xD659: 0x01, 0xD4B7: 0x01}},
        {   'a': 0x02,
            'wram': {0xD668: b'\x00\x02\x03\x00\x00\x00\x00\x00\x00', 0xD659: b'\xff'},
            'read': {0xD659: 0x01, 0xD4B7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD668: b' \x10\x08\x04\x02\x01\x00\x00\x00', 0xD659: b'\xff'},
            'read': {0xD659: 0x01, 0xD4B7: 0x01}},
    ],
    'FindBoosterDataPointer': [
        {'wram': {0xD656: b'\x00'}},
        {'wram': {0xD656: b'\x01'}},
        {'wram': {0xD656: b'\x02'}},
        {'wram': {0xD656: b'\x1b'}},
        {'wram': {0xD656: b'\x1c'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD656: b'\x1b'}},
    ],
    'AddBoosterCardToDrawnNonEnergies': [
        {   'wram': {0xC400: b'\x00', 0xD657: b'\x12', 0xC012: b'\x00'},
            'read': {0xC400: 0x02, 0xC012: 0x01}},
        {   'wram': {0xC400: b'\x01\x02\x00', 0xD657: b'\xff', 0xC0FF: b'\x0f'},
            'read': {0xC400: 0x04, 0xC0FF: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC400: b'\x00', 0xD657: b'~', 0xC07E: b'\x00'},
            'read': {0xC400: 0x02, 0xC07E: 0x01}},
    ],
    'AddBoosterCardsToCollection': [
        {   'hl': 0x1234,
            'wram': {0xC400: b'\x05\x0c\x00'},
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'read': {0xC400: 0x03},
            'sread': {0x00: {0xA105: 0x01, 0xA10C: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x5678,
            'wram': {0xC400: b'*\x00'},
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'read': {0xC400: 0x02},
            'sread': {0x00: {0xA12A: 0x01}}},
    ],
    'GenerateBoosterEnergies': [
        {   'wram': {0xD675: b'\x01\x00', 0xC416: b'\x00', 0xD657: b'\x00', 0xC001: b'\x00'},
            'expect': {0xC416: b'\x01\x00', 0xD657: b'\x01', 0xC001: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD675: b'\x01\x00', 0xC416: b'\x00', 0xD657: b'\x00', 0xC001: b'\x00'},
            'expect': {0xC416: b'\x01\x00', 0xD657: b'\x01', 0xC001: b'\x01'}},
    ],
    'DetermineBoosterCard': [
        {'d': 0xDD, 'e': 0xEE, 'wram': {0xD659: b'\x02', 0xD661: b'\x00', 0xD120: b'\x10\x01 \x02\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD659: b'\x02', 0xD661: b'\x00', 0xD120: b'\x10\x01 \x02\x00'}},
        {'d': 0x11, 'e': 0x22, 'wram': {0xD659: b'\x03', 0xD662: b'\x00', 0xD120: b'\x00'}},
    ],
    'CheckCardInSetAndRarity': [
        {'b': 0x11, 'c': 0x22, 'd': 0x33, 'e': 0x01, 'hl': 0x4455, 'wram': {0xD65A: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0x01,
            'hl': 0x1234,
            'wram': {0xD65A: b'\x00'}},
        {   'b': 0x11,
            'c': 0x22,
            'd': 0x33,
            'e': 0x40,
            'hl': 0x4455,
            'wram': {0xD65A: b'\x02', 0xD674: b'\t'}},
        {   'b': 0x11,
            'c': 0x22,
            'd': 0x33,
            'e': 0x40,
            'hl': 0x4455,
            'wram': {0xD65A: b'\x02', 0xD674: b'\x04'}},
    ],
    'CheckCardAlreadyDrawn': [
        {'wram': {0xD657: b'\x03', 0xC003: b'\x00'}, 'expect_regs': {'a': 0x00, 'f': 0x00}},
        {'wram': {0xD657: b'\x03', 0xC003: b'\x01'}, 'expect_regs': {'a': 0x01, 'f': 0x90}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD657: b'\x03', 0xC003: b'\x02'},
            'expect_regs': {'a': 0x02, 'f': 0x10}},
    ],
    'FindCardsInSetAndRarity': [
        {   'wram': {   0xC001: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01'},
            'read': {0xD65F: 0x09, 0xD120: 0x01, 0xD657: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC001: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01'},
            'read': {0xD65F: 0x09, 0xD120: 0x01, 0xD657: 0x01}},
    ],
    'GenerateBoosterNonEnergies': [
        {   'wram': {0xD65A: b'\x00', 0xD65C: b'\x00', 0xD65D: b'\x00', 0xD65E: b'\x00'},
            'expect_regs': {'a': 0xFF, 'f': 0x00}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD65A: b'\x00', 0xD65C: b'\x00', 0xD65D: b'\x00', 0xD65E: b'\x00'},
            'expect_regs': {'a': 0xFF, 'f': 0x00}},
    ],
    'InitBoosterData': [
        {   'wram': {   0xD656: b'\x00',
                        0xC400: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff',
                        0xC000: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD674: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD65B: b'\xff'},
            'instruction_budget': 0x30D40,
            'cycle_budget': 0xF4240,
            'read': {0xC400: 0x16, 0xC000: 0x0100, 0xD674: 0x0C, 0xD65B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD656: b'\x01',
                        0xC400: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff',
                        0xC000: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD674: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD65B: b'\xff'},
            'instruction_budget': 0x30D40,
            'cycle_budget': 0xF4240,
            'read': {0xC400: 0x16, 0xC000: 0x0100, 0xD674: 0x0C, 0xD65B: 0x01}},
    ],
    'GenerateBoosterPack': [
        {   'a': 0x00,
            'wram': {   0xC400: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff',
                        0xC000: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'},
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200,
            'read': {0xC400: 0x16},
            'sread': {0x00: {0xA100: 0x0100}}},
        {   'a': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC400: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff',
                        0xC000: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'},
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200,
            'read': {0xC400: 0x16},
            'sread': {0x00: {0xA100: 0x0100}}},
    ],
    'GenerateFightingEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE,
         'hl': 0x1234, 'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
    'GenerateFireEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
    'GenerateGrassEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
    'GenerateLightningEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
    'GeneratePsychicEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
    'GenerateWaterEnergy': [
        {'wram': {0xC000: b'\x00', 0xC416: b'\x00'}},
        {'wram': {0xC000: b'\xff', 0xC416: b'\x00'}},
    ],
}

MUTATIONS = {
    'GetCurrentRarityAmount': {   'source_symbol': 'GetCurrentRarityAmount',
        'before': '(uint16_t)(wBoosterData_CommonAmount_ADDR + a)',
        'after': '(uint16_t)(wBoosterData_CommonAmount_ADDR + a + 1u)',
        'case_ids': ['GetCurrentRarityAmount-0', 'GetCurrentRarityAmount-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GetBoosterCardType': {   'source_symbol': 'GetBoosterCardType',
        'before': '\tif (a >= NUM_CARD_TYPES)',
        'after': '\tif (a > NUM_CARD_TYPES)',
        'case_ids': ['GetBoosterCardType-6'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'CalculateTypeChances': {   'source_symbol': 'CalculateTypeChances',
        'before': '\t\tif (amount == 0u)',
        'after': '\t\tif (amount == 1u)',
        'case_ids': ['CalculateTypeChances-1', 'CalculateTypeChances-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'UpdateBoosterCardTypesChanceByte': {   'source_symbol': 'UpdateBoosterCardTypesChanceByte',
        'before': 'if (res == 0u || v < c) {',
        'after': 'if (v < c) {',
        'case_ids': [   'UpdateBoosterCardTypesChanceByte-0',
                        'UpdateBoosterCardTypesChanceByte-2',
                        'UpdateBoosterCardTypesChanceByte-4'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AppendCurrentCardToHL': {   'source_symbol': 'AppendCurrentCardToHL',
        'before': 'while (gb_read8(cursor++) != 0u)',
        'after': 'while (gb_read8(cursor++) == 0u)',
        'case_ids': [   'AppendCurrentCardToHL-0',
                        'AppendCurrentCardToHL-1',
                        'AppendCurrentCardToHL-2',
                        'AppendCurrentCardToHL-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterCardToTempCardCollection': {   'source_symbol': 'AddBoosterCardToTempCardCollection',
        'before': 'gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));',
        'after': 'gb_write8(slot, (uint8_t)(gb_read8(slot) + 2u));',
        'case_ids': [   'AddBoosterCardToTempCardCollection-0',
                        'AddBoosterCardToTempCardCollection-1',
                        'AddBoosterCardToTempCardCollection-2',
                        'AddBoosterCardToTempCardCollection-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterCardToDrawnEnergies': {   'source_symbol': 'AddBoosterCardToDrawnEnergies',
        'before': 'AddBoosterCardToTempCardCollection();',
        'after': 'gb_write8(address, (uint8_t)(old + 2u));',
        'case_ids': [   'AddBoosterCardToDrawnEnergies-0',
                        'AddBoosterCardToDrawnEnergies-1',
                        'AddBoosterCardToDrawnEnergies-2',
                        'AddBoosterCardToDrawnEnergies-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterEnergyToDrawnEnergies': {   'source_symbol': 'AddBoosterEnergyToDrawnEnergies',
        'before': 'wBoosterCurrentCard = a;',
        'after': 'wBoosterCurrentCard = (uint8_t)(a + 1u);',
        'case_ids': [   'AddBoosterEnergyToDrawnEnergies-0',
                        'AddBoosterEnergyToDrawnEnergies-1',
                        'AddBoosterEnergyToDrawnEnergies-2',
                        'AddBoosterEnergyToDrawnEnergies-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'ZeroBoosterRarityData': {   'source_symbol': 'ZeroBoosterRarityData',
        'before': '\twBoosterData_RareAmount = 0u;',
        'after': '\twBoosterData_RareAmount = 1u;',
        'case_ids': [   'ZeroBoosterRarityData-0',
                        'ZeroBoosterRarityData-1',
                        'ZeroBoosterRarityData-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateTwoTypesEnergyBooster': {   'source_symbol': 'GenerateTwoTypesEnergyBooster',
        'before': '(void)AddBoosterEnergyToDrawnEnergies(card);',
        'after': '(void)AddBoosterEnergyToDrawnEnergies((uint8_t)(card + 1u));',
        'case_ids': [   'GenerateTwoTypesEnergyBooster-0',
                        'GenerateTwoTypesEnergyBooster-1',
                        'GenerateTwoTypesEnergyBooster-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateRandomEnergy': {   'source_symbol': 'GenerateRandomEnergy',
        'before': 'return AddBoosterEnergyToDrawnEnergies((uint8_t)(random + 1u));',
        'after': 'return AddBoosterEnergyToDrawnEnergies((uint8_t)(random + 2u));',
        'case_ids': [   'GenerateRandomEnergy-0',
                        'GenerateRandomEnergy-1',
                        'GenerateRandomEnergy-2',
                        'GenerateRandomEnergy-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateEnergyBoosterGrassPsychic': {   'source_symbol': 'GenerateEnergyBoosterGrassPsychic',
        'before': '\treturn GenerateTwoTypesEnergyBooster(0x63CDu);',
        'after': '\treturn GenerateTwoTypesEnergyBooster(0x63CBu);',
        'case_ids': ['GenerateEnergyBoosterGrassPsychic-0', 'GenerateEnergyBoosterGrassPsychic-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateEnergyBoosterLightningFire': {   'source_symbol': 'GenerateEnergyBoosterLightningFire',
        'before': '\treturn GenerateTwoTypesEnergyBooster(0x63C9u);',
        'after': '\treturn GenerateTwoTypesEnergyBooster(0x63CBu);',
        'case_ids': [   'GenerateEnergyBoosterLightningFire-0',
                        'GenerateEnergyBoosterLightningFire-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateEnergyBoosterWaterFighting': {   'source_symbol': 'GenerateEnergyBoosterWaterFighting',
        'before': '\treturn GenerateTwoTypesEnergyBooster(0x63CBu);',
        'after': '\treturn GenerateTwoTypesEnergyBooster(0x63C9u);',
        'case_ids': [   'GenerateEnergyBoosterWaterFighting-0',
                        'GenerateEnergyBoosterWaterFighting-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateRandomEnergyBooster': {   'source_symbol': 'GenerateRandomEnergyBooster',
        'before': '\t\t(void)GenerateRandomEnergy();',
        'after': '\t\t(void)GenerateRandomEnergy();\n\t\t(void)GenerateRandomEnergy();',
        'case_ids': [   'GenerateRandomEnergyBooster-0',
                        'GenerateRandomEnergyBooster-1',
                        'GenerateRandomEnergyBooster-2',
                        'GenerateRandomEnergyBooster-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'PutEnergiesAndNonEnergiesTogether': {   'source_symbol': 'PutEnergiesAndNonEnergiesTogether',
        'before': '\twhile ((a = *energy++) != 0u) {',
        'after': '\twhile ((a = *energy++) == 0u) {',
        'case_ids': [   'PutEnergiesAndNonEnergiesTogether-0',
                        'PutEnergiesAndNonEnergiesTogether-1',
                        'PutEnergiesAndNonEnergiesTogether-2',
                        'PutEnergiesAndNonEnergiesTogether-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'LoadRarityAmountsToWram': {   'source_symbol': 'LoadRarityAmountsToWram',
        'before': '\tuint8_t common = (set < 2u) ? 5u : 6u;',
        'after': '\tuint8_t common = (set < 2u) ? 6u : 5u;',
        'case_ids': [   'LoadRarityAmountsToWram-0',
                        'LoadRarityAmountsToWram-1',
                        'LoadRarityAmountsToWram-2',
                        'LoadRarityAmountsToWram-3',
                        'LoadRarityAmountsToWram-4'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'DetermineBoosterCardType': {   'source_symbol': 'DetermineBoosterCardType',
        'before': '\t\tuint8_t chance = *table;',
        'after': '\t\tuint8_t chance = (uint8_t)(*table + 1u);',
        'case_ids': [   'DetermineBoosterCardType-1',
                        'DetermineBoosterCardType-2',
                        'DetermineBoosterCardType-3'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'FindBoosterDataPointer': {   'source_symbol': 'FindBoosterDataPointer',
        'before': 'return (uint16_t)(BOOSTER_DATA_BASE + (uint16_t)pack * 0x0Cu);',
        'after': 'return (uint16_t)(BOOSTER_DATA_BASE + 1u + (uint16_t)pack * 0x0Cu);',
        'case_ids': [   'FindBoosterDataPointer-0',
                        'FindBoosterDataPointer-1',
                        'FindBoosterDataPointer-2',
                        'FindBoosterDataPointer-3',
                        'FindBoosterDataPointer-4',
                        'FindBoosterDataPointer-5'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterCardToDrawnNonEnergies': {   'source_symbol': 'AddBoosterCardToDrawnNonEnergies',
        'before': '\tAppendCurrentCardToHL(&cursor);\n\tAddBoosterCardToTempCardCollection();',
        'after': '\tAppendCurrentCardToHL(&cursor);\n\t(void)0;',
        'case_ids': [   'AddBoosterCardToDrawnNonEnergies-0',
                        'AddBoosterCardToDrawnNonEnergies-1',
                        'AddBoosterCardToDrawnNonEnergies-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'AddBoosterCardsToCollection': {   'source_symbol': 'AddBoosterCardsToCollection',
        'before': '\t\tAddCardToCollection(card);',
        'after': '\t\t(void)card;',
        'case_ids': ['AddBoosterCardsToCollection-0', 'AddBoosterCardsToCollection-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateBoosterEnergies': {   'source_symbol': 'GenerateBoosterEnergies',
        'before': '\t(void)AddBoosterEnergyToDrawnEnergies(a);',
        'after': '\t(void)AddBoosterEnergyToDrawnEnergies(0u);',
        'case_ids': ['GenerateBoosterEnergies-0', 'GenerateBoosterEnergies-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'DetermineBoosterCard': {   'source_symbol': 'DetermineBoosterCard',
        'before': 'return (DetermineBoosterCardResult){0u, 0x90u, b, c, d, e, hl};',
        'after': 'return (DetermineBoosterCardResult){0u, 0x80u, b, c, d, e, hl};',
        'case_ids': ['DetermineBoosterCard-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'CheckCardInSetAndRarity': {   'source_symbol': 'CheckCardInSetAndRarity',
        'before': 'if (cur_rarity != rarity) {',
        'after': 'if (cur_rarity == rarity) {',
        'case_ids': ['CheckCardInSetAndRarity-0', 'CheckCardInSetAndRarity-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'CheckCardAlreadyDrawn': {   'source_symbol': 'CheckCardAlreadyDrawn',
        'before': 'uint8_t value = gb_read8((uint16_t)(wTempCardCollection_ADDR + index));',
        'after': 'uint8_t value = gb_read8((uint16_t)(wTempCardCollection_ADDR + index + 1u));',
        'case_ids': ['CheckCardAlreadyDrawn-1', 'CheckCardAlreadyDrawn-2'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'FindCardsInSetAndRarity': {   'source_symbol': 'FindCardsInSetAndRarity',
        'before': 'for (uint16_t card_id = 1u; card_id <= NUM_CARDS; card_id++) {',
        'after': 'for (uint16_t card_id = 1u; card_id <= NUM_CARDS + 1u; card_id++) {',
        'case_ids': ['FindCardsInSetAndRarity-0', 'FindCardsInSetAndRarity-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateBoosterNonEnergies': {   'source_symbol': 'GenerateBoosterNonEnergies',
        'before': 'return (GenerateBoosterNonEnergiesResult){rarity, 0x00u};',
        'after': 'return (GenerateBoosterNonEnergiesResult){rarity, 0x10u};',
        'case_ids': ['GenerateBoosterNonEnergies-0', 'GenerateBoosterNonEnergies-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'InitBoosterData': {   'source_symbol': 'InitBoosterData',
        'before': '\t\t\tc = (uint8_t)(a + c);',
        'after': '\t\t\tc = (uint8_t)(a + c + 1u);',
        'case_ids': ['InitBoosterData-0', 'InitBoosterData-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
    'GenerateBoosterPack': {   'source_symbol': 'GenerateBoosterPack',
        'before': '\twBoosterPackID = a;',
        'after': '\twBoosterPackID = (uint8_t)(a + 1u);',
        'case_ids': ['GenerateBoosterPack-0', 'GenerateBoosterPack-1'],
        'source': 'src/profiles/extended/home/booster_packs.c'},
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
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
