"""Extended oracle-diff cases for grass_club, seeded from tests/cases/grass_club.py."""

CONTRACT = {
    'GrassClubAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'Script_Nikki': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Preload_NikkiInGrassClub': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'GrassClubAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'Script_Nikki': [
        {'wram': {0xD31C: b'\x03'}},
        {'wram': {0xD31C: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31C: b'\x03'}},
    ],
    'Preload_NikkiInGrassClub': [
        {'wram': {0xD3CC: b'\x00'}},
        {'wram': {0xD3CC: b'\x02'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CC: b'\x02'}},
    ],
}

MUTATIONS = {
    'GrassClubAfterDuel': {   'source_symbol': 'GrassClubAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(GrassClubAfterDuelTable + 1u));',
        'case_ids': ['GrassClubAfterDuel-0'],
        'source': 'src/home/grass_club.c'},
    'Script_Nikki': {   'source_symbol': 'Script_Nikki',
        'before': 'return (ScriptNikkiResult){map, nikki_cp_flags(map, ISHIHARAS_HOUSE)};',
        'after': 'return (ScriptNikkiResult){map, nikki_cp_flags(map, 0x04u)};',
        'case_ids': ['Script_Nikki-0'],
        'source': 'src/home/grass_club.c'},
    'Preload_NikkiInGrassClub': {   'source_symbol': 'Preload_NikkiInGrassClub',
        'before': 'if (a == NIKKI_IN_GRASS_CLUB)',
        'after': 'if (a != NIKKI_IN_GRASS_CLUB)',
        'case_ids': ['Preload_NikkiInGrassClub-0',
                     'Preload_NikkiInGrassClub-1',
                     'Preload_NikkiInGrassClub-2'],
        'source': 'src/profiles/extended/home/grass_club.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record, _map in zip(SCHEMA2_CASES["Script_Nikki"], (0x5935, 0x660D, 0x5935)):
    _record["completion"] = {"mode": "pre-ret", "pc": _map, "bank": 3}
