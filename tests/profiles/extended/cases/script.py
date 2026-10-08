"""Extended oracle-diff cases for script: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('script', remove=(
    'Func_3b11',
    'GetNPCDuelConfigurations',
))
OWN = (
    'RunOverworldScript',
)
CONTRACT.update({
    'RunOverworldScript': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
})
CASES.update({
    'RunOverworldScript': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x44,
            'e': 0x55,
            'hl': 0x4567,
            'rom_bank': 0x03,
            'hbank_rom': 0x03,
            'wram': {sym("hBankROM"): b'\x03', sym("wScriptPointer"): b'\x00\xc5', sym("wNameBuffer"): b'\x004\x12', sym("wBreakScriptLoop"): b'\x00'},
            'read': {sym("hBankROM"): 0x01, sym("wScriptPointer"): 0x02, sym("wBreakScriptLoop"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'rom_bank': 0x03,
            'hbank_rom': 0x03,
            'wram': {sym("hBankROM"): b'\x03', sym("wScriptPointer"): b'\x00\xc5', sym("wNameBuffer"): b'\x004\x12', sym("wBreakScriptLoop"): b'\xff'},
            'read': {sym("hBankROM"): 0x01, sym("wScriptPointer"): 0x02, sym("wBreakScriptLoop"): 0x01}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x44,
            'e': 0x55,
            'hl': 0x4567,
            'rom_bank': 0x03,
            'hbank_rom': 0x03,
            'wram': {sym("hBankROM"): b'\x03', sym("wScriptPointer"): b'\x00\xc5', sym("wNameBuffer"): b'\x014\x12', sym("wBreakScriptLoop"): b'\x00'},
            'read': {sym("hBankROM"): 0x01, sym("wScriptPointer"): 0x02, sym("wBreakScriptLoop"): 0x01}},
    ],
})
MUTATIONS.update({
    'GetMapScriptPointer': {   'source_symbol': 'GetMapScriptPointer',
        'before': 'uint8_t f = found == 0u ? 0x80u : 0x10u;',
        'after': 'uint8_t f = found == 0u ? 0x10u : 0x80u;',
        'case_ids': [   'GetMapScriptPointer-2',
                        'GetMapScriptPointer-0',
                        'GetMapScriptPointer-1',
                        'GetMapScriptPointer-3',
                        'GetMapScriptPointer-4'],
        'source': 'src/profiles/extended/home/script.c'},
    'RunOverworldScript': {   'source_symbol': 'RunOverworldScript',
        'before': 'ScriptDispatchFn dispatch = ScriptDispatchLookupOpcode(opcode);',
        'after': 'ScriptDispatchFn dispatch = ScriptDispatchLookupOpcode((uint8_t)(opcode + 1u));',
        'case_ids': ['RunOverworldScript-0', 'RunOverworldScript-1'],
        'source': 'src/profiles/extended/home/script.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
