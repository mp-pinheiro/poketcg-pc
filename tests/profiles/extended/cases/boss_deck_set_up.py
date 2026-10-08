"""Extended oracle-diff cases for boss_deck_set_up: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_SETUP = Fixture(
    "ai-duel-fire-charge-setupbossstartinghandanddeck-entry",
    directory=_FIXTURES,
    holes=(sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter")),
    lcdc=sym("wLCDC"),
)
_SETUP_AVOID_PRIZE = Fixture(
    "boss-setup-avoid-prize-fighting-carriers",
    directory=_FIXTURES,
    holes=(sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter")),
    lcdc=sym("wLCDC"),
)
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('boss_deck_set_up')
OWN = ('SetUpBossStartingHandAndDeck',)
CONTRACT.update({
    'SetUpBossStartingHandAndDeck': {'compare': (), 'preserve': ()},
})
CASES.update({
    'SetUpBossStartingHandAndDeck': [
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerNumberOfCardsNotInDeck"): b'\x07',
                        sym("wPlayerNumberOfCardsInHand"): b'\x07',
                        sym("wPlayerHand"): b'56789:;',
                        sym("wPlayerDeckCards"): b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12',
                        sym("wBoosterCardsDrawn"): b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        sym("wBoosterTempEnergiesDrawn") + 2: b'\x08',
                        sym("wBoosterTempEnergiesDrawn") + 3: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        sym("wBoosterCardsDrawnEnd") + 0x21: b'\x08\x08\x01\x01\x08',
                        sym("wAICardListAvoidPrize"): b'\x00\x00'},
            'read': {sym("wAIDefendingPokemonWeakness"): 0x01, sym("wAISetupEnergyCount"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerNumberOfCardsNotInDeck"): b'\x07',
                        sym("wPlayerNumberOfCardsInHand"): b'\x07',
                        sym("wPlayerHand"): b'56789:;',
                        sym("wPlayerDeckCards"): b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12',
                        sym("wBoosterCardsDrawn"): b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        sym("wBoosterTempEnergiesDrawn") + 2: b'\x08',
                        sym("wBoosterTempEnergiesDrawn") + 3: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        sym("wBoosterCardsDrawnEnd") + 0x21: b'\x08\x08\x01\x01\x08',
                        sym("wAICardListAvoidPrize"): b'\x00\x00'},
            'read': {sym("wAIDefendingPokemonWeakness"): 0x01, sym("wAISetupEnergyCount"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
})
CASES['SetUpBossStartingHandAndDeck'] = [
    dict(_SETUP.case(vram=False), **_SETUP.regs),
    dict(_SETUP_AVOID_PRIZE.case(vram=False), **_SETUP_AVOID_PRIZE.regs),
]
MUTATIONS.update({
    'SetUpBossStartingHandAndDeck': {   'source_symbol': 'SetUpBossStartingHandAndDeck',
        'before': '\t\t\treturn (uint8_t)(entry == card);\n\t}',
        'after': '\t\t\treturn (uint8_t)(entry == card);\n\t\tlist++;\n\t}',
        'case_ids': ['SetUpBossStartingHandAndDeck-1'],
        'source': 'src/profiles/extended/home/boss_deck_set_up.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
