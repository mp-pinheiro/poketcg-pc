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
