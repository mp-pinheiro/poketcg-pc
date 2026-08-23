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

# >>> factory GetSavedDeckPointers
wMachineDeckPtrs = 0xD00D
CONTRACT["GetSavedDeckPointers"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["GetSavedDeckPointers"] = [
	{"wram": {wMachineDeckPtrs: b"\xaa" * 0x78}},  # 0x78 = 2 bytes * NUM_DECK_SAVE_MACHINE_SLOTS
	dict(POISON, wram={wMachineDeckPtrs: b"\x55" * 0x78}),
]
# <<< factory GetSavedDeckPointers

# >>> factory GetSavedDeckCount
CONTRACT["GetSavedDeckCount"] = {"compare": (), "preserve": ()}
CASES["GetSavedDeckCount"] = [
    {"sram": {0: {0xA350: bytes(0x54 * 0x3C)}}, "read": {0xD085: 1}},
    dict(POISON,
         sram={0: {0xA350: bytes(1 if i in (0, 0x54, 0xA8) else 0
                              for i in range(0x54 * 0x3C))}},
         read={0xD085: 1}),
    {"sram": {0: {0xA350: bytes(1 if i == 0 else 0
                              for i in range(0x54 * 0x3C))}},
     "read": {0xD085: 1}},
    {"sram": {0: {0xA350: bytes(1 if i == 0x54 else 0
                              for i in range(0x54 * 0x3C))}},
     "read": {0xD085: 1}},
    {"sram": {0: {0xA350: b"\x01" * (0x54 * 0x3C)}},
     "read": {0xD085: 1}},
]
# <<< factory GetSavedDeckCount

# >>> factory GetSelectedSavedDeckPtr
CONTRACT["GetSelectedSavedDeckPtr"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "hl")}
CASES["GetSelectedSavedDeckPtr"] = [
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x34\x12"}},
    dict(POISON,
         wram={0xD088: b"\x01", 0xD00D: b"\x78\x56\xBC\x9A"}),
    {"wram": {0xD088: b"\x00", 0xD00D: b"\x00\x00"}},
    {"wram": {0xD088: b"\x01", 0xD00D: b"\x00\x00\x78\x56"}},
    {"wram": {0xD088: b"\xFF",
              0xD00D: bytes(0x1FE) + b"\xEF\xBE\x00\x00"}},
]
# <<< factory GetSelectedSavedDeckPtr

# >>> factory SafelySwitchToSRAM0
CONTRACT["SafelySwitchToSRAM0"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SafelySwitchToSRAM0"] = [
    {"wram": {0xFF81: b"\x00", 0xD0A4: b"\x00"}, "read": {0xFF81: 1, 0xD0A4: 1}},
    dict(POISON,
         wram={0xFF81: b"\x02", 0xD0A4: b"\xEE"},
         read={0xFF81: 1, 0xD0A4: 1}),
    {"wram": {0xFF81: b"\x01", 0xD0A4: b"\x00"}, "read": {0xFF81: 1, 0xD0A4: 1}},
    {"wram": {0xFF81: b"\x03", 0xD0A4: b"\xFF"}, "read": {0xFF81: 1, 0xD0A4: 1}},
]
# <<< factory SafelySwitchToSRAM0

# >>> factory-cases-statics
wCardListVisibleOffset = 0xCEA1
wNumDeckMachineEntries = 0xD0A5
wUnableToScrollDown = 0xCECD
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wConsole = 0xCAB4
wLCDC = 0xCABB
# <<< factory-cases-statics

# >>> factory DrawListScrollArrows
CONTRACT["DrawListScrollArrows"] = {"compare": (), "preserve": ()}
CASES["DrawListScrollArrows"] = [
    {"wram": {wCardListVisibleOffset: b"\x00", wNumDeckMachineEntries: b"\x00", wUnableToScrollDown: b"\xAA"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
    dict(POISON, wram={wCardListVisibleOffset: b"\x01", wNumDeckMachineEntries: b"\x07", wUnableToScrollDown: b"\xAA"},
         read={wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
         vread={0: {0x9833: 1, 0x9953: 1}}),
    {"wram": {wCardListVisibleOffset: b"\x05", wNumDeckMachineEntries: b"\x0A", wUnableToScrollDown: b"\x00"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
    {"wram": {wCardListVisibleOffset: b"\xFA", wNumDeckMachineEntries: b"\x00", wUnableToScrollDown: b"\xFF"},
     "read": {wCardListVisibleOffset: 1, wNumDeckMachineEntries: 1, wUnableToScrollDown: 1},
     "vread": {0: {0x9833: 1, 0x9953: 1}}},
]
# <<< factory DrawListScrollArrows

# >>> factory SetDeckMachineTitleText
CONTRACT["SetDeckMachineTitleText"] = {"compare": ("hl",), "preserve": ()}
CASES["SetDeckMachineTitleText"] = [
    {"wram": {0xD0A2: b"\x00\x00", 0xCABB: b"\x00"}, "read": {0xFFAD: 1}},
    dict(POISON, wram={0xD0A2: b"\x00\x00", 0xCABB: b"\x00"}, read={0xFFAD: 1}),
]
# <<< factory SetDeckMachineTitleText

# >>> factory FindFirstEmptyDeckSlot
CONTRACT["FindFirstEmptyDeckSlot"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["FindFirstEmptyDeckSlot"] = [
    {"ramg": True, "sram": {0: {0xA218: b"\x00"}}},
    dict(POISON, ramg=True, sram={0: {0xA218: b"\x01", 0xA26C: b"\x00"}}),
    {"ramg": True, "sram": {0: {0xA218: b"\x01", 0xA26C: b"\x02", 0xA2C0: b"\x03", 0xA314: b"\x04"}}},
]
# <<< factory FindFirstEmptyDeckSlot

# >>> factory EmptyScreenAndDrawTextBox
CONTRACT["EmptyScreenAndDrawTextBox"] = {"compare": (), "preserve": ()}
CASES["EmptyScreenAndDrawTextBox"] = [
    {"wram": {wConsole: b"\x00", wLCDC: b"\x00"},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}},
    dict(POISON, wram={wConsole: b"\x00", wLCDC: b"\x00"},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}),
]
# <<< factory EmptyScreenAndDrawTextBox

# >>> factory PrintCardToSendText
CONTRACT["PrintCardToSendText"] = {"compare": (), "preserve": ()}
CASES["PrintCardToSendText"] = [
    {"wram": {wConsole: b"\x00", wLCDC: b"\x00"},
     "vread": {0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}},
    dict(POISON, wram={wConsole: b"\x00", wLCDC: b"\x00"},
         vread={0: {0x8000: 16, 0x8D00: 768, 0x9000: 896, 0x9380: 32, 0x9800: 32 * 14}}),
]
# <<< factory PrintCardToSendText

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
# >>> factory-mutation GetSavedDeckPointers
MUTATIONS["GetSavedDeckPointers"] = {
	"source_symbol": "GetSavedDeckPointers",
	"before": "gb_write8(d++, (uint8_t)h);\n\t\tgb_write8(d++, (uint8_t)(h >> 8));",
	"after": "gb_write8(d++, (uint8_t)(h >> 8));\n\t\tgb_write8(d++, (uint8_t)h);",
	"case_ids": ["GetSavedDeckPointers-0", "GetSavedDeckPointers-1"],
}
# <<< factory-mutation GetSavedDeckPointers
# >>> factory-mutation GetSavedDeckCount
MUTATIONS["GetSavedDeckCount"] = {"source_symbol": "GetSavedDeckCount", "before": "i * DECK_STRUCT_SIZE", "after": "i * (DECK_STRUCT_SIZE - 1u)", "case_ids": ["GetSavedDeckCount-1", "GetSavedDeckCount-3", "GetSavedDeckCount-4"]}
# <<< factory-mutation GetSavedDeckCount
# >>> factory-mutation GetSelectedSavedDeckPtr
MUTATIONS["GetSelectedSavedDeckPtr"] = {"source_symbol": "GetSelectedSavedDeckPtr", "before": "(uint8_t)(index << 1)", "after": "index", "case_ids": ["GetSelectedSavedDeckPtr-1", "GetSelectedSavedDeckPtr-3", "GetSelectedSavedDeckPtr-4"]}
# <<< factory-mutation GetSelectedSavedDeckPtr
# >>> factory-mutation SafelySwitchToSRAM0
MUTATIONS["SafelySwitchToSRAM0"] = {"source_symbol": "SafelySwitchToSRAM0", "before": "if (bank != 0u)", "after": "if (bank == 0u)", "case_ids": ["SafelySwitchToSRAM0-1", "SafelySwitchToSRAM0-2", "SafelySwitchToSRAM0-3"]}
# <<< factory-mutation SafelySwitchToSRAM0
# >>> factory-mutation DrawListScrollArrows
MUTATIONS["DrawListScrollArrows"] = {
    "source_symbol": "DrawListScrollArrows",
    "before": "WriteByteToBGMap0(tile, 19u, 1u);",
    "after": "WriteByteToBGMap0(tile, 19u, 11u);",
    "case_ids": ["DrawListScrollArrows-0", "DrawListScrollArrows-1", "DrawListScrollArrows-2", "DrawListScrollArrows-3"],
}
# <<< factory-mutation DrawListScrollArrows
# >>> factory-mutation SetDeckMachineTitleText
MUTATIONS["SetDeckMachineTitleText"] = {"source_symbol": "SetDeckMachineTitleText", "before": "\tInitTextPrinting(1u, 0u);", "after": "\tInitTextPrinting(0u, 0u);", "case_ids": ["SetDeckMachineTitleText-0", "SetDeckMachineTitleText-1"]}
# <<< factory-mutation SetDeckMachineTitleText
# >>> factory-mutation FindFirstEmptyDeckSlot
MUTATIONS["FindFirstEmptyDeckSlot"] = {"source_symbol": "FindFirstEmptyDeckSlot", "before": "\treturn (FindFirstEmptyDeckSlotResult){0u, 0x80u, hl};", "after": "\treturn (FindFirstEmptyDeckSlotResult){1u, 0x80u, hl};", "case_ids": ["FindFirstEmptyDeckSlot-0"]}
# <<< factory-mutation FindFirstEmptyDeckSlot
# >>> factory-mutation EmptyScreenAndDrawTextBox
MUTATIONS["EmptyScreenAndDrawTextBox"] = {"source_symbol": "EmptyScreenAndDrawTextBox", "before": "\tDrawRegularTextBox(&hl, 0u, 20u, 13u, 0u, 0u);", "after": "\tDrawRegularTextBox(&hl, 0u, 19u, 13u, 0u, 0u);", "case_ids": ["EmptyScreenAndDrawTextBox-0", "EmptyScreenAndDrawTextBox-1"]}
# <<< factory-mutation EmptyScreenAndDrawTextBox
# >>> factory-mutation PrintCardToSendText
MUTATIONS["PrintCardToSendText"] = {"source_symbol": "PrintCardToSendText", "before": "\tProcessTextFromID(CardToSendText);", "after": "\tProcessTextFromID(0u);", "case_ids": ["PrintCardToSendText-0", "PrintCardToSendText-1"]}
# <<< factory-mutation PrintCardToSendText
