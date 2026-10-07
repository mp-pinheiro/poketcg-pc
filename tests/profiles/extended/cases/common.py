"""Extended oracle-diff cases for common, seeded from tests/cases/common.py."""

CONTRACT = {
    'CountOppEnergyCardsInHand': {'compare': ('a', 'f', 'b'), 'preserve': ()},
    'ConvertHPToDamageCounters_Bank8': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CalculateWordTensDigit': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('a', 'b', 'c', 'd', 'e')},
    'PickTwoAttachedEnergyCards': {'compare': ('a', 'f', 'd'), 'preserve': ()},
    'ClearMemory_Bank8': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('a', 'f', 'b', 'c', 'd', 'e', 'hl')},
    'PickAttachedEnergyCardToRemove': {'compare': ('a', 'd'), 'preserve': ()},
    'CopyListWithFFTerminatorFromHLToDE_Bank8': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c')},
    'LookForCardIDInPlayArea_Bank8': {'compare': ('a', 'f', 'b', 'd', 'e'), 'preserve': ('d', 'e')},
    'CheckIfHasCardIDInHand': {'compare': ('a', 'f'), 'preserve': ()},
    'FindBasicEnergyCardsInLocation': {'compare': ('a', 'f', 'd', 'e', 'hl'), 'preserve': ()},
    'CalculateBDividedByA_Bank8': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CheckIfPlayerHasPokemonOtherThanMewtwoLv53': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'hl')},
    'RemoveFromListDifferentCardOfGivenType': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CountPokemonCardsInHandAndInPlayArea': {'compare': ('a',), 'preserve': (), 'wram_out': True},
    'LookForCardIDInLocation_Bank8': {'compare': ('a', 'f'), 'preserve': ()},
    'LookForCardIDInHandList_Bank8': {'compare': ('a', 'f', 'd'), 'preserve': ()},
    'LookForCardIDInHandAndPlayArea': {'compare': ('a', 'f'), 'preserve': ()},
    'LookForCardIDToTradeWithDifferentHandCard': {'compare': ('a', 'f', 'd'), 'preserve': ()},
    'LookForCardIDInDeck_GivenCardIDInHand': {'compare': ('a', 'f', 'd'), 'preserve': ()},
    'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea': {'compare': ('a', 'f', 'd'), 'preserve': ()},
    'AddStarterDeck': {'compare': (), 'preserve': ()},
    'FindDuplicatePokemonCards': {'compare': ('a', 'f', 'd'), 'preserve': (), 'wram_out': True},
    'AIPickEnergyCardToDiscard': {'compare': ('a', 'd'), 'preserve': ()},
    'HandleAIAntiMewtwoDeckStrategy': {'compare': ('a', 'f'), 'preserve': ()},
    'OpenBoosterPack': {'compare': (), 'preserve': (), 'wram_out': True},
    'AICheckIfAttackIsHighRecoil': {'compare': ('f', 'd'), 'preserve': ()},
    'ShowPromotionalCardScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    'CountOppEnergyCardsInHand': [
        {   'wram': {   0xC500: b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'wram': {   0xC500: b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0xFF,
            'wram': {   0xC500: b'\x01\x02\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC500: b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
    ],
    'ConvertHPToDamageCounters_Bank8': [
        {'a': 0x00},
        {'a': 0x01},
        {'a': 0x09},
        {'a': 0x0A},
        {'a': 0x0B},
        {'a': 0x64},
        {'a': 0xFF},
        {'a': 0x46, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'CalculateWordTensDigit': [
        {'hl': 0x00},
        {'hl': 0x01},
        {'hl': 0x09},
        {'hl': 0x0A},
        {'hl': 0x63},
        {'hl': 0x64},
        {'hl': 0x0100},
        {'hl': 0x7FFF},
        {'hl': 0xFFFF},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0xFA},
    ],
    'PickTwoAttachedEnergyCards': [
        {'a': 0x00, 'read': {0xCD78: 0x02, 0xCD3F: 0x02, 0xC500: 0x08}},
        {'a': 0x01, 'read': {0xCD78: 0x02, 0xCD3F: 0x02, 0xC500: 0x08}},
        {'a': 0x05, 'read': {0xCD78: 0x02, 0xCD3F: 0x02, 0xC500: 0x08}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xCD78: 0x02, 0xCD3F: 0x02, 0xC500: 0x08}},
        {   'a': 0x02,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xCD78: 0x02, 0xCD3F: 0x02, 0xC500: 0x08}},
    ],
    'ClearMemory_Bank8': [
        {   'a': 0x00,
            'hl': 0xC100,
            'wram': {   0xC100: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xC100: 0x0104}},
        {'a': 0x01, 'hl': 0xC200, 'wram': {0xC200: b'\xaa\xaa\xaa'}, 'read': {0xC200: 0x04}},
        {   'a': 0x05,
            'hl': 0xC300,
            'wram': {0xC300: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xC300: 0x08}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC400,
            'wram': {   0xC400: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xC400: 0x0104}},
        {   'a': 0x03,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC600,
            'wram': {0xC600: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xC600: 0x08}},
    ],
    'PickAttachedEnergyCardToRemove': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC200: 0x3C, 0xC500: 0x20}},
        {   'a': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC200: 0x3C, 0xC500: 0x20}},
        {   'a': 0x05,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC200: 0x3C, 0xC500: 0x20}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC200: 0x3C, 0xC500: 0x20}},
    ],
    'CopyListWithFFTerminatorFromHLToDE_Bank8': [
        {   'hl': 0xC100,
            'd': 0xC2,
            'e': 0x00,
            'wram': {0xC100: b'\xff'},
            'read': {0xC100: 0x01, 0xC200: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xC2,
            'e': 0x00,
            'hl': 0xC100,
            'wram': {0xC100: b'\x01\x02\xff'},
            'read': {0xC100: 0x03, 0xC200: 0x03}},
        {   'hl': 0xC1FF,
            'd': 0xC2,
            'e': 0xFF,
            'wram': {0xC1FF: b'\x01\xff'},
            'read': {0xC1FF: 0x02, 0xC2FF: 0x02}},
    ],
    'LookForCardIDInPlayArea_Bank8': [
        {'a': 0x00, 'b': 0x00, 'd': 0x00, 'e': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x00\x00'}},
        {'a': 0x01, 'b': 0x00, 'd': 0x00, 'e': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x01\x00'}},
        {'a': 0x08, 'b': 0x03, 'd': 0x00, 'e': 0x08, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x08\x00'}},
        {'a': 0x20, 'b': 0x05, 'd': 0x00, 'e': 0x20, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x20\x00'}},
        {'a': 0xFF, 'b': 0x00, 'd': 0x00, 'e': 0xFF, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\xff\x00'}},
        {'a': 0x08, 'f': 0xF0, 'b': 0x00, 'c': 0xCC, 'd': 0x00, 'e': 0x08, 'hl': 0x1234, 'wram': {0xFF97: b'\xc2', 0xC2BB: b'\x00', 0xC400: b'\x08\x00'}},
    ],
    'CheckIfHasCardIDInHand': [
        {'a': 0x01, 'd': 0x00, 'e': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00'}, 'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01'},
            'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x02',
                        0xC242: b'\x00',
                        0xC243: b'\x01',
                        0xC200: b'\x00',
                        0xC201: b'\x00',
                        0xC400: b'\x01\x01'},
            'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x02',
                        0xC242: b'\x00',
                        0xC243: b'\x01',
                        0xC200: b'\x00',
                        0xC201: b'\x00',
                        0xC400: b'\x01\x01'},
            'read': {0xC500: 0x20}},
    ],
    'FindBasicEnergyCardsInLocation': [
        {   'a': 0x02,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC27E: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC500: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x40}},
        {   'a': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC27E: b'\x01\x00\x06\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC500: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x03}},
        {   'a': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC27E: b'\x01\x00\x06\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xC500: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x03}},
    ],
    'CalculateBDividedByA_Bank8': [
        {   'a': 0x00,
            'b': 0x00,
            'oracle': False,
            'why': 'Divisor zero enters the assembly loop forever.',
            'expect_regs': {'a': 0x00, 'b': 0x00}},
        {'a': 0x01, 'b': 0x01},
        {'a': 0x01, 'b': 0xFF},
        {'a': 0x02, 'b': 0x05},
        {'a': 0xFF, 'b': 0xFF},
        {'a': 0x03, 'f': 0xF0, 'b': 0x0A, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'CheckIfPlayerHasPokemonOtherThanMewtwoLv53': [
        {'wram': {0xFF97: b'\xc3', 0xC400: b'\x08'}, 'read': {0xFF97: 0x01, 0xCC10: 0x01, 0xCC17: 0x01}},
        {   'wram': {   0xFF97: b'\xc3',
                        0xC400: b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'},
            'read': {0xFF97: 0x01, 0xCC10: 0x01, 0xCC17: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc3',
                        0xC400: b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'
                                b'\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d\x9d'},
            'read': {0xFF97: 0x01, 0xCC10: 0x01, 0xCC17: 0x01}},
    ],
    'RemoveFromListDifferentCardOfGivenType': [
        {'b': 0x11, 'c': 0x22, 'd': 0x00, 'e': 0xAA, 'hl': 0xC500, 'wram': {0xC500: b'\xff'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x00,
            'e': 0xAA,
            'hl': 0xC500,
            'wram': {0xC500: b'\xff'}},
        {   'b': 0x11,
            'c': 0x22,
            'd': 0x02,
            'e': 0xAA,
            'hl': 0xC500,
            'wram': {0xFF97: b'\xc2', 0xC400: b'\x01', 0xC500: b'\x00\xff'}},
    ],
    'CountPokemonCardsInHandAndInPlayArea': [
        {'c': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00', 0xC2EF: b'\x03'}, 'read': {0xCD78: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00', 0xC2EF: b'\x03'},
            'read': {0xCD78: 0x01}},
    ],
    'LookForCardIDInLocation_Bank8': [
        {   'a': 0x10,
            'e': 0x2A,
            'wram': {   0xC200: b'\x00',
                        0xC201: b'\x00',
                        0xC202: b'\x00',
                        0xC203: b'\x00',
                        0xC204: b'\x00',
                        0xC205: b'\x10',
                        0xC206: b'\x00',
                        0xC207: b'\x00',
                        0xC208: b'\x00',
                        0xC209: b'\x00',
                        0xC20A: b'\x00',
                        0xC20B: b'\x00',
                        0xC20C: b'\x00',
                        0xC20D: b'\x00',
                        0xC20E: b'\x00',
                        0xC20F: b'\x00',
                        0xC210: b'\x00',
                        0xC211: b'\x00',
                        0xC212: b'\x00',
                        0xC213: b'\x00',
                        0xC214: b'\x00',
                        0xC215: b'\x00',
                        0xC216: b'\x00',
                        0xC217: b'\x00',
                        0xC218: b'\x00',
                        0xC219: b'\x00',
                        0xC21A: b'\x00',
                        0xC21B: b'\x00',
                        0xC21C: b'\x00',
                        0xC21D: b'\x00',
                        0xC21E: b'\x00',
                        0xC21F: b'\x00',
                        0xC220: b'\x00',
                        0xC221: b'\x00',
                        0xC222: b'\x00',
                        0xC223: b'\x00',
                        0xC224: b'\x00',
                        0xC225: b'\x00',
                        0xC226: b'\x00',
                        0xC227: b'\x00',
                        0xC228: b'\x00',
                        0xC229: b'\x00',
                        0xC22A: b'\x00',
                        0xC22B: b'\x00',
                        0xC22C: b'\x00',
                        0xC22D: b'\x00',
                        0xC22E: b'\x00',
                        0xC22F: b'\x00',
                        0xC230: b'\x00',
                        0xC231: b'\x00',
                        0xC232: b'\x00',
                        0xC233: b'\x00',
                        0xC234: b'\x00',
                        0xC235: b'\x00',
                        0xC236: b'\x00',
                        0xC237: b'\x00',
                        0xC238: b'\x00',
                        0xC239: b'\x00',
                        0xC23A: b'\x00',
                        0xC23B: b'\x00',
                        0xFF97: b'\xc2',
                        0xC405: b'*'}},
        {   'a': 0x10,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xD7,
            'e': 0xBC,
            'hl': 0x1234,
            'wram': {   0xC200: b'\x00',
                        0xC201: b'\x00',
                        0xC202: b'\x00',
                        0xC203: b'\x00',
                        0xC204: b'\x00',
                        0xC205: b'\x10',
                        0xC206: b'\x00',
                        0xC207: b'\x00',
                        0xC208: b'\x00',
                        0xC209: b'\x00',
                        0xC20A: b'\x00',
                        0xC20B: b'\x00',
                        0xC20C: b'\x00',
                        0xC20D: b'\x00',
                        0xC20E: b'\x00',
                        0xC20F: b'\x00',
                        0xC210: b'\x00',
                        0xC211: b'\x00',
                        0xC212: b'\x00',
                        0xC213: b'\x00',
                        0xC214: b'\x00',
                        0xC215: b'\x00',
                        0xC216: b'\x00',
                        0xC217: b'\x00',
                        0xC218: b'\x00',
                        0xC219: b'\x00',
                        0xC21A: b'\x00',
                        0xC21B: b'\x00',
                        0xC21C: b'\x00',
                        0xC21D: b'\x00',
                        0xC21E: b'\x00',
                        0xC21F: b'\x00',
                        0xC220: b'\x00',
                        0xC221: b'\x00',
                        0xC222: b'\x00',
                        0xC223: b'\x00',
                        0xC224: b'\x00',
                        0xC225: b'\x00',
                        0xC226: b'\x00',
                        0xC227: b'\x00',
                        0xC228: b'\x00',
                        0xC229: b'\x00',
                        0xC22A: b'\x00',
                        0xC22B: b'\x00',
                        0xC22C: b'\x00',
                        0xC22D: b'\x00',
                        0xC22E: b'\x00',
                        0xC22F: b'\x00',
                        0xC230: b'\x00',
                        0xC231: b'\x00',
                        0xC232: b'\x00',
                        0xC233: b'\x00',
                        0xC234: b'\x00',
                        0xC235: b'\x00',
                        0xC236: b'\x00',
                        0xC237: b'\x00',
                        0xC238: b'\x00',
                        0xC239: b'\x00',
                        0xC23A: b'\x00',
                        0xC23B: b'\x00',
                        0xFF97: b'\xc2',
                        0xC405: b'*'}},
    ],
    'LookForCardIDInHandList_Bank8': [
        {'a': 0x01, 'd': 0x00, 'e': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00'}, 'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01\x00'},
            'read': {0xC500: 0x20}},
    ],
    'LookForCardIDInHandAndPlayArea': [
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01\x00',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
        {'a': 0x01, 'd': 0x00, 'e': 0x01, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00', 0xC2BB: b'\xff'}, 'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01\x00',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
    ],
    'LookForCardIDToTradeWithDifferentHandCard': [
        {   'a': 0x01,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01\x00'},
            'read': {0xC500: 0x20}},
        {'a': 0xAB, 'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0xAB, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00'}},
        {'a': 0x00, 'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00'}, 'read': {0xC500: 0x20}},
        {   'a': 0x00,
            'b': 0x00,
            'c': 0x02,
            'd': 0x00,
            'e': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x01',
                        0xC200: b'\x00',
                        0xC401: b'\x01'},
            'read': {0xC500: 0x20}},
        {   'a': 0x01,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x01,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x00',
                        0xC200: b'\x00',
                        0xC400: b'\x01'},
            'read': {0xC500: 0x20}},
    ],
    'LookForCardIDInDeck_GivenCardIDInHand': [
        {'a': 0xAB, 'b': 0x00, 'c': 0x01, 'd': 0x00, 'e': 0xAB, 'wram': {0xFF97: b'\xc2'}},
        {'a': 0x00, 'b': 0x00, 'c': 0xAB, 'd': 0x00, 'e': 0x00, 'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00'}, 'read': {0xC500: 0x20}},
        {   'a': 0x00,
            'd': 0x00,
            'e': 0x00,
            'b': 0x00,
            'c': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x03',
                        0xC200: b'\x00',
                        0xC403: b'\x01',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x01,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x03',
                        0xC200: b'\x00',
                        0xC403: b'\x01',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
    ],
    'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea': [
        {'a': 0xAB, 'b': 0x00, 'c': 0x01, 'd': 0x00, 'e': 0xAB, 'wram': {0xFF97: b'\xc2'}},
        {   'a': 0x00,
            'b': 0x00,
            'c': 0xAB,
            'd': 0x00,
            'e': 0x00,
            'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00', 0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
        {   'a': 0x00,
            'b': 0x00,
            'c': 0x01,
            'd': 0x00,
            'e': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x03',
                        0xC200: b'\x00',
                        0xC403: b'\x01',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x01,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x01',
                        0xC242: b'\x03',
                        0xC200: b'\x00',
                        0xC403: b'\x01',
                        0xC2BB: b'\xff'},
            'read': {0xC500: 0x20}},
    ],
    'AddStarterDeck': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xff',
                        0xC400: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;",
                        0xC478: b'<=>?@ABCDEFGHIJKLMNOPQRSTUVWXY'},
            'sram': {   0x00: {   0xA100: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80'}},
            'read': {0xFF97: 0x01},
            'sread': {0x00: {0xA100: 0x0100, 0xA300: 0x20}}},
        {   'a': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xff',
                        0xC400: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;",
                        0xC478: b'<=>?@ABCDEFGHIJKLMNOPQRSTUVWXY'},
            'sram': {   0x00: {   0xA100: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80'}},
            'read': {0xFF97: 0x01},
            'sread': {0x00: {0xA100: 0x0100, 0xA300: 0x20}}},
    ],
    'FindDuplicatePokemonCards': [
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2EE: b'\x02',
                        0xC242: b'\x05\x06',
                        0xC205: b'\x00',
                        0xC206: b'\x00',
                        0xC405: b'\t',
                        0xC406: b'\t'},
            'read': {0xCD78: 0x01, 0xC500: 0x03}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x01', 0xC242: b'\x05', 0xC205: b'\x00', 0xC405: b'\t'},
            'read': {0xCD78: 0x01, 0xC500: 0x02}},
    ],
    'AIPickEnergyCardToDiscard': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0x03,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC200: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xC500: 0x20}},
    ],
    'HandleAIAntiMewtwoDeckStrategy': [
        {   'wram': {0xCD2D: b'\x00'},
            'sram': {0x00: {}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'wram': {0xCD2D: b'\x00'},
            'sram': {0x00: {}},
            'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'OpenBoosterPack': [
        {   'wram': {   0xC200: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xC400: b'\x00',
                        0xCABB: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x02],
            'read': {0xFF97: 0x01, 0xC200: 0x3C, 0xC500: 0x01, 0xCB84: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC200: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xC400: b'\x00',
                        0xCABB: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x02],
            'read': {0xFF97: 0x01, 0xC200: 0x3C, 0xC500: 0x01, 0xCB84: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'AICheckIfAttackIsHighRecoil': [
        {   'wram': {   0xCD2D: b'\x80',
                        0xCD60: b'\x00',
                        0xCD44: b'\x10',
                        0xCD6A: b'\x00',
                        0xCD45: b'\x01\x02\x03\x04\x05\x06',
                        0xCD64: b'\x00\x00\x00\x00\x00\x00'},
            'expect': {0xCD60: b'\x01'},
            'expect_regs': {'f': 0x00},
            'read': {0xCD60: 0x01}},
        {   'wram': {   0xCD2D: b'\x80',
                        0xCD60: b'\xff',
                        0xCD44: b'\x7f',
                        0xCD6A: b'\x00',
                        0xCD45: b' 0@P`p',
                        0xCD64: b'\xaa\xbb\xcc\xdd\xee\xff'},
            'expect': {0xCD60: b'\x01'},
            'expect_regs': {'f': 0x00},
            'read': {0xCD60: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD2D: b'\x80',
                        0xCD60: b'\xaa',
                        0xCD44: b'\xbb',
                        0xCD6A: b'\xcc',
                        0xCD45: b'\x01#Eg\x89\xab',
                        0xCD64: b'\xde\xad\xbe\xef\x10 '},
            'expect': {0xCD60: b'\x01'},
            'expect_regs': {'f': 0x00},
            'read': {0xCD60: 0x01}},
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
                                b'\x02\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00\x00\x00\x01'
                                b'\x02\x00\x10\x00\x00\x01\x00\x00\x00\x10\x01\x00\x00\x01\x01\x01'
                                b'\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00\x00\x08\x01\x00\x00\x00'
                                b'\x00\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f+(\x0b'
                                b'\x00\x00\x1a8\x15\t\x1e\x1d,\x1f\x0f\x0f\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10&'
                                b'\x00\x011\x01&\x1f+(\x0b8\x12\x15\t\x1e\x1d,\x0f\x1c\x0e7'
                                b'/\x11\x08\x05\x17\x13\x04\n.\x1b9\x185\r!6\x062\'0\x07#4"\x16;\x03)'
                                b':\x02-3%*\x0c$ \x14\x13\x19\xff\xff\xff\xff\xff\xff\x80\x80'
                                b'\x80\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x05\t\x01\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10'
                                b'\x02\x11\x10\x00\x00\x00\x11\x01\x00\x00\x00\x00\x10\x01\x00\x02'
                                b'\x00\x00\x11\x01\x00\x10\x13\x00\x00\x02\x00\x00\x12\x00\x00\x00'
                                b'\x01\x00\x00\x02\x02\x00\x00\x00\x00\x01\x01\x02\x00\x02\x08\x00'
                                b"\x00\x01\x00\x00\x00\x00\x00\x002\x10\x02'\x00\x00$\x17-\x0b.5"
                                b'\x11\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x001/\x04\x13\x1d('2\x10\x02'\x03 \x19\x061/:"
                                b'\x1a-(\x0b.5\x11&\x12"\x1c3\x1e!\t\x0e\x00;\x18\x0f\x01+809:6)'
                                b'%\x15\x1b\r,*\x14\x07\x08\x0c4\x1f7#\x19\x19\x16 \x1a\xff'
                                b'\xff\xff\x80\x80\x80\x80\x00\x002(\x1e(\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x07\x07\x04'
                                b'\x00\xa5\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x115.\x0b-\x17$\xff8\x1a\xff$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x16\x16\x16'
                                b'\x16\x16\x00\x00\x00\x00\x00\x006\x00                              '
                                b'                     \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006VGLR HPC1.MI TN HR '
                                b"EOA 4.RA021SDW '.R8YGCNSYRFDAAEEEI A LTKIK.!N)SILADEOFGMO HA IC MBI("
                                b'TWEIGOI0RL  N CN\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00LGTIGCU 1LIIEKC E RRLMHE TDSNRHEVETR1 V'EAH0LU1GRTAU"
                                b'AA NKCD B UM. APPCNHISDBPT RTIAEO5GERKS0A TD OJNNDF\x03GLYTNG M'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x0001234569nH\x8d\x81\x84h\x9fNvb\x80\x98M:\x9ddK\x97m\x95fBE'
                                b'\x93\x82\x7f\x8a=YqQcJL\x88;\x90DGkSCz|uyot^O\x8e\x83<>e\x94g\x9b}'
                                b'\x8bj]aI\x8f\x99A\x9arT@_\x9c\x8cZwP\x96Rlx[V~X\x86\x9eW?8i'
                                b'\x89\x91\x85\\\x00{`\x87\x92FUs\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x0012345678\x928F\\mTn\x91\x7f{Nb^O\x9d_'
                                b':xYIZE@j\x85W\x87a~\x9e\x8b\x90\x8dU\x83\x8a\x97vi\x80\x9awBXHoMq'
                                b'>\x93u`\x88K9g\x00V}\x9fheA\x84\x89fc\x99ds\x8cRC<Ql=\x96\x8e\x9b'
                                b'[\x94St\x82;ky]\x95\x9cPpL\x86JDz|r\x81G\x8f?\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x03 \x00\x00\x1c '
                                b'\x00\x00\x1e \x00\x00\x1c@\x00\x00\x1d@\x00\x00\x1c`\x00\x00\x1e '
                                b'\x00\x00\x1c@\x00\x00\x1d@\x00\x00\x1c`\x00\x00\x01@\x00\x00\x02@'
                                b'\x00\x00\x03@\x00\x00\xc0\x01\x00\x00\xc2\x01\x00\x00\xc4\x01'
                                b'\x00\x00\xc6\x01\x00\x00\xc8\x01\x00\x00\xca\x01\x00\x00\xcc\x01'
                                b'\x00\x00\xce\x01\x00\x00\x04\x00\x00\x00\x14\x00\x00\x00$\x00'
                                b'\x00\x00\x05\x00\x00\x00\x15\x00\x00\x00%\x00\x00\x005\x00'
                                b'\x00\x004\x00\x00\x00(\x00\x00\x00&\x00\x00\x00\x16\x00'
                                b"\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x17\x00\x00\x00'\x00"
                                b'\x00\x00)\x00\x06Jennifer\x00\x030\x00\x00\x00\x00\x00\x00\x00\x11'
                                b'\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xe6\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x1d\x01A\x01$&\x16\x01\x00q\xb5-\xc3\x00\x00\xc3H\x03\x00\x00'
                                b'\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9c'
                                b'c\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb'
                                b'\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xbf\x02\x00\x02\x00\x00\xffW\xbf"\x1a'
                                b'\x01\x04\x00\x10R\x9cc\x8cQ\x00\x00\xff\x7f_3\x9f\x00\x04\x00\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00'
                                b'\x00\x11\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x03\x01\x00\x00\x00\x00\x00\x03'
                                b'\x00\x00\x01\x00\x00\x08\x02\x00\x00\xaa\x00\xa7\x00\x01\x00\x00'
                                b'\x00\x00\x00\x00\xe8\xdf\x00\x02\x02\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x07\x00\x0e'
                                b';S\x00\x00\xc3\x10\x00\x04\xa5\x00\x00\x00\xa5%\xff\x00\x190\x00#'
                                b'&\xc0\x03\x04%\x02\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00'
                                b'\xe5\x11\xd3\x08\x00\x0002\x00\x00\x00\x00\x00\x00\x10\x83'
                                b'\x08\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00&\x10\x00'
                                b'\x00\x10\xd4\x08\xd5\x08\x00\x00\x1e\x00\xf6I\x00\x08\x00\x03'
                                b'\x0e\x01\x10\x00\xd6\x08\x04\x00\n\x02\x00\xbe\x00\xd7\x08\x15'
                                b'\x00\xe5\x11\xd3\x08\x00\x0002\x00\x00\x00\x00\x00\x00\x10'
                                b'\x83\x08\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00&\x10'
                                b'\x00\x00\x10\xd4\x08\xd5\x08\x00\x00\x1e\x00\xf6I\x00\x08\x00'
                                b'\x03\x0e\x01\x10\x00\xd6\x08\x04\x00\n\x02\x00\xbe\x00\xd7\x08'
                                b'\x15\x10\x00\x00\x10\xd4\x08\xd5\x08\x00\x00\x1e\x00\xf6I\x00'
                                b'\x08\x00\x03\x0e\x1e\x00\n\n\x00\x00\x00\x00\x0000`\x00\x01\x00\x00'
                                b'\x00\x00\x00\x00\x00\xc2\xf0\x03\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x05\x02\x00\x01\x00!\x00\x00\x00\x00\x04\x00\x00\xc6\xc6\xa8'
                                b'\xa8\xa8\xa8\xae\xae\xa2\xa2\xa2\xa2\xcc\xcc\x9fp\x88\x80\x00'
                                b'\x00\x01\x00\n\x01\x00',
                        0xCCBE: b'\x00\x12\x11\x01\x01/\x1d\x00\x00\x03\x04\n\x0e\x19W\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00 \x01\x00\xa5\x01'
                                b'\x00\x00\x00\x00\x00\xff\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x016\x08\x00\x00\x00\x80P>2>\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x10\x00\x03\x02'
                                b'\x04\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x01\x01$'
                                b'\x01\x00\x00\x00\x00y\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x0e\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x005\xdd\x07\x17\t\x00\x00\x00\x00\x00\x00\x00\x0b\xff'
                                b'\x7f\xbf\x02\x00\x02\x00\x00\x0f\x01\rYo\x0f\x01\r\xa9'
                                b'\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83\x08\x02'
                                b'\x00\x00\x00\x02\x00\x00\x00\x00\xc0\x03\x00\x00\xc3\xc2\x01['
                                b'K\xcf\x01\x00\x00\x00\xa2\xff\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x01\n\x00\x00\x80\xc2"
                                b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x115.\x0b-\x17$\xff\xff\xff+$5\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x115.\x0b-\x17$\xff\xff\xff+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xD001: b'\x00\xc5^g\x0c\t\x06\x0c\x01\x02\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00@\x010`\x00\x00\x00\x0f\x0e\x14\x00\x01'
                                b'\x01\x00\x01\x01#\x02\x08d\xc0\x03\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x0c\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81\x82'
                                b'\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06'
                                b'\x06c\x05\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x80\x80\x80\x80\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x80\x00\x00\x00@\x00\x00\x00\x00\x80\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00@\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x06\x0c0`\x08\x0eS\x00\x00\x00!*\xff\x00\x00R\x9c'
                                b'c\x8cQ\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)m\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x10\x00\x00\x00'
                                b'\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\x00ZJ#\x04\xff\xff\xff\xff\xff\xff\x01\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x0f\x0e\x14p\xa0'
                                b'\x00\x00\x00\x1e\x00\x01\x04\x028\x04\x02]f\x00\x00\xaa'
                                b'\x00\x00\x01\xf0\x00\x04#\x01\x0e\x12\x02\x00\x0e\x02\x00\x00'
                                b'\x00\x00$\x02\x06\n\x02\x00\x1e\x02\x00\x00\x00\x00%\x03'
                                b'\x16\x0c\x00\x00\x1e\x00\x00\x00\x00\x00&\x04\x0c\x04\x00\x00'
                                b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x12\x06\x02\x02\x00\x16\x00\t'
                                b'\x00\x00\x00\x00\x00\xc0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00s\x03\x01\x00\x00\x00\x06\x00.\xe2\x00\x00\xf0\x00\x10'
                                b'\x00\x10\x00\x00\x10\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00'
                                b'\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00p\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x1e'
                                b'd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00W\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\x8c\x96\x00\xc2\x00\x14\x00\x01\x06'
                                b'\x01\x00\xc2\x00\x14\x00\x01\x06!\x00\xc3\x00\x14\x00\x01\x06'
                                b'\x07\x00\xc3\x00\x14\x00\x01\x06a\x00\xc3\x00\x14\x00\x01\x06'
                                b'\x97\x00\xc3\x00\x14\x00\x01\x06\x8c\x00\xc3\x00\n\x00\x00\x06'
                                b'\x98\x00\xc3\x00\n\x00\x00\x06\x98\x02\xc2\x00\x14\x00\x00\x06'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3\x00\n\x00\x00'
                                b'\x00PO\x03\x12\xbcL\x00aM\x01W\xff\x00\x00\x80\xbat,\x10\x05\x00*\x00'
                                b'\x00\x00\x00\x10\x00\x00XX\x00\xa5,\xbat\xd9t,\xe2s\xff\x00'
                                b'\x00\x00\x88 !O*\xe1hdi*\x82i\xff\x00\x00\x00\x08\x00( *\xe9U\xf4U*'
                                b'\x96U\x07\x00\x00\x00\x88\x10(\x1e*\x05U\x10U*AU\x10\x00\x00\x008\xd0'
                                b'<\x16*\xf1R\xfcR*-S\x06\x00\x00\x00\x88`(\x11*\xd8Q\xdfQ*'
                                b'\x90Q\x07\x00\x00\x00(`(\x0f*\xb2Q\xbdQ*LQ\x01\x00\x00\x00\x08\xd0'
                                b'(\x10*\xc1Q\xd4Q*nQ\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00XX\x00\x00\x00,\x00\x01c\x00\x05'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
                                b'\x08\x10&\x003{\x00\x00\x00\x00\x00\x00\x02\x01\x02\x03'
                                b'\x04\x05\x06\x07\x00\xe1U\x06\x00m\x00\x00\x0e\x04\x02\x02'
                                b'l\x03\xff\x01\x02\x02\x01\x0f\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00'
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
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00',
                        0xDCEE: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xFF80: b'\x08\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x00\x00\x00\x00\n\xc3\x11\x14\xc5\xc3\x00\x01\x07\x19\x12\x00'
                                b'\xff\xff\x00\x00\x00\x00\x9fp\xcc\x99\x0b\x01\x13\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFCE,
            'rom_bank': 0x08,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x80,
            'b': 0x01,
            'c': 0x60,
            'd': 0x00,
            'e': 0x63,
            'f': 0x00,
            'hl': 0xC3BB},
    ],
    'ShowPromotionalCardScreen': [
        {   'oracle': False,
            'why': 'Extended promotional screen waits for song and input completion outside the isolated oracle.',
            'expect': {0xCBD2: b'\x02', 0xFF97: b'\x01', 0xCCB2: b'\x01', 0xCCB4: b'\x02', 0xFFA8: b'\x01'}},
        {   'oracle': False,
            'why': 'Extended promotional screen waits for song and input completion outside the isolated oracle.',
            'expect': {0xCBD2: b'\x02', 0xFF97: b'\x01', 0xCCB2: b'\x01', 0xCCB4: b'\x02', 0xFFA8: b'\x01'}},
    ],
}

MUTATIONS = {
    'CountOppEnergyCardsInHand': {   'source_symbol': 'CountOppEnergyCardsInHand',
        'before': '\tif (r.f & F_C)',
        'after': '\tif (r.f & 0x20u)',
        'case_ids': [   'CountOppEnergyCardsInHand-0',
                        'CountOppEnergyCardsInHand-1',
                        'CountOppEnergyCardsInHand-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'ConvertHPToDamageCounters_Bank8': {   'source_symbol': 'ConvertHPToDamageCounters_Bank8',
        'before': '\treturn (uint8_t)(a / 10u);',
        'after': '\treturn (uint8_t)(a / 5u);',
        'case_ids': [   'ConvertHPToDamageCounters_Bank8-3',
                        'ConvertHPToDamageCounters_Bank8-5',
                        'ConvertHPToDamageCounters_Bank8-6'],
        'source': 'src/profiles/extended/home/common.c'},
    'CalculateWordTensDigit': {   'source_symbol': 'CalculateWordTensDigit',
        'before': '\treturn (uint16_t)(hl / 10u);',
        'after': '\treturn (uint16_t)(hl / 100u);',
        'case_ids': [   'CalculateWordTensDigit-3',
                        'CalculateWordTensDigit-4',
                        'CalculateWordTensDigit-8'],
        'source': 'src/profiles/extended/home/common.c'},
    'PickTwoAttachedEnergyCards': {   'source_symbol': 'PickTwoAttachedEnergyCards',
        'before': '\t\treturn (PickTwoResult){0xffu, 0u, 0u, pick_two_cp_flags(attached, 2u), d};',
        'after': '\t\treturn (PickTwoResult){0xfeu, 0u, 0u, pick_two_cp_flags(attached, 2u), d};',
        'case_ids': [   'PickTwoAttachedEnergyCards-0',
                        'PickTwoAttachedEnergyCards-1',
                        'PickTwoAttachedEnergyCards-2',
                        'PickTwoAttachedEnergyCards-3',
                        'PickTwoAttachedEnergyCards-4'],
        'source': 'src/profiles/extended/home/common.c'},
    'ClearMemory_Bank8': {   'source_symbol': 'ClearMemory_Bank8',
        'before': '\tuint32_t n = a ? (uint32_t)a : 0x100u;',
        'after': '\tuint32_t n = (uint32_t)a;',
        'case_ids': ['ClearMemory_Bank8-0', 'ClearMemory_Bank8-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'PickAttachedEnergyCardToRemove': {   'source_symbol': 'PickAttachedEnergyCardToRemove',
        'before': '\t\treturn (PickEnergyResult){0xffu, d};',
        'after': '\t\treturn (PickEnergyResult){0xfeu, d};',
        'case_ids': [   'PickAttachedEnergyCardToRemove-0',
                        'PickAttachedEnergyCardToRemove-1',
                        'PickAttachedEnergyCardToRemove-2',
                        'PickAttachedEnergyCardToRemove-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'CopyListWithFFTerminatorFromHLToDE_Bank8': {   'source_symbol': 'CopyListWithFFTerminatorFromHLToDE_Bank8',
        'before': '\t\tif (a == 0xFFu)',
        'after': '\t\tif (a == 0xFEu)',
        'case_ids': [   'CopyListWithFFTerminatorFromHLToDE_Bank8-0',
                        'CopyListWithFFTerminatorFromHLToDE_Bank8-1',
                        'CopyListWithFFTerminatorFromHLToDE_Bank8-2'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInPlayArea_Bank8': {   'source_symbol': 'LookForCardIDInPlayArea_Bank8',
        'before': '\t\tif (card_id == de)',
        'after': '\t\tif (card_id != de)',
        'case_ids': [   'LookForCardIDInPlayArea_Bank8-0',
                        'LookForCardIDInPlayArea_Bank8-1',
                        'LookForCardIDInPlayArea_Bank8-2',
                        'LookForCardIDInPlayArea_Bank8-3',
                        'LookForCardIDInPlayArea_Bank8-4',
                        'LookForCardIDInPlayArea_Bank8-5'],
        'source': 'src/profiles/extended/home/common.c'},
    'CheckIfHasCardIDInHand': {   'source_symbol': 'CheckIfHasCardIDInHand',
        'before': '\t\tif (count != 0u)',
        'after': '\t\tif (count == 0u)',
        'case_ids': ['CheckIfHasCardIDInHand-2', 'CheckIfHasCardIDInHand-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'FindBasicEnergyCardsInLocation': {   'source_symbol': 'FindBasicEnergyCardsInLocation',
        'before': '\t\tgb_write8(hl++, e);',
        'after': '\t\tgb_write8(hl++, (uint8_t)(e + 1u));',
        'case_ids': ['FindBasicEnergyCardsInLocation-1', 'FindBasicEnergyCardsInLocation-2'],
        'source': 'src/profiles/extended/home/common.c'},
    'CalculateBDividedByA_Bank8': {   'source_symbol': 'CalculateBDividedByA_Bank8',
        'before': '\t\tuint8_t result = (uint8_t)(remainder - divisor);',
        'after': '\t\tuint8_t result = (uint8_t)(remainder + divisor);',
        'case_ids': [   'CalculateBDividedByA_Bank8-1',
                        'CalculateBDividedByA_Bank8-2',
                        'CalculateBDividedByA_Bank8-3',
                        'CalculateBDividedByA_Bank8-4',
                        'CalculateBDividedByA_Bank8-5'],
        'source': 'src/profiles/extended/home/common.c'},
    'CheckIfPlayerHasPokemonOtherThanMewtwoLv53': {   'source_symbol': 'CheckIfPlayerHasPokemonOtherThanMewtwoLv53',
        'before': 'if (card_id != MEWTWO_LV53) {',
        'after': 'if (card_id == MEWTWO_LV53) {',
        'case_ids': [   'CheckIfPlayerHasPokemonOtherThanMewtwoLv53-0',
                        'CheckIfPlayerHasPokemonOtherThanMewtwoLv53-2'],
        'source': 'src/profiles/extended/home/common.c'},
    'RemoveFromListDifferentCardOfGivenType': {   'source_symbol': 'RemoveFromListDifferentCardOfGivenType',
        'before': 'matches = (d == 0x02u);',
        'after': 'matches = (d == 0x03u);',
        'case_ids': ['RemoveFromListDifferentCardOfGivenType-2'],
        'source': 'src/profiles/extended/home/common.c'},
    'CountPokemonCardsInHandAndInPlayArea': {   'source_symbol': 'CountPokemonCardsInHandAndInPlayArea',
        'before': 'GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;',
        'after': 'GetTurnDuelistVariable((uint8_t)(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA + '
                 '1u)).a;',
        'case_ids': [   'CountPokemonCardsInHandAndInPlayArea-0',
                        'CountPokemonCardsInHandAndInPlayArea-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInLocation_Bank8': {   'source_symbol': 'LookForCardIDInLocation_Bank8',
        'before': 'if (loc != location)',
        'after': 'if (loc == location)',
        'case_ids': ['LookForCardIDInLocation_Bank8-0'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInHandList_Bank8': {   'source_symbol': 'LookForCardIDInHandList_Bank8',
        'before': '\t\t\treturn (LookForCardIDInHandListResult){0xFFu, 0xC0u, d};',
        'after': '\t\t\treturn (LookForCardIDInHandListResult){0xFFu, 0x90u, d};',
        'case_ids': ['LookForCardIDInHandList_Bank8-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInHandAndPlayArea': {   'source_symbol': 'LookForCardIDInHandAndPlayArea',
        'before': '\tif (r1.f & 0x10u)',
        'after': '\tif (r1.f & 0x20u)',
        'case_ids': ['LookForCardIDInHandAndPlayArea-0'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDToTradeWithDifferentHandCard': {   'source_symbol': 'LookForCardIDToTradeWithDifferentHandCard',
        'before': '\tLookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, de);',
        'after': '\tLookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, (CardId)(de + 1u));',
        'case_ids': ['LookForCardIDToTradeWithDifferentHandCard-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInDeck_GivenCardIDInHand': {   'source_symbol': 'LookForCardIDInDeck_GivenCardIDInHand',
        'before': '\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);',
        'after': '\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x00u);',
        'case_ids': ['LookForCardIDInDeck_GivenCardIDInHand-2'],
        'source': 'src/profiles/extended/home/common.c'},
    'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea': {   'source_symbol': 'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea',
        'before': '\tif (!(r1.f & 0x10u))\n'
                  '\t\treturn (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r1.a, r1.f, 0u};',
        'after': '\tif (r1.f & 0x10u)\n'
                 '\t\treturn (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r1.a, r1.f, 0u};',
        'case_ids': ['LookForCardIDInDeck_GivenCardIDInHandAndPlayArea-0',
                     'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea-1',
                     'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea-2',
                     'LookForCardIDInDeck_GivenCardIDInHandAndPlayArea-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'AddStarterDeck': {   'source_symbol': 'AddStarterDeck',
        'before': '\t_AddStarterDeck(a);',
        'after': '\t_AddStarterDeck((uint8_t)(a + 1u));',
        'case_ids': ['AddStarterDeck-0', 'AddStarterDeck-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'FindDuplicatePokemonCards': {   'source_symbol': 'FindDuplicatePokemonCards',
        'before': 'wTempAI = inner_idx;',
        'after': 'wTempAI = outer_idx;',
        'case_ids': ['FindDuplicatePokemonCards-0'],
        'source': 'src/profiles/extended/home/common.c'},
    'AIPickEnergyCardToDiscard': {   'source_symbol': 'AIPickEnergyCardToDiscard',
        'before': 'if (total == 0u)\n\t\treturn (PickEnergyResult){0xFFu, d};',
        'after': 'if (total == 0u)\n\t\treturn (PickEnergyResult){0xFEu, d};',
        'case_ids': ['AIPickEnergyCardToDiscard-0', 'AIPickEnergyCardToDiscard-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'HandleAIAntiMewtwoDeckStrategy': {   'source_symbol': 'HandleAIAntiMewtwoDeckStrategy',
        'before': '\tf = (uint8_t)((f & 0x80u) | 0x10u);\n'
                  '\treturn (HandleAIAntiMewtwoDeckStrategyResult){a, f};',
        'after': '\tf = (uint8_t)((f & 0x80u) | 0x00u);\n'
                 '\treturn (HandleAIAntiMewtwoDeckStrategyResult){a, f};',
        'case_ids': ['HandleAIAntiMewtwoDeckStrategy-0', 'HandleAIAntiMewtwoDeckStrategy-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'OpenBoosterPack': {   'source_symbol': 'OpenBoosterPack',
        'before': 'void OpenBoosterPack(void)\n{\n\t_OpenBoosterPack();',
        'after': 'void OpenBoosterPack(void)\n{\n\t(void)0;',
        'case_ids': ['OpenBoosterPack-0', 'OpenBoosterPack-1'],
        'source': 'src/profiles/extended/home/common.c'},
    'AICheckIfAttackIsHighRecoil': {   'source_symbol': 'AICheckIfAttackIsHighRecoil',
        'before': '\t\t(uint8_t)((flag.f & 0x80u) | ((flag.f & 0x10u) ^ 0x10u)), d};',
        'after': '\t\t(uint8_t)(flag.f ^ 0x10u), d};',
        'case_ids': ['AICheckIfAttackIsHighRecoil-3'],
        'source': 'src/profiles/extended/home/common.c'},
    'ShowPromotionalCardScreen': {   'source_symbol': 'ShowPromotionalCardScreen',
        'before': 'void ShowPromotionalCardScreen(CardId de)\n{\n\t_ShowPromotionalCardScreen(de);',
        'after': 'void ShowPromotionalCardScreen(CardId de)\n'
                 '{\n'
                 '\t_ShowPromotionalCardScreen((CardId)(de + 1u));',
        'case_ids': ['ShowPromotionalCardScreen-0', 'ShowPromotionalCardScreen-1'],
        'source': 'src/profiles/extended/home/common.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
