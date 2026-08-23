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
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EE: b"\x06"}),
    {"wram": {0xFF97: b"\xC2", 0xC3EE: b"\x00"}},
]
# <<< factory AIDecide_Lass

# >>> factory AIDecide_Recycle
CONTRACT["AIDecide_Recycle"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Recycle"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2ED: b"\x00"}),
]
# <<< factory AIDecide_Recycle

# >>> factory AIDecide_Imakuni
CONTRACT["AIDecide_Imakuni"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Imakuni"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F0: b"\x00"}),
]
# <<< factory AIDecide_Imakuni
# >>> factory AIDecide_PokemonFlute
CONTRACT["AIDecide_PokemonFlute"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonFlute"] = [
    {"c": 0, "wram": {0xCC0E: b"\x01", 0xC510: b"\xff", 0xC3EF: b"\x00"}},
    {"c": 0, "wram": {0xCC0E: b"\x01", 0xC510: b"\x00\xff", 0xC3EF: b"\x00",
                      0xCE06: b"\xff", 0xCE08: b"\xff"}},
    dict(POISON, c=0, wram={0xCC0E: b"\x01", 0xC510: b"\xff", 0xC3EF: b"\x00"}),
]
# <<< factory AIDecide_PokemonFlute
# >>> factory AIDecide_ClefairyDollOrMysteriousFossil
CONTRACT["AIDecide_ClefairyDollOrMysteriousFossil"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_ClefairyDollOrMysteriousFossil"] = [
    {"wram": {0xC3EF: b"\x06"}},
    {"wram": {0xC3EF: b"\x03", 0xC2BB: b"\x00"}},
    dict(POISON, wram={0xC3EF: b"\x03", 0xC2BB: b"\x00"}),
]
# <<< factory AIDecide_ClefairyDollOrMysteriousFossil
# >>> factory AIDecide_Defender_Phase14
CONTRACT["AIDecide_Defender_Phase14"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Defender_Phase14"] = [
    dict(POISON),
    dict(POISON, wram={0xCCB4: b"\x01"}),
    dict(POISON, wram={0xCCB4: b"\x02"}),
    dict(POISON, wram={0xCCB4: b"\x08"}),
    dict(POISON, wram={0xC2C8: b"\x32"}),
]
# <<< factory AIDecide_Defender_Phase14

# >>> factory AIDecide_Bill
CONTRACT["AIDecide_Bill"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Bill"] = [
    dict(POISON, wram={0xC3BA: b"\x00"}),
    dict(POISON, wram={0xC3BA: b"\x03"}),
    dict(POISON, wram={0xC3BA: b"\x32"}),
    dict(POISON, wram={0xC3BA: b"\x33"}),
]
# <<< factory AIDecide_Bill


# >>> factory AIDecide_Gambler
CONTRACT["AIDecide_Gambler"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Gambler"] = [
    {"wram": {0xFF97: b"\xC2", 0xCC0E: b"\x34"}},
    {"wram": {0xFF97: b"\xC2", 0xCC0E: b"\x00", 0xCDA7: b"\x80", 0xC2BA: b"\x38"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCC0E: b"\x00", 0xCDA7: b"\x00", 0xC2BA: b"\x38"}),
    {"wram": {0xFF97: b"\xC2", 0xCC0E: b"\x00", 0xCDA7: b"\x00", 0xC2BA: b"\x38"}},
]
# <<< factory AIDecide_Gambler

# >>> factory AIDecide_Revive
CONTRACT["AIDecide_Revive"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_Revive"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC2EF: b"\x00", 0xC400: b"\x88"}},
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC2EF: b"\x00", 0xC400: b"\x87"}},
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC2EF: b"\x00", 0xC400: b"\xBA"}},
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC2EF: b"\x00", 0xC400: b"\xB9"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2ED: b"\x00"}),
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC2EF: b"\x00", 0xC400: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC400: b"\x88",
              0xC2EF: b"\x04"}},
]
# <<< factory AIDecide_Revive

# >>> factory AIDecide_ImposterProfessorOak
CONTRACT["AIDecide_ImposterProfessorOak"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_ImposterProfessorOak"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3BA: b"\x2E", 0xC3EE: b"\x05"}},
    {"wram": {0xFF97: b"\xC2", 0xC3BA: b"\x2E", 0xC3EE: b"\x06"}},
    {"wram": {0xFF97: b"\xC2", 0xC3BA: b"\x2D", 0xC3EE: b"\x08"}},
    {"wram": {0xFF97: b"\xC2", 0xC3BA: b"\x2D", 0xC3EE: b"\x09"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3BA: b"\x2E", 0xC3EE: b"\x05"}),
]
# <<< factory AIDecide_ImposterProfessorOak

# >>> factory PickPokedexCards_Unreferenced
CONTRACT["PickPokedexCards_Unreferenced"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PickPokedexCards_Unreferenced"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00",
              0xC27E: b"\x01\x02\x03\x04\x05"},
     "read": {0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}},
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x01",
              0xC27F: b"\x06\x07\x08\x09\x0A"},
     "read": {0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BA: b"\x00",
                       0xC27E: b"\x01\x02\x03\x04\x05"},
         read={0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}),
]
# <<< factory PickPokedexCards_Unreferenced

# >>> factory AIDecide_Pokedex
CONTRACT["AIDecide_Pokedex"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_Pokedex"] = [
    {"wram": {0xCDA6: b"\x05"}},
    dict(POISON, wram={0xCDA6: b"\x05"}),
    {"wram": {0xCDA6: b"\x06", 0xFF97: b"\xC2", 0xC2BA: b"\x38"}},
    {"wram": {0xCDA6: b"\x06", 0xFF97: b"\xC2", 0xC2BA: b"\x0A",
              0xCACA: b"\x00", 0xCACB: b"\x00", 0xCACC: b"\x27"}},
    {"wram": {0xCDA6: b"\x06", 0xFF97: b"\xC2", 0xC2BA: b"\x00",
              0xCACA: b"\x00", 0xCACB: b"\x00", 0xCACC: b"\x00",
              0xC27E: b"\x01\x02\x03\x04\x05"},
     "read": {0xCDA6: 1, 0xCE1A: 5, 0xCE08: 6, 0xCE0F: 5}},
]
# <<< factory AIDecide_Pokedex

# >>> factory AIDecide_ItemFinder
CONTRACT["AIDecide_ItemFinder"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_ItemFinder"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2ED: b"\x00"}),
    {"wram": {0xFF97: b"\xC2", 0xC2ED: b"\x01", 0xC27E: b"\x00", 0xC400: b"\x01"}},
]
# <<< factory AIDecide_ItemFinder

# >>> factory AIDecide_EnergyRetrieval
CONTRACT["AIDecide_EnergyRetrieval"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_EnergyRetrieval"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            0xC2EE: b"\x01",   # wPlayerDuelVariables DUELVARS_NUMBER_OF_CARDS_IN_HAND = 1
            0xC242: b"\x00",   # wPlayerDuelVariables DUELVARS_HAND[0] = deck_index 0
            0xC400: b"\x01",   # wPlayerDeck[0] = card id 1
        },
        "hram": {0xFF97: b"\xC2"},
        "expect_regs": {"a": 0xFF, "f": 0x00},
    },
]
# <<< factory AIDecide_EnergyRetrieval

# >>> factory AIDecide_SuperEnergyRetrieval
CONTRACT["AIDecide_SuperEnergyRetrieval"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_SuperEnergyRetrieval"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            0xC2EE: b"\x01",   # wPlayerDuelVariables DUELVARS_NUMBER_OF_CARDS_IN_HAND = 1
            0xC242: b"\x00",   # wPlayerDuelVariables DUELVARS_HAND[0] = deck_index 0
            0xC400: b"\x01",   # wPlayerDeck[0] = card id 1 (TYPE_ENERGY set on real ROM)
        },
        "hram": {0xFF97: b"\xC2"},
        "expect_regs": {"a": 0xFF, "f": 0x00},
    },
]
# <<< factory AIDecide_SuperEnergyRetrieval

# >>> factory AIDecide_PokemonBreeder
CONTRACT["AIDecide_PokemonBreeder"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonBreeder"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "instruction_budget": 2000000,
        "cycle_budget": 8000000,
        "wram": {0xC2EE: b"\x00"},   # wPlayerDuelVariables DUELVARS_NUMBER_OF_CARDS_IN_HAND = 0 (empty hand)
        "hram": {0xFF97: b"\xC2"},
        "expect_regs": {"a": 0x00, "f": 0x80},
    },
]
# <<< factory AIDecide_PokemonBreeder

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wce1a = 0xCE1A

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wce06 = 0xCE06
wce1a = 0xCE1A
wce1b = 0xCE1B
wAITrainerCardToPlay = 0xCE16

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wOpponentDeckID = 0xCC0E
# <<< factory-cases-statics

# >>> factory AIDecide_PokemonTrader_LegendaryMoltres
CONTRACT["AIDecide_PokemonTrader_LegendaryMoltres"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_LegendaryMoltres"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x0A",
        0xC200: b"\x00",
        0xC405: b"\x40",
        0xC40A: b"\x01",
    }, "expect": {wce1a: b"\x05"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}),
]
# <<< factory AIDecide_PokemonTrader_LegendaryMoltres

# >>> factory AIDecide_PokemonTrader_StrangePower
CONTRACT["AIDecide_PokemonTrader_StrangePower"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_StrangePower"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x0A",
        0xC200: b"\x00",
        0xC405: b"\x9B",
        0xC40A: b"\x01",
    }, "expect": {wce1a: b"\x05"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}),
]
# <<< factory AIDecide_PokemonTrader_StrangePower

# >>> factory AIDecide_PokemonTrader_LegendaryArticuno
CONTRACT["AIDecide_PokemonTrader_LegendaryArticuno"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_LegendaryArticuno"] = [
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x00",
        0xC200: b"\x00",
        wPlayerDeck: b"\x5E",
        0xC2BB: b"\xFF",
    }, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xB8",
        0xC40B: b"\xB8",
        0xC405: b"\x4B",
        0xC2BB: b"\xFF",
    }, "expect": {wce1a: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, wram={
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x00",
        0xC200: b"\x00",
        wPlayerDeck: b"\x5E",
        0xC2BB: b"\xFF",
    }, read={0xC510: 32}),
]
# <<< factory AIDecide_PokemonTrader_LegendaryArticuno

# >>> factory AIDecide_ComputerSearch_FireCharge
CONTRACT["AIDecide_ComputerSearch_FireCharge"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_ComputerSearch_FireCharge"] = [
    {"b": 0x00, "c": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xC5",
        0xC40B: b"\xDB",
        0xC405: b"\xB8",
        wAITrainerCardToPlay: b"\xFF",
    }, "expect": {wce06: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, b=0x00, c=0x00, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, read={0xC510: 32}),
]
# <<< factory AIDecide_ComputerSearch_FireCharge

# >>> factory AIDecide_ComputerSearch_Anger
CONTRACT["AIDecide_ComputerSearch_Anger"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_ComputerSearch_Anger"] = [
    {"b": 0x00, "c": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x03",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC244: b"\x0C",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC202: b"\x00",
        0xC40A: b"\xA7",
        0xC40B: b"\xC5",
        0xC40C: b"\xDB",
        0xC405: b"\xA8",
        0xC2BB: b"\xFF",
        wAITrainerCardToPlay: b"\xFF",
    }, "expect": {wce06: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, b=0x00, c=0x00, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, read={0xC510: 32}),
]
# <<< factory AIDecide_ComputerSearch_Anger

# >>> factory AIDecide_ComputerSearch_WondersOfScience
CONTRACT["AIDecide_ComputerSearch_WondersOfScience"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_ComputerSearch_WondersOfScience"] = [
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x05",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC244: b"\x0C",
        0xC245: b"\x0D",
        0xC246: b"\x0E",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC202: b"\x00",
        0xC203: b"\x00",
        0xC204: b"\x00",
        0xC40A: b"\x26",
        0xC40B: b"\x27",
        0xC40C: b"\x01",
        0xC40D: b"\x01",
        0xC40E: b"\x01",
    }, "read": {0xC510: 32}},
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xC5",
        0xC40B: b"\xDB",
        0xC405: b"\x26",
        wAITrainerCardToPlay: b"\xFF",
    }, "expect": {wce06: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, b=0x00, c=0x00, wram={
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x05",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC244: b"\x0C",
        0xC245: b"\x0D",
        0xC246: b"\x0E",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC202: b"\x00",
        0xC203: b"\x00",
        0xC204: b"\x00",
        0xC40A: b"\x26",
        0xC40B: b"\x27",
        0xC40C: b"\x01",
        0xC40D: b"\x01",
        0xC40E: b"\x01",
    }, read={0xC510: 32}),
]
# <<< factory AIDecide_ComputerSearch_WondersOfScience

# >>> factory AIDecide_ComputerSearch_RockCrusher
CONTRACT["AIDecide_ComputerSearch_RockCrusher"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_ComputerSearch_RockCrusher"] = [
    {"b": 0x00, "c": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xC5",
        0xC40B: b"\xDB",
        0xC405: b"\x7A",
        0xC2BB: b"\x06",
        0xC406: b"\x79",
        wAITrainerCardToPlay: b"\xFF",
    }, "expect": {wce06: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, b=0x00, c=0x00, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, read={0xC510: 32}),
]
# <<< factory AIDecide_ComputerSearch_RockCrusher

# >>> factory AIDecide_ComputerSearch
CONTRACT["AIDecide_ComputerSearch"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_ComputerSearch"] = [
    {"b": 0x00, "c": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}},
    {"b": 0x00, "c": 0x00, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x03",
        0xC242: b"\x14",
        0xC243: b"\x15",
        0xC244: b"\x16",
        0xC414: b"\x01",
        0xC415: b"\x01",
        0xC416: b"\x01",
        wOpponentDeckID: b"\x17",
    }, "read": {0xC510: 32}},
    dict(POISON, b=0x00, c=0x00, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}),
]
# <<< factory AIDecide_ComputerSearch

# >>> factory AIDecide_PokemonTrader_LegendaryRonald
CONTRACT["AIDecide_PokemonTrader_LegendaryRonald"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_LegendaryRonald"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xBC",
        0xC40B: b"\x76",
        0xC405: b"\x3D",
        0xC2BB: b"\xFF",
    }, "expect": {wce1a: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, read={0xC510: 32}),
]
# <<< factory AIDecide_PokemonTrader_LegendaryRonald

# >>> factory AIDecide_PokemonTrader_SoundOfTheWaves
CONTRACT["AIDecide_PokemonTrader_SoundOfTheWaves"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_SoundOfTheWaves"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x03",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC244: b"\x0C",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC202: b"\x00",
        0xC40A: b"\x51",
        0xC40B: b"\x49",
        0xC40C: b"\x49",
        0xC405: b"\x52",
        0xC2BB: b"\xFF",
    }, "expect": {wce1a: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, read={0xC510: 32}),
]
# <<< factory AIDecide_PokemonTrader_SoundOfTheWaves

# >>> factory AIDecide_PokemonTrader_LegendaryDragonite
CONTRACT["AIDecide_PokemonTrader_LegendaryDragonite"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["AIDecide_PokemonTrader_LegendaryDragonite"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2EF: b"\x01"}, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x02",
        0xC2EF: b"\x01",
        0xC242: b"\x0A",
        0xC243: b"\x0B",
        0xC200: b"\x00",
        0xC201: b"\x00",
        0xC40A: b"\xC0",
        0xC40B: b"\xC0",
        0xC405: b"\xB9",
    }, "expect": {wce1a: b"\x05"}, "read": {0xC510: 32}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2EF: b"\x01"}, read={0xC510: 32}),
]
# <<< factory AIDecide_PokemonTrader_LegendaryDragonite

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
# >>> factory-mutation AIDecide_Defender_Phase14
MUTATIONS["AIDecide_Defender_Phase14"] = {
    "source_symbol": "AIDecide_Defender_Phase14",
    "before": "\treturn (AIDecideResult){0x80u};",
    "after": "\treturn (AIDecideResult){0x10u};",
    "case_ids": ["AIDecide_Defender_Phase14-0"],
}
# <<< factory-mutation AIDecide_Defender_Phase14
MUTATIONS["AIDecide_Lass"] = {
    "source_symbol": "AIDecide_Lass",
    "before": "\t\treturn (AIDecideResult){hand_count == 0u ? 0x80u : 0x00u};",
    "after": "\t\treturn (AIDecideResult){0x00u};",
    "case_ids": ["AIDecide_Lass-3"],
}
# <<< factory-mutation AIDecide_Lass
# >>> factory-mutation AIDecide_Imakuni
MUTATIONS["AIDecide_Imakuni"] = {
    "source_symbol": "AIDecide_Imakuni",
    "before": "\treturn (AIDecideResult){0x10u};",
    "after": "\treturn (AIDecideResult){0x00u};",
    "case_ids": ["AIDecide_Imakuni-1"],
}
# <<< factory-mutation AIDecide_Imakuni# >>> factory-mutation AIDecide_Gambler
MUTATIONS["AIDecide_Gambler"] = {
    "source_symbol": "AIDecide_Gambler",
    "before": "return (AIDecideResult){(uint8_t)(remaining >= 56u ? 0x90u : 0x80u)};",
    "after": "return (AIDecideResult){0x80u};",
    "case_ids": ["AIDecide_Gambler-1"],
}
# <<< factory-mutation AIDecide_Gambler
# >>> factory-mutation AIDecide_Revive
MUTATIONS["AIDecide_Revive"] = {
    "source_symbol": "AIDecide_Revive",
    "before": "if (card == 0x88u || card == 0x87u)",
    "after": "if (card == 0x88u)",
    "case_ids": ["AIDecide_Revive-2"],
}
# <<< factory-mutation AIDecide_Revive
# >>> factory-mutation AIDecide_ImposterProfessorOak
MUTATIONS["AIDecide_ImposterProfessorOak"] = {
    "source_symbol": "AIDecide_ImposterProfessorOak",
    "before": "\tif (hand < 6u)",
    "after": "\tif (hand < 7u)",
    "case_ids": ["AIDecide_ImposterProfessorOak-1"],
}
# <<< factory-mutation AIDecide_ImposterProfessorOak
# >>> factory-mutation PickPokedexCards_Unreferenced
MUTATIONS["PickPokedexCards_Unreferenced"] = {
    "source_symbol": "PickPokedexCards_Unreferenced",
    "before": "return (PickPokedexResult){0xFFu, (uint8_t)(0x80u | 0x10u)};",
    "after": "return (PickPokedexResult){0xFFu, 0x10u};",
    "case_ids": ["PickPokedexCards_Unreferenced-0", "PickPokedexCards_Unreferenced-1"],
}
# <<< factory-mutation PickPokedexCards_Unreferenced
# >>> factory-mutation AIDecide_Recycle
MUTATIONS["AIDecide_Recycle"] = {
    "source_symbol": "AIDecide_Recycle",
    "before": "\tif (discard.f & 0x10u)\n\t\treturn (AIDecideResult){0x80u};",
    "after": "\tif (discard.f & 0x10u)\n\t\treturn (AIDecideResult){0x00u};",
    "case_ids": ["AIDecide_Recycle-0", "AIDecide_Recycle-1"],
}
# <<< factory-mutation AIDecide_Recycle

# >>> factory-mutation AIDecide_ClefairyDollOrMysteriousFossil
MUTATIONS["AIDecide_ClefairyDollOrMysteriousFossil"] = {
    "source_symbol": "AIDecide_ClefairyDollOrMysteriousFossil",
    "before": "uint8_t count = GetTurnDuelistVariable(0xEFu).a;\n\tif (count >= 6u)",
    "after": "uint8_t count = GetTurnDuelistVariable(0xEFu).a;\n\tif (count > 6u)",
    "case_ids": ["AIDecide_ClefairyDollOrMysteriousFossil-0", "AIDecide_ClefairyDollOrMysteriousFossil-1"],
}
# <<< factory-mutation AIDecide_ClefairyDollOrMysteriousFossil
# >>> factory-mutation AIDecide_PokemonFlute
MUTATIONS["AIDecide_PokemonFlute"] = {
    "source_symbol": "AIDecide_PokemonFlute",
    "before": "uint8_t count = GetNonTurnDuelistVariable(0xEFu).a;\n\tif (count >= 6u)",
    "after": "uint8_t count = GetNonTurnDuelistVariable(0xEFu).a;\n\tif (count > 6u)",
    "case_ids": ["AIDecide_PokemonFlute-0", "AIDecide_PokemonFlute-1"],
}
# <<< factory-mutation AIDecide_PokemonFlute
# >>> factory-mutation PickPokedexCards
MUTATIONS["PickPokedexCards"] = {
    "source_symbol": "PickPokedexCards",
    "before": "return (PickPokedexResult){0xFFu, 0x90u};",
    "after": "return (PickPokedexResult){0xFFu, 0x10u};",
    "case_ids": ["PickPokedexCards-0", "PickPokedexCards-1"],
}
# <<< factory-mutation PickPokedexCards
# Keep schema-2 inventory after appended routine cases.
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation AIDecide_Pokedex
MUTATIONS["AIDecide_Pokedex"] = {"source_symbol": "AIDecide_Pokedex", "before": "\tif (counter < 6u)", "after": "\tif (counter < 5u)", "case_ids": ["AIDecide_Pokedex-0"]}
# <<< factory-mutation AIDecide_Pokedex
# >>> factory-mutation AIDecide_ItemFinder
MUTATIONS["AIDecide_ItemFinder"] = {"source_symbol": "AIDecide_ItemFinder", "before": "return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 0u ? 0x80u : 0u)};", "after": "return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 1u ? 0x80u : 0u)};", "case_ids": ["AIDecide_ItemFinder-0", "AIDecide_ItemFinder-1"]}
# <<< factory-mutation AIDecide_ItemFinder
# >>> factory-mutation AIDecide_EnergyRetrieval
MUTATIONS["AIDecide_EnergyRetrieval"] = {
    "source_symbol": "AIDecide_EnergyRetrieval",
    "before": "return (AIDecideEnergyRetrievalResult){dup.a, 0x00u};",
    "after": "return (AIDecideEnergyRetrievalResult){0u, 0x00u};",
    "case_ids": ["AIDecide_EnergyRetrieval-0"],
}
# <<< factory-mutation AIDecide_EnergyRetrieval
# >>> factory-mutation AIDecide_SuperEnergyRetrieval
MUTATIONS["AIDecide_SuperEnergyRetrieval"] = {
    "source_symbol": "AIDecide_SuperEnergyRetrieval",
    "before": "return (AIDecideSuperEnergyRetrievalResult){dup1.a, 0x00u};",
    "after": "return (AIDecideSuperEnergyRetrievalResult){0u, 0x00u};",
    "case_ids": ["AIDecide_SuperEnergyRetrieval-0"],
}
# <<< factory-mutation AIDecide_SuperEnergyRetrieval
# >>> factory-mutation AIDecide_PokemonBreeder
MUTATIONS["AIDecide_PokemonBreeder"] = {
    "source_symbol": "AIDecide_PokemonBreeder",
    "before": "if (wce06 == 0u)\n\t\treturn (AIDecidePokemonBreederResult){0u, 0x80u};",
    "after": "if (wce06 == 0u)\n\t\treturn (AIDecidePokemonBreederResult){0u, 0x00u};",
    "case_ids": ["AIDecide_PokemonBreeder-0"],
}
# <<< factory-mutation AIDecide_PokemonBreeder
# >>> factory-mutation AIDecide_PokemonTrader_LegendaryMoltres
MUTATIONS["AIDecide_PokemonTrader_LegendaryMoltres"] = {"source_symbol": "AIDecide_PokemonTrader_LegendaryMoltres", "before": "\t\tuint8_t f = (r.a == 0u) ? 0x80u : 0u;", "after": "\t\tuint8_t f = (r.a == 0u) ? 0x80u : 0x40u;", "case_ids": ["AIDecide_PokemonTrader_LegendaryMoltres-0"]}
# <<< factory-mutation AIDecide_PokemonTrader_LegendaryMoltres
# >>> factory-mutation AIDecide_PokemonTrader_StrangePower
MUTATIONS["AIDecide_PokemonTrader_StrangePower"] = {"source_symbol": "AIDecide_PokemonTrader_StrangePower", "before": '\tLookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MR_MIME, MR_MIME);\n\tif (!(r.f & 0x10u)) {\n\t\tuint8_t f = (r.a == 0u) ? 0x80u : 0u;', "after": '\tLookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MR_MIME, MR_MIME);\n\tif (!(r.f & 0x10u)) {\n\t\tuint8_t f = (r.a == 0u) ? 0x80u : 0x40u;', "case_ids": ["AIDecide_PokemonTrader_StrangePower-0"]}
# <<< factory-mutation AIDecide_PokemonTrader_StrangePower
# >>> factory-mutation AIDecide_PokemonTrader_LegendaryArticuno
MUTATIONS["AIDecide_PokemonTrader_LegendaryArticuno"] = {"source_symbol": "AIDecide_PokemonTrader_LegendaryArticuno", "before": "\tCheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(CHANSEY);", "after": "\tCheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(DITTO);", "case_ids": ["AIDecide_PokemonTrader_LegendaryArticuno-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_LegendaryArticuno
# >>> factory-mutation AIDecide_ComputerSearch_FireCharge
MUTATIONS["AIDecide_ComputerSearch_FireCharge"] = {"source_symbol": "AIDecide_ComputerSearch_FireCharge", "before": '\tLookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, target);\n\tif (!(loc.f & 0x10u)) {\n\t\tuint8_t f = (loc.a == 0u) ? 0x80u : 0u;', "after": '\tLookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, target);\n\tif (!(loc.f & 0x10u)) {\n\t\tuint8_t f = (loc.a == 0u) ? 0x80u : 0x40u;', "case_ids": ["AIDecide_ComputerSearch_FireCharge-0"]}
# <<< factory-mutation AIDecide_ComputerSearch_FireCharge
# >>> factory-mutation AIDecide_ComputerSearch_Anger
MUTATIONS["AIDecide_ComputerSearch_Anger"] = {"source_symbol": "AIDecide_ComputerSearch_Anger", "before": "\treturn (AIDecide_ComputerSearch_AngerResult){wce06, 0x90u};", "after": "\treturn (AIDecide_ComputerSearch_AngerResult){wce06, 0x00u};", "case_ids": ["AIDecide_ComputerSearch_Anger-1"]}
# <<< factory-mutation AIDecide_ComputerSearch_Anger
# >>> factory-mutation AIDecide_ComputerSearch_WondersOfScience
MUTATIONS["AIDecide_ComputerSearch_WondersOfScience"] = {"source_symbol": "AIDecide_ComputerSearch_WondersOfScience", "before": "\treturn (AIDecide_ComputerSearch_WondersOfScienceResult){wce06, 0x90u};", "after": "\treturn (AIDecide_ComputerSearch_WondersOfScienceResult){wce06, 0x00u};", "case_ids": ["AIDecide_ComputerSearch_WondersOfScience-1"]}
# <<< factory-mutation AIDecide_ComputerSearch_WondersOfScience
# >>> factory-mutation AIDecide_ComputerSearch_RockCrusher
MUTATIONS["AIDecide_ComputerSearch_RockCrusher"] = {"source_symbol": "AIDecide_ComputerSearch_RockCrusher", "before": '\t\t\t\tif (gb_read8(wce1b_ADDR) != 0xFFu)\n\t\t\t\t\treturn (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u};\n\t\t\t\tcontinue;', "after": '\t\t\t\tif (gb_read8(wce1b_ADDR) != 0xFFu)\n\t\t\t\t\treturn (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x00u};\n\t\t\t\tcontinue;', "case_ids": ["AIDecide_ComputerSearch_RockCrusher-1"]}
# <<< factory-mutation AIDecide_ComputerSearch_RockCrusher
# >>> factory-mutation AIDecide_ComputerSearch
MUTATIONS["AIDecide_ComputerSearch"] = {"source_symbol": "AIDecide_ComputerSearch", "before": "\tif (deck_id == FIRE_CHARGE_DECK_ID) {", "after": "\tif (deck_id == ANGER_DECK_ID) {", "case_ids": ["AIDecide_ComputerSearch-1"]}
# <<< factory-mutation AIDecide_ComputerSearch
# >>> factory-mutation AIDecide_PokemonTrader_LegendaryRonald
MUTATIONS["AIDecide_PokemonTrader_LegendaryRonald"] = {"source_symbol": "AIDecide_PokemonTrader_LegendaryRonald", "before": "\t\tLookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(ZAPDOS_LV68);", "after": "\t\tLookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(ARTICUNO_LV37);", "case_ids": ["AIDecide_PokemonTrader_LegendaryRonald-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_LegendaryRonald
# >>> factory-mutation AIDecide_PokemonTrader_SoundOfTheWaves
MUTATIONS["AIDecide_PokemonTrader_SoundOfTheWaves"] = {"source_symbol": "AIDecide_PokemonTrader_SoundOfTheWaves", "before": "\t\th = CheckIfHasCardIDInHand(TENTACOOL);", "after": "\t\th = CheckIfHasCardIDInHand(SEADRA);", "case_ids": ["AIDecide_PokemonTrader_SoundOfTheWaves-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_SoundOfTheWaves
# >>> factory-mutation AIDecide_PokemonTrader_LegendaryDragonite
MUTATIONS["AIDecide_PokemonTrader_LegendaryDragonite"] = {"source_symbol": "AIDecide_PokemonTrader_LegendaryDragonite", "before": "\t\tCheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(DRAGONAIR);", "after": "\t\tCheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(GYARADOS);", "case_ids": ["AIDecide_PokemonTrader_LegendaryDragonite-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_LegendaryDragonite
