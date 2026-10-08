"""Extended oracle-diff cases for scenes: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('scenes', remove=(
    'LoadScene_LoadCompressedSGBPacket',
    'LoadScene_LoadSGBPacket',
    'LoadScene_SetCardPopAttrBlk',
    'LoadScene_SetGameBoyPrinterAttrBlk',
    '_DrawPortrait',
    '_LoadScene',
))
OWN = (
    '_LoadScene',
)
CONTRACT.update({
    '_LoadScene': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    '_LoadScene': [
        {   'a': 0x00,
            'b': 0x00,
            'c': 0x00,
            'wram': {sym("wConsole"): b'\x00', sym("wAllSpriteAnimationsDisabled"): b'\x00', sym("wCurTilemap"): b'\x00', sym("wd291"): b'\x00'},
            'sram': {0x00: {}},
            'read': {   sym("wSceneBaseX"): 0x01,
                        sym("wSceneBaseY"): 0x01,
                        sym("wd61f") + 1: 0x02,
                        sym("wHasSaveData"): 0x02,
                        sym("wBGP"): 0x01,
                        sym("wd291"): 0x01,
                        sym("wCurTilemap"): 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x00,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wConsole"): b'\x00', sym("wAllSpriteAnimationsDisabled"): b'\x00', sym("wCurTilemap"): b'w', sym("wd291"): b'"'},
            'sram': {0x00: {}},
            'read': {   sym("wSceneBaseX"): 0x01,
                        sym("wSceneBaseY"): 0x01,
                        sym("wd61f") + 1: 0x02,
                        sym("wHasSaveData"): 0x02,
                        sym("wBGP"): 0x01,
                        sym("wd291"): 0x01,
                        sym("wCurTilemap"): 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
        {   'a': 0x13,
            'b': 0x02,
            'c': 0x03,
            'wram': {sym("wConsole"): b'\x02', sym("wAllSpriteAnimationsDisabled"): b'\x00', sym("wCurTilemap"): b'\x00', sym("wd291"): b'\x00'},
            'sram': {0x00: {}},
            'read': {   sym("wSceneBaseX"): 0x01,
                        sym("wSceneBaseY"): 0x01,
                        sym("wd61f") + 1: 0x02,
                        sym("wHasSaveData"): 0x02,
                        sym("wBGP"): 0x01,
                        sym("wd291"): 0x01,
                        sym("wCurTilemap"): 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
    ],
})
MUTATIONS.update({
    '_LoadScene': {   'source_symbol': '_LoadScene',
        'before': '\twCurTilemap = saved_tilemap;',
        'after': '\twCurTilemap = 0u;',
        'case_ids': ['_LoadScene-0', '_LoadScene-1'],
        'source': 'src/profiles/extended/home/scenes.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
