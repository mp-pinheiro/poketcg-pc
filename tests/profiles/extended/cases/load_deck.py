"""Extended oracle-diff cases for load_deck: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('load_deck')
OWN = (
    'CompressDeckToSRAM',
    'DecompressSRAMDeck',
)
DECK_ENTRIES = bytes(sum(([index & 0xFF, 1 if index % 3 == 0 else 0] for index in range(1, 61)), []))
COMPRESSED = bytes([0x92, 1, 2, 3, 4, 5, 6, 7, 8, 0x49, 9, 10, 11, 12, 13, 14, 15, 16,
                    0x24, 17, 18, 19, 20, 21, 22, 23, 24, 0x92, 25, 26, 27, 28, 29, 30, 31, 32,
                    0x49, 33, 34, 35, 36, 37, 38, 39, 40, 0x24, 41, 42, 43, 44, 45, 46, 47, 48,
                    0x92, 49, 50, 51, 52, 53, 54, 55, 56, 0x40, 57, 58, 59, 60])
CONTRACT['CompressDeckToSRAM'] = {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')}
CASES['CompressDeckToSRAM'] = [
    {'d': 0xC1, 'e': 0x00, 'hl': sym("wDuelTempList"), 'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(120)}, 'read': {sym("wDuelTempList"): 68}},
    {'d': 0xC1, 'e': 0x00, 'hl': sym("wDuelTempList"), 'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: DECK_ENTRIES}, 'read': {sym("wDuelTempList"): 68}},
    {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xC1, 'e': 0x00, 'hl': sym("wDuelTempList"),
     'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes([0xFF, 0x01] * 60)}, 'read': {sym("wDuelTempList"): 68}},
]
CONTRACT['DecompressSRAMDeck'] = {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')}
CASES['DecompressSRAMDeck'] = [
    {'d': 0xC5, 'e': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'wram': {sym("wDuelTempList"): bytes(68)}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 120, sym("wDecompSavedDeckCount"): 1}},
    {'d': 0xC5, 'e': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'wram': {sym("wDuelTempList"): COMPRESSED}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 120, sym("wDecompSavedDeckCount"): 1}},
    {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xC5, 'e': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11,
     'wram': {sym("wDuelTempList"): bytes([0xFF] * 68)}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 120, sym("wDecompSavedDeckCount"): 1}},
]
MUTATIONS.update({
    'CompressDeckToSRAM': {'source_symbol': 'CompressDeckToSRAM',
        'before': 'gb_write8(destination++, (uint8_t)(command << 4));',
        'after': 'gb_write8(destination++, command);',
        'case_ids': ['CompressDeckToSRAM-1', 'CompressDeckToSRAM-2'],
        'source': 'src/profiles/extended/home/load_deck.c'},
    'DecompressSRAMDeck': {'source_symbol': 'DecompressSRAMDeck',
        'before': 'gb_write8(destination++, (uint8_t)(command >> 7));',
        'after': 'gb_write8(destination++, (uint8_t)(command & 0x01u));',
        'case_ids': ['DecompressSRAMDeck-1', 'DecompressSRAMDeck-2'],
        'source': 'src/profiles/extended/home/load_deck.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
