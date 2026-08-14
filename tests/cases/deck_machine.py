"""Oracle-diff cases for poketcg/src/engine/menus/deck_machine.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory CheckIfSelectedDeckMachineEntryIsEmpty
CONTRACT["CheckIfSelectedDeckMachineEntryIsEmpty"] = {"compare": ("d", "e", "f"), "preserve": ("d", "e")}
CASES["CheckIfSelectedDeckMachineEntryIsEmpty"] = [
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x50\xa3"}, "sram": {0: {0xA367: b"\x7f\x00"}}, "ramg": False},
    dict(POISON, wram={0xD088: b"\x01", 0xD00D: b"\x00\x00\x80\xa3"}, sram={0: {0xA397: b"\x00\x7f"}}, ramg=False),
]
# <<< factory CheckIfSelectedDeckMachineEntryIsEmpty

# >>> factory SafelySwitchToSRAM1
CONTRACT["SafelySwitchToSRAM1"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToSRAM1"] = [
    {"read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON, wram={0xFF81: b"\x01", 0xD0A4: b"\x55"}),
    {"wram": {0xFF81: b"\x02", 0xD0A4: b"\x09"}},
]
# <<< factory SafelySwitchToSRAM1

# >>> factory SafelySwitchToTempSRAMBank
CONTRACT["SafelySwitchToTempSRAMBank"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToTempSRAMBank"] = [
    {"read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON, wram={0xFF81: b"\x02", 0xD0A4: b"\x01"}),
    {"wram": {0xFF81: b"\x03", 0xD0A4: b"\x03"}},
]
# <<< factory SafelySwitchToTempSRAMBank

# >>> factory CheckIfHasEnoughCardsToBuildDeck
CONTRACT["CheckIfHasEnoughCardsToBuildDeck"] = {"compare": ("a", "f", "c", "hl"), "preserve": ("c",)}
CASES["CheckIfHasEnoughCardsToBuildDeck"] = [
    {"hl": 0xC100,
     "wram": {0xC000: b"\x00", 0xC100: b"\x00"},
     "read": {0xC000: 1}},
    dict(POISON, hl=0xC100,
         wram={0xC000: b"\x3c", 0xC100: b"\x00" * 60},
         read={0xC000: 1, 0xC100: 60}),
    {"hl": 0xC100,
     "wram": {0xC000: b"\x01", 0xC100: b"\x00\x00"},
     "read": {0xC000: 1, 0xC100: 2}},
    {"hl": 0xC100,
     "wram": {0xC000: b"\x00\x00\x00\x00\x00\x80", 0xC100: b"\x05"},
     "read": {0xC005: 1}},
    {"hl": 0xC100,
     "wram": {0xC000: b"\x01" * 60, 0xC100: bytes(range(60))},
     "read": {0xC000: 60, 0xC100: 60}},
]
# <<< factory CheckIfHasEnoughCardsToBuildDeck

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
MUTATIONS["CheckIfSelectedDeckMachineEntryIsEmpty"] = {"source_symbol": "CheckIfSelectedDeckMachineEntryIsEmpty", "before": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);", "after": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE - 1u);", "case_ids": ["CheckIfSelectedDeckMachineEntryIsEmpty-0", "CheckIfSelectedDeckMachineEntryIsEmpty-1"]}
# <<< factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
# >>> factory-mutation SafelySwitchToSRAM1
MUTATIONS["SafelySwitchToSRAM1"] = {"source_symbol": "SafelySwitchToSRAM1", "before": "if (hBankSRAM != 1u)", "after": "if (hBankSRAM == 1u)", "case_ids": ["SafelySwitchToSRAM1-0", "SafelySwitchToSRAM1-2"]}
# <<< factory-mutation SafelySwitchToSRAM1
# >>> factory-mutation SafelySwitchToTempSRAMBank
MUTATIONS["SafelySwitchToTempSRAMBank"] = {"source_symbol": "SafelySwitchToTempSRAMBank", "before": "if (hBankSRAM != wTempBankSRAM)", "after": "if (hBankSRAM != (uint8_t)(wTempBankSRAM + 1u))", "case_ids": ["SafelySwitchToTempSRAMBank-1"]}
# <<< factory-mutation SafelySwitchToTempSRAMBank
# >>> factory-mutation CheckIfHasEnoughCardsToBuildDeck
MUTATIONS["CheckIfHasEnoughCardsToBuildDeck"] = {"source_symbol": "CheckIfHasEnoughCardsToBuildDeck", "before": "if (count == 0u || count == CARD_NOT_OWNED)", "after": "if (count == 0u && count == CARD_NOT_OWNED)", "case_ids": ["CheckIfHasEnoughCardsToBuildDeck-0", "CheckIfHasEnoughCardsToBuildDeck-2", "CheckIfHasEnoughCardsToBuildDeck-3"]}
# <<< factory-mutation CheckIfHasEnoughCardsToBuildDeck
