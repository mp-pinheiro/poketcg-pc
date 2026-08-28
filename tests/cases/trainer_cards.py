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
        "expect_regs": {"a": 0xFF, "f": 0x80},
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
        "expect_regs": {"a": 0xFF, "f": 0x80},
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
        "wram": {0xC2EE: b"\x00", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF"},
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

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wPlayerDuelVariables = 0xC200
DUELVARS_ARENA_CARD = 0xBB
DUELVARS_ARENA_CARD_HP = 0xC8
DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA = 0xEF
wce06 = 0xCE06
wce08 = 0xCE08
IVYSAUR = 0x09

hWhoseTurn = 0xFF97

hWhoseTurn = 0xFF97
wOpponentDeckID = 0xCC0E

wDuelTempList = 0xC510
wOpponentDeckID = 0xCC0E
hWhoseTurn = 0xFF97

wAITrainerCardPhase = 0xCE18

hTempCardIndex_ff9f = 0xFF9F
hTemp_ffa0 = 0xFFA0
wAITrainerCardParameter = 0xCE19
wAITrainerCardToPlay = 0xCE16
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
BUDGET = dict(instruction_budget=20000000, cycle_budget=80000000)

hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wPlayerCardLocations = 0xC200
wPlayerArenaCard = 0xC2BB
wPlayerBench = 0xC2BC
wOpponentCardLocations = 0xC300
wOpponentArenaCard = 0xC3BB
wOpponentArenaCardHP = 0xC3C8
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDamage = 0xCCB9
wAIMinDamage = 0xCCBB
wAIMaxDamage = 0xCCBC
wSelectedAttack = 0xCCC6
wce06 = 0xCE06

def _defender13_case(location=b"\x00", extra=None, **overrides):
    wram = {
        hWhoseTurn: b"\xC2",
        hTempPlayAreaLocation_ff9d: location,
        wPlayerCardLocations: b"\x10",
        wOpponentCardLocations: b"\x10",
        wPlayerArenaCard: b"\x00",
        wOpponentArenaCard: b"\x00",
        wPlayerDeck: b"\xBE",
        wOpponentDeck: b"\xBE",
        wOpponentArenaCardHP: b"\x00",
        wDamage: b"\x00",
        wAIMinDamage: b"\x00",
        wAIMaxDamage: b"\x00",
        wSelectedAttack: b"\x00",
        wce06: b"\x00",
    }
    if extra:
        wram.update(extra)
    case = {
        "wram": wram,
        "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
        "instruction_budget": 40000000,
        "cycle_budget": 160000000,
        "read": {hTempPlayAreaLocation_ff9d: 1, wDamage: 1, wSelectedAttack: 1, wce06: 1},
    }
    case.update(overrides)
    return case

hWhoseTurn = 0xFF97
wAIPlayEnergyCardForRetreat = 0xCDD7
ARENA_VARS = 0xC200
ARENA_CARD = 0xC2BB
ARENA_COUNT = 0xC2EF
PLAYER_DECK = 0xC400

hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D

wArena = 0xC2BB
wOpponentArena = 0xC3BB
wScratch = 0xCE00

hWhoseTurn = 0xFF97
ARENA_CARD = 0xC2BB
ARENA_COUNT = 0xC2EF
PLAYER_DECK = 0xC400
hTempPlayAreaLocation_ff9d = 0xFF9D
wce06 = 0xCE06
wce08 = 0xCE08
wce0f = 0xCE0F
wTotalAttachedEnergies = 0xCC23

_pp13_hWhoseTurn = 0xFF97
_pp13_hTempPlayAreaLocation_ff9d = 0xFF9D
_pp13_wPlayerCardLocations = 0xC200
_pp13_wPlayerArenaCard = 0xC2BB
_pp13_wOpponentCardLocations = 0xC300
_pp13_wOpponentArenaCard = 0xC3BB
_pp13_wOpponentArenaCardHP = 0xC3C8
_pp13_wPlayerDeck = 0xC400
_pp13_wOpponentDeck = 0xC480
_pp13_wDamage = 0xCCB9
_pp13_wAIMinDamage = 0xCCBB
_pp13_wAIMaxDamage = 0xCCBC
_pp13_wTempTurnDuelistCardID = 0xCCC3
_pp13_wTempNonTurnDuelistCardID = 0xCCC4
_pp13_wSelectedAttack = 0xCCC6
_pp13_SNORLAX = 0xBE
_pp13_CARD_LOCATION_ARENA = 0x10

# Same landed seed shape as tests/cases/core.py's _kaod_case, which is what
# CheckIfAnyAttackKnocksOutDefendingCard itself is measured green with.  The
# defending card's HP at $C3C8 MUST stay 0x00 in every case: the `sub [hl]`
# inside CheckIfAnyAttackKnocksOutDefendingCard then resolves on the FIRST
# attack (borrow when the estimate is non-zero, zero when it is not), so the
# reference ROM returns after exactly one EstimateDamage_VersusDefendingCard
# call.  Any non-zero HP lets that subtraction fall through to SECOND_ATTACK
# and the reference blows the 240-frame oracle limit.
def _pp13_case(location=b"\x00", **overrides):
    wram = {
        _pp13_hWhoseTurn: b"\xC2",
        _pp13_hTempPlayAreaLocation_ff9d: location,
        _pp13_wPlayerCardLocations: bytes((_pp13_CARD_LOCATION_ARENA,)),
        _pp13_wOpponentCardLocations: bytes((_pp13_CARD_LOCATION_ARENA,)),
        _pp13_wPlayerArenaCard: b"\x00",
        _pp13_wOpponentArenaCard: b"\x00",
        _pp13_wPlayerDeck: bytes((_pp13_SNORLAX,)),
        _pp13_wOpponentDeck: bytes((_pp13_SNORLAX,)),
        _pp13_wOpponentArenaCardHP: b"\x00",
        _pp13_wDamage: b"\x00\x00",
        _pp13_wAIMinDamage: b"\x00",
        _pp13_wAIMaxDamage: b"\x00",
        _pp13_wTempTurnDuelistCardID: b"\x00",
        _pp13_wTempNonTurnDuelistCardID: b"\x00",
        _pp13_wSelectedAttack: b"\x00",
    }
    case = {
        "wram": wram,
        "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
        "instruction_budget": 40000000,
        "cycle_budget": 160000000,
        "read": {
            _pp13_hTempPlayAreaLocation_ff9d: 1,
            _pp13_wDamage: 2,
            _pp13_wTempTurnDuelistCardID: 2,
            _pp13_wSelectedAttack: 1,
        },
    }
    case.update(overrides)
    return case

hTempCardIndex_ff9f = 0xFF9F
wAITrainerCardToPlay = 0xCE16
wCurrentAIFlags = 0xCE21
wOpponentDeckID = 0xCC0E
wRNG1 = 0xCACA
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
BUDGET = dict(instruction_budget=20000000, cycle_budget=80000000)

hTempPlayAreaLocation_ffa1 = 0xFFA1
hTempRetreatCostCards = 0xFFA2

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
hTempPlayAreaLocation_ff9d = 0xFF9D
wSelectedAttack = 0xCCC6
wTotalAttachedEnergies = 0xCC23
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

# >>> factory AIDecide_Pokeball
CONTRACT["AIDecide_Pokeball"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_Pokeball"] = [
    {"wram": {wOpponentDeckID: b"\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x17", 0xC405: b"\xB8"}, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        wOpponentDeckID: b"\x28",
        0xC2EE: b"\x01",
        0xC242: b"\x0A",
        0xC200: b"\x00",
        0xC40A: b"\x02",
        0xC405: b"\x30",
    }, "read": {0xC510: 32}},
    {"wram": {
        hWhoseTurn: b"\xC2",
        wOpponentDeckID: b"\x2F",
        0xC2EE: b"\x01",
        0xC242: b"\x0A",
        0xC200: b"\x00",
        0xC40A: b"\x17",
        0xC405: b"\x18",
        0xC2BB: b"\xFF",
    }, "read": {0xC510: 32}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x17", 0xC405: b"\xB8"}, read={0xC510: 32}),
]
# <<< factory AIDecide_Pokeball

# >>> factory AIDecide_MrFuji
CONTRACT["AIDecide_MrFuji"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["AIDecide_MrFuji"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA: b"\x01"},
     "read": {wce06: 1, wce08: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2",
                       wPlayerDuelVariables + DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA: b"\x02",
                       wPlayerDuelVariables + DUELVARS_ARENA_CARD + 1: b"\x01",
                       wPlayerDeck + 1: bytes((IVYSAUR,)),
                       wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP + 1: b"\x10"},
         read={wce06: 1, wce08: 1}),
    {"wram": {hWhoseTurn: b"\xC2",
              wPlayerDuelVariables + DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA: b"\x02",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD + 1: b"\x01",
              wPlayerDeck + 1: bytes((IVYSAUR,)),
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP + 1: b"\x00"},
     "read": {wce06: 1, wce08: 1}},
]
# <<< factory AIDecide_MrFuji

# >>> factory AIDecide_PokemonTrader_BlisteringPokemon
CONTRACT["AIDecide_PokemonTrader_BlisteringPokemon"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonTrader_BlisteringPokemon"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}),
]
# <<< factory AIDecide_PokemonTrader_BlisteringPokemon

# >>> factory AIDecide_PokemonTrader_Flamethrower
CONTRACT["AIDecide_PokemonTrader_Flamethrower"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonTrader_Flamethrower"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}),
]
# <<< factory AIDecide_PokemonTrader_Flamethrower

# >>> factory AIDecide_PokemonTrader_FlowerGarden
CONTRACT["AIDecide_PokemonTrader_FlowerGarden"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonTrader_FlowerGarden"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}),
]
# <<< factory AIDecide_PokemonTrader_FlowerGarden

# >>> factory AIDecide_PokemonTrader_PowerGenerator
CONTRACT["AIDecide_PokemonTrader_PowerGenerator"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonTrader_PowerGenerator"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory AIDecide_PokemonTrader_PowerGenerator

# >>> factory AIDecide_PokemonTrader
CONTRACT["AIDecide_PokemonTrader"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PokemonTrader"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wOpponentDeckID: b"\xFF"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wOpponentDeckID: b"\x0C"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wOpponentDeckID: b"\xFF"}),
]
# <<< factory AIDecide_PokemonTrader

# >>> factory AIDecide_EnergySearch
CONTRACT["AIDecide_EnergySearch"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_EnergySearch"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000,
     "wram": {hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x00", 0xC200: b"\x01" * 0x3C},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wOpponentDeckID: b"\x00", 0xC200: b"\x01" * 0x3C},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory AIDecide_EnergySearch

# >>> factory _AIProcessHandTrainerCards
CONTRACT["_AIProcessHandTrainerCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_AIProcessHandTrainerCards"] = [
    {"a": 0x00, "wram": {wAITrainerCardPhase: b"\x00"}, "expect": {wAITrainerCardPhase: b"\x00"}},
    dict(POISON, a=0x00, wram={wAITrainerCardPhase: b"\x00"}, expect={wAITrainerCardPhase: b"\x00"}),
]
# <<< factory _AIProcessHandTrainerCards

# >>> factory AIPlay_Pokeball
CONTRACT["AIPlay_Pokeball"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Pokeball"] = [
    {"a": 0x00, "wram": {0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x00"}, "read": {0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0x00, "wram": {0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x78", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x80"}, "read": {0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\xDD", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AIPlay_Pokeball

# >>> factory AIPlay_Recycle
CONTRACT["AIPlay_Recycle"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Recycle"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x78", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x80"}, read={hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\xDD", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Recycle

# >>> factory AIPlay_Bill
CONTRACT["AIPlay_Bill"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Bill"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Bill
# >>> factory AIPlay_Defender
CONTRACT["AIPlay_Defender"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Defender"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Defender
# >>> factory AIPlay_Imakuni
CONTRACT["AIPlay_Imakuni"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Imakuni"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Imakuni
# >>> factory AIPlay_FullHeal
CONTRACT["AIPlay_FullHeal"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_FullHeal"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_FullHeal
# >>> factory AIPlay_ClefairyDollOrMysteriousFossil
CONTRACT["AIPlay_ClefairyDollOrMysteriousFossil"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_ClefairyDollOrMysteriousFossil"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_ClefairyDollOrMysteriousFossil
# >>> factory AIPlay_ImposterProfessorOak
CONTRACT["AIPlay_ImposterProfessorOak"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_ImposterProfessorOak"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_ImposterProfessorOak
# >>> factory AIPlay_PokemonCenter
CONTRACT["AIPlay_PokemonCenter"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_PokemonCenter"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={hTempCardIndex_ff9f: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_PokemonCenter

# >>> factory AIDecide_PlusPower_Phase14
CONTRACT["AIDecide_PlusPower_Phase14"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_PlusPower_Phase14"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCCC6: b"\x00", 0xCC23: b"\x00"}, "sram": {0: {}}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCCC6: b"\x00", 0xCC23: b"\x00"}, "sram": {0: {}}, "instruction_budget": 20000000, "cycle_budget": 80000000, **POISON},
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCCC6: b"\x00", 0xCC23: b"\x00"}, "sram": {0: {}}, "instruction_budget": 20000000, "cycle_budget": 80000000, **POISON},
]
# <<< factory AIDecide_PlusPower_Phase14

# >>> factory AIDecide_GustOfWind
CONTRACT["AIDecide_GustOfWind"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_GustOfWind"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x03", 0xCE20: b"\x10"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01"}),
]
# <<< factory AIDecide_GustOfWind

# >>> factory AIDecide_Defender_Phase13
CONTRACT["AIDecide_Defender_Phase13"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_Defender_Phase13"] = [
    _defender13_case(),
    _defender13_case(b"\x01"),
    dict(POISON, **_defender13_case()),
]
# <<< factory AIDecide_Defender_Phase13

# >>> factory AIDecide_Switch
CONTRACT["AIDecide_Switch"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_Switch"] = [
    {"wram": {hWhoseTurn: b"\xC2", wAIPlayEnergyCardForRetreat: b"\x00", ARENA_COUNT: b"\x01", ARENA_CARD: b"\x00", PLAYER_DECK: b"\x01", 0xC2C1: b"\xFF", ARENA_VARS: b"\x10"}, "instruction_budget": 5000000, "cycle_budget": 20000000},
    {"wram": {hWhoseTurn: b"\xC2", wAIPlayEnergyCardForRetreat: b"\x01", ARENA_COUNT: b"\x01", ARENA_CARD: b"\x00", PLAYER_DECK: b"\x01", 0xC2C1: b"\xFF", ARENA_VARS: b"\x10"}, "instruction_budget": 5000000, "cycle_budget": 20000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wAIPlayEnergyCardForRetreat: b"\x00", ARENA_COUNT: b"\x01", ARENA_CARD: b"\x00", PLAYER_DECK: b"\x01", 0xC2C1: b"\xFF", ARENA_VARS: b"\x10"}, instruction_budget=5000000, cycle_budget=20000000),
]
# <<< factory AIDecide_Switch

# >>> factory AIDecide_SuperEnergyRemoval
CONTRACT["AIDecide_SuperEnergyRemoval"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_SuperEnergyRemoval"] = [
    {"wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC2BB: b"\xFF\xFF\xFF\xFF\xFF", 0xC510: b"\xFF"}, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC2BB: b"\xFF\xFF\xFF\xFF\xFF", 0xC510: b"\xFF"}, keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory AIDecide_SuperEnergyRemoval

# >>> factory AIDecide_ScoopUp
CONTRACT["AIDecide_ScoopUp"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_ScoopUp"] = [
    {"wram": {0xFF97: b"\xC5", 0xC5EF: b"\x01"}, "read": {0xFF9D: 1}, "expect_regs": {"a": 1, "f": 0}, "expect": {0xFF9D: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC5", 0xC5EF: b"\x01"}, read={0xFF9D: 1}, expect_regs={"a": 1, "f": 0}, expect={0xFF9D: b"\x00"}),
    {"wram": {0xFF97: b"\xC5", 0xC5EF: b"\x00"}, "read": {0xFF9D: 1}, "expect_regs": {"a": 0, "f": 0x80}, "expect": {0xFF9D: b"\x00"}},
]
# <<< factory AIDecide_ScoopUp

# >>> factory AIDecide_FullHeal
CONTRACT["AIDecide_FullHeal"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_FullHeal"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F0: b"\x04"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F0: b"\x04"}),
]
# <<< factory AIDecide_FullHeal

# >>> factory AIDecide_EnergyRemoval
CONTRACT["AIDecide_EnergyRemoval"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_EnergyRemoval"] = [
    {"wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC2BB: b"\xFF" * 60, 0xC3BB: b"\xFF" * 60}, "read": {0xCE0F: 1, 0xCE1A: 1, 0xCC23: 1, 0xFF9D: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC2BB: b"\xFF" * 60, 0xC3BB: b"\xFF" * 60}, read={0xCE0F: 1, 0xCE1A: 1, 0xCC23: 1, 0xFF9D: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AIDecide_EnergyRemoval

# >>> factory AIDecide_PokemonCenter
CONTRACT["AIDecide_PokemonCenter"] = {"compare": ("f",), "preserve": ()}
CASES["AIDecide_PokemonCenter"] = [
    {"wram": {hWhoseTurn: b"\xC2", ARENA_COUNT: b"\x01", ARENA_CARD: b"\x00", PLAYER_DECK: b"\x01"},
     "read": {hTempPlayAreaLocation_ff9d: 1, wce06: 1, wce08: 1, wce0f: 1, wTotalAttachedEnergies: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", ARENA_COUNT: b"\x01", ARENA_CARD: b"\x00", PLAYER_DECK: b"\x01"},
         read={hTempPlayAreaLocation_ff9d: 1, wce06: 1, wce08: 1, wce0f: 1, wTotalAttachedEnergies: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AIDecide_PokemonCenter

# >>> factory AIDecide_PlusPower_Phase13
CONTRACT["AIDecide_PlusPower_Phase13"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_PlusPower_Phase13"] = [
    _pp13_case(),
    dict(POISON, **_pp13_case()),
    _pp13_case(location=b"\x01"),
]
# <<< factory AIDecide_PlusPower_Phase13

# >>> factory AIPlay_PlusPower
CONTRACT["AIPlay_PlusPower"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_PlusPower"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={0xFF9F: 1, 0xCDD6: 1, 0xCE21: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE21: b"\x80", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={0xFF9F: 1, 0xCDD6: 1, 0xCE21: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCE21: b"\xAA", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"},
         read={0xFF9F: 1, 0xCDD6: 1, 0xCE21: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_PlusPower

# >>> factory AIPlay_Potion
CONTRACT["AIPlay_Potion"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Potion"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\x00", 0xCE19: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\x77", 0xCE19: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC2BC: b"\x00", 0xC2C9: b"\xC0", 0xC400: b"\x01", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\x00", 0xCE19: b"\x01", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC2BC: b"\x00", 0xC2C9: b"\xC0", 0xC400: b"\x01", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Potion

# >>> factory AIPlay_GustOfWind
CONTRACT["AIPlay_GustOfWind"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_GustOfWind"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE21: b"\x0F", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x80"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_GustOfWind

# >>> factory AIPlay_Switch
CONTRACT["AIPlay_Switch"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Switch"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE21: b"\x00", 0xCDB4: b"\x55", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1, 0xCDB4: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\xA5", 0xCE21: b"\x01", 0xCDB4: b"\xAA", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1, 0xCDB4: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xEE", 0xCE21: b"\x00", 0xCDB4: b"\x99", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1, 0xCDB4: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Switch

# >>> factory AIPlay_Maintenance
CONTRACT["AIPlay_Maintenance"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Maintenance"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE1A: b"\x34", 0xCE1B: b"\x00", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE1A: b"\x78", 0xCE1B: b"\x02", 0xCE21: b"\x10", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE1A: b"\xDD", 0xCE1B: b"\xEE", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Maintenance

# >>> factory AIPlay_ComputerSearch
CONTRACT["AIPlay_ComputerSearch"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_ComputerSearch"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE1A: b"\x34", 0xCE1B: b"\x00", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA2: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE1A: b"\x78", 0xCE1B: b"\x02", 0xCE21: b"\x10", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x80"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA2: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCE1A: b"\xDD", 0xCE1B: b"\xEE", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA2: 1, 0xFFA0: 1, 0xFFA1: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_ComputerSearch

# >>> factory AIPlay_ItemFinder
CONTRACT["AIPlay_ItemFinder"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_ItemFinder"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE1A: b"\x56", 0xCE1B: b"\x02", 0xCE21: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE1A: b"\x12", 0xCE1B: b"\x03", 0xCE21: b"\x80", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCE1A: b"\xDD", 0xCE1B: b"\xEE", 0xCE21: b"\xAA", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_ItemFinder

# >>> factory AIPlay_Pokedex
CONTRACT["AIPlay_Pokedex"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Pokedex"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE1A: b"\x34", 0xCE1B: b"\x00", 0xCE1C: b"\x01", 0xCE1D: b"\x02", 0xCE1E: b"\x03", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 7}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE1A: b"\x78", 0xCE1B: b"\x02", 0xCE1C: b"\x04", 0xCE1D: b"\x05", 0xCE1E: b"\x06", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 7}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xEE", 0xCE1A: b"\xDD", 0xCE1B: b"\xEE", 0xCE1C: b"\xDD", 0xCE1D: b"\xEE", 0xCE1E: b"\xDD", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 7}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Pokedex

# >>> factory AIPlay_Gambler
CONTRACT["AIPlay_Gambler"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_Gambler"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE21: b"\x00", 0xCC0E: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCBF9: b"\x01"}, read={0xCE21: 1, 0xFF9F: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE21: b"\x10", 0xCC0E: b"\x2A", 0xCACA: b"\x12\x34\x56", 0xCBF9: b"\x01"}, read={0xCE21: 1, 0xFF9F: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, a=0xAA, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE21: b"\x00", 0xCC0E: b"\x00", 0xCACA: b"\xAA\xBB\xCC", 0xCBF9: b"\x01"}, read={0xCE21: 1, 0xFF9F: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_Gambler

# >>> factory AIPlay_EnergyRetrieval
CONTRACT["AIPlay_EnergyRetrieval"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_EnergyRetrieval"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCE1A: b"\x02", 0xCE1B: b"\xFF", 0xCE21: b"\x01", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00", 0xFFA3: b"\x55"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1, 0xFFA3: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x78", 0xCE1A: b"\x00", 0xCE1B: b"\x02", 0xCE21: b"\x20", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x80", 0xFFA3: b"\xAA"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1, 0xFFA3: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCE1A: b"\xEE", 0xCE1B: b"\xFF", 0xCE21: b"\xBB", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00", 0xFFA3: b"\xCC"}, read={0xCE21: 1, 0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 1, 0xFFA3: 1}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_EnergyRetrieval

# >>> factory AIPlay_SuperEnergyRemoval
CONTRACT["AIPlay_SuperEnergyRemoval"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_SuperEnergyRemoval"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\x12", 0xCE19: b"\x34", 0xCE1A: b"\x56", 0xCE1B: b"\x78", 0xCE1C: b"\x9A", 0xCE1D: b"\xBC", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 4}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\x77", 0xCE19: b"\x44", 0xCE1A: b"\x02", 0xCE1B: b"\x05", 0xCE1C: b"\x06", 0xCE1D: b"\x07", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x80"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 4}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
    dict(POISON, wram={0xFF80: b"\x08", 0xFF97: b"\xC2", 0xCE16: b"\xDD", 0xCE19: b"\xEE", 0xCE1A: b"\xCC", 0xCE1B: b"\xBB", 0xCE1C: b"\xAA", 0xCE1D: b"\x99", 0xCABB: b"\x00", 0xCBF9: b"\x01", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1, 0xFFA1: 1, 0xFFA2: 4}, keys=[0x00, 0x01], setup=SETUP, **BUDGET),
]
# <<< factory AIPlay_SuperEnergyRemoval

# >>> factory AIDecide_SuperPotion_Phase11
CONTRACT["AIDecide_SuperPotion_Phase11"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecide_SuperPotion_Phase11"] = [{"wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC2C8: b"\x00", 0xCC23: b"\x00"}, "read": {0xFF9D: 1, 0xCCC6: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000}, {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC2C8: b"\x00", 0xCC23: b"\x00"}, "read": {0xFF9D: 1, 0xCCC6: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000}]
# <<< factory AIDecide_SuperPotion_Phase11

# >>> factory AIPlay_EnergySearch
CONTRACT["AIPlay_EnergySearch"] = {"compare": ("f",), "preserve": ()}
CASES["AIPlay_EnergySearch"] = [
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x00", 0xCE19: b"\x34", 0xCBF9: b"\x01", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, instruction_budget=20000000, cycle_budget=80000000),
    dict(a=0x00, wram={0xFF80: b"\x08", 0xCE16: b"\x77", 0xCE19: b"\x34", 0xCBF9: b"\x01", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, wram={0xFF80: b"\x08", 0xCE16: b"\xDD", 0xCE19: b"\xDD", 0xCBF9: b"\x01", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00"}, read={0xFF9F: 1, 0xFFA0: 1}, keys=[0x00, 0x01], setup=SETUP, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AIPlay_EnergySearch

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
    "before": "return (AIDecideEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u)};",
    "after": "return (AIDecideEnergyRetrievalResult){hand_energy.a, 0u};",
    "case_ids": ["AIDecide_EnergyRetrieval-0"],
}
# <<< factory-mutation AIDecide_EnergyRetrieval
# >>> factory-mutation AIDecide_SuperEnergyRetrieval
MUTATIONS["AIDecide_SuperEnergyRetrieval"] = {
    "source_symbol": "AIDecide_SuperEnergyRetrieval",
    "before": "return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u)};",
    "after": "return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, 0u};",
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
# >>> factory-mutation AIDecide_Pokeball
MUTATIONS["AIDecide_Pokeball"] = {"source_symbol": "AIDecide_Pokeball", "before": "\t\tr = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHANSEY);", "after": "\t\tr = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, TAUROS);", "case_ids": ["AIDecide_Pokeball-1"]}
# <<< factory-mutation AIDecide_Pokeball
# >>> factory-mutation AIDecide_MrFuji
MUTATIONS["AIDecide_MrFuji"] = {"source_symbol": "AIDecide_MrFuji", "before": "return (AIDecideResult){0xC0u};\n\n\tuint8_t d", "after": "return (AIDecideResult){0x10u};\n\n\tuint8_t d", "case_ids": ["AIDecide_MrFuji-0"]}
# <<< factory-mutation AIDecide_MrFuji
# >>> factory-mutation AIDecide_PokemonTrader_BlisteringPokemon
MUTATIONS["AIDecide_PokemonTrader_BlisteringPokemon"] = {"source_symbol": "AIDecide_PokemonTrader_BlisteringPokemon", "before": "a = r6.a;", "after": "a = 0u;", "case_ids": ["AIDecide_PokemonTrader_BlisteringPokemon-0", "AIDecide_PokemonTrader_BlisteringPokemon-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_BlisteringPokemon
# >>> factory-mutation AIDecide_PokemonTrader_Flamethrower
MUTATIONS["AIDecide_PokemonTrader_Flamethrower"] = {"source_symbol": "AIDecide_PokemonTrader_Flamethrower", "before": "a = r10.a;", "after": "a = 0u;", "case_ids": ["AIDecide_PokemonTrader_Flamethrower-0", "AIDecide_PokemonTrader_Flamethrower-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_Flamethrower
# >>> factory-mutation AIDecide_PokemonTrader_FlowerGarden
MUTATIONS["AIDecide_PokemonTrader_FlowerGarden"] = {"source_symbol": "AIDecide_PokemonTrader_FlowerGarden", "before": "a = r2.a;\n\tif (r2.f & 0x10u) goto find_duplicates;\n\n\treturn", "after": "a = 0u;\n\tif (r2.f & 0x10u) goto find_duplicates;\n\n\treturn", "case_ids": ["AIDecide_PokemonTrader_FlowerGarden-0", "AIDecide_PokemonTrader_FlowerGarden-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_FlowerGarden
# >>> factory-mutation AIDecide_PokemonTrader_PowerGenerator
MUTATIONS["AIDecide_PokemonTrader_PowerGenerator"] = {"source_symbol": "AIDecide_PokemonTrader_PowerGenerator", "before": "a = r16.a;", "after": "a = 0xFFu;", "case_ids": ["AIDecide_PokemonTrader_PowerGenerator-0", "AIDecide_PokemonTrader_PowerGenerator-1"]}
# <<< factory-mutation AIDecide_PokemonTrader_PowerGenerator
# >>> factory-mutation AIDecide_PokemonTrader
MUTATIONS["AIDecide_PokemonTrader"] = {"source_symbol": "AIDecide_PokemonTrader", "before": "return (AIDecide_PokemonTraderResult){deck_id, (uint8_t)(deck_id == 0u ? 0x80u : 0x00u)};", "after": "return (AIDecide_PokemonTraderResult){deck_id, 0xFFu};", "case_ids": ["AIDecide_PokemonTrader-0", "AIDecide_PokemonTrader-2"]}
# <<< factory-mutation AIDecide_PokemonTrader
# >>> factory-mutation AIDecide_EnergySearch
MUTATIONS["AIDecide_EnergySearch"] = {
    "source_symbol": "AIDecide_EnergySearch",
    "before": "\treturn (AIDecideEnergySearchResult){0u, 0x80u};",
    "after": "\treturn (AIDecideEnergySearchResult){0u, 0x00u};",
    "case_ids": ["AIDecide_EnergySearch-0", "AIDecide_EnergySearch-1"],
}
# <<< factory-mutation AIDecide_EnergySearch
# >>> factory-mutation _AIProcessHandTrainerCards
MUTATIONS["_AIProcessHandTrainerCards"] = {
    "source_symbol": "_AIProcessHandTrainerCards",
    "before": "\twAITrainerCardPhase = a;",
    "after": "\twAITrainerCardPhase = (uint8_t)(a ^ 0x01u);",
    "case_ids": ["_AIProcessHandTrainerCards-0", "_AIProcessHandTrainerCards-1"],
}
# <<< factory-mutation _AIProcessHandTrainerCards
# >>> factory-mutation AIPlay_Pokeball
MUTATIONS["AIPlay_Pokeball"] = {"source_symbol": "AIPlay_Pokeball", "before": "AIPlayPokeballResult AIPlay_Pokeball(void)\n{\n\tuint8_t card = wAITrainerCardToPlay;\n\thTempCardIndex_ff9f = card;", "after": "AIPlayPokeballResult AIPlay_Pokeball(void)\n{\n\tuint8_t card = wAITrainerCardParameter;\n\thTempCardIndex_ff9f = card;", "case_ids": ["AIPlay_Pokeball-0", "AIPlay_Pokeball-1", "AIPlay_Pokeball-2"]}
# <<< factory-mutation AIPlay_Pokeball
# >>> factory-mutation AIPlay_Recycle
MUTATIONS["AIPlay_Recycle"] = {"source_symbol": "AIPlay_Recycle", "before": "AIDecideResult AIPlay_Recycle(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;", "after": "AIDecideResult AIPlay_Recycle(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardParameter;", "case_ids": ["AIPlay_Recycle-0", "AIPlay_Recycle-1", "AIPlay_Recycle-2"]}
# <<< factory-mutation AIPlay_Recycle
# >>> factory-mutation AIDecide_PlusPower_Phase14
MUTATIONS["AIDecide_PlusPower_Phase14"] = {"source_symbol": "AIDecide_PlusPower_Phase14", "before": "\tCheckIfSelectedAttackIsUnusableResult unusable =\n\t\tCheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tif ((unusable.f & 0x10u) != 0u)\n\t\treturn (AIDecideResult){0u};", "after": "\tCheckIfSelectedAttackIsUnusableResult unusable =\n\t\tCheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tif ((unusable.f & 0x10u) != 0u)\n\t\treturn (AIDecideResult){0x10u};", "case_ids": ["AIDecide_PlusPower_Phase14-0", "AIDecide_PlusPower_Phase14-1"]}
# <<< factory-mutation AIDecide_PlusPower_Phase14
# >>> factory-mutation AIDecide_GustOfWind
MUTATIONS["AIDecide_GustOfWind"] = {"source_symbol": "AIDecide_GustOfWind", "before": "AIDecideResult AIDecide_GustOfWind(void)\n{\n\tuint8_t bench_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;\n\tif (bench_count == 1u)", "after": "AIDecideResult AIDecide_GustOfWind(void)\n{\n\tuint8_t bench_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;\n\tif (bench_count < 1u)", "case_ids": ["AIDecide_GustOfWind-0"]}
# <<< factory-mutation AIDecide_GustOfWind
# >>> factory-mutation AIDecide_Defender_Phase13
MUTATIONS["AIDecide_Defender_Phase13"] = {"source_symbol": "AIDecide_Defender_Phase13", "before": "AIDecideResult AIDecide_Defender_Phase13(void)\n{\n\thTempPlayAreaLocation_ff9d = 0u;", "after": "AIDecideResult AIDecide_Defender_Phase13(void)\n{\n\thTempPlayAreaLocation_ff9d = 1u;", "case_ids": ["AIDecide_Defender_Phase13-0", "AIDecide_Defender_Phase13-1"]}
# <<< factory-mutation AIDecide_Defender_Phase13
# >>> factory-mutation AIDecide_Switch
MUTATIONS["AIDecide_Switch"] = {"source_symbol": "AIDecide_Switch", "before": "\t\treturn (AIDecide_SwitchResult){r.a, (uint8_t)((r.f & 0x80u) | ((r.f & 0x10u) ? 0u : 0x10u))};", "after": "\t\treturn (AIDecide_SwitchResult){0u, (uint8_t)((r.f & 0x80u) | ((r.f & 0x10u) ? 0u : 0x10u))};", "case_ids": ["AIDecide_Switch-0", "AIDecide_Switch-1", "AIDecide_Switch-2"]}
# <<< factory-mutation AIDecide_Switch
# >>> factory-mutation AIDecide_SuperEnergyRemoval
MUTATIONS["AIDecide_SuperEnergyRemoval"] = {"source_symbol": "AIDecide_SuperEnergyRemoval", "before": "AIDecideResult AIDecide_SuperEnergyRemoval(void)\n{\n\treturn (AIDecideResult){0x00u};", "after": "AIDecideResult AIDecide_SuperEnergyRemoval(void)\n{\n\treturn (AIDecideResult){0x10u};", "case_ids": ["AIDecide_SuperEnergyRemoval-0", "AIDecide_SuperEnergyRemoval-1"]}
# <<< factory-mutation AIDecide_SuperEnergyRemoval
# >>> factory-mutation AIDecide_ScoopUp
MUTATIONS["AIDecide_ScoopUp"] = {"source_symbol": "AIDecide_ScoopUp", "before": "AIDecide_ScoopUpResult AIDecide_ScoopUp(void)\n{\n\thTempPlayAreaLocation_ff9d = 0u;", "after": "AIDecide_ScoopUpResult AIDecide_ScoopUp(void)\n{\n\thTempPlayAreaLocation_ff9d = 1u;", "case_ids": ["AIDecide_ScoopUp-0", "AIDecide_ScoopUp-1"]}
# <<< factory-mutation AIDecide_ScoopUp
# >>> factory-mutation AIDecide_FullHeal
MUTATIONS["AIDecide_FullHeal"] = {"source_symbol": "AIDecide_FullHeal", "before": "AIDecideFullHealResult AIDecide_FullHeal(void)\n{\n\tuint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;", "after": "AIDecideFullHealResult AIDecide_FullHeal(void)\n{\n\tuint8_t status = 0u;", "case_ids": ["AIDecide_FullHeal-1", "AIDecide_FullHeal-2"]}
# <<< factory-mutation AIDecide_FullHeal
# >>> factory-mutation AIDecide_EnergyRemoval
MUTATIONS["AIDecide_EnergyRemoval"] = {"source_symbol": "AIDecide_EnergyRemoval", "before": "\tuint8_t start = PLAY_AREA_ARENA;\n\tif (ko.f & 0x10u) {", "after": "\tuint8_t start = PLAY_AREA_BENCH_1;\n\tif (ko.f & 0x10u) {", "case_ids": ["AIDecide_EnergyRemoval-0"]}
# <<< factory-mutation AIDecide_EnergyRemoval
# >>> factory-mutation AIDecide_PokemonCenter
MUTATIONS["AIDecide_PokemonCenter"] = {"source_symbol": "AIDecide_PokemonCenter", "before": "AIDecideResult AIDecide_PokemonCenter(void)\n{\n\thTempPlayAreaLocation_ff9d = 0u;", "after": "AIDecideResult AIDecide_PokemonCenter(void)\n{\n\thTempPlayAreaLocation_ff9d = 1u;", "case_ids": ["AIDecide_PokemonCenter-0", "AIDecide_PokemonCenter-1"]}
# <<< factory-mutation AIDecide_PokemonCenter
# >>> factory-mutation AIDecide_PlusPower_Phase13
MUTATIONS["AIDecide_PlusPower_Phase13"] = {
    "source_symbol": "AIDecide_PlusPower_Phase13",
    "before": "\t/* .cannot_ko: the active Pokemon's id goes to wTempTurnDuelistCardID. */\n\tDuelistVarResult attacker = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);\n\twTempTurnDuelistCardID = (uint8_t)GetCardIDFromDeckIndex(attacker.a);",
    "after": "\t/* .cannot_ko: the active Pokemon's id goes to wTempTurnDuelistCardID. */\n\tDuelistVarResult attacker = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);\n\twTempTurnDuelistCardID = (uint8_t)(GetCardIDFromDeckIndex(attacker.a) + 1u);",
    "case_ids": ["AIDecide_PlusPower_Phase13-0", "AIDecide_PlusPower_Phase13-1", "AIDecide_PlusPower_Phase13-2"],
}
# <<< factory-mutation AIDecide_PlusPower_Phase13

# >>> factory-mutation AIPlay_Bill
MUTATIONS["AIPlay_Bill"] = {"source_symbol": "AIPlay_Bill",
    "before": "AIDecideResult AIPlay_Bill(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_Bill(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_Bill-0"]}
# <<< factory-mutation AIPlay_Bill
# >>> factory-mutation AIPlay_Defender
MUTATIONS["AIPlay_Defender"] = {"source_symbol": "AIPlay_Defender",
    "before": "AIDecideResult AIPlay_Defender(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_Defender(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_Defender-0"]}
# <<< factory-mutation AIPlay_Defender
# >>> factory-mutation AIPlay_Imakuni
MUTATIONS["AIPlay_Imakuni"] = {"source_symbol": "AIPlay_Imakuni",
    "before": "AIDecideResult AIPlay_Imakuni(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_Imakuni(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_Imakuni-0"]}
# <<< factory-mutation AIPlay_Imakuni
# >>> factory-mutation AIPlay_FullHeal
MUTATIONS["AIPlay_FullHeal"] = {"source_symbol": "AIPlay_FullHeal",
    "before": "AIDecideResult AIPlay_FullHeal(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_FullHeal(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_FullHeal-0"]}
# <<< factory-mutation AIPlay_FullHeal
# >>> factory-mutation AIPlay_ClefairyDollOrMysteriousFossil
MUTATIONS["AIPlay_ClefairyDollOrMysteriousFossil"] = {"source_symbol": "AIPlay_ClefairyDollOrMysteriousFossil",
    "before": "AIDecideResult AIPlay_ClefairyDollOrMysteriousFossil(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_ClefairyDollOrMysteriousFossil(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_ClefairyDollOrMysteriousFossil-0"]}
# <<< factory-mutation AIPlay_ClefairyDollOrMysteriousFossil
# >>> factory-mutation AIPlay_ImposterProfessorOak
MUTATIONS["AIPlay_ImposterProfessorOak"] = {"source_symbol": "AIPlay_ImposterProfessorOak",
    "before": "AIDecideResult AIPlay_ImposterProfessorOak(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_ImposterProfessorOak(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_ImposterProfessorOak-0"]}
# <<< factory-mutation AIPlay_ImposterProfessorOak
# >>> factory-mutation AIPlay_PokemonCenter
MUTATIONS["AIPlay_PokemonCenter"] = {"source_symbol": "AIPlay_PokemonCenter",
    "before": "AIDecideResult AIPlay_PokemonCenter(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_PokemonCenter(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);",
    "case_ids": ["AIPlay_PokemonCenter-0"]}
# <<< factory-mutation AIPlay_PokemonCenter
# >>> factory-mutation AIPlay_PlusPower
MUTATIONS["AIPlay_PlusPower"] = {
    "source_symbol": "AIPlay_PlusPower",
    "before": "AIDecideResult AIPlay_PlusPower(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_PLUSPOWER);\n\twAIPlusPowerAttack = wAITrainerCardParameter;",
    "after": "AIDecideResult AIPlay_PlusPower(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_PLUSPOWER);\n\twAIPlusPowerAttack = wAITrainerCardToPlay;",
    "case_ids": ["AIPlay_PlusPower-0", "AIPlay_PlusPower-1", "AIPlay_PlusPower-2"]
}
# <<< factory-mutation AIPlay_PlusPower
# >>> factory-mutation AIPlay_Potion
MUTATIONS["AIPlay_Potion"] = {"source_symbol": "AIPlay_Potion", "before": "AIDecideResult AIPlay_Potion(void)\n{\n\tuint8_t card = wAITrainerCardToPlay;\n\thTempCardIndex_ff9f = card;", "after": "AIDecideResult AIPlay_Potion(void)\n{\n\tuint8_t card = wAITrainerCardParameter;\n\thTempCardIndex_ff9f = card;", "case_ids": ["AIPlay_Potion-0", "AIPlay_Potion-1", "AIPlay_Potion-2"]}
# <<< factory-mutation AIPlay_Potion
# >>> factory-mutation AIPlay_GustOfWind
MUTATIONS["AIPlay_GustOfWind"] = {"source_symbol": "AIPlay_GustOfWind", "before": "AIDecideResult AIPlay_GustOfWind(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags |= 0x10u;", "after": "AIDecideResult AIPlay_GustOfWind(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags |= 0u;", "case_ids": ["AIPlay_GustOfWind-0", "AIPlay_GustOfWind-1", "AIPlay_GustOfWind-2"]}
# <<< factory-mutation AIPlay_GustOfWind
# >>> factory-mutation AIPlay_Switch
MUTATIONS["AIPlay_Switch"] = {"source_symbol": "AIPlay_Switch", "before": "AIDecideResult AIPlay_Switch(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_SWITCH);", "after": "AIDecideResult AIPlay_Switch(void)\n{\n\twCurrentAIFlags = 0u;", "case_ids": ["AIPlay_Switch-0", "AIPlay_Switch-1", "AIPlay_Switch-2"]}
# <<< factory-mutation AIPlay_Switch
# >>> factory-mutation AIPlay_Maintenance
MUTATIONS["AIPlay_Maintenance"] = {"source_symbol": "AIPlay_Maintenance", "before": "AIDecideResult AIPlay_Maintenance(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);", "after": "AIDecideResult AIPlay_Maintenance(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | 0u);", "case_ids": ["AIPlay_Maintenance-0"]}
# <<< factory-mutation AIPlay_Maintenance
# >>> factory-mutation AIPlay_ComputerSearch
MUTATIONS["AIPlay_ComputerSearch"] = {
    "source_symbol": "AIPlay_ComputerSearch",
    "before": "AIDecideResult AIPlay_ComputerSearch(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags = (uint8_t)(flags | AI_FLAG_MODIFIED_HAND);",
    "after": "AIDecideResult AIPlay_ComputerSearch(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags = (uint8_t)(flags | 0u);",
    "case_ids": ["AIPlay_ComputerSearch-0", "AIPlay_ComputerSearch-1", "AIPlay_ComputerSearch-2"]
}
# <<< factory-mutation AIPlay_ComputerSearch
# >>> factory-mutation AIPlay_ItemFinder
MUTATIONS["AIPlay_ItemFinder"] = {"source_symbol": "AIPlay_ItemFinder", "before": "AIDecideResult AIPlay_ItemFinder(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags |= AI_FLAG_MODIFIED_HAND;", "after": "AIDecideResult AIPlay_ItemFinder(void)\n{\n\tuint8_t flags = wCurrentAIFlags;\n\tflags |= 0u;", "case_ids": ["AIPlay_ItemFinder-0"]}
# <<< factory-mutation AIPlay_ItemFinder
# >>> factory-mutation AIPlay_Pokedex
MUTATIONS["AIPlay_Pokedex"] = {"source_symbol": "AIPlay_Pokedex", "before": "AIDecideResult AIPlay_Pokedex(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;", "after": "AIDecideResult AIPlay_Pokedex(void)\n{\n\thTempCardIndex_ff9f = 0u;", "case_ids": ["AIPlay_Pokedex-1"]}
# <<< factory-mutation AIPlay_Pokedex
# >>> factory-mutation AIPlay_Gambler
MUTATIONS["AIPlay_Gambler"] = {
    "source_symbol": "AIPlay_Gambler",
    "before": "AIDecideResult AIPlay_Gambler(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);",
    "after": "AIDecideResult AIPlay_Gambler(void)\n{\n\twCurrentAIFlags = wCurrentAIFlags;",
    "case_ids": ["AIPlay_Gambler-0"]
}
# <<< factory-mutation AIPlay_Gambler
# >>> factory-mutation AIPlay_EnergyRetrieval
MUTATIONS["AIPlay_EnergyRetrieval"] = {"source_symbol": "AIPlay_EnergyRetrieval", "before": "AIDecideResult AIPlay_EnergyRetrieval(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);", "after": "AIDecideResult AIPlay_EnergyRetrieval(void)\n{\n\twCurrentAIFlags = (uint8_t)(wCurrentAIFlags | 0u);", "case_ids": ["AIPlay_EnergyRetrieval-0"]}
# <<< factory-mutation AIPlay_EnergyRetrieval
# >>> factory-mutation AIPlay_SuperEnergyRemoval
MUTATIONS["AIPlay_SuperEnergyRemoval"] = {"source_symbol": "AIPlay_SuperEnergyRemoval", "before": "AIDecideResult AIPlay_SuperEnergyRemoval(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;", "after": "AIDecideResult AIPlay_SuperEnergyRemoval(void)\n{\n\thTempCardIndex_ff9f = (uint8_t)(wAITrainerCardToPlay + 1u);", "case_ids": ["AIPlay_SuperEnergyRemoval-0", "AIPlay_SuperEnergyRemoval-1", "AIPlay_SuperEnergyRemoval-2"]}
# <<< factory-mutation AIPlay_SuperEnergyRemoval
# >>> factory-mutation AIDecide_SuperPotion_Phase11
MUTATIONS["AIDecide_SuperPotion_Phase11"] = {"source_symbol": "AIDecide_SuperPotion_Phase11", "before": "\t\tif (card == 0xffu) return (AIDecideSuperPotionPhase11Result){0xffu, 0xC0u};", "after": "\t\tif (card == 0xffu) return (AIDecideSuperPotionPhase11Result){0u, 0xC0u};", "case_ids": ["AIDecide_SuperPotion_Phase11-0"]}
# <<< factory-mutation AIDecide_SuperPotion_Phase11
# >>> factory-mutation AIPlay_EnergySearch
MUTATIONS["AIPlay_EnergySearch"] = {
    "source_symbol": "AIPlay_EnergySearch",
    "before": "AIDecideResult AIPlay_EnergySearch(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardToPlay;",
    "after": "AIDecideResult AIPlay_EnergySearch(void)\n{\n\thTempCardIndex_ff9f = wAITrainerCardParameter;",
    "case_ids": ["AIPlay_EnergySearch-0"]
}
# <<< factory-mutation AIPlay_EnergySearch
