"""Oracle-diff cases for poketcg/src/engine/auto_deck_machines.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wCurAutoDeckMachine_A = 0xD0A9
sAutoDecks_A = 0xA350
wDismantledDeckName_A = 0xD089
wAutoDeckMachineTextDescriptions_A = 0xD0AA

hBankSRAM = 0xFF81
wTempBankSRAM = 0xD0A4
wMachineDeckPtrs = 0xD00D
wSelectedDeckMachineEntry = 0xD088
wDecksToBeDismantled = 0xD0A6
# <<< factory-cases-statics

# >>> factory ReadAutoDeckConfiguration
CONTRACT["ReadAutoDeckConfiguration"] = {"compare": (), "preserve": (), "wram_out": True, "sram_out": True}
CASES["ReadAutoDeckConfiguration"] = [
    {"wram": {wCurAutoDeckMachine_A: b"\x00"},
     "sram": {0: {sAutoDecks_A: bytes([0xFF] * (0x54 * 5))}},
     "instruction_budget": 300000, "cycle_budget": 1500000,
     "read": {wDismantledDeckName_A: 32, wAutoDeckMachineTextDescriptions_A: 10},
     "sread": {0: {sAutoDecks_A: 0x54 * 5}}},
    dict(POISON, wram={wCurAutoDeckMachine_A: b"\x01"},
         sram={0: {sAutoDecks_A: bytes([0xFF] * (0x54 * 5))}},
         instruction_budget=300000, cycle_budget=1500000,
         read={wDismantledDeckName_A: 32, wAutoDeckMachineTextDescriptions_A: 10},
         sread={0: {sAutoDecks_A: 0x54 * 5}}),
]
# <<< factory ReadAutoDeckConfiguration

# >>> factory CheckWhichDecksToDismantleToBuildSavedDeck
CONTRACT["CheckWhichDecksToDismantleToBuildSavedDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckWhichDecksToDismantleToBuildSavedDeck"] = [
    {"wram": {hBankSRAM: b"\x00", wTempBankSRAM: b"\x00", wSelectedDeckMachineEntry: b"\x00",
              wMachineDeckPtrs: b"\xE8\xC0", 0xC000: b"\x00", 0xC100: b"\x00"},
     "sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={hBankSRAM: b"\x00", wTempBankSRAM: b"\x00", wSelectedDeckMachineEntry: b"\x00",
                       wMachineDeckPtrs: b"\xE8\xC0", 0xC000: b"\x00", 0xC100: b"\x00"},
         sram={0: {}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory CheckWhichDecksToDismantleToBuildSavedDeck

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation ReadAutoDeckConfiguration
MUTATIONS["ReadAutoDeckConfiguration"] = {"source_symbol": "ReadAutoDeckConfiguration", "before": "\t\tuint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + (uint16_t)b * 2u);", "after": "\t\tuint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + (uint16_t)b * 2u + 1u);", "case_ids": ["ReadAutoDeckConfiguration-0", "ReadAutoDeckConfiguration-1"]}
# <<< factory-mutation ReadAutoDeckConfiguration
# >>> factory-mutation CheckWhichDecksToDismantleToBuildSavedDeck
MUTATIONS["CheckWhichDecksToDismantleToBuildSavedDeck"] = {
    "source_symbol": "CheckWhichDecksToDismantleToBuildSavedDeck",
    "before": "\tf = (uint8_t)((f & 0x80u) | 0x10u);\n\treturn (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};",
    "after": "\tf = (uint8_t)((f & 0x80u) | 0x00u);\n\treturn (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};",
    "case_ids": ["CheckWhichDecksToDismantleToBuildSavedDeck-0", "CheckWhichDecksToDismantleToBuildSavedDeck-1"],
}
# <<< factory-mutation CheckWhichDecksToDismantleToBuildSavedDeck
