"""Extended oracle-diff cases for npc_data: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('npc_data', remove=('_GetNPCDuelConfigurations',))
OWN = (
    'LoadNPCSpriteData',
)
CONTRACT.update({
    'LoadNPCSpriteData': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
})
CASES.update({
    'LoadNPCSpriteData': [
        {   'a': 0x00,
            'wram': {sym("wConsole"): b'\x00'},
            'read': {sym("wTempNPC"): 0x01, sym("wNPCSpriteID"): 0x01, sym("wNPCAnim"): 0x01, sym("wNPCAnimFlags"): 0x01}},
        {   'a': 0x01,
            'b': 0x12,
            'c': 0x34,
            'd': 0x56,
            'e': 0x78,
            'hl': 0x2468,
            'wram': {sym("wConsole"): b'\x02'},
            'read': {sym("wTempNPC"): 0x01, sym("wNPCSpriteID"): 0x01, sym("wNPCAnim"): 0x01, sym("wNPCAnimFlags"): 0x01}},
        {   'a': 0x08,
            'b': 0xA6,
            'c': 0xAA,
            'd': 0x3C,
            'e': 0xC3,
            'hl': 0x9ABC,
            'wram': {sym("wConsole"): b'\x01'},
            'read': {sym("wTempNPC"): 0x01, sym("wNPCSpriteID"): 0x01, sym("wNPCAnim"): 0x01, sym("wNPCAnimFlags"): 0x01}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wConsole"): b'\x02'},
            'read': {sym("wTempNPC"): 0x01, sym("wNPCSpriteID"): 0x01, sym("wNPCAnim"): 0x01, sym("wNPCAnimFlags"): 0x01}},
    ],
})
MUTATIONS.update({
    'LoadNPCSpriteData': {   'source_symbol': 'LoadNPCSpriteData',
        'before': '\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, header.hl);',
        'after': '\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, (uint16_t)(header.hl + 1u));',
        'case_ids': [   'LoadNPCSpriteData-0',
                        'LoadNPCSpriteData-1',
                        'LoadNPCSpriteData-2',
                        'LoadNPCSpriteData-3'],
        'source': 'src/profiles/extended/home/npc_data.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
