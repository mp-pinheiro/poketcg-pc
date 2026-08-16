"""Oracle-diff cases for poketcg/src/engine/menus/deck_configuration.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DecrementDeckCardsInCollection
CONTRACT["DecrementDeckCardsInCollection"] = {"compare": ("hl",), "preserve": ()}
sCardCollection = 0xA100
CASES["DecrementDeckCardsInCollection"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00"}, "sram": {0: {sCardCollection: b"\x00" * 4}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x02\x00"}, "sram": {0: {sCardCollection: b"\x05\x05\x05"}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01" * 60}, "sram": {0: {sCardCollection + 1: b"\x63"}}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE}, hl=0xC100, wram={0xC100: b"\x00"}, sram={0: {sCardCollection: b"\x00" * 4}}),
]
# <<< factory DecrementDeckCardsInCollection


# >>> factory AddDeckToCollection
CONTRACT["AddDeckToCollection"] = {"compare": ("hl",), "preserve": ()}
sCardCollection2 = 0xA100
CASES["AddDeckToCollection"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00"}, "sram": {0: {sCardCollection2: b"\x00" * 4}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x02\x00"}, "sram": {0: {sCardCollection2: b"\x05\x05\x05"}}},
    {"hl": 0xC100, "wram": {0xC100: b"\x01" * 60}, "sram": {0: {sCardCollection2 + 1: b"\x62"}}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE}, hl=0xC100, wram={0xC100: b"\x00"}, sram={0: {sCardCollection2: b"\x00" * 4}}),
]
# <<< factory AddDeckToCollection


# >>> factory CopyListFromHLToDE
CONTRACT["CopyListFromHLToDE"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["CopyListFromHLToDE"] = [
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\x00"}, "read": {0xC200: 1}},
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\x01\x02\x00"}, "read": {0xC200: 3}},
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\xFF" * 5 + b"\x00"}, "read": {0xC200: 6}},
    dict({"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC}, hl=0xC100, d=0xC2, e=0x00, wram={0xC100: b"\x00"}, read={0xC200: 1}),
]
# <<< factory CopyListFromHLToDE


# >>> factory CalculateOnesAndTensDigits
CONTRACT["CalculateOnesAndTensDigits"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CalculateOnesAndTensDigits"] = [
    {"a": 0, "wram": {0xCEB6: b"\xFF\xFF"}},
    dict(POISON, wram={0xCEB6: b"\xFF\xFF"}),
    {"a": 1, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 9, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 10, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 19, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 99, "wram": {0xCEB6: b"\xFF\xFF"}},
    {"a": 255, "wram": {0xCEB6: b"\xFF\xFF"}},
]
# <<< factory CalculateOnesAndTensDigits




# >>> factory InitCardSelectionParams
CONTRACT["InitCardSelectionParams"] = {"compare": ("a", "c", "hl"), "preserve": ("c",)}
CASES["InitCardSelectionParams"] = [
    {"a": 0x00, "hl": 0xC100, "wram": {0xC100: b"\x00" * 9}, "read": {0xCEA3: 12, 0xFFB3: 1}},
    dict(POISON, a=0x5A, hl=0xC100, wram={0xC100: bytes(range(1, 10))},
         read={0xCEA3: 12, 0xFFB3: 1}),
    {"a": 0xFF, "hl": 0xC1F8, "wram": {0xC1F8: b"\x11\x22\x33\x44\x55\x66\x77\x88\x99"},
     "read": {0xCEA3: 12, 0xFFB3: 1}},
]
# <<< factory InitCardSelectionParams


# >>> factory ClearMemory_Bank2
CONTRACT["ClearMemory_Bank2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank2"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\xAA" * 0x100}},
    dict(POISON, a=1, hl=0xC200, wram={0xC200: b"\xAA"}),
    {"a": 1, "hl": 0xC300, "wram": {0xC300: b"\xAA"}},
    {"a": 0xFF, "hl": 0xC400, "wram": {0xC400: b"\xAA" * 0xFF}},
]
# <<< factory ClearMemory_Bank2

# >>> factory CheckIfHasOtherValidDecks
CONTRACT["CheckIfHasOtherValidDecks"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfHasOtherValidDecks"] = [
    {"wram": {0xCEB2: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xCEB2: b"\x01\x01\x00\x00"}),
    {"wram": {0xCEB2: b"\x01\x00\x00\x00"}},
    {"wram": {0xCEB2: b"\x00\x01\x00\x00"}},
    {"wram": {0xCEB2: b"\x01\x00\x01\x00"}},
    {"wram": {0xCEB2: b"\x00\x00\x01\x01"}},
]
# <<< factory CheckIfHasOtherValidDecks

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DecrementDeckCardsInCollection
MUTATIONS["DecrementDeckCardsInCollection"] = {
    "source_symbol": "DecrementDeckCardsInCollection",
    "before": "gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));",
    "after": "gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));",
    "case_ids": ["DecrementDeckCardsInCollection-1"],
}
# <<< factory-mutation DecrementDeckCardsInCollection
# >>> factory-mutation AddDeckToCollection
MUTATIONS["AddDeckToCollection"] = {
    "source_symbol": "AddDeckToCollection",
    "before": "gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));",
    "after": "gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));",
    "case_ids": ["AddDeckToCollection-1"],
}
# <<< factory-mutation AddDeckToCollection
# >>> factory-mutation CopyListFromHLToDE
MUTATIONS["CopyListFromHLToDE"] = {
    "source_symbol": "CopyListFromHLToDE",
    "before": "if (a == 0)\n\t\t\tbreak;\n\t\td++;",
    "after": "if (a == 0)\n\t\t\tbreak;\n\t\td += 2u;",
    "case_ids": ["CopyListFromHLToDE-1"],
}
# <<< factory-mutation CopyListFromHLToDE
# >>> factory-mutation CalculateOnesAndTensDigits
MUTATIONS["CalculateOnesAndTensDigits"] = {"source_symbol": "CalculateOnesAndTensDigits", "before": "if (tens != 0u)", "after": "if (tens > 1u)", "case_ids": ["CalculateOnesAndTensDigits-4", "CalculateOnesAndTensDigits-5"]}
# <<< factory-mutation CalculateOnesAndTensDigits
# >>> factory-mutation InitCardSelectionParams
MUTATIONS["InitCardSelectionParams"] = {
    "source_symbol": "InitCardSelectionParams",
    "before": "for (uint8_t i = 0; i < 9u; i++)",
    "after": "for (uint8_t i = 0; i < 8u; i++)",
    "case_ids": ["InitCardSelectionParams-1", "InitCardSelectionParams-2"],
}
# <<< factory-mutation InitCardSelectionParams
# >>> factory-mutation ClearMemory_Bank2
MUTATIONS["ClearMemory_Bank2"] = {"source_symbol": "ClearMemory_Bank2", "before": "uint32_t n = count ? count : 0x100u;", "after": "uint32_t n = count ? count : 0xFFu;", "case_ids": ["ClearMemory_Bank2-0", "ClearMemory_Bank2-1"]}
# <<< factory-mutation ClearMemory_Bank2
# >>> factory-mutation CheckIfHasOtherValidDecks
MUTATIONS["CheckIfHasOtherValidDecks"] = {
    "source_symbol": "CheckIfHasOtherValidDecks",
    "before": "if (gb_read8(hl) == 0)",
    "after": "if (gb_read8(hl) != 0)",
    "case_ids": ["CheckIfHasOtherValidDecks-0", "CheckIfHasOtherValidDecks-1", "CheckIfHasOtherValidDecks-2", "CheckIfHasOtherValidDecks-3"],
}
# <<< factory-mutation CheckIfHasOtherValidDecks
