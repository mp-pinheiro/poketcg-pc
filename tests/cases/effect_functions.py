"""Oracle-diff cases for poketcg/src/engine/duel/effect_functions.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}




# >>> factory UpdateExpectedAIDamage
CONTRACT["UpdateExpectedAIDamage"] = {"compare": (), "preserve": ()}
CASES["UpdateExpectedAIDamage"] = [
	{"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0x05, "d": 0x03, "e": 0x07, "wram": {0xCCB9: b"\x10"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0xFF, "d": 0xFF, "e": 0xFF, "wram": {0xCCB9: b"\xFF"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	dict(POISON, wram={0xCCB9: b"\x22"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory UpdateExpectedAIDamage


# >>> factory SetExpectedAIDamage
CONTRACT["SetExpectedAIDamage"] = {"compare": (), "preserve": ()}
CASES["SetExpectedAIDamage"] = [
	{"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0x05, "d": 0x03, "e": 0x07, "wram": {0xCCB9: b"\xAA\xBB"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0xFF, "d": 0xFF, "e": 0xFF, "wram": {0xCCB9: b"\x01\x02"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	dict(POISON, wram={0xCCB9: b"\x33\x44"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SetExpectedAIDamage


# >>> factory IsPlayerTurn
CONTRACT["IsPlayerTurn"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["IsPlayerTurn"] = [
    {},
    dict(POISON),
    {"b": 1, "c": 2, "d": 3, "e": 4},
]
# <<< factory IsPlayerTurn


# >>> factory UpdateExpectedAIDamage_AccountForPoison
CONTRACT["UpdateExpectedAIDamage_AccountForPoison"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["UpdateExpectedAIDamage_AccountForPoison"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    {"a": 0x05, "d": 0x01, "e": 0x0A, "wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    dict(POISON, a=0x03, d=0x07, e=0x11, wram={0xCCB9: b"\x30"}, read={0xCCB9: 1, 0xCCBB: 2}),
    {"a": 0xFF, "d": 0xFF, "e": 0x00, "wram": {0xCCB9: b"\xFF"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
]
# <<< factory UpdateExpectedAIDamage_AccountForPoison

# >>> factory ApplySubstatus1ToAttackingCard
CONTRACT["ApplySubstatus1ToAttackingCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["ApplySubstatus1ToAttackingCard"] = [
    {},
    {"a": 1},
    {"a": 0xFF},
    dict(POISON, a=0x20),
]
# <<< factory ApplySubstatus1ToAttackingCard


# >>> factory SetNoEffectFromStatus
CONTRACT["SetNoEffectFromStatus"] = {"compare": (), "preserve": ()}
CASES["SetNoEffectFromStatus"] = [
    {"read": {0xCCED: 1}},
    dict(POISON, read={0xCCED: 1}),
]
# <<< factory SetNoEffectFromStatus

# >>> factory SetDefiniteAIDamage
CONTRACT["SetDefiniteAIDamage"] = {"compare": (), "preserve": ()}
CASES["SetDefiniteAIDamage"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xCCB9: b"\x42"}, "read": {0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x99"}, read={0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SetDefiniteAIDamage

# >>> factory PickRandomPlayAreaCard
CONTRACT["PickRandomPlayAreaCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PickRandomPlayAreaCard"] = [
	{"a": 0},
	{"a": 1},
	dict(POISON, a=0x40),
]
# <<< factory PickRandomPlayAreaCard

# >>> factory GetNextPositionInTempList
CONTRACT["GetNextPositionInTempList"] = {"compare": ("hl", "d", "e"), "preserve": ("d", "e")}
CASES["GetNextPositionInTempList"] = [
	{"wram": {0xFFB2: b"\x00"}, "read": {0xFFB2: 1}},
	{"wram": {0xFFB2: b"\x01"}, "read": {0xFFB2: 1}},
	dict(POISON, wram={0xFFB2: b"\xFF"}, read={0xFFB2: 1}),
]
# <<< factory GetNextPositionInTempList

# >>> factory QueueStatusCondition
wStatusConditionQueue = 0xCCCE
wStatusConditionQueueIndex = 0xCCCD
wTempNonTurnDuelistCardID = 0xCCC4
wWhoseTurn = 0xCC05
hWhoseTurn = 0xFF97
wNoEffectFromWhichStatus = 0xCCF1
wEffectFailed = 0xCCED

CONTRACT["QueueStatusCondition"] = {"compare": ("f",), "preserve": ()}
CASES["QueueStatusCondition"] = [
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x01"},
     "read": {wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}},
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x00", wTempNonTurnDuelistCardID: b"\xcb"},
     "read": {wNoEffectFromWhichStatus: 1, wEffectFailed: 1}},
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x00", wTempNonTurnDuelistCardID: b"\xcc"},
     "read": {wNoEffectFromWhichStatus: 1, wEffectFailed: 1}},
    dict(POISON, b=1, c=2, wram={hWhoseTurn: b"\x01", wWhoseTurn: b"\x00"},
         read={wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}),
    {"b": 3, "c": 4, "wram": {hWhoseTurn: b"\x02", wWhoseTurn: b"\x02", wStatusConditionQueueIndex: b"\x00"},
     "read": {wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}},
]
# <<< factory QueueStatusCondition

# >>> factory CommentedOut_2c086
CONTRACT["CommentedOut_2c086"] = {"compare": ("a",), "preserve": ("a",)}
CASES["CommentedOut_2c086"] = [
    {"a": 0},
    dict(POISON, a=0xAA),
    {"a": 1},
    {"a": 255},
]
# <<< factory CommentedOut_2c086

# >>> factory SetWasUnsuccessful
wEffectFailed = 0xCCED

CONTRACT["SetWasUnsuccessful"] = {"compare": (), "preserve": ()}
CASES["SetWasUnsuccessful"] = [
    {"wram": {wEffectFailed: b"\x00"}, "read": {wEffectFailed: 1}},
    dict(POISON, wram={wEffectFailed: b"\xFF"}, read={wEffectFailed: 1}),
]
# <<< factory SetWasUnsuccessful

# >>> factory Teleport_SwitchEffect
CONTRACT["Teleport_SwitchEffect"] = {"compare": (), "preserve": ()}
hTemp_ffa0 = 0xFFA0
wDuelDisplayedScreen = 0xCAC2
CASES["Teleport_SwitchEffect"] = [
    {"wram": {hTemp_ffa0: b"\x00", wDuelDisplayedScreen: b"\x05"}},
    {"wram": {hTemp_ffa0: b"\x01", wDuelDisplayedScreen: b"\xFF"}},
    dict(POISON, wram={hTemp_ffa0: b"\x02", wDuelDisplayedScreen: b"\x03"}),
]
# <<< factory Teleport_SwitchEffect

# >>> factory SetDamageToATimes20
CONTRACT["SetDamageToATimes20"] = {"compare": (), "preserve": ()}
wDamage = 0xCCB9
CASES["SetDamageToATimes20"] = [
    {"a": 0, "read": {wDamage: 2}},
    {"a": 1, "read": {wDamage: 2}},
    {"a": 10, "read": {wDamage: 2}},
    {"a": 255, "read": {wDamage: 2}},
    dict(POISON, a=5, read={wDamage: 2}),
]
# <<< factory SetDamageToATimes20

# >>> factory CreateTrainerCardListFromDiscardPile
CONTRACT["CreateTrainerCardListFromDiscardPile"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["CreateTrainerCardListFromDiscardPile"] = [
	{"wram": {0xC37E: b"\x00"}, "read": {0xC510: 4}},
	dict(POISON, wram={0xC37E: b"\x00"}),
	{"wram": {0xC510: b"\x00\x00\x00\x00"}},
]
# <<< factory CreateTrainerCardListFromDiscardPile

# >>> factory CreateEnergyCardListFromDiscardPile
CONTRACT["CreateEnergyCardListFromDiscardPile"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["CreateEnergyCardListFromDiscardPile"] = [
	{"c": 0, "wram": {0xC340: b"\x00"}},
	{"c": 1, "wram": {0xC340: b"\x00"}},
	dict(POISON, wram={0xC340: b"\x00"}),
	dict(POISON, c=1, wram={0xC340: b"\x00"}),
]
# <<< factory CreateEnergyCardListFromDiscardPile

# >>> factory GetAttackName
CONTRACT["GetAttackName"] = {"compare": ("hl",), "preserve": ()}
CASES["GetAttackName"] = [
	{"d": 0, "e": 0},
	{"d": 1, "e": 1},
	{"d": 5, "e": 0},
	dict(POISON, d=8, e=0),
	dict(POISON, d=8, e=1),
]
# <<< factory GetAttackName


# >>> factory ClefableMinimizeEffect
CONTRACT["ClefableMinimizeEffect"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["ClefableMinimizeEffect"] = [
    {"read": {0xC2F1: 1}},
    dict(POISON, read={0xC2F1: 1}),
]
# <<< factory ClefableMinimizeEffect


# >>> factory HandleAIMetronomeEffect
CONTRACT["HandleAIMetronomeEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["HandleAIMetronomeEffect"] = [
    {"wram": {0xC100: b"\x00"}},
    dict(POISON, wram={0xC100: b"\x00"}),
]
# <<< factory HandleAIMetronomeEffect

# >>> factory ParalysisEffect
CONTRACT["ParalysisEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ParalysisEffect"] = [
    {"read": {0xCB00: 0x100, 0xCC00: 0x100}},
    dict(POISON, read={0xCB00: 0x100, 0xCC00: 0x100}),
]
# <<< factory ParalysisEffect

# >>> factory ConfusionEffect
CONTRACT["ConfusionEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ConfusionEffect"] = [
    {"read": {0xCB00: 0x100, 0xCC00: 0x100}},
    dict(POISON, read={0xCB00: 0x100, 0xCC00: 0x100}),
]
# <<< factory ConfusionEffect

# >>> factory InvisibleWallEffect
CONTRACT["InvisibleWallEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["InvisibleWallEffect"] = [
    {},
    dict(POISON),
    {"f": 0x80},
]
# <<< factory InvisibleWallEffect

# >>> factory CheckIfDefendingPokemonHasAnyAttack
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wOpponentDuelVariables = 0xC300
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
DUELVARS_ARENA_CARD = 0xBB
BULBASAUR = 0x08
BEEDRILL = 0x11
SNORLAX = 0xBE
CLEFAIRY_DOLL = 0xCB
MYSTERIOUS_FOSSIL = 0xCC

CONTRACT["CheckIfDefendingPokemonHasAnyAttack"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfDefendingPokemonHasAnyAttack"] = [
    # Opponent's arena has Bulbasaur (Leech Seed, category DAMAGE_NORMAL=0): has an attack, a==0 at exit.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wOpponentDeck: bytes((BULBASAUR,))},
     "read": {hWhoseTurn: 1}},
    # Beedrill (category DAMAGE_X=3, nonzero non-power): has an attack, a!=0 at exit.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wOpponentDeck: bytes((BEEDRILL,))},
     "read": {hWhoseTurn: 1}},
    # Snorlax (Pokemon Power Atk1 + real Atk2 "Body Slam"): has an attack.
    {"wram": {hWhoseTurn: b"\xC3", wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wPlayerDeck: bytes((SNORLAX,))},
     "read": {hWhoseTurn: 1}},
    # Clefairy Doll (Trainer-as-Pokemon: Atk1=POKEMON_POWER, Atk2 zeroed): no attack.
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wOpponentDeck: bytes((CLEFAIRY_DOLL,)), wOpponentDuelVariables: b"\x10"},
     "read": {hWhoseTurn: 1}},
    dict(POISON,
         wram={hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
               wOpponentDeck: bytes((MYSTERIOUS_FOSSIL,)), wOpponentDuelVariables: b"\x10"},
         read={hWhoseTurn: 1}),
]
# <<< factory CheckIfDefendingPokemonHasAnyAttack

# >>> factory UpdateDevolvedCardHPAndStage
hTempPlayAreaLocation_ff9d = 0xFF9D
DUELVARS_ARENA_CARD_HP = 0xC8
DUELVARS_ARENA_CARD_STAGE = 0xCE
IVYSAUR = 0x09
METAPOD = 0x0D
CATERPIE = 0x0C
BUTTERFREE = 0x0E

CONTRACT["UpdateDevolvedCardHPAndStage"] = {"compare": (), "preserve": ()}
CASES["UpdateDevolvedCardHPAndStage"] = [
    # Arena, Ivysaur (max HP 60) devolving to Bulbasaur (max HP 40), no HP clamp.
    {"a": 1, "wram": {hTempPlayAreaLocation_ff9d: b"\x00", hWhoseTurn: b"\xC2",
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
                      wPlayerDeck: bytes((IVYSAUR,)),
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x37",
                      wPlayerDeck + 1: bytes((BULBASAUR,))},
     "read": {wPlayerDuelVariables + DUELVARS_ARENA_CARD: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STAGE: 1}},
    # Bench slot 1, opponent side, Metapod devolving to Caterpie, no HP clamp.
    {"a": 3, "wram": {hTempPlayAreaLocation_ff9d: b"\x01", hWhoseTurn: b"\xC3",
                      wOpponentDuelVariables + DUELVARS_ARENA_CARD + 1: bytes((2,)),
                      wOpponentDeck + 2: bytes((METAPOD,)),
                      wOpponentDuelVariables + DUELVARS_ARENA_CARD_HP + 1: b"\x41",
                      wOpponentDeck + 3: bytes((CATERPIE,))},
     "read": {wOpponentDuelVariables + DUELVARS_ARENA_CARD + 1: 1,
              wOpponentDuelVariables + DUELVARS_ARENA_CARD_HP + 1: 1,
              wOpponentDuelVariables + DUELVARS_ARENA_CARD_STAGE + 1: 1}},
    # Snorlax (max HP 90, HP field 0 -> damage 90) devolving to Bulbasaur (max HP 40): damage exceeds new max HP, clamp to 0.
    {"a": 6, "wram": {hTempPlayAreaLocation_ff9d: b"\x00", hWhoseTurn: b"\xC2",
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD: bytes((5,)),
                      wPlayerDeck + 5: bytes((SNORLAX,)),
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x00",
                      wPlayerDeck + 6: bytes((BULBASAUR,))},
     "read": {wPlayerDuelVariables + DUELVARS_ARENA_CARD: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STAGE: 1}},
    # Snorlax (HP field 50 -> damage 40) devolving to Bulbasaur (max HP 40): exact boundary, no-borrow path yields 0.
    {"a": 6, "wram": {hTempPlayAreaLocation_ff9d: b"\x00", hWhoseTurn: b"\xC2",
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD: bytes((5,)),
                      wPlayerDeck + 5: bytes((SNORLAX,)),
                      wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x32",
                      wPlayerDeck + 6: bytes((BULBASAUR,))},
     "read": {wPlayerDuelVariables + DUELVARS_ARENA_CARD: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: 1,
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STAGE: 1}},
    dict(POISON, a=7,
         wram={hTempPlayAreaLocation_ff9d: b"\x02", hWhoseTurn: b"\xC3",
               wOpponentDuelVariables + DUELVARS_ARENA_CARD + 2: bytes((4,)),
               wOpponentDeck + 4: bytes((BUTTERFREE,)),
               wOpponentDuelVariables + DUELVARS_ARENA_CARD_HP + 2: b"\x07",
               wOpponentDeck + 7: bytes((METAPOD,))},
         read={wOpponentDuelVariables + DUELVARS_ARENA_CARD + 2: 1,
               wOpponentDuelVariables + DUELVARS_ARENA_CARD_HP + 2: 1,
               wOpponentDuelVariables + DUELVARS_ARENA_CARD_STAGE + 2: 1}),
]
# <<< factory UpdateDevolvedCardHPAndStage

# >>> factory DodrioRage_DamageBoostEffect
hWhoseTurn = 0xFF97
wDamage = 0xCCB9
wPlayerDeck = 0xC400
CONTRACT["DodrioRage_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["DodrioRage_DamageBoostEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
              wPlayerDeck: b"\x01", wDamage: b"\x00\x00"},
     "read": {wDamage: 2}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
                        wPlayerDeck: b"\x01", wDamage: b"\x00\x00"},
         read={wDamage: 2}),
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xC9",
              wPlayerDeck: b"\x01", wDamage: b"\x05\x00"},
     "read": {wDamage: 2}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xFF",
              wPlayerDeck: b"\x01", wDamage: b"\xFF\x00"},
     "read": {wDamage: 2}},
]
# <<< factory DodrioRage_DamageBoostEffect

# >>> factory DragonairSlam_AIEffect
CONTRACT["DragonairSlam_AIEffect"] = {"compare": (), "preserve": ()}
CASES["DragonairSlam_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory DragonairSlam_AIEffect

# >>> factory CheckIfPlayAreaHasAnyDamage
CONTRACT["CheckIfPlayAreaHasAnyDamage"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["CheckIfPlayAreaHasAnyDamage"] = [
    {},
    dict(POISON),
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x00",
              0xC400: b"\x08", 0xC2C8: b"\x28"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x00",
              0xC400: b"\x08", 0xC2C8: b"\x1E"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x00", 0xC2BB: b"\x00",
              0xC400: b"\x08", 0xC2C8: b"\x1E"}},
]
# <<< factory CheckIfPlayAreaHasAnyDamage



# >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic
CONTRACT["CreateEnergyCardListFromDiscardPile_OnlyBasic"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["CreateEnergyCardListFromDiscardPile_OnlyBasic"] = [
    {},
    dict(POISON),
]
# <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic

# >>> factory KabutoArmorEffect
CONTRACT["KabutoArmorEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["KabutoArmorEffect"] = [
    {},
    dict(POISON),
    {"f": 0x80},
]
# <<< factory KabutoArmorEffect

# >>> factory CuboneRage_DamageBoostEffect
CONTRACT["CuboneRage_DamageBoostEffect"] = {"compare": ("b", "d", "hl"), "preserve": ("b", "d", "hl")}
CR_HWT = 0xFF97
CR_ARENA_IDX = 0xC2BB
CR_ARENA_HP = 0xC2C8
CR_PDECK = 0xC400
CR_WDMG = 0xCCB9
CASES["CuboneRage_DamageBoostEffect"] = [
    {"wram": {CR_HWT: b"\xC2", CR_ARENA_IDX: b"\x00", CR_ARENA_HP: b"\x00",
              CR_PDECK: b"\x01", CR_WDMG: b"\x00\x00"}},
    {"wram": {CR_HWT: b"\xC2", CR_ARENA_IDX: b"\x00", CR_ARENA_HP: b"\x71",
              CR_PDECK: b"\x01", CR_WDMG: b"\x00\x00"}},
    {"wram": {CR_HWT: b"\xC2", CR_ARENA_IDX: b"\x00", CR_ARENA_HP: b"\xD0",
              CR_PDECK: b"\x01", CR_WDMG: b"\x00\x00"}},
    {"wram": {CR_HWT: b"\xC2", CR_ARENA_IDX: b"\x00", CR_ARENA_HP: b"\x00",
              CR_PDECK: b"\x01", CR_WDMG: b"\xFF\x00"}},
    dict(POISON, wram={CR_HWT: b"\xC2", CR_ARENA_IDX: b"\x00", CR_ARENA_HP: b"\x05",
                        CR_PDECK: b"\x01", CR_WDMG: b"\x10\x00"}),
]
# <<< factory CuboneRage_DamageBoostEffect

# >>> factory PoisonEffect
CONTRACT["PoisonEffect"] = {"compare": ("f",), "preserve": ()}
CASES["PoisonEffect"] = [
    {"read": {0xCB00: 0x100, 0xCC00: 0x100}},
    dict(POISON, read={0xCB00: 0x100, 0xCC00: 0x100}),
]
# <<< factory PoisonEffect

# >>> factory DoublePoisonEffect
CONTRACT["DoublePoisonEffect"] = {"compare": ("f",), "preserve": ()}
CASES["DoublePoisonEffect"] = [
    {"read": {0xCB00: 0x100, 0xCC00: 0x100}},
    dict(POISON, read={0xCB00: 0x100, 0xCC00: 0x100}),
]
# <<< factory DoublePoisonEffect

# >>> factory LoadCardNameAndInputColor
CONTRACT["LoadCardNameAndInputColor"] = {"compare": (), "preserve": ()}
CASES["LoadCardNameAndInputColor"] = [
	{"a": 0, "wram": {0xCC27: b"\x00\x00"}, "read": {0xCE3F: 4}},
	{"a": 1, "wram": {0xCC27: b"\x12\x34"}, "read": {0xCE3F: 4}},
	{"a": 2, "wram": {0xCC27: b"\x9A\xBC"}, "read": {0xCE3F: 4}},
	{"a": 3, "wram": {0xCC27: b"\x9A\xBC"}, "read": {0xCE3F: 4}},
	{"a": 4, "wram": {0xCC27: b"\x56\x78"}, "read": {0xCE3F: 4}},
	{"a": 5, "wram": {0xCC27: b"\xDE\xF0"}, "read": {0xCE3F: 4}},
	dict(POISON, a=2, wram={0xCC27: b"\x9A\xBC"}, read={0xCE3F: 4}),
]
# <<< factory LoadCardNameAndInputColor



# >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon
CONTRACT["AIPickEnergyCardToDiscardFromDefendingPokemon"] = {"compare": ("a",), "preserve": ()}
CASES["AIPickEnergyCardToDiscardFromDefendingPokemon"] = [
    {"wram": {0xC0EF: b"\x00"}},
    {"wram": {0xC1EF: b"\x00"}},
    dict(POISON, wram={0xC0EF: b"\x00"}),
    dict(POISON, wram={0xC1EF: b"\x00"}),
]
# <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon


# >>> factory AIFindTargetForBenchAttack
CONTRACT["AIFindTargetForBenchAttack"] = {"compare": ("a",), "preserve": ()}
CASES["AIFindTargetForBenchAttack"] = [
    {"wram": {0xC0EF: b"\x01"}},
    {"wram": {0xC1EF: b"\x01"}},
    dict(POISON, wram={0xC0EF: b"\x01"}),
    dict(POISON, wram={0xC1EF: b"\x01"}),
]
# <<< factory AIFindTargetForBenchAttack


# >>> factory ApplyExtraWaterEnergyDamageBonus
CONTRACT["ApplyExtraWaterEnergyDamageBonus"] = {"compare": (), "preserve": ()}
CASES["ApplyExtraWaterEnergyDamageBonus"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory ApplyExtraWaterEnergyDamageBonus


# >>> factory OmastarSpikeCannon_AIEffect
CONTRACT["OmastarSpikeCannon_AIEffect"] = {"compare": ("a",), "preserve": ()}
CASES["OmastarSpikeCannon_AIEffect"] = [
    dict(POISON, read={0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory OmastarSpikeCannon_AIEffect

# >>> factory ClairvoyanceEffect
CONTRACT["ClairvoyanceEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                                   "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["ClairvoyanceEffect"] = [dict(POISON)]
# <<< factory ClairvoyanceEffect

# >>> factory KrabbyCallForFamily_AISelectEffect
CONTRACT["KrabbyCallForFamily_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["KrabbyCallForFamily_AISelectEffect"] = [
    {"c": 0, "d": 0, "e": 0, "read": {0xFFA0: 1}},
    dict(POISON, c=1, d=0x12, e=0x34, read={0xFFA0: 1}),
    {"c": 0xFF, "d": 0xFF, "e": 0xFF, "read": {0xFFA0: 1}},
]
# <<< factory KrabbyCallForFamily_AISelectEffect

# >>> factory CreateListOfEnergyAttachedToArena
CONTRACT["CreateListOfEnergyAttachedToArena"] = {"compare": ("a", "c", "f", "hl"), "preserve": ()}
CASES["CreateListOfEnergyAttachedToArena"] = [
    {"a": 0x08, "wram": {0xFF97: b"\x00"}, "read": {0xC510: 1}},
    dict(POISON, a=0x10, wram={0xFF97: b"\x00"}, read={0xC510: 1}),
]
# <<< factory CreateListOfEnergyAttachedToArena


# >>> factory HandleNoDamageOrEffect
CONTRACT["HandleNoDamageOrEffect"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["HandleNoDamageOrEffect"] = [
    {"hl": 0x1234, "wram": {0xCCC7: b"\x00"}},
    {"hl": 0x0000, "wram": {0xCCC7: b"\x80"}},
    dict(POISON, hl=0x4567, wram={0xCCC7: b"\x80"}),
    dict(POISON, hl=0x1234, wram={0xCCC7: b"\x00"}),
]
# <<< factory HandleNoDamageOrEffect


# >>> factory ArcanineFlamethrower_CheckEnergy
CONTRACT["ArcanineFlamethrower_CheckEnergy"] = {"compare": ("a", "f", "e", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["ArcanineFlamethrower_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
]
# <<< factory ArcanineFlamethrower_CheckEnergy

# >>> factory ArcanineFlamethrower_DiscardEffect
CONTRACT["ArcanineFlamethrower_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["ArcanineFlamethrower_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA0: b"\x01"}),
]
# <<< factory ArcanineFlamethrower_DiscardEffect

# >>> factory PoisonWhip_AIEffect
CONTRACT["PoisonWhip_AIEffect"] = {"compare": (), "preserve": ()}
CASES["PoisonWhip_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory PoisonWhip_AIEffect

# >>> factory SolarPower_CheckUse
CONTRACT["SolarPower_CheckUse"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SolarPower_CheckUse"] = [
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x20"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2C2: b"\x20"}),
    dict(POISON, a=1, wram={0xFF97: b"\xC2", 0xC2C2: b"\x20"}),
    dict(POISON, f=0, wram={0xFF97: b"\xC2", 0xC2C2: b"\x20"}),
    dict(POISON, hl=0x4567, wram={0xFF97: b"\xC2", 0xC2C2: b"\x20"}),
]
# <<< factory SolarPower_CheckUse

# >>> factory DevolutionBeam_LoadAnimation
CONTRACT["DevolutionBeam_LoadAnimation"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["DevolutionBeam_LoadAnimation"] = [
    {"wram": {0xCCB8: b"\x00"}},
    dict(POISON, wram={0xCCB8: b"\xAA"}),
]
# <<< factory DevolutionBeam_LoadAnimation


# >>> factory CheckIfTurnDuelistHasEvolvedCards
CONTRACT["CheckIfTurnDuelistHasEvolvedCards"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfTurnDuelistHasEvolvedCards"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x01\x02\xFF",
              0xC2CE: b"\x00\x00\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x01\x02\xFF",
              0xC2CE: b"\x00\x01\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x01\xFF",
                       0xC2CE: b"\x00\x00"}, read={0xFF97: 1}),
]
# <<< factory CheckIfTurnDuelistHasEvolvedCards

# >>> factory FindFirstNonBasicCardInPlayArea
CONTRACT["FindFirstNonBasicCardInPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["FindFirstNonBasicCardInPlayArea"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03",
              0xC2CE: b"\x00\x00\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03",
              0xC2CE: b"\x00\x01\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03",
              0xC2CE: b"\x00\x00\x01"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01",
                       0xC2CE: b"\x01"}),
]
# <<< factory FindFirstNonBasicCardInPlayArea

# >>> factory Wildfire_AISelectEffect
CONTRACT["Wildfire_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Wildfire_AISelectEffect"] = [
    {"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 6, "wram": {0xFFA0: b"\x55"}, "read": {0xFFA0: 1}},
]
# <<< factory Wildfire_AISelectEffect

# >>> factory FireBlast_CheckEnergy
CONTRACT["FireBlast_CheckEnergy"] = {"compare": ("a", "f", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["FireBlast_CheckEnergy"] = [
    {},
    dict(POISON),
    {"a": 1, "f": 0x10, "b": 1, "c": 0, "d": 0xFF, "e": 0xFF, "hl": 0x0100, "wram": {0xCC1B: b"\x01\x02\x03\x04\x05\x06\x07\x08"}},
]
# <<< factory FireBlast_CheckEnergy

# >>> factory BigEggsplosion_AIEffect
CONTRACT["BigEggsplosion_AIEffect"] = {"compare": (), "preserve": ()}
CASES["BigEggsplosion_AIEffect"] = [
    {"hTempPlayAreaLocation_ff9d": 0, "wram": {0xFF9D: b"\x00", 0xCCBB: b"\xAA", 0xCCBC: b"\xAA", 0xCCB9: b"\xAA"}},
    dict(POISON, wram={0xFF9D: b"\x01", 0xCCBB: b"\xAA", 0xCCBC: b"\xAA", 0xCCB9: b"\xAA"}),
    {"wram": {0xFF9D: b"\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF", 0xCCB9: b"\xFF"}},
]
# <<< factory BigEggsplosion_AIEffect

# >>> factory Thrash_AIEffect
CONTRACT["Thrash_AIEffect"] = {"compare": (), "preserve": ()}
CASES["Thrash_AIEffect"] = [
    {"wram": {0xCCBB: b"\x00", 0xCCBC: b"\x00", 0xCCB9: b"\x00"}},
    dict(POISON, wram={0xCCBB: b"\xAA", 0xCCBC: b"\xAA", 0xCCB9: b"\xAA"}),
    {"wram": {0xCCBB: b"\xFF", 0xCCBC: b"\xFF", 0xCCB9: b"\xFF"}},
]
# <<< factory Thrash_AIEffect

# >>> factory Prophecy_CheckDeck
CONTRACT["Prophecy_CheckDeck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["Prophecy_CheckDeck"] = [
    {},
    dict(POISON),
]
# <<< factory Prophecy_CheckDeck

# >>> factory TryGiveDamageCounter_DamageSwap
CONTRACT["TryGiveDamageCounter_DamageSwap"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["TryGiveDamageCounter_DamageSwap"] = [
    {"wram": {0xFFA1: b"\x00", 0xFFA2: b"\x00"}, "read": {0xC100: 0x900}},
    dict(POISON, wram={0xFFA1: b"\x02", 0xFFA2: b"\x01"}, read={0xC100: 0x900}),
    {"b": 1, "c": 2, "d": 3, "e": 4, "wram": {0xFFA1: b"\x03", 0xFFA2: b"\x04"}, "read": {0xC100: 0x900}},
]
# <<< factory TryGiveDamageCounter_DamageSwap

# >>> factory TransparencyEffect
CONTRACT["TransparencyEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["TransparencyEffect"] = [{}, dict(POISON)]
# <<< factory TransparencyEffect

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation UpdateExpectedAIDamage
MUTATIONS["UpdateExpectedAIDamage"] = {
	"source_symbol": "UpdateExpectedAIDamage",
	"before": "gb_write8(wDamage_ADDR, (uint8_t)(a + hl));",
	"after": "gb_write8(wDamage_ADDR, (uint8_t)(a + hl + 1u));",
	"case_ids": ["UpdateExpectedAIDamage-0", "UpdateExpectedAIDamage-1", "UpdateExpectedAIDamage-2", "UpdateExpectedAIDamage-3"],
}
# <<< factory-mutation UpdateExpectedAIDamage
# >>> factory-mutation SetExpectedAIDamage
MUTATIONS["SetExpectedAIDamage"] = {
	"source_symbol": "SetExpectedAIDamage",
	"before": "gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);",
	"after": "gb_write8((uint16_t)(wDamage_ADDR + 1u), 1u);",
	"case_ids": ["SetExpectedAIDamage-0", "SetExpectedAIDamage-1", "SetExpectedAIDamage-2", "SetExpectedAIDamage-3"],
}
# <<< factory-mutation SetExpectedAIDamage
# >>> factory-mutation IsPlayerTurn
MUTATIONS["IsPlayerTurn"] = {
    "source_symbol": "IsPlayerTurn",
    "before": "\tDuelistVarResult r = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);",
    "after": "\tDuelistVarResult r = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);",
    "case_ids": ["IsPlayerTurn-0", "IsPlayerTurn-1", "IsPlayerTurn-2"],
}
# <<< factory-mutation IsPlayerTurn
# >>> factory-mutation UpdateExpectedAIDamage_AccountForPoison
MUTATIONS["UpdateExpectedAIDamage_AccountForPoison"] = {
    "source_symbol": "UpdateExpectedAIDamage_AccountForPoison",
    "before": "\t\tUpdateExpectedAIDamage(a, d, e);",
    "after": "\t\tUpdateExpectedAIDamage(a, e, d);",
    "case_ids": ["UpdateExpectedAIDamage_AccountForPoison-1", "UpdateExpectedAIDamage_AccountForPoison-2"],
}
# <<< factory-mutation UpdateExpectedAIDamage_AccountForPoison
# >>> factory-mutation ApplySubstatus1ToAttackingCard
MUTATIONS["ApplySubstatus1ToAttackingCard"] = {
    "source_symbol": "ApplySubstatus1ToAttackingCard",
    "before": "\treturn (uint16_t)(r.hl + 1u);",
    "after": "\treturn r.hl;",
    "case_ids": ["ApplySubstatus1ToAttackingCard-0", "ApplySubstatus1ToAttackingCard-1", "ApplySubstatus1ToAttackingCard-2", "ApplySubstatus1ToAttackingCard-3"],
}
# <<< factory-mutation ApplySubstatus1ToAttackingCard
# >>> factory-mutation SetNoEffectFromStatus
MUTATIONS["SetNoEffectFromStatus"] = {"source_symbol": "SetNoEffectFromStatus", "before": "gb_write8(0xCCEDu, 0x01u);", "after": "gb_write8(0xCCEDu, 0x02u);", "case_ids": ["SetNoEffectFromStatus-0", "SetNoEffectFromStatus-1"]}
# <<< factory-mutation SetNoEffectFromStatus
# >>> factory-mutation SetDefiniteAIDamage
MUTATIONS["SetDefiniteAIDamage"] = {"source_symbol": "SetDefiniteAIDamage", "before": "gb_write8(0xCCBBu, a);", "after": "gb_write8(0xCCBBu, 0x00u);", "case_ids": ["SetDefiniteAIDamage-1", "SetDefiniteAIDamage-0", "SetDefiniteAIDamage-2"]}
# <<< factory-mutation SetDefiniteAIDamage
# >>> factory-mutation PickRandomPlayAreaCard
MUTATIONS["PickRandomPlayAreaCard"] = {
	"source_symbol": "PickRandomPlayAreaCard",
	"before": "return (PickRandomPlayAreaCardResult){a, (uint8_t)(a == 0 ? 0x80u : 0u)};",
	"after": "return (PickRandomPlayAreaCardResult){a, (uint8_t)(a == 0 ? 0x00u : 0u)};",
	"case_ids": ["PickRandomPlayAreaCard-0"],
}
# <<< factory-mutation PickRandomPlayAreaCard
# >>> factory-mutation GetNextPositionInTempList
MUTATIONS["GetNextPositionInTempList"] = {
	"source_symbol": "GetNextPositionInTempList",
	"before": "return (uint16_t)(hTempList_ADDR + a);",
	"after": "return (uint16_t)(hTempList_ADDR + a + 1u);",
	"case_ids": ["GetNextPositionInTempList-0", "GetNextPositionInTempList-1"],
}
# <<< factory-mutation GetNextPositionInTempList
# >>> factory-mutation QueueStatusCondition
MUTATIONS["QueueStatusCondition"] = {
    "source_symbol": "QueueStatusCondition",
    "before": "return (QueueStatusConditionResult){0x10u};",
    "after": "return (QueueStatusConditionResult){0x00u};",
    "case_ids": ["QueueStatusCondition-0", "QueueStatusCondition-3", "QueueStatusCondition-4"],
}
# <<< factory-mutation QueueStatusCondition
# >>> factory-mutation CommentedOut_2c086
MUTATIONS["CommentedOut_2c086"] = {
    "source_symbol": "CommentedOut_2c086",
    "before": "\treturn a;",
    "after": "\treturn (uint8_t)(a + 1u);",
    "case_ids": ["CommentedOut_2c086-0", "CommentedOut_2c086-1", "CommentedOut_2c086-2", "CommentedOut_2c086-3"],
}
# <<< factory-mutation CommentedOut_2c086
# >>> factory-mutation SetWasUnsuccessful
MUTATIONS["SetWasUnsuccessful"] = {
    "source_symbol": "SetWasUnsuccessful",
    "before": "wEffectFailed = EFFECT_FAILED_UNSUCCESSFUL;",
    "after": "wEffectFailed = 0x00u;",
    "case_ids": ["SetWasUnsuccessful-0", "SetWasUnsuccessful-1"],
}
# <<< factory-mutation SetWasUnsuccessful
# >>> factory-mutation Teleport_SwitchEffect
MUTATIONS["Teleport_SwitchEffect"] = {
    "source_symbol": "Teleport_SwitchEffect",
    "before": "wDuelDisplayedScreen = 0u;",
    "after": "wDuelDisplayedScreen = 1u;",
    "case_ids": ["Teleport_SwitchEffect-0", "Teleport_SwitchEffect-1"],
}
# <<< factory-mutation Teleport_SwitchEffect
# >>> factory-mutation SetDamageToATimes20
MUTATIONS["SetDamageToATimes20"] = {
    "source_symbol": "SetDamageToATimes20",
    "before": "hl = (uint16_t)(hl + de);",
    "after": "hl = (uint16_t)(hl - de);",
    "case_ids": ["SetDamageToATimes20-1", "SetDamageToATimes20-2", "SetDamageToATimes20-3"],
}
# <<< factory-mutation SetDamageToATimes20
# >>> factory-mutation CreateTrainerCardListFromDiscardPile
MUTATIONS["CreateTrainerCardListFromDiscardPile"] = {
	"source_symbol": "CreateTrainerCardListFromDiscardPile",
	"before": "return (CreateTrainerCardListFromDiscardPileResult){TX_ThereAreNoTrainerCardsInDiscardPileText, 0x90u};",
	"after": "return (CreateTrainerCardListFromDiscardPileResult){TX_ThereAreNoTrainerCardsInDiscardPileText, 0x10u};",
	"case_ids": ["CreateTrainerCardListFromDiscardPile-0", "CreateTrainerCardListFromDiscardPile-1", "CreateTrainerCardListFromDiscardPile-2"],
}
# <<< factory-mutation CreateTrainerCardListFromDiscardPile
# >>> factory-mutation CreateEnergyCardListFromDiscardPile
MUTATIONS["CreateEnergyCardListFromDiscardPile"] = {
	"source_symbol": "CreateEnergyCardListFromDiscardPile",
	"before": "uint8_t f = (first == 0xFFu) ? 0x90u : 0x00u;",
	"after": "uint8_t f = (first == 0xFFu) ? 0x80u : 0x00u;",
	"case_ids": ["CreateEnergyCardListFromDiscardPile-0", "CreateEnergyCardListFromDiscardPile-1"],
}
# <<< factory-mutation CreateEnergyCardListFromDiscardPile
# >>> factory-mutation GetAttackName
MUTATIONS["GetAttackName"] = {
	"source_symbol": "GetAttackName",
	"before": "uint16_t addr = (e == 0u) ? wLoadedCard1Atk1Name_ADDR : wLoadedCard1Atk2Name_ADDR;",
	"after": "uint16_t addr = (e != 0u) ? wLoadedCard1Atk1Name_ADDR : wLoadedCard1Atk2Name_ADDR;",
	"case_ids": ["GetAttackName-0", "GetAttackName-1"],
}
# <<< factory-mutation GetAttackName
# >>> factory-mutation ClefableMinimizeEffect
MUTATIONS["ClefableMinimizeEffect"] = {
    "source_symbol": "ClefableMinimizeEffect",
    "before": "\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_20);",
    "after": "\treturn (uint16_t)(0u & ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_20));",
    "case_ids": ["ClefableMinimizeEffect-0", "ClefableMinimizeEffect-1"],
}
# <<< factory-mutation ClefableMinimizeEffect
# >>> factory-mutation HandleAIMetronomeEffect
MUTATIONS["HandleAIMetronomeEffect"] = {
    "source_symbol": "HandleAIMetronomeEffect",
    "before": "\t(void)0;",
    "after": "\tgb_write8(0xC100u, 0xFFu);",
    "case_ids": ["HandleAIMetronomeEffect-0", "HandleAIMetronomeEffect-1"],
}
# <<< factory-mutation HandleAIMetronomeEffect
# >>> factory-mutation ParalysisEffect
MUTATIONS["ParalysisEffect"] = {
    "source_symbol": "ParalysisEffect",
    "before": "return QueueStatusCondition(PSN_DBLPSN, PARALYZED);",
    "after": "return QueueStatusCondition(PSN_DBLPSN, CONFUSED);",
    "case_ids": ["ParalysisEffect-0", "ParalysisEffect-1"],
}
# <<< factory-mutation ParalysisEffect
# >>> factory-mutation ConfusionEffect
MUTATIONS["ConfusionEffect"] = {
    "source_symbol": "ConfusionEffect",
    "before": "return QueueStatusCondition(PSN_DBLPSN, CONFUSED);",
    "after": "return QueueStatusCondition(PSN_DBLPSN, PARALYZED);",
    "case_ids": ["ConfusionEffect-0", "ConfusionEffect-1"],
}
# <<< factory-mutation ConfusionEffect
# >>> factory-mutation InvisibleWallEffect
MUTATIONS["InvisibleWallEffect"] = {
    "source_symbol": "InvisibleWallEffect",
    "before": "\treturn (uint8_t)((f & 0x80u) | 0x10u);",
    "after": "\treturn (uint8_t)((f & 0x80u) | 0x20u);",
    "case_ids": ["InvisibleWallEffect-0", "InvisibleWallEffect-1", "InvisibleWallEffect-2"],
}
# <<< factory-mutation InvisibleWallEffect
# >>> factory-mutation CheckIfDefendingPokemonHasAnyAttack
MUTATIONS["CheckIfDefendingPokemonHasAnyAttack"] = {
	"source_symbol": "CheckIfDefendingPokemonHasAnyAttack",
	"before": "f = (category == 0u) ? 0x80u : 0x00u;",
	"after": "f = (category == 0u) ? 0x00u : 0x80u;",
	"case_ids": ["CheckIfDefendingPokemonHasAnyAttack-0", "CheckIfDefendingPokemonHasAnyAttack-1"],
}
# <<< factory-mutation CheckIfDefendingPokemonHasAnyAttack
# >>> factory-mutation UpdateDevolvedCardHPAndStage
MUTATIONS["UpdateDevolvedCardHPAndStage"] = {
	"source_symbol": "UpdateDevolvedCardHPAndStage",
	"before": "uint8_t new_hp = (new_max_hp < damage) ? 0u : (uint8_t)(new_max_hp - damage);",
	"after": "uint8_t new_hp = (new_max_hp < damage) ? 0u : (uint8_t)(new_max_hp + damage);",
	"case_ids": ["UpdateDevolvedCardHPAndStage-0", "UpdateDevolvedCardHPAndStage-1"],
}
# <<< factory-mutation UpdateDevolvedCardHPAndStage
# >>> factory-mutation DodrioRage_DamageBoostEffect
MUTATIONS["DodrioRage_DamageBoostEffect"] = {
    "source_symbol": "DodrioRage_DamageBoostEffect",
    "before": "AddToDamage(r.a);",
    "after": "AddToDamage((uint8_t)(r.a + 1u));",
    "case_ids": ["DodrioRage_DamageBoostEffect-0", "DodrioRage_DamageBoostEffect-1", "DodrioRage_DamageBoostEffect-2", "DodrioRage_DamageBoostEffect-3"],
}
# <<< factory-mutation DodrioRage_DamageBoostEffect
# >>> factory-mutation DragonairSlam_AIEffect
MUTATIONS["DragonairSlam_AIEffect"] = {
    "source_symbol": "DragonairSlam_AIEffect",
    "before": "SetExpectedAIDamage(30u, 0u, 60u);",
    "after": "SetExpectedAIDamage(31u, 0u, 60u);",
    "case_ids": ["DragonairSlam_AIEffect-0", "DragonairSlam_AIEffect-1", "DragonairSlam_AIEffect-2"],
}
# <<< factory-mutation DragonairSlam_AIEffect
# >>> factory-mutation CheckIfPlayAreaHasAnyDamage
MUTATIONS["CheckIfPlayAreaHasAnyDamage"] = {
    "source_symbol": "CheckIfPlayAreaHasAnyDamage",
    "before": "uint32_t n = count.a ? count.a : 0x100u;",
    "after": "uint32_t n = count.a;",
    "case_ids": ["CheckIfPlayAreaHasAnyDamage-4"],
}
# <<< factory-mutation CheckIfPlayAreaHasAnyDamage
# >>> factory-mutation CreateEnergyCardListFromDiscardPile_OnlyBasic
MUTATIONS["CreateEnergyCardListFromDiscardPile_OnlyBasic"] = {
    "source_symbol": "CreateEnergyCardListFromDiscardPile_OnlyBasic",
    "before": "\treturn CreateEnergyCardListFromDiscardPile(0x01u);",
    "after": "\tCreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile(0x01u); return (CreateEnergyCardListFromDiscardPileResult){r.hl, 0x00u};",
    "case_ids": ["CreateEnergyCardListFromDiscardPile_OnlyBasic-0", "CreateEnergyCardListFromDiscardPile_OnlyBasic-1"],
}
# <<< factory-mutation CreateEnergyCardListFromDiscardPile_OnlyBasic
# >>> factory-mutation KabutoArmorEffect
MUTATIONS["KabutoArmorEffect"] = {
    "source_symbol": "KabutoArmorEffect",
    "before": "uint8_t KabutoArmorEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t KabutoArmorEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x20u);\n}",
    "case_ids": ["KabutoArmorEffect-0", "KabutoArmorEffect-1", "KabutoArmorEffect-2"],
}
# <<< factory-mutation KabutoArmorEffect
# >>> factory-mutation CuboneRage_DamageBoostEffect
MUTATIONS["CuboneRage_DamageBoostEffect"] = {
    "source_symbol": "CuboneRage_DamageBoostEffect",
    "before": "\tAddToDamage(r.a);",
    "after": "\tAddToDamage((uint8_t)(r.a + 1u));",
    "case_ids": ["CuboneRage_DamageBoostEffect-0", "CuboneRage_DamageBoostEffect-1",
                 "CuboneRage_DamageBoostEffect-2", "CuboneRage_DamageBoostEffect-3",
                 "CuboneRage_DamageBoostEffect-4"],
}
# <<< factory-mutation CuboneRage_DamageBoostEffect
# >>> factory-mutation PoisonEffect
MUTATIONS["PoisonEffect"] = {
    "source_symbol": "PoisonEffect",
    "before": "return QueueStatusCondition(CNF_SLP_PRZ, POISONED);",
    "after": "return QueueStatusCondition(CNF_SLP_PRZ, DOUBLE_POISONED);",
    "case_ids": ["PoisonEffect-0", "PoisonEffect-1"],
}
# <<< factory-mutation PoisonEffect
# >>> factory-mutation DoublePoisonEffect
MUTATIONS["DoublePoisonEffect"] = {
    "source_symbol": "DoublePoisonEffect",
    "before": "return QueueStatusCondition(CNF_SLP_PRZ, DOUBLE_POISONED);",
    "after": "return QueueStatusCondition(CNF_SLP_PRZ, POISONED);",
    "case_ids": ["DoublePoisonEffect-0", "DoublePoisonEffect-1"],
}
# <<< factory-mutation DoublePoisonEffect
# >>> factory-mutation LoadCardNameAndInputColor
MUTATIONS["LoadCardNameAndInputColor"] = {"source_symbol": "LoadCardNameAndInputColor", "before": "\tCOLOR_TEXT_LIGHTNING,", "after": "\tCOLOR_TEXT_WATER,", "case_ids": ["LoadCardNameAndInputColor-2", "LoadCardNameAndInputColor-3"]}
# <<< factory-mutation LoadCardNameAndInputColor
# >>> factory-mutation AIPickEnergyCardToDiscardFromDefendingPokemon
MUTATIONS["AIPickEnergyCardToDiscardFromDefendingPokemon"] = {
    "source_symbol": "AIPickEnergyCardToDiscardFromDefendingPokemon",
    "before": "return (AIPickEnergyCardToDiscardResult){0xFFu};",
    "after": "return (AIPickEnergyCardToDiscardResult){0xFEu};",
    "case_ids": ["AIPickEnergyCardToDiscardFromDefendingPokemon-0"],
}
# <<< factory-mutation AIPickEnergyCardToDiscardFromDefendingPokemon
# >>> factory-mutation AIFindTargetForBenchAttack
MUTATIONS["AIFindTargetForBenchAttack"] = {
    "source_symbol": "AIFindTargetForBenchAttack",
    "before": "return (AIFindTargetForBenchAttackResult){target};",
    "after": "return (AIFindTargetForBenchAttackResult){(uint8_t)(target + 1u)};",
    "case_ids": ["AIFindTargetForBenchAttack-0"],
}
# <<< factory-mutation AIFindTargetForBenchAttack
# >>> factory-mutation ApplyExtraWaterEnergyDamageBonus
MUTATIONS["ApplyExtraWaterEnergyDamageBonus"] = {
    "source_symbol": "ApplyExtraWaterEnergyDamageBonus",
    "before": "wAIMinDamage = wDamage;",
    "after": "wAIMinDamage = (uint8_t)(wDamage + 1u);",
    "case_ids": ["ApplyExtraWaterEnergyDamageBonus-0"],
}
# <<< factory-mutation ApplyExtraWaterEnergyDamageBonus
# >>> factory-mutation OmastarSpikeCannon_AIEffect
MUTATIONS["OmastarSpikeCannon_AIEffect"] = {
    "source_symbol": "OmastarSpikeCannon_AIEffect",
    "before": "\tSetExpectedAIDamage((uint8_t)30u, 0u, 60u);",
    "after": "\tSetExpectedAIDamage((uint8_t)30u, 0u, 61u);",
    "case_ids": ["OmastarSpikeCannon_AIEffect-0"],
}
# <<< factory-mutation OmastarSpikeCannon_AIEffect
# >>> factory-mutation ClairvoyanceEffect
MUTATIONS["ClairvoyanceEffect"] = {
    "source_symbol": "ClairvoyanceEffect",
    "before": "return (uint8_t)((f & 0x80u) | (uint8_t)0x10u);",
    "after": "return (uint8_t)((f & 0x80u) | (uint8_t)0x00u);",
    "case_ids": ["ClairvoyanceEffect-0"],
}
# <<< factory-mutation ClairvoyanceEffect
# >>> factory-mutation KrabbyCallForFamily_AISelectEffect
MUTATIONS["KrabbyCallForFamily_AISelectEffect"] = {"source_symbol": "KrabbyCallForFamily_AISelectEffect", "before": "if ((uint8_t)card_id == KRABBY)", "after": "if ((uint8_t)card_id != KRABBY)", "case_ids": ["KrabbyCallForFamily_AISelectEffect-0", "KrabbyCallForFamily_AISelectEffect-1"]}
# <<< factory-mutation KrabbyCallForFamily_AISelectEffect
# >>> factory-mutation CreateListOfEnergyAttachedToArena
MUTATIONS["CreateListOfEnergyAttachedToArena"] = {
    "source_symbol": "CreateListOfEnergyAttachedToArena",
    "before": "gb_write8(dst, 0xFFu);",
    "after": "gb_write8(dst, 0xFEu);",
    "case_ids": ["CreateListOfEnergyAttachedToArena-0", "CreateListOfEnergyAttachedToArena-1"],
}
# <<< factory-mutation CreateListOfEnergyAttachedToArena
# >>> factory-mutation HandleNoDamageOrEffect
MUTATIONS["HandleNoDamageOrEffect"] = {
    "source_symbol": "HandleNoDamageOrEffect",
    "before": "return (HandleNoDamageOrEffectResult){(uint8_t)(0x10u | (check.hl == 0u ? 0x80u : 0x00u)), check.hl};",
    "after": "return (HandleNoDamageOrEffectResult){0x00u, check.hl};",
    "case_ids": ["HandleNoDamageOrEffect-1", "HandleNoDamageOrEffect-2"],
}
# <<< factory-mutation HandleNoDamageOrEffect
# >>> factory-mutation ArcanineFlamethrower_CheckEnergy
MUTATIONS["ArcanineFlamethrower_CheckEnergy"] = {"source_symbol": "ArcanineFlamethrower_CheckEnergy", "before": "\tuint16_t hl = NotEnoughFireEnergyText;", "after": "\tuint16_t hl = (uint16_t)(NotEnoughFireEnergyText + 1u);", "case_ids": ["ArcanineFlamethrower_CheckEnergy-0", "ArcanineFlamethrower_CheckEnergy-1"]}
# <<< factory-mutation ArcanineFlamethrower_CheckEnergy
# >>> factory-mutation ArcanineFlamethrower_DiscardEffect
MUTATIONS["ArcanineFlamethrower_DiscardEffect"] = {"source_symbol": "ArcanineFlamethrower_DiscardEffect", "before": "\tuint8_t card = gb_read8(hTemp_ffa0_ADDR);", "after": "\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR + 1u));", "case_ids": ["ArcanineFlamethrower_DiscardEffect-1"]}
# <<< factory-mutation ArcanineFlamethrower_DiscardEffect
# >>> factory-mutation PoisonWhip_AIEffect
MUTATIONS["PoisonWhip_AIEffect"] = {
    "source_symbol": "PoisonWhip_AIEffect",
    "before": "UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);",
    "after": "UpdateExpectedAIDamage_AccountForPoison(11u, 10u, 10u);",
    "case_ids": ["PoisonWhip_AIEffect-0"],
}
# <<< factory-mutation PoisonWhip_AIEffect
# >>> factory-mutation SolarPower_CheckUse
MUTATIONS["SolarPower_CheckUse"] = {
    "source_symbol": "SolarPower_CheckUse",
    "before": "return (SolarPowerCheckUseResult){0x10u, 0x00CAu};",
    "after": "return (SolarPowerCheckUseResult){0x90u, 0x00CAu};",
    "case_ids": ["SolarPower_CheckUse-0"],
}
# <<< factory-mutation SolarPower_CheckUse
# >>> factory-mutation DevolutionBeam_LoadAnimation
MUTATIONS["DevolutionBeam_LoadAnimation"] = {"source_symbol": "DevolutionBeam_LoadAnimation", "before": "wLoadedAttackAnimation = ATK_ANIM_NONE;", "after": "wLoadedAttackAnimation = 1u;", "case_ids": ["DevolutionBeam_LoadAnimation-0", "DevolutionBeam_LoadAnimation-1"]}
# <<< factory-mutation DevolutionBeam_LoadAnimation
# >>> factory-mutation CheckIfTurnDuelistHasEvolvedCards
MUTATIONS["CheckIfTurnDuelistHasEvolvedCards"] = {
    "source_symbol": "CheckIfTurnDuelistHasEvolvedCards",
    "before": "return (CheckAttackResult){0x90u};",
    "after": "return (CheckAttackResult){0x80u};",
    "case_ids": ["CheckIfTurnDuelistHasEvolvedCards-0"],
}
# <<< factory-mutation CheckIfTurnDuelistHasEvolvedCards
# >>> factory-mutation FindFirstNonBasicCardInPlayArea
MUTATIONS["FindFirstNonBasicCardInPlayArea"] = {
    "source_symbol": "FindFirstNonBasicCardInPlayArea",
    "before": "return (FindFirstNonBasicCardInPlayAreaResult){0x00u, 0x80u};",
    "after": "return (FindFirstNonBasicCardInPlayAreaResult){0x00u, 0x00u};",
    "case_ids": ["FindFirstNonBasicCardInPlayArea-0"],
}
# <<< factory-mutation FindFirstNonBasicCardInPlayArea
# >>> factory-mutation Wildfire_AISelectEffect
MUTATIONS["Wildfire_AISelectEffect"] = {"source_symbol": "Wildfire_AISelectEffect", "before": "\tuint8_t a = 0x00u;", "after": "\tuint8_t a = 0x01u;", "case_ids": ["Wildfire_AISelectEffect-0", "Wildfire_AISelectEffect-1", "Wildfire_AISelectEffect-2"]}
# <<< factory-mutation Wildfire_AISelectEffect
# >>> factory-mutation FireBlast_CheckEnergy
MUTATIONS["FireBlast_CheckEnergy"] = {"source_symbol": "FireBlast_CheckEnergy", "before": "NotEnoughFireEnergyText};", "after": "0u};", "case_ids": ["FireBlast_CheckEnergy-0", "FireBlast_CheckEnergy-1", "FireBlast_CheckEnergy-2"]}
# <<< factory-mutation FireBlast_CheckEnergy
# >>> factory-mutation BigEggsplosion_AIEffect
MUTATIONS["BigEggsplosion_AIEffect"] = {"source_symbol": "BigEggsplosion_AIEffect", "before": "\twAIMinDamage = 0u;", "after": "\twAIMinDamage = 1u;", "case_ids": ["BigEggsplosion_AIEffect-0", "BigEggsplosion_AIEffect-1", "BigEggsplosion_AIEffect-2"]}
# <<< factory-mutation BigEggsplosion_AIEffect
# >>> factory-mutation Thrash_AIEffect
MUTATIONS["Thrash_AIEffect"] = {"source_symbol": "Thrash_AIEffect", "before": "\tSetExpectedAIDamage(35u, 30u, 40u);", "after": "\tSetExpectedAIDamage(36u, 30u, 40u);", "case_ids": ["Thrash_AIEffect-0", "Thrash_AIEffect-1", "Thrash_AIEffect-2"]}
# <<< factory-mutation Thrash_AIEffect
# >>> factory-mutation Prophecy_CheckDeck
MUTATIONS["Prophecy_CheckDeck"] = {"source_symbol": "Prophecy_CheckDeck", "before": "\tif (turn.a < DECK_SIZE)", "after": "\tif (turn.a >= DECK_SIZE)", "case_ids": ["Prophecy_CheckDeck-0", "Prophecy_CheckDeck-1"]}
# <<< factory-mutation Prophecy_CheckDeck
# >>> factory-mutation TryGiveDamageCounter_DamageSwap
MUTATIONS["TryGiveDamageCounter_DamageSwap"] = {"source_symbol": "TryGiveDamageCounter_DamageSwap", "before": "uint8_t new_hp = (uint8_t)(10u + gb_read8(source_hp));", "after": "uint8_t new_hp = (uint8_t)(20u + gb_read8(source_hp));", "case_ids": ["TryGiveDamageCounter_DamageSwap-0", "TryGiveDamageCounter_DamageSwap-1", "TryGiveDamageCounter_DamageSwap-2"]}
# <<< factory-mutation TryGiveDamageCounter_DamageSwap
# >>> factory-mutation TransparencyEffect
MUTATIONS["TransparencyEffect"] = {"source_symbol": "TransparencyEffect", "before": "\treturn 0x10u;", "after": "\treturn 0x00u;", "case_ids": ["TransparencyEffect-0", "TransparencyEffect-1"]}
# <<< factory-mutation TransparencyEffect
