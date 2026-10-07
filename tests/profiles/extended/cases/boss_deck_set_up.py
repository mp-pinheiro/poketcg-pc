"""Extended oracle-diff cases for boss_deck_set_up, seeded from tests/cases/boss_deck_set_up.py."""
from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_SETUP = Fixture(
    "ai-duel-fire-charge-setupbossstartinghandanddeck-entry",
    directory=_FIXTURES,
    holes=(0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D),
    lcdc=0xCABB,
)
_SETUP_AVOID_PRIZE = Fixture(
    "boss-setup-avoid-prize-fighting-carriers",
    directory=_FIXTURES,
    holes=(0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D),
    lcdc=0xCABB,
)

CONTRACT = {
    'SetUpBossStartingHandAndDeck': {'compare': (), 'preserve': ()},
}

CASES = {
    'SetUpBossStartingHandAndDeck': [
        {   'wram': {   0xFF97: b'\xc2',
                        0xC2BA: b'\x07',
                        0xC2EE: b'\x07',
                        0xC242: b'56789:;',
                        0xC27E: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12',
                        0xC400: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xC418: b'\x08',
                        0xC419: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xC44D: b'\x08\x08\x01\x01\x08',
                        0xCD2E: b'\x00\x00'},
            'read': {0xCD8D: 0x01, 0xCD8F: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xC2BA: b'\x07',
                        0xC2EE: b'\x07',
                        0xC242: b'56789:;',
                        0xC27E: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12',
                        0xC400: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xC418: b'\x08',
                        0xC419: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xC44D: b'\x08\x08\x01\x01\x08',
                        0xCD2E: b'\x00\x00'},
            'read': {0xCD8D: 0x01, 0xCD8F: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
}
CASES['SetUpBossStartingHandAndDeck'] = [
    dict(_SETUP.case(vram=False), **_SETUP.regs),
    dict(_SETUP_AVOID_PRIZE.case(vram=False), **_SETUP_AVOID_PRIZE.regs),
]


MUTATIONS = {
    'SetUpBossStartingHandAndDeck': {   'source_symbol': 'SetUpBossStartingHandAndDeck',
        'before': '\t\t\treturn (uint8_t)(entry == card);\n\t}',
        'after': '\t\t\treturn (uint8_t)(entry == card);\n\t\tlist++;\n\t}',
        'case_ids': ['SetUpBossStartingHandAndDeck-1'],
        'source': 'src/profiles/extended/home/boss_deck_set_up.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
