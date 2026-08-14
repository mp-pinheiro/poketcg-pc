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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
MUTATIONS["CheckIfSelectedDeckMachineEntryIsEmpty"] = {"source_symbol": "CheckIfSelectedDeckMachineEntryIsEmpty", "before": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);", "after": "uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE - 1u);", "case_ids": ["CheckIfSelectedDeckMachineEntryIsEmpty-0", "CheckIfSelectedDeckMachineEntryIsEmpty-1"]}
# <<< factory-mutation CheckIfSelectedDeckMachineEntryIsEmpty
