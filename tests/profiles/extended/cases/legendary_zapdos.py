"""Extended oracle-diff cases for legendary_zapdos, seeded from tests/cases/legendary_zapdos.py."""

CONTRACT = {
    'AIDoTurn_LegendaryZapdos': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryZapdos': [
        {   'keys': [0x00, 0x01],
            'wram': {   0xFF97: b'\xc2',
                        0xCD2D: b'\x80',
                        0xC2EE: b'\x00',
                        0xC3EE: b'\x00',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\x00',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb9\xff',
                        0xC600: b'\xb9\xff',
                        0xCBB5: b'\x01',
                        0xCAC2: b'\x01',
                        0xCABB: b'\x00',
                        0xCBA3: b'\x01'},
            'read': {0xCDA6: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'wram': {   0xFF97: b'\xc2',
                        0xCD2D: b'\x80',
                        0xC2EE: b'\x00',
                        0xC3EE: b'\x00',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\x00',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb9\xff',
                        0xC600: b'\xb9\xff',
                        0xCBB5: b'\x01',
                        0xCAC2: b'\x01',
                        0xCABB: b'\x00',
                        0xCBA3: b'\x01'},
            'read': {0xCDA6: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryZapdos': {   'source_symbol': 'AIDoTurn_LegendaryZapdos',
        'before': '\treturn (AIDoTurn_LegendaryZapdosResult){decision.f};',
        'after': '\treturn (AIDoTurn_LegendaryZapdosResult){0xffu};',
        'case_ids': ['AIDoTurn_LegendaryZapdos-0', 'AIDoTurn_LegendaryZapdos-1'],
        'source': 'src/profiles/extended/home/legendary_zapdos.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
