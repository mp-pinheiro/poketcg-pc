"""Extended oracle-diff cases for psychic_club_entrance, seeded from tests/cases/psychic_club_entrance.py."""

CONTRACT = {
    'TryFirstRonaldDuel': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ()},
    'TrySecondRonaldDuel': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ()},
    'LoadClubEntrance': {'compare': (), 'preserve': ()},
    'ClubEntranceAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Func_e8a0': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'Preload_Ronald1InClubEntrance': {'compare': ('a', 'f'), 'preserve': ()},
    'Preload_Ronald2InClubEntrance': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'Preload_Ronald3InClubEntrance': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
}

CASES = {
    'TryFirstRonaldDuel': [
        {   'b': 0x12,
            'c': 0x34,
            'hl': 0x00,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<',
                        0xD3D4: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<'}},
        {   'b': 0x56,
            'c': 0x78,
            'hl': 0x00,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19q\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<',
                        0xD3D4: b' '}},
    ],
    'TrySecondRonaldDuel': [
        {   'b': 0x12,
            'c': 0x34,
            'hl': 0x00,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<'}},
    ],
    'LoadClubEntrance': [
        {   'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<'},
            'read': {0xD399: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<'},
            'read': {0xD399: 0x01}},
    ],
    'ClubEntranceAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'q'}},
        {'wram': {0xD0B0: b'\x00', 0xD0B1: b'r'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'q'}},
    ],
    'Func_e8a0': [
        {'a': 0x01, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {'a': 0x02},
        {'a': 0x02, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'Preload_Ronald1InClubEntrance': [
        {'wram': {0xD3D4: b'\x00'}},
        {'wram': {0xD3D4: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3D4: b'\x7f'}},
    ],
    'Preload_Ronald2InClubEntrance': [
        {'wram': {0xD3D4: b'\x00', 0xD3C1: b'\x00'}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {'wram': {0xD3D4: b'\x00', 0xD3C1: b'\xc0'}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {'wram': {0xD3D4: b' '}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3D4: b'@'},
            'read': {0xD39A: 0x01, 0xD39B: 0x01}},
    ],
    'Preload_Ronald3InClubEntrance': [
        {'wram': {0xD3D4: b'\x00', 0xD3C1: b'\x00'}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {'wram': {0xD3D4: b'\x00', 0xD3C1: b'\xf8'}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {'wram': {0xD3D4: b'\x08'}, 'read': {0xD39A: 0x01, 0xD39B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3D4: b'\x10'},
            'read': {0xD39A: 0x01, 0xD39B: 0x01}},
    ],
}

MUTATIONS = {
    'TryFirstRonaldDuel': {   'source_symbol': 'TryFirstRonaldDuel',
        'before': '\tSetNextNPCAndScriptResult r2 = '
                  'SetNextNPCAndScript(Script_FirstRonaldDuel_ADDR, hl);',
        'after': '\tSetNextNPCAndScriptResult r2 = '
                 'SetNextNPCAndScript((uint16_t)(Script_FirstRonaldDuel_ADDR + 1u), hl);',
        'case_ids': ['TryFirstRonaldDuel-0'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'TrySecondRonaldDuel': {   'source_symbol': 'TrySecondRonaldDuel',
        'before': 'return (TrySecondRonaldDuelResult){r.a, r.f, b, c, hl};',
        'after': 'return (TrySecondRonaldDuelResult){0u, r.f, b, c, hl};',
        'case_ids': ['TrySecondRonaldDuel-0', 'TrySecondRonaldDuel-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'LoadClubEntrance': {   'source_symbol': 'LoadClubEntrance',
        'before': 'TryFirstRonaldEncounterResult r3 = TryFirstRonaldEncounter(r2.b, r2.c, r2.hl);',
        'after': 'TryFirstRonaldEncounterResult r3 = {0};',
        'case_ids': ['LoadClubEntrance-0', 'LoadClubEntrance-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'ClubEntranceAfterDuel': {   'source_symbol': 'ClubEntranceAfterDuel',
        'before': 'FindEndOfDuelScriptResult r = FindEndOfDuelScript(ClubEntranceAfterDuelTable);',
        'after': 'FindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(ClubEntranceAfterDuelTable + 1u));',
        'case_ids': ['ClubEntranceAfterDuel-0', 'ClubEntranceAfterDuel-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'Func_e8a0': {   'source_symbol': 'Func_e8a0',
        'before': '\t\twLoadNPCXPos = 0x08u;',
        'after': '\t\twLoadNPCXPos = 0x09u;',
        'case_ids': ['Func_e8a0-0'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'Preload_Ronald1InClubEntrance': {   'source_symbol': 'Preload_Ronald1InClubEntrance',
        'before': '\tif (a < TRUE)\n\t\tf |= 0x10u;',
        'after': '\tif (a <= TRUE)\n\t\tf |= 0x10u;',
        'case_ids': ['Preload_Ronald1InClubEntrance-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'Preload_Ronald2InClubEntrance': {   'source_symbol': 'Preload_Ronald2InClubEntrance',
        'before': 'GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE), b, c, d, 2u, hl);',
        'after': 'GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE), b, c, d, 3u, hl);',
        'case_ids': ['Preload_Ronald2InClubEntrance-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
    'Preload_Ronald3InClubEntrance': {   'source_symbol': 'Preload_Ronald3InClubEntrance',
        'before': 'GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE), b, c, d, 5u, hl);',
        'after': 'GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE), b, c, d, 4u, hl);',
        'case_ids': ['Preload_Ronald3InClubEntrance-1'],
        'source': 'src/profiles/extended/home/psychic_club_entrance.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
