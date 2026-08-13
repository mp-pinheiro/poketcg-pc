"""Oracle-diff cases for poketcg/src/engine/duel/ai/trainer_cards.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory RemoveCardFromList
CONTRACT["RemoveCardFromList"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["RemoveCardFromList"] = [
    {"hl": 0xC101, "wram": {0xC100: b"\xaa\xff"}},
    {"hl": 0xC101, "wram": {0xC100: b"\xaa\x01\x02\xff\x55"}},
    dict(POISON, hl=0xC102, wram={0xC100: b"\x10\x11\x12\x13\xff"}),
]
# <<< factory RemoveCardFromList

# >>> factory FindDuplicateCards
CONTRACT["FindDuplicateCards"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["FindDuplicateCards"] = [
    {"hl": 0xC900, "wram": {0xC900: b"\xff", 0xCE0F: b"\x00\x00"}},
    {"hl": 0xC900, "wram": {0xC900: b"\x00\x01\xff", 0xCE0F: b"\x00\x00"}},
    {"hl": 0xC900, "wram": {0xC900: b"\x05\xff", 0xCE0F: b"\x00\x00"}},
    dict(POISON, hl=0xC900, wram={0xC900: b"\x02\x03\x04\xff", 0xCE0F: b"\xaa\xbb"}),
]
# <<< factory FindDuplicateCards


# >>> factory FindAndRemoveCardFromList
CONTRACT["FindAndRemoveCardFromList"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["FindAndRemoveCardFromList"] = [
    {"a": 0, "hl": 0xC900, "wram": {0xC900: b"\x00\xff"}},
    {"a": 5, "hl": 0xC900, "wram": {0xC900: b"\x01\x02\x05\x07\xff"}},
    dict(POISON, a=3, hl=0xC900, wram={0xC900: b"\x01\x03\x05\xff"}),
]
# <<< factory FindAndRemoveCardFromList

# >>> factory PickPokedexCards
CONTRACT["PickPokedexCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PickPokedexCards"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00",
              0xC27E: b"\x01\x02\x03\x04\x05"},
     "read": {0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BA: b"\x00",
                       0xC27E: b"\x01\x02\x03\x04\x05"},
         read={0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}),
]
# <<< factory PickPokedexCards

# >>> factory AIDecide_Maintenance
CONTRACT["AIDecide_Maintenance"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_Maintenance"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BE: b"\x03", 0xCC0E: b"\x01",
              0xCE16: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BE: b"\x03", 0xCC0E: b"\x01",
                       0xCE16: b"\x00"}),
]
# <<< factory AIDecide_Maintenance

# >>> factory AIDecide_Lass
CONTRACT["AIDecide_Lass"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Lass"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EE: b"\x06"}},
    {"wram": {0xFF97: b"\xC2", 0xC3EE: b"\x07",
              0xC249: b"\x00\x00\x00\x00\x00\x00\x00",
              0xC210: b"\x10"}},
]
# <<< factory AIDecide_Lass

# >>> factory AIDecide_Imakuni
CONTRACT["AIDecide_Imakuni"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Imakuni"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x00"}},
]
# <<< factory AIDecide_Imakuni
# >>> factory AIDecide_PokemonFlute
CONTRACT["AIDecide_PokemonFlute"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonFlute"] = [
    {"c": 0, "wram": {0xCC0E: b"\x01", 0xC510: b"\xff", 0xC3EF: b"\x00"}},
    {"c": 0, "wram": {0xCC0E: b"\x01", 0xC510: b"\x00\xff", 0xC3EF: b"\x00",
                      0xCE06: b"\xff", 0xCE08: b"\xff"}},
]
# <<< factory AIDecide_PokemonFlute
# >>> factory AIDecide_ClefairyDollOrMysteriousFossil
CONTRACT["AIDecide_ClefairyDollOrMysteriousFossil"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_ClefairyDollOrMysteriousFossil"] = [
    {"wram": {0xC3EF: b"\x06"}},
    {"wram": {0xC3EF: b"\x03", 0xC2BB: b"\x00"}},
]
# <<< factory AIDecide_ClefairyDollOrMysteriousFossil
# >>> factory AIDecide_Defender_Phase14
CONTRACT["AIDecide_Defender_Phase14"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Defender_Phase14"] = [dict(POISON, wram={0xC2C8: b"\x32"})]
# <<< factory AIDecide_Defender_Phase14
# >>> factory AIDecide_Bill
CONTRACT["AIDecide_Bill"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Bill"] = [{"wram": {0xC3BA: b"\x33"}}]
# <<< factory AIDecide_Bill

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation RemoveCardFromList
MUTATIONS["RemoveCardFromList"] = {
    "source_symbol": "RemoveCardFromList",
    "before": "\t*hl = (uint16_t)(*hl - 1u);",
    "after": "\t*hl = (uint16_t)(*hl - 2u);",
    "case_ids": ["RemoveCardFromList-0", "RemoveCardFromList-1", "RemoveCardFromList-2"],
}
# <<< factory-mutation RemoveCardFromList
# >>> factory-mutation FindDuplicateCards
MUTATIONS["FindDuplicateCards"] = {
    "source_symbol": "FindDuplicateCards",
    "before": "return (FindDupResult){0xFFu, 0x90u, outer};",
    "after": "return (FindDupResult){0xFFu, 0x10u, outer};",
    "case_ids": ["FindDuplicateCards-0", "FindDuplicateCards-2"],
}
# <<< factory-mutation FindDuplicateCards
# >>> factory-mutation FindAndRemoveCardFromList
MUTATIONS["FindAndRemoveCardFromList"] = {
    "source_symbol": "FindAndRemoveCardFromList",
    "before": "\tRemoveCardFromList(&p);",
    "after": "\tp = hl; RemoveCardFromList(&p);",
    "case_ids": ["FindAndRemoveCardFromList-1", "FindAndRemoveCardFromList-2"],
}
# <<< factory-mutation FindAndRemoveCardFromList

# >>> factory-mutation AIDecide_Bill
MUTATIONS["AIDecide_Bill"] = {
    "source_symbol": "AIDecide_Bill",
    "before": "\treturn (AIDecideResult){f};",
    "after": "\treturn (AIDecideResult){0};",
    "case_ids": ["AIDecide_Bill-0"],
}
# <<< factory-mutation AIDecide_Bill