"""Extended oracle-diff cases for auto_deck_machines, seeded from tests/cases/auto_deck_machines.py."""

CONTRACT = {
    'ReadAutoDeckConfiguration': {'compare': (), 'preserve': (), 'wram_out': True, 'sram_out': True},
    'CheckWhichDecksToDismantleToBuildSavedDeck': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'ReadAutoDeckConfiguration': [
        {   'wram': {0xD096: b'\x00'},
            'sram': {   0x00: {   0xA470: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'}},
            'instruction_budget': 0x493E0,
            'cycle_budget': 0x16E360,
            'read': {0xD076: 0x20, 0xD097: 0x0A},
            'sread': {0x00: {0xA470: 0x01A4}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD096: b'\x01'},
            'sram': {   0x00: {   0xA470: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                          b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'}},
            'instruction_budget': 0x493E0,
            'cycle_budget': 0x16E360,
            'read': {0xD076: 0x20, 0xD097: 0x0A},
            'sread': {0x00: {0xA470: 0x01A4}}},
    ],
    'CheckWhichDecksToDismantleToBuildSavedDeck': [
        {   'wram': {   0xFF81: b'\x00',
                        0xD091: b'\x00',
                        0xD075: b'\x00',
                        0xD00E: b'\xe8\xc0',
                        0xC000: b'\x00',
                        0xC100: b'\x00'},
            'sram': {0x00: {}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF81: b'\x00',
                        0xD091: b'\x00',
                        0xD075: b'\x00',
                        0xD00E: b'\xe8\xc0',
                        0xC000: b'\x00',
                        0xC100: b'\x00'},
            'sram': {0x00: {}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
}

MUTATIONS = {
    'ReadAutoDeckConfiguration': {   'source_symbol': 'ReadAutoDeckConfiguration',
        'before': '\t\tuint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + '
                  '(uint16_t)b * 2u);',
        'after': '\t\tuint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + '
                 '(uint16_t)b * 2u + 1u);',
        'case_ids': ['ReadAutoDeckConfiguration-0', 'ReadAutoDeckConfiguration-1'],
        'source': 'src/profiles/extended/home/auto_deck_machines.c'},
    'CheckWhichDecksToDismantleToBuildSavedDeck': {   'source_symbol': 'CheckWhichDecksToDismantleToBuildSavedDeck',
        'before': '\tf = (uint8_t)((f & 0x80u) | 0x10u);\n'
                  '\treturn (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};',
        'after': '\tf = (uint8_t)((f & 0x80u) | 0x00u);\n'
                 '\treturn (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};',
        'case_ids': [   'CheckWhichDecksToDismantleToBuildSavedDeck-0',
                        'CheckWhichDecksToDismantleToBuildSavedDeck-1'],
        'source': 'src/profiles/extended/home/auto_deck_machines.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
