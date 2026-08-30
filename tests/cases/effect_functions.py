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
# >>> factory SleepEffect
CONTRACT["SleepEffect"] = {"compare": (), "preserve": ()}
CASES["SleepEffect"] = [
    {"wram": {0xFF97: b"\x00", 0xCC05: b"\x01"},
     "read": {0xCCCE: 3, 0xCCCD: 1}},
    {"wram": {0xFF97: b"\x01", 0xCC05: b"\x00"},
     "read": {0xCCCE: 3, 0xCCCD: 1}},
    dict(POISON, wram={0xFF97: b"\x00", 0xCC05: b"\x01"},
         read={0xCCCE: 3, 0xCCCD: 1}),
]
# <<< factory SleepEffect
# >>> factory SetDefiniteDamage
CONTRACT["SetDefiniteDamage"] = {"compare": (), "preserve": ()}
CASES["SetDefiniteDamage"] = [
    {"a": 0x00, "wram": {0xCCB9: b"\x12\x34", 0xCCBA: b"\x56", 0xCCBB: b"\x78"},
     "read": {0xCCB9: 2, 0xCCBA: 1, 0xCCBB: 1}},
    {"a": 0xFF, "wram": {0xCCB9: b"\xAA\xBB", 0xCCBA: b"\xCC", 0xCCBB: b"\xDD"},
     "read": {0xCCB9: 2, 0xCCBA: 1, 0xCCBB: 1}},
    dict(POISON, a=0x42, wram={0xCCB9: b"\x99\x88", 0xCCBA: b"\x77", 0xCCBB: b"\x66"},
         read={0xCCB9: 2, 0xCCBA: 1, 0xCCBB: 1}),
]
# <<< factory SetDefiniteDamage



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

# >>> factory Barrier_CheckEnergy
CONTRACT["Barrier_CheckEnergy"] = {"compare": ("a", "f", "b", "c", "d", "hl"), "preserve": ("b", "c", "d")}
CASES["Barrier_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
]
# <<< factory Barrier_CheckEnergy

# >>> factory ResetDevolvedCardStatus
CONTRACT["ResetDevolvedCardStatus"] = {"compare": ("a",), "preserve": ()}
CASES["ResetDevolvedCardStatus"] = [
    {"wram": {0xFF9D: b"\x00", 0xFF9E: b"\xC0", 0xC0F0: b"\x01", 0xC0D4: b"\x02", 0xC0C2: b"\x04"},
     "read": {0xC0F0: 8, 0xC0D4: 1, 0xC0C2: 1}},
    {"wram": {0xFF9D: b"\x01", 0xFF9E: b"\xC0", 0xC0D5: b"\x02", 0xC0C3: b"\x04"},
     "read": {0xC0D5: 1, 0xC0C3: 1}},
    dict(POISON, wram={0xFF9D: b"\x00", 0xFF9E: b"\xC0", 0xC0F0: b"\x01", 0xC0D4: b"\x02", 0xC0C2: b"\x04"},
         read={0xC0F0: 8, 0xC0D4: 1, 0xC0C2: 1}),
    dict(POISON, wram={0xFF9D: b"\x01", 0xFF9E: b"\xC0", 0xC0D5: b"\x02", 0xC0C3: b"\x04"},
         read={0xC0D5: 1, 0xC0C3: 1}),
]
# <<< factory ResetDevolvedCardStatus

# >>> factory EeveeQuickAttack_AIEffect
CONTRACT["EeveeQuickAttack_AIEffect"] = {"compare": (), "preserve": ()}
CASES["EeveeQuickAttack_AIEffect"] = [
    {"wram": {0xCCBB: b"\x00", 0xCCBC: b"\x00", 0xCCB9: b"\x00"}},
    dict(POISON, wram={0xCCBB: b"\xAA", 0xCCBC: b"\xBB", 0xCCB9: b"\xCC"}),
]
# <<< factory EeveeQuickAttack_AIEffect

# >>> factory MirrorMove_AIEffect
CONTRACT["MirrorMove_AIEffect"] = {"compare": (), "preserve": ()}
CASES["MirrorMove_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x00\x00", 0xCCBB: b"\xAA", 0xCCBC: b"\xBB"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x2A\x01", 0xCCBB: b"\xAA", 0xCCBC: b"\xBB"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F3: b"\x7F\x00", 0xCCBB: b"\xAA", 0xCCBC: b"\xBB"}),
    dict(POISON, a=0x11, wram={0xFF97: b"\xC2", 0xC2F3: b"\xFF\xFF", 0xCCBB: b"\xAA", 0xCCBC: b"\xBB"}),
]
# <<< factory MirrorMove_AIEffect

# >>> factory MirrorMove_InitialEffect1
CONTRACT["MirrorMove_InitialEffect1"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["MirrorMove_InitialEffect1"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x00\x00\x00\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x01\x00\x00\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x00\x01\x00\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x00\x00\x01\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x00\x00\x00\x01"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F3: b"\x00\x00\x00\x00"}),
]
# <<< factory MirrorMove_InitialEffect1

# >>> factory FuryAttack_AIEffect
CONTRACT["FuryAttack_AIEffect"] = {"compare": (), "preserve": ()}
CASES["FuryAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory FuryAttack_AIEffect

# >>> factory RetreatAidEffect
CONTRACT["RetreatAidEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                                "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["RetreatAidEffect"] = [{}, dict(POISON), {"f": 0x80}]
# <<< factory RetreatAidEffect

# >>> factory FriendshipSong_BenchCheck
CONTRACT["FriendshipSong_BenchCheck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["FriendshipSong_BenchCheck"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x05"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x06"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x07"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EF: b"\x00"}),
]
# <<< factory FriendshipSong_BenchCheck

# >>> factory ExpandEffect
CONTRACT["ExpandEffect"] = {"compare": (), "preserve": ()}
CASES["ExpandEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2E7: b"\x00"}, "read": {0xC2CB: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2E7: b"\xFF"}, read={0xC2E7: 1}),
]
# <<< factory ExpandEffect

# >>> factory CheckIfThereAreAnyEnergyCardsAttached
CONTRACT["CheckIfThereAreAnyEnergyCardsAttached"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfThereAreAnyEnergyCardsAttached"] = [
    {"wram": {hWhoseTurn: b"\xC2"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x01"}),
]
# <<< factory CheckIfThereAreAnyEnergyCardsAttached

# >>> factory PokeBall_DeckCheck
CONTRACT["PokeBall_DeckCheck"] = {"compare": ("a", "f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["PokeBall_DeckCheck"] = [
    {},
    dict(POISON),
    {"a": 1},
    {"a": 0xFF},
]
# <<< factory PokeBall_DeckCheck

# >>> factory Recycle_DiscardPileCheck
CONTRACT["Recycle_DiscardPileCheck"] = {"compare": ("f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["Recycle_DiscardPileCheck"] = [
    {},
    dict(POISON),
    {"a": 1},
    {"a": 0xFF},
]
# <<< factory Recycle_DiscardPileCheck

# >>> factory CreateBasicPokemonCardListFromDiscardPile
CONTRACT["CreateBasicPokemonCardListFromDiscardPile"] = {"compare": ("f",), "preserve": ()}
CASES["CreateBasicPokemonCardListFromDiscardPile"] = [
    {"wram": {0xC37E: b"\x00"}, "read": {0xC510: 1}},
    dict(POISON, wram={0xC37E: b"\x00"}),
    {"wram": {0xC37E: b"\x01", 0xC510: b"\x00"}},
]
# <<< factory CreateBasicPokemonCardListFromDiscardPile


# >>> factory CreatePokemonCardListFromHand
CONTRACT["CreatePokemonCardListFromHand"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b",)}
CASES["CreatePokemonCardListFromHand"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00"}),
]
# <<< factory CreatePokemonCardListFromHand

# >>> factory Pokedex_DeckCheck
CONTRACT["Pokedex_DeckCheck"] = {"compare": ("a", "f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["Pokedex_DeckCheck"] = [
    {},
    dict(POISON),
]
# <<< factory Pokedex_DeckCheck

# >>> factory Pokedex_OrderDeckCardsEffect
CONTRACT["Pokedex_OrderDeckCardsEffect"] = {
    "compare": ("a", "f", "c", "hl", "b", "d", "e"),
    "preserve": ("b", "d", "e"),
}
CASES["Pokedex_OrderDeckCardsEffect"] = [
    {"c": 0x77, "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00",
                         0xC27E: b"\x01\x02\x03", 0xFFA0: b"\x02\xFF"},
     "read": {0xC2BA: 1, 0xC202: 1, 0xC27E: 3, 0xFFA0: 2}},
    {"a": 0x05, "b": 0xBB, "d": 0xDD, "e": 0xEE, "c": 0x66,
     "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00",
              0xC27E: b"\x01\x02\x03\x04", 0xFFA0: b"\x02\x03\xFF"},
     "read": {0xC2BA: 1, 0xC202: 1, 0xC203: 1, 0xC27E: 4, 0xFFA0: 3}},
    {"a": 0xFF, "b": 0x11, "d": 0x22, "e": 0x33, "c": 0x44,
     "wram": {0xFF97: b"\xC3", 0xC3BA: b"\x01",
              0xC37E: b"\x05\x06\x07", 0xFFA0: b"\x05\x06\x07\xFF"},
     "read": {0xC3BA: 1, 0xC305: 1, 0xC306: 1, 0xC307: 1, 0xC37E: 3,
              0xFFA0: 4}},
    dict(POISON, c=0x99, wram={0xFF97: b"\xC2", 0xC2BA: b"\x00",
                               0xC27E: b"\x08\x09", 0xFFA0: b"\x08\xFF"},
         read={0xC2BA: 1, 0xC208: 1, 0xC27E: 2, 0xFFA0: 2}),
]
# <<< factory Pokedex_OrderDeckCardsEffect

# >>> factory Maintenance_HandCheck
CONTRACT["Maintenance_HandCheck"] = {
    "compare": ("a", "f", "hl", "b", "c", "d", "e"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["Maintenance_HandCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"},
     "read": {0xC2EE: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x02"},
     "read": {0xC2EE: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x03"},
     "read": {0xC2EE: 1}},
    {"wram": {0xFF97: b"\xC3", 0xC3EE: b"\x09"},
     "read": {0xC3EE: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\xFF"},
         read={0xC2EE: 1}),
]
# <<< factory Maintenance_HandCheck

# >>> factory DevolutionSpray_PlayAreaEvolutionCheck
CONTRACT["DevolutionSpray_PlayAreaEvolutionCheck"] = {"compare": ("hl", "f"), "preserve": ()}
CASES["DevolutionSpray_PlayAreaEvolutionCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC2BB: b"\x00\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x00"}),
]
# <<< factory DevolutionSpray_PlayAreaEvolutionCheck

# >>> factory SpitPoison_AIEffect
CONTRACT["SpitPoison_AIEffect"] = {"compare": (), "preserve": ()}
CASES["SpitPoison_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory SpitPoison_AIEffect

# >>> factory GloomPoisonPowder_AIEffect
CONTRACT["GloomPoisonPowder_AIEffect"] = {"compare": (), "preserve": ()}
CASES["GloomPoisonPowder_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory GloomPoisonPowder_AIEffect

# >>> factory FoulOdorEffect
CONTRACT["FoulOdorEffect"] = {"compare": ("f",), "preserve": ()}
CASES["FoulOdorEffect"] = [
    {"wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x01"},
     "read": {hWhoseTurn: 1, wWhoseTurn: 1, wStatusConditionQueue: 6,
              wStatusConditionQueueIndex: 1}},
    {"wram": {hWhoseTurn: b"\x01", wWhoseTurn: b"\x00"},
     "read": {hWhoseTurn: 1, wWhoseTurn: 1, wStatusConditionQueue: 6,
              wStatusConditionQueueIndex: 1}},
    dict(POISON, wram={hWhoseTurn: b"\x00", wWhoseTurn: b"\x01"},
         read={hWhoseTurn: 1, wWhoseTurn: 1, wStatusConditionQueue: 6,
               wStatusConditionQueueIndex: 1}),
]
# <<< factory FoulOdorEffect

# >>> factory KakunaPoisonPowder_AIEffect
CONTRACT["KakunaPoisonPowder_AIEffect"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c")}
CASES["KakunaPoisonPowder_AIEffect"] = [
    dict(POISON, wram={0xCCB9: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 2}),
    dict(POISON, a=0x01, wram={0xCCB9: b"\x10"}, read={0xCCB9: 1, 0xCCBB: 2}),
    dict(POISON, b=0x02, wram={0xCCB9: b"\x20"}, read={0xCCB9: 1, 0xCCBB: 2}),
    dict(POISON, c=0x03, wram={0xCCB9: b"\x30"}, read={0xCCB9: 1, 0xCCBB: 2}),
]
# <<< factory KakunaPoisonPowder_AIEffect


# >>> factory SwordsDanceEffect
CONTRACT["SwordsDanceEffect"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["SwordsDanceEffect"] = [
    {"wram": {0xCCC3: b"\x00"}, "read": {0xCCC3: 1}},
    {"wram": {0xCCC3: b"\x2E"}, "read": {0xCCC3: 1}},
    dict(POISON, wram={0xCCC3: b"\x2E"}, read={0xCCC3: 1}),
]
# <<< factory SwordsDanceEffect


# >>> factory Twineedle_AIEffect
CONTRACT["Twineedle_AIEffect"] = {"compare": (), "preserve": ()}
CASES["Twineedle_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory Twineedle_AIEffect


# >>> factory BeedrillPoisonSting_AIEffect
CONTRACT["BeedrillPoisonSting_AIEffect"] = {"compare": (), "preserve": ()}
CASES["BeedrillPoisonSting_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory BeedrillPoisonSting_AIEffect


# >>> factory FoulGas_AIEffect
CONTRACT["FoulGas_AIEffect"] = {"compare": (), "preserve": ()}
CASES["FoulGas_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xCCB9: b"\x05"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xFF"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory FoulGas_AIEffect


# >>> factory Sprout_AISelectEffect
CONTRACT["Sprout_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Sprout_AISelectEffect"] = [
    {"c": 0, "d": 0, "e": 0, "read": {0xFFA0: 1}},
    dict(POISON, c=1, d=0x12, e=0x34, read={0xFFA0: 1}),
    {"c": 0xFF, "d": 0xFF, "e": 0xFF, "read": {0xFFA0: 1}},
]
# <<< factory Sprout_AISelectEffect


# >>> factory Teleport_CheckBench
CONTRACT["Teleport_CheckBench"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Teleport_CheckBench"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x02"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x02"}),
]
# <<< factory Teleport_CheckBench


# >>> factory Teleport_AISelectEffect
CONTRACT["Teleport_AISelectEffect"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["Teleport_AISelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x00", 0xCACA: b"\x12\x34\x56"}, "read": {0xFFA0: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xCACA: b"\x12\x34\x56"}, "read": {0xFFA0: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x06", 0xCACA: b"\xde\xad\xbe"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x04", 0xCACA: b"\x80\x01\xff"}, read={0xFFA0: 1}),
]
# <<< factory Teleport_AISelectEffect


# >>> factory HornHazard_AIEffect
CONTRACT["HornHazard_AIEffect"] = {"compare": (), "preserve": ()}
CASES["HornHazard_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory HornHazard_AIEffect


# >>> factory NidorinaDoubleKick_AIEffect
CONTRACT["NidorinaDoubleKick_AIEffect"] = {"compare": (), "preserve": ()}
CASES["NidorinaDoubleKick_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory NidorinaDoubleKick_AIEffect


# >>> factory NidorinoDoubleKick_AIEffect
CONTRACT["NidorinoDoubleKick_AIEffect"] = {"compare": (), "preserve": ()}
CASES["NidorinoDoubleKick_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory NidorinoDoubleKick_AIEffect

# >>> factory WeedlePoisonSting_AIEffect
CONTRACT["WeedlePoisonSting_AIEffect"] = {"compare": (), "preserve": ()}
CASES["WeedlePoisonSting_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory WeedlePoisonSting_AIEffect

# >>> factory BellsproutCallForFamily_AISelectEffect
CONTRACT["BellsproutCallForFamily_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["BellsproutCallForFamily_AISelectEffect"] = [
    {"c": 0, "d": 0, "e": 0, "read": {0xFFA0: 1}},
    dict(POISON, c=1, d=0x12, e=0x34, read={0xFFA0: 1}),
    {"c": 0xFF, "d": 0xFF, "e": 0xFF, "read": {0xFFA0: 1}},
]
# <<< factory BellsproutCallForFamily_AISelectEffect

# >>> factory WeezingSmog_AIEffect
CONTRACT["WeezingSmog_AIEffect"] = {"compare": (), "preserve": ()}
CASES["WeezingSmog_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xCCB9: b"\x05"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xFF"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory WeezingSmog_AIEffect

# >>> factory NidoranFFurySwipes_AIEffect
CONTRACT["NidoranFFurySwipes_AIEffect"] = {"compare": (), "preserve": ()}
CASES["NidoranFFurySwipes_AIEffect"] = [
    {"read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, a=0xFF, f=0xFF, hl=0x1234, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory NidoranFFurySwipes_AIEffect


# >>> factory NidoranFCallForFamily_AISelectEffect
CONTRACT["NidoranFCallForFamily_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["NidoranFCallForFamily_AISelectEffect"] = [
    {"c": 0, "d": 0, "e": 0, "read": {0xFFA0: 1}},
    dict(POISON, c=1, d=0x12, e=0x34, read={0xFFA0: 1}),
    {"c": 0xFF, "d": 0xFF, "e": 0xFF, "read": {0xFFA0: 1}},
]
# <<< factory NidoranFCallForFamily_AISelectEffect


# >>> factory ToxicGasEffect
CONTRACT["ToxicGasEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                              "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["ToxicGasEffect"] = [
    {},
    dict(POISON),
    {"f": 0x80},
]
# <<< factory ToxicGasEffect


# >>> factory Sludge_AIEffect
CONTRACT["Sludge_AIEffect"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c")}
CASES["Sludge_AIEffect"] = [
    dict(POISON, wram={0xCCB9: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 2}),
    dict(POISON, a=0x01, wram={0xCCB9: b"\x10"}, read={0xCCB9: 1, 0xCCBB: 2}),
    dict(POISON, b=0x02, wram={0xCCB9: b"\x20"}, read={0xCCB9: 1, 0xCCBB: 2}),
]
# <<< factory Sludge_AIEffect


# >>> factory KadabraRecover_DiscardEffect
CONTRACT["KadabraRecover_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["KadabraRecover_DiscardEffect"] = [
	{"wram": {0xFFA0: b"\x00"}},
	dict(POISON, wram={0xFFA0: b"\x05"}),
	{"a": 1, "f": 0x10, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 0x1234, "wram": {0xFFA0: b"\xFF"}},
]
# <<< factory KadabraRecover_DiscardEffect

# >>> factory PrimeapeFurySwipes_AIEffect
CONTRACT["PrimeapeFurySwipes_AIEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")}
CASES["PrimeapeFurySwipes_AIEffect"] = [{}, dict(POISON), {"a": 1, "f": 2, "b": 3, "c": 4, "d": 5, "e": 6, "hl": 7}]
# <<< factory PrimeapeFurySwipes_AIEffect

# >>> factory StretchKick_CheckBench
CONTRACT["StretchKick_CheckBench"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["StretchKick_CheckBench"] = [
    {"a": 0},
    dict(POISON),
    {"a": 1},
    {"a": 2},
    {"a": 3},
]
# <<< factory StretchKick_CheckBench


# >>> factory Cowardice_CheckUseAndBench
CONTRACT["Cowardice_CheckUseAndBench"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["Cowardice_CheckUseAndBench"] = [
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\x00", 0xC2EF: b"\x01", 0xC2BB: b"\x01\xFF\xFF\xFF\xFF\xFF\xFF", 0xC3BB: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2C2: b"\x10"}},
    {"wram": {0xFF9D: b"\x01", 0xFF97: b"\x00", 0xC2EF: b"\x02", 0xC2BB: b"\x01\x02\xFF", 0xC3BB: b"\xFF", 0xC2C3: b"\x10"}},
    dict(POISON, wram={0xFF9D: b"\x00", 0xFF97: b"\x00", 0xC2EF: b"\x02", 0xC2BB: b"\x01\x02\xFF", 0xC3BB: b"\xFF", 0xC2C2: b"\x00"}),
]
# <<< factory Cowardice_CheckUseAndBench



# >>> factory Cowardice_ReturnToHandEffect
CONTRACT["Cowardice_ReturnToHandEffect"] = {"compare": ("a",), "preserve": ()}
CASES["Cowardice_ReturnToHandEffect"] = [
    {"wram": {0xFFA0: b"\x00", 0xFFA1: b"\x01", 0xCAC2: b"\x05", 0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC2BB: b"\x01\x02\xFF\xFF\xFF\xFF\xFF", 0xC3BB: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\xFF"}},
    {"wram": {0xFFA0: b"\x01", 0xFFA1: b"\x02", 0xCAC2: b"\xFF", 0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC2BB: b"\x01\x02\xFF\xFF\xFF\xFF\xFF", 0xC3BB: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\xFF"}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xFFA1: b"\x03", 0xCAC2: b"\x03", 0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x01\xFF\xFF\xFF\xFF\xFF\xFF", 0xC3BB: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\xFF"}),
    dict(POISON, a=1, f=2, b=3, c=4, d=5, e=6, hl=7, wram={0xFFA0: b"\x01", 0xFFA1: b"\x04", 0xCAC2: b"\x00", 0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC2BB: b"\x01\x02\xFF\xFF\xFF\xFF\xFF", 0xC3BB: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\xFF"}),
]
# <<< factory Cowardice_ReturnToHandEffect




# >>> factory LightScreenEffect
CONTRACT["LightScreenEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["LightScreenEffect"] = [{}, dict(POISON)]
# <<< factory LightScreenEffect


# >>> factory StarmieRecover_CheckEnergyHP
CONTRACT["StarmieRecover_CheckEnergyHP"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d")}
CASES["StarmieRecover_CheckEnergyHP"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC200: b"\x10",
              0xC400: b"\x08\x03", 0xC2C8: b"\x28", 0xCC1B: b"\x00" * 8},
     "read": {0xCC1B: 8}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC200: b"\x10",
                       0xC400: b"\x08\x03", 0xC2C8: b"\x28", 0xCC1B: b"\x00" * 8},
         read={0xCC1B: 8}),
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC200: b"\x10\x10",
              0xC400: b"\x08\x03", 0xC2C8: b"\x28",
              0xCC1B: b"\x00\x00\x00\x01\x00\x00\x00\x00"},
     "read": {0xCC1B: 8}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC200: b"\x10\x10",
              0xC400: b"\x08\x03", 0xC2C8: b"\x05",
              0xCC1B: b"\x00\x00\x00\x01\x00\x00\x00\x00"},
     "read": {0xCC1B: 8}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC200: b"\x10\x10",
                       0xC400: b"\x08\x03", 0xC2C8: b"\x0A",
                       0xCC1B: b"\x00\x00\x00\x01\x00\x00\x00\x00"},
         read={0xCC1B: 8}),
]
# <<< factory StarmieRecover_CheckEnergyHP


# >>> factory StarmieRecover_DiscardEffect
CONTRACT["StarmieRecover_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["StarmieRecover_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA0: b"\x05"}),
    {"a": 0x7F, "f": 0x10, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 0x1234,
     "wram": {0xFFA0: b"\xFF"}},
]
# <<< factory StarmieRecover_DiscardEffect

# >>> factory CheckIfCardHasGrassEnergyAttached
CONTRACT["CheckIfCardHasGrassEnergyAttached"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d")}
CASES["CheckIfCardHasGrassEnergyAttached"] = [
    {"wram": {0xFF97: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x01"}},
    {"wram": {0xFF97: b"\xC2", 0xC200: b"\x10", 0xC400: b"\xCB"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC200: b"\x10", 0xC401: b"\x01"}),
]
# <<< factory CheckIfCardHasGrassEnergyAttached

# >>> factory GrimerMinimizeEffect
CONTRACT["GrimerMinimizeEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["GrimerMinimizeEffect"] = [
    {"wram": {0xFF97: b"\xC2"}, "read": {0xC2E7: 1}},
    {"a": 0x01, "wram": {0xFF97: b"\xC2"}, "read": {0xC2E7: 1}},
    dict(POISON, a=0xFF, wram={0xFF97: b"\xC2"}, read={0xC2E7: 1}),
]
# <<< factory GrimerMinimizeEffect

# >>> factory Quickfreeze_InitialEffect
CONTRACT["Quickfreeze_InitialEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Quickfreeze_InitialEffect"] = [
    {"f": 0x00},
    {"f": 0x80},
    dict(POISON),
]
# <<< factory Quickfreeze_InitialEffect


# >>> factory FocusEnergyEffect
CONTRACT["FocusEnergyEffect"] = {"compare": (), "preserve": ()}
CASES["FocusEnergyEffect"] = [
    {"wram": {0xCCC3: b"\x00", 0xFF97: b"\xC2", 0xC2E7: b"\x00"},
     "read": {0xC2E7: 1}},
    {"wram": {0xCCC3: b"\x5A", 0xFF97: b"\xC2", 0xC2E7: b"\x00"},
     "read": {0xC2E7: 1}},
    dict(POISON, wram={0xCCC3: b"\x5A", 0xFF97: b"\xC2", 0xC2E7: b"\x00"},
         read={0xC2E7: 1}),
]
# <<< factory FocusEnergyEffect


# >>> factory MagnetonSonicboom_UnaffectedByColorEffect
CONTRACT["MagnetonSonicboom_UnaffectedByColorEffect"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["MagnetonSonicboom_UnaffectedByColorEffect"] = [
	{"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2}},
	dict(POISON, wram={0xCCB9: b"\x12\x01"}, read={0xCCB9: 2}),
]
# <<< factory MagnetonSonicboom_UnaffectedByColorEffect

# >>> factory MagnetonSonicboom_NullEffect
CONTRACT["MagnetonSonicboom_NullEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["MagnetonSonicboom_NullEffect"] = [
	{"wram": {0xC100: b"\x00"}, "read": {0xC100: 1}},
	dict(POISON, wram={0xC100: b"\x5A"}, read={0xC100: 1}),
]
# <<< factory MagnetonSonicboom_NullEffect

# >>> factory ElectrodeSonicboom_UnaffectedByColorEffect
CONTRACT["ElectrodeSonicboom_UnaffectedByColorEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["ElectrodeSonicboom_UnaffectedByColorEffect"] = [
	{"wram": {0xCCB9: b"\x00\x00"}},
	dict(POISON, wram={0xCCB9: b"\x01\x02"}),
	{"wram": {0xCCB9: b"\xFF\x00"}},
]
# <<< factory ElectrodeSonicboom_UnaffectedByColorEffect

# >>> factory EnergySpike_AISelectEffect
CONTRACT["EnergySpike_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["EnergySpike_AISelectEffect"] = [{"read": {0xFFA0: 1}}, dict(POISON, wram={0xFFA0: b"\x55"}, read={0xFFA0: 1})]
# <<< factory EnergySpike_AISelectEffect

# >>> factory CometPunch_AIEffect
CONTRACT["CometPunch_AIEffect"] = {"compare": (), "preserve": ()}
CASES["CometPunch_AIEffect"] = [
	{"wram": {0xC000: b"\x00" * 0xF00}, "read": {0xC000: 0xF00}},
	dict(POISON, wram={0xC000: b"\x00" * 0xF00}, read={0xC000: 0xF00}),
	{"wram": {0xC000: b"\xFF" * 0xF00}, "read": {0xC000: 0xF00}},
]
# <<< factory CometPunch_AIEffect

# >>> factory Conversion1_WeaknessCheck
CONTRACT["Conversion1_WeaknessCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Conversion1_WeaknessCheck"] = [
    {"wram": {0xCC98: b"\x00"}},
    {"wram": {0xCC98: b"\x01"}},
    dict(POISON, wram={0xCC98: b"\x00"}),
    dict(POISON, wram={0xCC98: b"\x01"}),
]
# <<< factory Conversion1_WeaknessCheck

# >>> factory Conversion2_ResistanceCheck
CONTRACT["Conversion2_ResistanceCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Conversion2_ResistanceCheck"] = [
    {"wram": {0xCC99: b"\x00"}},
    {"wram": {0xCC99: b"\x01"}},
    dict(POISON, wram={0xCC99: b"\x00"}),
    dict(POISON, wram={0xCC99: b"\x01"}),
]
# <<< factory Conversion2_ResistanceCheck

# >>> factory ElectrodeSonicboom_NullEffect
CONTRACT["ElectrodeSonicboom_NullEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ElectrodeSonicboom_NullEffect"] = [{}, dict(POISON, wram={0xFFA0: b"\x5A"}), {"wram": {0xFFA0: b"\xA5"}}]
# <<< factory ElectrodeSonicboom_NullEffect

# >>> factory FirstAid_DamageCheck
CONTRACT["FirstAid_DamageCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["FirstAid_DamageCheck"] = [
    {},
    dict(POISON),
]
# <<< factory FirstAid_DamageCheck

# >>> factory DoTheWaveEffect
CONTRACT["DoTheWaveEffect"] = {"compare": (), "preserve": ()}
CASES["DoTheWaveEffect"] = [
	{"wram": {0xCCED: b"\x00"}, "read": {0xCC00: 0x100}},
	dict(POISON, wram={0xCCED: b"\x01"}, read={0xCC00: 0x100}),
	{"a": 1, "wram": {0xCCED: b"\xFE"}, "read": {0xCC00: 0x100}},
	{"a": 0xFF, "wram": {0xCCED: b"\x7F"}, "read": {0xCC00: 0x100}},
]
# <<< factory DoTheWaveEffect

# >>> factory FullHeal_StatusCheck
CONTRACT["FullHeal_StatusCheck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["FullHeal_StatusCheck"] = [
    {"wram": {0xCC00: b"\x00"}},
    {"wram": {0xCC00: b"\x01"}},
    dict(POISON, wram={0xCC00: b"\x02"}),
]
# <<< factory FullHeal_StatusCheck

# >>> factory PoisonFang_AIEffect
CONTRACT["PoisonFang_AIEffect"] = {"compare": (), "preserve": ()}
CASES["PoisonFang_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    dict(POISON, wram={0xCCB9: b"\x14"}, read={0xCCB9: 1, 0xCCBB: 2}),
]
# <<< factory PoisonFang_AIEffect

# >>> factory WeepinbellPoisonPowder_AIEffect
CONTRACT["WeepinbellPoisonPowder_AIEffect"] = {"compare": (), "preserve": ()}
CASES["WeepinbellPoisonPowder_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    dict(POISON, wram={0xCCB9: b"\x14"}, read={0xCCB9: 1, 0xCCBB: 2}),
]
# <<< factory WeepinbellPoisonPowder_AIEffect

# >>> factory Toxic_AIEffect
CONTRACT["Toxic_AIEffect"] = {"compare": (), "preserve": ()}
CASES["Toxic_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xCCB9: b"\x10"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xFF"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory Toxic_AIEffect

# >>> factory BoyfriendsEffect
CONTRACT["BoyfriendsEffect"] = {"compare": (), "preserve": ()}
CASES["BoyfriendsEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00\x01\x02\x03\xFF", 0xC400: b"\x19\x10\x19\x19\x10", 0xCCB9: b"\x00"}, "read": {0xCCB9: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00\x01\xFF", 0xC400: b"\x19\x10\x19", 0xCCB9: b"\x05"}, read={0xCCB9: 1}),
]
# <<< factory BoyfriendsEffect

# >>> factory IvysaurPoisonPowder_AIEffect
CONTRACT["IvysaurPoisonPowder_AIEffect"] = {"compare": (), "preserve": ()}
CASES["IvysaurPoisonPowder_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 1, 0xCCBB: 2, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00", 0xCCBB: b"\x05", 0xCCBC: b"\x02"},
         read={0xCCB9: 1, 0xCCBB: 2, 0xCCBC: 1}),
]
# <<< factory IvysaurPoisonPowder_AIEffect

# >>> factory EnergyTrans_CheckPlayArea
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
hTemp_ffa0 = 0xFFA0
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400

CONTRACT["EnergyTrans_CheckPlayArea"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c")
}
CASES["EnergyTrans_CheckPlayArea"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wPlayerDuelVariables: b"\x00", wPlayerDuelVariables + 0xBC: b"\xFF",
              0xC300 + 0xBC: b"\xFF", wPlayerDeck: b"\x01"},
     "read": {hTemp_ffa0: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
                       wPlayerDuelVariables: b"\x10", wPlayerDuelVariables + 0xBC: b"\xFF",
                       0xC300 + 0xBC: b"\xFF", wPlayerDeck: b"\x01"},
         read={hTemp_ffa0: 1}),
]
# <<< factory EnergyTrans_CheckPlayArea

# >>> factory Firegiver_InitialEffect
CONTRACT["Firegiver_InitialEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["Firegiver_InitialEffect"] = [dict(POISON), {"f": 0x00}, {"f": 0x80}, {"f": 0x7F}]
# <<< factory Firegiver_InitialEffect


# >>> factory MoltresLv37DiveBomb_AIEffect
CONTRACT["MoltresLv37DiveBomb_AIEffect"] = {"compare": (), "preserve": ()}
CASES["MoltresLv37DiveBomb_AIEffect"] = [dict(POISON, read={0xCCB9: 3}), {"a": 0x00, "f": 0x00, "d": 0x00, "e": 0x00, "wram": {0xCCBB: b"\x00", 0xCCBC: b"\x00"}, "read": {0xCCB9: 3}}]
# <<< factory MoltresLv37DiveBomb_AIEffect


# >>> factory GetEnergyAttachedMultiplierDamage
CONTRACT["GetEnergyAttachedMultiplierDamage"] = {"compare": ("d", "e"), "preserve": ()}
CASES["GetEnergyAttachedMultiplierDamage"] = [
    {"wram": {0xFF97: b"\xC3", 0xC200: b"\x10", 0xC400: b"\x01"}},
    dict(POISON, wram={0xFF97: b"\xC3", 0xC200: b"\x10\x10", 0xC400: b"\x01\x02"}),
    {"wram": {0xFF97: b"\xC3", 0xC200: b"\x10\x10\x10\x10\x10", 0xC400: b"\x01\x02\x03\x04\x05"}}
]
# <<< factory GetEnergyAttachedMultiplierDamage


# >>> factory ClefairyDoll_BenchCheck
CONTRACT["ClefairyDoll_BenchCheck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["ClefairyDoll_BenchCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x05"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x06"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x07"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x06"}),
]
# <<< factory ClefairyDoll_BenchCheck

# >>> factory ClefairyDoll_PlaceInPlayAreaEffect
CONTRACT["ClefairyDoll_PlaceInPlayAreaEffect"] = {"compare": (), "preserve": ()}
CASES["ClefairyDoll_PlaceInPlayAreaEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2EF: b"\x00",
              0xC2EE: b"\x01", 0xC242: b"\x00", 0xC400: b"\x08"},
     "read": {0xC2EF: 1, 0xC2BB: 1, 0xC2C8: 1, 0xC2CE: 1, 0xC2C2: 1,
              0xC2D4: 1, 0xC2E0: 1, 0xC2DA: 1, 0xC2F0: 1}},
    {"wram": {0xFF97: b"\xC2", 0xFF9F: b"\x05", 0xC2EF: b"\x06"},
     "read": {0xC2EF: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9F: b"\x05", 0xC2EF: b"\x06"},
         read={0xC2EF: 1}),
]
# <<< factory ClefairyDoll_PlaceInPlayAreaEffect


# >>> factory Wildfire_DiscardDeckEffect
CONTRACT["Wildfire_DiscardDeckEffect"] = {"compare": (), "preserve": ()}
CASES["Wildfire_DiscardDeckEffect"] = [
    {"setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "wram": {0xFF97: b"\xC2", 0xC3BA: b"\x00", 0xC3ED: b"\x00", 0xFFA0: b"\x01",
              0xC37E: b"\x01\x02"},
     "read": {0xFF97: 1, 0xC3BA: 1, 0xC3ED: 1}},
    {"setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "wram": {0xFF97: b"\xC2", 0xC3BA: b"\x3A", 0xC37E: b"\x01\x02",
              0xC3ED: b"\x00", 0xFFA0: b"\x02"},
     "read": {0xFF97: 1, 0xC3BA: 1, 0xC3ED: 1}},
    dict(POISON, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         wram={0xFF97: b"\xC2", 0xC3BA: b"\x3C", 0xC37E: b"\x01",
               0xC3ED: b"\x00", 0xFFA0: b"\x05"},
         read={0xFF97: 1, 0xC3BA: 1, 0xC3ED: 1}),
]
# <<< factory Wildfire_DiscardDeckEffect

# >>> factory MoltresLv35DiveBomb_AIEffect
CONTRACT["MoltresLv35DiveBomb_AIEffect"] = {"compare": (), "preserve": ()}
CASES["MoltresLv35DiveBomb_AIEffect"] = [
    dict(POISON, read={0xCCB9: 3}),
    {"wram": {0xCCB9: b"\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 3}},
]
# <<< factory MoltresLv35DiveBomb_AIEffect

# >>> factory EnergyBurnCheck_Unreferenced
CONTRACT["EnergyBurnCheck_Unreferenced"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["EnergyBurnCheck_Unreferenced"] = [
    dict(POISON, wram={0xFF97: bytes((0xC2,)), 0xC2BB: bytes((0x00,)), 0xC2F0: bytes((0x00,)), 0xC2BC: bytes((0xFF,)), 0xC3BC: bytes((0xFF,)), 0xC400: bytes((0x32,))}),
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x00", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF", 0xC400: bytes((0x32,))}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x00", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF", 0xC400: bytes((0x31,))}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x80", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF", 0xC400: bytes((0x32,))}},
]
# <<< factory EnergyBurnCheck_Unreferenced

# >>> factory FlareonRage_DamageBoostEffect
CONTRACT["FlareonRage_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["FlareonRage_DamageBoostEffect"] = [
    dict(POISON, wram={0xFF97: bytes((0xC2,)), 0xC2BB: bytes((0x00,)), 0xC2C8: bytes((0x00,)), 0xC400: bytes((0x01,)), 0xCCB9: bytes((0x00, 0x00))}, read={0xCCB9: 2}),
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", 0xC400: b"\x01", 0xCCB9: b"\x10\x00"}, "read": {0xCCB9: 2}},
]
# <<< factory FlareonRage_DamageBoostEffect

# >>> factory Shift_OncePerTurnCheck
CONTRACT["Shift_OncePerTurnCheck"] = {"compare": ("f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["Shift_OncePerTurnCheck"] = [
    {"wram": {
        0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2BB: b"\xff", 0xC2BC: b"\xff",
        0xC2C2: b"\x00", 0xC2F0: b"\x00", 0xC3BB: b"\xff", 0xC3BC: b"\xff",
    }},
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x20"}},
    {"wram": {0xFF9D: b"\x01", 0xFF97: b"\xC2", 0xC2C3: b"\x20"}},
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x00", 0xC2F0: b"\x01"}},
    dict(POISON, wram={0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x20"}),
]
# <<< factory Shift_OncePerTurnCheck

# >>> factory VenomPowder_AIEffect
CONTRACT["VenomPowder_AIEffect"] = {"compare": (), "preserve": ()}
CASES["VenomPowder_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory VenomPowder_AIEffect

# >>> factory TangelaPoisonPowder_AIEffect
CONTRACT["TangelaPoisonPowder_AIEffect"] = {"compare": (), "preserve": ()}
CASES["TangelaPoisonPowder_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    dict(POISON),
    dict(POISON, a=1),
    dict(POISON, f=0, hl=0x4567),
]
# <<< factory TangelaPoisonPowder_AIEffect

# >>> factory PetalDance_AIEffect
CONTRACT["PetalDance_AIEffect"] = {"compare": (), "preserve": ()}
CASES["PetalDance_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, a=0x01, f=0x00, hl=0x4567,
         wram={0xCCB9: b"\x12\x34", 0xCCBB: b"\x56", 0xCCBC: b"\x78"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory PetalDance_AIEffect

# >>> factory RainDanceEffect
CONTRACT["RainDanceEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                           "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["RainDanceEffect"] = [dict(POISON)]
# <<< factory RainDanceEffect

# >>> factory PsyduckFurySwipes_AIEffect
CONTRACT["PsyduckFurySwipes_AIEffect"] = {"compare": (), "preserve": ()}
CASES["PsyduckFurySwipes_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory PsyduckFurySwipes_AIEffect

# >>> factory VaporeonQuickAttack_AIEffect
CONTRACT["VaporeonQuickAttack_AIEffect"] = {"compare": (), "preserve": ()}
CASES["VaporeonQuickAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory VaporeonQuickAttack_AIEffect

# >>> factory JellyfishSting_AIEffect
CONTRACT["JellyfishSting_AIEffect"] = {"compare": (), "preserve": ()}
CASES["JellyfishSting_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x14"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory JellyfishSting_AIEffect

# >>> factory PoliwhirlAmnesia_CheckAttacks
CONTRACT["PoliwhirlAmnesia_CheckAttacks"] = {"compare": ("f",), "preserve": ()}
CASES["PoliwhirlAmnesia_CheckAttacks"] = [
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wOpponentDeck: bytes((BULBASAUR,))}, "read": {hWhoseTurn: 1}},
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wOpponentDeck: bytes((CLEFAIRY_DOLL,)), wOpponentDuelVariables: b"\x10"},
     "read": {hWhoseTurn: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2",
                       wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
                       wOpponentDeck: bytes((MYSTERIOUS_FOSSIL,)),
                       wOpponentDuelVariables: b"\x10"}, read={hWhoseTurn: 1}),
]
# <<< factory PoliwhirlAmnesia_CheckAttacks

# >>> factory HeadacheEffect
CONTRACT["HeadacheEffect"] = {"compare": (), "preserve": ()}
CASES["HeadacheEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EB: b"\x00"}, "read": {0xC3EB: 1}},
    {"wram": {0xFF97: b"\xC3", 0xC2EB: b"\x00"}, "read": {0xC2EB: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC3EB: b"\x02"}, "read": {0xC3EB: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EB: b"\x00"}, read={0xC3EB: 1}),
]
# <<< factory HeadacheEffect

# >>> factory ArcanineQuickAttack_AIEffect
CONTRACT["ArcanineQuickAttack_AIEffect"] = {"compare": (), "preserve": ()}
CASES["ArcanineQuickAttack_AIEffect"] = [
    {"wram": {0xCCBB: b"\x00", 0xCCBC: b"\x00", 0xCCB9: b"\x00"}},
    dict(POISON, wram={0xCCBB: b"\xAA", 0xCCBC: b"\xBB", 0xCCB9: b"\xCC"}),
]
# <<< factory ArcanineQuickAttack_AIEffect

# >>> factory FlamesOfRage_CheckEnergy
CONTRACT["FlamesOfRage_CheckEnergy"] = {"compare": ("a", "f", "e", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["FlamesOfRage_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
]
# <<< factory FlamesOfRage_CheckEnergy

# >>> factory MagmarFlamethrower_DiscardEffect
CONTRACT["MagmarFlamethrower_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["MagmarFlamethrower_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA0: b"\x01"}),
]
# <<< factory MagmarFlamethrower_DiscardEffect

# >>> factory MagmarSmog_AIEffect
CONTRACT["MagmarSmog_AIEffect"] = {"compare": (), "preserve": ()}
CASES["MagmarSmog_AIEffect"] = [
    {"wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON), dict(POISON, a=1), dict(POISON, f=0), dict(POISON, hl=0x4567),
]
# <<< factory MagmarSmog_AIEffect

# >>> factory Wildfire_CheckEnergy
CONTRACT["Wildfire_CheckEnergy"] = {"compare": ("a", "f", "e", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["Wildfire_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 6,
     "wram": {0xCC1B: b"\x01\x02\x03\x04\x05\x06\x07\x08"}, "read": {0xCC1B: 8}},
]
# <<< factory Wildfire_CheckEnergy

# >>> factory MrMimeMeditate_DamageBoostEffect
CONTRACT["MrMimeMeditate_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["MrMimeMeditate_DamageBoostEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3BB: b"\x00", 0xC3C8: b"\x00",
              0xC480: b"\x01", 0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2}},
    {"wram": {0xFF97: b"\xC2", 0xC3BB: b"\x00", 0xC3C8: b"\xC9",
              0xC480: b"\x01", 0xCCB9: b"\x05\x00"}, "read": {0xCCB9: 2}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3BB: b"\x00", 0xC3C8: b"\x71",
                       0xC480: b"\x01", 0xCCB9: b"\x10\x00"}, read={0xCCB9: 2}),
]
# <<< factory MrMimeMeditate_DamageBoostEffect

# >>> factory DancingEmbers_AIEffect
CONTRACT["DancingEmbers_AIEffect"] = {"compare": (), "preserve": ()}
CASES["DancingEmbers_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory DancingEmbers_AIEffect

# >>> factory FlareonFlamethrower_DiscardEffect
CONTRACT["FlareonFlamethrower_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["FlareonFlamethrower_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA0: b"\x01"}),
]
# <<< factory FlareonFlamethrower_DiscardEffect

# >>> factory MagmarFlamethrower_CheckEnergy
CONTRACT["MagmarFlamethrower_CheckEnergy"] = {"compare": ("a", "f", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["MagmarFlamethrower_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    {"wram": {0xCC1B: b"\x01" + b"\x00" * 7}, "read": {0xCC1B: 8}},
    {"wram": {0xCC1B: b"\x02" + b"\x00" * 7}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\x00" * 8}, read={0xCC1B: 8}),
]
# <<< factory MagmarFlamethrower_CheckEnergy

# >>> factory FlamesOfRage_DiscardEffect
CONTRACT["FlamesOfRage_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["FlamesOfRage_DiscardEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xFFA0: b"\x00\x01", 0xC2ED: b"\x00"}, "read": {0xFFA0: 2, 0xC2ED: 1, 0xC27E: 2}},
    {"wram": {0xFF97: b"\xC2", 0xFFA0: b"\x05\x06", 0xC2ED: b"\x00"}, "read": {0xFFA0: 2, 0xC2ED: 1, 0xC27E: 2}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFFA0: b"\x08\x09", 0xC2ED: b"\x00"}, read={0xFFA0: 2, 0xC2ED: 1, 0xC27E: 2}),
]
# <<< factory FlamesOfRage_DiscardEffect

# >>> factory FlamesOfRage_DamageBoostEffect
CONTRACT["FlamesOfRage_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["FlamesOfRage_DamageBoostEffect"] = [
    dict(POISON, wram={0xFF97: bytes((0xC2,)), 0xC2BB: bytes((0x00,)), 0xC2C8: bytes((0x00,)), 0xC400: bytes((0x01,)), 0xCCB9: bytes((0x00, 0x00))}, read={0xCCB9: 2}),
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", 0xC400: b"\x01", 0xCCB9: b"\x10\x00"}, "read": {0xCCB9: 2}},
]
# <<< factory FlamesOfRage_DamageBoostEffect

# >>> factory CharmeleonFlamethrower_CheckEnergy
CONTRACT["CharmeleonFlamethrower_CheckEnergy"] = {"compare": ("a", "f", "e", "hl", "b", "c", "d"), "preserve": ("b", "c", "d")}
CASES["CharmeleonFlamethrower_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
]
# <<< factory CharmeleonFlamethrower_CheckEnergy

# >>> factory CharmeleonFlamethrower_DiscardEffect
CONTRACT["CharmeleonFlamethrower_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["CharmeleonFlamethrower_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA0: b"\x01"}),
    {"a": 1, "f": 0x10, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 0x1234, "wram": {0xFFA0: b"\xFF"}},
]
# <<< factory CharmeleonFlamethrower_DiscardEffect

# >>> factory EnergyBurnEffect
CONTRACT["EnergyBurnEffect"] = {"compare": ("f",), "preserve": ()}
CASES["EnergyBurnEffect"] = [
    {},
    dict(POISON),
]
# <<< factory EnergyBurnEffect

# >>> factory FireSpin_CheckEnergy
CONTRACT["FireSpin_CheckEnergy"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["FireSpin_CheckEnergy"] = [
    {"wram": {0xFF97: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x01"}, "read": {0xC510: 2}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC200: b"\x00"}, read={0xC510: 2}),
]
# <<< factory FireSpin_CheckEnergy

# >>> factory FlareonQuickAttack_AIEffect
CONTRACT["FlareonQuickAttack_AIEffect"] = {"compare": (), "preserve": ()}
CASES["FlareonQuickAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory FlareonQuickAttack_AIEffect

# >>> factory FlareonFlamethrower_CheckEnergy
CONTRACT["FlareonFlamethrower_CheckEnergy"] = {"compare": ("a", "f", "e", "hl", "b", "c", "d"),
                                                "preserve": ("b", "c", "d")}
CASES["FlareonFlamethrower_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00" * 8}, "read": {0xCC1B: 8}},
    dict(POISON, wram={0xCC1B: b"\xAA" * 8}, read={0xCC1B: 8}),
]
# <<< factory FlareonFlamethrower_CheckEnergy

# >>> factory Prophecy_AISelectEffect
CONTRACT["Prophecy_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["Prophecy_AISelectEffect"] = [
    {"wram": {0xFFA0: b"\x00"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
]
# <<< factory Prophecy_AISelectEffect

# >>> factory Prophecy_ReorderDeckEffect
CONTRACT["Prophecy_ReorderDeckEffect"] = {"compare": ("a", "c", "f", "hl", "b", "d", "e"), "preserve": ("b", "d", "e")}
CASES["Prophecy_ReorderDeckEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00",
              0xC27E: b"\x01\x02\xFF", 0xFFA0: b"\x00\x01\x02\xFF"},
     "read": {0xC2BA: 1, 0xC202: 1, 0xC203: 1, 0xC27E: 3, 0xFFA0: 4}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BA: b"\x00",
                       0xC27E: b"\x03\x04\xFF", 0xFFA0: b"\x00\x03\x04\xFF"},
         read={0xC2BA: 1, 0xC203: 1, 0xC204: 1, 0xC27E: 3, 0xFFA0: 4}),
]
# <<< factory Prophecy_ReorderDeckEffect

# >>> factory SuperEnergyRetrieval_HandEnergyCheck
CONTRACT["SuperEnergyRetrieval_HandEnergyCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SuperEnergyRetrieval_HandEnergyCheck"] = [
    {},
    dict(POISON),
    {"a": 1, "f": 1, "d": 1, "hl": 1},
]
# <<< factory SuperEnergyRetrieval_HandEnergyCheck

# >>> factory GetNextPositionInTempList_TrainerEffects
CONTRACT["GetNextPositionInTempList_TrainerEffects"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetNextPositionInTempList_TrainerEffects"] = [
    {"wram": {0xFFB2: b"\x00"}},
    {"wram": {0xFFB2: b"\x01"}},
    {"wram": {0xFFB2: b"\xFF"}},
    dict(POISON, wram={0xFFB2: b"\x00"}),
]
# <<< factory GetNextPositionInTempList_TrainerEffects

# >>> factory NinetalesLure_AISelectEffect
CONTRACT["NinetalesLure_AISelectEffect"] = {"compare": ("a",), "preserve": ()}
CASES["NinetalesLure_AISelectEffect"] = [
	{"wram": {0xFFA0: b"\x00"}, "read": {0xFFA0: 1}},
	dict(POISON, wram={0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
	{"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
]
# <<< factory NinetalesLure_AISelectEffect

# >>> factory Ember_CheckEnergy
CONTRACT["Ember_CheckEnergy"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Ember_CheckEnergy"] = [
    {"wram": {0xCC1B: b"\x00\x00\x00\x00\x00\x00\x00\x00"}},
    dict(POISON, wram={0xCC1B: b"\xAA\xBB\xCC\xDD\xEE\xFF\x11\x22"}),
    {"wram": {0xCC1B: b"\x01\x00\x00\x00\x00\x00\x00\x00"}},
]
# <<< factory Ember_CheckEnergy

# >>> factory DestinyBond_CheckEnergy
CONTRACT["DestinyBond_CheckEnergy"] = {"compare": ("a", "f", "b", "c", "d", "hl"), "preserve": ("b", "c", "d")}
CASES["DestinyBond_CheckEnergy"] = [
	{"wram": {0xCC1B: b"\x00\x00\x00\x00\x00\x00\x00\x00"}},
	dict(POISON, wram={0xCC1B: b"\x00\x00\x00\x00\x00\x00\x00\x00"}),
	{"wram": {0xCC1B: b"\x01\x02\x03\x04\x05\x06\x07\x08"}},
]
# <<< factory DestinyBond_CheckEnergy

# >>> factory ComputerSearch_HandDeckCheck
CONTRACT["ComputerSearch_HandDeckCheck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["ComputerSearch_HandDeckCheck"] = [
    {},
    dict(POISON),
    {"a": 1},
    {"a": 2},
    {"a": 3},
    {"a": 0xFF},
]
# <<< factory ComputerSearch_HandDeckCheck

# >>> factory MrFuji_BenchCheck
CONTRACT["MrFuji_BenchCheck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["MrFuji_BenchCheck"] = [
    {},
    dict(POISON),
    {"a": 1},
    {"a": 2},
    {"a": 0xFF},
]
# <<< factory MrFuji_BenchCheck
# >>> factory Peek_OncePerTurnCheck
CONTRACT["Peek_OncePerTurnCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["Peek_OncePerTurnCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF"}),
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x01", 0xC2BC: b"\xFF",
              0xC3BC: b"\xFF", 0xC201: b"\x20"}},
]
# <<< factory Peek_OncePerTurnCheck

# >>> factory Wail_BenchCheck
CONTRACT["Wail_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Wail_BenchCheck"] = [{}, dict(POISON), {"a": 6}, {"a": 2}]
# <<< factory Wail_BenchCheck

# >>> factory StepIn_SwitchEffect
CONTRACT["StepIn_SwitchEffect"] = {"compare": (), "preserve": ()}
CASES["StepIn_SwitchEffect"] = [{"wram": {0xFFA0: b"\x01"}}]
# <<< factory StepIn_SwitchEffect

# >>> factory ThickSkinnedEffect
CONTRACT["ThickSkinnedEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ThickSkinnedEffect"] = [{}, dict(POISON)]
# <<< factory ThickSkinnedEffect

# >>> factory HealingWind_InitialEffect
CONTRACT["HealingWind_InitialEffect"] = {"compare": ("f",), "preserve": ()}
CASES["HealingWind_InitialEffect"] = [{}, dict(POISON)]
# <<< factory HealingWind_InitialEffect

# >>> factory PickRandomBasicCardFromDeck
CONTRACT["PickRandomBasicCardFromDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PickRandomBasicCardFromDeck"] = [{}, dict(POISON)]
# <<< factory PickRandomBasicCardFromDeck

# >>> factory DrawSymbolOnPlayAreaCursor
CONTRACT["DrawSymbolOnPlayAreaCursor"] = {"compare": (), "preserve": ()}
CASES["DrawSymbolOnPlayAreaCursor"] = [
    {"a": 0, "b": 0x77, "read": {0x9840: 1}},
    {"a": 1, "b": 0x77, "read": {0x98A0: 1}},
    {"a": 2, "b": 1, "read": {0x9900: 1}},
]
# <<< factory DrawSymbolOnPlayAreaCursor
# >>> factory Func_2c6d9
CONTRACT["Func_2c6d9"] = {"compare": ("f",), "preserve": ()}
CASES["Func_2c6d9"] = [
    {"keys": 0x01, "wram": {0xC590: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    dict(POISON, keys=0x02, wram={0xC590: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         vread={0: {0x9980: 1, 0x9A32: 1}}),
]
# <<< factory Func_2c6d9


# >>> factory GustOfWind_BenchCheck
CONTRACT["GustOfWind_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["GustOfWind_BenchCheck"] = [{"f": 0}, dict(POISON), {"a": 2, "f": 0xF0}]
# <<< factory GustOfWind_BenchCheck

# >>> factory MarowakCallForFamily_AISelectEffect
CONTRACT["MarowakCallForFamily_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["MarowakCallForFamily_AISelectEffect"] = [
    {"wram": {0xC400: b"\xFF"}, "read": {0xC510: 1}},
    {"wram": {0xC400: b"\x00\xFF"}, "read": {0xC510: 2}},
]
# <<< factory MarowakCallForFamily_AISelectEffect

# >>> factory CreateListOfFireEnergyAttachedToArena
CONTRACT["CreateListOfFireEnergyAttachedToArena"] = {"compare": ("a", "c", "f", "hl"), "preserve": ()}
CASES["CreateListOfFireEnergyAttachedToArena"] = [{}, dict(POISON)]
# <<< factory CreateListOfFireEnergyAttachedToArena
# >>> factory CreateEnergyCardListFromDiscardPile_AllEnergy
CONTRACT["CreateEnergyCardListFromDiscardPile_AllEnergy"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["CreateEnergyCardListFromDiscardPile_AllEnergy"] = [{}, dict(POISON)]
# <<< factory CreateEnergyCardListFromDiscardPile_AllEnergy
# >>> factory CheckIfDeckIsEmpty
CONTRACT["CheckIfDeckIsEmpty"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["CheckIfDeckIsEmpty"] = [{}, {"wram": {0xC2BA: b"\x3C"}}, {"wram": {0xC2BA: b"\x50"}}]
# <<< factory CheckIfDeckIsEmpty
# >>> factory VictreebelLure_AssertPokemonInBench
CONTRACT["VictreebelLure_AssertPokemonInBench"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["VictreebelLure_AssertPokemonInBench"] = [{}, dict(POISON)]
# <<< factory VictreebelLure_AssertPokemonInBench
# >>> factory Toxic_DoublePoisonEffect
CONTRACT["Toxic_DoublePoisonEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Toxic_DoublePoisonEffect"] = [{}, dict(POISON)]
# <<< factory Toxic_DoublePoisonEffect

# >>> factory NinetalesLure_CheckBench
CONTRACT["NinetalesLure_CheckBench"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["NinetalesLure_CheckBench"] = [{}, {"wram": {0xC3EF: b"\x02"}}]
# <<< factory NinetalesLure_CheckBench
# >>> factory ScoopUp_BenchCheck
CONTRACT["ScoopUp_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["ScoopUp_BenchCheck"] = [{}, {"wram": {0xC2EF: b"\x02"}}]
# <<< factory ScoopUp_BenchCheck
# >>> factory MysteriousFossil_BenchCheck
CONTRACT["MysteriousFossil_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["MysteriousFossil_BenchCheck"] = [{}, {"wram": {0xC2EF: b"\x06"}}]
# <<< factory MysteriousFossil_BenchCheck
# >>> factory TrainerCardAsPokemon_BenchCheck
CONTRACT["TrainerCardAsPokemon_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["TrainerCardAsPokemon_BenchCheck"] = [{}, {"wram": {0xC2EF: b"\x02", 0xFF9D: b"\x00"}}]
# <<< factory TrainerCardAsPokemon_BenchCheck
# >>> factory VictreebelLure_AssertPokemonInBench
CONTRACT["VictreebelLure_AssertPokemonInBench"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["VictreebelLure_AssertPokemonInBench"] = [{}, {"wram": {0xC3EF: b"\x02"}}]
# <<< factory VictreebelLure_AssertPokemonInBench
# >>> factory ThunderboltEffect
CONTRACT["ThunderboltEffect"] = {"compare": (), "preserve": ()}
CASES["ThunderboltEffect"] = [{}, dict(POISON)]
# <<< factory ThunderboltEffect
# >>> factory TrainerCardAsPokemon_DiscardEffect
CONTRACT["TrainerCardAsPokemon_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["TrainerCardAsPokemon_DiscardEffect"] = [{}, dict(POISON)]
# <<< factory TrainerCardAsPokemon_DiscardEffect
# >>> factory MysteriousFossil_PlaceInPlayAreaEffect
CONTRACT["MysteriousFossil_PlaceInPlayAreaEffect"] = {"compare": (), "preserve": ()}
CASES["MysteriousFossil_PlaceInPlayAreaEffect"] = [{}, dict(POISON)]
# <<< factory MysteriousFossil_PlaceInPlayAreaEffect

# >>> factory Barrier_DiscardEffect
CONTRACT["Barrier_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["Barrier_DiscardEffect"] = [
    {"wram": {0xFFA0: b"\x00"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
    {"wram": {0xFFA0: b"\x01"}, "read": {0xFFA0: 1}},
    {"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
]
# <<< factory Barrier_DiscardEffect

# >>> factory DestinyBond_DiscardEffect
CONTRACT["DestinyBond_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["DestinyBond_DiscardEffect"] = [{}, dict(POISON)]
# <<< factory DestinyBond_DiscardEffect
# >>> factory Ember_DiscardEffect
CONTRACT["Ember_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["Ember_DiscardEffect"] = [{}, dict(POISON)]
# <<< factory Ember_DiscardEffect
# >>> factory FireBlast_DiscardEffect
CONTRACT["FireBlast_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["FireBlast_DiscardEffect"] = [{}, dict(POISON)]
# <<< factory FireBlast_DiscardEffect
# >>> factory FireSpin_AISelectEffect
CONTRACT["FireSpin_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["FireSpin_AISelectEffect"] = [{}, dict(POISON)]
# <<< factory FireSpin_AISelectEffect
# >>> factory FireSpin_DiscardEffect
CONTRACT["FireSpin_DiscardEffect"] = {"compare": (), "preserve": ()}
CASES["FireSpin_DiscardEffect"] = [{}, dict(POISON)]
# <<< factory FireSpin_DiscardEffect

# >>> factory PidgeottoMirrorMove_InitialEffect1
CONTRACT["PidgeottoMirrorMove_InitialEffect1"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["PidgeottoMirrorMove_InitialEffect1"] = [
	{},
	dict(POISON),
]
# <<< factory PidgeottoMirrorMove_InitialEffect1

# >>> factory ClefairyMetronome_CheckAttacks
CONTRACT["ClefairyMetronome_CheckAttacks"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["ClefairyMetronome_CheckAttacks"] = [
	{},
	dict(POISON),
]
# <<< factory ClefairyMetronome_CheckAttacks

# >>> factory Psychic_DamageBoostEffect
CONTRACT["Psychic_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["Psychic_DamageBoostEffect"] = [
	{"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2}},
	dict(POISON, wram={0xCCB9: b"\x34\x12"}, read={0xCCB9: 2}),
	{"wram": {0xCCB9: b"\xFF\xFF"}, "read": {0xCCB9: 2}},
]
# <<< factory Psychic_DamageBoostEffect

# >>> factory Barrier_AISelectEffect
CONTRACT["Barrier_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Barrier_AISelectEffect"] = [
	{"wram": {0xC510: b"\x00", 0xFFA0: b"\x00"}, "read": {0xFFA0: 1}},
	dict(POISON, wram={0xC510: b"\xFF", 0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
	{"wram": {0xC510: b"\x01", 0xFFA0: b"\x7E"}, "read": {0xFFA0: 1}},
]
# <<< factory Barrier_AISelectEffect

# >>> factory Whirlpool_AISelectEffect
CONTRACT["Whirlpool_AISelectEffect"] = {"compare": ("a",), "preserve": ()}
CASES["Whirlpool_AISelectEffect"] = [
	{"wram": {0xFFA0: b"\x00"}},
	{"wram": {0xFFA0: b"\x5a"}},
	dict(POISON, wram={0xFFA0: b"\xff"}),
]
# <<< factory Whirlpool_AISelectEffect

# >>> factory Whirlpool_DiscardEffect
CONTRACT["Whirlpool_DiscardEffect"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["Whirlpool_DiscardEffect"] = [
	# all-zero entry: hTemp_ffa0 = 0 -> full path, PutCardInDiscardPile(0) writes
	{"wram": {0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x00"}},
	{"hl": 0xC100, "wram": {0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x37"}},
	# boundary: selected card == $ff -> return at cp $ff, no discard happens
	{"hl": 0xC100, "wram": {0xC000: b"\x00" * 0xF00, 0xFFA0: b"\xff"}},
	# boundary: one below $ff
	{"hl": 0xC100, "wram": {0xC000: b"\x00" * 0xF00, 0xFFA0: b"\xfe"}},
	{"hl": 0xC200, "wram": {0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x01"}},
	dict(POISON, hl=0xC100, wram={0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x05"}),
	# nonzero byte at [hl] to exercise HandleNoDamageOrEffect's other flag outcome
	{"hl": 0xC300, "wram": {0xC000: b"\x00" * 0xF00, 0xC300: b"\xff", 0xFFA0: b"\x2a"}},
]
# <<< factory Whirlpool_DiscardEffect

# >>> factory EnergyRemoval_EnergyCheck
CONTRACT["EnergyRemoval_EnergyCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["EnergyRemoval_EnergyCheck"] = [
	{},
	dict(POISON),
]
# <<< factory EnergyRemoval_EnergyCheck

# >>> factory EnergyRemoval_AISelection
CONTRACT["EnergyRemoval_AISelection"] = {"compare": ("a",), "preserve": ()}
CASES["EnergyRemoval_AISelection"] = [
	{},
	dict(POISON),
]
# <<< factory EnergyRemoval_AISelection

# >>> factory EnergyRetrieval_HandEnergyCheck
CONTRACT["EnergyRetrieval_HandEnergyCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["EnergyRetrieval_HandEnergyCheck"] = [
	{},  # zeroed duel vars: hand count 0 < 2, early ret c with NotEnoughCardsInHandText
	dict(POISON),
]
# <<< factory EnergyRetrieval_HandEnergyCheck

# >>> factory MrMimeMeditate_AIEffect
wDamage = 0xCCB9
CONTRACT["MrMimeMeditate_AIEffect"] = {"compare": (), "preserve": ()}
CASES["MrMimeMeditate_AIEffect"] = [
	{},
	{"wram": {wDamage: b"\xff\xff"}},
	dict(POISON, wram={wDamage: b"\x00\x0f"}),
]
# <<< factory MrMimeMeditate_AIEffect

# >>> factory PsywaveEffect
wDamage = 0xCCB9
CONTRACT["PsywaveEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["PsywaveEffect"] = [
	{},
	{"wram": {wDamage: b"\xaa\x55"}},
	dict(POISON, wram={wDamage: b"\xff\xff"}),
]
# <<< factory PsywaveEffect

# >>> factory PokemonCenter_DamageCheck
CONTRACT["PokemonCenter_DamageCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["PokemonCenter_DamageCheck"] = [{}, dict(POISON)]
# <<< factory PokemonCenter_DamageCheck

# >>> factory PokemonBreeder_HandPlayAreaCheck
CONTRACT["PokemonBreeder_HandPlayAreaCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["PokemonBreeder_HandPlayAreaCheck"] = [{}, dict(POISON, hl=0x1234)]
# <<< factory PokemonBreeder_HandPlayAreaCheck

# >>> factory PokemonTrader_HandDeckCheck
CONTRACT["PokemonTrader_HandDeckCheck"] = {"compare": ("a", "f", "c", "d", "e", "hl"), "preserve": ()}
CASES["PokemonTrader_HandDeckCheck"] = [{}, {"wram": {0xC2EE: b"\x01"}}, dict(POISON, wram={0xC200: b"\x01\x01", 0xC2EE: b"\x02\x00\x01"})]
# <<< factory PokemonTrader_HandDeckCheck

# >>> factory VictreebelLure_GetBenchPokemonWithLowestHP
CONTRACT["VictreebelLure_GetBenchPokemonWithLowestHP"] = {"compare": (), "preserve": ()}
CASES["VictreebelLure_GetBenchPokemonWithLowestHP"] = [
    {"read": {0xFFA0: 1}},
    dict(POISON, read={0xFFA0: 1}),
]
# <<< factory VictreebelLure_GetBenchPokemonWithLowestHP

# >>> factory Sprout_CheckDeckAndPlayArea
CONTRACT["Sprout_CheckDeckAndPlayArea"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["Sprout_CheckDeckAndPlayArea"] = [{}, dict(POISON)]
# <<< factory Sprout_CheckDeckAndPlayArea

# >>> factory NidoranFCallForFamily_CheckDeckAndPlayArea
CONTRACT["NidoranFCallForFamily_CheckDeckAndPlayArea"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["NidoranFCallForFamily_CheckDeckAndPlayArea"] = [{}, dict(POISON)]
# <<< factory NidoranFCallForFamily_CheckDeckAndPlayArea

# >>> factory DragonairHyperBeam_AISelectEffect
CONTRACT["DragonairHyperBeam_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["DragonairHyperBeam_AISelectEffect"] = [{"read": {0xFFA0: 1}}, dict(POISON, read={0xFFA0: 1})]
# <<< factory DragonairHyperBeam_AISelectEffect

# >>> factory ClefableMetronome_CheckAttacks
CONTRACT["ClefableMetronome_CheckAttacks"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["ClefableMetronome_CheckAttacks"] = [{}, dict(POISON)]
# <<< factory ClefableMetronome_CheckAttacks

# >>> factory Scavenge_CheckDiscardPile
CONTRACT["Scavenge_CheckDiscardPile"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["Scavenge_CheckDiscardPile"] = [{"read": {0xCC1B: 8}}, dict(POISON, wram={0xCC1B: b"\xaa" * 8}, read={0xCC1B: 8})]
# <<< factory Scavenge_CheckDiscardPile

# >>> factory Scavenge_AISelectEffect
CONTRACT["Scavenge_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Scavenge_AISelectEffect"] = [{"read": {0xFFA0: 2}}, dict(POISON, wram={0xFFA0: b"\xaa\xbb"}, read={0xFFA0: 2})]
# <<< factory Scavenge_AISelectEffect

# >>> factory SlowpokeAmnesia_CheckAttacks
CONTRACT["SlowpokeAmnesia_CheckAttacks"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SlowpokeAmnesia_CheckAttacks"] = [{}, dict(POISON)]
# <<< factory SlowpokeAmnesia_CheckAttacks

# >>> factory DevolutionBeam_CheckPlayArea
CONTRACT["DevolutionBeam_CheckPlayArea"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["DevolutionBeam_CheckPlayArea"] = [{}, dict(POISON)]
# <<< factory DevolutionBeam_CheckPlayArea

# >>> factory DevolutionBeam_AISelectEffect
CONTRACT["DevolutionBeam_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["DevolutionBeam_AISelectEffect"] = [{"read": {0xFFA0: 2}}, dict(POISON, wram={0xFFA0: b"\xaa\xbb"}, read={0xFFA0: 2})]
# <<< factory DevolutionBeam_AISelectEffect

# >>> factory MewtwoAltEnergyAbsorption_CheckDiscardPile
CONTRACT["MewtwoAltEnergyAbsorption_CheckDiscardPile"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["MewtwoAltEnergyAbsorption_CheckDiscardPile"] = [{}, dict(POISON)]
# <<< factory MewtwoAltEnergyAbsorption_CheckDiscardPile

# >>> factory MewtwoAltEnergyAbsorption_AISelectEffect
CONTRACT["MewtwoAltEnergyAbsorption_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["MewtwoAltEnergyAbsorption_AISelectEffect"] = [
    {"read": {0xC510: 1, 0xFFA0: 3}},
    dict(POISON, read={0xC510: 1, 0xFFA0: 3}),
]
# <<< factory MewtwoAltEnergyAbsorption_AISelectEffect

# >>> factory MewtwoEnergyAbsorption_CheckDiscardPile
CONTRACT["MewtwoEnergyAbsorption_CheckDiscardPile"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["MewtwoEnergyAbsorption_CheckDiscardPile"] = [
    {"read": {0xC510: 1}},
    dict(POISON, read={0xC510: 1}),
]
# <<< factory MewtwoEnergyAbsorption_CheckDiscardPile

# >>> factory MewtwoEnergyAbsorption_AISelectEffect
CONTRACT["MewtwoEnergyAbsorption_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["MewtwoEnergyAbsorption_AISelectEffect"] = [
    {"read": {0xC510: 1, 0xFFA0: 3}},
    dict(POISON, read={0xC510: 1, 0xFFA0: 3}),
]
# <<< factory MewtwoEnergyAbsorption_AISelectEffect

# >>> factory JynxMeditate_AIEffect
wDamage = 0xCCB9
wAIMinDamage = 0xCCBB
wAIMaxDamage = 0xCCBC
CONTRACT["JynxMeditate_AIEffect"] = {"compare": (), "preserve": ()}
CASES["JynxMeditate_AIEffect"] = [
	{"wram": {wDamage: b"\x00\x00"},
	 "read": {wDamage: 2, wAIMinDamage: 1, wAIMaxDamage: 1}},
	dict(POISON, wram={wDamage: b"\x00\x0f"},
	     read={wDamage: 2, wAIMinDamage: 1, wAIMaxDamage: 1}),
]
# <<< factory JynxMeditate_AIEffect

# >>> factory MysteryAttack_RandomEffect
CONTRACT["MysteryAttack_RandomEffect"] = {"compare": (), "preserve": ()}
CASES["MysteryAttack_RandomEffect"] = [{"read": {0xFFA0: 1, 0xCCB8: 1}}, dict(POISON, wram={0xCCB8: b"\xaa"}, read={0xFFA0: 1, 0xCCB8: 1})]
# <<< factory MysteryAttack_RandomEffect

# >>> factory MarowakCallForFamily_CheckDeckAndPlayArea
CONTRACT["MarowakCallForFamily_CheckDeckAndPlayArea"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["MarowakCallForFamily_CheckDeckAndPlayArea"] = [
    {},
    dict(POISON),
]
# <<< factory MarowakCallForFamily_CheckDeckAndPlayArea

# >>> factory IceBreath_ZeroDamage
CONTRACT["IceBreath_ZeroDamage"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["IceBreath_ZeroDamage"] = [
    {},
    dict(POISON),
    {"a": 0x7F, "b": 1, "c": 2, "d": 3, "e": 4, "hl": 0x0100},
]
# <<< factory IceBreath_ZeroDamage

# >>> factory AIPickFireEnergyCardToDiscard
CONTRACT["AIPickFireEnergyCardToDiscard"] = {"compare": (), "preserve": ()}
CASES["AIPickFireEnergyCardToDiscard"] = [
    {"wram": {0xC510: b"\x00\x00\x00\x00"}, "read": {0xC510: 8, 0xFFA0: 1}},
    dict(POISON, wram={0xC510: b"\xAA\xBB\xCC\xDD"}, read={0xC510: 8, 0xFFA0: 1}),
    {"wram": {0xC510: b"\x01\xFF\x00\x00"}, "read": {0xC510: 8, 0xFFA0: 1}},
]
# <<< factory AIPickFireEnergyCardToDiscard

# >>> factory FlamesOfRage_AIEffect
CONTRACT["FlamesOfRage_AIEffect"] = {"compare": (), "preserve": ()}
CASES["FlamesOfRage_AIEffect"] = [
    {"read": {0xCB00: 0x100, 0xCC00: 0x100, 0xCD00: 0x100, 0xCE00: 0x100}},
    dict(POISON, read={0xCB00: 0x100, 0xCC00: 0x100, 0xCD00: 0x100, 0xCE00: 0x100}),
    {"wram": {0xCC00: b"\xAA" * 0x100},
     "read": {0xCB00: 0x100, 0xCC00: 0x100, 0xCD00: 0x100, 0xCE00: 0x100}},
]
# <<< factory FlamesOfRage_AIEffect

# >>> factory ArcanineFlamethrower_AISelectEffect
wDuelTempList = 0xC510
hTempList = 0xFFA0

CONTRACT["ArcanineFlamethrower_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["ArcanineFlamethrower_AISelectEffect"] = [
	{"wram": {wDuelTempList: bytes(0x40), hTempList: bytes(0x10)}},
	{"wram": {wDuelTempList: b"\x00\x64\xff\xff" + bytes(0x3c), hTempList: bytes(0x10)}},
	dict(POISON, wram={wDuelTempList: b"\x00\x64\xff\xff" + bytes(0x3c), hTempList: bytes(0x10)}),
]
# <<< factory ArcanineFlamethrower_AISelectEffect

# >>> factory FlamesOfRage_AISelectEffect
CONTRACT["FlamesOfRage_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["FlamesOfRage_AISelectEffect"] = [
	{"wram": {wDuelTempList: bytes(0x40), hTempList: bytes(0x10)}},
	{"wram": {wDuelTempList: b"\x00\x99\xff\xff" + bytes(0x3c), hTempList: b"\x00\x55" + bytes(0x0e)}},
	dict(POISON, wram={wDuelTempList: b"\x00\x64\xff\xff" + bytes(0x3c), hTempList: b"\x00\x77" + bytes(0x0e)}),
]
# <<< factory FlamesOfRage_AISelectEffect

# >>> factory FireBlast_AISelectEffect
CONTRACT["FireBlast_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["FireBlast_AISelectEffect"] = [
	{"wram": {wDuelTempList: bytes(0x40), hTempList: bytes(0x10)}},
	{"wram": {wDuelTempList: b"\x00\x64\xff\xff" + bytes(0x3c), hTempList: bytes(0x10)}},
	dict(POISON, wram={wDuelTempList: b"\x00\x64\xff\xff" + bytes(0x3c), hTempList: bytes(0x10)}),
]
# <<< factory FireBlast_AISelectEffect

# >>> factory EnergyConversion_CheckEnergy
CONTRACT["EnergyConversion_CheckEnergy"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["EnergyConversion_CheckEnergy"] = [
    {},
    dict(POISON),
]
# <<< factory EnergyConversion_CheckEnergy

# >>> factory EnergyConversion_AISelectEffect
CONTRACT["EnergyConversion_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["EnergyConversion_AISelectEffect"] = [
    {"wram": {0xC510: b"\xFF"}, "read": {0xFFA0: 3}},
    dict(POISON, wram={0xC510: b"\x01\x02\xFF"}, read={0xFFA0: 3}),
    {"wram": {0xC510: b"\x10\x20\x30"}, "read": {0xFFA0: 3}},
]
# <<< factory EnergyConversion_AISelectEffect

# >>> factory HypnoDarkMind_AISelectEffect
CONTRACT["HypnoDarkMind_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["HypnoDarkMind_AISelectEffect"] = [
    {"read": {0xFFA0: 1}},
    dict(POISON, read={0xFFA0: 1}),
    {"wram": {0xFFA0: b"\x12"}, "read": {0xFFA0: 1}},
]
# <<< factory HypnoDarkMind_AISelectEffect

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wOpponentDuelVariables = 0xC300
wOpponentDeck = 0xC480
DUELVARS_ARENA_CARD = 0xBB
SNORLAX = 0xBE
BULBASAUR = 0x08

hWhoseTurn = 0xFF97
wOpponentDuelVariables = 0xC300
wOpponentDeck = 0xC480
DUELVARS_ARENA_CARD = 0xBB
BULBASAUR = 0x08
SNORLAX = 0xBE

hWhoseTurn = 0xFF97
wDamage = 0xCCB9
wPlayerDeck = 0xC400

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hTemp_ffa0 = 0xFFA0

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDuelTempList = 0xC510
hTempList = 0xFFA0
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wDamage = 0xCCB9
wAIMinDamage = 0xCCBA

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
hTempPlayAreaLocation_ff9d = 0xFF9D
wMetronomeEnergyCost = 0xCCF0
wDamage = 0xCCB9
wAIMinDamage = 0xCCBB
wAIMaxDamage = 0xCCBC
WATER_ENERGY = 0x03

hWhoseTurn = 0xFF97
wOpponentDuelVariables = 0xC300
hTemp_ffa0 = 0xFFA0

hWhoseTurn = 0xFF97

hWhoseTurn = 0xFF97
wOpponentDuelVariables = 0xC300
wOpponentDeck = 0xC480
IVYSAUR = 0x09

hWhoseTurn = 0xFF97
wOpponentDuelVariables = 0xC300
wOpponentDeck = 0xC480
WATER_ENERGY = 0x03

hTemp_ffa0 = 0xFFA0

hTemp_ffa0 = 0xFFA0
wDuelTempList = 0xC510
hWhoseTurn = 0xFF97

hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
hTemp_ffa0 = 0xFFA0
wDuelTempList = 0xC510
CHARMANDER = 0x30

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
WATER_ENERGY = 0x03

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wTempTurnDuelistCardID = 0xCCC3
BULBASAUR = 0x08
IVYSAUR = 0x09

hWhoseTurn = 0xFF97
wOpponentArenaCard = 0xC3BB
wOpponentDeck = 0xC480

wNoDamageOrEffect = 0xCCC7

hWhoseTurn = 0xFF97
hTemp_ffa0 = 0xFFA0

hWhoseTurn = 0xFF97
wDuelType = 0xCE22

hAIEnergyTransEnergyCard = 0xFFA2
hAIEnergyTransPlayAreaLocation = 0xFFA3
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTempCardIndex_ff9f = 0xFF9F
hTemp_ffa0 = 0xFFA0
hWhoseTurn = 0xFF97

wLoadedCard1Name = 0xCC27
wTxRam2 = 0xCE3F
wTxRam2_b = 0xCE41

hWhoseTurn = 0xFF97
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
hTemp_ffa0 = 0xFFA0
wNoDamageOrEffect = 0xCCC7

hWhoseTurn = 0xFF97
wDamage = 0xCCB9
wLoadedAttackAnimation = 0xCCB8

hWhoseTurn = 0xFF97
TURN_EFFECT = 0xC2F8
TURN_DAMAGE = 0xC2F3
TURN_STATUS = 0xC2F5
TURN_SUBSTATUS2 = 0xC2F6
NON_TURN_STATUS = 0xC3F0
NON_TURN_SUBSTATUS2 = 0xC3E8
wDamage = 0xCCB9
wLoadedAttackAnimation = 0xCCB8

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
hTemp_ffa0 = 0xFFA0

hTempList = 0xFFA0
wDuelTempList = 0xC510
hWhoseTurn = 0xFF97
player_duel_page = 0xC200
card_location = 0xC203
hand_count = 0xC2EE
discard_count = 0xC2ED
duelist_type = 0xC2F1
hand_card = 0xC242
discard_card = 0xC27E

hTemp_ffa0 = 0xFFA0
wDuelTempList = 0xC510
hWhoseTurn = 0xFF97
wDuelistType = 0xC2F1
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hCurSelectionItem = 0xFFB2
hKeysPressed = 0xFF91
hWhoseTurn = 0xFF97
wPlayerArenaCard = 0xC2BB
wPlayerDeck = 0xC242
wPlayerDuelistType = 0xC201
wOpponentDuelistType = 0xC301
wDuelDisplayedScreen = 0xCAC2
wDuelTempList = 0xC510
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTempCardIndex_ff98 = 0xFF98
wTotalAttachedEnergies = 0xCC23

hCurSelectionItem = 0xFFB2
hTempPlayAreaLocation_ffa1 = 0xFFA1
hTemp_ffa0 = 0xFFA0
wNumMenuItems = 0xCD14
hWhoseTurn = 0xFF97
wPlayerArenaCard = 0xC2BB
wExcludeArenaPokemon = 0xCBD2

wDuelTempList = 0xC510
wLoadedCard2Type = 0xCC65
wLoadedCard2Stage = 0xCC6E

KR_PLAYER_TURN = 0xC2
KR_wConsole = 0xCAB4
KR_wLCDC = 0xCABB
KR_ARENA_HP = 0xC8 - 0xBB
KR_ARENA_STAGE = 0xCE - 0xBB
KR_ARENA_STATUS = 0xF0 - 0xBB
KR_ARENA_PLUSPOWER = 0xE0 - 0xBB
KR_ARENA_DEFENDER = 0xE6 - 0xBB

Scaven_TURN = 0xC2
Scaven_CONSOLE = 0xCAB4
Scaven_LCDC = 0xCABB
Scaven_HP = 0xC8 - 0xBB
Scaven_STAGE = 0xCE - 0xBB
Scaven_STATUS = 0xF0 - 0xBB
Scaven_PLUS = 0xE0 - 0xBB
Scaven_DEF = 0xE6 - 0xBB

PLAYER_TURN = 0xC2
wConsole = 0xCAB4
wLCDC = 0xCABB
wEnergyDiscardMenuDenominator = 0xCBFA
wEnergyDiscardMenuNumerator = 0xCBFB
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xE6 - 0xBB

SR_TURN = 0xC2
SR_CONSOLE = 0xCAB4
SR_LCDC = 0xCABB
SR_HP = 0xC8 - 0xBB
SR_STAGE = 0xCE - 0xBB
SR_STATUS = 0xF0 - 0xBB
SR_PLUS = 0xE0 - 0xBB
SR_DEF = 0xE6 - 0xBB

wTempPlayAreaLocation_cceb = 0xCCEB
wTxRam2 = 0xCE3F
wTxRam2_b = 0xCE41
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
FRAME_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]

SAH_hTempPlayAreaLocation_ffa1 = 0xFFA1
SAH_hWhoseTurn = 0xFF97
SAH_TURN = 0xC2
SAH_DUELIST_TYPE = 0xC2F1
SAH_HAND_COUNT = 0xC2EE
SAH_HAND = 0xC242
SAH_wPlayerDeck = 0xC400
SAH_wLoadedCard1 = 0xCC24
SAH_wLCDC = 0xCABB
SAH_rLCDC = 0xFF40

RAH_hTempList = 0xFFA0
RAH_hWhoseTurn = 0xFF97
RAH_TURN = 0xC2
RAH_DUELIST_TYPE = 0xC2F1
RAH_LOCATIONS = 0xC200
RAH_DECK_CARDS = 0xC27E
RAH_NOT_IN_DECK = 0xC2BA
RAH_wPlayerDeck = 0xC400
RAH_wLoadedCard1 = 0xCC24
RAH_wLCDC = 0xCABB
RAH_rLCDC = 0xFF40

wStage = 0xC2CF

CFF_hTemp_ffa0 = 0xFFA0
CFF_hWhoseTurn = 0xFF97
CFF_TURN = 0xC2
CFF_DUELIST_TYPE = 0xC2F1
CFF_LOCATIONS = 0xC200
CFF_DECK_CARDS = 0xC27E
CFF_NOT_IN_DECK = 0xC2BA
CFF_HAND_COUNT = 0xC2EE
CFF_NUM_IN_PLAY = 0xC2CF
CFF_wLCDC = 0xCABB

CFF_hTemp_ffa0 = 0xFFA0
CFF_hWhoseTurn = 0xFF97
CFF_LCD_SHADOW = 0xCABB
CFF_DUELIST_TYPE = 0xC2F1
CFF_OTHER_DUELIST_TYPE = 0xC3F1
CFF_OTHER_LOCATIONS = 0xC300
CFF_OTHER_DECK_CARDS = 0xC37E
CFF_OTHER_DISCARD_COUNT = 0xC3ED
CFF_OTHER_HAND_COUNT = 0xC3EE
CFF_OTHER_PLAY_COUNT = 0xC3CF

RV_hTemp_ffa0 = 0xFFA0
RV_hWhoseTurn = 0xFF97
RV_TURN = 0xC2
RV_DUELIST_TYPE = 0xC2F1
RV_LOCATIONS = 0xC200
RV_ARENA_HP = 0xC2C8
RV_NUM_IN_PLAY = 0xC2CF
RV_HAND_COUNT = 0xC2EE
RV_DECK_CARDS = 0xC27E
RV_NOT_IN_DECK = 0xC2BA
RV_BULBASAUR = 0x08

IF_hTempList = 0xFFA0
IF_hWhoseTurn = 0xFF97
IF_TURN = 0xC2
IF_DUELIST_TYPE = 0xC2F1
IF_LOCATIONS = 0xC200
IF_HAND_COUNT = 0xC2EE
IF_HAND = 0xC242
IF_DISCARD_COUNT = 0xC2F2
IF_NOT_IN_DECK = 0xC2BA

hWhoseTurn = 0xFF97
wLCDC = 0xCABB
wDuelTempList = 0xC510
hTemp_ffa0 = 0xFFA0
wEnergyDiscardPlayAreaLocation = 0xCBE0

hTemp_ffa0 = 0xFFA0
hTempPlayAreaLocation_ffa1 = 0xFFA1
wDuelType = 0xCC09
hWhoseTurn = 0xFF97

hTempCardIndex_ff98 = 0xFF98
hTempPlayAreaLocation_ffa1 = 0xFFA1
hTemp_ffa0 = 0xFFA0
wLoadedCard2Stage = 0xCC6E
wLoadedCard2Type = 0xCC65

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerArenaCard = 0xC2BB
wExcludeArenaPokemon = 0xCBD2
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
PLAYER_TURN = 0xC2

hTemp_ffa0 = 0xFFA0
hTempPlayAreaLocation_ffa1 = 0xFFA1

wDealtDamage = 0xCCBF
wDuelDisplayedScreen = 0xCAC2
wNoDamageOrEffect = 0xCCC7

hTemp_ffa0 = 0xFFA0
wDuelDisplayedScreen = 0xCAC2

hTempList = 0xFFA0

hTempPlayAreaLocation_ff9d = 0xFF9D
hWhoseTurn = 0xFF97
wLoadedAttackAnimation = 0xCCB8

hCurSelectionItem = 0xFFB2
wDuelTempList = 0xC510

wPlayerDeck = 0xC27E
hWhoseTurn = 0xFF97
wDuelistType = 0xCC0D

hTemp_ffa0 = 0xFFA0
_wram_txram3 = 0xCE43

hCurSelectionItem = 0xFFB2
hTempCardIndex_ff98 = 0xFF98
hTempCardIndex_ff9f = 0xFF9F
wDuelTempList = 0xC500

hCurSelectionItem = 0xFFB2
hTempCardIndex_ff98 = 0xFF98
hWhoseTurn = 0xFF97
wDuelTempList = 0xC510

hTemp_ffa0 = 0xFFA0
wDuelDisplayedScreen = 0xCAC2
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

HPS_KEYS = [0x00, 0x01]
HPS_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
HPS_SEED = {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xCBD0: b"\x00", 0xCD9A: b"\x01", 0xC2BA: b"\x3B", 0xC2B9: b"\x01", 0xC401: b"\x08"}
HPS_READ = {0xCE75: 1, 0xC510: 2, 0xC51A: 2, 0xFFA1: 2, 0xFFB2: 1}

# The reference stays bounded only if WaitAttackAnimation's `call DoFrame /
# CheckAnyAnimationPlaying / jr c` loop retires on its first pass. That loop
# never advances animation state here because wDoFrameFunction is NULL, so the
# case has to make CheckAnyAnimationPlaying report "nothing playing": it ANDs
# wActiveScreenAnim ($D42A), wd4c0 ($D4C0) and wAnimationQueue ($D423, 7 bytes)
# and returns nc only when every one of them is $FF.
#   wAttackAnimationIsPlaying ($CE7E) = TRUE keeps PlayAttackAnimationCommands
#   off its ResetAnimationQueue prologue, which would otherwise re-register
#   wDoFrameFunction, enable the LCD and park WaitForVBlank at pc $0271.
#   wDuelAnimBufferCurPos ($D4AC) = 8 with wDuelAnimBufferSize ($D4AD) = 0 makes
#   LoadDuelAnimationToBuffer see (size + DUEL_ANIM_STRUCT_SIZE) & $7F == curpos,
#   i.e. a full ring, so every PlayDuelAnimation the heal command list issues is
#   a pure no-op on both sides and the seeded pair comes back unchanged.
#   wLCDC ($CABB) = 0 turns the single WaitForVBlank into an immediate return.
ANIM_IDLE = {
    0xCE7E: b"\x01",
    0xD423: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF",
    0xD42A: b"\xFF",
    0xD4C0: b"\xFF",
    0xD4AC: b"\x08",
    0xD4AD: b"\x00",
    0xCABB: b"\x00",
}

# Arena slot of the $C2 duelist: deck index 0 in DUELVARS_ARENA_CARD ($C2BB),
# that index mapping to card 1 in the deck card list at $C400, and the card's
# current HP in DUELVARS_ARENA_CARD_HP ($C2C8).
def _hp_recovery_case(hp, **kwargs):
    wram = {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x01",
            0xC2C8: bytes([hp]), 0xCCB8: b"\x00", 0xCCBD: b"\x00\x00"}
    wram.update(ANIM_IDLE)
    if "wram" in kwargs:
        wram.update(kwargs.pop("wram"))
    case = {"wram": wram,
            "read": {0xC2C8: 1, 0xCCB8: 1, 0xCCBD: 2},
            "instruction_budget": 20000000,
            "cycle_budget": 80000000}
    case.update(kwargs)
    return case

hTemp_ffa0 = 0xFFA0
_acid_toss_fix = {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x1E\x00"}
_acid_toss_fix_tail = dict(_acid_toss_fix)
_acid_toss_fix_tail[0xCACA] = b"\x00\x00\x80"
SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
BUDGET = dict(instruction_budget=20000000, cycle_budget=80000000)
POISON = dict(a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234)

hWhoseTurn = 0xFF97
wPlayerArenaCard = 0xC2BB
wPlayerDeck = 0xC400
wArenaCardStatus = 0xC2F0
wLoadedCard1ID = 0xCC2B
BULBASAUR = 0x08
CLEFAIRY_DOLL = 0xCB
MYSTERIOUS_FOSSIL = 0xCC
FRAME_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
FRAME_BUDGET = {"instruction_budget": 20000000, "cycle_budget": 80000000}

hAIPkmnPowerEffectParam = 0xFFA1

_RDP_BASE = {
    0xFF97: b"\xC2", 0xFF9D: b"\x01",
    0xC2EF: b"\x01", 0xC3EF: b"\x01",
    0xC2BB: b"\x00", 0xC3BB: b"\x00",
    0xC2C8: b"\x50", 0xC3C8: b"\x50",
    0xC400: b"\x01", 0xC480: b"\x01",
    0xCABB: b"\x00",
    0xCACA: b"\x00\x00\x00",
}
_RDP_IDLE = {
    0xCE7E: b"\x01",
    0xD423: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF",
    0xD42A: b"\xFF", 0xD4C0: b"\xFF",
    0xD4AC: b"\x08", 0xD4AD: b"\x00",
}
def _rdp_case(rng, poison=False):
    wram = dict(_RDP_BASE)
    wram.update(_RDP_IDLE)
    wram[0xCACA] = rng
    case = {
        "d": 0x00, "e": 0x14, "wram": wram,
        "read": {0xCCC7: 1, 0xCCE6: 1, 0xCCB8: 1},
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "instruction_budget": 20000000, "cycle_budget": 80000000,
    }
    if poison:
        case.update(POISON)
    return case

def _big_thunder_case(rng, poison=False):
    case = _rdp_case(rng, poison=poison)
    case["read"] = {0xCCC7: 1, 0xCCE6: 1, 0xCCB8: 1, 0xC2C8: 1, 0xC3C8: 1}
    return case

wDuelType = 0xCC09
hWhoseTurn = 0xFF97
wLCDC = 0xCABB
wDuelDisplayedScreen = 0xCAC2
hTemp_ffa0 = 0xFFA0

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
hTempCardIndex_ff9f = 0xFF9F
hCurSelectionItem = 0xFFB2
wDuelType = 0xCC09
wDuelTempList = 0xC510

hTempList = 0xFFA0
hWhoseTurn = 0xFF97
wDuelType = 0xCC09
wDuelDisplayedScreen = 0xCAC2
wLCDC = 0xCABB
wNotInDeck = 0xC2BA
wDiscardCount = 0xC2ED
wHandCount = 0xC2EE

PB_TURN = 0xC2
PB_HWHOSE_TURN = 0xFF97
PB_DUELIST_TYPE = 0xC2F1
PB_LOCATIONS = 0xC200
PB_DECK_CARDS = 0xC27E
PB_NOT_IN_DECK = 0xC2BA
PB_HAND_COUNT = 0xC2EE
PB_WLCDC = 0xCABB

hTempPlayAreaLocation_ff9d = 0xFF9D
hWhoseTurn = 0xFF97
wLoadedAttackAnimation = 0xCCB8
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wAnimationsDisabled = 0xD421
wLCDC = 0xCABB
# <<< factory-cases-statics

# >>> factory AIPickAttackForAmnesia
CONTRACT["AIPickAttackForAmnesia"] = {"compare": ("a",), "preserve": ()}
CASES["AIPickAttackForAmnesia"] = [
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wOpponentDeck: bytes((BULBASAUR,))}, "read": {hWhoseTurn: 1}},
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wOpponentDeck: bytes((SNORLAX,))}, "read": {hWhoseTurn: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wOpponentDeck: bytes((SNORLAX,))}, read={hWhoseTurn: 1}),
]
# <<< factory AIPickAttackForAmnesia

# >>> factory MirrorMove_AISelection
CONTRACT["MirrorMove_AISelection"] = {"compare": (), "preserve": ()}
CASES["MirrorMove_AISelection"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x77"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x03", 0xFFA0: b"\x77"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x01", 0xC0EF: b"\x00", 0xFFA0: b"\x77"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2F8: b"\x02", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wOpponentDeck: bytes((BULBASAUR,)), 0xFFA0: b"\x77"}),
]
# <<< factory MirrorMove_AISelection

# >>> factory KinglerFlail_HPCheck
CONTRACT["KinglerFlail_HPCheck"] = {"compare": (), "preserve": ()}
CASES["KinglerFlail_HPCheck"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", wPlayerDeck: b"\x01", wDamage: b"\x99", wAIMinDamage: b"\x88"},
     "read": {wDamage: 1, wAIMinDamage: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", wPlayerDeck: b"\x01", wDamage: b"\x77", wAIMinDamage: b"\x66"},
     "read": {wDamage: 1, wAIMinDamage: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x71", wPlayerDeck: b"\x01", wDamage: b"\x55", wAIMinDamage: b"\x44"},
         read={wDamage: 1, wAIMinDamage: 1}),
]
# <<< factory KinglerFlail_HPCheck

# >>> factory MagikarpFlail_HPCheck
CONTRACT["MagikarpFlail_HPCheck"] = {"compare": (), "preserve": ()}
CASES["MagikarpFlail_HPCheck"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", wPlayerDeck: b"\x01", wDamage: b"\x99", wAIMinDamage: b"\x88"},
     "read": {wDamage: 1, wAIMinDamage: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", wPlayerDeck: b"\x01", wDamage: b"\x77", wAIMinDamage: b"\x66"},
     "read": {wDamage: 1, wAIMinDamage: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x71", wPlayerDeck: b"\x01", wDamage: b"\x55", wAIMinDamage: b"\x44"},
         read={wDamage: 1, wAIMinDamage: 1}),
]
# <<< factory MagikarpFlail_HPCheck

# >>> factory SuperFang_HalfHPEffect
CONTRACT["SuperFang_HalfHPEffect"] = {"compare": (), "preserve": ()}
CASES["SuperFang_HalfHPEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3C8: b"\x00", 0xCCB9: b"\x12\x34", 0xCCBB: b"\x56", 0xCCBC: b"\x78"},
     "read": {0xFF97: 1, 0xC3C8: 1, 0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC3C8: b"\x3C", 0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
     "read": {0xFF97: 1, 0xC3C8: 1, 0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xFF97: b"\xC3", 0xC2C8: b"\x33", 0xCCB9: b"\x01\x02", 0xCCBB: b"\x03", 0xCCBC: b"\x04"},
     "read": {0xFF97: 1, 0xC2C8: 1, 0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xFF97: b"\xC2", 0xC3C8: b"\xFF", 0xCCB9: b"\x99\x88", 0xCCBB: b"\x77", 0xCCBC: b"\x66"},
     "read": {0xFF97: 1, 0xC3C8: 1, 0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory SuperFang_HalfHPEffect

# >>> factory KarateChop_DamageSubtractionEffect
CONTRACT["KarateChop_DamageSubtractionEffect"] = {"compare": (), "preserve": ()}
CASES["KarateChop_DamageSubtractionEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
              wPlayerDeck: b"\x01", wDamage: b"\xFF\x00"},
     "read": {wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05",
              wPlayerDeck: b"\x01", wDamage: b"\xFF\x00"},
     "read": {wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xD0",
              wPlayerDeck: b"\x01", wDamage: b"\xFF\x00"},
     "read": {wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
                       wPlayerDeck: b"\x01", wDamage: b"\xFF\x00"},
         read={wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory KarateChop_DamageSubtractionEffect

# >>> factory SpearowMirrorMove_AISelection
CONTRACT["SpearowMirrorMove_AISelection"] = {"compare": (), "preserve": ()}
CASES["SpearowMirrorMove_AISelection"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x77"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x03", 0xFFA0: b"\x77"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F8: b"\x01", 0xC0EF: b"\x00", 0xFFA0: b"\x77"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2F8: b"\x02", wOpponentDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wOpponentDeck: bytes((BULBASAUR,)), 0xFFA0: b"\x77"}),
]
# <<< factory SpearowMirrorMove_AISelection

# >>> factory CharmeleonFlamethrower_AISelectEffect
CONTRACT["CharmeleonFlamethrower_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["CharmeleonFlamethrower_AISelectEffect"] = [
    {"wram": {0xC510: bytes(0x40), 0xFFA0: bytes(0x10)}},
    {"wram": {0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}},
    dict(POISON, wram={0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}),
]
# <<< factory CharmeleonFlamethrower_AISelectEffect

# >>> factory ClefableMetronome_AISelectEffect
CONTRACT["ClefableMetronome_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClefableMetronome_AISelectEffect"] = [
    {"wram": {0xC100: b"\x00"}},
    dict(POISON, wram={0xC100: b"\x00"}),
]
# <<< factory ClefableMetronome_AISelectEffect

# >>> factory Ember_AISelectEffect
CONTRACT["Ember_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Ember_AISelectEffect"] = [
    {"wram": {0xC510: bytes(0x40), 0xFFA0: bytes(0x10)}},
    {"wram": {0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}},
    dict(POISON, wram={0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}),
]
# <<< factory Ember_AISelectEffect

# >>> factory FlareonFlamethrower_AISelectEffect
CONTRACT["FlareonFlamethrower_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["FlareonFlamethrower_AISelectEffect"] = [
    {"wram": {0xC510: bytes(0x40), 0xFFA0: bytes(0x10)}},
    {"wram": {0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}},
    dict(POISON, wram={0xC510: b"\x00\x64\xff\xff" + bytes(0x3C), 0xFFA0: bytes(0x10)}),
]
# <<< factory FlareonFlamethrower_AISelectEffect

# >>> factory DestinyBond_DestinyBondEffect
CONTRACT["DestinyBond_DestinyBondEffect"] = {"compare": ("hl",), "preserve": ()};
CASES["DestinyBond_DestinyBondEffect"] = [
    {},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234},
]
# <<< factory DestinyBond_DestinyBondEffect

# >>> factory FlareonRage_AIEffect
CONTRACT["FlareonRage_AIEffect"] = {"compare": (), "preserve": ()}
CASES["FlareonRage_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", 0xC400: b"\x01", 0xCCB9: b"\x10\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory FlareonRage_AIEffect

# >>> factory GolduckHyperBeam_AISelectEffect
CONTRACT["GolduckHyperBeam_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["GolduckHyperBeam_AISelectEffect"] = [
    {"read": {hTemp_ffa0: 1}},
    dict(POISON, read={hTemp_ffa0: 1}),
]
# <<< factory GolduckHyperBeam_AISelectEffect

# >>> factory OnixHardenEffect
CONTRACT["OnixHardenEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["OnixHardenEffect"] = [
    {},
    dict(POISON),
]
# <<< factory OnixHardenEffect

# >>> factory PoliwhirlAmnesia_AISelectEffect
CONTRACT["PoliwhirlAmnesia_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["PoliwhirlAmnesia_AISelectEffect"] = [
	{"read": {hTemp_ffa0: 1}},
	dict(POISON, read={hTemp_ffa0: 1}),
]
# <<< factory PoliwhirlAmnesia_AISelectEffect

# >>> factory StretchKick_AISelectEffect
CONTRACT["StretchKick_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["StretchKick_AISelectEffect"] = [
    {"read": {hTemp_ffa0: 1}},
    dict(POISON, read={hTemp_ffa0: 1}),
]
# <<< factory StretchKick_AISelectEffect

# >>> factory VaporeonWaterGunEffect
CONTRACT["VaporeonWaterGunEffect"] = {"compare": (), "preserve": ()};
CASES["VaporeonWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory VaporeonWaterGunEffect

# >>> factory Potion_DamageCheck
CONTRACT["Potion_DamageCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["Potion_DamageCheck"] = [
    {},
    dict(POISON),
]
# <<< factory Potion_DamageCheck

# >>> factory CloysterSpikeCannon_AIEffect
CONTRACT["CloysterSpikeCannon_AIEffect"] = {"compare": (), "preserve": ()}
CASES["CloysterSpikeCannon_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory CloysterSpikeCannon_AIEffect

# >>> factory JolteonDoubleKick_AIEffect
CONTRACT["JolteonDoubleKick_AIEffect"] = {"compare": (), "preserve": ()}
CASES["JolteonDoubleKick_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory JolteonDoubleKick_AIEffect

# >>> factory RapidashStomp_AIEffect
CONTRACT["RapidashStomp_AIEffect"] = {"compare": (), "preserve": ()}
CASES["RapidashStomp_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory RapidashStomp_AIEffect

# >>> factory StoneBarrage_AIEffect
CONTRACT["StoneBarrage_AIEffect"] = {"compare": (), "preserve": ()}
CASES["StoneBarrage_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", 0xCCBB: b"\x00", 0xCCBC: b"\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB", 0xCCBB: b"\xCC", 0xCCBC: b"\xDD"},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xCCB9: b"\xFF\xFF", 0xCCBB: b"\xFF", 0xCCBC: b"\xFF"},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory StoneBarrage_AIEffect

# >>> factory DestinyBond_AISelectEffect
CONTRACT["DestinyBond_AISelectEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DestinyBond_AISelectEffect"] = [
    {"read": {wDuelTempList: 1, hTempList: 1}},
    dict(POISON, read={wDuelTempList: 1, hTempList: 1}),
]
# <<< factory DestinyBond_AISelectEffect

# >>> factory Rampage_AIEffect
CONTRACT["Rampage_AIEffect"] = {"compare": (), "preserve": ()}
CASES["Rampage_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", 0xC400: b"\x01", 0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", 0xC400: b"\x01", 0xCCB9: b"\x10\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xFF", 0xC400: b"\x01", 0xCCB9: b"\xFF\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
]
# <<< factory Rampage_AIEffect

# >>> factory SuperPotion_DamageEnergyCheck
CONTRACT["SuperPotion_DamageEnergyCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SuperPotion_DamageEnergyCheck"] = [
    {},
    dict(POISON),
]
# <<< factory SuperPotion_DamageEnergyCheck

# >>> factory KrabbyCallForFamily_CheckDeckAndPlayArea
CONTRACT["KrabbyCallForFamily_CheckDeckAndPlayArea"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["KrabbyCallForFamily_CheckDeckAndPlayArea"] = [
    {},
    dict(POISON),
    {"wram": {0xC2BA: b"\x01", 0xC2EF: b"\x00"}},
    {"wram": {0xC2BA: b"\x01", 0xC2EF: b"\x06"}},
    {"wram": {0xC2BA: b"\x01", 0xC2EF: b"\x07"}},
]
# <<< factory KrabbyCallForFamily_CheckDeckAndPlayArea

# >>> factory Revive_BenchCheck
CONTRACT["Revive_BenchCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["Revive_BenchCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x00", 0xC27E: b"\x00", 0xC37E: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x05", 0xC27E: b"\x00", 0xC37E: b"\x00"}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x06", 0xC27E: b"\x00", 0xC37E: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x05", 0xC27E: b"\x00", 0xC37E: b"\x00"}),
]
# <<< factory Revive_BenchCheck

# >>> factory DragonairHyperBeam_DiscardEffect
CONTRACT["DragonairHyperBeam_DiscardEffect"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["DragonairHyperBeam_DiscardEffect"] = [
    {"hl": 0xC100, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x00"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    {"hl": 0xC100, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\xFF"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    {"hl": 0xC300, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xC300: b"\xFF", 0xFFA0: b"\x2A"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    dict(POISON, hl=0xC100, wram={0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x05"}, read={0xC000: 0xF00, 0xC3F8: 1}),
]
# <<< factory DragonairHyperBeam_DiscardEffect

# >>> factory MirrorMove_ExecuteStatusEffect
CONTRACT["MirrorMove_ExecuteStatusEffect"] = {"compare": ("f",), "preserve": ()}
CASES["MirrorMove_ExecuteStatusEffect"] = [
    {"a": 0xc0, "wram": {0xff97: b"\x00", 0xcc05: b"\x01"}, "read": {0xccce: 3, 0xcccd: 1}},
    {"a": 0x80, "wram": {0xff97: b"\x00", 0xcc05: b"\x01"}, "read": {0xccce: 3, 0xcccd: 1}},
    {"a": 0x01, "wram": {0xff97: b"\x00", 0xcc05: b"\x01"}, "read": {0xccce: 3, 0xcccd: 1}},
    {"a": 0x02, "wram": {0xff97: b"\x00", 0xcc05: b"\x01"}, "read": {0xccce: 3, 0xcccd: 1}},
    dict(POISON, a=0x03, wram={0xff97: b"\x00", 0xcc05: b"\x01"}, read={0xccce: 3, 0xcccd: 1}),
]
# <<< factory MirrorMove_ExecuteStatusEffect

# >>> factory Curse_CheckDamageAndBench
CONTRACT["Curse_CheckDamageAndBench"] = {"compare": ("f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e"), "hram_out": True}
CASES["Curse_CheckDamageAndBench"] = [
    {"wram": {0xFF9D: b"\x00", 0xC2C2: b"\x20"}, "expect": {0xFFA0: b"\x00"}},
    {"wram": {0xFF9D: b"\x00", 0xC2C2: b"\x00", 0xC3EF: b"\x01"}, "expect": {0xFFA0: b"\x00"}},
    {"wram": {0xFF9D: b"\x00", 0xC2C2: b"\x00", 0xC3EF: b"\x02", 0xC3BB: b"\x00", 0xC3BC: b"\x00", 0xC3C8: b"\x00", 0xC3C9: b"\x00"}, "expect": {0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFF9D: b"\x01", 0xC2C3: b"\x20"}, expect={0xFFA0: b"\x01"}),
]
# <<< factory Curse_CheckDamageAndBench

# >>> factory SpearowMirrorMove_AIEffect
CONTRACT["SpearowMirrorMove_AIEffect"] = {"compare": (), "preserve": ()}
CASES["SpearowMirrorMove_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x2A", 0xCCBB: b"\x00", 0xCCBC: b"\x00"}, "expect": {0xCCBB: b"\x2A", 0xCCBC: b"\x2A"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F3: b"\x7F", 0xCCBB: b"\x11", 0xCCBC: b"\x22"}, expect={0xCCBB: b"\x7F", 0xCCBC: b"\x7F"}),
]
# <<< factory SpearowMirrorMove_AIEffect

# >>> factory SpearowMirrorMove_InitialEffect1
CONTRACT["SpearowMirrorMove_InitialEffect1"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SpearowMirrorMove_InitialEffect1"] = [
    {},
    dict(POISON),
]
# <<< factory SpearowMirrorMove_InitialEffect1

# >>> factory PidgeottoMirrorMove_AIEffect
CONTRACT["PidgeottoMirrorMove_AIEffect"] = {"compare": (), "preserve": ()}
CASES["PidgeottoMirrorMove_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F3: b"\x2A", 0xCCBB: b"\x00", 0xCCBC: b"\x00"}, "expect": {0xCCBB: b"\x2A", 0xCCBC: b"\x2A"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F3: b"\x7F", 0xCCBB: b"\x11", 0xCCBC: b"\x22"}, expect={0xCCBB: b"\x7F", 0xCCBC: b"\x7F"}),
]
# <<< factory PidgeottoMirrorMove_AIEffect

# >>> factory PidgeottoMirrorMove_AISelection
CONTRACT["PidgeottoMirrorMove_AISelection"] = {"compare": (), "preserve": ()}
CASES["PidgeottoMirrorMove_AISelection"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x77"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x55"}, read={0xFFA0: 1}),
]
# <<< factory PidgeottoMirrorMove_AISelection

# >>> factory ClefairyMetronome_AISelectEffect
CONTRACT["ClefairyMetronome_AISelectEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl"), "wram_out": True}
CASES["ClefairyMetronome_AISelectEffect"] = [
    {"wram": {0xC100: b"\x00"}, "expect": {0xC100: b"\x00"}},
    dict(POISON, wram={0xC100: b"\x00"}, expect={0xC100: b"\x00"}),
]
# <<< factory ClefairyMetronome_AISelectEffect

# >>> factory EnergySpike_DeckCheck
CONTRACT["EnergySpike_DeckCheck"] = {"compare": ("a", "f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["EnergySpike_DeckCheck"] = [
    {},
    {"wram": {0xC2BA: b"\x3C"}},
    {"wram": {0xC2BA: b"\x50"}},
    dict(POISON),
]
# <<< factory EnergySpike_DeckCheck

# >>> factory MagmarFlamethrower_AISelectEffect
CONTRACT["MagmarFlamethrower_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["MagmarFlamethrower_AISelectEffect"] = [
    {"wram": {0xC510: b"\x00\x00\x00\x00", 0xFFA0: b"\x00"}, "read": {0xC510: 8, 0xFFA0: 1}},
    dict(POISON, wram={0xC510: b"\xAA\xBB\xCC\xDD", 0xFFA0: b"\x00"}, read={0xC510: 8, 0xFFA0: 1}),
    {"wram": {0xC510: b"\x01\xFF\x00\x00", 0xFFA0: b"\x00"}, "read": {0xC510: 8, 0xFFA0: 1}},
]
# <<< factory MagmarFlamethrower_AISelectEffect

# >>> factory OmastarWaterGunEffect
CONTRACT["OmastarWaterGunEffect"] = {"compare": (), "preserve": ()};
CASES["OmastarWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory OmastarWaterGunEffect

# >>> factory CuboneRage_AIEffect
CONTRACT["CuboneRage_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["CuboneRage_AIEffect"] = [
    {"wram": {0xCCB9: b"\x05"}, "read": {0xCCB9: 1, 0xCCBB: 1}},
    dict(POISON, wram={0xCCB9: b"\x05"}, read={0xCCB9: 1, 0xCCBB: 1}),
]
# <<< factory CuboneRage_AIEffect

# >>> factory GravelerHardenEffect
CONTRACT["GravelerHardenEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["GravelerHardenEffect"] = [
    {},
    dict(POISON),
]
# <<< factory GravelerHardenEffect

# >>> factory KarateChop_AIEffect
CONTRACT["KarateChop_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["KarateChop_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
              0xC400: b"\x01", 0xCCB9: b"\xFA\x00"},
     "read": {0xCCB9: 2, 0xCCBB: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
                       0xC400: b"\x01", 0xCCB9: b"\xFA\x00"},
         read={0xCCB9: 2, 0xCCBB: 1}),
]
# <<< factory KarateChop_AIEffect

# >>> factory LaprasWaterGunEffect
CONTRACT["LaprasWaterGunEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LaprasWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory LaprasWaterGunEffect

# >>> factory OmanyteWaterGunEffect
CONTRACT["OmanyteWaterGunEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["OmanyteWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory OmanyteWaterGunEffect

# >>> factory PoliwrathWaterGunEffect
CONTRACT["PoliwrathWaterGunEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PoliwrathWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00", 0xCC23: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00", 0xCC23: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory PoliwrathWaterGunEffect

# >>> factory SeadraWaterGunEffect
CONTRACT["SeadraWaterGunEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SeadraWaterGunEffect"] = [
    {"wram": {0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00", 0xCC23: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x0A", 0xCCF0: b"\x00", 0xFF9D: b"\x00", 0xCC23: b"\x00"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SeadraWaterGunEffect

# >>> factory SuperFang_AIEffect
CONTRACT["SuperFang_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SuperFang_AIEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xCCB9: b"\x0A\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCCB9: b"\x0A\x00"}, read={0xCCB9: 2, 0xCCBB: 1}),
]
# <<< factory SuperFang_AIEffect

# >>> factory DragoniteLv41Slam_AIEffect
CONTRACT["DragoniteLv41Slam_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DragoniteLv41Slam_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory DragoniteLv41Slam_AIEffect

# >>> factory ElectabuzzQuickAttack_AIEffect
CONTRACT["ElectabuzzQuickAttack_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ElectabuzzQuickAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory ElectabuzzQuickAttack_AIEffect

# >>> factory JolteonQuickAttack_AIEffect
CONTRACT["JolteonQuickAttack_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["JolteonQuickAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory JolteonQuickAttack_AIEffect

# >>> factory LeekSlap_AIEffect
CONTRACT["LeekSlap_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LeekSlap_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory LeekSlap_AIEffect

# >>> factory PinMissile_AIEffect
CONTRACT["PinMissile_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PinMissile_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory PinMissile_AIEffect

# >>> factory SandslashFurySwipes_AIEffect
CONTRACT["SandslashFurySwipes_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SandslashFurySwipes_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SandslashFurySwipes_AIEffect

# >>> factory Thunderpunch_AIEffect
CONTRACT["Thunderpunch_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Thunderpunch_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x00\x00"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory Thunderpunch_AIEffect

# >>> factory StarmieRecover_AISelectEffect
CONTRACT["StarmieRecover_AISelectEffect"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["StarmieRecover_AISelectEffect"] = [
    {"wram": {0xFF97: b"\x00"}, "read": {0xC510: 1, 0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\x00"}, read={0xC510: 1, 0xFFA0: 1}),
]
# <<< factory StarmieRecover_AISelectEffect

# >>> factory BellsproutCallForFamily_CheckDeckAndPlayArea
CONTRACT["BellsproutCallForFamily_CheckDeckAndPlayArea"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["BellsproutCallForFamily_CheckDeckAndPlayArea"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00", 0xC2EF: b"\x03"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C"}),
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00", 0xC2EF: b"\x06"}},
]
# <<< factory BellsproutCallForFamily_CheckDeckAndPlayArea

# >>> factory Spark_AISelectEffect
CONTRACT["Spark_AISelectEffect"] = {"compare": ("a",), "preserve": (), "wram_out": True}
CASES["Spark_AISelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01"}, read={0xFFA0: 1}),
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x02", 0xC0EF: b"\x01"}, "read": {0xFFA0: 1}},
]
# <<< factory Spark_AISelectEffect

# >>> factory DamageSwap_CheckDamage
CONTRACT["DamageSwap_CheckDamage"] = {"compare": ("f", "hl"), "preserve": (), "wram_out": True}
CASES["DamageSwap_CheckDamage"] = [
    {"wram": {0xFF9D: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xFF9D: b"\x00"}, read={0xFFA0: 1}, instruction_budget=2000000, cycle_budget=8000000),
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xC2C8: b"\x28", 0xFF9D: b"\x00", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF"}, "read": {0xFFA0: 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory DamageSwap_CheckDamage

# >>> factory PokemonFlute_BenchCheck
CONTRACT["PokemonFlute_BenchCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["PokemonFlute_BenchCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x06"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x06"}),
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x02", 0xC37E: b"\x00"}, "read": {0xC510: 1}},
]
# <<< factory PokemonFlute_BenchCheck

# >>> factory Heal_OncePerTurnCheck
CONTRACT["Heal_OncePerTurnCheck"] = {"compare": ("f", "hl"), "preserve": (), "wram_out": True}
CASES["Heal_OncePerTurnCheck"] = [
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x20"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x20"}, read={0xFFA0: 1}),
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x00", 0xC2EF: b"\x01",
              0xC2BB: b"\x00", 0xC400: b"\x08", 0xC2C8: b"\x28"}, "read": {0xFFA0: 1}},
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2C2: b"\x00",
              0xC2BC: b"\xFF", 0xC3BC: b"\xFF"}, "read": {0xFFA0: 1}},
]
# <<< factory Heal_OncePerTurnCheck

# >>> factory Shift_ChangeColorEffect
CONTRACT["Shift_ChangeColorEffect"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["Shift_ChangeColorEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xFFA1: b"\x03",
              0xC2BB: b"\x10", 0xC400 + 0x10: b"\x20", 0xC2C2: b"\x00", 0xC2D4: b"\x00",
              0xCC27: b"\x00\x00"},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC2C2: 1, 0xC2D4: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xFFA1: b"\x03",
              0xC2BB: b"\x10", 0xC400 + 0x10: b"\x20", 0xC2C2: b"\x00", 0xC2D4: b"\x00",
              0xCC27: b"\x00\x00"},
         keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC2C2: 1, 0xC2D4: 1}),
]
# <<< factory Shift_ChangeColorEffect

# >>> factory MagikarpFlail_AIEffect
CONTRACT["MagikarpFlail_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["MagikarpFlail_AIEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", wPlayerDeck: b"\x01",
              wDamage: b"\x99", wAIMinDamage: b"\x88"},
     "read": {wDamage: 1, wAIMinDamage: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", wPlayerDeck: b"\x01",
                       wDamage: b"\x77", wAIMinDamage: b"\x66"},
         read={wDamage: 1, wAIMinDamage: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory MagikarpFlail_AIEffect

# >>> factory PoliwagWaterGunEffect
CONTRACT["PoliwagWaterGunEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PoliwagWaterGunEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wMetronomeEnergyCost: b"\x00", wDamage: b"\x0A",
              wPlayerDuelVariables: b"\x10\x10\x10",
              wPlayerDeck: bytes((WATER_ENERGY, WATER_ENERGY, WATER_ENERGY))},
     "read": {wDamage: 1, wAIMinDamage: 1, wAIMaxDamage: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
                       wMetronomeEnergyCost: b"\x00", wDamage: b"\x0A",
                       wPlayerDuelVariables: b"\x10\x10\x10",
                       wPlayerDeck: bytes((WATER_ENERGY, WATER_ENERGY, WATER_ENERGY))},
         read={wDamage: 1, wAIMinDamage: 1, wAIMaxDamage: 1}),
]
# <<< factory PoliwagWaterGunEffect

# >>> factory TaurosStomp_AIEffect
CONTRACT["TaurosStomp_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["TaurosStomp_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory TaurosStomp_AIEffect

# >>> factory DodrioRage_AIEffect
CONTRACT["DodrioRage_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DodrioRage_AIEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xC9",
              wPlayerDeck: b"\x01", wDamage: b"\x05\x00"},
     "read": {wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\xC9",
                       wPlayerDeck: b"\x01", wDamage: b"\x05\x00"},
         read={wDamage: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory DodrioRage_AIEffect

# >>> factory DragoniteLv45Slam_AIEffect
CONTRACT["DragoniteLv45Slam_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DragoniteLv45Slam_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory DragoniteLv45Slam_AIEffect

# >>> factory GengarDarkMind_AISelectEffect
CONTRACT["GengarDarkMind_AISelectEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["GengarDarkMind_AISelectEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + 0xEF: b"\x01"},
     "read": {hTemp_ffa0: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wOpponentDuelVariables + 0xEF: b"\x02",
                       0xC0EF: b"\x01", 0xC1EF: b"\x01"},
         read={hTemp_ffa0: 1}),
]
# <<< factory GengarDarkMind_AISelectEffect

# >>> factory PoliwhirlDoubleslap_AIEffect
CONTRACT["PoliwhirlDoubleslap_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PoliwhirlDoubleslap_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory PoliwhirlDoubleslap_AIEffect

# >>> factory KinglerFlail_AIEffect
CONTRACT["KinglerFlail_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["KinglerFlail_AIEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00", wPlayerDeck: b"\x01",
              wDamage: b"\x99", wAIMinDamage: b"\x88"},
     "read": {wDamage: 1, wAIMinDamage: 1, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05", wPlayerDeck: b"\x01",
                       wDamage: b"\x77", wAIMinDamage: b"\x66"},
         read={wDamage: 1, wAIMinDamage: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory KinglerFlail_AIEffect

# >>> factory JynxDoubleslap_AIEffect
CONTRACT["JynxDoubleslap_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["JynxDoubleslap_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory JynxDoubleslap_AIEffect

# >>> factory Bonemerang_AIEffect
CONTRACT["Bonemerang_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Bonemerang_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory Bonemerang_AIEffect

# >>> factory Barrier_BarrierEffect
CONTRACT["Barrier_BarrierEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Barrier_BarrierEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2E7: b"\x00"}, "read": {0xC2E7: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2E7: b"\x00"}, read={0xC2E7: 1}),
]
# <<< factory Barrier_BarrierEffect

# >>> factory HydroPumpEffect
CONTRACT["HydroPumpEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HydroPumpEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wMetronomeEnergyCost: b"\x00", wDamage: b"\x0A",
              wPlayerDuelVariables: b"\x10\x10\x10\x10\x10",
              wPlayerDeck: bytes((WATER_ENERGY,)) * 5},
     "read": {wDamage: 1, wAIMinDamage: 1, wAIMaxDamage: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
                       wMetronomeEnergyCost: b"\x00", wDamage: b"\x0A",
                       wPlayerDuelVariables: b"\x10\x10\x10\x10\x10",
                       wPlayerDeck: bytes((WATER_ENERGY,)) * 5},
         read={wDamage: 1, wAIMinDamage: 1, wAIMaxDamage: 1}),
]
# <<< factory HydroPumpEffect

# >>> factory MysteryAttack_AIEffect
CONTRACT["MysteryAttack_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["MysteryAttack_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\xAA\xBB"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory MysteryAttack_AIEffect

# >>> factory HurricaneEffect
CONTRACT["HurricaneEffect"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["HurricaneEffect"] = [
    {"hl": 0x0000, "wram": {0xCCC7: b"\x80"}},
    {"hl": 0x1234, "wram": {0xCCC7: b"\x00", hWhoseTurn: b"\xC2",
              wOpponentDuelVariables + 0xC8: b"\x00"},
     "read": {hWhoseTurn: 1}},
    dict(POISON, hl=0x1234, wram={0xCCC7: b"\x00", hWhoseTurn: b"\xC2",
                       wOpponentDuelVariables + 0xC8: b"\x1E",
                       wOpponentDuelVariables: b"\x00" * 60,
                       wOpponentDuelVariables + 0xBB: b"\x00",
                       wOpponentDeck: bytes((IVYSAUR,))},
         keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=2000000, cycle_budget=8000000,
         read={hWhoseTurn: 1, wOpponentDuelVariables + 0xBB: 1, wOpponentDuelVariables + 0xC8: 1}),
]
# <<< factory HurricaneEffect

# >>> factory Psychic_AIEffect
CONTRACT["Psychic_AIEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Psychic_AIEffect"] = [
    {"wram": {0xCCB9: b"\x00\x00", hWhoseTurn: b"\xC2",
              wOpponentDuelVariables: b"\x10", wOpponentDeck: bytes((WATER_ENERGY,))},
     "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x05\x00", hWhoseTurn: b"\xC2",
                       wOpponentDuelVariables: b"\x10", wOpponentDeck: bytes((WATER_ENERGY,))},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory Psychic_AIEffect

# >>> factory SlowpokeAmnesia_AISelectEffect
CONTRACT["SlowpokeAmnesia_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["SlowpokeAmnesia_AISelectEffect"] = [
    {"read": {hTemp_ffa0: 1}},
    dict(POISON, read={hTemp_ffa0: 1}),
]
# <<< factory SlowpokeAmnesia_AISelectEffect

# >>> factory KadabraRecover_AISelectEffect
CONTRACT["KadabraRecover_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["KadabraRecover_AISelectEffect"] = [
    {"wram": {hWhoseTurn: b"\x00"}, "read": {hTemp_ffa0: 1}},
    dict(POISON, wram={hWhoseTurn: b"\x00"}, read={hTemp_ffa0: 1}),
]
# <<< factory KadabraRecover_AISelectEffect

# >>> factory GolduckHyperBeam_DiscardEffect
CONTRACT["GolduckHyperBeam_DiscardEffect"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GolduckHyperBeam_DiscardEffect"] = [
    {"hl": 0xC100, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x00"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    {"hl": 0xC100, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\xFF"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    {"hl": 0xC300, "wram": {0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xC300: b"\xFF", 0xFFA0: b"\x2A"}, "read": {0xC000: 0xF00, 0xC3F8: 1}},
    dict(POISON, hl=0xC100, wram={0xFF97: b"\xC2", 0xC000: b"\x00" * 0xF00, 0xFFA0: b"\x05"}, read={0xC000: 0xF00, 0xC3F8: 1}),
]
# <<< factory GolduckHyperBeam_DiscardEffect

# >>> factory StrangeBehavior_CheckDamage
CONTRACT["StrangeBehavior_CheckDamage"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["StrangeBehavior_CheckDamage"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, hTempPlayAreaLocation_ff9d: b"\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, hTempPlayAreaLocation_ff9d: b"\x01"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, hTempPlayAreaLocation_ff9d: b"\x00"}),
]
# <<< factory StrangeBehavior_CheckDamage

# >>> factory EnergyTrans_PrintProcedure
CONTRACT["EnergyTrans_PrintProcedure"] = {"compare": (), "preserve": ()}
CASES["EnergyTrans_PrintProcedure"] = [
    {"wram": {hWhoseTurn: b"\xC2"}, "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, wram={hWhoseTurn: b"\xC2"}, keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=2000000, cycle_budget=8000000,
         vread={0: {0x9800: 0x400}}),
]
# <<< factory EnergyTrans_PrintProcedure

# >>> factory ItemFinder_HandDiscardPileCheck
CONTRACT["ItemFinder_HandDiscardPileCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["ItemFinder_HandDiscardPileCheck"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x05", 0xC37E: b"\x00"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x01"}),
]
# <<< factory ItemFinder_HandDiscardPileCheck

# >>> factory Wildfire_DiscardEnergyEffect
CONTRACT["Wildfire_DiscardEnergyEffect"] = {"compare": (), "preserve": ()}
CASES["Wildfire_DiscardEnergyEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x00", 0xC000: b"\x00" * 0xF00}},
    {"wram": {hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x02", 0xC000: b"\x00" * 0xF00,
              wPlayerDuelVariables: bytes((0x10, 0x10)),
              wPlayerDeck: bytes((CHARMANDER, CHARMANDER))}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x02", 0xC000: b"\x00" * 0xF00,
                       wPlayerDuelVariables: bytes((0x10, 0x10)),
                       wPlayerDeck: bytes((CHARMANDER, CHARMANDER))}),
]
# <<< factory Wildfire_DiscardEnergyEffect

# >>> factory SuperEnergyRemoval_EnergyCheck
CONTRACT["SuperEnergyRemoval_EnergyCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SuperEnergyRemoval_EnergyCheck"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00,
              wPlayerDuelVariables: b"\x10", wPlayerDeck: bytes((WATER_ENERGY,))}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00}),
]
# <<< factory SuperEnergyRemoval_EnergyCheck

# >>> factory MorphEffect
CONTRACT["MorphEffect"] = {"compare": (), "preserve": ()}
CASES["MorphEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xBA: b"\x3C"},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "vread": {0: {0x9800: 0x400}}},
    {"wram": {hWhoseTurn: b"\xC2",
              wPlayerDuelVariables + 0xBA: b"\x00",
              wPlayerDeck: bytes([BULBASAUR]) * 60,
              wPlayerDuelVariables + 0xBB: b"\x05",
              wPlayerDuelVariables + 0xCE: b"\x00",
              wTempTurnDuelistCardID: bytes([IVYSAUR])},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xBA: b"\x3C"},
         keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=2000000, cycle_budget=8000000,
         vread={0: {0x9800: 0x400}}),
]
# <<< factory MorphEffect

# >>> factory AISelectConversionColor
CONTRACT["AISelectConversionColor"] = {"compare": (), "preserve": ()}
CASES["AISelectConversionColor"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01"}, read={0xFFA0: 1}),
]
# <<< factory AISelectConversionColor

# >>> factory PrintArenaCardNameAndColorText
CONTRACT["PrintArenaCardNameAndColorText"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintArenaCardNameAndColorText"] = [
    {"hl": 0, "d": 0x01, "e": 0x0E, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xFFA0: b"\x00", 0xC590: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0, d=0x01, e=0x0E, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xFFA0: b"\x00", 0xC590: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintArenaCardNameAndColorText

# >>> factory Conversion1_AISelectEffect
CONTRACT["Conversion1_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Conversion1_AISelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xFFA0: b"\xAA"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xFFA0: b"\xAA"}, read={0xFFA0: 1}),
]
# <<< factory Conversion1_AISelectEffect

# >>> factory Conversion2_ChangeResistanceEffect
CONTRACT["Conversion2_ChangeResistanceEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["Conversion2_ChangeResistanceEffect"] = [
    {"d": 0x01, "e": 0x0E, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xFFA0: b"\x00", 0xC590: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC2EA: 1}},
    dict(POISON, d=0x01, e=0x0E, wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xFFA0: b"\x00", 0xC590: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC2EA: 1}),
]
# <<< factory Conversion2_ChangeResistanceEffect

# >>> factory Conversion2_AISelectEffect
CONTRACT["Conversion2_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Conversion2_AISelectEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", wOpponentArenaCard: b"\x00", wOpponentDeck: b"\x10"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wOpponentArenaCard: b"\x00", wOpponentDeck: b"\x10"}, read={0xFFA0: 1}),
]
# <<< factory Conversion2_AISelectEffect

# >>> factory MirrorMove_AfterDamage
CONTRACT["MirrorMove_AfterDamage"] = {"compare": ("a", "hl", "d", "e"), "preserve": ("d", "e")}
CASES["MirrorMove_AfterDamage"] = [
    {"d": 0x01, "e": 0x0E, "wram": {wNoDamageOrEffect: b"\x01"}},
    dict(POISON, d=0x01, e=0x0E, wram={wNoDamageOrEffect: b"\x01"}),
]
# <<< factory MirrorMove_AfterDamage

# >>> factory PidgeottoMirrorMove_AfterDamage
CONTRACT["PidgeottoMirrorMove_AfterDamage"] = {"compare": ("a", "hl", "d", "e"), "preserve": ("d", "e")}
CASES["PidgeottoMirrorMove_AfterDamage"] = [
    {"d": 0x01, "e": 0x0E, "wram": {wNoDamageOrEffect: b"\x01"}},
    dict(POISON, d=0x01, e=0x0E, wram={wNoDamageOrEffect: b"\x01"}),
]
# <<< factory PidgeottoMirrorMove_AfterDamage

# >>> factory SpearowMirrorMove_AfterDamage
CONTRACT["SpearowMirrorMove_AfterDamage"] = {"compare": ("a", "hl", "d", "e"), "preserve": ("d", "e")}
CASES["SpearowMirrorMove_AfterDamage"] = [
    {"d": 0x01, "e": 0x0E, "wram": {wNoDamageOrEffect: b"\x01"}},
    dict(POISON, d=0x01, e=0x0E, wram={wNoDamageOrEffect: b"\x01"}),
]
# <<< factory SpearowMirrorMove_AfterDamage

# >>> factory Func_2c0a8
CONTRACT["Func_2c0a8"] = {"compare": ("a",), "preserve": ()}
CASES["Func_2c0a8"] = [
    {"keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x99", 0xC3F1: b"\x00",
              0xC2BA: b"\x3C", 0xCAC2: b"\x09",
              0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
     "read": {hTemp_ffa0: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x99", 0xC3F1: b"\x00",
               0xC2BA: b"\x3C", 0xCAC2: b"\x09",
               0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
         read={hTemp_ffa0: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory Func_2c0a8

# >>> factory ShuffleCardsInDeck
CONTRACT["ShuffleCardsInDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ShuffleCardsInDeck"] = [
    {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0, "keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {wDuelType: b"\x00", hWhoseTurn: b"\xC2", 0xC2BA: b"\x3B", 0xCAC2: b"\x09",
              0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={wDuelType: b"\x00", hWhoseTurn: b"\xC2", 0xC2BA: b"\x3B", 0xCAC2: b"\x09",
               0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory ShuffleCardsInDeck

# >>> factory DrawPlayAreaScreenToShowChanges
CONTRACT["DrawPlayAreaScreenToShowChanges"] = {"compare": (), "preserve": ()}
CASES["DrawPlayAreaScreenToShowChanges"] = [
    {"a": 0x12, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "hram": {0xFF9D: b"\x00"},
     "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08",
              0xC2BB + 0xC8: b"\x00", 0xC2BB + 0xCE: b"\x00",
              0xC2BB + 0xF0: b"\x00", 0xC2BB + 0xF2: b"\x00",
              0xCBD2: b"\x00"},
     "expect": {0xFF9D: b"\x12"}, "read": {0xFF9D: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, a=0xAA, keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         hram={0xFF9D: b"\x00"},
         wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08",
               0xC2BB + 0xC8: b"\x00", 0xC2BB + 0xCE: b"\x00",
               0xC2BB + 0xF0: b"\x00", 0xC2BB + 0xF2: b"\x00",
               0xCBD2: b"\x00"},
         expect={0xFF9D: b"\xAA"}, read={0xFF9D: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawPlayAreaScreenToShowChanges

# >>> factory EnergyRemoval_DiscardEffect
CONTRACT["EnergyRemoval_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["EnergyRemoval_DiscardEffect"] = [
    {"wram": {0xFFA1: b"\x00", 0xFFA0: b"\x00"}},
    dict(POISON, wram={0xFFA1: b"\x00", 0xFFA0: b"\x00"}),
]
# <<< factory EnergyRemoval_DiscardEffect

# >>> factory SuperEnergyRemoval_DiscardEffect
CONTRACT["SuperEnergyRemoval_DiscardEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SuperEnergyRemoval_DiscardEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xFFA1: b"\x05", 0xFFA3: b"\x06\xFF",
              0xC2F1: b"\x00", 0xC2ED: b"\x00", 0xC3ED: b"\x00"},
     "expect": {0xC205: b"\x02", 0xC27D: b"\x05", 0xC306: b"\x02",
                 0xC37D: b"\x06", 0xC2ED: b"\x01", 0xC3ED: b"\x01"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFFA1: b"\x05", 0xFFA3: b"\x06\xFF",
                       0xC2F1: b"\x00", 0xC2ED: b"\x00", 0xC3ED: b"\x00"},
         expect={0xC205: b"\x02", 0xC27D: b"\x05", 0xC306: b"\x02",
                 0xC37D: b"\x06", 0xC2ED: b"\x01", 0xC3ED: b"\x01"}),
]
# <<< factory SuperEnergyRemoval_DiscardEffect

# >>> factory EnergyTrans_AIEffect
CONTRACT["EnergyTrans_AIEffect"] = {"compare": (), "preserve": ()}
CASES["EnergyTrans_AIEffect"] = [
    {"hram": {hAIEnergyTransEnergyCard: b"\x05", hAIEnergyTransPlayAreaLocation: b"\x02"},
     "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC205: b"\x00", 0xC2EE: b"\x00",
              0xC242: b"\x00", 0xC400: b"\x08", 0xC2BB + 0xC8: b"\x00",
              0xC2BB + 0xCE: b"\x00", 0xC2BB + 0xF0: b"\x00",
              0xC2BB + 0xF2: b"\x00", 0xCBD2: b"\x00"},
     "expect": {0xC205: b"\x12", 0xC242: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hram={hAIEnergyTransEnergyCard: b"\x05", hAIEnergyTransPlayAreaLocation: b"\x02"},
         keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         wram={0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC205: b"\x00", 0xC2EE: b"\x00",
               0xC242: b"\x00", 0xC400: b"\x08", 0xC2BB + 0xC8: b"\x00",
               0xC2BB + 0xCE: b"\x00", 0xC2BB + 0xF0: b"\x00",
               0xC2BB + 0xF2: b"\x00", 0xCBD2: b"\x00"},
         expect={0xC205: b"\x12", 0xC242: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory EnergyTrans_AIEffect

# >>> factory StrangeBehavior_SwapEffect
CONTRACT["StrangeBehavior_SwapEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["StrangeBehavior_SwapEffect"] = [
    {"wram": {0xFF97: b"\xC1", 0xFFA0: b"\x00", 0xFFA1: b"\x00", 0xFFA2: b"\x00", 0xC1C8: b"\x0A", 0xC1EF: b"\x00"},
     "sram": {0: {}}, "setup": [{"fn": "SetupText", "d": 0x38, "e": 0x9F}],
     "read": {0xC1C8: 1}, "instruction_budget": 12000000, "cycle_budget": 48000000},
    dict(POISON, wram={0xFF97: b"\xC1", 0xFFA0: b"\x00", 0xFFA1: b"\x00", 0xFFA2: b"\x00", 0xC1C8: b"\x0A", 0xC1EF: b"\x00"},
         sram={0: {}}, setup=[{"fn": "SetupText", "d": 0x38, "e": 0x9F}], read={0xC1C8: 1},
         instruction_budget=12000000, cycle_budget=48000000),
]
# <<< factory StrangeBehavior_SwapEffect

# >>> factory Defender_AttachDefenderEffect
CONTRACT["Defender_AttachDefenderEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Defender_AttachDefenderEffect"] = [
    {"a": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": {hWhoseTurn: b"\xC2", hTempCardIndex_ff9f: b"\x01", hTemp_ffa0: b"\x00", 0xC2DA: b"\x00", 0xC201: b"\x00", 0xC2F1: b"\x00"}, "expect": {0xC2DA: b"\x01"}, "read": {0xC2DA: 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempCardIndex_ff9f: b"\x01", hTemp_ffa0: b"\x00", 0xC2DA: b"\x00", 0xC201: b"\x00", 0xC2F1: b"\x00"}, expect={0xC2DA: b"\x01"}, read={0xC2DA: 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Defender_AttachDefenderEffect

# >>> factory DamageSwap_SwapEffect
CONTRACT["DamageSwap_SwapEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["DamageSwap_SwapEffect"] = [
    {"wram": {0xFF97: b"\xC1", 0xFFA0: b"\x00", 0xFFA1: b"\x00", 0xFFA2: b"\x00", 0xC1C8: b"\x0A", 0xC1EF: b"\x00"},
     "sram": {0: {}}, "setup": [{"fn": "SetupText", "d": 0x38, "e": 0x9F}],
     "read": {0xC1C8: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC1", 0xFFA0: b"\x00", 0xFFA1: b"\x00", 0xFFA2: b"\x00", 0xC1C8: b"\x0A", 0xC1EF: b"\x00"},
         sram={0: {}}, setup=[{"fn": "SetupText", "d": 0x38, "e": 0x9F}], read={0xC1C8: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DamageSwap_SwapEffect

# >>> factory PrintDevolvedCardNameAndLevelText
CONTRACT["PrintDevolvedCardNameAndLevelText"] = {"compare": (), "preserve": ()}
CASES["PrintDevolvedCardNameAndLevelText"] = [
    {"b": 0x11, "c": 0x22, "d": 0x00, "e": 0x01, "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "wram": {0xFF97: b"\x00", 0xC400: b"\x08\x09", 0xC590: b"\x00", 0xCE3F: b"\x00\x00\x00\x00"},
     "read": {0xCC27: 2, 0xCE3F: 4}},
    dict(POISON, keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         wram={0xFF97: b"\x00", 0xC400: b"\x08\x09", 0xC590: b"\x00", 0xCE3F: b"\x00\x00\x00\x00"},
         read={0xCC27: 2, 0xCE3F: 4}),
]
# <<< factory PrintDevolvedCardNameAndLevelText

# >>> factory ApplySubstatus2ToDefendingCard
CONTRACT["ApplySubstatus2ToDefendingCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["ApplySubstatus2ToDefendingCard"] = [
    {"a": 0x01, "hl": 0xC200, "wram": {hWhoseTurn: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"a": 0x7F, "hl": 0xC240, "wram": {hWhoseTurn: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, a=0xA5, hl=0xC280, wram={hWhoseTurn: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),
]
# <<< factory ApplySubstatus2ToDefendingCard

# >>> factory ApplyAmnesiaToAttack
CONTRACT["ApplyAmnesiaToAttack"] = {"compare": (), "preserve": ()}
CASES["ApplyAmnesiaToAttack"] = [
    {"a": 0x01, "f": 0x00, "b": 0x02, "c": 0x03, "d": 0x04, "e": 0x05, "hl": 0x0000, "wram": {hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x00", 0xC3F6: b"\x00", 0xC3F2: b"\x00", 0xC3F8: b"\x00", hTemp_ffa0: b"\x02"}, "read": {0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}},
    dict(POISON, hl=0x0000, wram={hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x11", 0xC3F6: b"\x22", 0xC3F2: b"\x33", 0xC3F8: b"\x44", hTemp_ffa0: b"\x03"}, read={0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}),
]
# <<< factory ApplyAmnesiaToAttack

# >>> factory MirrorMove_BeforeDamage
CONTRACT["MirrorMove_BeforeDamage"] = {"compare": (), "preserve": ()}
CASES["MirrorMove_BeforeDamage"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F3: b"\x00\x00\x00\x00", 0xC3E8: b"\x00"},
     "read": {wDamage: 2, 0xCCB8: 1, 0xC3E8: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F3: b"\x34\x12\x00\x00", 0xC3E8: b"\x00"},
     "read": {wDamage: 2, 0xCCB8: 1, 0xC3E8: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2F3: b"\x34\x12\x00\x00", 0xC3E8: b"\x00"},
         read={wDamage: 2, 0xCCB8: 1, 0xC3E8: 1}),
]
# <<< factory MirrorMove_BeforeDamage

# >>> factory SpearowMirrorMove_BeforeDamage
CONTRACT["SpearowMirrorMove_BeforeDamage"] = {"compare": (), "preserve": ()}
CASES["SpearowMirrorMove_BeforeDamage"] = [
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x00\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x11", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x01", TURN_DAMAGE: b"\x12\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x22", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x01\x02", TURN_STATUS: b"\x10", TURN_SUBSTATUS2: b"\x33", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x34\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x44", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}}
]
# <<< factory SpearowMirrorMove_BeforeDamage

# >>> factory PidgeottoMirrorMove_BeforeDamage
CONTRACT["PidgeottoMirrorMove_BeforeDamage"] = {"compare": (), "preserve": ()}
CASES["PidgeottoMirrorMove_BeforeDamage"] = [
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x00\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x11", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x01", TURN_DAMAGE: b"\x12\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x22", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x01\x02", TURN_STATUS: b"\x10", TURN_SUBSTATUS2: b"\x33", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}},
    {"wram": {hWhoseTurn: b"\xC2", TURN_EFFECT: b"\x00", TURN_DAMAGE: b"\x34\x00", TURN_STATUS: b"\x00", TURN_SUBSTATUS2: b"\x44", NON_TURN_STATUS: b"\x00", NON_TURN_SUBSTATUS2: b"\x00", wDamage: b"\x00\x00", wLoadedAttackAnimation: b"\x00"}, "read": {wDamage: 2, wLoadedAttackAnimation: 1, NON_TURN_SUBSTATUS2: 1}}
]
# <<< factory PidgeottoMirrorMove_BeforeDamage

# >>> factory PoliwhirlAmnesia_DisableEffect
CONTRACT["PoliwhirlAmnesia_DisableEffect"] = {"compare": (), "preserve": ()}
CASES["PoliwhirlAmnesia_DisableEffect"] = [
    {"a": 0x01, "f": 0x00, "b": 0x02, "c": 0x03, "d": 0x04, "e": 0x05, "hl": 0x0000, "wram": {hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x00", 0xC3F6: b"\x00", 0xC3F2: b"\x00", 0xC3F8: b"\x00", hTemp_ffa0: b"\x02"}, "read": {0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}},
    dict(POISON, hl=0x0000, wram={hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x11", 0xC3F6: b"\x22", 0xC3F2: b"\x33", 0xC3F8: b"\x44", hTemp_ffa0: b"\x03"}, read={0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}),
]
# <<< factory PoliwhirlAmnesia_DisableEffect

# >>> factory SlowpokeAmnesia_DisableEffect
CONTRACT["SlowpokeAmnesia_DisableEffect"] = {"compare": (), "preserve": ()}
CASES["SlowpokeAmnesia_DisableEffect"] = [
    {"a": 0x01, "f": 0x00, "b": 0x02, "c": 0x03, "d": 0x04, "e": 0x05, "hl": 0x0000, "wram": {hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x00", 0xC3F6: b"\x00", 0xC3F2: b"\x00", 0xC3F8: b"\x00", hTemp_ffa0: b"\x02"}, "read": {0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}},
    dict(POISON, hl=0x0000, wram={hWhoseTurn: b"\xC2", wNoDamageOrEffect: b"\x00", 0xC3E8: b"\x11", 0xC3F6: b"\x22", 0xC3F2: b"\x33", 0xC3F8: b"\x44", hTemp_ffa0: b"\x03"}, read={0xC3E8: 1, 0xC3F6: 1, 0xC3F2: 1, 0xC3F8: 1}),
]
# <<< factory SlowpokeAmnesia_DisableEffect

# >>> factory HorseaSmokescreenEffect
CONTRACT["HorseaSmokescreenEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["HorseaSmokescreenEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, hl=0xC280, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),
]
# <<< factory HorseaSmokescreenEffect

# >>> factory PikachuAltLv16GrowlEffect
CONTRACT["PikachuAltLv16GrowlEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["PikachuAltLv16GrowlEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, hl=0xC280, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),
]
# <<< factory PikachuAltLv16GrowlEffect

# >>> factory MagmarSmokescreenEffect
CONTRACT["MagmarSmokescreenEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["MagmarSmokescreenEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, hl=0xC280, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),
]
# <<< factory MagmarSmokescreenEffect

# >>> factory PikachuLv16GrowlEffect
CONTRACT["PikachuLv16GrowlEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["PikachuLv16GrowlEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, hl=0xC280, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),
]
# <<< factory PikachuLv16GrowlEffect

# >>> factory PounceEffect
CONTRACT["PounceEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["PounceEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),]
# <<< factory PounceEffect

# >>> factory SandAttackEffect
CONTRACT["SandAttackEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["SandAttackEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, hl=0xC280, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),]
# <<< factory SandAttackEffect

# >>> factory SnivelEffect
CONTRACT["SnivelEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["SnivelEffect"] = [
    {"hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xC3E8: b"\x00", 0xC3F6: b"\x00"}, "read": {0xC3E8: 1, 0xC3F6: 1}},
    {"hl": 0xC240, "wram": {0xFF97: b"\xC3", 0xC2E8: b"\x12", 0xC2F6: b"\x34"}, "read": {0xC2E8: 1, 0xC2F6: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3E8: b"\x55", 0xC3F6: b"\x66"}, read={0xC3E8: 1, 0xC3F6: 1}),]
# <<< factory SnivelEffect

# >>> factory Conversion1_ChangeWeaknessEffect
CONTRACT["Conversion1_ChangeWeaknessEffect"] = {"compare": ("hl",), "preserve": ()}
CASES["Conversion1_ChangeWeaknessEffect"] = [
    {"d": 0x01, "e": 0x0E, "hl": 0x0000, "wram": {0xCCC7: b"\x80"}, "read": {0xCCC7: 1}},
    {"d": 0x01, "e": 0x0E, "hl": 0xC200, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC3BB: b"\x00", 0xC3E9: b"\x00", 0xC400: b"\x08", 0xC590: b"\x00", 0xFFA0: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC3E9: 1, 0xC3F7: 1}},
    dict(POISON, d=0x01, e=0x0E, hl=0xC240, wram={0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC3BB: b"\x00", 0xC3E9: b"\x55", 0xC400: b"\x08", 0xC590: b"\x00", 0xFFA0: b"\x02"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC3E9: 1, 0xC3F7: 1}),
]
# <<< factory Conversion1_ChangeWeaknessEffect

# >>> factory EnergyRetrieval_DiscardAndAddToHandEffect
CONTRACT["EnergyRetrieval_DiscardAndAddToHandEffect"] = {"compare": (), "preserve": ()}
CASES["EnergyRetrieval_DiscardAndAddToHandEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempList: b"\x03\x03\xFF", player_duel_page: b"\x00", card_location: b"\x01", hand_count: b"\x01", discard_count: b"\x00", duelist_type: b"\x00", hand_card: b"\x03", discard_card: b"\x00", wDuelTempList: b"\x00\x00\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", hTempList: b"\x03\x03\x04\xFF", player_duel_page: b"\x00", card_location: b"\x01", hand_count: b"\x01", discard_count: b"\x00", duelist_type: b"\x00", hand_card: b"\x03", discard_card: b"\x00", wDuelTempList: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempList: b"\x03\x03\xFF", player_duel_page: b"\x00", card_location: b"\x01", hand_count: b"\x01", discard_count: b"\x00", duelist_type: b"\x00", hand_card: b"\x03", discard_card: b"\x00", wDuelTempList: b"\x00\x00\x00"}),
]
# <<< factory EnergyRetrieval_DiscardAndAddToHandEffect

# >>> factory SuperEnergyRetrieval_DiscardAndAddToHandEffect
CONTRACT["SuperEnergyRetrieval_DiscardAndAddToHandEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["SuperEnergyRetrieval_DiscardAndAddToHandEffect"] = [
    {"b": 0x12, "c": 0x34, "wram": {hTemp_ffa0: b"\x03\x04\x03\x04\xFF", hWhoseTurn: b"\xC2", wDuelistType: b"\x00", 0xC2EE: b"\x02", 0xC2ED: b"\x00", 0xC203: b"\x01", 0xC204: b"\x01", 0xC242: b"\x03\x04"}, "read": {wDuelTempList: 3}},
    {"b": 0x56, "c": 0x78, "wram": {hTemp_ffa0: b"\x05\x06\x05\x06\xFF", hWhoseTurn: b"\xC2", wDuelistType: b"\x00", 0xC2EE: b"\x02", 0xC2ED: b"\x00", 0xC205: b"\x01", 0xC206: b"\x01", 0xC244: b"\x05\x06"}, "read": {wDuelTempList: 3}},
    dict(POISON, wram={hTemp_ffa0: b"\x03\x04\x03\x04\xFF", hWhoseTurn: b"\xC2", wDuelistType: b"\x00", 0xC2EE: b"\x02", 0xC2ED: b"\x00", 0xC203: b"\x01", 0xC204: b"\x01", 0xC242: b"\x03\x04"}, read={wDuelTempList: 3}),
]
# <<< factory SuperEnergyRetrieval_DiscardAndAddToHandEffect

# >>> factory HandleDefendingPokemonAttackSelection
CONTRACT["HandleDefendingPokemonAttackSelection"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["HandleDefendingPokemonAttackSelection"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x07", wPlayerDuelistType: b"\x00", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": 0x02, "read": {hCurSelectionItem: 1, wDuelTempList: 4}, "instruction_budget": 1000000, "cycle_budget": 10000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x07", wPlayerDuelistType: b"\x00", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=0x02, read={hCurSelectionItem: 1, wDuelTempList: 4}, instruction_budget=1000000, cycle_budget=10000000),
]
# <<< factory HandleDefendingPokemonAttackSelection

# >>> factory HandleEnergyDiscardEffectSelection
CONTRACT["HandleEnergyDiscardEffectSelection"] = {"compare": (), "preserve": ()}
CASES["HandleEnergyDiscardEffectSelection"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, "read": {hWhoseTurn: 1, hTemp_ffa0: 1}, "instruction_budget": 500000, "cycle_budget": 2000000},
    {"wram": {hWhoseTurn: b"\xC3", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, "read": {hWhoseTurn: 1, hTemp_ffa0: 1}, "instruction_budget": 500000, "cycle_budget": 2000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x55", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, read={hWhoseTurn: 1, hTemp_ffa0: 1}, instruction_budget=500000, cycle_budget=2000000),
]
# <<< factory HandleEnergyDiscardEffectSelection

# >>> factory DragonairHyperBeam_PlayerSelectEffect
CONTRACT["DragonairHyperBeam_PlayerSelectEffect"] = {"compare": (), "preserve": ()}
CASES["DragonairHyperBeam_PlayerSelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, "read": {0xFF97: 1, 0xFFA0: 1}, "instruction_budget": 500000, "cycle_budget": 2000000},
    {"wram": {0xFF97: b"\xC3", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, "read": {0xFF97: 1, 0xFFA0: 1}, "instruction_budget": 500000, "cycle_budget": 2000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFFA0: b"\x55", 0xC200: b"\x00" * 0x3C, 0xC300: b"\x00" * 0x3C}, read={0xFF97: 1, 0xFFA0: 1}, instruction_budget=500000, cycle_budget=2000000),
]
# <<< factory DragonairHyperBeam_PlayerSelectEffect

# >>> factory GolduckHyperBeam_PlayerSelectEffect
CONTRACT["GolduckHyperBeam_PlayerSelectEffect"] = {"compare": (), "preserve": ()}
CASES["GolduckHyperBeam_PlayerSelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC300: b"\x00" * 60, 0xCABB: b"\x00", hTempCardIndex_ff98: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC300: b"\x00" * 60, 0xCABB: b"\x00", hTempCardIndex_ff98: b"\x00"}, read={0xFFA0: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory GolduckHyperBeam_PlayerSelectEffect

# >>> factory MirrorMove_PlayerSelection
CONTRACT["MirrorMove_PlayerSelection"] = {"compare": (), "preserve": ()}
CASES["MirrorMove_PlayerSelection"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, read={0xFFA0: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory MirrorMove_PlayerSelection

# >>> factory SpearowMirrorMove_PlayerSelection
CONTRACT["SpearowMirrorMove_PlayerSelection"] = {"compare": (), "preserve": ()}
CASES["SpearowMirrorMove_PlayerSelection"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x00", 0xFFA0: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, read={0xFFA0: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory SpearowMirrorMove_PlayerSelection

# >>> factory StrangeBehavior_SelectAndSwapEffect
CONTRACT["StrangeBehavior_SelectAndSwapEffect"] = {"compare": (), "preserve": ()}
CASES["StrangeBehavior_SelectAndSwapEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01", wExcludeArenaPokemon: b"\x00", 0xC2F1: b"\x01"}, "read": {0xCBC8: 1}, "instruction_budget": 6000000, "cycle_budget": 20000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01", wExcludeArenaPokemon: b"\x00", 0xC2F1: b"\x01"}, read={0xCBC8: 1}, instruction_budget=6000000, cycle_budget=20000000),
]
# <<< factory StrangeBehavior_SelectAndSwapEffect

# >>> factory PidgeottoMirrorMove_PlayerSelection
CONTRACT["PidgeottoMirrorMove_PlayerSelection"] = {"compare": (), "preserve": ()}
CASES["PidgeottoMirrorMove_PlayerSelection"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x01", 0xC300: b"\x00" * 60, 0xFFA0: b"\x00", 0xCABB: b"\x00"}, read={0xFFA0: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory PidgeottoMirrorMove_PlayerSelection

# >>> factory LookForCardsInDeck
CONTRACT["LookForCardsInDeck"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardsInDeck"] = [
    {"a": 0x01, "d": 0x00, "e": 0x12, "hl": 0x1234, "wram": {0xC510: b"\xff", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={0xC510: b"\xff", 0xCABB: b"\x80", 0xFF40: b"\x80"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000),
    {"a": 0x00, "d": 0x04, "e": 0x00, "hl": 0x0000, "wram": {0xC510: b"\xff", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000}
]
# <<< factory LookForCardsInDeck

# >>> factory KadabraRecover_PlayerSelectEffect
CONTRACT["KadabraRecover_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["KadabraRecover_PlayerSelectEffect"] = [
    # B cancels: `ret c` fires and hTemp_ffa0 is left alone.
    {"keys": [0x00, 0x02],
     "wram": {hWhoseTurn: bytes((KR_PLAYER_TURN,)), KR_wConsole: b"\x00", KR_wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + KR_ARENA_HP: b"\x00",
      wPlayerArenaCard + KR_ARENA_STAGE: b"\x00",
      wPlayerArenaCard + KR_ARENA_STATUS: b"\x00",
      wPlayerArenaCard + KR_ARENA_PLUSPOWER: b"\x00",
      wPlayerArenaCard + KR_ARENA_DEFENDER: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    # A accepts: the tail copies hTempCardIndex_ff98 into hTemp_ffa0.
    {"keys": [0x00, 0x01],
     "wram": {hWhoseTurn: bytes((KR_PLAYER_TURN,)), KR_wConsole: b"\x00", KR_wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + KR_ARENA_HP: b"\x00",
      wPlayerArenaCard + KR_ARENA_STAGE: b"\x00",
      wPlayerArenaCard + KR_ARENA_STATUS: b"\x00",
      wPlayerArenaCard + KR_ARENA_PLUSPOWER: b"\x00",
      wPlayerArenaCard + KR_ARENA_DEFENDER: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={hWhoseTurn: bytes((KR_PLAYER_TURN,)), KR_wConsole: b"\x00", KR_wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + KR_ARENA_HP: b"\x00",
      wPlayerArenaCard + KR_ARENA_STAGE: b"\x00",
      wPlayerArenaCard + KR_ARENA_STATUS: b"\x00",
      wPlayerArenaCard + KR_ARENA_PLUSPOWER: b"\x00",
      wPlayerArenaCard + KR_ARENA_DEFENDER: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory KadabraRecover_PlayerSelectEffect

# >>> factory Scavenge_PlayerSelectEnergyEffect
CONTRACT["Scavenge_PlayerSelectEnergyEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Scavenge_PlayerSelectEnergyEffect"] = [
    {"keys": [0x00, 0x02],
     "wram": {hWhoseTurn: bytes((Scaven_TURN,)), Scaven_CONSOLE: b"\x00", Scaven_LCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + Scaven_HP: b"\x00",
      wPlayerArenaCard + Scaven_STAGE: b"\x00",
      wPlayerArenaCard + Scaven_STATUS: b"\x00",
      wPlayerArenaCard + Scaven_PLUS: b"\x00",
      wPlayerArenaCard + Scaven_DEF: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    {"keys": [0x00, 0x01],
     "wram": {hWhoseTurn: bytes((Scaven_TURN,)), Scaven_CONSOLE: b"\x00", Scaven_LCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + Scaven_HP: b"\x00",
      wPlayerArenaCard + Scaven_STAGE: b"\x00",
      wPlayerArenaCard + Scaven_STATUS: b"\x00",
      wPlayerArenaCard + Scaven_PLUS: b"\x00",
      wPlayerArenaCard + Scaven_DEF: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={hWhoseTurn: bytes((Scaven_TURN,)), Scaven_CONSOLE: b"\x00", Scaven_LCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + Scaven_HP: b"\x00",
      wPlayerArenaCard + Scaven_STAGE: b"\x00",
      wPlayerArenaCard + Scaven_STATUS: b"\x00",
      wPlayerArenaCard + Scaven_PLUS: b"\x00",
      wPlayerArenaCard + Scaven_DEF: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory Scavenge_PlayerSelectEnergyEffect

# >>> factory PlayerPickFireEnergyCardToDiscard
CONTRACT["PlayerPickFireEnergyCardToDiscard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PlayerPickFireEnergyCardToDiscard"] = [
    {"keys": [0x00, 0x02],
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02],
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory PlayerPickFireEnergyCardToDiscard

# >>> factory ArcanineFlamethrower_PlayerSelectEffect
CONTRACT["ArcanineFlamethrower_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ArcanineFlamethrower_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory ArcanineFlamethrower_PlayerSelectEffect

# >>> factory CharmeleonFlamethrower_PlayerSelectEffect
CONTRACT["CharmeleonFlamethrower_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CharmeleonFlamethrower_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory CharmeleonFlamethrower_PlayerSelectEffect

# >>> factory Barrier_PlayerSelectEffect
CONTRACT["Barrier_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Barrier_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFF98: 1, 0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFF98: 1, 0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Barrier_PlayerSelectEffect

# >>> factory StarmieRecover_PlayerSelectEffect
CONTRACT["StarmieRecover_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["StarmieRecover_PlayerSelectEffect"] = [
    # Only an accept leaves .loop_input, so A is the terminating input.
    {"keys": [0x00, 0x01],
     "wram": {hWhoseTurn: bytes((SR_TURN,)), SR_CONSOLE: b"\x00", SR_LCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + SR_HP: b"\x00",
      wPlayerArenaCard + SR_STAGE: b"\x00",
      wPlayerArenaCard + SR_STATUS: b"\x00",
      wPlayerArenaCard + SR_PLUS: b"\x00",
      wPlayerArenaCard + SR_DEF: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={hWhoseTurn: bytes((SR_TURN,)), SR_CONSOLE: b"\x00", SR_LCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + SR_HP: b"\x00",
      wPlayerArenaCard + SR_STAGE: b"\x00",
      wPlayerArenaCard + SR_STATUS: b"\x00",
      wPlayerArenaCard + SR_PLUS: b"\x00",
      wPlayerArenaCard + SR_DEF: b"\x00",
      wDuelTempList: b"\xFF",
      hTempCardIndex_ff98: b"\x05", hTemp_ffa0: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory StarmieRecover_PlayerSelectEffect

# >>> factory DestinyBond_PlayerSelectEffect
CONTRACT["DestinyBond_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DestinyBond_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFF98: 1, 0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFF98: 1, 0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DestinyBond_PlayerSelectEffect

# >>> factory FlamesOfRage_PlayerSelectEffect
CONTRACT["FlamesOfRage_PlayerSelectEffect"] = {"compare": (), "preserve": ()}
CASES["FlamesOfRage_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xFF98: 1, 0xFFB2: 1, 0xCBE0: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xFF98: 1, 0xFFB2: 1, 0xCBE0: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FlamesOfRage_PlayerSelectEffect

# >>> factory HandleColorChangeScreen
CONTRACT["HandleColorChangeScreen"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["HandleColorChangeScreen"] = [
    {"a": 0x01, "f": 0x00, "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": FRAME_SETUP, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000, "read": {0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}},
    dict(POISON, a=0x00, wram={0xCABB: b"\x80", 0xFF40: b"\x80"}, setup=FRAME_SETUP, keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000, read={0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}),
]
# <<< factory HandleColorChangeScreen

# >>> factory Ember_PlayerSelectEffect
CONTRACT["Ember_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Ember_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory Ember_PlayerSelectEffect

# >>> factory FireBlast_PlayerSelectEffect
CONTRACT["FireBlast_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["FireBlast_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory FireBlast_PlayerSelectEffect

# >>> factory MagmarFlamethrower_PlayerSelectEffect
CONTRACT["MagmarFlamethrower_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["MagmarFlamethrower_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory MagmarFlamethrower_PlayerSelectEffect

# >>> factory FlareonFlamethrower_PlayerSelectEffect
CONTRACT["FlareonFlamethrower_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["FlareonFlamethrower_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "rom_bank": 1,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {hTemp_ffa0: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x02], rom_bank=1,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wLCDC: b"\x00",
      wPlayerArenaCard: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
      wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
      wDuelTempList: b"\xFF",
      wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07",
      hTempCardIndex_ff98: b"\x05"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={hTemp_ffa0: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory FlareonFlamethrower_PlayerSelectEffect

# >>> factory Conversion1_PlayerSelectEffect
CONTRACT["Conversion1_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Conversion1_PlayerSelectEffect"] = [
    {"wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": FRAME_SETUP,
     "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000,
     "read": {hTemp_ffa0: 1, 0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}},
    dict(POISON, wram={0xCABB: b"\x80", 0xFF40: b"\x80"}, setup=FRAME_SETUP,
         keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000,
         read={hTemp_ffa0: 1, 0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}),
]
# <<< factory Conversion1_PlayerSelectEffect

# >>> factory Conversion2_PlayerSelectEffect
CONTRACT["Conversion2_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["Conversion2_PlayerSelectEffect"] = [
    {"wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": FRAME_SETUP,
     "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000,
     "read": {0xFFA0: 1, 0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}},
    dict(POISON, wram={0xCABB: b"\x80", 0xFF40: b"\x80"}, setup=FRAME_SETUP,
         keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000,
         read={0xFFA0: 1, 0xCCEB: 1, 0xCE3F: 1, 0xCE41: 1}),
]
# <<< factory Conversion2_PlayerSelectEffect

# >>> factory AskWhetherToQuitSelectingCards
CONTRACT["AskWhetherToQuitSelectingCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AskWhetherToQuitSelectingCards"] = [
	{"a": 0x03, "wram": {0xFFB2: b"\x00", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {0xCE43: 2}},
	{"a": 0x05, "wram": {0xFFB2: b"\x02", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {0xCE43: 2}},
	dict(POISON, a=0x07, wram={0xFFB2: b"\x01", 0xCABB: b"\x00", 0xC510: b"\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=80000000, read={0xCE43: 2}),
]
# <<< factory AskWhetherToQuitSelectingCards

# >>> factory Scavenge_AddToHandEffect
CONTRACT["Scavenge_AddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Scavenge_AddToHandEffect"] = [
    # Player's own turn: IsPlayerTurn sets carry and `ret c` returns before the
    # detail screen, so no frame/input machinery is reachable here.
    {"wram": {SAH_hWhoseTurn: bytes((SAH_TURN,)), SAH_DUELIST_TYPE: b"\x00",
      SAH_HAND_COUNT: b"\x00", SAH_HAND: b"\xFF\xFF",
      SAH_hTempPlayAreaLocation_ffa1: b"\x00"},
     "read": {SAH_HAND_COUNT: 1, SAH_HAND: 2}},
    # Opponent's turn: the screen runs, so real frames and a cycled A are needed.
    {"keys": [0x00, 0x01],
     "wram": {SAH_wLCDC: b"\x80", SAH_rLCDC: b"\x80",
      SAH_hWhoseTurn: bytes((SAH_TURN,)), SAH_DUELIST_TYPE: b"\x01",
      SAH_HAND_COUNT: b"\x00", SAH_HAND: b"\xFF\xFF",
      SAH_wPlayerDeck: b"\x10", SAH_wLoadedCard1: b"\x00",
      SAH_hTempPlayAreaLocation_ffa1: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {SAH_HAND_COUNT: 1, SAH_HAND: 2, SAH_wLoadedCard1: 64},
     "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={SAH_wLCDC: b"\x80", SAH_rLCDC: b"\x80",
         SAH_hWhoseTurn: bytes((SAH_TURN,)), SAH_DUELIST_TYPE: b"\x01",
         SAH_HAND_COUNT: b"\x00", SAH_HAND: b"\xFF\xFF",
         SAH_wPlayerDeck: b"\x10", SAH_wLoadedCard1: b"\x00",
         SAH_hTempPlayAreaLocation_ffa1: b"\x00"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={SAH_HAND_COUNT: 1, SAH_HAND: 2, SAH_wLoadedCard1: 64},
         instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory Scavenge_AddToHandEffect

# >>> factory Recycle_AddToHandEffect
CONTRACT["Recycle_AddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Recycle_AddToHandEffect"] = [
    # No card selected: `cp $ff` / `ret z` leaves before any side effect.
    {"wram": {RAH_hTempList: b"\xFF"}, "read": {RAH_LOCATIONS: 4, RAH_DECK_CARDS: 4, RAH_NOT_IN_DECK: 1}},
    # Player's own turn: the card moves to hand and back onto the deck, then
    # `ret c` returns before the detail screen. The screen branch itself is
    # covered by DisplayCardDetailScreen's own cases.
    {"wram": {RAH_hWhoseTurn: bytes((RAH_TURN,)), RAH_DUELIST_TYPE: b"\x00",
      RAH_hTempList: b"\x00", RAH_NOT_IN_DECK: b"\x01"}, "read": {RAH_LOCATIONS: 4, RAH_DECK_CARDS: 4, RAH_NOT_IN_DECK: 1}},
    dict(POISON, wram={RAH_hWhoseTurn: bytes((RAH_TURN,)), RAH_DUELIST_TYPE: b"\x00",
         RAH_hTempList: b"\x00", RAH_NOT_IN_DECK: b"\x01"}, read={RAH_LOCATIONS: 4, RAH_DECK_CARDS: 4, RAH_NOT_IN_DECK: 1}),
]
# <<< factory Recycle_AddToHandEffect

# >>> factory PokemonBreeder_EvolveEffect
CONTRACT["PokemonBreeder_EvolveEffect"] = {"compare": ("a", "f", "c", "d", "e", "hl"), "preserve": ()}
# b is a callee clobber that no ported callee models, so it is not compared.
CASES["PokemonBreeder_EvolveEffect"] = [
    {"keys": [0x00, 0x01], "a": 0x12, "f": 0x00, "b": 0x34, "c": 0x56, "d": 0x78, "e": 0x9A, "hl": 0x4567, "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xFFA0: b"\x01", 0xFFA1: b"\x01", 0xC2F1: b"\x01", 0xCAC2: b"\x01"}, "read": {0xFF98: 1, 0xC2CF: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "a": 0xA5, "f": 0x80, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x89AB, "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xFFA0: b"\x01", 0xFFA1: b"\x01", 0xC2F1: b"\x01", 0xCAC2: b"\x01"}, "read": {0xFF98: 1, 0xC2CF: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xFFA0: b"\x01", 0xFFA1: b"\x01", 0xC2F1: b"\x01", 0xCAC2: b"\x01"}, read={0xFF98: 1, 0xC2CF: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory PokemonBreeder_EvolveEffect

# >>> factory Sprout_PutInPlayAreaEffect
CONTRACT["Sprout_PutInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Sprout_PutInPlayAreaEffect"] = [
    # hTemp_ffa0 defaults to 0, selecting the fetch-and-bench branch; the
    # player's own turn then makes `jr c` skip the detail screen (covered by
    # DisplayCardDetailScreen's own cases). SetupText seeds the glyph cache
    # the deck-shuffle animation walks.
    {"wram": {CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
      CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
         CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory Sprout_PutInPlayAreaEffect

# >>> factory NidoranFCallForFamily_PutInPlayAreaEffect
CONTRACT["NidoranFCallForFamily_PutInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["NidoranFCallForFamily_PutInPlayAreaEffect"] = [
    # hTemp_ffa0 defaults to 0, selecting the fetch-and-bench branch; the
    # player's own turn then makes `jr c` skip the detail screen (covered by
    # DisplayCardDetailScreen's own cases). SetupText seeds the glyph cache
    # the deck-shuffle animation walks.
    {"wram": {CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
      CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
         CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory NidoranFCallForFamily_PutInPlayAreaEffect

# >>> factory MarowakCallForFamily_PutInPlayAreaEffect
CONTRACT["MarowakCallForFamily_PutInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["MarowakCallForFamily_PutInPlayAreaEffect"] = [
    # hTemp_ffa0 defaults to 0, selecting the fetch-and-bench branch; the
    # player's own turn then makes `jr c` skip the detail screen (covered by
    # DisplayCardDetailScreen's own cases). SetupText seeds the glyph cache
    # the deck-shuffle animation walks.
    {"wram": {CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
      CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
         CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory MarowakCallForFamily_PutInPlayAreaEffect

# >>> factory KrabbyCallForFamily_PutInPlayAreaEffect
CONTRACT["KrabbyCallForFamily_PutInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["KrabbyCallForFamily_PutInPlayAreaEffect"] = [
    # hTemp_ffa0 defaults to 0, selecting the fetch-and-bench branch; the
    # player's own turn then makes `jr c` skip the detail screen (covered by
    # DisplayCardDetailScreen's own cases). SetupText seeds the glyph cache
    # the deck-shuffle animation walks.
    {"wram": {CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
      CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
         CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory KrabbyCallForFamily_PutInPlayAreaEffect

# >>> factory PokemonFlute_PlaceInPlayAreaText
CONTRACT["PokemonFlute_PlaceInPlayAreaText"] = {"compare": (), "preserve": ()}
CASES["PokemonFlute_PlaceInPlayAreaText"] = [
    {"wram": {CFF_hWhoseTurn: b"\xC2", CFF_DUELIST_TYPE: b"\x00", CFF_OTHER_DUELIST_TYPE: b"\x00", CFF_hTemp_ffa0: b"\x00", CFF_OTHER_LOCATIONS: b"\x02", CFF_OTHER_DECK_CARDS: b"\x00", CFF_OTHER_DISCARD_COUNT: b"\x01", CFF_OTHER_HAND_COUNT: b"\x00", CFF_OTHER_PLAY_COUNT: b"\x00", 0xFF40: b"\x00", CFF_LCD_SHADOW: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "read": {CFF_OTHER_LOCATIONS: 2, CFF_OTHER_DECK_CARDS: 2, CFF_OTHER_DISCARD_COUNT: 1, CFF_OTHER_HAND_COUNT: 1, CFF_OTHER_PLAY_COUNT: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, wram={CFF_hWhoseTurn: b"\xC2", CFF_DUELIST_TYPE: b"\x00", CFF_OTHER_DUELIST_TYPE: b"\x00", CFF_hTemp_ffa0: b"\x00", CFF_OTHER_LOCATIONS: b"\x02", CFF_OTHER_DECK_CARDS: b"\x00", CFF_OTHER_DISCARD_COUNT: b"\x01", CFF_OTHER_HAND_COUNT: b"\x00", CFF_OTHER_PLAY_COUNT: b"\x00", 0xFF40: b"\x00", CFF_LCD_SHADOW: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], read={CFF_OTHER_LOCATIONS: 2, CFF_OTHER_DECK_CARDS: 2, CFF_OTHER_DISCARD_COUNT: 1, CFF_OTHER_HAND_COUNT: 1, CFF_OTHER_PLAY_COUNT: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PokemonFlute_PlaceInPlayAreaText

# >>> factory Revive_PlaceInPlayAreaEffect
CONTRACT["Revive_PlaceInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Revive_PlaceInPlayAreaEffect"] = [
    # Player's own turn: the card is benched and its HP halved, then `ret c`
    # returns before the detail screen.
    {"wram": {RV_hWhoseTurn: bytes((RV_TURN,)), RV_DUELIST_TYPE: b"\x00",
      RV_hTemp_ffa0: b"\x01",
      RV_DECK_CARDS: bytes((RV_BULBASAUR,)),
      RV_LOCATIONS + 1: b"\x08",
      RV_NOT_IN_DECK: b"\x01", RV_NUM_IN_PLAY: b"\x00"}, "read": {RV_ARENA_HP: 8, RV_LOCATIONS: 4, RV_NUM_IN_PLAY: 1, RV_HAND_COUNT: 1}},
    dict(POISON, wram={RV_hWhoseTurn: bytes((RV_TURN,)), RV_DUELIST_TYPE: b"\x00",
         RV_hTemp_ffa0: b"\x01",
         RV_DECK_CARDS: bytes((RV_BULBASAUR,)),
         RV_LOCATIONS + 1: b"\x08",
         RV_NOT_IN_DECK: b"\x01", RV_NUM_IN_PLAY: b"\x00"}, read={RV_ARENA_HP: 8, RV_LOCATIONS: 4, RV_NUM_IN_PLAY: 1, RV_HAND_COUNT: 1}),
]
# <<< factory Revive_PlaceInPlayAreaEffect

# >>> factory ItemFinder_DiscardAddToHandEffect
CONTRACT["ItemFinder_DiscardAddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ItemFinder_DiscardAddToHandEffect"] = [
    # Player's own turn: both hand cards are discarded and the wanted card is
    # pulled back, then `ret c` returns before the detail screen (which
    # DisplayCardDetailScreen's own cases already cover).
    {"wram": {IF_hWhoseTurn: bytes((IF_TURN,)), IF_DUELIST_TYPE: b"\x00",
      IF_hTempList: b"\x01\x02\x03",
      IF_LOCATIONS + 1: b"\x01", IF_LOCATIONS + 2: b"\x01",
      IF_HAND_COUNT: b"\x02", IF_HAND: b"\x01\x02",
      IF_NOT_IN_DECK: b"\x03"}, "read": {IF_LOCATIONS: 6, IF_HAND_COUNT: 1, IF_HAND: 4, IF_NOT_IN_DECK: 1}},
    dict(POISON, wram={IF_hWhoseTurn: bytes((IF_TURN,)), IF_DUELIST_TYPE: b"\x00",
         IF_hTempList: b"\x01\x02\x03",
         IF_LOCATIONS + 1: b"\x01", IF_LOCATIONS + 2: b"\x01",
         IF_HAND_COUNT: b"\x02", IF_HAND: b"\x01\x02",
         IF_NOT_IN_DECK: b"\x03"}, read={IF_LOCATIONS: 6, IF_HAND_COUNT: 1, IF_HAND: 4, IF_NOT_IN_DECK: 1}),
]
# <<< factory ItemFinder_DiscardAddToHandEffect

# >>> factory BellsproutCallForFamily_PutInPlayAreaEffect
CONTRACT["BellsproutCallForFamily_PutInPlayAreaEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["BellsproutCallForFamily_PutInPlayAreaEffect"] = [
    # hTemp_ffa0 defaults to 0, selecting the fetch-and-bench branch; the
    # player's own turn then makes `jr c` skip the detail screen (covered by
    # DisplayCardDetailScreen's own cases). SetupText seeds the glyph cache
    # the deck-shuffle animation walks.
    {"wram": {CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
      CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={CFF_hWhoseTurn: bytes((CFF_TURN,)), CFF_DUELIST_TYPE: b"\x00",
         CFF_NOT_IN_DECK: b"\x01", CFF_wLCDC: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={CFF_LOCATIONS: 4, CFF_DECK_CARDS: 8, CFF_NOT_IN_DECK: 1, CFF_HAND_COUNT: 1, CFF_NUM_IN_PLAY: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory BellsproutCallForFamily_PutInPlayAreaEffect

# >>> factory Wildfire_PlayerSelectEffect
CONTRACT["Wildfire_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Wildfire_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wLCDC: b"\x00", wDuelTempList: b"\xFF"}, "read": {wEnergyDiscardPlayAreaLocation: 1, hTemp_ffa0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wLCDC: b"\x00", wDuelTempList: b"\xFF"}, "read": {wEnergyDiscardPlayAreaLocation: 1, hTemp_ffa0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory Wildfire_PlayerSelectEffect

# >>> factory Whirlpool_PlayerSelectEffect
CONTRACT["Whirlpool_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Whirlpool_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFF98: 1, 0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFF98: 1, 0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Whirlpool_PlayerSelectEffect

# >>> factory FireSpin_PlayerSelectEffect
CONTRACT["FireSpin_PlayerSelectEffect"] = {"compare": (), "preserve": ()}
CASES["FireSpin_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xFF98: 1, 0xFFB2: 1, 0xCBE0: 1, 0xCBFA: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xFF98: 1, 0xFFB2: 1, 0xCBE0: 1, 0xCBFA: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FireSpin_PlayerSelectEffect

# >>> factory EnergySpike_AttachEnergyEffect
CONTRACT["EnergySpike_AttachEnergyEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EnergySpike_AttachEnergyEffect"] = [
    {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0, "keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {hTemp_ffa0: b"\xFF", wDuelType: b"\x00", hWhoseTurn: b"\xC2", 0xC2BA: b"\x3B", 0xCAC2: b"\x09", 0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
     "read": {hTemp_ffa0: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={hTemp_ffa0: b"\xFF", wDuelType: b"\x00", hWhoseTurn: b"\xC2", 0xC2BA: b"\x3B", 0xCAC2: b"\x09", 0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
         read={hTemp_ffa0: 1}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory EnergySpike_AttachEnergyEffect

# >>> factory ScoopUp_ReturnToHandEffect
CONTRACT["ScoopUp_ReturnToHandEffect"] = {"compare": (), "preserve": ()}
CASES["ScoopUp_ReturnToHandEffect"] = [
    {"wram": {0xFFA0: b"\x00", 0xFFA1: b"\x01", 0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC200: b"\x10\x02\xFF\xFF\xFF\xFF\xFF", 0xC300: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\x01", 0xC400: b"\x01"}, "read": {0xFFA0: 1, 0xFFA1: 1, 0xFF98: 1, 0xC200: 7, 0xC2EF: 1}},
    {"wram": {0xFFA0: b"\x01", 0xFFA1: b"\x02", 0xFF97: b"\xC2", 0xC2EF: b"\x02", 0xC200: b"\x11\x10\xFF\xFF\xFF\xFF\xFF", 0xC300: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\x01", 0xC400: b"\x01"}, "read": {0xFFA0: 1, 0xFFA1: 1, 0xFF98: 1, 0xC200: 7, 0xC2EF: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xFFA1: b"\x03", 0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC200: b"\x10\xFF\xFF\xFF\xFF\xFF\xFF", 0xC300: b"\xFF\xFF\xFF\xFF\xFF\xFF", 0xC2ED: b"\x00", 0xC27E: b"\x01", 0xC400: b"\x01"}, read={0xFFA0: 1, 0xFFA1: 1, 0xFF98: 1, 0xC200: 7, 0xC2EF: 1}),
]
# <<< factory ScoopUp_ReturnToHandEffect

# >>> factory EnergyTrans_TransferEffect
CONTRACT["EnergyTrans_TransferEffect"] = {"compare": ("a",), "preserve": ()}
CASES["EnergyTrans_TransferEffect"] = [
    {"instruction_budget": 6000000, "cycle_budget": 20000000,
     "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xF1: b"\x01",
              wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
              wExcludeArenaPokemon: b"\x00"}},
    dict(POISON, instruction_budget=6000000, cycle_budget=20000000,
         wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xF1: b"\x01",
               wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
               wExcludeArenaPokemon: b"\x00"}),
    {"f": 0x00, "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xF1: b"\x01",
              wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
              wExcludeArenaPokemon: b"\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xF1: b"\x01",
              wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
              wExcludeArenaPokemon: b"\x00"}},
    dict(POISON, instruction_budget=6000000, cycle_budget=20000000,
         wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xF1: b"\x01",
               wPlayerArenaCard: b"\xFF", wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
               wExcludeArenaPokemon: b"\x00"}),
]
# <<< factory EnergyTrans_TransferEffect

# >>> factory DamageSwap_SelectAndSwapEffect
CONTRACT["DamageSwap_SelectAndSwapEffect"] = {"compare": (), "preserve": ()}
CASES["DamageSwap_SelectAndSwapEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC2EF: b"\x01", 0xCBD2: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00"}, "read": {0xCBC8: 1}, "instruction_budget": 6000000, "cycle_budget": 20000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xC2EF: b"\x01", 0xCBD2: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00"}, "read": {0xCBC8: 1}, "instruction_budget": 6000000, "cycle_budget": 20000000}
]
# <<< factory DamageSwap_SelectAndSwapEffect

# >>> factory Gigashock_PlayerSelectEffect
CONTRACT["Gigashock_PlayerSelectEffect"] = {"compare": (), "preserve": ()}
CASES["Gigashock_PlayerSelectEffect"] = [
    {"wram": {0xFF97: b"\x00", 0xC2EF: b"\x01", 0xC3EF: b"\x01"}, "read": {0xFF97: 1, 0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\x00", 0xC2EF: b"\x01", 0xC3EF: b"\x01"}, read={0xFF97: 1, 0xFFA0: 1}),
]
# <<< factory Gigashock_PlayerSelectEffect

# >>> factory HandleSwitchDefendingPokemonEffect
CONTRACT["HandleSwitchDefendingPokemonEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleSwitchDefendingPokemonEffect"] = [
    {"a": 0xFF, "wram": {0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"a": 1, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}}
]
# <<< factory HandleSwitchDefendingPokemonEffect

# >>> factory PidgeottoWhirlwind_SwitchEffect
CONTRACT["PidgeottoWhirlwind_SwitchEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PidgeottoWhirlwind_SwitchEffect"] = [
    {"wram": {0xFFA0: b"\xFF", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}}
]
# <<< factory PidgeottoWhirlwind_SwitchEffect

# >>> factory ButterfreeWhirlwind_SwitchEffect
CONTRACT["ButterfreeWhirlwind_SwitchEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ButterfreeWhirlwind_SwitchEffect"] = [
    {"wram": {0xFFA0: b"\xFF", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}}
]
# <<< factory ButterfreeWhirlwind_SwitchEffect

# >>> factory PidgeyWhirlwind_SwitchEffect
CONTRACT["PidgeyWhirlwind_SwitchEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PidgeyWhirlwind_SwitchEffect"] = [
    {"wram": {0xFFA0: b"\xFF", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}}
]
# <<< factory PidgeyWhirlwind_SwitchEffect

# >>> factory TerrorStrike_SwitchDefendingPokemon
CONTRACT["TerrorStrike_SwitchDefendingPokemon"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TerrorStrike_SwitchDefendingPokemon"] = [
    {"wram": {hTemp_ffa0: b"\x00"}, "read": {hTemp_ffa0: 1}},
    {"wram": {hTemp_ffa0: b"\x01", hTempPlayAreaLocation_ffa1: b"\xFF"}, "read": {hTemp_ffa0: 1, hTempPlayAreaLocation_ffa1: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {hTemp_ffa0: b"\x01", hTempPlayAreaLocation_ffa1: b"\x01", 0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC300: b"\x00" * 0xC8 + b"\x20", 0xCCEF: b"\x00", 0xCAC2: b"\x55", 0xCCC5: b"\x77"}, "read": {0xFF97: 1, 0xCCEF: 1, 0xCAC2: 1, 0xCCC5: 1}}
]
# <<< factory TerrorStrike_SwitchDefendingPokemon

# >>> factory Gale_SwitchEffect
CONTRACT["Gale_SwitchEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Gale_SwitchEffect"] = [
    {"hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC3C8: b"\x01", 0xC3EF: b"\x02", 0xC2EF: b"\x02", 0xCCBF: b"\x12\x34", 0xCAC2: b"\x55"}, "read": {0xCCBF: 2, 0xCAC2: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x00", 0xC3C8: b"\x01", 0xC3EF: b"\x02", 0xC2EF: b"\x02", 0xCCBF: b"\x12\x34", 0xCAC2: b"\x55"}, "read": {0xCCBF: 2, 0xCAC2: 1}},
    {"hl": 0, "wram": {0xFF97: b"\xC2", 0xCCC7: b"\x80", 0xC2EF: b"\x02", 0xCAC2: b"\x55"}, "read": {0xCAC2: 1}}
]
# <<< factory Gale_SwitchEffect

# >>> factory Shift_PlayerSelectEffect
CONTRACT["Shift_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Shift_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xC2EF: b"\x01",
      0xC2BB: b"\x00", 0xC2BC: b"\xFF", 0xC2D4: b"\x81",
      0xC3BB: b"\xFF", 0xC3BC: b"\xFF", 0xC400: b"\x08",
      0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": FRAME_SETUP, "instruction_budget": 20000000,
     "cycle_budget": 100000000, "read": {0xFFA1: 1}},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xC2EF: b"\x01",
          0xC2BB: b"\x00", 0xC2BC: b"\xFF", 0xC2D4: b"\x81",
          0xC3BB: b"\xFF", 0xC3BC: b"\xFF", 0xC400: b"\x08",
          0xCABB: b"\x80", 0xFF40: b"\x80"},
         setup=FRAME_SETUP, instruction_budget=20000000,
         cycle_budget=100000000, read={0xFFA1: 1}),
]
# <<< factory Shift_PlayerSelectEffect

# >>> factory HandlePlayerMetronomeEffect
CONTRACT["HandlePlayerMetronomeEffect"] = {"compare": ("f",), "preserve": ()}
# Seeds: $FF97 hWhoseTurn, $FF9F hTempCardIndex_ff9f, $C2F1 wPlayerDuelistType,
# $CABB wLCDC (0 keeps WaitForVBlank a no-op), $CAC2 wDuelDisplayedScreen,
# $CC10 wPlayerAttackingAttackIndex/CardIndex/CardID, $CCAA wLoadedAttackName,
# $CCC2 wTempCardID_ccc2, $CCC6 wSelectedAttack, $CE73 wMetronomeSelectedAttack.
# Read: $CCF0 wMetronomeEnergyCost. keys cycle release/press so the text box
# wait and the attack menu each see an edge.
CASES["HandlePlayerMetronomeEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, "read": {0xCCF0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, read={0xCCF0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x03, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, "read": {0xCCF0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\xC9\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, "read": {0xCCF0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory HandlePlayerMetronomeEffect

# >>> factory ClefairyMetronome_UseAttackEffect
CONTRACT["ClefairyMetronome_UseAttackEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ClefairyMetronome_UseAttackEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, "read": {0xCCF0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, read={0xCCF0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ClefairyMetronome_UseAttackEffect

# >>> factory ClefableMetronome_UseAttackEffect
CONTRACT["ClefableMetronome_UseAttackEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ClefableMetronome_UseAttackEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, "read": {0xCCF0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xFF9F: b"\x00", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01", 0xCC10: b"\x00\x00\x00", 0xCCAA: b"\x00\x00", 0xCCC2: b"\x00", 0xCCC6: b"\x00", 0xCE73: b"\x00\x00"}, read={0xCCF0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ClefableMetronome_UseAttackEffect

# >>> factory Curse_PlayerSelectEffect
CONTRACT["Curse_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
# keys cycle modulo their length on both sides (runner.c input_index, src/mem.c
# g_key_entries), so [0x00, 0x02] is a fresh B edge every other frame: one
# dismisses DrawWholeScreenTextBox's WaitForWideTextBoxInput (A or B), the next
# cancels the play area menu. Being edge-periodic, the exit is the same whatever
# phase the two runners settle on. wLCDC ($CABB) starts clear so the reference
# does not halt in WaitForVBlank before EnableLCD arms the PPU. hWhoseTurn is
# swapped once on entry and once on the cancel exit, so it comes back as seeded.
CASES["Curse_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00"}, "read": {0xFF97: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={0xFF97: b"\xC2", 0xCABB: b"\x00"}, read={0xFF97: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Curse_PlayerSelectEffect

# >>> factory MrFuji_ReturnToDeckEffect
CONTRACT["MrFuji_ReturnToDeckEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["MrFuji_ReturnToDeckEffect"] = [
    {"b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xC2F1: b"\x00",
               0xC2BA: b"\x3C", 0xC2BB: b"\x01", 0xC2BC: b"\xFF\xFF\xFF\xFF",
               0xC201: b"\x10", 0xC2EF: b"\x02", 0xCAC2: b"\x09"},
     "read": {0xFF98: 1, 0xC201: 1, 0xC2B9: 1, 0xC2BA: 1, 0xC2BB: 5, 0xC2EF: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234,
         wram={0xFF97: b"\xC2", 0xFFA0: b"\x00", 0xC2F1: b"\x00",
               0xC2BA: b"\x3C", 0xC2BB: b"\x01", 0xC2BC: b"\xFF\xFF\xFF\xFF",
               0xC201: b"\x10", 0xC2EF: b"\x02", 0xCAC2: b"\x09"},
         read={0xFF98: 1, 0xC201: 1, 0xC2B9: 1, 0xC2BA: 1, 0xC2BB: 5, 0xC2EF: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory MrFuji_ReturnToDeckEffect

# >>> factory Serial_TossCoinATimes
CONTRACT["Serial_TossCoinATimes"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["Serial_TossCoinATimes"] = [
    dict(POISON, a=0x01, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x00, "d": 0x12, "e": 0x34,
     "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x80",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
     "read": {0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x01, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory Serial_TossCoinATimes

# >>> factory TossCoinATimes_BankB
CONTRACT["TossCoinATimes_BankB"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["TossCoinATimes_BankB"] = [
    dict(POISON, a=0x01, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x00, "d": 0x12, "e": 0x34,
     "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x80",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
     "read": {0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory TossCoinATimes_BankB

# >>> factory Serial_TossZeroCoins
CONTRACT["Serial_TossZeroCoins"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["Serial_TossZeroCoins"] = [
    dict(POISON, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory Serial_TossZeroCoins

# >>> factory Serial_TossCoin
CONTRACT["Serial_TossCoin"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["Serial_TossCoin"] = [
    dict(POISON, a=0x01, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x00, "d": 0x12, "e": 0x34,
     "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x80",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
     "read": {0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x01, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory Serial_TossCoin

# >>> factory NinetalesLure_SwitchEffect
CONTRACT["NinetalesLure_SwitchEffect"] = {"compare": (), "preserve": ()}
CASES["NinetalesLure_SwitchEffect"] = [
    {"wram": {hTemp_ffa0: b"\x00", wDuelDisplayedScreen: b"\xFF"}},
    {"wram": {hTemp_ffa0: b"\x01", wDuelDisplayedScreen: b"\xFF"}},
    dict(POISON, wram={hTemp_ffa0: b"\x02", wDuelDisplayedScreen: b"\xFF"}),
]
# <<< factory NinetalesLure_SwitchEffect

# >>> factory VictreebelLure_SwitchDefendingPokemon
CONTRACT["VictreebelLure_SwitchDefendingPokemon"] = {"compare": (), "preserve": ()}
CASES["VictreebelLure_SwitchDefendingPokemon"] = [
    {"wram": {0xFFA0: b"\x00", 0xCAC2: b"\xFF"}},
    {"wram": {0xFFA0: b"\x01", 0xCAC2: b"\xFF"}},
    dict(POISON, wram={0xFFA0: b"\x02", 0xCAC2: b"\xFF"}),
]
# <<< factory VictreebelLure_SwitchDefendingPokemon

# >>> factory DancingEmbers_MultiplierEffect
CONTRACT["DancingEmbers_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["DancingEmbers_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DancingEmbers_MultiplierEffect

# >>> factory NidoranFFurySwipes_MultiplierEffect
CONTRACT["NidoranFFurySwipes_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["NidoranFFurySwipes_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory NidoranFFurySwipes_MultiplierEffect

# >>> factory PsyduckFurySwipes_MultiplierEffect
CONTRACT["PsyduckFurySwipes_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["PsyduckFurySwipes_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PsyduckFurySwipes_MultiplierEffect

# >>> factory JolteonDoubleKick_MultiplierEffect
CONTRACT["JolteonDoubleKick_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["JolteonDoubleKick_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory JolteonDoubleKick_MultiplierEffect

# >>> factory CometPunch_MultiplierEffect
CONTRACT["CometPunch_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["CometPunch_MultiplierEffect"] = [
    dict(POISON,
         keys=[0x00, 0x01],
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCCB9: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory CometPunch_MultiplierEffect

# >>> factory PinMissile_MultiplierEffect
CONTRACT["PinMissile_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["PinMissile_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PinMissile_MultiplierEffect

# >>> factory PrimeapeFurySwipes_MultiplierEffect
CONTRACT["PrimeapeFurySwipes_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["PrimeapeFurySwipes_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrimeapeFurySwipes_MultiplierEffect

# >>> factory SandslashFurySwipes_MultiplierEffect
CONTRACT["SandslashFurySwipes_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["SandslashFurySwipes_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SandslashFurySwipes_MultiplierEffect

# >>> factory DragoniteLv45Slam_MultiplierEffect
CONTRACT["DragoniteLv45Slam_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["DragoniteLv45Slam_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DragoniteLv45Slam_MultiplierEffect

# >>> factory FuryAttack_MultiplierEffect
CONTRACT["FuryAttack_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["FuryAttack_MultiplierEffect"] = [
    dict(POISON,
         keys=[0x00, 0x01],
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCCB9: 1},
         instruction_budget=20000000, cycle_budget=80000000),
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory FuryAttack_MultiplierEffect

# >>> factory Bonemerang_MultiplierEffect
CONTRACT["Bonemerang_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["Bonemerang_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Bonemerang_MultiplierEffect

# >>> factory CloysterSpikeCannon_MultiplierEffect
CONTRACT["CloysterSpikeCannon_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["CloysterSpikeCannon_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory CloysterSpikeCannon_MultiplierEffect

# >>> factory NidorinaDoubleKick_MultiplierEffect
CONTRACT["NidorinaDoubleKick_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["NidorinaDoubleKick_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory NidorinaDoubleKick_MultiplierEffect

# >>> factory DragoniteLv41Slam_MultiplierEffect
CONTRACT["DragoniteLv41Slam_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["DragoniteLv41Slam_MultiplierEffect"] = [
    dict(POISON,
         keys=[0x00, 0x01],
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCCB9: 1},
         instruction_budget=20000000, cycle_budget=80000000),
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory DragoniteLv41Slam_MultiplierEffect

# >>> factory NidorinoDoubleKick_MultiplierEffect
CONTRACT["NidorinoDoubleKick_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["NidorinoDoubleKick_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory NidorinoDoubleKick_MultiplierEffect

# >>> factory OmastarSpikeCannon_MultiplierEffect
CONTRACT["OmastarSpikeCannon_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["OmastarSpikeCannon_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OmastarSpikeCannon_MultiplierEffect

# >>> factory JynxDoubleslap_MultiplierEffect
CONTRACT["JynxDoubleslap_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["JynxDoubleslap_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xFF97: b"\x01", 0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xFF97: b"\x01", 0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory JynxDoubleslap_MultiplierEffect

# >>> factory PoliwhirlDoubleslap_MultiplierEffect
CONTRACT["PoliwhirlDoubleslap_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["PoliwhirlDoubleslap_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xFF97: b"\x01", 0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xFF97: b"\x01", 0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PoliwhirlDoubleslap_MultiplierEffect

# >>> factory Twineedle_MultiplierEffect
CONTRACT["Twineedle_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["Twineedle_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Twineedle_MultiplierEffect

# >>> factory DragonairSlam_MultiplierEffect
CONTRACT["DragonairSlam_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["DragonairSlam_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DragonairSlam_MultiplierEffect

# >>> factory PetalDance_MultiplierEffect
CONTRACT["PetalDance_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["PetalDance_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCCCE: 8, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2, 0xFF97: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCCCE: 8, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2, 0xFF97: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PetalDance_MultiplierEffect

# >>> factory PlayTrainerEffectAnimation
CONTRACT["PlayTrainerEffectAnimation"] = {"compare": (), "preserve": ()}
CASES["PlayTrainerEffectAnimation"] = [
    {"a": 0x00, "f": 0x00, "b": 0x02, "c": 0x01, "d": 0x00, "e": 0x20, "hl": 0xC200,
     "wram": {0xFF97: b"\xC2", 0xCC05: b"\xC2", 0xCCC4: b"\x15"},
     "read": {0xCCB8: 1, 0xCE7E: 1, 0xCE81: 1, 0xCE82: 1, 0xCE83: 1, 0xCE84: 1, 0xCE7F: 2}},
    {"a": 0x00, "f": 0x80, "b": 0x05, "c": 0x07, "d": 0x01, "e": 0x45, "hl": 0xC300,
     "wram": {0xFF97: b"\xC2", 0xCC05: b"\xC3", 0xCCC4: b"\xA0"},
     "read": {0xCCB8: 1, 0xCE7E: 1, 0xCE81: 1, 0xCE82: 1, 0xCE83: 1, 0xCE84: 1, 0xCE7F: 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xFF97: b"\xC2", 0xCC05: b"\xC2", 0xCCC4: b"\xFE"},
     "oracle": False, "why": "nonzero trainer animation enters the frame-driven animation wait outside the isolated primary oracle path",
     "expect": {0xCCB8: b"\xAA"}}
]
# <<< factory PlayTrainerEffectAnimation

# >>> factory StretchKick_BenchDamageEffect
CONTRACT["StretchKick_BenchDamageEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c", "hl")}
CASES["StretchKick_BenchDamageEffect"] = [
    {"wram": {0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory StretchKick_BenchDamageEffect

# >>> factory IceBreath_RandomPokemonDamageEffect
CONTRACT["IceBreath_RandomPokemonDamageEffect"] = {"compare": (), "preserve": ()}
CASES["IceBreath_RandomPokemonDamageEffect"] = [
	{"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
	dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory IceBreath_RandomPokemonDamageEffect

# >>> factory HypnoDarkMind_DamageBenchEffect
CONTRACT["HypnoDarkMind_DamageBenchEffect"] = {"compare": (), "preserve": ()}
CASES["HypnoDarkMind_DamageBenchEffect"] = [
    {"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
    {"wram": {0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory HypnoDarkMind_DamageBenchEffect

# >>> factory GengarDarkMind_DamageBenchEffect
CONTRACT["GengarDarkMind_DamageBenchEffect"] = {"compare": (), "preserve": ()}
CASES["GengarDarkMind_DamageBenchEffect"] = [
    {"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
    {"wram": {0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory GengarDarkMind_DamageBenchEffect

# >>> factory Spark_BenchDamageEffect
CONTRACT["Spark_BenchDamageEffect"] = {"compare": (), "preserve": ()}
CASES["Spark_BenchDamageEffect"] = [
    {"wram": {0xFFA0: b"\xFF"}, "read": {0xFFA0: 1}},
    {"wram": {0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory Spark_BenchDamageEffect

# >>> factory CatPunchEffect
CONTRACT["CatPunchEffect"] = {"compare": (), "preserve": ()}
CASES["CatPunchEffect"] = [
	{"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCB8: 1, 0xCCEB: 1}},
	dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCB8: 1, 0xCCEB: 1}),
]
# <<< factory CatPunchEffect

# >>> factory Gigashock_BenchDamageEffect
CONTRACT["Gigashock_BenchDamageEffect"] = {"compare": (), "preserve": ()}
CASES["Gigashock_BenchDamageEffect"] = [
    {"wram": {0xFFA0: b"\xff"}},
    {"wram": {0xFFA0: b"\x00\xff", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
    dict(POISON, wram={0xFFA0: b"\x00\xff", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory Gigashock_BenchDamageEffect

# >>> factory ChainLightningEffect
CONTRACT["ChainLightningEffect"] = {"compare": (), "preserve": ()}
CASES["ChainLightningEffect"] = [
    # defending card is PIDGEY ($A3, TYPE_PKMN_COLORLESS): the routine stores
    # the color and returns before touching either Bench.
    {"wram": {0xFF97: b"\xC2", 0xC3D4: b"\x00", 0xC3BB: b"\x00", 0xC480: b"\xA3", 0xCCE6: b"\x00"},
     "read": {0xFFB2: 1, 0xCCE6: 1}},
    # defending card is BULBASAUR ($08, TYPE_PKMN_GRASS); both play areas hold
    # one Pokemon, so each Bench walk exits on its first `dec e`.
    {"wram": {0xFF97: b"\xC2", 0xC3D4: b"\x00", 0xC3BB: b"\x00", 0xC480: b"\x08",
              0xC3EF: b"\x01", 0xC2EF: b"\x01", 0xCCE6: b"\x00"},
     "read": {0xFFB2: 1, 0xCCE6: 1}},
    # one Bench card on each side, CHARMANDER ($30, TYPE_PKMN_FIRE): both
    # colors miss the stored GRASS, so no damage is dealt.
    {"wram": {0xFF97: b"\xC2", 0xC3D4: b"\x00\x00", 0xC3BB: b"\x00\x01",
              0xC480: b"\x08\x30", 0xC2D5: b"\x00", 0xC2BC: b"\x01", 0xC401: b"\x30",
              0xC3EF: b"\x02", 0xC2EF: b"\x02", 0xCCE6: b"\x00"},
     "read": {0xFFB2: 1, 0xCCE6: 1}},
    dict(POISON,
         wram={0xFF97: b"\xC2", 0xC3D4: b"\x00\x00", 0xC3BB: b"\x00\x01",
               0xC480: b"\x08\x30", 0xC2D5: b"\x00", 0xC2BC: b"\x01", 0xC401: b"\x30",
               0xC3EF: b"\x02", 0xC2EF: b"\x02", 0xCCE6: b"\x00"},
         read={0xFFB2: 1, 0xCCE6: 1}),
]
# <<< factory ChainLightningEffect

# >>> factory Firegiver_AddToHandEffect
CONTRACT["Firegiver_AddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Firegiver_AddToHandEffect"] = [
    # Every card location byte holds CARD_LOCATION_ARENA, so the scan never hits
    # CARD_LOCATION_DECK, no Fire Energy is found, and the routine stores the
    # $ff terminator at wDuelTempList and takes the ThereWasNoFireEnergy exit.
    # keys taps A for the wide text box, wLCDC=0 keeps WaitForVBlank a no-op
    # until EnableLCD, wDuelDisplayedScreen=SHUFFLE_DECK keeps
    # PlayDeckShuffleAnimation out of EmptyScreen/portraits (so
    # wVBlankOAMCopyToggle stays clear), and 59 cards not in the deck sends it
    # down the one-card path instead of the shuffle animation.
    {"b": 0x00, "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x09",
              0xC2BA: b"\x3B", 0xC200: b"\x10" * 60, 0xC510: b"\x00"},
     "read": {0xC510: 1}, "expect": {0xC510: b"\xFF"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x09",
               0xC2BA: b"\x3B", 0xC200: b"\x10" * 60, 0xC510: b"\x00"},
         read={0xC510: 1}, expect={0xC510: b"\xFF"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Firegiver_AddToHandEffect

# >>> factory PlayAttackAnimationOverAttackingPokemon
CONTRACT["PlayAttackAnimationOverAttackingPokemon"] = {"compare": ("f",), "preserve": ()}
CASES["PlayAttackAnimationOverAttackingPokemon"] = [
    {"a": 0x00, "f": 0x80, "b": 0x02, "c": 0x01, "d": 0x00, "e": 0x20, "hl": 0xC200,
     "wram": {0xFF97: b"\xC2", 0xFF9D: b"\x02", 0xCC05: b"\xC2", 0xCCC4: b"\x15"},
     "read": {0xCCB8: 1, 0xCE7E: 1, 0xCE81: 1, 0xCE82: 1, 0xCE83: 1, 0xCE84: 1, 0xCE7F: 2}},
    {"a": 0x00, "f": 0x80, "b": 0x05, "c": 0x07, "d": 0x01, "e": 0x45, "hl": 0xC300,
     "wram": {0xFF97: b"\xC2", 0xFF9D: b"\x05", 0xCC05: b"\xC3", 0xCCC4: b"\xA0"},
     "read": {0xCCB8: 1, 0xCE7E: 1, 0xCE81: 1, 0xCE82: 1, 0xCE83: 1, 0xCE84: 1, 0xCE7F: 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xFF97: b"\xC2", 0xFF9D: b"\x02", 0xCC05: b"\xC2", 0xCCC4: b"\xFE"},
     "oracle": False, "why": "nonzero attack animation enters the frame-driven animation wait outside the isolated primary oracle path",
     "expect": {0xCCB8: b"\xAA"}}
]
# <<< factory PlayAttackAnimationOverAttackingPokemon

# >>> factory PokemonTrader_PlayerHandSelection
CONTRACT["PokemonTrader_PlayerHandSelection"] = {"compare": (), "preserve": ()}
CASES["PokemonTrader_PlayerHandSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xC2EE: b"\x01", 0xC242: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00", 0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00", 0xFF91: b"\x02", 0xFFB1: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xFFA0: 1}, "rom_bank": 1, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={0xC2EE: b"\x01", 0xC242: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00", 0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00", 0xFF91: b"\x02", 0xFFB1: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xFFA0: 1}, rom_bank=1, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PokemonTrader_PlayerHandSelection

# >>> factory EnergyRetrieval_PlayerDiscardPileSelection
CONTRACT["EnergyRetrieval_PlayerDiscardPileSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EnergyRetrieval_PlayerDiscardPileSelection"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFFB2: 1, 0xC510: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFFB2: 1, 0xC510: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EnergyRetrieval_PlayerDiscardPileSelection

# >>> factory EnergyRetrieval_PlayerHandSelection
CONTRACT["EnergyRetrieval_PlayerHandSelection"] = {"compare": (), "preserve": ()}
CASES["EnergyRetrieval_PlayerHandSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xC2EE: b"\x02", 0xC242: b"\x00", 0xC243: b"\x01", 0xC510: b"\xFF", 0xCABB: b"\x00", 0xFF91: b"\x02", 0xFF98: b"\x00", 0xFF9F: b"\x00", 0xFFA0: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "rom_bank": 1, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={0xC2EE: b"\x02", 0xC242: b"\x00", 0xC243: b"\x01", 0xC510: b"\xFF", 0xCABB: b"\x00", 0xFF91: b"\x02", 0xFF98: b"\x00", 0xFF9F: b"\x00", 0xFFA0: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], rom_bank=1, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EnergyRetrieval_PlayerHandSelection

# >>> factory HandleEnergyCardsInDiscardPileSelection
CONTRACT["HandleEnergyCardsInDiscardPileSelection"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["HandleEnergyCardsInDiscardPileSelection"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFFB2: 1, 0xC510: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFFB2: 1, 0xC510: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandleEnergyCardsInDiscardPileSelection

# >>> factory EnergyConversion_PlayerSelectEffect
CONTRACT["EnergyConversion_PlayerSelectEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["EnergyConversion_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFFB2: 1, 0xC510: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFFB2: 1, 0xC510: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EnergyConversion_PlayerSelectEffect

# >>> factory MewtwoAltEnergyAbsorption_PlayerSelectEffect
CONTRACT["MewtwoAltEnergyAbsorption_PlayerSelectEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["MewtwoAltEnergyAbsorption_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFFB2: 1, 0xC510: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFFB2: 1, 0xC510: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MewtwoAltEnergyAbsorption_PlayerSelectEffect

# >>> factory MewtwoEnergyAbsorption_PlayerSelectEffect
CONTRACT["MewtwoEnergyAbsorption_PlayerSelectEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["MewtwoEnergyAbsorption_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, "read": {0xFFB2: 1, 0xC510: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC510: b"\xFF"}, read={0xFFB2: 1, 0xC510: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MewtwoEnergyAbsorption_PlayerSelectEffect

# >>> factory FetchEffect
CONTRACT["FetchEffect"] = {"compare": (), "preserve": ()}
CASES["FetchEffect"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01", 0xC2BA: b"\x00", 0xC2EE: b"\x00", 0xCC0D: b"\x01", 0xC201: b"\x00"}, "read": {0xC2BA: 1, 0xC2EE: 1, 0xC201: 1, 0xC242: 1}, "expect": {0xC2BA: b"\x01", 0xC2EE: b"\x01", 0xC201: b"\x01", 0xC242: b"\x01"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x02", 0xC2BA: b"\x00", 0xC2EE: b"\x01", 0xC242: b"\x01", 0xCC0D: b"\x01", 0xC202: b"\x00"}, "read": {0xC2BA: 1, 0xC2EE: 1, 0xC202: 1, 0xC243: 1}, "expect": {0xC2BA: b"\x01", 0xC2EE: b"\x02", 0xC202: b"\x01", 0xC243: b"\x02"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wPlayerDeck: b"\x03", 0xC2BA: b"\x00", 0xC2EE: b"\x00", 0xCC0D: b"\x01", 0xC203: b"\x00"}, read={0xC2BA: 1, 0xC2EE: 1, 0xC203: 1, 0xC242: 1}, expect={0xC2BA: b"\x01", 0xC2EE: b"\x01", 0xC203: b"\x01", 0xC242: b"\x01"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FetchEffect

# >>> factory ProfessorOakEffect
CONTRACT["ProfessorOakEffect"] = {"compare": (), "preserve": ()}
CASES["ProfessorOakEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xC2BA: b"\x00", 0xCABB: b"\x00"},
     "read": {0xC510: 2, 0xCBE8: 1, 0xCBE9: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xC2BA: b"\x00", 0xCABB: b"\x00"},
         read={0xC510: 2, 0xCBE8: 1, 0xCBE9: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ProfessorOakEffect

# >>> factory Maintenance_ReturnToDeckAndDrawEffect
CONTRACT["Maintenance_ReturnToDeckAndDrawEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Maintenance_ReturnToDeckAndDrawEffect"] = [
    {"wram": {0xFF97: b"\xC3", 0xC3F1: b"\x01", 0xC3BA: b"\x02", 0xC3EE: b"\x02", 0xC342: b"\x00\x01", 0xC300: b"\x20\x20", 0xC37E: b"\x00" * 60, 0xCABB: b"\x00"}, "read": {0xC3BA: 1, 0xC37E: 60, 0xC300: 2, 0xC3EE: 1, 0xC342: 1, 0xFF98: 1}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC3", 0xC3F1: b"\x01", 0xC3BA: b"\x02", 0xC3EE: b"\x02", 0xC342: b"\x00\x01", 0xC300: b"\x20\x20", 0xC37E: b"\x00" * 60, 0xCABB: b"\x00"}, read={0xC3BA: 1, 0xC37E: 60, 0xC300: 2, 0xC3EE: 1, 0xC342: 1, 0xFF98: 1}, keys=[0x00, 0x01], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Maintenance_ReturnToDeckAndDrawEffect

# >>> factory ThunderJolt_RecoilEffect
CONTRACT["ThunderJolt_RecoilEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ThunderJolt_RecoilEffect"] = [
    {"f": 0x00, "wram": {hTemp_ffa0: b"\x01"},
     "read": {hTemp_ffa0: 1, _wram_txram3: 2}},
    dict(POISON, wram={hTemp_ffa0: b"\x01"},
         read={hTemp_ffa0: 1, _wram_txram3: 2}),
]
# <<< factory ThunderJolt_RecoilEffect

# >>> factory ZapdosThunder_RecoilEffect
CONTRACT["ZapdosThunder_RecoilEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ZapdosThunder_RecoilEffect"] = [
    {"f": 0x00, "wram": {0xFFA0: b"\x01", 0xCABB: b"\x00"},
     "read": {0xFFA0: 1, 0xCE43: 2}},
    dict(POISON, wram={0xFFA0: b"\x01", 0xCABB: b"\x00"},
         read={0xFFA0: 1, 0xCE43: 2}),
]
# <<< factory ZapdosThunder_RecoilEffect

# >>> factory BillEffect
CONTRACT["BillEffect"] = {"compare": (), "preserve": ()}
CASES["BillEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00", 0xC2EE: b"\x00", 0xC2F1: b"\x00", 0xC27E: b"\x08\x09", 0xCABB: b"\x00"}, "read": {0xC2BA: 1, 0xC2EE: 1, 0xC208: 1, 0xC209: 1, 0xC241: 2, 0xFF98: 1, 0xCBE8: 1, 0xCBE9: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00", 0xC2EE: b"\x00", 0xC2F1: b"\x80", 0xC27E: b"\x08\x09", 0xCABB: b"\x00"}, "read": {0xC2BA: 1, 0xC2EE: 1, 0xC208: 1, 0xC209: 1, 0xC241: 2, 0xFF98: 1, 0xCBE8: 1, 0xCBE9: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x00", 0xC2EE: b"\x00", 0xC2F1: b"\x00", 0xC27E: b"\x08\x09", 0xCABB: b"\x00"}, read={0xC2BA: 1, 0xC2EE: 1, 0xC208: 1, 0xC209: 1, 0xC241: 2, 0xFF98: 1, 0xCBE8: 1, 0xCBE9: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory BillEffect

# >>> factory ImposterProfessorOakEffect
CONTRACT["ImposterProfessorOakEffect"] = {"compare": (), "preserve": ()}
CASES["ImposterProfessorOakEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xC2BA: b"\x00", 0xC3EE: b"\x00", 0xC3BA: b"\x00", 0xCABB: b"\x00"},
     "read": {0xC510: 2, 0xCBE8: 1, 0xCBE9: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xC2BA: b"\x00", 0xC3EE: b"\x00", 0xC3BA: b"\x00", 0xCABB: b"\x00"},
         read={0xC510: 2, 0xCBE8: 1, 0xCBE9: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ImposterProfessorOakEffect

# >>> factory HandlePlayerSelection2HandCards
CONTRACT["HandlePlayerSelection2HandCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandlePlayerSelection2HandCards"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory HandlePlayerSelection2HandCards

# >>> factory HandlePlayerSelection2HandCardsToDiscard
CONTRACT["HandlePlayerSelection2HandCardsToDiscard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandlePlayerSelection2HandCardsToDiscard"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory HandlePlayerSelection2HandCardsToDiscard

# >>> factory SuperEnergyRetrieval_PlayerHandSelection
CONTRACT["SuperEnergyRetrieval_PlayerHandSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SuperEnergyRetrieval_PlayerHandSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFB2: 1, 0xC510: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFB2: 1, 0xC510: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory SuperEnergyRetrieval_PlayerHandSelection

# >>> factory Maintenance_PlayerSelection
CONTRACT["Maintenance_PlayerSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Maintenance_PlayerSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", hTempCardIndex_ff98: b"\x00", hTempCardIndex_ff9f: b"\x00"}, "read": {hCurSelectionItem: 1, wDuelTempList: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory Maintenance_PlayerSelection

# >>> factory ItemFinder_PlayerSelection
CONTRACT["ItemFinder_PlayerSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ItemFinder_PlayerSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory ItemFinder_PlayerSelection

# >>> factory SlicingWindEffect
CONTRACT["SlicingWindEffect"] = {"compare": ("d", "e"), "preserve": ()}
CASES["SlicingWindEffect"] = [
	{"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, "read": {0xCCEB: 1}},
	dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCC7: b"\x01", 0xCCEB: b"\xAA"}, read={0xCCEB: 1}),
]
# <<< factory SlicingWindEffect

# >>> factory SuperEnergyRetrieval_PlayerDiscardPileSelection
CONTRACT["SuperEnergyRetrieval_PlayerDiscardPileSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SuperEnergyRetrieval_PlayerDiscardPileSelection"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", hCurSelectionItem: b"\x00", wDuelTempList: b"\xFF", 0xC2ED: b"\x00", 0xCABB: b"\x00"}, "read": {0xFFA0: 2}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", hCurSelectionItem: b"\x00", wDuelTempList: b"\xFF", 0xC2ED: b"\x00", 0xCABB: b"\x00"}, read={0xFFA0: 2}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SuperEnergyRetrieval_PlayerDiscardPileSelection

# >>> factory ComputerSearch_PlayerDiscardHandSelection
CONTRACT["ComputerSearch_PlayerDiscardHandSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ComputerSearch_PlayerDiscardHandSelection"] = [
    {"keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFB2: 1, 0xC510: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x02], "wram": {0xFF97: b"\xC2", 0xCABB: b"\x00", 0xC500: b"\xFF", 0xFF98: b"\x00", 0xFF9F: b"\x00"}, "read": {0xFFB2: 1, 0xC510: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory ComputerSearch_PlayerDiscardHandSelection

# >>> factory Pokedex_PlayerSelection
# One card left in the deck ($C2BA = 59) caps the ordering at a single card, so
# one A tap finishes the selection and .clear_list is never re-entered. $C2B9 is
# DUELVARS_DECK_CARDS + 59, the only deck slot copied into wDuelTempList; it
# holds deck index 5, whose card id sits at wPlayerDeck + 5 ($C405). $CABB = 0
# keeps WaitForVBlank a no-op until the screen code runs EnableLCD itself,
# $CAB4 = 0 pins the console to DMG so no SGB packet is sent, and $CD9A = 1
# leaves the "Is this OK?" cursor on YES so A confirms instead of restarting.
# Observed: wDuelTempList ($C510 = 05 FF), its ordering slots ($C51A = 01 FF),
# wNumberOfCardsToOrder ($CE75 = 02), hTempList ($FFA0 = 05 FF) and
# hCurSelectionItem ($FFB2 = 02).
CONTRACT["Pokedex_PlayerSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Pokedex_PlayerSelection"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xCAB4: b"\x00", 0xCABB: b"\x00", 0xCD9A: b"\x01",
              0xC2BA: b"\x3B", 0xC2B9: b"\x05", 0xC405: b"\x08",
              0xFFA0: b"\x00\x00"},
     "read": {0xC510: 2, 0xC51A: 2, 0xCE75: 1, 0xFFA0: 2, 0xFFB2: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xCAB4: b"\x00", 0xCABB: b"\x00", 0xCD9A: b"\x01",
              0xC2BA: b"\x3B", 0xC2B9: b"\x05", 0xC405: b"\x08",
              0xFFA0: b"\x00\x00"},
     "read": {0xC510: 2, 0xC51A: 2, 0xCE75: 1, 0xFFA0: 2, 0xFFB2: 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory Pokedex_PlayerSelection

# >>> factory Thrash_RecoilEffect
CONTRACT["Thrash_RecoilEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Thrash_RecoilEffect"] = [
    {"f": 0x00, "wram": {0xFFA0: b"\x01", 0xCABB: b"\x00"},
     "read": {0xFFA0: 1, 0xCCB8: 1}},
    dict(POISON, wram={0xFFA0: b"\x01", 0xCABB: b"\x00"},
         read={0xFFA0: 1, 0xCCB8: 1}),
]
# <<< factory Thrash_RecoilEffect

# >>> factory RaichuThunder_RecoilEffect
CONTRACT["RaichuThunder_RecoilEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["RaichuThunder_RecoilEffect"] = [
    {"f": 0x00, "wram": {hTemp_ffa0: b"\x01"},
     "read": {hTemp_ffa0: 1, _wram_txram3: 2}},
    dict(POISON, wram={hTemp_ffa0: b"\x01"},
         read={hTemp_ffa0: 1, _wram_txram3: 2}),
]
# <<< factory RaichuThunder_RecoilEffect

# >>> factory BigEggsplosion_MultiplierEffect
CONTRACT["BigEggsplosion_MultiplierEffect"] = {"compare": (), "preserve": ()}
CASES["BigEggsplosion_MultiplierEffect"] = [
    {"keys": [0x00, 0x01],
     "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
     "read": {0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCACA: b"\x00\x00\x80", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x00\x00"},
         read={0xCCB9: 3, 0xCCBB: 1, 0xCCBC: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE43: 2, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory BigEggsplosion_MultiplierEffect

# >>> factory PokemonFlute_PlayerSelection
CONTRACT["PokemonFlute_PlayerSelection"] = {"compare": (), "preserve": ()}
CASES["PokemonFlute_PlayerSelection"] = [
    {"keys": [0x00, 0x02],
     "wram": {0xFF97: b"\xC2", 0xC37E: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00",
              0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00",
              0xFF91: b"\x02", 0xFFB1: b"\x00", 0xFF98: b"\x05", 0xFFA0: b"\x00"},
     "read": {0xFFA0: 1}, "expect": {0xFFA0: b"\x05"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "keys": [0x00, 0x02],
     "wram": {0xFF97: b"\xC2", 0xC37E: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00",
              0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00",
              0xFF91: b"\x02", 0xFFB1: b"\x00", 0xFF98: b"\x05", 0xFFA0: b"\x00"},
     "read": {0xFFA0: 1}, "expect": {0xFFA0: b"\x05"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         wram={0xFF97: b"\xC2", 0xC37E: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00",
               0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00",
               0xFF91: b"\x02", 0xFFB1: b"\x00", 0xFF98: b"\x05", 0xFFA0: b"\x00"},
         read={0xFFA0: 1}, expect={0xFFA0: b"\x05"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PokemonFlute_PlayerSelection

# >>> factory DevolutionBeam_DevolveEffect
CONTRACT["DevolutionBeam_DevolveEffect"] = {"compare": (), "preserve": ()}
CASES["DevolutionBeam_DevolveEffect"] = [
    {"wram": {hTemp_ffa0: b"\xff", wDuelDisplayedScreen: b"\x00"}, "read": {wDuelDisplayedScreen: 1}},
    dict(POISON, wram={hTemp_ffa0: b"\xff", wDuelDisplayedScreen: b"\x00"}, read={wDuelDisplayedScreen: 1}),
]
# <<< factory DevolutionBeam_DevolveEffect

# >>> factory MarowakCallForFamily_PlayerSelectEffect
CONTRACT["MarowakCallForFamily_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["MarowakCallForFamily_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MarowakCallForFamily_PlayerSelectEffect

# >>> factory DealDamageToAllBenchedPokemon
CONTRACT["DealDamageToAllBenchedPokemon"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ()}
CASES["DealDamageToAllBenchedPokemon"] = [
    {"a": 0x14, "f": 0x00, "wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01"})
]
# <<< factory DealDamageToAllBenchedPokemon

# >>> factory HandleProphecyScreen
CONTRACT["HandleProphecyScreen"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleProphecyScreen"] = [
    {"keys": HPS_KEYS, "wram": dict(HPS_SEED), "setup": HPS_SETUP, "read": dict(HPS_READ), "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=HPS_KEYS, wram=dict(HPS_SEED), setup=HPS_SETUP, read=dict(HPS_READ), instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandleProphecyScreen

# >>> factory EarthquakeEffect
CONTRACT["EarthquakeEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["EarthquakeEffect"] = [
    {"f": 0x00, "wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01"}, "read": {0xCCE6: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x01"}, read={0xCCE6: 1}),
]
# <<< factory EarthquakeEffect

# >>> factory Blizzard_BenchDamageEffect
CONTRACT["Blizzard_BenchDamageEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["Blizzard_BenchDamageEffect"] = [
    {"f": 0x00, "wram": {0xFFA0: b"\x00", 0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xCCE6: b"\x00"}, "read": {0xCCE6: 1}},
    {"f": 0x00, "wram": {0xFFA0: b"\x01", 0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xCCE6: b"\x00"}, "read": {0xCCE6: 1}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xCCE6: b"\x00"}, read={0xCCE6: 1}),
]
# <<< factory Blizzard_BenchDamageEffect

# >>> factory Thunderpunch_RecoilEffect
CONTRACT["Thunderpunch_RecoilEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Thunderpunch_RecoilEffect"] = [
    {"f": 0x00, "wram": {hTemp_ffa0: b"\x01"},
     "read": {hTemp_ffa0: 1}},
    dict(POISON, wram={hTemp_ffa0: b"\x01"},
         read={hTemp_ffa0: 1}),
]
# <<< factory Thunderpunch_RecoilEffect

# >>> factory Revive_PlayerSelection
CONTRACT["Revive_PlayerSelection"] = {"compare": (), "preserve": ()}
CASES["Revive_PlayerSelection"] = [
    {"keys": [0x00, 0x02],
     "wram": {0xFF97: b"\xC2", 0xC37E: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00",
              0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00",
              0xFF91: b"\x02", 0xFFB1: b"\x00", 0xFF98: b"\x05", 0xFFA0: b"\x00"},
     "read": {0xFFA0: 1}, "expect": {0xFFA0: b"\x05"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         wram={0xFF97: b"\xC2", 0xC37E: b"\x00", 0xC510: b"\xFF", 0xCABB: b"\x00",
               0xCBCF: b"\x00", 0xCBD0: b"\x00", 0xCBD6: b"\x00", 0xCBDF: b"\x00",
               0xFF91: b"\x02", 0xFFB1: b"\x00", 0xFF98: b"\x05", 0xFFA0: b"\x00"},
         read={0xFFA0: 1}, expect={0xFFA0: b"\x05"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Revive_PlayerSelection

# >>> factory BellsproutCallForFamily_PlayerSelectEffect
CONTRACT["BellsproutCallForFamily_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["BellsproutCallForFamily_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory BellsproutCallForFamily_PlayerSelectEffect

# >>> factory EnergySearch_PlayerSelection
CONTRACT["EnergySearch_PlayerSelection"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EnergySearch_PlayerSelection"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EnergySearch_PlayerSelection

# >>> factory KrabbyCallForFamily_PlayerSelectEffect
CONTRACT["KrabbyCallForFamily_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["KrabbyCallForFamily_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory KrabbyCallForFamily_PlayerSelectEffect

# >>> factory NidoranFCallForFamily_PlayerSelectEffect
CONTRACT["NidoranFCallForFamily_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["NidoranFCallForFamily_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x00"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory NidoranFCallForFamily_PlayerSelectEffect

# >>> factory TossCoin_BankB
CONTRACT["TossCoin_BankB"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["TossCoin_BankB"] = [
    dict(POISON, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, d=0x56, e=0x78,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x80",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x78\x56"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TossCoin_BankB

# >>> factory GustOfWind_SwitchEffect
CONTRACT["GustOfWind_SwitchEffect"] = {"compare": (), "preserve": ()}
CASES["GustOfWind_SwitchEffect"] = [
    {"wram": {0xCAC2: b"\x05", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "read": {0xCAC2: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {0xCAC2: b"\xFF", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "read": {0xCAC2: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xCAC2: b"\x03", 0xCABB: b"\x80", 0xFF40: b"\x80"}, read={0xCAC2: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory GustOfWind_SwitchEffect

# >>> factory Confusion50PercentEffect
CONTRACT["Confusion50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Confusion50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Confusion50PercentEffect

# >>> factory Poison50PercentEffect
CONTRACT["Poison50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Poison50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Poison50PercentEffect

# >>> factory ApplyAndAnimateHPRecovery
CONTRACT["ApplyAndAnimateHPRecovery"] = {"compare": (), "preserve": ()}
CASES["ApplyAndAnimateHPRecovery"] = [
    _hp_recovery_case(0x50, d=0x00, e=0x14),
    _hp_recovery_case(0x10, d=0x00, e=0x01),
    _hp_recovery_case(0x08, d=0x00, e=0x7F),
    _hp_recovery_case(0x30, **POISON),
]
# <<< factory ApplyAndAnimateHPRecovery

# >>> factory Paralysis50PercentEffect
CONTRACT["Paralysis50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Paralysis50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Paralysis50PercentEffect

# >>> factory PlayerPickAttackForAmnesia
CONTRACT["PlayerPickAttackForAmnesia"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PlayerPickAttackForAmnesia"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PlayerPickAttackForAmnesia

# >>> factory ZubatSupersonicEffect
CONTRACT["ZubatSupersonicEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ZubatSupersonicEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ZubatSupersonicEffect

# >>> factory ShellderSupersonicEffect
CONTRACT["ShellderSupersonicEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ShellderSupersonicEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ShellderSupersonicEffect

# >>> factory TentacruelSupersonicEffect
CONTRACT["TentacruelSupersonicEffect"] = {"compare": ("f",), "preserve": ()}
CASES["TentacruelSupersonicEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TentacruelSupersonicEffect

# >>> factory FirstAid_HealEffect
CONTRACT["FirstAid_HealEffect"] = {"compare": (), "preserve": ()}
CASES["FirstAid_HealEffect"] = [
    _hp_recovery_case(0x50),
    _hp_recovery_case(0x10),
    _hp_recovery_case(0x08),
    _hp_recovery_case(0x30, **POISON),
]
# <<< factory FirstAid_HealEffect

# >>> factory GolbatLeechLifeEffect
CONTRACT["GolbatLeechLifeEffect"] = {"compare": (), "preserve": ()}
CASES["GolbatLeechLifeEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x14\x00"}),
    _hp_recovery_case(0x10, wram={0xCCBF: b"\x01\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x14\x00"}),
]
# <<< factory GolbatLeechLifeEffect

# >>> factory VenonatLeechLifeEffect
CONTRACT["VenonatLeechLifeEffect"] = {"compare": (), "preserve": ()}
CASES["VenonatLeechLifeEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x14\x00"}),
    _hp_recovery_case(0x10, wram={0xCCBF: b"\x01\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x14\x00"}),
]
# <<< factory VenonatLeechLifeEffect

# >>> factory ZubatLeechLifeEffect
CONTRACT["ZubatLeechLifeEffect"] = {"compare": (), "preserve": ()}
CASES["ZubatLeechLifeEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x14\x00"}),
    _hp_recovery_case(0x10, wram={0xCCBF: b"\x01\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x14\x00"}),
]
# <<< factory ZubatLeechLifeEffect

# >>> factory ExeggcuteLeechSeedEffect
CONTRACT["ExeggcuteLeechSeedEffect"] = {"compare": (), "preserve": ()}
CASES["ExeggcuteLeechSeedEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x14\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x00\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x14\x00"}),
]
# <<< factory ExeggcuteLeechSeedEffect

# >>> factory BulbasaurLeechSeedEffect
CONTRACT["BulbasaurLeechSeedEffect"] = {"compare": (), "preserve": ()}
CASES["BulbasaurLeechSeedEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x14\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x00\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x14\x00"}),
]
# <<< factory BulbasaurLeechSeedEffect

# >>> factory PoliwhirlAmnesia_PlayerSelectEffect
CONTRACT["PoliwhirlAmnesia_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PoliwhirlAmnesia_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC2F1: b"\x01", 0xCABB: b"\x00", 0xCAC2: b"\x01"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PoliwhirlAmnesia_PlayerSelectEffect

# >>> factory SlowpokeAmnesia_PlayerSelectEffect
CONTRACT["SlowpokeAmnesia_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SlowpokeAmnesia_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xC2F1: b"\x00", 0xC3BB: b"\x00", 0xC480: b"\x08", 0xC3F1: b"\x01", 0xCAC2: b"\x01", 0xCABB: b"\x00", 0xFFA0: b"\x55"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xC2F1: b"\x00", 0xC3BB: b"\x00", 0xC480: b"\x08", 0xC3F1: b"\x01", 0xCAC2: b"\x01", 0xFFA0: b"\x55"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SlowpokeAmnesia_PlayerSelectEffect

# >>> factory LickitungSupersonicEffect
CONTRACT["LickitungSupersonicEffect"] = {"compare": ("f",), "preserve": ()}
CASES["LickitungSupersonicEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCCED: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCCED: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LickitungSupersonicEffect

# >>> factory NidorinaSupersonicEffect
CONTRACT["NidorinaSupersonicEffect"] = {"compare": ("f",), "preserve": ()}
CASES["NidorinaSupersonicEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCC4: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCC4: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory NidorinaSupersonicEffect

# >>> factory Sleep50PercentEffect
CONTRACT["Sleep50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Sleep50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Sleep50PercentEffect

# >>> factory KadabraRecover_HealEffect
CONTRACT["KadabraRecover_HealEffect"] = {"compare": (), "preserve": ()}
CASES["KadabraRecover_HealEffect"] = [
    _hp_recovery_case(0x50),
    _hp_recovery_case(0x10),
    _hp_recovery_case(0x08),
    _hp_recovery_case(0x30, **POISON),
]
# <<< factory KadabraRecover_HealEffect

# >>> factory StarmieRecover_HealEffect
CONTRACT["StarmieRecover_HealEffect"] = {"compare": (), "preserve": ()}
CASES["StarmieRecover_HealEffect"] = [
    _hp_recovery_case(0x50),
    _hp_recovery_case(0x10),
    _hp_recovery_case(0x08),
    _hp_recovery_case(0x30, **POISON),
]
# <<< factory StarmieRecover_HealEffect

# >>> factory SingEffect
CONTRACT["SingEffect"] = {"compare": ("f",), "preserve": ()}
CASES["SingEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2,
               0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2,
               0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SingEffect

# >>> factory SleepingGasEffect
CONTRACT["SleepingGasEffect"] = {"compare": ("f",), "preserve": ()}
CASES["SleepingGasEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCCCD: 1, 0xCCCE: 3},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SleepingGasEffect

# >>> factory AbsorbEffect
CONTRACT["AbsorbEffect"] = {"compare": (), "preserve": ()}
CASES["AbsorbEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x1e\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x19\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x00\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x1e\x00"}),
]
# <<< factory AbsorbEffect

# >>> factory ButterfreeMegaDrainEffect
CONTRACT["ButterfreeMegaDrainEffect"] = {"compare": (), "preserve": ()}
CASES["ButterfreeMegaDrainEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x1e\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x19\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x00\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x1e\x00"}),
]
# <<< factory ButterfreeMegaDrainEffect

# >>> factory AcidEffect
_acid_toss_fix = {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06",
                  0xCABB: b"\x00", 0xCACA: b"\x00\x00\x00",
                  0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
                  0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"}
_acid_toss_fix_tail = dict(_acid_toss_fix)
_acid_toss_fix_tail[0xCACA] = b"\x00\x00\x80"
_acid_setup = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
CONTRACT["AcidEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["AcidEffect"] = [
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", **_acid_toss_fix},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x55", 0xC2F6: b"\x66", **_acid_toss_fix_tail},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, hl=0xC240, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x12", 0xC2F6: b"\x34", **_acid_toss_fix},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory AcidEffect

# >>> factory BoneAttackEffect
CONTRACT["BoneAttackEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["BoneAttackEffect"] = [
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", **_acid_toss_fix},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x55", 0xC2F6: b"\x66", **_acid_toss_fix_tail},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, hl=0xC240, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x12", 0xC2F6: b"\x34", **_acid_toss_fix},
         read={0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory BoneAttackEffect

# >>> factory ArcanineQuickAttack_DamageBoostEffect
CONTRACT["ArcanineQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["ArcanineQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ArcanineQuickAttack_DamageBoostEffect

# >>> factory EeveeQuickAttack_DamageBoostEffect
CONTRACT["EeveeQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["EeveeQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EeveeQuickAttack_DamageBoostEffect

# >>> factory ElectabuzzQuickAttack_DamageBoostEffect
CONTRACT["ElectabuzzQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["ElectabuzzQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ElectabuzzQuickAttack_DamageBoostEffect

# >>> factory FlareonQuickAttack_DamageBoostEffect
CONTRACT["FlareonQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["FlareonQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FlareonQuickAttack_DamageBoostEffect

# >>> factory JolteonQuickAttack_DamageBoostEffect
CONTRACT["JolteonQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["JolteonQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory JolteonQuickAttack_DamageBoostEffect

# >>> factory FearowAgilityEffect
CONTRACT["FearowAgilityEffect"] = {"compare": (), "preserve": ()}
CASES["FearowAgilityEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FearowAgilityEffect

# >>> factory ClampEffect
CONTRACT["ClampEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ClampEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCB9: b"\x10\x00", 0xCCED: b"\x00",
               0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCCCD: 1, 0xCCCE: 3,
               0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCB9: b"\x10\x00", 0xCCED: b"\x00",
               0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCCCD: 1, 0xCCCE: 3,
               0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ClampEffect

# >>> factory HideInShellEffect
CONTRACT["HideInShellEffect"] = {"compare": ("f",), "preserve": ()}
CASES["HideInShellEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HideInShellEffect

# >>> factory KakunaStiffenEffect
CONTRACT["KakunaStiffenEffect"] = {"compare": ("f",), "preserve": ()}
CASES["KakunaStiffenEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory KakunaStiffenEffect

# >>> factory MetapodStiffenEffect
CONTRACT["MetapodStiffenEffect"] = {"compare": ("f",), "preserve": ()}
CASES["MetapodStiffenEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MetapodStiffenEffect

# >>> factory LeerEffect
CONTRACT["LeerEffect"] = {"compare": ("f",), "preserve": ()}
CASES["LeerEffect"] = [
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LeerEffect

# >>> factory Fly_Success50PercentEffect
CONTRACT["Fly_Success50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["Fly_Success50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Fly_Success50PercentEffect

# >>> factory MoltresLv35DiveBomb_Success50PercentEffect
CONTRACT["MoltresLv35DiveBomb_Success50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["MoltresLv35DiveBomb_Success50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MoltresLv35DiveBomb_Success50PercentEffect

# >>> factory MoltresLv37DiveBomb_Success50PercentEffect
CONTRACT["MoltresLv37DiveBomb_Success50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["MoltresLv37DiveBomb_Success50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MoltresLv37DiveBomb_Success50PercentEffect

# >>> factory HornHazard_NoDamage50PercentEffect
CONTRACT["HornHazard_NoDamage50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["HornHazard_NoDamage50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", 0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCB9: 2, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HornHazard_NoDamage50PercentEffect

# >>> factory RapidashStomp_DamageBoostEffect
CONTRACT["RapidashStomp_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["RapidashStomp_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory RapidashStomp_DamageBoostEffect

# >>> factory ScrunchEffect
CONTRACT["ScrunchEffect"] = {"compare": ("f",), "preserve": ()}
CASES["ScrunchEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ScrunchEffect

# >>> factory SquirtleWithdrawEffect
CONTRACT["SquirtleWithdrawEffect"] = {"compare": ("f",), "preserve": ()}
CASES["SquirtleWithdrawEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SquirtleWithdrawEffect

# >>> factory TailWagEffect
CONTRACT["TailWagEffect"] = {"compare": ("f",), "preserve": ()}
CASES["TailWagEffect"] = [
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(hl=0xC200, keys=[0x00, 0x01],
         wram={0xC2E8: b"\x00", 0xC2F6: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xC2E8: 1, 0xC2F6: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TailWagEffect

# >>> factory TantrumEffect
CONTRACT["TantrumEffect"] = {"compare": ("f",), "preserve": ()}
CASES["TantrumEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TantrumEffect

# >>> factory Rampage_Confusion50PercentEffect
CONTRACT["Rampage_Confusion50PercentEffect"] = {"compare": (), "preserve": ()}
CASES["Rampage_Confusion50PercentEffect"] = [
    # No duelist seeds: the reference toss path leaves hWhoseTurn elsewhere
    # (known harness asymmetry), and any seeded address is compared at exit.
    # AddToDamage(damage.a) still runs deterministically on both sides; the
    # mutation's +1 shows up in wDamage ($CCB9) whether or not damage is 0.
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", 0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCCCD: 1, 0xCCCE: 3, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", 0xCCCD: b"\x00", 0xCCCE: b"\x00\x00\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCCCD: 1, 0xCCCE: 3, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Rampage_Confusion50PercentEffect

# >>> factory WartortleWithdrawEffect
CONTRACT["WartortleWithdrawEffect"] = {"compare": ("f",), "preserve": ()}
CASES["WartortleWithdrawEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", 0xCCED: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCCED: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory WartortleWithdrawEffect

# >>> factory VenusaurMegaDrainEffect
CONTRACT["VenusaurMegaDrainEffect"] = {"compare": (), "preserve": ()}
CASES["VenusaurMegaDrainEffect"] = [
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x1e\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x19\x00"}),
    _hp_recovery_case(0x50, wram={0xCCBF: b"\x00\x00"}),
    _hp_recovery_case(0x30, **POISON, wram={0xCCBF: b"\x1e\x00"}),
]
# <<< factory VenusaurMegaDrainEffect

# >>> factory Thunderpunch_ModifierEffect
CONTRACT["Thunderpunch_ModifierEffect"] = {"compare": (), "preserve": ()}
CASES["Thunderpunch_ModifierEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x00\x00", 0xFFA0: b"\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xFFA0: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x00\x00", 0xFFA0: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xFFA0: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Thunderpunch_ModifierEffect

# >>> factory SeadraAgilityEffect
CONTRACT["SeadraAgilityEffect"] = {"compare": (), "preserve": ()}
CASES["SeadraAgilityEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SeadraAgilityEffect

# >>> factory RaichuAgilityEffect
CONTRACT["RaichuAgilityEffect"] = {"compare": (), "preserve": ()}
CASES["RaichuAgilityEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory RaichuAgilityEffect

# >>> factory RapidashAgilityEffect
CONTRACT["RapidashAgilityEffect"] = {"compare": (), "preserve": ()}
CASES["RapidashAgilityEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB8: b"\x00", **_acid_toss_fix},
         read={0xCCB8: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory RapidashAgilityEffect

# >>> factory SpacingOut_Success50PercentEffect
CONTRACT["SpacingOut_Success50PercentEffect"] = {"compare": (), "preserve": ()}
CASES["SpacingOut_Success50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCD9C: b"\xFF",
               0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\x00",
               0xFFA0: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00"},
         read={0xFFA0: 1, 0xCCB8: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCD9C: b"\xFF",
               0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\x00",
               0xFFA0: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00"},
         read={0xFFA0: 1, 0xCCB8: 1, 0xCCED: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory SpacingOut_Success50PercentEffect

# >>> factory VaporeonQuickAttack_DamageBoostEffect
CONTRACT["VaporeonQuickAttack_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["VaporeonQuickAttack_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory VaporeonQuickAttack_DamageBoostEffect

# >>> factory Thrash_ModifierEffect
CONTRACT["Thrash_ModifierEffect"] = {"compare": (), "preserve": ()}
CASES["Thrash_ModifierEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x00\x00", 0xFFA0: b"\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xFFA0: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x00\x00", 0xFFA0: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xFFA0: 1, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Thrash_ModifierEffect

# >>> factory ZapdosThunder_Recoil50PercentEffect
CONTRACT["ZapdosThunder_Recoil50PercentEffect"] = {"compare": (), "preserve": ()}
CASES["ZapdosThunder_Recoil50PercentEffect"] = [
    dict(keys=[0x00, 0x01], wram={hTemp_ffa0: b"\x00", **_acid_toss_fix}, read={hTemp_ffa0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01], wram={hTemp_ffa0: b"\x00", **_acid_toss_fix_tail}, read={hTemp_ffa0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01], wram={hTemp_ffa0: b"\x77", **_acid_toss_fix}, read={hTemp_ffa0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory ZapdosThunder_Recoil50PercentEffect

# >>> factory RaichuThunder_Recoil50PercentEffect
CONTRACT["RaichuThunder_Recoil50PercentEffect"] = {"compare": (), "preserve": ()}
CASES["RaichuThunder_Recoil50PercentEffect"] = [
    dict(keys=[0x00, 0x01], wram={**_acid_toss_fix}, read={hTemp_ffa0: 1}, setup=SETUP, **BUDGET),
    dict(keys=[0x00, 0x01], wram={**_acid_toss_fix_tail}, read={hTemp_ffa0: 1}, setup=SETUP, **BUDGET),
    dict(POISON, keys=[0x00, 0x01], wram={**_acid_toss_fix}, read={hTemp_ffa0: 1}, setup=SETUP, **BUDGET),
]
# <<< factory RaichuThunder_Recoil50PercentEffect

# >>> factory TaurosStomp_DamageBoostEffect
CONTRACT["TaurosStomp_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["TaurosStomp_DamageBoostEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TaurosStomp_DamageBoostEffect

# >>> factory MirrorMove_InitialEffect2
CONTRACT["MirrorMove_InitialEffect2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["MirrorMove_InitialEffect2"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x00"}, "read": {0xFFA0: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x01"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x01"}, read={0xFFA0: 1}),
]
# <<< factory MirrorMove_InitialEffect2

# >>> factory MysteryAttack_RecoverEffect
CONTRACT["MysteryAttack_RecoverEffect"] = {"compare": (), "preserve": ()}
CASES["MysteryAttack_RecoverEffect"] = [
    _hp_recovery_case(0x50, wram={hTemp_ffa0: b"\x04"}),
    _hp_recovery_case(0x10, wram={hTemp_ffa0: b"\x03"}),
    _hp_recovery_case(0x08, wram={hTemp_ffa0: b"\x00"}),
    _hp_recovery_case(0x30, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={hTemp_ffa0: b"\x04"}),
]
# <<< factory MysteryAttack_RecoverEffect

# >>> factory ThunderJolt_Recoil50PercentEffect
CONTRACT["ThunderJolt_Recoil50PercentEffect"] = {"compare": ("a", "f", "b", "hl"), "preserve": ()}
CASES["ThunderJolt_Recoil50PercentEffect"] = [
    dict(keys=[0x00, 0x01], wram={0xFFA0: b"\x00", **_acid_toss_fix}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01], wram={0xFFA0: b"\x00", **_acid_toss_fix_tail}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01], wram={0xFFA0: b"\x77", **_acid_toss_fix}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ThunderJolt_Recoil50PercentEffect

# >>> factory LeekSlap_NoDamage50PercentEffect
CONTRACT["LeekSlap_NoDamage50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["LeekSlap_NoDamage50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", 0xCCBB: b"\x10", 0xCCBC: b"\x00", **_acid_toss_fix},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xCCB9: b"\x10\x00", 0xCCBB: b"\x10", 0xCCBC: b"\x00", **_acid_toss_fix_tail},
         read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1, 0xCAC2: 1},
         setup=_acid_setup, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LeekSlap_NoDamage50PercentEffect

# >>> factory Blizzard_BenchDamage50PercentEffect
CONTRACT["Blizzard_BenchDamage50PercentEffect"] = {"compare": (), "preserve": ()}
CASES["Blizzard_BenchDamage50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1,
               0xCE4E: 2, 0xCAC2: 1, 0xFFA0: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1,
               0xCE4E: 2, 0xCAC2: 1, 0xFFA0: 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Blizzard_BenchDamage50PercentEffect

# >>> factory SpearowMirrorMove_InitialEffect2
CONTRACT["SpearowMirrorMove_InitialEffect2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SpearowMirrorMove_InitialEffect2"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x00"}, "read": {0xFFA0: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2F8: b"\x01"}, "read": {0xFFA0: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2F8: b"\x01"}, read={0xFFA0: 1}),
]
# <<< factory SpearowMirrorMove_InitialEffect2

# >>> factory PidgeottoMirrorMove_InitialEffect2
CONTRACT["PidgeottoMirrorMove_InitialEffect2"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PidgeottoMirrorMove_InitialEffect2"] = [
	{},
	dict(POISON),
]
# <<< factory PidgeottoMirrorMove_InitialEffect2

# >>> factory VenomPowder_PoisonConfusion50PercentEffect
CONTRACT["VenomPowder_PoisonConfusion50PercentEffect"] = {"compare": ("f",), "preserve": ()}
CASES["VenomPowder_PoisonConfusion50PercentEffect"] = [
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCF1: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3,
               0xCE4E: 2, 0xCCF1: 1, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCF1: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3,
               0xCE4E: 2, 0xCCF1: 1, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory VenomPowder_PoisonConfusion50PercentEffect

# >>> factory ThunderstormEffect
CONTRACT["ThunderstormEffect"] = {"compare": (), "preserve": ()}
CASES["ThunderstormEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xFFA1: b"\xFF"},
     "read": {0xFFB2: 1, 0xFFA0: 1, 0xFFA1: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x01", 0xFFA1: b"\xFF"},
         read={0xFFB2: 1, 0xFFA0: 1, 0xFFA1: 1}),
]
# <<< factory ThunderstormEffect

# >>> factory FoulGas_PoisonOrConfusionEffect
CONTRACT["FoulGas_PoisonOrConfusionEffect"] = {"compare": ("f",), "preserve": ()}
CASES["FoulGas_PoisonOrConfusionEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCCCD: 1, 0xCCCE: 3, 0xCE4E: 2, 0xCAC2: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory FoulGas_PoisonOrConfusionEffect

# >>> factory Sprout_PlayerSelectEffect
CONTRACT["Sprout_PlayerSelectEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Sprout_PlayerSelectEffect"] = [
    {"keys": [0x00, 0x10, 0x01], "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "read": {0xFFA0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x10, 0x01], wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCABB: b"\x80", 0xFF40: b"\x80"}, read={0xFFA0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Sprout_PlayerSelectEffect

# >>> factory FullHeal_ClearStatusEffect
CONTRACT["FullHeal_ClearStatusEffect"] = {"compare": (), "preserve": ()}
CASES["FullHeal_ClearStatusEffect"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": {0xFF97: b"\xC2", 0xCC05: b"\xC2", 0xCCC4: b"\x15", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC3F1: b"\x00", 0xC2F0: b"\x77", 0xC3F0: b"\x55", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80"}, "read": {0xC2F0: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, f=0xF0, wram={0xFF97: b"\xC2", 0xCC05: b"\xC2", 0xCCC4: b"\x15", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC3F1: b"\x00", 0xC2F0: b"\x77", 0xC3F0: b"\x55", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80"}, read={0xC2F0: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory FullHeal_ClearStatusEffect

# >>> factory ImakuniEffect
CONTRACT["ImakuniEffect"] = {"compare": (), "preserve": ()}
CASES["ImakuniEffect"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)), wArenaCardStatus: b"\x00"}, "read": {wArenaCardStatus: 1}, **dict(FRAME_BUDGET), "setup": FRAME_SETUP, "keys": [0x00, 0x01]},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((CLEFAIRY_DOLL,)), wArenaCardStatus: b"\x00"}, "read": {wArenaCardStatus: 1}, **dict(FRAME_BUDGET), "setup": FRAME_SETUP, "keys": [0x00, 0x01]},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((MYSTERIOUS_FOSSIL,)), wArenaCardStatus: b"\x00"}, "read": {wArenaCardStatus: 1}, **dict(FRAME_BUDGET), "setup": FRAME_SETUP, "keys": [0x00, 0x01]},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)), wArenaCardStatus: b"\xF0"}, "read": {wArenaCardStatus: 1}, **dict(FRAME_BUDGET), "setup": FRAME_SETUP, "keys": [0x00, 0x01]},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)), wArenaCardStatus: b"\xF0"}, read={wArenaCardStatus: 1}, **dict(FRAME_BUDGET), setup=FRAME_SETUP, keys=[0x00, 0x01]),
]
# <<< factory ImakuniEffect

# >>> factory GamblerEffect
CONTRACT["GamblerEffect"] = {"compare": (), "preserve": ()}
CASES["GamblerEffect"] = [{"keys": [0x00, 0x01], "wram": {0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xF0\x00"}, "read": {0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCBE8: 1, 0xCBE9: 1}, "setup": [{"fn": "SwapTurn"}, {"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}, dict(POISON, keys=[0x00, 0x01], wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00", 0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01", 0xCE4E: b"\xF0\x00"}, read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1, 0xCBE8: 1, 0xCBE9: 1}, setup=[{"fn": "SwapTurn"}, {"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory GamblerEffect

# >>> factory HealingWind_PlayAreaHealEffect
CONTRACT["HealingWind_PlayAreaHealEffect"] = {"compare": (), "preserve": ()}
CASES["HealingWind_PlayAreaHealEffect"] = [
    _hp_recovery_case(0x50, wram={0xC2EF: b"\x01", 0xFF9D: b"\x00"}, read={0xC2C8: 1, 0xCCB8: 1, 0xFF9D: 1}),
    _hp_recovery_case(0x40, wram={0xC2EF: b"\x01", 0xFF9D: b"\x00"}, read={0xC2C8: 1, 0xCCB8: 1, 0xFF9D: 1}),
    _hp_recovery_case(0x10, wram={0xC2EF: b"\x01", 0xFF9D: b"\x00"}, read={0xC2C8: 1, 0xCCB8: 1, 0xFF9D: 1}),
    _hp_recovery_case(0x30, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={0xC2EF: b"\x01", 0xFF9D: b"\x00"}, read={0xC2C8: 1, 0xCCB8: 1, 0xFF9D: 1}),
]
# <<< factory HealingWind_PlayAreaHealEffect

# >>> factory SpitPoison_Poison50PercentEffect
CONTRACT["SpitPoison_Poison50PercentEffect"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["SpitPoison_Poison50PercentEffect"] = [
    dict(keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1,
               0xCCCD: 1, 0xCCCE: 3, 0xCCB8: 1, 0xCCED: 1, 0xCCF1: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01],
         wram={0xC2F1: b"\x00", 0xCC09: b"\x00", 0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00", 0xCCCD: b"\x00", 0xCCB8: b"\x00", 0xCCED: b"\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF", 0xCD9F: b"\x01",
               0xCE4E: b"\xEE\xDD"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2, 0xCAC2: 1,
               0xCCCD: 1, 0xCCCE: 3, 0xCCB8: 1, 0xCCED: 1, 0xCCF1: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SpitPoison_Poison50PercentEffect

# >>> factory Peek_SelectEffect
CONTRACT["Peek_SelectEffect"] = {"compare": (), "preserve": ()}
CASES["Peek_SelectEffect"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", 0xC2F1: b"\x00", 0xC2C2: b"\x00", hTemp_ffa0: b"\x00", hAIPkmnPowerEffectParam: b"\x00", 0xCABB: b"\x00", 0xC23C: b"\x00", 0xC2EC: b"\x3F", 0xC400: b"\x08"}, "read": {0xC2C2: 1, hAIPkmnPowerEffectParam: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 30000000, "cycle_budget": 120000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", 0xC2F1: b"\x00", 0xC2C2: b"\x00", hTemp_ffa0: b"\x00", hAIPkmnPowerEffectParam: b"\x00", 0xCABB: b"\x00", 0xC23C: b"\x00", 0xC2EC: b"\x3F", 0xC400: b"\x08"}, read={0xC2C2: 1, hAIPkmnPowerEffectParam: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=30000000, cycle_budget=120000000),
]
# <<< factory Peek_SelectEffect

# >>> factory MagneticStormEffect
CONTRACT["MagneticStormEffect"] = {"compare": (), "preserve": ()}
CASES["MagneticStormEffect"] = [
    {
        "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x10\x00",
                 wPlayerDuelVariables + 0xEF: b"\x01",
                 wPlayerDuelVariables + 0xBB: b"\x00",
                 wPlayerDuelVariables + 0xBC: b"\xFF",
                 0xC2F1: b"\x00",
                 wPlayerDeck: b"\x08\x01",
                 wOpponentDuelVariables + 0xBB: b"\xFF",
                 wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00",
                 wDuelTempList: b"\xAA\xAA"},
        "read": {wDuelTempList: 2, hTempList: 1},
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "keys": [0x00, 0x01],
        "instruction_budget": 20000000, "cycle_budget": 80000000
    },
    {
        "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x10\x10",
                 wPlayerDuelVariables + 0xEF: b"\x01",
                 wPlayerDuelVariables + 0xBB: b"\x00",
                 wPlayerDuelVariables + 0xBC: b"\xFF",
                 0xC2F1: b"\x00",
                 wPlayerDeck: b"\x08\x01",
                 wOpponentDuelVariables + 0xBB: b"\xFF",
                 wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00",
                 wDuelTempList: b"\xAA\xAA"},
        "read": {wDuelTempList: 2, hTempList: 1},
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "keys": [0x00, 0x01],
        "instruction_budget": 20000000, "cycle_budget": 80000000
    },
    dict(POISON,
         wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x10\x10",
               wPlayerDuelVariables + 0xEF: b"\x01",
               wPlayerDuelVariables + 0xBB: b"\x00",
               wPlayerDuelVariables + 0xBC: b"\xFF",
               0xC2F1: b"\x00",
               wPlayerDeck: b"\x08\x01",
               wOpponentDuelVariables + 0xBB: b"\xFF",
               wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00",
               wDuelTempList: b"\xAA\xAA"},
         read={wDuelTempList: 2, hTempList: 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x01],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory MagneticStormEffect

# >>> factory RandomlyDamagePlayAreaPokemon
CONTRACT["RandomlyDamagePlayAreaPokemon"] = {"compare": ("a", "f"), "preserve": ()}
CASES["RandomlyDamagePlayAreaPokemon"] = [
    _rdp_case(b"\x00\x00\x00"),
    _rdp_case(b"\x00\x40\x00"),
    _rdp_case(b"\x00\x00\x00", poison=True),
]
# <<< factory RandomlyDamagePlayAreaPokemon

# >>> factory BigThunderEffect
CONTRACT["BigThunderEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["BigThunderEffect"] = [
    _big_thunder_case(b"\x00\x00\x00"),
    _big_thunder_case(b"\x00\x40\x00"),
    _big_thunder_case(b"\x00\x00\x00", poison=True),
]
# <<< factory BigThunderEffect

# >>> factory EnergySearch_AddToHandEffect
CONTRACT["EnergySearch_AddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EnergySearch_AddToHandEffect"] = [
    {"keys": 0, "wram": {wDuelType: b"\x00", hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x01", 0xC2BA: b"\x3B", 0xC2B9: b"\x01", 0xC201: b"\x00", 0xC2EE: b"\x00", 0xC242: b"\xFF", wDuelDisplayedScreen: b"\x09", 0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00", wLCDC: b"\x00"}, "read": {0xC2BA: 1, 0xC201: 1, 0xC2EE: 1, 0xC242: 1, 0xFFA0: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 3000000, "cycle_budget": 10000000},
    {"wram": {hWhoseTurn: b"\xC2", hTemp_ffa0: b"\xFF", 0xC2BA: b"\x3B", wDuelDisplayedScreen: b"\x09", 0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00", wLCDC: b"\x00"}, "read": {0xFFA0: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 3000000, "cycle_budget": 10000000},
    dict(POISON, wram={wDuelType: b"\x00", hWhoseTurn: b"\xC2", hTemp_ffa0: b"\x01", 0xC2BA: b"\x3B", 0xC2B9: b"\x01", 0xC201: b"\x00", 0xC2EE: b"\x00", 0xC242: b"\xFF", wDuelDisplayedScreen: b"\x09", 0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00", wLCDC: b"\x00"}, read={0xC2BA: 1, 0xC201: 1, 0xC2EE: 1, 0xC242: 1, 0xFFA0: 1}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=3000000, cycle_budget=10000000),
]
# <<< factory EnergySearch_AddToHandEffect

# >>> factory LassEffect
CONTRACT["LassEffect"] = {"compare": (), "preserve": ()}
CASES["LassEffect"] = [
    {"keys": [0x00, 0x01], "wram": {hWhoseTurn: b"\xC2", wDuelType: b"\x00", 0xC2ED: b"\x00", 0xC3ED: b"\x00", hTempCardIndex_ff9f: b"\x00", 0xCABB: b"\x00"}, "read": {hCurSelectionItem: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", wDuelType: b"\x00", 0xC2ED: b"\x00", 0xC3ED: b"\x00", hTempCardIndex_ff9f: b"\x00", 0xCABB: b"\x00"}, read={hCurSelectionItem: 1}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LassEffect

# >>> factory ComputerSearch_DiscardAddToHandEffect
CONTRACT["ComputerSearch_DiscardAddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ComputerSearch_DiscardAddToHandEffect"] = [
    {"b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": 0,
     "wram": {hWhoseTurn: b"\xC2", wDuelType: b"\x00", wDuelDisplayedScreen: b"\x09", wLCDC: b"\x00",
              wNotInDeck: b"\x3B", wDiscardCount: b"\x00", wHandCount: b"\x00"},
     "read": {0xC200: 256, wNotInDeck: 1, wDiscardCount: 1, wHandCount: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 3000000, "cycle_budget": 10000000},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, keys=0,
         wram={hWhoseTurn: b"\xC2", wDuelType: b"\x00", wDuelDisplayedScreen: b"\x09", wLCDC: b"\x00",
               wNotInDeck: b"\x3B", wDiscardCount: b"\x00", wHandCount: b"\x00"},
         read={0xC200: 256, wNotInDeck: 1, wDiscardCount: 1, wHandCount: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=3000000, cycle_budget=10000000),
]
# <<< factory ComputerSearch_DiscardAddToHandEffect

# >>> factory PokeBall_AddToHandEffect
CONTRACT["PokeBall_AddToHandEffect"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PokeBall_AddToHandEffect"] = [
    {},
    dict(POISON),
]
# <<< factory PokeBall_AddToHandEffect

# >>> factory HealPlayAreaCardHP
CONTRACT["HealPlayAreaCardHP"] = {"compare": (), "preserve": ()}
CASES["HealPlayAreaCardHP"] = [
    {"a": 0x14, "wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x20", wPlayerDeck: b"\x08", wLCDC: b"\x00", wAnimationsDisabled: b"\x01", wLoadedAttackAnimation: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "read": {wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: 1, wLoadedAttackAnimation: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x3F", wPlayerDeck: b"\x08", wLCDC: b"\x00", wAnimationsDisabled: b"\x01", wLoadedAttackAnimation: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "read": {wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: 1, wLoadedAttackAnimation: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00", wPlayerDuelVariables + DUELVARS_ARENA_CARD_HP: b"\x10", wPlayerDeck: b"\x08", wLCDC: b"\x00", wAnimationsDisabled: b"\x01", wLoadedAttackAnimation: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], read={wLoadedAttackAnimation: 1}, instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory HealPlayAreaCardHP

# >>> factory Potion_HealEffect
CONTRACT["Potion_HealEffect"] = {"compare": (), "preserve": ()}
CASES["Potion_HealEffect"] = [
    {"a": 0x10, "f": 0x80, "wram": {0xFFA0: b"\x02", 0xFFA1: b"\x14", 0xFF9D: b"\x07", 0xCCB8: b"\x00", 0xCE7E: b"\x01"}, "read": {0xFF9D: 1, 0xCCB8: 1, 0xCE7E: 1}},
    dict(POISON, wram={0xFFA0: b"\x03", 0xFFA1: b"\x01", 0xFF9D: b"\x05", 0xCCB8: b"\x00", 0xCE7E: b"\x01"}, read={0xFF9D: 1, 0xCCB8: 1, 0xCE7E: 1}),
    {"a": 0xFF, "wram": {0xFFA0: b"\x09", 0xFFA1: b"\x00", 0xFF9D: b"\x01", 0xCCB8: b"\xFF", 0xCE7E: b"\xFF"}, "read": {0xFF9D: 1, 0xCCB8: 1, 0xCE7E: 1}},
]
# <<< factory Potion_HealEffect

from tests.cases._schema_migration import legacy_to_schema
# >>> factory CheckIfCardIsBasicEnergy
CONTRACT["CheckIfCardIsBasicEnergy"] = {"compare": ("f",), "preserve": ()}
CASES["CheckIfCardIsBasicEnergy"] = [
	{"a": 0, "wram": {0xFF97: b"\xC2", 0xC27E: b"\x01"}, "read": {0xCC65: 64}},
	{"a": 0xFF, "wram": {0xFF97: b"\xC2", 0xC37D: b"\x01"}, "read": {0xCC65: 64}},
	{"a": 0, "wram": {0xFF97: b"\xC2", 0xC400: b"\x07"},
	 "read": {0xCC65: 1}},
]
# <<< factory CheckIfCardIsBasicEnergy
# >>> factory CopyPlayAreaHPToBackup_Unreferenced
CONTRACT["CopyPlayAreaHPToBackup_Unreferenced"] = {"compare": (), "preserve": ()}
CASES["CopyPlayAreaHPToBackup_Unreferenced"] = [
	{"read": {0xCE76: 6}},
]
# <<< factory CopyPlayAreaHPToBackup_Unreferenced
# >>> factory CopyPlayAreaHPFromBackup_Unreferenced
CONTRACT["CopyPlayAreaHPFromBackup_Unreferenced"] = {"compare": (), "preserve": ()}
CASES["CopyPlayAreaHPFromBackup_Unreferenced"] = [
	{"wram": {0xCE76: b"\x01\x02\x03\x04\x05\x06"}, "read": {0xCE76: 6}},
]
# <<< factory CopyPlayAreaHPFromBackup_Unreferenced
# >>> factory EnergySearch_DeckCheck
CONTRACT["EnergySearch_DeckCheck"] = {"compare": ("f",), "preserve": ()}
CASES["EnergySearch_DeckCheck"] = [
	{"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x00"}},
	{"wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C"}},
]
# <<< factory EnergySearch_DeckCheck
# >>> factory Gale_LoadAnimation
CONTRACT["Gale_LoadAnimation"] = {"compare": (), "preserve": ()}
CASES["Gale_LoadAnimation"] = [
	{"wram": {0xCCB8: b"\x00"}, "read": {0xCCB8: 1}},
	{"wram": {0xCCB8: b"\xFF"}, "read": {0xCCB8: 1}},
]
# <<< factory Gale_LoadAnimation
# >>> factory CreatePlayableStage2PokemonCardListFromHand
CONTRACT["CreatePlayableStage2PokemonCardListFromHand"] = {"compare": ("f",), "preserve": ()}
CASES["CreatePlayableStage2PokemonCardListFromHand"] = [
	{"read": {0xC100: 1}},
	{"wram": {0xC100: b"\xFF"}, "read": {0xC100: 1}},
]
# <<< factory CreatePlayableStage2PokemonCardListFromHand

# >>> factory MixUpEffect
CONTRACT["MixUpEffect"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["MixUpEffect"] = [
	dict(POISON,
	     wram={0xC510: b"\xFF"},
	     keys=[0x00, 0x01],
	     setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
	     instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory MixUpEffect

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {}

# >>> factory-mutation MixUpEffect
MUTATIONS["MixUpEffect"] = {
	"source_symbol": "MixUpEffect",
	"before": "gb_write8(hCurSelectionItem_ADDR, count);",
	"after": "gb_write8(hCurSelectionItem_ADDR, (uint8_t)(count + 1u));",
	"case_ids": ["MixUpEffect-0"],
}
# <<< factory-mutation MixUpEffect

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
    "before": "void DodrioRage_DamageBoostEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage(r.a);\n}",
    "after": "void DodrioRage_DamageBoostEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage((uint8_t)(r.a + 1u));\n}",
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
# >>> factory-mutation Func_2c6d9
MUTATIONS["Func_2c6d9"] = {
    "source_symbol": "Func_2c6d9",
    "before": "return DrawWideTextBox_WaitForInput(0x0031u);",
    "after": "return (WaitResult){0x00u};",
    "case_ids": ["Func_2c6d9-0", "Func_2c6d9-1"],
}
# <<< factory-mutation Func_2c6d9
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
    "before": "uint8_t ClairvoyanceEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t ClairvoyanceEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x00u);\n}",
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
    "before": "void PoisonWhip_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);\n}",
    "after": "void PoisonWhip_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(11u, 10u, 10u);\n}",
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
# >>> factory-mutation Barrier_CheckEnergy
MUTATIONS["Barrier_CheckEnergy"] = {"source_symbol": "Barrier_CheckEnergy", "before": "#define NotEnoughPsychicEnergyText 0x00c2u", "after": "#define NotEnoughPsychicEnergyText 0x00c3u", "case_ids": ["Barrier_CheckEnergy-0", "Barrier_CheckEnergy-1"]}
# <<< factory-mutation Barrier_CheckEnergy
# >>> factory-mutation ResetDevolvedCardStatus
MUTATIONS["ResetDevolvedCardStatus"] = {
    "source_symbol": "ResetDevolvedCardStatus",
    "before": "return (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location);",
    "after": "return (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location + 1u);",
    "case_ids": ["ResetDevolvedCardStatus-0", "ResetDevolvedCardStatus-1",
                 "ResetDevolvedCardStatus-2", "ResetDevolvedCardStatus-3"],
}
# <<< factory-mutation ResetDevolvedCardStatus
# >>> factory-mutation EeveeQuickAttack_AIEffect
MUTATIONS["EeveeQuickAttack_AIEffect"] = {
    "source_symbol": "EeveeQuickAttack_AIEffect",
    "before": "SetExpectedAIDamage(20u, 10u, 30u);",
    "after": "SetExpectedAIDamage(21u, 10u, 30u);",
    "case_ids": ["EeveeQuickAttack_AIEffect-0", "EeveeQuickAttack_AIEffect-1"],
}
# <<< factory-mutation EeveeQuickAttack_AIEffect
# >>> factory-mutation MirrorMove_AIEffect
MUTATIONS["MirrorMove_AIEffect"] = {
    "source_symbol": "MirrorMove_AIEffect",
    "before": "wAIMaxDamage = wAIMinDamage;",
    "after": "wAIMaxDamage = (uint8_t)(wAIMinDamage + 1u);",
    "case_ids": ["MirrorMove_AIEffect-0", "MirrorMove_AIEffect-1"],
}
# <<< factory-mutation MirrorMove_AIEffect
# >>> factory-mutation MirrorMove_InitialEffect1
MUTATIONS["MirrorMove_InitialEffect1"] = {
    "source_symbol": "MirrorMove_InitialEffect1",
    "before": "return (MirrorMoveInitialEffect1Result){0x90u, 0x00C6u};",
    "after": "return (MirrorMoveInitialEffect1Result){0x90u, 0x00C7u};",
    "case_ids": ["MirrorMove_InitialEffect1-0", "MirrorMove_InitialEffect1-5"],
}
# <<< factory-mutation MirrorMove_InitialEffect1
# >>> factory-mutation FuryAttack_AIEffect
MUTATIONS["FuryAttack_AIEffect"] = {
    "source_symbol": "FuryAttack_AIEffect",
    "before": "SetExpectedAIDamage(10u, 0u, 20u);",
    "after": "SetExpectedAIDamage(11u, 0u, 20u);",
    "case_ids": ["FuryAttack_AIEffect-0", "FuryAttack_AIEffect-1"],
}
# <<< factory-mutation FuryAttack_AIEffect
# >>> factory-mutation RetreatAidEffect
MUTATIONS["RetreatAidEffect"] = {
    "source_symbol": "RetreatAidEffect",
    "before": "uint8_t RetreatAidEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t RetreatAidEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x20u);\n}",
    "case_ids": ["RetreatAidEffect-0", "RetreatAidEffect-1", "RetreatAidEffect-2"],
}
# <<< factory-mutation RetreatAidEffect
# >>> factory-mutation FriendshipSong_BenchCheck
MUTATIONS["FriendshipSong_BenchCheck"] = {
    "source_symbol": "FriendshipSong_BenchCheck",
    "before": "count.a >= 6u",
    "after": "count.a > 6u",
    "case_ids": ["FriendshipSong_BenchCheck-2"],
}
# <<< factory-mutation FriendshipSong_BenchCheck
# >>> factory-mutation ExpandEffect
MUTATIONS["ExpandEffect"] = {
    "source_symbol": "ExpandEffect",
    "before": "\t(void)ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_10);",
    "after": "\t(void)ApplySubstatus1ToAttackingCard((uint8_t)(SUBSTATUS1_REDUCE_BY_10 + 1u));",
    "case_ids": ["ExpandEffect-0", "ExpandEffect-1"],
}
# <<< factory-mutation ExpandEffect
# >>> factory-mutation CheckIfThereAreAnyEnergyCardsAttached
MUTATIONS["CheckIfThereAreAnyEnergyCardsAttached"] = {
    "source_symbol": "CheckIfThereAreAnyEnergyCardsAttached",
    "before": "return (CheckIfThereAreAnyEnergyCardsAttachedResult){0x00u};",
    "after": "return (CheckIfThereAreAnyEnergyCardsAttachedResult){0x90u};",
    "case_ids": ["CheckIfThereAreAnyEnergyCardsAttached-1"],
}
# <<< factory-mutation CheckIfThereAreAnyEnergyCardsAttached
# >>> factory-mutation PokeBall_DeckCheck
MUTATIONS["PokeBall_DeckCheck"] = {"source_symbol": "PokeBall_DeckCheck", "before": "if (!borrow)", "after": "if (borrow)", "case_ids": ["PokeBall_DeckCheck-0", "PokeBall_DeckCheck-1", "PokeBall_DeckCheck-2", "PokeBall_DeckCheck-3"]}
# <<< factory-mutation PokeBall_DeckCheck
# >>> factory-mutation Recycle_DiscardPileCheck
MUTATIONS["Recycle_DiscardPileCheck"] = {"source_symbol": "Recycle_DiscardPileCheck", "before": "if (borrow)", "after": "if (!borrow)", "case_ids": ["Recycle_DiscardPileCheck-0", "Recycle_DiscardPileCheck-1", "Recycle_DiscardPileCheck-2", "Recycle_DiscardPileCheck-3"]}
# <<< factory-mutation Recycle_DiscardPileCheck
# >>> factory-mutation CreateBasicPokemonCardListFromDiscardPile
MUTATIONS["CreateBasicPokemonCardListFromDiscardPile"] = {
    "source_symbol": "CreateBasicPokemonCardListFromDiscardPile",
    "before": "return (CreateBasicPokemonCardListFromDiscardPileResult){0x90u};",
    "after": "return (CreateBasicPokemonCardListFromDiscardPileResult){0x80u};",
    "case_ids": ["CreateBasicPokemonCardListFromDiscardPile-0", "CreateBasicPokemonCardListFromDiscardPile-1", "CreateBasicPokemonCardListFromDiscardPile-2"],
}
# <<< factory-mutation CreateBasicPokemonCardListFromDiscardPile
# >>> factory-mutation CreatePokemonCardListFromHand
MUTATIONS["CreatePokemonCardListFromHand"] = {"source_symbol": "CreatePokemonCardListFromHand", "before": "if (gb_read8(wLoadedCard2Type_ADDR) < TYPE_ENERGY)", "after": "if (gb_read8(wLoadedCard2Type_ADDR) >= TYPE_ENERGY)", "case_ids": ["CreatePokemonCardListFromHand-0", "CreatePokemonCardListFromHand-1"]}
# <<< factory-mutation CreatePokemonCardListFromHand
# >>> factory-mutation Pokedex_DeckCheck
MUTATIONS["Pokedex_DeckCheck"] = {"source_symbol": "Pokedex_DeckCheck", "before": "uint8_t f = (count < DECK_SIZE) ? 0x00u : (uint8_t)(count == DECK_SIZE ? 0x90u : 0x10u);", "after": "uint8_t f = (count >= DECK_SIZE) ? 0x00u : (uint8_t)(count == DECK_SIZE ? 0x90u : 0x10u);", "case_ids": ["Pokedex_DeckCheck-0", "Pokedex_DeckCheck-1"]}
# <<< factory-mutation Pokedex_DeckCheck
# >>> factory-mutation Pokedex_OrderDeckCardsEffect
MUTATIONS["Pokedex_OrderDeckCardsEffect"] = {
    "source_symbol": "Pokedex_OrderDeckCardsEffect",
    "before": "c = (uint8_t)(c + 1u);",
    "after": "c = (uint8_t)(c + 2u);",
    "case_ids": ["Pokedex_OrderDeckCardsEffect-0", "Pokedex_OrderDeckCardsEffect-1"],
}
# <<< factory-mutation Pokedex_OrderDeckCardsEffect
# >>> factory-mutation Maintenance_HandCheck
MUTATIONS["Maintenance_HandCheck"] = {
    "source_symbol": "Maintenance_HandCheck",
    "before": "if (result == 0u)",
    "after": "if (result != 0u)",
    "case_ids": ["Maintenance_HandCheck-0", "Maintenance_HandCheck-1", "Maintenance_HandCheck-2"],
}
# <<< factory-mutation Maintenance_HandCheck
# >>> factory-mutation DevolutionSpray_PlayAreaEvolutionCheck
MUTATIONS["DevolutionSpray_PlayAreaEvolutionCheck"] = {
    "source_symbol": "DevolutionSpray_PlayAreaEvolutionCheck",
    "before": "gb_read8(wLoadedCard2Stage_ADDR) != 0u",
    "after": "gb_read8(wLoadedCard2Stage_ADDR) == 0u",
    "case_ids": ["DevolutionSpray_PlayAreaEvolutionCheck-0", "DevolutionSpray_PlayAreaEvolutionCheck-1", "DevolutionSpray_PlayAreaEvolutionCheck-2"],
}
# <<< factory-mutation DevolutionSpray_PlayAreaEvolutionCheck
# >>> factory-mutation SpitPoison_AIEffect
MUTATIONS["SpitPoison_AIEffect"] = {
    "source_symbol": "SpitPoison_AIEffect",
    "before": "SetExpectedAIDamage(5u, 0u, 10u);",
    "after": "SetExpectedAIDamage(6u, 0u, 10u);",
    "case_ids": ["SpitPoison_AIEffect-0", "SpitPoison_AIEffect-1", "SpitPoison_AIEffect-2"],
}
# <<< factory-mutation SpitPoison_AIEffect
# >>> factory-mutation GloomPoisonPowder_AIEffect
MUTATIONS["GloomPoisonPowder_AIEffect"] = {
    "source_symbol": "GloomPoisonPowder_AIEffect",
    "before": "void GloomPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);\n}",
    "after": "void GloomPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(11u, 10u, 10u);\n}",
    "case_ids": ["GloomPoisonPowder_AIEffect-0"],
}
# <<< factory-mutation GloomPoisonPowder_AIEffect
# >>> factory-mutation FoulOdorEffect
MUTATIONS["FoulOdorEffect"] = {
    "source_symbol": "FoulOdorEffect",
    "before": "\tSwapTurn();\n\treturn r;",
    "after": "\treturn r;",
    "case_ids": ["FoulOdorEffect-0", "FoulOdorEffect-1", "FoulOdorEffect-2"],
}
# <<< factory-mutation FoulOdorEffect
# >>> factory-mutation KakunaPoisonPowder_AIEffect
MUTATIONS["KakunaPoisonPowder_AIEffect"] = {
    "source_symbol": "KakunaPoisonPowder_AIEffect",
    "before": "void KakunaPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void KakunaPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}",
    "case_ids": ["KakunaPoisonPowder_AIEffect-0", "KakunaPoisonPowder_AIEffect-1"],
}
# <<< factory-mutation KakunaPoisonPowder_AIEffect
# >>> factory-mutation SwordsDanceEffect
MUTATIONS["SwordsDanceEffect"] = {
    "source_symbol": "SwordsDanceEffect",
    "before": "if (gb_read8(0xCCC3u) != 0x2Eu)",
    "after": "if (gb_read8(0xCCC3u) == 0x2Eu)",
    "case_ids": ["SwordsDanceEffect-0", "SwordsDanceEffect-1", "SwordsDanceEffect-2"],
}
# <<< factory-mutation SwordsDanceEffect
# >>> factory-mutation Twineedle_AIEffect
MUTATIONS["Twineedle_AIEffect"] = {
    "source_symbol": "Twineedle_AIEffect",
    "before": "void Twineedle_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}",
    "after": "void Twineedle_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}",
    "case_ids": ["Twineedle_AIEffect-0", "Twineedle_AIEffect-1", "Twineedle_AIEffect-2"],
}
# <<< factory-mutation Twineedle_AIEffect
# >>> factory-mutation BeedrillPoisonSting_AIEffect
MUTATIONS["BeedrillPoisonSting_AIEffect"] = {
    "source_symbol": "BeedrillPoisonSting_AIEffect",
    "before": "void BeedrillPoisonSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void BeedrillPoisonSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}",
    "case_ids": ["BeedrillPoisonSting_AIEffect-0", "BeedrillPoisonSting_AIEffect-1", "BeedrillPoisonSting_AIEffect-2", "BeedrillPoisonSting_AIEffect-3", "BeedrillPoisonSting_AIEffect-4"],
}
# <<< factory-mutation BeedrillPoisonSting_AIEffect
# >>> factory-mutation FoulGas_AIEffect
MUTATIONS["FoulGas_AIEffect"] = {
    "source_symbol": "FoulGas_AIEffect",
    "before": "UpdateExpectedAIDamage(5u, 0u, 10u);",
    "after": "UpdateExpectedAIDamage(6u, 0u, 10u);",
    "case_ids": ["FoulGas_AIEffect-0", "FoulGas_AIEffect-1", "FoulGas_AIEffect-2"],
}
# <<< factory-mutation FoulGas_AIEffect
# >>> factory-mutation Sprout_AISelectEffect
MUTATIONS["Sprout_AISelectEffect"] = {
    "source_symbol": "Sprout_AISelectEffect",
    "before": "if ((uint8_t)GetCardIDFromDeckIndex(card) == ODDISH)",
    "after": "if ((uint8_t)GetCardIDFromDeckIndex(card) != ODDISH)",
    "case_ids": ["Sprout_AISelectEffect-0", "Sprout_AISelectEffect-1", "Sprout_AISelectEffect-2"],
}
# <<< factory-mutation Sprout_AISelectEffect
# >>> factory-mutation Teleport_CheckBench
MUTATIONS["Teleport_CheckBench"] = {"source_symbol": "Teleport_CheckBench", "before": "if (count.a == 2u)", "after": "if (count.a == 3u)", "case_ids": ["Teleport_CheckBench-2"]}
# <<< factory-mutation Teleport_CheckBench
# >>> factory-mutation Teleport_AISelectEffect
MUTATIONS["Teleport_AISelectEffect"] = {"source_symbol": "Teleport_AISelectEffect", "before": "hTemp_ffa0 = a;", "after": "hTemp_ffa0 = (uint8_t)(a + 1u);", "case_ids": ["Teleport_AISelectEffect-1"]}
# <<< factory-mutation Teleport_AISelectEffect
# >>> factory-mutation HornHazard_AIEffect
MUTATIONS["HornHazard_AIEffect"] = {
    "source_symbol": "HornHazard_AIEffect",
    "before": "void HornHazard_AIEffect(void)\n{\n\tSetExpectedAIDamage(15u, 0u, 30u);\n}",
    "after": "void HornHazard_AIEffect(void)\n{\n\tSetExpectedAIDamage(16u, 0u, 30u);\n}",
    "case_ids": ["HornHazard_AIEffect-0", "HornHazard_AIEffect-1", "HornHazard_AIEffect-2"],
}
# <<< factory-mutation HornHazard_AIEffect
# >>> factory-mutation NidorinaDoubleKick_AIEffect
MUTATIONS["NidorinaDoubleKick_AIEffect"] = {
    "source_symbol": "NidorinaDoubleKick_AIEffect",
    "before": "void NidorinaDoubleKick_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}",
    "after": "void NidorinaDoubleKick_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}",
    "case_ids": ["NidorinaDoubleKick_AIEffect-0", "NidorinaDoubleKick_AIEffect-1", "NidorinaDoubleKick_AIEffect-2"],
}
# <<< factory-mutation NidorinaDoubleKick_AIEffect
# >>> factory-mutation NidorinoDoubleKick_AIEffect
MUTATIONS["NidorinoDoubleKick_AIEffect"] = {"source_symbol": "NidorinoDoubleKick_AIEffect", "before": "void NidorinoDoubleKick_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}", "after": "void NidorinoDoubleKick_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}", "case_ids": ["NidorinoDoubleKick_AIEffect-0", "NidorinoDoubleKick_AIEffect-1", "NidorinoDoubleKick_AIEffect-2"]}
# <<< factory-mutation NidorinoDoubleKick_AIEffect
# >>> factory-mutation WeedlePoisonSting_AIEffect
MUTATIONS["WeedlePoisonSting_AIEffect"] = {"source_symbol": "WeedlePoisonSting_AIEffect", "before": "void WeedlePoisonSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}", "after": "void WeedlePoisonSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}", "case_ids": ["WeedlePoisonSting_AIEffect-0", "WeedlePoisonSting_AIEffect-1", "WeedlePoisonSting_AIEffect-2", "WeedlePoisonSting_AIEffect-3", "WeedlePoisonSting_AIEffect-4"]}
# <<< factory-mutation WeedlePoisonSting_AIEffect
# >>> factory-mutation BellsproutCallForFamily_AISelectEffect
MUTATIONS["BellsproutCallForFamily_AISelectEffect"] = {
    "source_symbol": "BellsproutCallForFamily_AISelectEffect",
    "before": "if ((uint8_t)GetCardIDFromDeckIndex(card) == BELLSPROUT)",
    "after": "if ((uint8_t)GetCardIDFromDeckIndex(card) != BELLSPROUT)",
    "case_ids": ["BellsproutCallForFamily_AISelectEffect-0", "BellsproutCallForFamily_AISelectEffect-1", "BellsproutCallForFamily_AISelectEffect-2"],
}
# <<< factory-mutation BellsproutCallForFamily_AISelectEffect
# >>> factory-mutation WeezingSmog_AIEffect
MUTATIONS["WeezingSmog_AIEffect"] = {
    "source_symbol": "WeezingSmog_AIEffect",
    "before": "void WeezingSmog_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);",
    "after": "void WeezingSmog_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);",
    "case_ids": ["WeezingSmog_AIEffect-0", "WeezingSmog_AIEffect-1", "WeezingSmog_AIEffect-2"],
}
# <<< factory-mutation WeezingSmog_AIEffect
# >>> factory-mutation NidoranFFurySwipes_AIEffect
MUTATIONS["NidoranFFurySwipes_AIEffect"] = {"source_symbol": "NidoranFFurySwipes_AIEffect", "before": "SetExpectedAIDamage(30u / 2u, 0u, 30u);", "after": "SetExpectedAIDamage(16u, 0u, 30u);", "case_ids": ["NidoranFFurySwipes_AIEffect-0", "NidoranFFurySwipes_AIEffect-1"]}
# <<< factory-mutation NidoranFFurySwipes_AIEffect
# >>> factory-mutation NidoranFCallForFamily_AISelectEffect
MUTATIONS["NidoranFCallForFamily_AISelectEffect"] = {"source_symbol": "NidoranFCallForFamily_AISelectEffect", "before": "if ((uint8_t)card_id == NIDORANF || (uint8_t)card_id == NIDORANM)", "after": "if ((uint8_t)card_id != NIDORANF || (uint8_t)card_id == NIDORANM)", "case_ids": ["NidoranFCallForFamily_AISelectEffect-0", "NidoranFCallForFamily_AISelectEffect-1"]}
# <<< factory-mutation NidoranFCallForFamily_AISelectEffect
# >>> factory-mutation ToxicGasEffect
MUTATIONS["ToxicGasEffect"] = {
    "source_symbol": "ToxicGasEffect",
    "before": "uint8_t ToxicGasEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t ToxicGasEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x20u);\n}",
    "case_ids": ["ToxicGasEffect-0", "ToxicGasEffect-1", "ToxicGasEffect-2"],
}
# <<< factory-mutation ToxicGasEffect
# >>> factory-mutation Sludge_AIEffect
MUTATIONS["Sludge_AIEffect"] = {
    "source_symbol": "Sludge_AIEffect",
    "before": "void Sludge_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void Sludge_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}",
    "case_ids": ["Sludge_AIEffect-0", "Sludge_AIEffect-1", "Sludge_AIEffect-2"],
}
# <<< factory-mutation Sludge_AIEffect
# >>> factory-mutation KadabraRecover_DiscardEffect
MUTATIONS["KadabraRecover_DiscardEffect"] = {"source_symbol": "KadabraRecover_DiscardEffect", "before": "\tuint8_t a = hTemp_ffa0;", "after": "\tuint8_t a = 0u;", "case_ids": ["KadabraRecover_DiscardEffect-1", "KadabraRecover_DiscardEffect-2"]}
# <<< factory-mutation KadabraRecover_DiscardEffect
# >>> factory-mutation PrimeapeFurySwipes_AIEffect
MUTATIONS["PrimeapeFurySwipes_AIEffect"] = {"source_symbol": "PrimeapeFurySwipes_AIEffect", "before": "return (PrimeapeFurySwipesAIResult){0x3cu, 0x80u, 0x00u, 0x3cu};", "after": "return (PrimeapeFurySwipesAIResult){0x1eu, 0x80u, 0x00u, 0x3cu};", "case_ids": ["PrimeapeFurySwipes_AIEffect-0", "PrimeapeFurySwipes_AIEffect-1", "PrimeapeFurySwipes_AIEffect-2"]}
# <<< factory-mutation PrimeapeFurySwipes_AIEffect
# >>> factory-mutation StretchKick_CheckBench
MUTATIONS["StretchKick_CheckBench"] = {"source_symbol": "StretchKick_CheckBench", "before": "\treturn (StretchKickCheckBenchResult){r.a, f, EffectNoPokemonOnTheBenchText};", "after": "\treturn (StretchKickCheckBenchResult){r.a, f, 0x00b8u};", "case_ids": ["StretchKick_CheckBench-0", "StretchKick_CheckBench-1", "StretchKick_CheckBench-2", "StretchKick_CheckBench-3", "StretchKick_CheckBench-4"]}
# <<< factory-mutation StretchKick_CheckBench
# >>> factory-mutation LightScreenEffect
MUTATIONS["LightScreenEffect"] = {"source_symbol": "LightScreenEffect", "before": "\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_HALVE_DAMAGE);", "after": "\treturn (uint16_t)(ApplySubstatus1ToAttackingCard(SUBSTATUS1_HALVE_DAMAGE) + 1u);", "case_ids": ["LightScreenEffect-0", "LightScreenEffect-1"]}
# <<< factory-mutation LightScreenEffect


# >>> factory-mutation StarmieRecover_CheckEnergyHP
MUTATIONS["StarmieRecover_CheckEnergyHP"] = {"source_symbol": "StarmieRecover_CheckEnergyHP", "before": "\tenergy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER));", "after": "\tenergy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER + 1u));", "case_ids": ["StarmieRecover_CheckEnergyHP-2", "StarmieRecover_CheckEnergyHP-3", "StarmieRecover_CheckEnergyHP-4"]}
# <<< factory-mutation StarmieRecover_CheckEnergyHP

# >>> factory-mutation StarmieRecover_DiscardEffect
MUTATIONS["StarmieRecover_DiscardEffect"] = {"source_symbol": "StarmieRecover_DiscardEffect", "before": "\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR));", "after": "\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR + 1u));", "case_ids": ["StarmieRecover_DiscardEffect-1", "StarmieRecover_DiscardEffect-2"]}
# <<< factory-mutation StarmieRecover_DiscardEffect

# >>> factory-mutation Cowardice_CheckUseAndBench
MUTATIONS["Cowardice_CheckUseAndBench"] = {"source_symbol": "Cowardice_CheckUseAndBench", "before": "return (CowardiceCheckUseAndBenchResult){0x70u, EffectNoPokemonOnTheBenchText};", "after": "return (CowardiceCheckUseAndBenchResult){0x71u, EffectNoPokemonOnTheBenchText};", "case_ids": ["Cowardice_CheckUseAndBench-0"]}
# <<< factory-mutation Cowardice_CheckUseAndBench

# >>> factory-mutation Cowardice_ReturnToHandEffect
MUTATIONS["Cowardice_ReturnToHandEffect"] = {"source_symbol": "Cowardice_ReturnToHandEffect", "before": "\t(void)ShiftAllPokemonToFirstPlayAreaSlots();\n\twDuelDisplayedScreen = 0u;", "after": "\t(void)ShiftAllPokemonToFirstPlayAreaSlots();\n\twDuelDisplayedScreen = 1u;", "case_ids": ["Cowardice_ReturnToHandEffect-0"]}
# <<< factory-mutation Cowardice_ReturnToHandEffect
# >>> factory-mutation CheckIfCardHasGrassEnergyAttached
MUTATIONS["CheckIfCardHasGrassEnergyAttached"] = {
    "source_symbol": "CheckIfCardHasGrassEnergyAttached",
    "before": "if (GetCardType(card_id) != TYPE_ENERGY_GRASS)",
    "after": "if (GetCardType(card_id) == TYPE_ENERGY_GRASS)",
    "case_ids": ["CheckIfCardHasGrassEnergyAttached-0", "CheckIfCardHasGrassEnergyAttached-1", "CheckIfCardHasGrassEnergyAttached-2"],
}
# <<< factory-mutation CheckIfCardHasGrassEnergyAttached
# >>> factory-mutation GrimerMinimizeEffect
MUTATIONS["GrimerMinimizeEffect"] = {
    "source_symbol": "GrimerMinimizeEffect",
    "before": "uint16_t GrimerMinimizeEffect(void)\n{\n\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_20);\n}",
    "after": "uint16_t GrimerMinimizeEffect(void)\n{\n\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_10);\n}",
    "case_ids": ["GrimerMinimizeEffect-0", "GrimerMinimizeEffect-1", "GrimerMinimizeEffect-2"],
}
# <<< factory-mutation GrimerMinimizeEffect
# >>> factory-mutation Quickfreeze_InitialEffect
MUTATIONS["Quickfreeze_InitialEffect"] = {
    "source_symbol": "Quickfreeze_InitialEffect",
    "before": "uint8_t Quickfreeze_InitialEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t Quickfreeze_InitialEffect(uint8_t f)\n{\n\treturn (uint8_t)(f & 0x80u);\n}",
    "case_ids": ["Quickfreeze_InitialEffect-0", "Quickfreeze_InitialEffect-1", "Quickfreeze_InitialEffect-2"],
}
# <<< factory-mutation Quickfreeze_InitialEffect
# >>> factory-mutation FocusEnergyEffect
MUTATIONS["FocusEnergyEffect"] = {
    "source_symbol": "FocusEnergyEffect",
    "before": "if (gb_read8(0xCCC3u) != 0x5Au)",
    "after": "if (gb_read8(0xCCC3u) == 0x5Au)",
    "case_ids": ["FocusEnergyEffect-0", "FocusEnergyEffect-1", "FocusEnergyEffect-2"],
}
# <<< factory-mutation FocusEnergyEffect
# >>> factory-mutation MagnetonSonicboom_UnaffectedByColorEffect
MUTATIONS["MagnetonSonicboom_UnaffectedByColorEffect"] = {"source_symbol": "MagnetonSonicboom_UnaffectedByColorEffect", "before": "(uint8_t)(1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)", "after": "(uint8_t)(1u << (UNAFFECTED_BY_WEAKNESS_RESISTANCE_F - 1u))", "case_ids": ["MagnetonSonicboom_UnaffectedByColorEffect-0", "MagnetonSonicboom_UnaffectedByColorEffect-1"]}
# <<< factory-mutation MagnetonSonicboom_UnaffectedByColorEffect
# >>> factory-mutation MagnetonSonicboom_NullEffect
MUTATIONS["MagnetonSonicboom_NullEffect"] = {"source_symbol": "MagnetonSonicboom_NullEffect", "before": "\t/* null effect */", "after": "\tgb_write8(0xC100u, 1u);", "case_ids": ["MagnetonSonicboom_NullEffect-0", "MagnetonSonicboom_NullEffect-1"]}
# <<< factory-mutation MagnetonSonicboom_NullEffect
# >>> factory-mutation ElectrodeSonicboom_UnaffectedByColorEffect
MUTATIONS["ElectrodeSonicboom_UnaffectedByColorEffect"] = {"source_symbol": "ElectrodeSonicboom_UnaffectedByColorEffect", "before": "\tgb_write8(hl, (uint8_t)(value | (uint8_t)(1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)));", "after": "\tgb_write8(hl, (uint8_t)(value & (uint8_t)~(1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)));", "case_ids": ["ElectrodeSonicboom_UnaffectedByColorEffect-0", "ElectrodeSonicboom_UnaffectedByColorEffect-1", "ElectrodeSonicboom_UnaffectedByColorEffect-2"]}
# <<< factory-mutation ElectrodeSonicboom_UnaffectedByColorEffect
# >>> factory-mutation EnergySpike_AISelectEffect
MUTATIONS["EnergySpike_AISelectEffect"] = {"source_symbol": "EnergySpike_AISelectEffect", "before": "hTemp_ffa0 = 0xffu;", "after": "hTemp_ffa0 = 0xfeu;", "case_ids": ["EnergySpike_AISelectEffect-0", "EnergySpike_AISelectEffect-1"]}
# <<< factory-mutation EnergySpike_AISelectEffect
# >>> factory-mutation CometPunch_AIEffect
MUTATIONS["CometPunch_AIEffect"] = {"source_symbol": "CometPunch_AIEffect", "before": "SetExpectedAIDamage(0x28u, 0x00u, 0x50u);", "after": "SetExpectedAIDamage(0x27u, 0x00u, 0x50u);", "case_ids": ["CometPunch_AIEffect-0", "CometPunch_AIEffect-1", "CometPunch_AIEffect-2"]}
# <<< factory-mutation CometPunch_AIEffect
# >>> factory-mutation Conversion1_WeaknessCheck
MUTATIONS["Conversion1_WeaknessCheck"] = {"source_symbol": "Conversion1_WeaknessCheck", "before": "if (weakness == 0u)", "after": "if (weakness == 1u)", "case_ids": ["Conversion1_WeaknessCheck-0", "Conversion1_WeaknessCheck-1", "Conversion1_WeaknessCheck-2", "Conversion1_WeaknessCheck-3"]}
# <<< factory-mutation Conversion1_WeaknessCheck
# >>> factory-mutation Conversion2_ResistanceCheck
MUTATIONS["Conversion2_ResistanceCheck"] = {"source_symbol": "Conversion2_ResistanceCheck", "before": "if (resistance == 0u)", "after": "if (resistance == 1u)", "case_ids": ["Conversion2_ResistanceCheck-0", "Conversion2_ResistanceCheck-1", "Conversion2_ResistanceCheck-2", "Conversion2_ResistanceCheck-3"]}
# <<< factory-mutation Conversion2_ResistanceCheck
# >>> factory-mutation ElectrodeSonicboom_NullEffect
MUTATIONS["ElectrodeSonicboom_NullEffect"] = {"source_symbol": "ElectrodeSonicboom_NullEffect", "before": "\thTemp_ffa0 = null_effect_value;", "after": "\thTemp_ffa0 = 0u;", "case_ids": ["ElectrodeSonicboom_NullEffect-1", "ElectrodeSonicboom_NullEffect-2"]}
# <<< factory-mutation ElectrodeSonicboom_NullEffect
# >>> factory-mutation FirstAid_DamageCheck
MUTATIONS["FirstAid_DamageCheck"] = {"source_symbol": "FirstAid_DamageCheck", "before": "return (FirstAidDamageCheckResult){NoDamageCountersText, flags};", "after": "return (FirstAidDamageCheckResult){(uint16_t)(NoDamageCountersText + 1u), flags};", "case_ids": ["FirstAid_DamageCheck-0", "FirstAid_DamageCheck-1"]}
# <<< factory-mutation FirstAid_DamageCheck
# >>> factory-mutation DoTheWaveEffect
MUTATIONS["DoTheWaveEffect"] = {"source_symbol": "DoTheWaveEffect", "before": "\tuint8_t amount = ATimes10((uint8_t)(r.a - 1u));", "after": "\tuint8_t amount = ATimes10((uint8_t)(r.a - 2u));", "case_ids": ["DoTheWaveEffect-0", "DoTheWaveEffect-1", "DoTheWaveEffect-2", "DoTheWaveEffect-3"]}
# <<< factory-mutation DoTheWaveEffect
# >>> factory-mutation FullHeal_StatusCheck
MUTATIONS["FullHeal_StatusCheck"] = {"source_symbol": "FullHeal_StatusCheck", "before": "if (status != 0u)", "after": "if (status == 0u)", "case_ids": ["FullHeal_StatusCheck-0", "FullHeal_StatusCheck-1", "FullHeal_StatusCheck-2"]}
# <<< factory-mutation FullHeal_StatusCheck
# >>> factory-mutation PoisonFang_AIEffect
MUTATIONS["PoisonFang_AIEffect"] = {
    "source_symbol": "PoisonFang_AIEffect",
    "before": "void PoisonFang_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);\n}",
    "after": "void PoisonFang_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(11u, 10u, 10u);\n}",
    "case_ids": ["PoisonFang_AIEffect-0", "PoisonFang_AIEffect-1"],
}
# <<< factory-mutation PoisonFang_AIEffect
# >>> factory-mutation WeepinbellPoisonPowder_AIEffect
MUTATIONS["WeepinbellPoisonPowder_AIEffect"] = {
    "source_symbol": "WeepinbellPoisonPowder_AIEffect",
    "before": "void WeepinbellPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void WeepinbellPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}",
    "case_ids": ["WeepinbellPoisonPowder_AIEffect-0", "WeepinbellPoisonPowder_AIEffect-1"],
}
# <<< factory-mutation WeepinbellPoisonPowder_AIEffect
# >>> factory-mutation Toxic_AIEffect
MUTATIONS["Toxic_AIEffect"] = {"source_symbol": "Toxic_AIEffect", "before": "UpdateExpectedAIDamage(20u, 20u, 20u);", "after": "UpdateExpectedAIDamage(21u, 20u, 20u);", "case_ids": ["Toxic_AIEffect-0", "Toxic_AIEffect-1", "Toxic_AIEffect-2"]}
# <<< factory-mutation Toxic_AIEffect
# >>> factory-mutation BoyfriendsEffect
MUTATIONS["BoyfriendsEffect"] = {"source_symbol": "BoyfriendsEffect", "before": "AddToDamage(ATimes10((uint8_t)(c << 1)));", "after": "AddToDamage(ATimes10((uint8_t)(c << 1)) + 1u);", "case_ids": ["BoyfriendsEffect-0", "BoyfriendsEffect-1"]}
# <<< factory-mutation BoyfriendsEffect
# >>> factory-mutation IvysaurPoisonPowder_AIEffect
MUTATIONS["IvysaurPoisonPowder_AIEffect"] = {
    "source_symbol": "IvysaurPoisonPowder_AIEffect",
    "before": "void IvysaurPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);",
    "after": "void IvysaurPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(9u, 10u, 10u);",
    "case_ids": ["IvysaurPoisonPowder_AIEffect-0", "IvysaurPoisonPowder_AIEffect-1"],
}
# <<< factory-mutation IvysaurPoisonPowder_AIEffect
# >>> factory-mutation EnergyTrans_CheckPlayArea
MUTATIONS["EnergyTrans_CheckPlayArea"] = {
    "source_symbol": "EnergyTrans_CheckPlayArea",
    "before": "return (EnergyTransCheckPlayAreaResult){DECK_SIZE, 0x90u, NoGrassEnergyText, 0u};",
    "after": "return (EnergyTransCheckPlayAreaResult){DECK_SIZE, 0x90u, (uint16_t)(NoGrassEnergyText + 1u), 0u};",
    "case_ids": ["EnergyTrans_CheckPlayArea-0"],
}
# <<< factory-mutation EnergyTrans_CheckPlayArea
# >>> factory-mutation Firegiver_InitialEffect
MUTATIONS["Firegiver_InitialEffect"] = {"source_symbol": "Firegiver_InitialEffect", "before": "uint8_t Firegiver_InitialEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}", "after": "uint8_t Firegiver_InitialEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x00u);\n}", "case_ids": ["Firegiver_InitialEffect-0", "Firegiver_InitialEffect-1", "Firegiver_InitialEffect-2", "Firegiver_InitialEffect-3"]}
# <<< factory-mutation Firegiver_InitialEffect
# >>> factory-mutation MoltresLv37DiveBomb_AIEffect
MUTATIONS["MoltresLv37DiveBomb_AIEffect"] = {"source_symbol": "MoltresLv37DiveBomb_AIEffect", "before": "void MoltresLv37DiveBomb_AIEffect(void)\n{\n\tSetExpectedAIDamage(35u, 0u, 70u);\n}", "after": "void MoltresLv37DiveBomb_AIEffect(void)\n{\n\tSetExpectedAIDamage(36u, 0u, 70u);\n}", "case_ids": ["MoltresLv37DiveBomb_AIEffect-0", "MoltresLv37DiveBomb_AIEffect-1"]}
# <<< factory-mutation MoltresLv37DiveBomb_AIEffect
# >>> factory-mutation GetEnergyAttachedMultiplierDamage
MUTATIONS["GetEnergyAttachedMultiplierDamage"] = {"source_symbol": "GetEnergyAttachedMultiplierDamage", "before": "return (uint16_t)(count * 10u);", "after": "return (uint16_t)(count * 9u);", "case_ids": ["GetEnergyAttachedMultiplierDamage-1", "GetEnergyAttachedMultiplierDamage-2"]}
# <<< factory-mutation GetEnergyAttachedMultiplierDamage


# >>> factory-mutation ClefairyDoll_BenchCheck
MUTATIONS["ClefairyDoll_BenchCheck"] = {
    "source_symbol": "ClefairyDoll_BenchCheck",
    "before": "uint8_t f = (uint8_t)(count.a >= 6u ? 0x10u : 0x00u);",
    "after": "uint8_t f = (uint8_t)(count.a > 6u ? 0x10u : 0x00u);",
    "case_ids": ["ClefairyDoll_BenchCheck-2"],
}
# <<< factory-mutation ClefairyDoll_BenchCheck
# >>> factory-mutation ClefairyDoll_PlaceInPlayAreaEffect
MUTATIONS["ClefairyDoll_PlaceInPlayAreaEffect"] = {
    "source_symbol": "ClefairyDoll_PlaceInPlayAreaEffect",
    "before": "PutHandPokemonCardInPlayArea(hTempCardIndex_ff9f, 0x00u);",
    "after": "PutHandPokemonCardInPlayArea((uint8_t)(hTempCardIndex_ff9f + 1u), 0x00u);",
    "case_ids": ["ClefairyDoll_PlaceInPlayAreaEffect-0"],
}

# >>> factory Fly_AIEffect
CONTRACT["Fly_AIEffect"] = {"compare": (), "preserve": ()}
CASES["Fly_AIEffect"] = [{"wram": {0xCCB9: b"\x00\x00\x00"}, "read": {0xCCB9: 3}},
                         dict(POISON, wram={0xCCB9: b"\x40\x50\x60"}, read={0xCCB9: 3})]
# <<< factory Fly_AIEffect
# >>> factory Gigashock_AISelectEffect
CONTRACT["Gigashock_AISelectEffect"] = {"compare": (), "preserve": ()}
CASES["Gigashock_AISelectEffect"] = [
    {"wram": {0xFF97: b"\xC2", 0xC3EF: b"\x05", 0xC3C9: b"\x1E\x0A\x14\x28"}, "read": {0xFFA0: 4}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC3EF: b"\x06", 0xC3C9: b"\x32\x28\x1E\x14\x0A"}, read={0xFFA0: 4}),
]
# <<< factory Gigashock_AISelectEffect
# >>> factory-mutation Fly_AIEffect
MUTATIONS["Fly_AIEffect"] = {"source_symbol": "Fly_AIEffect", "before": "SetExpectedAIDamage(15u, 0u, 30u);", "after": "SetExpectedAIDamage(16u, 0u, 30u);", "case_ids": ["Fly_AIEffect-0", "Fly_AIEffect-1"]}
# <<< factory-mutation Fly_AIEffect
# >>> factory-mutation Gigashock_AISelectEffect
MUTATIONS["Gigashock_AISelectEffect"] = {"source_symbol": "Gigashock_AISelectEffect", "before": "gb_write8((uint16_t)(hTempList_ADDR + 3u), 0xffu);", "after": "gb_write8((uint16_t)(hTempList_ADDR + 3u), 0u);", "case_ids": ["Gigashock_AISelectEffect-0", "Gigashock_AISelectEffect-1"]}
# <<< factory-mutation Gigashock_AISelectEffect
MUTATIONS["Wildfire_DiscardDeckEffect"] = {
    "source_symbol": "Wildfire_DiscardDeckEffect",
    "before": "if (cards_left < count)",
    "after": "if (cards_left > count)",
    "case_ids": ["Wildfire_DiscardDeckEffect-0", "Wildfire_DiscardDeckEffect-1", "Wildfire_DiscardDeckEffect-2"],
}
# <<< factory-mutation Wildfire_DiscardDeckEffect
# >>> factory-mutation MoltresLv35DiveBomb_AIEffect
MUTATIONS["MoltresLv35DiveBomb_AIEffect"] = {
    "source_symbol": "MoltresLv35DiveBomb_AIEffect",
    "before": "SetExpectedAIDamage(40u, 0u, 80u);",
    "after": "SetExpectedAIDamage(41u, 0u, 80u);",
    "case_ids": ["MoltresLv35DiveBomb_AIEffect-0", "MoltresLv35DiveBomb_AIEffect-1"],
}
# <<< factory-mutation MoltresLv35DiveBomb_AIEffect
# >>> factory-mutation EnergyBurnCheck_Unreferenced
MUTATIONS["EnergyBurnCheck_Unreferenced"] = {
    "source_symbol": "EnergyBurnCheck_Unreferenced",
    "before": "if (card_id == 0x32u)",
    "after": "if (card_id == 0x33u)",
    "case_ids": ["EnergyBurnCheck_Unreferenced-0", "EnergyBurnCheck_Unreferenced-1", "EnergyBurnCheck_Unreferenced-2", "EnergyBurnCheck_Unreferenced-3"]
}
# <<< factory-mutation EnergyBurnCheck_Unreferenced
# >>> factory-mutation FlareonRage_DamageBoostEffect
MUTATIONS["FlareonRage_DamageBoostEffect"] = {
    "source_symbol": "FlareonRage_DamageBoostEffect",
    "before": "void FlareonRage_DamageBoostEffect(void)\n{\n    CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n    AddToDamage(r.a);\n}",
    "after": "void FlareonRage_DamageBoostEffect(void)\n{\n    CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n    AddToDamage((uint8_t)(r.a + 1u));\n}",
    "case_ids": ["FlareonRage_DamageBoostEffect-0", "FlareonRage_DamageBoostEffect-1"]
}
# <<< factory-mutation FlareonRage_DamageBoostEffect


SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)# >>> factory-mutation Shift_OncePerTurnCheck
MUTATIONS["Shift_OncePerTurnCheck"] = {
    "source_symbol": "Shift_OncePerTurnCheck",
    "before": "return (ShiftOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};",
    "after": "return (ShiftOncePerTurnCheckResult){0x10u, 0u};",
    "case_ids": ["Shift_OncePerTurnCheck-1"],
}
# <<< factory-mutation Shift_OncePerTurnCheck
# >>> factory-mutation VenomPowder_AIEffect
MUTATIONS["VenomPowder_AIEffect"] = {
    "source_symbol": "VenomPowder_AIEffect",
    "before": "void VenomPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage(5u, 0u, 10u);\n}",
    "after": "void VenomPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage(6u, 0u, 10u);\n}",
    "case_ids": ["VenomPowder_AIEffect-0"],
}
# <<< factory-mutation VenomPowder_AIEffect
# >>> factory-mutation TangelaPoisonPowder_AIEffect
MUTATIONS["TangelaPoisonPowder_AIEffect"] = {
    "source_symbol": "TangelaPoisonPowder_AIEffect",
    "before": "void TangelaPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void TangelaPoisonPowder_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 1u, 10u);\n}",
    "case_ids": ["TangelaPoisonPowder_AIEffect-0", "TangelaPoisonPowder_AIEffect-1",
                 "TangelaPoisonPowder_AIEffect-2", "TangelaPoisonPowder_AIEffect-3"],
}
# <<< factory-mutation TangelaPoisonPowder_AIEffect
# >>> factory-mutation PetalDance_AIEffect
MUTATIONS["PetalDance_AIEffect"] = {
    "source_symbol": "PetalDance_AIEffect",
    "before": "void PetalDance_AIEffect(void)\n{\n\tSetExpectedAIDamage(60u, 0u, 120u);\n}",
    "after": "void PetalDance_AIEffect(void)\n{\n\tSetExpectedAIDamage(61u, 0u, 120u);\n}",
    "case_ids": ["PetalDance_AIEffect-0", "PetalDance_AIEffect-1",
                 "PetalDance_AIEffect-2", "PetalDance_AIEffect-3"],
}
# <<< factory-mutation PetalDance_AIEffect
# >>> factory-mutation RainDanceEffect
MUTATIONS["RainDanceEffect"] = {
    "source_symbol": "RainDanceEffect",
    "before": "uint8_t RainDanceEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x10u);\n}",
    "after": "uint8_t RainDanceEffect(uint8_t f)\n{\n\treturn (uint8_t)((f & 0x80u) | 0x00u);\n}",
    "case_ids": ["RainDanceEffect-0"],
}
# <<< factory-mutation RainDanceEffect
# >>> factory-mutation PsyduckFurySwipes_AIEffect
MUTATIONS["PsyduckFurySwipes_AIEffect"] = {
    "source_symbol": "PsyduckFurySwipes_AIEffect",
    "before": "SetExpectedAIDamage((uint8_t)(30u / 2u), 0u, 30u);",
    "after": "SetExpectedAIDamage((uint8_t)(32u / 2u), 0u, 30u);",
    "case_ids": ["PsyduckFurySwipes_AIEffect-0", "PsyduckFurySwipes_AIEffect-1"],
}
# <<< factory-mutation PsyduckFurySwipes_AIEffect
# >>> factory-mutation VaporeonQuickAttack_AIEffect
MUTATIONS["VaporeonQuickAttack_AIEffect"] = {
    "source_symbol": "VaporeonQuickAttack_AIEffect",
    "before": "SetExpectedAIDamage((10u + 30u) / 2u, 10u, 30u);",
    "after": "SetExpectedAIDamage((12u + 30u) / 2u, 10u, 30u);",
    "case_ids": ["VaporeonQuickAttack_AIEffect-0", "VaporeonQuickAttack_AIEffect-1"],
}
# <<< factory-mutation VaporeonQuickAttack_AIEffect
# >>> factory-mutation JellyfishSting_AIEffect
MUTATIONS["JellyfishSting_AIEffect"] = {
    "source_symbol": "JellyfishSting_AIEffect",
    "before": "void JellyfishSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);\n}",
    "after": "void JellyfishSting_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(11u, 10u, 10u);\n}",
    "case_ids": ["JellyfishSting_AIEffect-0", "JellyfishSting_AIEffect-1"],
}
# <<< factory-mutation JellyfishSting_AIEffect
# >>> factory-mutation PoliwhirlAmnesia_CheckAttacks
MUTATIONS["PoliwhirlAmnesia_CheckAttacks"] = {
    "source_symbol": "PoliwhirlAmnesia_CheckAttacks",
    "before": "if ((uint8_t)(lo | hi) == 0u)",
    "after": "if ((uint8_t)(lo | hi) != 0u)",
    "case_ids": ["PoliwhirlAmnesia_CheckAttacks-1", "PoliwhirlAmnesia_CheckAttacks-0", "PoliwhirlAmnesia_CheckAttacks-2"],
}
# <<< factory-mutation PoliwhirlAmnesia_CheckAttacks
# >>> factory-mutation HeadacheEffect
MUTATIONS["HeadacheEffect"] = {
    "source_symbol": "HeadacheEffect",
    "before": "\tgb_write8(substatus.hl, (uint8_t)(substatus.a | (1u << SUBSTATUS3_HEADACHE_F)));",
    "after": "\tgb_write8(substatus.hl, substatus.a);",
    "case_ids": ["HeadacheEffect-0", "HeadacheEffect-1", "HeadacheEffect-2"],
}
# <<< factory-mutation HeadacheEffect
# >>> factory-mutation SleepEffect
MUTATIONS["SleepEffect"] = {
    "source_symbol": "SleepEffect",
    "before": "\treturn QueueStatusCondition(PSN_DBLPSN, ASLEEP);",
    "after": "\treturn QueueStatusCondition(PSN_DBLPSN, CONFUSED);",
    "case_ids": ["SleepEffect-0", "SleepEffect-1"],
}
# <<< factory-mutation SleepEffect
# >>> factory-mutation SetDefiniteDamage
MUTATIONS["SetDefiniteDamage"] = {
    "source_symbol": "SetDefiniteDamage",
    "before": "\tgb_write8(wAIMinDamage_ADDR, a);",
    "after": "\tgb_write8(wAIMinDamage_ADDR, (uint8_t)(a + 1u));",
    "case_ids": ["SetDefiniteDamage-0", "SetDefiniteDamage-1", "SetDefiniteDamage-2"],
}
# <<< factory-mutation SetDefiniteDamage
# >>> factory-mutation ArcanineQuickAttack_AIEffect
MUTATIONS["ArcanineQuickAttack_AIEffect"] = {
    "source_symbol": "ArcanineQuickAttack_AIEffect",
    "before": "void ArcanineQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage((10u + 30u) / 2u, 10u, 30u);",
    "after": "void ArcanineQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage((12u + 30u) / 2u, 10u, 30u);",
    "case_ids": ["ArcanineQuickAttack_AIEffect-0", "ArcanineQuickAttack_AIEffect-1"],
}
# <<< factory-mutation ArcanineQuickAttack_AIEffect
# >>> factory-mutation FlamesOfRage_CheckEnergy
MUTATIONS["FlamesOfRage_CheckEnergy"] = {
    "source_symbol": "FlamesOfRage_CheckEnergy",
    "before": "return (FlamesOfRageCheckEnergyResult){a, f, PLAY_AREA_ARENA,\n\t\tNotEnoughFireEnergyText};",
    "after": "return (FlamesOfRageCheckEnergyResult){a, f, PLAY_AREA_ARENA + 1u,\n\t\tNotEnoughFireEnergyText};",
    "case_ids": ["FlamesOfRage_CheckEnergy-0", "FlamesOfRage_CheckEnergy-1"],
}
# <<< factory-mutation FlamesOfRage_CheckEnergy
# >>> factory-mutation MagmarFlamethrower_DiscardEffect
MUTATIONS["MagmarFlamethrower_DiscardEffect"] = {
    "source_symbol": "MagmarFlamethrower_DiscardEffect",
    "before": "uint8_t MagmarFlamethrower_DiscardEffect(void)\n{\n\tuint8_t card = gb_read8(hTemp_ffa0_ADDR);\n\tPutCardInDiscardPile(card);\n\treturn card;\n}",
    "after": "uint8_t MagmarFlamethrower_DiscardEffect(void)\n{\n\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR + 1u));\n\tPutCardInDiscardPile(card);\n\treturn card;\n}",
    "case_ids": ["MagmarFlamethrower_DiscardEffect-1"],
}
# <<< factory-mutation MagmarFlamethrower_DiscardEffect
# >>> factory-mutation MagmarSmog_AIEffect
MUTATIONS["MagmarSmog_AIEffect"] = {
    "source_symbol": "MagmarSmog_AIEffect",
    "before": "void MagmarSmog_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);\n}",
    "after": "void MagmarSmog_AIEffect(void)\n{\n\tUpdateExpectedAIDamage_AccountForPoison(6u, 0u, 10u);\n}",
    "case_ids": ["MagmarSmog_AIEffect-0"],
}
# <<< factory-mutation MagmarSmog_AIEffect
# >>> factory-mutation Wildfire_CheckEnergy
MUTATIONS["Wildfire_CheckEnergy"] = {
    "source_symbol": "Wildfire_CheckEnergy",
    "before": "return (WildfireCheckEnergyResult){energy, f, PLAY_AREA_ARENA, hl};",
    "after": "return (WildfireCheckEnergyResult){energy, f, PLAY_AREA_ARENA, 0u};",
    "case_ids": ["Wildfire_CheckEnergy-0", "Wildfire_CheckEnergy-1", "Wildfire_CheckEnergy-2"],
}
# <<< factory-mutation Wildfire_CheckEnergy
# >>> factory-mutation MrMimeMeditate_DamageBoostEffect
MUTATIONS["MrMimeMeditate_DamageBoostEffect"] = {
    "source_symbol": "MrMimeMeditate_DamageBoostEffect",
    "before": "void MrMimeMeditate_DamageBoostEffect(void)\n{\n\tSwapTurn();\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSwapTurn();\n\tAddToDamage(r.a);\n}",
    "after": "void MrMimeMeditate_DamageBoostEffect(void)\n{\n\tSwapTurn();\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSwapTurn();\n\tAddToDamage((uint8_t)(r.a + 1u));\n}",
    "case_ids": ["MrMimeMeditate_DamageBoostEffect-0", "MrMimeMeditate_DamageBoostEffect-1", "MrMimeMeditate_DamageBoostEffect-2"],
}
# <<< factory-mutation MrMimeMeditate_DamageBoostEffect
# >>> factory-mutation DancingEmbers_AIEffect
MUTATIONS["DancingEmbers_AIEffect"] = {
    "source_symbol": "DancingEmbers_AIEffect",
    "before": "\tSetExpectedAIDamage(80u / 2u, 0u, 80u);",
    "after": "\tSetExpectedAIDamage(80u / 2u, 0u, 81u);",
    "case_ids": ["DancingEmbers_AIEffect-0", "DancingEmbers_AIEffect-1"],
}
# <<< factory-mutation DancingEmbers_AIEffect
# >>> factory-mutation FlareonFlamethrower_DiscardEffect
MUTATIONS["FlareonFlamethrower_DiscardEffect"] = {"source_symbol": "FlareonFlamethrower_DiscardEffect", "before": "\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR));", "after": "\tuint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR + 1u));", "case_ids": ["FlareonFlamethrower_DiscardEffect-1"]}
# <<< factory-mutation FlareonFlamethrower_DiscardEffect
# >>> factory-mutation MagmarFlamethrower_CheckEnergy
MUTATIONS["MagmarFlamethrower_CheckEnergy"] = {"source_symbol": "MagmarFlamethrower_CheckEnergy", "before": "	uint16_t magmar_hl = NotEnoughFireEnergyText;", "after": "	uint16_t magmar_hl = (uint16_t)(NotEnoughFireEnergyText + 1u);", "case_ids": ["MagmarFlamethrower_CheckEnergy-0", "MagmarFlamethrower_CheckEnergy-1", "MagmarFlamethrower_CheckEnergy-2", "MagmarFlamethrower_CheckEnergy-3"]}
# <<< factory-mutation MagmarFlamethrower_CheckEnergy
# >>> factory-mutation FlamesOfRage_DiscardEffect
MUTATIONS["FlamesOfRage_DiscardEffect"] = {
    "source_symbol": "FlamesOfRage_DiscardEffect",
    "before": "\tPutCardInDiscardPile(gb_read8(hTempList_ADDR));",
    "after": "\tPutCardInDiscardPile(gb_read8((uint16_t)(hTempList_ADDR + 1u)));",
    "case_ids": ["FlamesOfRage_DiscardEffect-0"],
}
# <<< factory-mutation FlamesOfRage_DiscardEffect
# >>> factory-mutation FlamesOfRage_DamageBoostEffect
MUTATIONS["FlamesOfRage_DamageBoostEffect"] = {
    "source_symbol": "FlamesOfRage_DamageBoostEffect",
    "before": "void FlamesOfRage_DamageBoostEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage(r.a);",
    "after": "void FlamesOfRage_DamageBoostEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage((uint8_t)(r.a + 1u));",
    "case_ids": ["FlamesOfRage_DamageBoostEffect-0"],
}
# <<< factory-mutation FlamesOfRage_DamageBoostEffect
# >>> factory-mutation CharmeleonFlamethrower_CheckEnergy
MUTATIONS["CharmeleonFlamethrower_CheckEnergy"] = {
    "source_symbol": "CharmeleonFlamethrower_CheckEnergy",
    "before": "return (CharmeleonFlamethrowerCheckEnergyResult){energy, f, 0u, hl};",
    "after": "return (CharmeleonFlamethrowerCheckEnergyResult){energy, f, 1u, hl};",
    "case_ids": ["CharmeleonFlamethrower_CheckEnergy-0", "CharmeleonFlamethrower_CheckEnergy-1"],
}
# <<< factory-mutation CharmeleonFlamethrower_CheckEnergy
# >>> factory-mutation CharmeleonFlamethrower_DiscardEffect
MUTATIONS["CharmeleonFlamethrower_DiscardEffect"] = {
    "source_symbol": "CharmeleonFlamethrower_DiscardEffect",
    "before": "uint8_t CharmeleonFlamethrower_DiscardEffect(void)\n{\n\tuint8_t card = gb_read8(hTemp_ffa0_ADDR);\n\tPutCardInDiscardPile(card);\n\treturn card;",
    "after": "uint8_t CharmeleonFlamethrower_DiscardEffect(void)\n{\n\tuint8_t card = gb_read8(hTemp_ffa0_ADDR);\n\tPutCardInDiscardPile(card);\n\treturn (uint8_t)(card + 1u);",
    "case_ids": ["CharmeleonFlamethrower_DiscardEffect-0", "CharmeleonFlamethrower_DiscardEffect-1", "CharmeleonFlamethrower_DiscardEffect-2"],
}
# <<< factory-mutation CharmeleonFlamethrower_DiscardEffect
# >>> factory-mutation EnergyBurnEffect
MUTATIONS["EnergyBurnEffect"] = {
    "source_symbol": "EnergyBurnEffect",
    "before": "return (EnergyBurnEffectResult){(uint8_t)((f & 0x80u) | 0x10u)};",
    "after": "return (EnergyBurnEffectResult){(uint8_t)(f & 0x80u)};",
    "case_ids": ["EnergyBurnEffect-1"],
}
# <<< factory-mutation EnergyBurnEffect
# >>> factory-mutation FireSpin_CheckEnergy
MUTATIONS["FireSpin_CheckEnergy"] = {
    "source_symbol": "FireSpin_CheckEnergy",
    "before": "if (count < 2u)",
    "after": "if (count < 1u)",
    "case_ids": ["FireSpin_CheckEnergy-0"],
}
# <<< factory-mutation FireSpin_CheckEnergy
# >>> factory-mutation FlareonQuickAttack_AIEffect
MUTATIONS["FlareonQuickAttack_AIEffect"] = {
    "source_symbol": "FlareonQuickAttack_AIEffect",
    "before": "SetExpectedAIDamage((uint8_t)(40u / 2u), 10u, 30u);",
    "after": "SetExpectedAIDamage((uint8_t)(42u / 2u), 10u, 30u);",
    "case_ids": ["FlareonQuickAttack_AIEffect-0", "FlareonQuickAttack_AIEffect-1"],
}
# <<< factory-mutation FlareonQuickAttack_AIEffect
# >>> factory-mutation FlareonFlamethrower_CheckEnergy
MUTATIONS["FlareonFlamethrower_CheckEnergy"] = {
    "source_symbol": "FlareonFlamethrower_CheckEnergy",
    "before": "return (FlareonFlamethrowerCheckEnergyResult){a, f, PLAY_AREA_ARENA,\n\t\tNotEnoughFireEnergyText};",
    "after": "return (FlareonFlamethrowerCheckEnergyResult){a, f, PLAY_AREA_ARENA + 1u,\n\t\tNotEnoughFireEnergyText};",
    "case_ids": ["FlareonFlamethrower_CheckEnergy-0", "FlareonFlamethrower_CheckEnergy-1"],
}
# <<< factory-mutation FlareonFlamethrower_CheckEnergy
# >>> factory-mutation Prophecy_AISelectEffect
MUTATIONS["Prophecy_AISelectEffect"] = {
    "source_symbol": "Prophecy_AISelectEffect",
    "before": "hTemp_ffa0 = 0xffu;\n\treturn (ProphecyAISelectEffectResult){0xffu};",
    "after": "hTemp_ffa0 = 0x00u;\n\treturn (ProphecyAISelectEffectResult){0xffu};",
    "case_ids": ["Prophecy_AISelectEffect-0", "Prophecy_AISelectEffect-1"],
}
# <<< factory-mutation Prophecy_AISelectEffect
# >>> factory-mutation Prophecy_ReorderDeckEffect
MUTATIONS["Prophecy_ReorderDeckEffect"] = {
    "source_symbol": "Prophecy_ReorderDeckEffect",
    "before": "if (a == 0xffu)\n\t\treturn (ProphecyReorderDeckEffectResult){a, 0u, 0x00u, hl};",
    "after": "if (a != 0xffu)\n\t\treturn (ProphecyReorderDeckEffectResult){a, 0u, 0x00u, hl};",
    "case_ids": ["Prophecy_ReorderDeckEffect-0", "Prophecy_ReorderDeckEffect-1"],
}
# <<< factory-mutation Prophecy_ReorderDeckEffect
# >>> factory-mutation SuperEnergyRetrieval_HandEnergyCheck
MUTATIONS["SuperEnergyRetrieval_HandEnergyCheck"] = {"source_symbol": "SuperEnergyRetrieval_HandEnergyCheck", "before": "return (SuperEnergyRetrievalHandEnergyCheckResult){NotEnoughCardsInHandText, 0x70u};", "after": "return (SuperEnergyRetrievalHandEnergyCheckResult){ThereAreNoBasicEnergyCardsInDiscardPileText, 0x70u};", "case_ids": ["SuperEnergyRetrieval_HandEnergyCheck-0", "SuperEnergyRetrieval_HandEnergyCheck-1", "SuperEnergyRetrieval_HandEnergyCheck-2"]}
# <<< factory-mutation SuperEnergyRetrieval_HandEnergyCheck
# >>> factory-mutation GetNextPositionInTempList_TrainerEffects
MUTATIONS["GetNextPositionInTempList_TrainerEffects"] = {"source_symbol": "GetNextPositionInTempList_TrainerEffects", "before": "hCurSelectionItem = (uint8_t)(selection + 1u);", "after": "hCurSelectionItem = (uint8_t)(selection + 2u);", "case_ids": ["GetNextPositionInTempList_TrainerEffects-0", "GetNextPositionInTempList_TrainerEffects-1", "GetNextPositionInTempList_TrainerEffects-2", "GetNextPositionInTempList_TrainerEffects-3"]}
# <<< factory-mutation GetNextPositionInTempList_TrainerEffects
# >>> factory-mutation NinetalesLure_AISelectEffect
MUTATIONS["NinetalesLure_AISelectEffect"] = {"source_symbol": "NinetalesLure_AISelectEffect", "before": "\thTemp_ffa0 = r.a;", "after": "\thTemp_ffa0 = (uint8_t)(r.a + 1u);", "case_ids": ["NinetalesLure_AISelectEffect-0", "NinetalesLure_AISelectEffect-1", "NinetalesLure_AISelectEffect-2"]}
# <<< factory-mutation NinetalesLure_AISelectEffect
# >>> factory-mutation Ember_CheckEnergy
MUTATIONS["Ember_CheckEnergy"] = {"source_symbol": "Ember_CheckEnergy", "before": "\tif (fire == 1u)", "after": "\tif (fire == 0u)", "case_ids": ["Ember_CheckEnergy-0", "Ember_CheckEnergy-1"]}
# <<< factory-mutation Ember_CheckEnergy
# >>> factory-mutation DestinyBond_CheckEnergy
MUTATIONS["DestinyBond_CheckEnergy"] = {"source_symbol": "DestinyBond_CheckEnergy", "before": "\tuint16_t hl = NotEnoughPsychicEnergyText;", "after": "\tuint16_t hl = 0u;", "case_ids": ["DestinyBond_CheckEnergy-0", "DestinyBond_CheckEnergy-1", "DestinyBond_CheckEnergy-2"]}
# <<< factory-mutation DestinyBond_CheckEnergy
# >>> factory-mutation ComputerSearch_HandDeckCheck
MUTATIONS["ComputerSearch_HandDeckCheck"] = {"source_symbol": "ComputerSearch_HandDeckCheck", "before": "#define NotEnoughCardsInHandText 0x00b6u", "after": "#define NotEnoughCardsInHandText 0x00b1u", "case_ids": ["ComputerSearch_HandDeckCheck-0", "ComputerSearch_HandDeckCheck-1", "ComputerSearch_HandDeckCheck-2", "ComputerSearch_HandDeckCheck-3", "ComputerSearch_HandDeckCheck-4", "ComputerSearch_HandDeckCheck-5"]}
# <<< factory-mutation ComputerSearch_HandDeckCheck
# >>> factory-mutation MrFuji_BenchCheck
MUTATIONS["MrFuji_BenchCheck"] = {"source_symbol": "MrFuji_BenchCheck", "before": "#define EffectNoPokemonOnTheBenchText 0x00b7u", "after": "#define EffectNoPokemonOnTheBenchText 0x00b1u", "case_ids": ["MrFuji_BenchCheck-0", "MrFuji_BenchCheck-1", "MrFuji_BenchCheck-2", "MrFuji_BenchCheck-3", "MrFuji_BenchCheck-4"]}
# <<< factory-mutation MrFuji_BenchCheck
# >>> factory-mutation DrawSymbolOnPlayAreaCursor
MUTATIONS["DrawSymbolOnPlayAreaCursor"] = {"source_symbol": "DrawSymbolOnPlayAreaCursor", "before": "uint8_t row = (uint8_t)(a * 3u + 2u);", "after": "uint8_t row = (uint8_t)(a * 3u + 3u);", "case_ids": ["DrawSymbolOnPlayAreaCursor-0", "DrawSymbolOnPlayAreaCursor-1", "DrawSymbolOnPlayAreaCursor-2"]}
# <<< factory-mutation DrawSymbolOnPlayAreaCursor
# >>> factory-mutation GustOfWind_BenchCheck
MUTATIONS["GustOfWind_BenchCheck"] = {"source_symbol": "GustOfWind_BenchCheck", "before": "uint8_t flags = 0x40u;", "after": "uint8_t flags = 0x00u;", "case_ids": ["GustOfWind_BenchCheck-0", "GustOfWind_BenchCheck-1", "GustOfWind_BenchCheck-2"]}
# <<< factory-mutation GustOfWind_BenchCheck
# >>> factory-mutation MarowakCallForFamily_AISelectEffect
MUTATIONS["MarowakCallForFamily_AISelectEffect"] = {"source_symbol": "MarowakCallForFamily_AISelectEffect", "before": "if (gb_read8(wLoadedCard2Stage_ADDR) == 0u)", "after": "if (gb_read8(wLoadedCard2Stage_ADDR) != 0u)", "case_ids": ["MarowakCallForFamily_AISelectEffect-0", "MarowakCallForFamily_AISelectEffect-1"]}
# <<< factory-mutation MarowakCallForFamily_AISelectEffect
# >>> factory-mutation Peek_OncePerTurnCheck
MUTATIONS["Peek_OncePerTurnCheck"] = {"source_symbol": "Peek_OncePerTurnCheck", "before": "if (flags.a & USED_PKMN_POWER_THIS_TURN)", "after": "if (!(flags.a & USED_PKMN_POWER_THIS_TURN))", "case_ids": ["Peek_OncePerTurnCheck-0"]}
# <<< factory-mutation Peek_OncePerTurnCheck
# >>> factory-mutation Wail_BenchCheck
MUTATIONS["Wail_BenchCheck"] = {"source_symbol": "Wail_BenchCheck", "before": "if (turn.a < 6u)", "after": "if (turn.a < 5u)", "case_ids": ["Wail_BenchCheck-0", "Wail_BenchCheck-2"]}
# <<< factory-mutation Wail_BenchCheck
# >>> factory-mutation ThickSkinnedEffect
MUTATIONS["ThickSkinnedEffect"] = {"source_symbol": "ThickSkinnedEffect", "before": "0x10u", "after": "0x00u", "case_ids": ["ThickSkinnedEffect-0"]}
# <<< factory-mutation ThickSkinnedEffect
# >>> factory-mutation HealingWind_InitialEffect
MUTATIONS["HealingWind_InitialEffect"] = {"source_symbol": "HealingWind_InitialEffect", "before": "0x10u", "after": "0x00u", "case_ids": ["HealingWind_InitialEffect-0"]}
# <<< factory-mutation HealingWind_InitialEffect

# >>> factory DreamEaterEffect
CONTRACT["DreamEaterEffect"] = {"compare": ("a", "f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["DreamEaterEffect"] = [
    {},
    dict(POISON),
]
# <<< factory DreamEaterEffect

# >>> factory JynxMeditate_DamageBoostEffect
CONTRACT["JynxMeditate_DamageBoostEffect"] = {"compare": (), "preserve": ()}
CASES["JynxMeditate_DamageBoostEffect"] = [{}, dict(POISON)]
# <<< factory JynxMeditate_DamageBoostEffect
# >>> factory KadabraRecover_CheckEnergyHP
CONTRACT["KadabraRecover_CheckEnergyHP"] = {"compare": ("a", "f", "b", "c", "d", "hl"), "preserve": ("b", "d")}
CASES["KadabraRecover_CheckEnergyHP"] = [{}, dict(POISON)]
# <<< factory KadabraRecover_CheckEnergyHP
# >>> factory MewtwoAltEnergyAbsorption_AddToHandEffect
CONTRACT["MewtwoAltEnergyAbsorption_AddToHandEffect"] = {"compare": (), "preserve": ()}
CASES["MewtwoAltEnergyAbsorption_AddToHandEffect"] = [{"wram": {0xFFA0: b"\xFF"}}, dict(POISON, wram={0xFFA0: b"\xFF"})]
# <<< factory MewtwoAltEnergyAbsorption_AddToHandEffect
# >>> factory MewtwoEnergyAbsorption_AddToHandEffect
CONTRACT["MewtwoEnergyAbsorption_AddToHandEffect"] = {"compare": (), "preserve": ()}
CASES["MewtwoEnergyAbsorption_AddToHandEffect"] = [{"wram": {0xFFA0: b"\xFF"}}, dict(POISON, wram={0xFFA0: b"\xFF"})]
# <<< factory MewtwoEnergyAbsorption_AddToHandEffect
# >>> factory NeutralizingShieldEffect
CONTRACT["NeutralizingShieldEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["NeutralizingShieldEffect"] = [{}, dict(POISON)]
# <<< factory NeutralizingShieldEffect
# >>> factory PealOfThunder_InitialEffect
CONTRACT["PealOfThunder_InitialEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PealOfThunder_InitialEffect"] = [{}, dict(POISON)]
# <<< factory PealOfThunder_InitialEffect
# >>> factory PrehistoricPowerEffect
CONTRACT["PrehistoricPowerEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PrehistoricPowerEffect"] = [{}, dict(POISON)]
# <<< factory PrehistoricPowerEffect
# >>> factory Scavenge_DiscardEffect
CONTRACT["Scavenge_DiscardEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["Scavenge_DiscardEffect"] = [{"wram": {0xFFA0: b"\x00"}}, dict(POISON, wram={0xFFA0: b"\x05"})]
# <<< factory Scavenge_DiscardEffect

# >>> factory-mutation DreamEaterEffect
MUTATIONS["DreamEaterEffect"] = {"source_symbol": "DreamEaterEffect", "before": "if (masked == ASLEEP)", "after": "if (masked != ASLEEP)", "case_ids": ["DreamEaterEffect-0", "DreamEaterEffect-1"]}
# <<< factory-mutation DreamEaterEffect
# >>> factory-mutation JynxMeditate_DamageBoostEffect
MUTATIONS["JynxMeditate_DamageBoostEffect"] = {"source_symbol": "JynxMeditate_DamageBoostEffect", "before": "AddToDamage(damage.a);", "after": "AddToDamage((uint8_t)(damage.a + 1u));", "case_ids": ["JynxMeditate_DamageBoostEffect-0", "JynxMeditate_DamageBoostEffect-1"]}
# <<< factory-mutation JynxMeditate_DamageBoostEffect
# >>> factory-mutation KadabraRecover_CheckEnergyHP
MUTATIONS["KadabraRecover_CheckEnergyHP"] = {"source_symbol": "KadabraRecover_CheckEnergyHP", "before": "\t\tf |= 0x20u;\n\tif (energy < 1u)", "after": "\t\tf |= 0x20u;\n\tif (energy < 2u)", "case_ids": ["KadabraRecover_CheckEnergyHP-0", "KadabraRecover_CheckEnergyHP-1"]}
# <<< factory-mutation KadabraRecover_CheckEnergyHP
# >>> factory-mutation MewtwoAltEnergyAbsorption_AddToHandEffect
MUTATIONS["MewtwoAltEnergyAbsorption_AddToHandEffect"] = {"source_symbol": "MewtwoAltEnergyAbsorption_AddToHandEffect", "before": "if (card == 0xffu)", "after": "if (card != 0xffu)", "case_ids": ["MewtwoAltEnergyAbsorption_AddToHandEffect-0", "MewtwoAltEnergyAbsorption_AddToHandEffect-1"]}
# <<< factory-mutation MewtwoAltEnergyAbsorption_AddToHandEffect
# >>> factory-mutation MewtwoEnergyAbsorption_AddToHandEffect
MUTATIONS["MewtwoEnergyAbsorption_AddToHandEffect"] = {"source_symbol": "MewtwoEnergyAbsorption_AddToHandEffect", "before": "MewtwoAltEnergyAbsorption_AddToHandEffect();", "after": "MewtwoEnergyAbsorption_AddToHandEffect();", "case_ids": ["MewtwoEnergyAbsorption_AddToHandEffect-0", "MewtwoEnergyAbsorption_AddToHandEffect-1"]}
# <<< factory-mutation MewtwoEnergyAbsorption_AddToHandEffect
# >>> factory-mutation NeutralizingShieldEffect
MUTATIONS["NeutralizingShieldEffect"] = {"source_symbol": "NeutralizingShieldEffect", "before": "return 0x10u;", "after": "return 0x00u;", "case_ids": ["NeutralizingShieldEffect-0", "NeutralizingShieldEffect-1"]}
# <<< factory-mutation NeutralizingShieldEffect
# >>> factory-mutation PealOfThunder_InitialEffect
MUTATIONS["PealOfThunder_InitialEffect"] = {"source_symbol": "PealOfThunder_InitialEffect", "before": "return 0x10u;", "after": "return 0x00u;", "case_ids": ["PealOfThunder_InitialEffect-0", "PealOfThunder_InitialEffect-1"]}
# <<< factory-mutation PealOfThunder_InitialEffect
# >>> factory-mutation PrehistoricPowerEffect
MUTATIONS["PrehistoricPowerEffect"] = {"source_symbol": "PrehistoricPowerEffect", "before": "return 0x10u;", "after": "return 0x00u;", "case_ids": ["PrehistoricPowerEffect-0", "PrehistoricPowerEffect-1"]}
# <<< factory-mutation PrehistoricPowerEffect
# >>> factory-mutation Scavenge_DiscardEffect
MUTATIONS["Scavenge_DiscardEffect"] = {"source_symbol": "Scavenge_DiscardEffect", "before": "PutCardInDiscardPile(card);", "after": "PutCardInDiscardPile(0u);", "case_ids": ["Scavenge_DiscardEffect-0", "Scavenge_DiscardEffect-1"]}
# <<< factory-mutation Scavenge_DiscardEffect

# >>> factory-mutation CreateListOfFireEnergyAttachedToArena
MUTATIONS["CreateListOfFireEnergyAttachedToArena"] = {"source_symbol": "CreateListOfFireEnergyAttachedToArena", "before": "return CreateListOfEnergyAttachedToArena(0x08u);", "after": "return CreateListOfEnergyAttachedToArena(0x03u);", "case_ids": ["CreateListOfFireEnergyAttachedToArena-0", "CreateListOfFireEnergyAttachedToArena-1"]}
# <<< factory-mutation CreateListOfFireEnergyAttachedToArena
# >>> factory-mutation CreateEnergyCardListFromDiscardPile_AllEnergy
MUTATIONS["CreateEnergyCardListFromDiscardPile_AllEnergy"] = {"source_symbol": "CreateEnergyCardListFromDiscardPile_AllEnergy", "before": "return CreateEnergyCardListFromDiscardPile(0x00u);", "after": "return CreateEnergyCardListFromDiscardPile(0x01u);", "case_ids": ["CreateEnergyCardListFromDiscardPile_AllEnergy-0", "CreateEnergyCardListFromDiscardPile_AllEnergy-1"]}
# <<< factory-mutation CreateEnergyCardListFromDiscardPile_AllEnergy
# >>> factory-mutation CheckIfDeckIsEmpty
MUTATIONS["CheckIfDeckIsEmpty"] = {"source_symbol": "CheckIfDeckIsEmpty", "before": "if (count.a == DECK_SIZE)", "after": "if (count.a != DECK_SIZE)", "case_ids": ["CheckIfDeckIsEmpty-0", "CheckIfDeckIsEmpty-1"]}
# <<< factory-mutation CheckIfDeckIsEmpty
# >>> factory-mutation VictreebelLure_AssertPokemonInBench
MUTATIONS["VictreebelLure_AssertPokemonInBench"] = {"source_symbol": "VictreebelLure_AssertPokemonInBench", "before": "return (VictreebelLureAssertPokemonInBenchResult){", "after": "return (VictreebelLureAssertPokemonInBenchResult){0u, 0u, EffectNoPokemonOnTheBenchText};", "case_ids": ["VictreebelLure_AssertPokemonInBench-0", "VictreebelLure_AssertPokemonInBench-1"]}
# <<< factory-mutation VictreebelLure_AssertPokemonInBench
# >>> factory-mutation Toxic_DoublePoisonEffect
MUTATIONS["Toxic_DoublePoisonEffect"] = {"source_symbol": "Toxic_DoublePoisonEffect", "before": "return DoublePoisonEffect();", "after": "return PoisonEffect();", "case_ids": ["Toxic_DoublePoisonEffect-0", "Toxic_DoublePoisonEffect-1"]}
# <<< factory-mutation Toxic_DoublePoisonEffect
# >>> factory-mutation NinetalesLure_CheckBench
MUTATIONS["NinetalesLure_CheckBench"] = {"source_symbol": "NinetalesLure_CheckBench", "before": "effect_compare(count.a, 2u)", "after": "effect_compare(count.a, 3u)", "case_ids": ["NinetalesLure_CheckBench-0", "NinetalesLure_CheckBench-1"]}
# <<< factory-mutation NinetalesLure_CheckBench
# >>> factory-mutation ScoopUp_BenchCheck
MUTATIONS["ScoopUp_BenchCheck"] = {"source_symbol": "ScoopUp_BenchCheck", "before": "effect_compare(count.a, 2u)", "after": "effect_compare(count.a, 3u)", "case_ids": ["ScoopUp_BenchCheck-0", "ScoopUp_BenchCheck-1"]}
# <<< factory-mutation ScoopUp_BenchCheck
# >>> factory-mutation MysteriousFossil_BenchCheck
MUTATIONS["MysteriousFossil_BenchCheck"] = {"source_symbol": "MysteriousFossil_BenchCheck", "before": "count.a == 6u", "after": "count.a == 5u", "case_ids": ["MysteriousFossil_BenchCheck-0", "MysteriousFossil_BenchCheck-1"]}
# <<< factory-mutation MysteriousFossil_BenchCheck
# >>> factory-mutation TrainerCardAsPokemon_BenchCheck
MUTATIONS["TrainerCardAsPokemon_BenchCheck"] = {"source_symbol": "TrainerCardAsPokemon_BenchCheck", "before": "effect_compare(count.a, 2u)", "after": "effect_compare(count.a, 3u)", "case_ids": ["TrainerCardAsPokemon_BenchCheck-0", "TrainerCardAsPokemon_BenchCheck-1"]}
# <<< factory-mutation TrainerCardAsPokemon_BenchCheck
# >>> factory-mutation VictreebelLure_AssertPokemonInBench
MUTATIONS["VictreebelLure_AssertPokemonInBench"] = {"source_symbol": "VictreebelLure_AssertPokemonInBench", "before": "effect_compare(count.a, 2u)", "after": "effect_compare(count.a, 3u)", "case_ids": ["VictreebelLure_AssertPokemonInBench-0", "VictreebelLure_AssertPokemonInBench-1"]}
# <<< factory-mutation VictreebelLure_AssertPokemonInBench
# >>> factory-mutation ThunderboltEffect
MUTATIONS["ThunderboltEffect"] = {"source_symbol": "ThunderboltEffect", "before": "if (card == 0xffu)", "after": "if (card == 0xfeu)", "case_ids": ["ThunderboltEffect-0", "ThunderboltEffect-1"]}
# <<< factory-mutation ThunderboltEffect
# >>> factory-mutation TrainerCardAsPokemon_DiscardEffect
MUTATIONS["TrainerCardAsPokemon_DiscardEffect"] = {"source_symbol": "TrainerCardAsPokemon_DiscardEffect", "before": "if (location == PLAY_AREA_ARENA)", "after": "if (location != PLAY_AREA_ARENA)", "case_ids": ["TrainerCardAsPokemon_DiscardEffect-0", "TrainerCardAsPokemon_DiscardEffect-1"]}
# <<< factory-mutation TrainerCardAsPokemon_DiscardEffect
# >>> factory-mutation MysteriousFossil_PlaceInPlayAreaEffect
MUTATIONS["MysteriousFossil_PlaceInPlayAreaEffect"] = {"source_symbol": "MysteriousFossil_PlaceInPlayAreaEffect", "before": "hTempCardIndex_ff9f", "after": "hTempCardIndex_ff9f + 1u", "case_ids": ["MysteriousFossil_PlaceInPlayAreaEffect-0", "MysteriousFossil_PlaceInPlayAreaEffect-1"]}
# <<< factory-mutation MysteriousFossil_PlaceInPlayAreaEffect
# >>> factory LeekSlap_OncePerDuelCheck
CONTRACT["LeekSlap_OncePerDuelCheck"] = {"compare": ("f",), "preserve": ()}
CASES["LeekSlap_OncePerDuelCheck"] = [{}, {"wram": {0xC200: b"\x40"}}]
# <<< factory LeekSlap_OncePerDuelCheck
# >>> factory LeekSlap_SetUsedThisDuelFlag
CONTRACT["LeekSlap_SetUsedThisDuelFlag"] = {"compare": (), "preserve": ()}
CASES["LeekSlap_SetUsedThisDuelFlag"] = [{}]
# <<< factory LeekSlap_SetUsedThisDuelFlag
# >>> factory PlusPowerEffect
CONTRACT["PlusPowerEffect"] = {"compare": (), "preserve": ()}
CASES["PlusPowerEffect"] = [{"wram": {0xFF9F: b"\x01"}}]
# <<< factory PlusPowerEffect
# >>> factory StepIn_BenchCheck
CONTRACT["StepIn_BenchCheck"] = {"compare": ("f", "hl"), "preserve": ()}
CASES["StepIn_BenchCheck"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BC: b"\xFF", 0xC3BC: b"\xFF"}},
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x01", 0xC2BC: b"\xFF",
              0xC3BC: b"\xFF"}},
]
# <<< factory StepIn_BenchCheck
# >>> factory StrikesBackEffect
CONTRACT["StrikesBackEffect"] = {"compare": ("f",), "preserve": ()}
CASES["StrikesBackEffect"] = [{}, dict(POISON)]
# <<< factory StrikesBackEffect
# >>> factory Switch_BenchCheck
CONTRACT["Switch_BenchCheck"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Switch_BenchCheck"] = [{}, {"a": 2}, {"a": 6}]
# <<< factory Switch_BenchCheck
# >>> factory Switch_SwitchEffect
CONTRACT["Switch_SwitchEffect"] = {"compare": (), "preserve": ()}
CASES["Switch_SwitchEffect"] = [{"wram": {0xFFA0: b"\x01"}}]
# <<< factory Switch_SwitchEffect
# >>> factory-mutation LeekSlap_OncePerDuelCheck
MUTATIONS["LeekSlap_OncePerDuelCheck"] = {"source_symbol": "LeekSlap_OncePerDuelCheck", "before": "USED_LEEK_SLAP_THIS_DUEL_F", "after": "USED_LEEK_SLAP_THIS_DUEL_F + 1u", "case_ids": ["LeekSlap_OncePerDuelCheck-0"]}
# <<< factory-mutation LeekSlap_OncePerDuelCheck
# >>> factory-mutation LeekSlap_SetUsedThisDuelFlag
MUTATIONS["LeekSlap_SetUsedThisDuelFlag"] = {"source_symbol": "LeekSlap_SetUsedThisDuelFlag", "before": "USED_LEEK_SLAP_THIS_DUEL_F", "after": "USED_LEEK_SLAP_THIS_DUEL_F + 1u", "case_ids": ["LeekSlap_SetUsedThisDuelFlag-0"]}
# <<< factory-mutation LeekSlap_SetUsedThisDuelFlag
# >>> factory-mutation PlusPowerEffect
MUTATIONS["PlusPowerEffect"] = {"source_symbol": "PlusPowerEffect", "before": " + 1u", "after": " + 2u", "case_ids": ["PlusPowerEffect-0"]}
# <<< factory-mutation PlusPowerEffect
# >>> factory-mutation StepIn_BenchCheck
MUTATIONS["StepIn_BenchCheck"] = {"source_symbol": "StepIn_BenchCheck", "before": "PLAY_AREA_ARENA", "after": "PLAY_AREA_ARENA + 1u", "case_ids": ["StepIn_BenchCheck-0", "StepIn_BenchCheck-1"]}
# <<< factory-mutation StepIn_BenchCheck
# >>> factory-mutation StrikesBackEffect
MUTATIONS["StrikesBackEffect"] = {"source_symbol": "StrikesBackEffect", "before": "0x10u", "after": "0x00u", "case_ids": ["StrikesBackEffect-0"]}
# <<< factory-mutation StrikesBackEffect
# >>> factory-mutation Switch_BenchCheck
MUTATIONS["Switch_BenchCheck"] = {"source_symbol": "Switch_BenchCheck", "before": "effect_compare(count.a, 2u)", "after": "effect_compare(count.a, 3u)", "case_ids": ["Switch_BenchCheck-0", "Switch_BenchCheck-1", "Switch_BenchCheck-2"]}
# <<< factory-mutation Switch_BenchCheck
# >>> factory-mutation Switch_SwitchEffect
MUTATIONS["Switch_SwitchEffect"] = {"source_symbol": "Switch_SwitchEffect", "before": "hTemp_ffa0", "after": "hTemp_ffa0 + 1u", "case_ids": ["Switch_SwitchEffect-0"]}
# <<< factory-mutation Switch_SwitchEffect
# >>> factory TryGiveDamageCounter_StrangeBehavior
CONTRACT["TryGiveDamageCounter_StrangeBehavior"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["TryGiveDamageCounter_StrangeBehavior"] = [
    {"wram": {0xFFA0: b"\x00", 0xFFA1: b"\x01", 0xC0C8: b"\x20", 0xC0C9: b"\x30"}, "read": {0xC100: 0x900}},
    dict(POISON, wram={0xFFA0: b"\x00", 0xFFA1: b"\x01", 0xC0C8: b"\x0A", 0xC0C9: b"\x20"}, read={0xC100: 0x900}),
    {"b": 1, "c": 2, "d": 3, "e": 4, "wram": {0xFFA0: b"\x01", 0xFFA1: b"\x00", 0xC0C8: b"\x20", 0xC0C9: b"\x30"}, "read": {0xC100: 0x900}},
]
# <<< factory TryGiveDamageCounter_StrangeBehavior
# >>> factory SpacingOut_CheckDamage
CONTRACT["SpacingOut_CheckDamage"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d")}
CASES["SpacingOut_CheckDamage"] = [
    {"wram": {0xC0BB: b"\x01", 0xC0C8: b"\x00"}},
    dict(POISON, wram={0xC0BB: b"\x01", 0xC0C8: b"\x0A"}),
    {"wram": {0xC0BB: b"\x01", 0xC0C8: b"\x14"}},
]
# <<< factory SpacingOut_CheckDamage
# >>> factory SpacingOut_HealEffect
CONTRACT["SpacingOut_HealEffect"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["SpacingOut_HealEffect"] = [
    {"wram": {0xFFA0: b"\x00", 0xC0BB: b"\x01", 0xC0C8: b"\x20"}},
    dict(POISON, wram={0xFFA0: b"\x01", 0xC0BB: b"\x01", 0xC0C8: b"\x20"}),
    {"a": 1, "f": 0x10, "wram": {0xFFA0: b"\x01", 0xC0BB: b"\x01", 0xC0C8: b"\x00"}},
]
# <<< factory SpacingOut_HealEffect
# >>> factory-mutation TryGiveDamageCounter_StrangeBehavior
MUTATIONS["TryGiveDamageCounter_StrangeBehavior"] = {"source_symbol": "TryGiveDamageCounter_StrangeBehavior", "before": "if (remaining == 0u)", "after": "if (remaining == 1u)", "case_ids": ["TryGiveDamageCounter_StrangeBehavior-0", "TryGiveDamageCounter_StrangeBehavior-1", "TryGiveDamageCounter_StrangeBehavior-2"]}
# <<< factory-mutation TryGiveDamageCounter_StrangeBehavior
# >>> factory-mutation SpacingOut_CheckDamage
MUTATIONS["SpacingOut_CheckDamage"] = {"source_symbol": "SpacingOut_CheckDamage", "before": "effect_compare(damage.a, 10u)", "after": "effect_compare(damage.a, 20u)", "case_ids": ["SpacingOut_CheckDamage-0", "SpacingOut_CheckDamage-1", "SpacingOut_CheckDamage-2"]}
# <<< factory-mutation SpacingOut_CheckDamage
# >>> factory-mutation SpacingOut_HealEffect
MUTATIONS["SpacingOut_HealEffect"] = {"source_symbol": "SpacingOut_HealEffect", "before": "uint8_t new_hp = (uint8_t)(10u + hp.a);", "after": "uint8_t new_hp = (uint8_t)(20u + hp.a);", "case_ids": ["SpacingOut_HealEffect-0", "SpacingOut_HealEffect-1", "SpacingOut_HealEffect-2"]}
# <<< factory-mutation SpacingOut_HealEffect
# >>> factory-mutation CheckIfCardIsBasicEnergy
MUTATIONS["CheckIfCardIsBasicEnergy"] = {"source_symbol": "CheckIfCardIsBasicEnergy", "before": "if (type >= TYPE_ENERGY_DOUBLE_COLORLESS)", "after": "if (type > TYPE_ENERGY_DOUBLE_COLORLESS)", "case_ids": ["CheckIfCardIsBasicEnergy-2"]}
# <<< factory-mutation CheckIfCardIsBasicEnergy
# >>> factory-mutation CopyPlayAreaHPToBackup_Unreferenced
MUTATIONS["CopyPlayAreaHPToBackup_Unreferenced"] = {"source_symbol": "CopyPlayAreaHPToBackup_Unreferenced", "before": "wBackupPlayerAreaHP_ADDR + i", "after": "wBackupPlayerAreaHP_ADDR + i + 1u", "case_ids": ["CopyPlayAreaHPToBackup_Unreferenced-0"]}
# <<< factory-mutation CopyPlayAreaHPToBackup_Unreferenced
# >>> factory-mutation CopyPlayAreaHPFromBackup_Unreferenced
MUTATIONS["CopyPlayAreaHPFromBackup_Unreferenced"] = {"source_symbol": "CopyPlayAreaHPFromBackup_Unreferenced", "before": "\t\tgb_write8((uint16_t)(wBackupPlayerAreaHP_ADDR + i", "after": "\t\tgb_write8((uint16_t)(wBackupPlayerAreaHP_ADDR + i + 1u", "case_ids": ["CopyPlayAreaHPFromBackup_Unreferenced-0"]}
# <<< factory-mutation CopyPlayAreaHPFromBackup_Unreferenced
# >>> factory-mutation EnergySearch_DeckCheck
MUTATIONS["EnergySearch_DeckCheck"] = {"source_symbol": "EnergySearch_DeckCheck", "before": "count.a == DECK_SIZE", "after": "count.a != DECK_SIZE", "case_ids": ["EnergySearch_DeckCheck-0", "EnergySearch_DeckCheck-1"]}
# <<< factory-mutation EnergySearch_DeckCheck
# >>> factory-mutation Gale_LoadAnimation
MUTATIONS["Gale_LoadAnimation"] = {"source_symbol": "Gale_LoadAnimation", "before": "wLoadedAttackAnimation = 0x87u;", "after": "wLoadedAttackAnimation = 0x88u;", "case_ids": ["Gale_LoadAnimation-0", "Gale_LoadAnimation-1"]}
# <<< factory-mutation Gale_LoadAnimation
# >>> factory-mutation CreatePlayableStage2PokemonCardListFromHand
MUTATIONS["CreatePlayableStage2PokemonCardListFromHand"] = {"source_symbol": "CreatePlayableStage2PokemonCardListFromHand", "before": "gb_write8(dst, 0xffu);", "after": "gb_write8(dst, 0xfeu);", "case_ids": ["CreatePlayableStage2PokemonCardListFromHand-0", "CreatePlayableStage2PokemonCardListFromHand-1"]}
# <<< factory-mutation CreatePlayableStage2PokemonCardListFromHand
# >>> factory-mutation PickRandomBasicCardFromDeck
MUTATIONS["PickRandomBasicCardFromDeck"] = {"source_symbol": "PickRandomBasicCardFromDeck", "before": "wLoadedCard2Type >= TYPE_ENERGY", "after": "wLoadedCard2Type > TYPE_ENERGY", "case_ids": ["PickRandomBasicCardFromDeck-0", "PickRandomBasicCardFromDeck-1"]}
# <<< factory-mutation PickRandomBasicCardFromDeck
# >>> factory-mutation StepIn_SwitchEffect
MUTATIONS["StepIn_SwitchEffect"] = {"source_symbol": "StepIn_SwitchEffect", "before": "SwapArenaWithBenchPokemon(hTemp_ffa0)", "after": "SwapArenaWithBenchPokemon((uint8_t)(hTemp_ffa0 + 1u))", "case_ids": ["StepIn_SwitchEffect-0"]}
# <<< factory-mutation StepIn_SwitchEffect
# >>> factory-mutation Barrier_DiscardEffect
MUTATIONS["Barrier_DiscardEffect"] = {"source_symbol": "Barrier_DiscardEffect", "before": "\treturn value;", "after": "\treturn 0u;", "case_ids": ["Barrier_DiscardEffect-1", "Barrier_DiscardEffect-2", "Barrier_DiscardEffect-3"]}
# <<< factory-mutation Barrier_DiscardEffect
# >>> factory-mutation DestinyBond_DiscardEffect
MUTATIONS["DestinyBond_DiscardEffect"] = {"source_symbol": "DestinyBond_DiscardEffect", "before": "gb_read8(hTempList_ADDR)", "after": "gb_read8((uint16_t)(hTempList_ADDR + 1u))", "case_ids": ["DestinyBond_DiscardEffect-0", "DestinyBond_DiscardEffect-1"]}
# <<< factory-mutation DestinyBond_DiscardEffect
# >>> factory-mutation Ember_DiscardEffect
MUTATIONS["Ember_DiscardEffect"] = {"source_symbol": "Ember_DiscardEffect", "before": "PutCardInDiscardPile(hTemp_ffa0);", "after": "PutCardInDiscardPile(0u);", "case_ids": ["Ember_DiscardEffect-0", "Ember_DiscardEffect-1"]}
# <<< factory-mutation Ember_DiscardEffect
# >>> factory-mutation FireBlast_DiscardEffect
MUTATIONS["FireBlast_DiscardEffect"] = {"source_symbol": "FireBlast_DiscardEffect", "before": "PutCardInDiscardPile(hTemp_ffa0);", "after": "PutCardInDiscardPile(0u);", "case_ids": ["FireBlast_DiscardEffect-0", "FireBlast_DiscardEffect-1"]}
# <<< factory-mutation FireBlast_DiscardEffect
# >>> factory-mutation FireSpin_AISelectEffect
MUTATIONS["FireSpin_AISelectEffect"] = {"source_symbol": "FireSpin_AISelectEffect", "before": "\tgb_write8(hTempList_ADDR, gb_read8(wDuelTempList_ADDR", "after": "\tgb_write8(hTempList_ADDR, gb_read8((uint16_t)(wDuelTempList_ADDR + 1u)", "case_ids": ["FireSpin_AISelectEffect-0", "FireSpin_AISelectEffect-1"]}
# <<< factory-mutation FireSpin_AISelectEffect
# >>> factory-mutation FireSpin_DiscardEffect
MUTATIONS["FireSpin_DiscardEffect"] = {"source_symbol": "FireSpin_DiscardEffect", "before": "\tPutCardInDiscardPile(gb_read8(hTempList_ADDR", "after": "\tPutCardInDiscardPile(gb_read8((uint16_t)(hTempList_ADDR + 1u)", "case_ids": ["FireSpin_DiscardEffect-0", "FireSpin_DiscardEffect-1"]}
# <<< factory-mutation FireSpin_DiscardEffect
# Keep schema-2 inventory after appended routine cases.
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)# >>> factory-mutation PidgeottoMirrorMove_InitialEffect1
MUTATIONS["PidgeottoMirrorMove_InitialEffect1"] = {"source_symbol": "PidgeottoMirrorMove_InitialEffect1", "before": "\treturn MirrorMove_InitialEffect1();", "after": "\treturn (MirrorMoveInitialEffect1Result){0};", "case_ids": ["PidgeottoMirrorMove_InitialEffect1-0", "PidgeottoMirrorMove_InitialEffect1-1"]}
# <<< factory-mutation PidgeottoMirrorMove_InitialEffect1
# >>> factory-mutation ClefairyMetronome_CheckAttacks
MUTATIONS["ClefairyMetronome_CheckAttacks"] = {"source_symbol": "ClefairyMetronome_CheckAttacks", "before": "\treturn (ClefairyMetronomeCheckAttacksResult){r.f, NoAttackMayBeChoosenText};", "after": "\treturn (ClefairyMetronomeCheckAttacksResult){r.f, 0};", "case_ids": ["ClefairyMetronome_CheckAttacks-0", "ClefairyMetronome_CheckAttacks-1"]}
# <<< factory-mutation ClefairyMetronome_CheckAttacks
# >>> factory-mutation Psychic_DamageBoostEffect
MUTATIONS["Psychic_DamageBoostEffect"] = {"source_symbol": "Psychic_DamageBoostEffect", "before": "\tgb_write8((uint16_t)(wDamage_ADDR + 1u), (uint8_t)(sum >> 8));", "after": "\tgb_write8(wDamage_ADDR, (uint8_t)(sum >> 8));", "case_ids": ["Psychic_DamageBoostEffect-1", "Psychic_DamageBoostEffect-2"]}
# <<< factory-mutation Psychic_DamageBoostEffect
# >>> factory-mutation Barrier_AISelectEffect
MUTATIONS["Barrier_AISelectEffect"] = {"source_symbol": "Barrier_AISelectEffect", "before": "\tuint8_t value = gb_read8(wDuelTempList_ADDR);", "after": "\tuint8_t value = gb_read8(hTemp_ffa0_ADDR);", "case_ids": ["Barrier_AISelectEffect-1", "Barrier_AISelectEffect-2"]}
# <<< factory-mutation Barrier_AISelectEffect
# >>> factory-mutation Whirlpool_AISelectEffect
MUTATIONS["Whirlpool_AISelectEffect"] = {
	"source_symbol": "Whirlpool_AISelectEffect",
	"before": "uint8_t a = AIPickEnergyCardToDiscardFromDefendingPokemon().a;\n\thTemp_ffa0 = a;",
	"after": "uint8_t a = AIPickEnergyCardToDiscardFromDefendingPokemon().a;\n\thTemp_ffa0 = (uint8_t)~a;",
	"case_ids": ["Whirlpool_AISelectEffect-0", "Whirlpool_AISelectEffect-1", "Whirlpool_AISelectEffect-2"],
}
# <<< factory-mutation Whirlpool_AISelectEffect
# >>> factory-mutation Whirlpool_DiscardEffect
MUTATIONS["Whirlpool_DiscardEffect"] = {
	"source_symbol": "Whirlpool_DiscardEffect",
	"before": "\tPutCardInDiscardPile(whirlpool_card);",
	"after": "\tPutCardInDiscardPile(whirlpool_card + 1u);",
	"case_ids": ["Whirlpool_DiscardEffect-0", "Whirlpool_DiscardEffect-1", "Whirlpool_DiscardEffect-4", "Whirlpool_DiscardEffect-5"],
}
# <<< factory-mutation Whirlpool_DiscardEffect
# >>> factory-mutation EnergyRemoval_EnergyCheck
MUTATIONS["EnergyRemoval_EnergyCheck"] = {
	"source_symbol": "EnergyRemoval_EnergyCheck",
	"before": "{r.f, NoEnergyAttachedToOpponentsActiveText}",
	"after": "{r.f, 0x00b6u}",
	"case_ids": ["EnergyRemoval_EnergyCheck-0", "EnergyRemoval_EnergyCheck-1"],
}
# <<< factory-mutation EnergyRemoval_EnergyCheck
# >>> factory-mutation EnergyRemoval_AISelection
MUTATIONS["EnergyRemoval_AISelection"] = {
	"source_symbol": "EnergyRemoval_AISelection",
	"before": "return AIPickEnergyCardToDiscardFromDefendingPokemon().a;",
	"after": "return AIPickEnergyCardToDiscardFromDefendingPokemon().a + 1u;",
	"case_ids": ["EnergyRemoval_AISelection-0", "EnergyRemoval_AISelection-1"],
}
# <<< factory-mutation EnergyRemoval_AISelection
# >>> factory-mutation EnergyRetrieval_HandEnergyCheck
MUTATIONS["EnergyRetrieval_HandEnergyCheck"] = {
	"source_symbol": "EnergyRetrieval_HandEnergyCheck",
	"before": "return (EnergyRetrievalHandEnergyCheckResult){NotEnoughCardsInHandText, 0x70u};",
	"after": "return (EnergyRetrievalHandEnergyCheckResult){NotEnoughCardsInHandText, 0x50u};",
	"case_ids": ["EnergyRetrieval_HandEnergyCheck-0", "EnergyRetrieval_HandEnergyCheck-1"],
}
# <<< factory-mutation EnergyRetrieval_HandEnergyCheck
# >>> factory-mutation MrMimeMeditate_AIEffect
MUTATIONS["MrMimeMeditate_AIEffect"] = {
	"source_symbol": "MrMimeMeditate_AIEffect",
	"before": "\tMrMimeMeditate_DamageBoostEffect();\n\tSetDefiniteAIDamage();",
	"after": "\tSetDefiniteAIDamage();\n\tSetDefiniteAIDamage();",
	"case_ids": ["MrMimeMeditate_AIEffect-1", "MrMimeMeditate_AIEffect-2"],
}
# <<< factory-mutation MrMimeMeditate_AIEffect
# >>> factory-mutation PsywaveEffect
MUTATIONS["PsywaveEffect"] = {
	"source_symbol": "PsywaveEffect",
	"before": "\tuint16_t de = GetEnergyAttachedMultiplierDamage();\n\tuint16_t hl = wDamage_ADDR;",
	"after": "\tuint16_t de = GetEnergyAttachedMultiplierDamage();\n\tuint16_t hl = (uint16_t)(wDamage_ADDR + 2u);",
	"case_ids": ["PsywaveEffect-0", "PsywaveEffect-1", "PsywaveEffect-2"],
}
# <<< factory-mutation PsywaveEffect
# >>> factory-mutation PokemonCenter_DamageCheck
MUTATIONS["PokemonCenter_DamageCheck"] = {"source_symbol": "PokemonCenter_DamageCheck", "before": "\treturn (PokemonCenterDamageCheckResult){r.f, NoPokemonWithDamageCountersText};", "after": "\treturn (PokemonCenterDamageCheckResult){r.f, ConditionsForEvolvingToStage2NotFulfilledText};", "case_ids": ["PokemonCenter_DamageCheck-0", "PokemonCenter_DamageCheck-1"]}
# <<< factory-mutation PokemonCenter_DamageCheck
# >>> factory-mutation PokemonBreeder_HandPlayAreaCheck
MUTATIONS["PokemonBreeder_HandPlayAreaCheck"] = {"source_symbol": "PokemonBreeder_HandPlayAreaCheck", "before": "\tif (f & 0x10u)", "after": "\tif (f & 0x20u)", "case_ids": ["PokemonBreeder_HandPlayAreaCheck-0", "PokemonBreeder_HandPlayAreaCheck-1"]}
# <<< factory-mutation PokemonBreeder_HandPlayAreaCheck
# >>> factory-mutation PokemonTrader_HandDeckCheck
MUTATIONS["PokemonTrader_HandDeckCheck"] = {"source_symbol": "PokemonTrader_HandDeckCheck", "before": "\tuint16_t message = ThereAreNoCardsInHandThatYouCanChangeText;", "after": "\tuint16_t message = ConditionsForEvolvingToStage2NotFulfilledText;", "case_ids": ["PokemonTrader_HandDeckCheck-0", "PokemonTrader_HandDeckCheck-1", "PokemonTrader_HandDeckCheck-2"]}
# <<< factory-mutation PokemonTrader_HandDeckCheck
# >>> factory-mutation VictreebelLure_GetBenchPokemonWithLowestHP
MUTATIONS["VictreebelLure_GetBenchPokemonWithLowestHP"] = {"source_symbol": "VictreebelLure_GetBenchPokemonWithLowestHP", "before": "\tAIFindTargetForBenchAttackResult target = AIFindTargetForBenchAttack();\n\thTemp_ffa0 = target.a;", "after": "\tAIFindTargetForBenchAttackResult target = AIFindTargetForBenchAttack();\n\thTemp_ffa0 = (uint8_t)(target.a ^ 0x01u);", "case_ids": ["VictreebelLure_GetBenchPokemonWithLowestHP-0", "VictreebelLure_GetBenchPokemonWithLowestHP-1"]}
# <<< factory-mutation VictreebelLure_GetBenchPokemonWithLowestHP
# >>> factory-mutation Sprout_CheckDeckAndPlayArea
MUTATIONS["Sprout_CheckDeckAndPlayArea"] = {"source_symbol": "Sprout_CheckDeckAndPlayArea", "before": "\treturn (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText, sprout_flags};", "after": "\treturn (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText + 1u, sprout_flags};", "case_ids": ["Sprout_CheckDeckAndPlayArea-0", "Sprout_CheckDeckAndPlayArea-1"]}
# <<< factory-mutation Sprout_CheckDeckAndPlayArea
# >>> factory-mutation NidoranFCallForFamily_CheckDeckAndPlayArea
MUTATIONS["NidoranFCallForFamily_CheckDeckAndPlayArea"] = {"source_symbol": "NidoranFCallForFamily_CheckDeckAndPlayArea", "before": "\treturn (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText, family_flags};", "after": "\treturn (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText + 1u, family_flags};", "case_ids": ["NidoranFCallForFamily_CheckDeckAndPlayArea-0", "NidoranFCallForFamily_CheckDeckAndPlayArea-1"]}
# <<< factory-mutation NidoranFCallForFamily_CheckDeckAndPlayArea
# >>> factory-mutation DragonairHyperBeam_AISelectEffect
MUTATIONS["DragonairHyperBeam_AISelectEffect"] = {"source_symbol": "DragonairHyperBeam_AISelectEffect", "before": "void DragonairHyperBeam_AISelectEffect(void)\n{\n\tAIPickEnergyCardToDiscardResult r = AIPickEnergyCardToDiscardFromDefendingPokemon();\n\thTemp_ffa0 = r.a;", "after": "void DragonairHyperBeam_AISelectEffect(void)\n{\n\tAIPickEnergyCardToDiscardResult r = AIPickEnergyCardToDiscardFromDefendingPokemon();\n\thTemp_ffa0 = (uint8_t)(r.a + 1u);", "case_ids": ["DragonairHyperBeam_AISelectEffect-0", "DragonairHyperBeam_AISelectEffect-1"]}
# <<< factory-mutation DragonairHyperBeam_AISelectEffect
# >>> factory-mutation ClefableMetronome_CheckAttacks
MUTATIONS["ClefableMetronome_CheckAttacks"] = {"source_symbol": "ClefableMetronome_CheckAttacks", "before": "\treturn (ClefableMetronomeCheckAttacksResult){r.f, NoAttackMayBeChoosenText};", "after": "\treturn (ClefableMetronomeCheckAttacksResult){r.f, (uint16_t)(NoAttackMayBeChoosenText + 1u)};", "case_ids": ["ClefableMetronome_CheckAttacks-0", "ClefableMetronome_CheckAttacks-1"]}
# <<< factory-mutation ClefableMetronome_CheckAttacks
# >>> factory-mutation Scavenge_CheckDiscardPile
MUTATIONS["Scavenge_CheckDiscardPile"] = {"source_symbol": "Scavenge_CheckDiscardPile", "before": "\t\treturn (ScavengeCheckDiscardPileResult){NotEnoughPsychicEnergyText, 0x70u};", "after": "\t\treturn (ScavengeCheckDiscardPileResult){ThereAreNoTrainerCardsInDiscardPileText, 0x70u};", "case_ids": ["Scavenge_CheckDiscardPile-0", "Scavenge_CheckDiscardPile-1"]}
# <<< factory-mutation Scavenge_CheckDiscardPile
# >>> factory-mutation Scavenge_AISelectEffect
MUTATIONS["Scavenge_AISelectEffect"] = {"source_symbol": "Scavenge_AISelectEffect", "before": "\thTemp_ffa0 = wDuelTempList;", "after": "\thTempPlayAreaLocation_ffa1 = wDuelTempList;", "case_ids": ["Scavenge_AISelectEffect-1"]}
# <<< factory-mutation Scavenge_AISelectEffect
# >>> factory-mutation SlowpokeAmnesia_CheckAttacks
MUTATIONS["SlowpokeAmnesia_CheckAttacks"] = {"source_symbol": "SlowpokeAmnesia_CheckAttacks", "before": "\treturn (SlowpokeAmnesiaCheckAttacksResult){r.f, NoAttackMayBeChoosenText};", "after": "\treturn (SlowpokeAmnesiaCheckAttacksResult){r.f, NotEnoughPsychicEnergyText};", "case_ids": ["SlowpokeAmnesia_CheckAttacks-0", "SlowpokeAmnesia_CheckAttacks-1"]}
# <<< factory-mutation SlowpokeAmnesia_CheckAttacks
# >>> factory-mutation DevolutionBeam_CheckPlayArea
MUTATIONS["DevolutionBeam_CheckPlayArea"] = {"source_symbol": "DevolutionBeam_CheckPlayArea", "before": "if ((r.f & 0x10u) == 0u)", "after": "if ((r.f & 0x10u) != 0u)", "case_ids": ["DevolutionBeam_CheckPlayArea-0", "DevolutionBeam_CheckPlayArea-1"]}
# <<< factory-mutation DevolutionBeam_CheckPlayArea
# >>> factory-mutation DevolutionBeam_AISelectEffect
MUTATIONS["DevolutionBeam_AISelectEffect"] = {"source_symbol": "DevolutionBeam_AISelectEffect", "before": "\thTempPlayAreaLocation_ffa1 = r.a;", "after": "\thTempPlayAreaLocation_ffa1 = (uint8_t)(r.a + 1u);", "case_ids": ["DevolutionBeam_AISelectEffect-0", "DevolutionBeam_AISelectEffect-1"]}
# <<< factory-mutation DevolutionBeam_AISelectEffect
# >>> factory-mutation MewtwoAltEnergyAbsorption_CheckDiscardPile
MUTATIONS["MewtwoAltEnergyAbsorption_CheckDiscardPile"] = {"source_symbol": "MewtwoAltEnergyAbsorption_CheckDiscardPile", "before": "\treturn (CreateEnergyCardListFromDiscardPileResult){ThereAreNoEnergyCardsInDiscardPileText, r.f};", "after": "\treturn (CreateEnergyCardListFromDiscardPileResult){ThereAreNoStage1PokemonText, r.f};", "case_ids": ["MewtwoAltEnergyAbsorption_CheckDiscardPile-0", "MewtwoAltEnergyAbsorption_CheckDiscardPile-1"]}
# <<< factory-mutation MewtwoAltEnergyAbsorption_CheckDiscardPile
# >>> factory-mutation MewtwoAltEnergyAbsorption_AISelectEffect
MUTATIONS["MewtwoAltEnergyAbsorption_AISelectEffect"] = {"source_symbol": "MewtwoAltEnergyAbsorption_AISelectEffect", "before": "MewtwoAltEnergyAbsorptionAISelectEffectResult MewtwoAltEnergyAbsorption_AISelectEffect(void)\n{\n\t(void)CreateEnergyCardListFromDiscardPile_AllEnergy();\n\tuint16_t hl = wDuelTempList_ADDR;", "after": "MewtwoAltEnergyAbsorptionAISelectEffectResult MewtwoAltEnergyAbsorption_AISelectEffect(void)\n{\n\t(void)CreateEnergyCardListFromDiscardPile_AllEnergy();\n\tuint16_t hl = (uint16_t)(wDuelTempList_ADDR + 1u);", "case_ids": ["MewtwoAltEnergyAbsorption_AISelectEffect-0", "MewtwoAltEnergyAbsorption_AISelectEffect-1"]}
# <<< factory-mutation MewtwoAltEnergyAbsorption_AISelectEffect
# >>> factory-mutation MewtwoEnergyAbsorption_CheckDiscardPile
MUTATIONS["MewtwoEnergyAbsorption_CheckDiscardPile"] = {"source_symbol": "MewtwoEnergyAbsorption_CheckDiscardPile", "before": "\t\tThereAreNoEnergyCardsInDiscardPileText, r.f, 0u, 0u, wDuelTempList_ADDR", "after": "\t\t(uint16_t)(ThereAreNoEnergyCardsInDiscardPileText + 1u), r.f, 0u, 0u, wDuelTempList_ADDR", "case_ids": ["MewtwoEnergyAbsorption_CheckDiscardPile-0", "MewtwoEnergyAbsorption_CheckDiscardPile-1"]}
# <<< factory-mutation MewtwoEnergyAbsorption_CheckDiscardPile
# >>> factory-mutation MewtwoEnergyAbsorption_AISelectEffect
MUTATIONS["MewtwoEnergyAbsorption_AISelectEffect"] = {"source_symbol": "MewtwoEnergyAbsorption_AISelectEffect", "before": "MewtwoEnergyAbsorptionAISelectEffectResult MewtwoEnergyAbsorption_AISelectEffect(void)\n{\n\t(void)CreateEnergyCardListFromDiscardPile_AllEnergy();\n\tuint16_t hl = wDuelTempList_ADDR;", "after": "MewtwoEnergyAbsorptionAISelectEffectResult MewtwoEnergyAbsorption_AISelectEffect(void)\n{\n\t(void)CreateEnergyCardListFromDiscardPile_AllEnergy();\n\tuint16_t hl = (uint16_t)(wDuelTempList_ADDR + 1u);", "case_ids": ["MewtwoEnergyAbsorption_AISelectEffect-0", "MewtwoEnergyAbsorption_AISelectEffect-1"]}
# <<< factory-mutation MewtwoEnergyAbsorption_AISelectEffect
# >>> factory-mutation JynxMeditate_AIEffect
MUTATIONS["JynxMeditate_AIEffect"] = {"source_symbol": "JynxMeditate_AIEffect", "before": "void JynxMeditate_AIEffect(void)\n{\n\tJynxMeditate_DamageBoostEffect();\n\tSetDefiniteAIDamage();\n}", "after": "void JynxMeditate_AIEffect(void)\n{\n\tJynxMeditate_DamageBoostEffect();\n\tJynxMeditate_DamageBoostEffect();\n}", "case_ids": ["JynxMeditate_AIEffect-1"]}
# <<< factory-mutation JynxMeditate_AIEffect
# >>> factory-mutation MysteryAttack_RandomEffect
MUTATIONS["MysteryAttack_RandomEffect"] = {"source_symbol": "MysteryAttack_RandomEffect", "before": "\thTemp_ffa0 = effect;", "after": "\thTemp_ffa0 = (uint8_t)(effect + 1u);", "case_ids": ["MysteryAttack_RandomEffect-0", "MysteryAttack_RandomEffect-1"]}
# <<< factory-mutation MysteryAttack_RandomEffect
# >>> factory-mutation MarowakCallForFamily_CheckDeckAndPlayArea
MUTATIONS["MarowakCallForFamily_CheckDeckAndPlayArea"] = {
    "source_symbol": "MarowakCallForFamily_CheckDeckAndPlayArea",
    "before": "\t\t| (v.a >= MAX_PLAY_AREA_POKEMON ? 0x10u : 0x00u));",
    "after": "\t\t| (v.a >= MAX_PLAY_AREA_POKEMON ? 0x00u : 0x10u));",
    "case_ids": ["MarowakCallForFamily_CheckDeckAndPlayArea-0", "MarowakCallForFamily_CheckDeckAndPlayArea-1"],
}
# <<< factory-mutation MarowakCallForFamily_CheckDeckAndPlayArea
# >>> factory-mutation IceBreath_ZeroDamage
MUTATIONS["IceBreath_ZeroDamage"] = {
    "source_symbol": "IceBreath_ZeroDamage",
    "before": "\tuint8_t ice_breath_damage = 0u;",
    "after": "\tuint8_t ice_breath_damage = 0x10u;",
    "case_ids": ["IceBreath_ZeroDamage-0", "IceBreath_ZeroDamage-1", "IceBreath_ZeroDamage-2"],
}
# <<< factory-mutation IceBreath_ZeroDamage
# >>> factory-mutation AIPickFireEnergyCardToDiscard
MUTATIONS["AIPickFireEnergyCardToDiscard"] = {
    "source_symbol": "AIPickFireEnergyCardToDiscard",
    "before": "\thTemp_ffa0 = gb_read8(wDuelTempList_ADDR);",
    "after": "\thTemp_ffa0 = gb_read8((uint16_t)(wDuelTempList_ADDR + 1u));",
    "case_ids": ["AIPickFireEnergyCardToDiscard-0", "AIPickFireEnergyCardToDiscard-1", "AIPickFireEnergyCardToDiscard-2"],
}
# <<< factory-mutation AIPickFireEnergyCardToDiscard
# >>> factory-mutation FlamesOfRage_AIEffect
MUTATIONS["FlamesOfRage_AIEffect"] = {
    "source_symbol": "FlamesOfRage_AIEffect",
    "before": "\tFlamesOfRage_DamageBoostEffect();\n\tSetDefiniteAIDamage();",
    "after": "\tFlamesOfRage_DamageBoostEffect();\n\t(void)0;",
    "case_ids": ["FlamesOfRage_AIEffect-2"],
}
# <<< factory-mutation FlamesOfRage_AIEffect
# >>> factory-mutation ArcanineFlamethrower_AISelectEffect
MUTATIONS["ArcanineFlamethrower_AISelectEffect"] = {
	"source_symbol": "ArcanineFlamethrower_AISelectEffect",
	"before": "void ArcanineFlamethrower_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}",
	"after": "void ArcanineFlamethrower_AISelectEffect(void)\n{\n}",
	"case_ids": ["ArcanineFlamethrower_AISelectEffect-1", "ArcanineFlamethrower_AISelectEffect-2"],
}
# <<< factory-mutation ArcanineFlamethrower_AISelectEffect
# >>> factory-mutation FlamesOfRage_AISelectEffect
MUTATIONS["FlamesOfRage_AISelectEffect"] = {
	"source_symbol": "FlamesOfRage_AISelectEffect",
	"before": "void FlamesOfRage_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n\tgb_write8((uint16_t)(hTempList_ADDR + 1u), gb_read8((uint16_t)(wDuelTempList_ADDR + 1u)));\n}",
	"after": "void FlamesOfRage_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n\tgb_write8((uint16_t)(hTempList_ADDR + 0u), gb_read8((uint16_t)(wDuelTempList_ADDR + 1u)));\n}",
	"case_ids": ["FlamesOfRage_AISelectEffect-1", "FlamesOfRage_AISelectEffect-2"],
}
# <<< factory-mutation FlamesOfRage_AISelectEffect
# >>> factory-mutation FireBlast_AISelectEffect
MUTATIONS["FireBlast_AISelectEffect"] = {
	"source_symbol": "FireBlast_AISelectEffect",
	"before": "void FireBlast_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}",
	"after": "void FireBlast_AISelectEffect(void)\n{\n}",
	"case_ids": ["FireBlast_AISelectEffect-1", "FireBlast_AISelectEffect-2"],
}
# <<< factory-mutation FireBlast_AISelectEffect
# >>> factory-mutation EnergyConversion_CheckEnergy
MUTATIONS["EnergyConversion_CheckEnergy"] = {"source_symbol": "EnergyConversion_CheckEnergy", "before": "\treturn (EnergyConversionCheckEnergyResult){ThereAreNoEnergyCardsInDiscardPileText, r.f};", "after": "\treturn (EnergyConversionCheckEnergyResult){ThereAreNoEnergyCardsInDiscardPileText, 0u};", "case_ids": ["EnergyConversion_CheckEnergy-0", "EnergyConversion_CheckEnergy-1"]}
# <<< factory-mutation EnergyConversion_CheckEnergy
# >>> factory-mutation EnergyConversion_AISelectEffect
MUTATIONS["EnergyConversion_AISelectEffect"] = {"source_symbol": "EnergyConversion_AISelectEffect", "before": "if (value == 0xffu)", "after": "if (value == 0xfeu)", "case_ids": ["EnergyConversion_AISelectEffect-0", "EnergyConversion_AISelectEffect-1"]}
# <<< factory-mutation EnergyConversion_AISelectEffect
# >>> factory-mutation HypnoDarkMind_AISelectEffect
MUTATIONS["HypnoDarkMind_AISelectEffect"] = {"source_symbol": "HypnoDarkMind_AISelectEffect", "before": "gb_write8(hTemp_ffa0_ADDR, 0xffu);", "after": "gb_write8(hTemp_ffa0_ADDR, 0u);", "case_ids": ["HypnoDarkMind_AISelectEffect-0", "HypnoDarkMind_AISelectEffect-1", "HypnoDarkMind_AISelectEffect-2"]}
# <<< factory-mutation HypnoDarkMind_AISelectEffect
# >>> factory-mutation AIPickAttackForAmnesia
MUTATIONS["AIPickAttackForAmnesia"] = {"source_symbol": "AIPickAttackForAmnesia", "before": "\t\tif (check.f & 0x10u) {", "after": "\t\tif (!(check.f & 0x10u)) {", "case_ids": ["AIPickAttackForAmnesia-0", "AIPickAttackForAmnesia-1"]}
# <<< factory-mutation AIPickAttackForAmnesia
# >>> factory-mutation MirrorMove_AISelection
MUTATIONS["MirrorMove_AISelection"] = {
    "source_symbol": "MirrorMove_AISelection",
    "before": "hTemp_ffa0 = 0xFFu;",
    "after": "hTemp_ffa0 = 0xFEu;",
    "case_ids": ["MirrorMove_AISelection-0", "MirrorMove_AISelection-1"],
}
# <<< factory-mutation MirrorMove_AISelection
# >>> factory-mutation KinglerFlail_HPCheck
MUTATIONS["KinglerFlail_HPCheck"] = {
    "source_symbol": "KinglerFlail_HPCheck",
    "before": "\tSetDefiniteDamage(r.a);",
    "after": "\tSetDefiniteDamage((uint8_t)(r.a + 1u));",
    "case_ids": ["KinglerFlail_HPCheck-0", "KinglerFlail_HPCheck-1", "KinglerFlail_HPCheck-2"],
}
# <<< factory-mutation KinglerFlail_HPCheck
# >>> factory-mutation MagikarpFlail_HPCheck
MUTATIONS["MagikarpFlail_HPCheck"] = {
    "source_symbol": "MagikarpFlail_HPCheck",
    "before": "void MagikarpFlail_HPCheck(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSetDefiniteDamage(r.a);\n}",
    "after": "void MagikarpFlail_HPCheck(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSetDefiniteDamage((uint8_t)(r.a + 1u));\n}",
    "case_ids": ["MagikarpFlail_HPCheck-0", "MagikarpFlail_HPCheck-1", "MagikarpFlail_HPCheck-2"],
}
# <<< factory-mutation MagikarpFlail_HPCheck
# >>> factory-mutation SuperFang_HalfHPEffect
MUTATIONS["SuperFang_HalfHPEffect"] = {
    "source_symbol": "SuperFang_HalfHPEffect",
    "before": "\tSetDefiniteDamage(damage);",
    "after": "\tSetDefiniteDamage((uint8_t)(damage + 1u));",
    "case_ids": ["SuperFang_HalfHPEffect-0", "SuperFang_HalfHPEffect-1", "SuperFang_HalfHPEffect-2", "SuperFang_HalfHPEffect-3"],
}
# <<< factory-mutation SuperFang_HalfHPEffect
# >>> factory-mutation KarateChop_DamageSubtractionEffect
MUTATIONS["KarateChop_DamageSubtractionEffect"] = {
    "source_symbol": "KarateChop_DamageSubtractionEffect",
    "before": "uint16_t remaining = (uint16_t)(damage_value - (uint16_t)damage.a);",
    "after": "uint16_t remaining = (uint16_t)(damage_value - (uint16_t)(damage.a + 1u));",
    "case_ids": ["KarateChop_DamageSubtractionEffect-0", "KarateChop_DamageSubtractionEffect-1", "KarateChop_DamageSubtractionEffect-2", "KarateChop_DamageSubtractionEffect-3"],
}
# <<< factory-mutation KarateChop_DamageSubtractionEffect
# >>> factory-mutation SpearowMirrorMove_AISelection
MUTATIONS["SpearowMirrorMove_AISelection"] = {"source_symbol": "SpearowMirrorMove_AISelection", "before": "MirrorMove_AISelection();", "after": "(void)0;", "case_ids": ["SpearowMirrorMove_AISelection-0", "SpearowMirrorMove_AISelection-1"]}
# <<< factory-mutation SpearowMirrorMove_AISelection
# >>> factory-mutation CharmeleonFlamethrower_AISelectEffect
MUTATIONS["CharmeleonFlamethrower_AISelectEffect"] = {
    "source_symbol": "CharmeleonFlamethrower_AISelectEffect",
    "before": "void CharmeleonFlamethrower_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}",
    "after": "void CharmeleonFlamethrower_AISelectEffect(void)\n{\n}",
    "case_ids": ["CharmeleonFlamethrower_AISelectEffect-1", "CharmeleonFlamethrower_AISelectEffect-2"],
}
# <<< factory-mutation CharmeleonFlamethrower_AISelectEffect
# >>> factory-mutation ClefableMetronome_AISelectEffect
MUTATIONS["ClefableMetronome_AISelectEffect"] = {"source_symbol": "ClefableMetronome_AISelectEffect", "before": "HandleAIMetronomeEffect();", "after": "gb_write8(0xC100u, 0xFFu);", "case_ids": ["ClefableMetronome_AISelectEffect-0", "ClefableMetronome_AISelectEffect-1"]}
# <<< factory-mutation ClefableMetronome_AISelectEffect
# >>> factory-mutation Ember_AISelectEffect
MUTATIONS["Ember_AISelectEffect"] = {
    "source_symbol": "Ember_AISelectEffect",
    "before": "void Ember_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}",
    "after": "void Ember_AISelectEffect(void)\n{\n}",
    "case_ids": ["Ember_AISelectEffect-1", "Ember_AISelectEffect-2"],
}
# <<< factory-mutation Ember_AISelectEffect
# >>> factory-mutation FlareonFlamethrower_AISelectEffect
MUTATIONS["FlareonFlamethrower_AISelectEffect"] = {
    "source_symbol": "FlareonFlamethrower_AISelectEffect",
    "before": "void FlareonFlamethrower_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}",
    "after": "void FlareonFlamethrower_AISelectEffect(void)\n{\n}",
    "case_ids": ["FlareonFlamethrower_AISelectEffect-1", "FlareonFlamethrower_AISelectEffect-2"],
}
# <<< factory-mutation FlareonFlamethrower_AISelectEffect
# >>> factory-mutation DestinyBond_DestinyBondEffect
MUTATIONS["DestinyBond_DestinyBondEffect"] = {"source_symbol": "DestinyBond_DestinyBondEffect", "before": "\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_DESTINY_BOND);", "after": "\treturn (uint16_t)(ApplySubstatus1ToAttackingCard(SUBSTATUS1_DESTINY_BOND) + 1u);", "case_ids": ["DestinyBond_DestinyBondEffect-0", "DestinyBond_DestinyBondEffect-1"]}
# <<< factory-mutation DestinyBond_DestinyBondEffect
# >>> factory-mutation FlareonRage_AIEffect
MUTATIONS["FlareonRage_AIEffect"] = {"source_symbol": "FlareonRage_AIEffect", "before": "\tFlareonRage_DamageBoostEffect();\n\tSetDefiniteAIDamage();", "after": "\tFlareonRage_DamageBoostEffect();\n\t(void)0;", "case_ids": ["FlareonRage_AIEffect-2"]}
# <<< factory-mutation FlareonRage_AIEffect
# >>> factory-mutation GolduckHyperBeam_AISelectEffect
MUTATIONS["GolduckHyperBeam_AISelectEffect"] = {"source_symbol": "GolduckHyperBeam_AISelectEffect", "before": "gb_write8(hTemp_ffa0_ADDR, result.a);", "after": "gb_write8(hTemp_ffa0_ADDR, (uint8_t)(result.a + 1u));", "case_ids": ["GolduckHyperBeam_AISelectEffect-0", "GolduckHyperBeam_AISelectEffect-1"]}
# <<< factory-mutation GolduckHyperBeam_AISelectEffect
# >>> factory-mutation OnixHardenEffect
MUTATIONS["OnixHardenEffect"] = {"source_symbol": "OnixHardenEffect", "before": "	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40);", "after": "	return (uint16_t)(ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40) + 1u);", "case_ids": ["OnixHardenEffect-0", "OnixHardenEffect-1"]}
# <<< factory-mutation OnixHardenEffect
# >>> factory-mutation PoliwhirlAmnesia_AISelectEffect
MUTATIONS["PoliwhirlAmnesia_AISelectEffect"] = {"source_symbol": "PoliwhirlAmnesia_AISelectEffect", "before": "\thTemp_ffa0 = result;", "after": "\thTemp_ffa0 = (uint8_t)(result + 1u);", "case_ids": ["PoliwhirlAmnesia_AISelectEffect-0", "PoliwhirlAmnesia_AISelectEffect-1"]}
# <<< factory-mutation PoliwhirlAmnesia_AISelectEffect
# >>> factory-mutation StretchKick_AISelectEffect
MUTATIONS["StretchKick_AISelectEffect"] = {"source_symbol": "StretchKick_AISelectEffect", "before": "\tAIFindTargetForBenchAttackResult result = AIFindTargetForBenchAttack();\n\thTemp_ffa0 = result.a;", "after": "\tAIFindTargetForBenchAttackResult result = AIFindTargetForBenchAttack();\n\thTemp_ffa0 = (uint8_t)(result.a + 1u);", "case_ids": ["StretchKick_AISelectEffect-0", "StretchKick_AISelectEffect-1"]}
# <<< factory-mutation StretchKick_AISelectEffect
# >>> factory-mutation VaporeonWaterGunEffect
MUTATIONS["VaporeonWaterGunEffect"] = {
    "source_symbol": "VaporeonWaterGunEffect",
    "before": "\tApplyExtraWaterEnergyDamageBonus(2u, 1u);",
    "after": "\tApplyExtraWaterEnergyDamageBonus(2u, 1u);\n\twAIMinDamage = (uint8_t)(wAIMinDamage + 1u);",
    "case_ids": ["VaporeonWaterGunEffect-0", "VaporeonWaterGunEffect-1"],
}
# <<< factory-mutation VaporeonWaterGunEffect
# >>> factory-mutation Potion_DamageCheck
MUTATIONS["Potion_DamageCheck"] = {"source_symbol": "Potion_DamageCheck", "before": "\treturn (PotionDamageCheckResult){r.f, NoPokemonWithDamageCountersText};", "after": "\treturn (PotionDamageCheckResult){r.f, (uint16_t)(NoPokemonWithDamageCountersText + 1u)};", "case_ids": ["Potion_DamageCheck-0", "Potion_DamageCheck-1"]}
# <<< factory-mutation Potion_DamageCheck
# >>> factory-mutation CloysterSpikeCannon_AIEffect
MUTATIONS["CloysterSpikeCannon_AIEffect"] = {"source_symbol": "CloysterSpikeCannon_AIEffect", "before": "void CloysterSpikeCannon_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}", "after": "void CloysterSpikeCannon_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}", "case_ids": ["CloysterSpikeCannon_AIEffect-0", "CloysterSpikeCannon_AIEffect-1", "CloysterSpikeCannon_AIEffect-2"]}
# <<< factory-mutation CloysterSpikeCannon_AIEffect
# >>> factory-mutation JolteonDoubleKick_AIEffect
MUTATIONS["JolteonDoubleKick_AIEffect"] = {"source_symbol": "JolteonDoubleKick_AIEffect", "before": "\tSetExpectedAIDamage(20u, 0u, 40u);", "after": "\tSetExpectedAIDamage(21u, 0u, 40u);", "case_ids": ["JolteonDoubleKick_AIEffect-0", "JolteonDoubleKick_AIEffect-1", "JolteonDoubleKick_AIEffect-2"]}
# <<< factory-mutation JolteonDoubleKick_AIEffect
# >>> factory-mutation RapidashStomp_AIEffect
MUTATIONS["RapidashStomp_AIEffect"] = {
    "source_symbol": "RapidashStomp_AIEffect",
    "before": "\tSetExpectedAIDamage(25u, 20u, 30u);",
    "after": "\tSetExpectedAIDamage(26u, 20u, 30u);",
    "case_ids": ["RapidashStomp_AIEffect-0", "RapidashStomp_AIEffect-1", "RapidashStomp_AIEffect-2"],
}
# <<< factory-mutation RapidashStomp_AIEffect
# >>> factory-mutation StoneBarrage_AIEffect
MUTATIONS["StoneBarrage_AIEffect"] = {"source_symbol": "StoneBarrage_AIEffect", "before": "\tSetExpectedAIDamage(10u, 0u, 100u);", "after": "\tSetExpectedAIDamage(11u, 0u, 100u);", "case_ids": ["StoneBarrage_AIEffect-0", "StoneBarrage_AIEffect-1", "StoneBarrage_AIEffect-2"]}
# <<< factory-mutation StoneBarrage_AIEffect
# >>> factory-mutation DestinyBond_AISelectEffect
MUTATIONS["DestinyBond_AISelectEffect"] = {"source_symbol": "DestinyBond_AISelectEffect", "before": "\thTempList = wDuelTempList;", "after": "\thTempList = (uint8_t)(wDuelTempList + 1u);", "case_ids": ["DestinyBond_AISelectEffect-0", "DestinyBond_AISelectEffect-1"]}
# <<< factory-mutation DestinyBond_AISelectEffect
# >>> factory-mutation Rampage_AIEffect
MUTATIONS["Rampage_AIEffect"] = {
    "source_symbol": "Rampage_AIEffect",
    "before": "void Rampage_AIEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage(r.a);\n\tSetDefiniteAIDamage();\n}",
    "after": "void Rampage_AIEffect(void)\n{\n\tCardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage((uint8_t)(r.a + 1u));\n\tSetDefiniteAIDamage();\n}",
    "case_ids": ["Rampage_AIEffect-0", "Rampage_AIEffect-1", "Rampage_AIEffect-2", "Rampage_AIEffect-3"]
}
# <<< factory-mutation Rampage_AIEffect
# >>> factory-mutation SuperPotion_DamageEnergyCheck
MUTATIONS["SuperPotion_DamageEnergyCheck"] = {"source_symbol": "SuperPotion_DamageEnergyCheck", "before": "\tif ((damage.f & 0x10u) != 0u)", "after": "\tif ((damage.f & 0x10u) == 0u)", "case_ids": ["SuperPotion_DamageEnergyCheck-0", "SuperPotion_DamageEnergyCheck-1"]}
# <<< factory-mutation SuperPotion_DamageEnergyCheck
# >>> factory-mutation KrabbyCallForFamily_CheckDeckAndPlayArea
MUTATIONS["KrabbyCallForFamily_CheckDeckAndPlayArea"] = {"source_symbol": "KrabbyCallForFamily_CheckDeckAndPlayArea", "before": "KrabbyCallForFamily_CheckDeckAndPlayArea(void)\n{\n\tCheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();\n\tif (deck.f & 0x10u)", "after": "KrabbyCallForFamily_CheckDeckAndPlayArea(void)\n{\n\tCheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();\n\tif (!(deck.f & 0x10u))", "case_ids": ["KrabbyCallForFamily_CheckDeckAndPlayArea-0", "KrabbyCallForFamily_CheckDeckAndPlayArea-1"]}
# <<< factory-mutation KrabbyCallForFamily_CheckDeckAndPlayArea
# >>> factory-mutation Revive_BenchCheck
MUTATIONS["Revive_BenchCheck"] = {"source_symbol": "Revive_BenchCheck", "before": "\tif (count.a >= MAX_PLAY_AREA_POKEMON) {", "after": "\tif (count.a > MAX_PLAY_AREA_POKEMON) {", "case_ids": ["Revive_BenchCheck-2"]}
# <<< factory-mutation Revive_BenchCheck
# >>> factory-mutation DragonairHyperBeam_DiscardEffect
MUTATIONS["DragonairHyperBeam_DiscardEffect"] = {"source_symbol": "DragonairHyperBeam_DiscardEffect", "before": "\tgb_write8(result.hl, LAST_TURN_EFFECT_DISCARD_ENERGY);", "after": "\tgb_write8(result.hl, 0x02u);", "case_ids": ["DragonairHyperBeam_DiscardEffect-0", "DragonairHyperBeam_DiscardEffect-3"]}
# <<< factory-mutation DragonairHyperBeam_DiscardEffect
# >>> factory-mutation MirrorMove_ExecuteStatusEffect
MUTATIONS["MirrorMove_ExecuteStatusEffect"] = {
    "source_symbol": "MirrorMove_ExecuteStatusEffect",
    "before": "\treturn (MirrorMoveExecuteStatusEffectResult){0xa0u};",
    "after": "\treturn (MirrorMoveExecuteStatusEffectResult){0x00u};",
    "case_ids": ["MirrorMove_ExecuteStatusEffect-0", "MirrorMove_ExecuteStatusEffect-1", "MirrorMove_ExecuteStatusEffect-2", "MirrorMove_ExecuteStatusEffect-3", "MirrorMove_ExecuteStatusEffect-4"],
}
# <<< factory-mutation MirrorMove_ExecuteStatusEffect
# >>> factory-mutation Curse_CheckDamageAndBench
MUTATIONS["Curse_CheckDamageAndBench"] = {"source_symbol": "Curse_CheckDamageAndBench", "before": "if ((flags.a & USED_PKMN_POWER_THIS_TURN) != 0u)", "after": "if ((flags.a & USED_PKMN_POWER_THIS_TURN) == 0u)", "case_ids": ["Curse_CheckDamageAndBench-0", "Curse_CheckDamageAndBench-1", "Curse_CheckDamageAndBench-2", "Curse_CheckDamageAndBench-3"]}
# <<< factory-mutation Curse_CheckDamageAndBench
# >>> factory-mutation SpearowMirrorMove_AIEffect
MUTATIONS["SpearowMirrorMove_AIEffect"] = {
    "source_symbol": "SpearowMirrorMove_AIEffect",
    "before": "\tMirrorMove_AIEffect();",
    "after": "\treturn;",
    "case_ids": ["SpearowMirrorMove_AIEffect-0", "SpearowMirrorMove_AIEffect-1"],
}
# <<< factory-mutation SpearowMirrorMove_AIEffect
# >>> factory-mutation SpearowMirrorMove_InitialEffect1
MUTATIONS["SpearowMirrorMove_InitialEffect1"] = {
    "source_symbol": "SpearowMirrorMove_InitialEffect1",
    "before": "MirrorMoveInitialEffect1Result SpearowMirrorMove_InitialEffect1(void)\n{\n\treturn MirrorMove_InitialEffect1();\n}",
    "after": "MirrorMoveInitialEffect1Result SpearowMirrorMove_InitialEffect1(void)\n{\n\treturn (MirrorMoveInitialEffect1Result){0};\n}",
    "case_ids": ["SpearowMirrorMove_InitialEffect1-0", "SpearowMirrorMove_InitialEffect1-1"],
}
# <<< factory-mutation SpearowMirrorMove_InitialEffect1
# >>> factory-mutation PidgeottoMirrorMove_AIEffect
MUTATIONS["PidgeottoMirrorMove_AIEffect"] = {
    "source_symbol": "PidgeottoMirrorMove_AIEffect",
    "before": "void PidgeottoMirrorMove_AIEffect(void)\n{\n\tMirrorMove_AIEffect();\n}",
    "after": "void PidgeottoMirrorMove_AIEffect(void)\n{\n\treturn;\n}",
    "case_ids": ["PidgeottoMirrorMove_AIEffect-0", "PidgeottoMirrorMove_AIEffect-1"],
}
# <<< factory-mutation PidgeottoMirrorMove_AIEffect
# >>> factory-mutation PidgeottoMirrorMove_AISelection
MUTATIONS["PidgeottoMirrorMove_AISelection"] = {"source_symbol": "PidgeottoMirrorMove_AISelection", "before": "void PidgeottoMirrorMove_AISelection(void)\n{\n\tMirrorMove_AISelection();\n}", "after": "void PidgeottoMirrorMove_AISelection(void)\n{\n\treturn;\n}", "case_ids": ["PidgeottoMirrorMove_AISelection-0", "PidgeottoMirrorMove_AISelection-1"]}
# <<< factory-mutation PidgeottoMirrorMove_AISelection
# >>> factory-mutation ClefairyMetronome_AISelectEffect
MUTATIONS["ClefairyMetronome_AISelectEffect"] = {"source_symbol": "ClefairyMetronome_AISelectEffect", "before": "void ClefairyMetronome_AISelectEffect(void)\n{\n\tHandleAIMetronomeEffect();\n}", "after": "void ClefairyMetronome_AISelectEffect(void)\n{\n\tgb_write8(0xC100u, 0xFFu);\n}", "case_ids": ["ClefairyMetronome_AISelectEffect-0", "ClefairyMetronome_AISelectEffect-1"]}
# <<< factory-mutation ClefairyMetronome_AISelectEffect
# >>> factory-mutation EnergySpike_DeckCheck
MUTATIONS["EnergySpike_DeckCheck"] = {"source_symbol": "EnergySpike_DeckCheck", "before": "\treturn CheckIfDeckIsEmpty();", "after": "\treturn (CheckIfDeckIsEmptyResult){0u, 0u, 0u};", "case_ids": ["EnergySpike_DeckCheck-0", "EnergySpike_DeckCheck-1", "EnergySpike_DeckCheck-2", "EnergySpike_DeckCheck-3"]}
# <<< factory-mutation EnergySpike_DeckCheck
# >>> factory-mutation MagmarFlamethrower_AISelectEffect
MUTATIONS["MagmarFlamethrower_AISelectEffect"] = {"source_symbol": "MagmarFlamethrower_AISelectEffect", "before": "void MagmarFlamethrower_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();\n}", "after": "void MagmarFlamethrower_AISelectEffect(void)\n{\n\treturn;\n}", "case_ids": ["MagmarFlamethrower_AISelectEffect-0", "MagmarFlamethrower_AISelectEffect-1"]}
# <<< factory-mutation MagmarFlamethrower_AISelectEffect
# >>> factory-mutation OmastarWaterGunEffect
MUTATIONS["OmastarWaterGunEffect"] = {
    "source_symbol": "OmastarWaterGunEffect",
    "before": "\tApplyExtraWaterEnergyDamageBonus(1u, 1u);",
    "after": "\tApplyExtraWaterEnergyDamageBonus(1u, 1u);\n\twAIMinDamage = (uint8_t)(wAIMinDamage + 1u);",
    "case_ids": ["OmastarWaterGunEffect-0", "OmastarWaterGunEffect-1"],
}
# <<< factory-mutation OmastarWaterGunEffect
# >>> factory-mutation CuboneRage_AIEffect
MUTATIONS["CuboneRage_AIEffect"] = {"source_symbol": "CuboneRage_AIEffect", "before": "\tCuboneRage_DamageBoostEffect();\n\tSetDefiniteAIDamage();", "after": "\tCuboneRage_DamageBoostEffect();\n\t(void)0;", "case_ids": ["CuboneRage_AIEffect-0", "CuboneRage_AIEffect-1"]}
# <<< factory-mutation CuboneRage_AIEffect
# >>> factory-mutation GravelerHardenEffect
MUTATIONS["GravelerHardenEffect"] = {"source_symbol": "GravelerHardenEffect", "before": "uint16_t GravelerHardenEffect(void)\n{\n\treturn ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40);\n}", "after": "uint16_t GravelerHardenEffect(void)\n{\n\treturn (uint16_t)(ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40) + 1u);\n}", "case_ids": ["GravelerHardenEffect-0", "GravelerHardenEffect-1"]}
# <<< factory-mutation GravelerHardenEffect
# >>> factory-mutation KarateChop_AIEffect
MUTATIONS["KarateChop_AIEffect"] = {"source_symbol": "KarateChop_AIEffect", "before": "void KarateChop_AIEffect(void)\n{\n\tKarateChop_DamageSubtractionEffect();\n\tSetDefiniteAIDamage();\n}", "after": "void KarateChop_AIEffect(void)\n{\n\tKarateChop_DamageSubtractionEffect();\n\t(void)0;\n}", "case_ids": ["KarateChop_AIEffect-0", "KarateChop_AIEffect-1"]}
# <<< factory-mutation KarateChop_AIEffect
# >>> factory-mutation LaprasWaterGunEffect
MUTATIONS["LaprasWaterGunEffect"] = {"source_symbol": "LaprasWaterGunEffect", "before": "void LaprasWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(1u, 0u);\n}", "after": "void LaprasWaterGunEffect(void)\n{\n\t(void)0;\n}", "case_ids": ["LaprasWaterGunEffect-0", "LaprasWaterGunEffect-1"]}
# <<< factory-mutation LaprasWaterGunEffect
# >>> factory-mutation OmanyteWaterGunEffect
MUTATIONS["OmanyteWaterGunEffect"] = {"source_symbol": "OmanyteWaterGunEffect", "before": "void OmanyteWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(1u, 0u);\n}", "after": "void OmanyteWaterGunEffect(void)\n{\n\t(void)0;\n}", "case_ids": ["OmanyteWaterGunEffect-0", "OmanyteWaterGunEffect-1"]}
# <<< factory-mutation OmanyteWaterGunEffect
# >>> factory-mutation PoliwrathWaterGunEffect
MUTATIONS["PoliwrathWaterGunEffect"] = {"source_symbol": "PoliwrathWaterGunEffect", "before": "void PoliwrathWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(2u, 1u);\n}", "after": "void PoliwrathWaterGunEffect(void)\n{\n\t(void)0;\n}", "case_ids": ["PoliwrathWaterGunEffect-0", "PoliwrathWaterGunEffect-1"]}
# <<< factory-mutation PoliwrathWaterGunEffect
# >>> factory-mutation SeadraWaterGunEffect
MUTATIONS["SeadraWaterGunEffect"] = {"source_symbol": "SeadraWaterGunEffect", "before": "void SeadraWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(1u, 1u);\n}", "after": "void SeadraWaterGunEffect(void)\n{\n\t(void)0;\n}", "case_ids": ["SeadraWaterGunEffect-0", "SeadraWaterGunEffect-1"]}
# <<< factory-mutation SeadraWaterGunEffect
# >>> factory-mutation SuperFang_AIEffect
MUTATIONS["SuperFang_AIEffect"] = {"source_symbol": "SuperFang_AIEffect", "before": "void SuperFang_AIEffect(void)\n{\n\tSuperFang_HalfHPEffect();\n\tSetDefiniteAIDamage();\n}", "after": "void SuperFang_AIEffect(void)\n{\n\t(void)0;\n\tSetDefiniteAIDamage();\n}", "case_ids": ["SuperFang_AIEffect-0", "SuperFang_AIEffect-1"]}
# <<< factory-mutation SuperFang_AIEffect
# >>> factory-mutation DragoniteLv41Slam_AIEffect
MUTATIONS["DragoniteLv41Slam_AIEffect"] = {"source_symbol": "DragoniteLv41Slam_AIEffect", "before": "void DragoniteLv41Slam_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}", "after": "void DragoniteLv41Slam_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}", "case_ids": ["DragoniteLv41Slam_AIEffect-0", "DragoniteLv41Slam_AIEffect-1"]}
# <<< factory-mutation DragoniteLv41Slam_AIEffect
# >>> factory-mutation ElectabuzzQuickAttack_AIEffect
MUTATIONS["ElectabuzzQuickAttack_AIEffect"] = {"source_symbol": "ElectabuzzQuickAttack_AIEffect", "before": "void ElectabuzzQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(20u, 10u, 30u);\n}", "after": "void ElectabuzzQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(21u, 10u, 30u);\n}", "case_ids": ["ElectabuzzQuickAttack_AIEffect-0", "ElectabuzzQuickAttack_AIEffect-1"]}
# <<< factory-mutation ElectabuzzQuickAttack_AIEffect
# >>> factory-mutation JolteonQuickAttack_AIEffect
MUTATIONS["JolteonQuickAttack_AIEffect"] = {"source_symbol": "JolteonQuickAttack_AIEffect", "before": "void JolteonQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(20u, 10u, 30u);\n}", "after": "void JolteonQuickAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(21u, 10u, 30u);\n}", "case_ids": ["JolteonQuickAttack_AIEffect-0", "JolteonQuickAttack_AIEffect-1"]}
# <<< factory-mutation JolteonQuickAttack_AIEffect
# >>> factory-mutation LeekSlap_AIEffect
MUTATIONS["LeekSlap_AIEffect"] = {"source_symbol": "LeekSlap_AIEffect", "before": "void LeekSlap_AIEffect(void)\n{\n\tSetExpectedAIDamage(15u, 0u, 30u);\n}", "after": "void LeekSlap_AIEffect(void)\n{\n\tSetExpectedAIDamage(16u, 0u, 30u);\n}", "case_ids": ["LeekSlap_AIEffect-0", "LeekSlap_AIEffect-1"]}
# <<< factory-mutation LeekSlap_AIEffect
# >>> factory-mutation PinMissile_AIEffect
MUTATIONS["PinMissile_AIEffect"] = {"source_symbol": "PinMissile_AIEffect", "before": "void PinMissile_AIEffect(void)\n{\n\tSetExpectedAIDamage(40u, 0u, 80u);\n}", "after": "void PinMissile_AIEffect(void)\n{\n\tSetExpectedAIDamage(41u, 0u, 80u);\n}", "case_ids": ["PinMissile_AIEffect-0", "PinMissile_AIEffect-1"]}
# <<< factory-mutation PinMissile_AIEffect
# >>> factory-mutation SandslashFurySwipes_AIEffect
MUTATIONS["SandslashFurySwipes_AIEffect"] = {"source_symbol": "SandslashFurySwipes_AIEffect", "before": "void SandslashFurySwipes_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);\n}", "after": "void SandslashFurySwipes_AIEffect(void)\n{\n\tSetExpectedAIDamage(31u, 0u, 60u);\n}", "case_ids": ["SandslashFurySwipes_AIEffect-0", "SandslashFurySwipes_AIEffect-1"]}
# <<< factory-mutation SandslashFurySwipes_AIEffect
# >>> factory-mutation Thunderpunch_AIEffect
MUTATIONS["Thunderpunch_AIEffect"] = {"source_symbol": "Thunderpunch_AIEffect", "before": "void Thunderpunch_AIEffect(void)\n{\n\tSetExpectedAIDamage(35u, 30u, 40u);\n}", "after": "void Thunderpunch_AIEffect(void)\n{\n\tSetExpectedAIDamage(36u, 30u, 40u);\n}", "case_ids": ["Thunderpunch_AIEffect-0", "Thunderpunch_AIEffect-1"]}
# <<< factory-mutation Thunderpunch_AIEffect
# >>> factory-mutation StarmieRecover_AISelectEffect
MUTATIONS["StarmieRecover_AISelectEffect"] = {"source_symbol": "StarmieRecover_AISelectEffect", "before": "\tuint8_t a = wDuelTempList;\n\thTemp_ffa0 = a;", "after": "\tuint8_t a = wDuelTempList;\n\thTemp_ffa0 = 0u;", "case_ids": ["StarmieRecover_AISelectEffect-0", "StarmieRecover_AISelectEffect-1"]}
# <<< factory-mutation StarmieRecover_AISelectEffect
# >>> factory-mutation BellsproutCallForFamily_CheckDeckAndPlayArea
MUTATIONS["BellsproutCallForFamily_CheckDeckAndPlayArea"] = {"source_symbol": "BellsproutCallForFamily_CheckDeckAndPlayArea", "before": "\tuint8_t c = (var.a >= MAX_PLAY_AREA_POKEMON) ? 0x10u : 0u;", "after": "\tuint8_t c = (var.a > MAX_PLAY_AREA_POKEMON) ? 0x10u : 0u;", "case_ids": ["BellsproutCallForFamily_CheckDeckAndPlayArea-2"]}
# <<< factory-mutation BellsproutCallForFamily_CheckDeckAndPlayArea
# >>> factory-mutation Spark_AISelectEffect
MUTATIONS["Spark_AISelectEffect"] = {"source_symbol": "Spark_AISelectEffect", "before": "\tif (var.a < 2u)\n\t\treturn (SparkAISelectEffectResult){var.a};", "after": "\tif (var.a < 1u)\n\t\treturn (SparkAISelectEffectResult){var.a};", "case_ids": ["Spark_AISelectEffect-0", "Spark_AISelectEffect-1"]}
# <<< factory-mutation Spark_AISelectEffect
# >>> factory-mutation DamageSwap_CheckDamage
MUTATIONS["DamageSwap_CheckDamage"] = {"source_symbol": "DamageSwap_CheckDamage", "before": "\tif (has_damage.f & 0x10u) {", "after": "\tif (!(has_damage.f & 0x10u)) {", "case_ids": ["DamageSwap_CheckDamage-0", "DamageSwap_CheckDamage-2"]}
# <<< factory-mutation DamageSwap_CheckDamage
# >>> factory-mutation PokemonFlute_BenchCheck
MUTATIONS["PokemonFlute_BenchCheck"] = {"source_symbol": "PokemonFlute_BenchCheck", "before": "\tDuelistVarResult count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tif (count.a >= MAX_PLAY_AREA_POKEMON) {", "after": "\tDuelistVarResult count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tif (count.a > MAX_PLAY_AREA_POKEMON) {", "case_ids": ["PokemonFlute_BenchCheck-0"]}
# <<< factory-mutation PokemonFlute_BenchCheck
# >>> factory-mutation Heal_OncePerTurnCheck
MUTATIONS["Heal_OncePerTurnCheck"] = {"source_symbol": "Heal_OncePerTurnCheck", "before": "\tif (flags.a & USED_PKMN_POWER_THIS_TURN)\n\t\treturn (HealOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};", "after": "\tif (!(flags.a & USED_PKMN_POWER_THIS_TURN))\n\t\treturn (HealOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};", "case_ids": ["Heal_OncePerTurnCheck-0", "Heal_OncePerTurnCheck-2"]}
# <<< factory-mutation Heal_OncePerTurnCheck
# >>> factory-mutation Shift_ChangeColorEffect
MUTATIONS["Shift_ChangeColorEffect"] = {"source_symbol": "Shift_ChangeColorEffect", "before": "\tuint8_t new_type = (uint8_t)(hAIPkmnPowerEffectParam | HAS_CHANGED_COLOR);", "after": "\tuint8_t new_type = hAIPkmnPowerEffectParam;", "case_ids": ["Shift_ChangeColorEffect-0"]}
# <<< factory-mutation Shift_ChangeColorEffect
# >>> factory-mutation MagikarpFlail_AIEffect
MUTATIONS["MagikarpFlail_AIEffect"] = {"source_symbol": "MagikarpFlail_AIEffect", "before": "MagikarpFlail_HPCheck();", "after": "(void)0;", "case_ids": ["MagikarpFlail_AIEffect-0", "MagikarpFlail_AIEffect-1"]}
# <<< factory-mutation MagikarpFlail_AIEffect
# >>> factory-mutation PoliwagWaterGunEffect
MUTATIONS["PoliwagWaterGunEffect"] = {"source_symbol": "PoliwagWaterGunEffect", "before": "void PoliwagWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(1u, 0u);", "after": "void PoliwagWaterGunEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(2u, 0u);", "case_ids": ["PoliwagWaterGunEffect-0", "PoliwagWaterGunEffect-1"]}
# <<< factory-mutation PoliwagWaterGunEffect
# >>> factory-mutation TaurosStomp_AIEffect
MUTATIONS["TaurosStomp_AIEffect"] = {"source_symbol": "TaurosStomp_AIEffect", "before": "void TaurosStomp_AIEffect(void)\n{\n\tSetExpectedAIDamage(25u, 20u, 30u);", "after": "void TaurosStomp_AIEffect(void)\n{\n\tSetExpectedAIDamage(25u, 20u, 40u);", "case_ids": ["TaurosStomp_AIEffect-0", "TaurosStomp_AIEffect-1"]}
# <<< factory-mutation TaurosStomp_AIEffect
# >>> factory-mutation DodrioRage_AIEffect
MUTATIONS["DodrioRage_AIEffect"] = {"source_symbol": "DodrioRage_AIEffect", "before": "DodrioRage_DamageBoostEffect();", "after": "(void)0;", "case_ids": ["DodrioRage_AIEffect-0", "DodrioRage_AIEffect-1"]}
# <<< factory-mutation DodrioRage_AIEffect
# >>> factory-mutation DragoniteLv45Slam_AIEffect
MUTATIONS["DragoniteLv45Slam_AIEffect"] = {"source_symbol": "DragoniteLv45Slam_AIEffect", "before": "void DragoniteLv45Slam_AIEffect(void)\n{\n\tSetExpectedAIDamage(40u, 0u, 80u);", "after": "void DragoniteLv45Slam_AIEffect(void)\n{\n\tSetExpectedAIDamage(40u, 0u, 40u);", "case_ids": ["DragoniteLv45Slam_AIEffect-0", "DragoniteLv45Slam_AIEffect-1"]}
# <<< factory-mutation DragoniteLv45Slam_AIEffect
# >>> factory-mutation GengarDarkMind_AISelectEffect
MUTATIONS["GengarDarkMind_AISelectEffect"] = {"source_symbol": "GengarDarkMind_AISelectEffect", "before": "DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tif (r.a < 2u)", "after": "DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tif (r.a < 1u)", "case_ids": ["GengarDarkMind_AISelectEffect-0"]}
# <<< factory-mutation GengarDarkMind_AISelectEffect
# >>> factory-mutation PoliwhirlDoubleslap_AIEffect
MUTATIONS["PoliwhirlDoubleslap_AIEffect"] = {"source_symbol": "PoliwhirlDoubleslap_AIEffect", "before": "void PoliwhirlDoubleslap_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);", "after": "void PoliwhirlDoubleslap_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 40u);", "case_ids": ["PoliwhirlDoubleslap_AIEffect-0", "PoliwhirlDoubleslap_AIEffect-1"]}
# <<< factory-mutation PoliwhirlDoubleslap_AIEffect
# >>> factory-mutation KinglerFlail_AIEffect
MUTATIONS["KinglerFlail_AIEffect"] = {"source_symbol": "KinglerFlail_AIEffect", "before": "KinglerFlail_HPCheck();", "after": "(void)0;", "case_ids": ["KinglerFlail_AIEffect-0", "KinglerFlail_AIEffect-1"]}
# <<< factory-mutation KinglerFlail_AIEffect
# >>> factory-mutation JynxDoubleslap_AIEffect
MUTATIONS["JynxDoubleslap_AIEffect"] = {"source_symbol": "JynxDoubleslap_AIEffect", "before": "void JynxDoubleslap_AIEffect(void)\n{\n\tSetExpectedAIDamage(10u, 0u, 20u);", "after": "void JynxDoubleslap_AIEffect(void)\n{\n\tSetExpectedAIDamage(10u, 0u, 40u);", "case_ids": ["JynxDoubleslap_AIEffect-0", "JynxDoubleslap_AIEffect-1"]}
# <<< factory-mutation JynxDoubleslap_AIEffect
# >>> factory-mutation Bonemerang_AIEffect
MUTATIONS["Bonemerang_AIEffect"] = {"source_symbol": "Bonemerang_AIEffect", "before": "void Bonemerang_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 60u);", "after": "void Bonemerang_AIEffect(void)\n{\n\tSetExpectedAIDamage(30u, 0u, 40u);", "case_ids": ["Bonemerang_AIEffect-0", "Bonemerang_AIEffect-1"]}
# <<< factory-mutation Bonemerang_AIEffect
# >>> factory-mutation Barrier_BarrierEffect
MUTATIONS["Barrier_BarrierEffect"] = {"source_symbol": "Barrier_BarrierEffect", "before": "(void)ApplySubstatus1ToAttackingCard(SUBSTATUS1_BARRIER);", "after": "(void)ApplySubstatus1ToAttackingCard(0u);", "case_ids": ["Barrier_BarrierEffect-0", "Barrier_BarrierEffect-1"]}
# <<< factory-mutation Barrier_BarrierEffect
# >>> factory-mutation HydroPumpEffect
MUTATIONS["HydroPumpEffect"] = {"source_symbol": "HydroPumpEffect", "before": "void HydroPumpEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(3u, 0u);", "after": "void HydroPumpEffect(void)\n{\n\tApplyExtraWaterEnergyDamageBonus(4u, 0u);", "case_ids": ["HydroPumpEffect-0", "HydroPumpEffect-1"]}
# <<< factory-mutation HydroPumpEffect
# >>> factory-mutation MysteryAttack_AIEffect
MUTATIONS["MysteryAttack_AIEffect"] = {"source_symbol": "MysteryAttack_AIEffect", "before": "void MysteryAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(10u, 0u, 20u);", "after": "void MysteryAttack_AIEffect(void)\n{\n\tSetExpectedAIDamage(10u, 0u, 40u);", "case_ids": ["MysteryAttack_AIEffect-0", "MysteryAttack_AIEffect-1"]}
# <<< factory-mutation MysteryAttack_AIEffect
# >>> factory-mutation HurricaneEffect
MUTATIONS["HurricaneEffect"] = {"source_symbol": "HurricaneEffect", "before": "gb_write8(arena_addr, 0xFFu);", "after": "gb_write8(arena_addr, 0x00u);", "case_ids": ["HurricaneEffect-2"]}
# <<< factory-mutation HurricaneEffect
# >>> factory-mutation Psychic_AIEffect
MUTATIONS["Psychic_AIEffect"] = {"source_symbol": "Psychic_AIEffect", "before": "Psychic_DamageBoostEffect();", "after": "(void)0;", "case_ids": ["Psychic_AIEffect-0", "Psychic_AIEffect-1"]}
# <<< factory-mutation Psychic_AIEffect
# >>> factory-mutation SlowpokeAmnesia_AISelectEffect
MUTATIONS["SlowpokeAmnesia_AISelectEffect"] = {"source_symbol": "SlowpokeAmnesia_AISelectEffect", "before": "gb_write8(hTemp_ffa0_ADDR, a);", "after": "gb_write8(hTemp_ffa0_ADDR, (uint8_t)(a + 1u));", "case_ids": ["SlowpokeAmnesia_AISelectEffect-0", "SlowpokeAmnesia_AISelectEffect-1"]}
# <<< factory-mutation SlowpokeAmnesia_AISelectEffect
# >>> factory-mutation KadabraRecover_AISelectEffect
MUTATIONS["KadabraRecover_AISelectEffect"] = {"source_symbol": "KadabraRecover_AISelectEffect", "before": "uint8_t a = gb_read8(wDuelTempList_ADDR);\n\tgb_write8(hTemp_ffa0_ADDR, a);", "after": "uint8_t a = gb_read8(wDuelTempList_ADDR);\n\tgb_write8(hTemp_ffa0_ADDR, (uint8_t)(a + 1u));", "case_ids": ["KadabraRecover_AISelectEffect-0", "KadabraRecover_AISelectEffect-1"]}
# <<< factory-mutation KadabraRecover_AISelectEffect
# >>> factory-mutation GolduckHyperBeam_DiscardEffect
MUTATIONS["GolduckHyperBeam_DiscardEffect"] = {"source_symbol": "GolduckHyperBeam_DiscardEffect", "before": "gb_write8(effect_var.hl, LAST_TURN_EFFECT_DISCARD_ENERGY);", "after": "gb_write8(effect_var.hl, 0u);", "case_ids": ["GolduckHyperBeam_DiscardEffect-2"]}
# <<< factory-mutation GolduckHyperBeam_DiscardEffect
# >>> factory-mutation StrangeBehavior_CheckDamage
MUTATIONS["StrangeBehavior_CheckDamage"] = {"source_symbol": "StrangeBehavior_CheckDamage", "before": "if (hp.a < 20u)", "after": "if (hp.a < 0u)", "case_ids": ["StrangeBehavior_CheckDamage-0", "StrangeBehavior_CheckDamage-1"]}
# <<< factory-mutation StrangeBehavior_CheckDamage
# >>> factory-mutation EnergyTrans_PrintProcedure
MUTATIONS["EnergyTrans_PrintProcedure"] = {"source_symbol": "EnergyTrans_PrintProcedure", "before": "DrawWholeScreenTextBox(ProcedureForEnergyTransferText);", "after": "DrawWholeScreenTextBox((uint16_t)(ProcedureForEnergyTransferText + 1u));", "case_ids": ["EnergyTrans_PrintProcedure-0", "EnergyTrans_PrintProcedure-1"]}
# <<< factory-mutation EnergyTrans_PrintProcedure
# >>> factory-mutation ItemFinder_HandDiscardPileCheck
MUTATIONS["ItemFinder_HandDiscardPileCheck"] = {"source_symbol": "ItemFinder_HandDiscardPileCheck", "before": "if (count.a < 3u)", "after": "if (count.a < 0u)", "case_ids": ["ItemFinder_HandDiscardPileCheck-0", "ItemFinder_HandDiscardPileCheck-2"]}
# <<< factory-mutation ItemFinder_HandDiscardPileCheck
# >>> factory-mutation Wildfire_DiscardEnergyEffect
MUTATIONS["Wildfire_DiscardEnergyEffect"] = {"source_symbol": "Wildfire_DiscardEnergyEffect", "before": "for (uint8_t c = count; c != 0u; c--) {", "after": "for (uint8_t c = (uint8_t)(count - 1u); c != 0u; c--) {", "case_ids": ["Wildfire_DiscardEnergyEffect-1", "Wildfire_DiscardEnergyEffect-2"]}
# <<< factory-mutation Wildfire_DiscardEnergyEffect
# >>> factory-mutation SuperEnergyRemoval_EnergyCheck
MUTATIONS["SuperEnergyRemoval_EnergyCheck"] = {"source_symbol": "SuperEnergyRemoval_EnergyCheck", "before": "CheckIfThereAreAnyEnergyCardsAttached();\n\tif (r1.f & 0x10u)", "after": "CheckIfThereAreAnyEnergyCardsAttached();\n\tif (!(r1.f & 0x10u))", "case_ids": ["SuperEnergyRemoval_EnergyCheck-0", "SuperEnergyRemoval_EnergyCheck-1"]}
# <<< factory-mutation SuperEnergyRemoval_EnergyCheck
# >>> factory-mutation MorphEffect
MUTATIONS["MorphEffect"] = {"source_symbol": "MorphEffect", "before": "(void)DrawWideTextBox_WaitForInput(AttackUnsuccessfulText);", "after": "(void)DrawWideTextBox_WaitForInput(0x0000u);", "case_ids": ["MorphEffect-0", "MorphEffect-2"]}
# <<< factory-mutation MorphEffect
# >>> factory-mutation AISelectConversionColor
MUTATIONS["AISelectConversionColor"] = {"source_symbol": "AISelectConversionColor", "before": "\tgb_write8(hTemp_ffa0_ADDR, Random(NUM_COLORED_TYPES));", "after": "\tgb_write8(hTemp_ffa0_ADDR, (uint8_t)(Random(NUM_COLORED_TYPES) + 1u));", "case_ids": ["AISelectConversionColor-0", "AISelectConversionColor-1"]}
# <<< factory-mutation AISelectConversionColor
# >>> factory-mutation PrintArenaCardNameAndColorText
MUTATIONS["PrintArenaCardNameAndColorText"] = {"source_symbol": "PrintArenaCardNameAndColorText", "before": "\treturn DrawWideTextBox_PrintText(hl);", "after": "\treturn DrawWideTextBox_PrintText((uint16_t)(hl + 1u));", "case_ids": ["PrintArenaCardNameAndColorText-0", "PrintArenaCardNameAndColorText-1"]}
# <<< factory-mutation PrintArenaCardNameAndColorText
# >>> factory-mutation Conversion1_AISelectEffect
MUTATIONS["Conversion1_AISelectEffect"] = {
    "source_symbol": "Conversion1_AISelectEffect",
    "before": "\tAISelectConversionColor();",
    "after": "\t(void)0;",
    "case_ids": ["Conversion1_AISelectEffect-0", "Conversion1_AISelectEffect-1"],
}
# <<< factory-mutation Conversion1_AISelectEffect
# >>> factory-mutation Conversion2_ChangeResistanceEffect
MUTATIONS["Conversion2_ChangeResistanceEffect"] = {
    "source_symbol": "Conversion2_ChangeResistanceEffect",
    "before": "\tgb_write8(v.hl, wr);",
    "after": "\tgb_write8(v.hl, (uint8_t)(wr + 1u));",
    "case_ids": ["Conversion2_ChangeResistanceEffect-0", "Conversion2_ChangeResistanceEffect-1"],
}
# <<< factory-mutation Conversion2_ChangeResistanceEffect
# >>> factory-mutation Conversion2_AISelectEffect
MUTATIONS["Conversion2_AISelectEffect"] = {
    "source_symbol": "Conversion2_AISelectEffect",
    "before": "\t\tgb_write8(hTemp_ffa0_ADDR, type);",
    "after": "\t\tgb_write8(hTemp_ffa0_ADDR, (uint8_t)(type + 1u));",
    "case_ids": ["Conversion2_AISelectEffect-0", "Conversion2_AISelectEffect-1"],
}
# <<< factory-mutation Conversion2_AISelectEffect
# >>> factory-mutation MirrorMove_AfterDamage
MUTATIONS["MirrorMove_AfterDamage"] = {
    "source_symbol": "MirrorMove_AfterDamage",
    "before": "\tif (a != 0u) {",
    "after": "\tif (a != 1u) {",
    "case_ids": ["MirrorMove_AfterDamage-0", "MirrorMove_AfterDamage-1"],
}
# <<< factory-mutation MirrorMove_AfterDamage
# >>> factory-mutation PidgeottoMirrorMove_AfterDamage
MUTATIONS["PidgeottoMirrorMove_AfterDamage"] = {
    "source_symbol": "PidgeottoMirrorMove_AfterDamage",
    "before": "\treturn MirrorMove_AfterDamage(d, e, hl_in);",
    "after": "\treturn MirrorMove_AfterDamage(d, e, (uint16_t)(hl_in + 1u));",
    "case_ids": ["PidgeottoMirrorMove_AfterDamage-0", "PidgeottoMirrorMove_AfterDamage-1"],
}
# <<< factory-mutation PidgeottoMirrorMove_AfterDamage
# >>> factory-mutation SpearowMirrorMove_AfterDamage
MUTATIONS["SpearowMirrorMove_AfterDamage"] = {
    "source_symbol": "SpearowMirrorMove_AfterDamage",
    "before": "\tTextResult r = MirrorMove_AfterDamage(d, e, hl_in);",
    "after": "\tTextResult r = MirrorMove_AfterDamage(d, e, (uint16_t)(hl_in + 1u));",
    "case_ids": ["SpearowMirrorMove_AfterDamage-0", "SpearowMirrorMove_AfterDamage-1"],
}
# <<< factory-mutation SpearowMirrorMove_AfterDamage
# >>> factory-mutation Func_2c0a8
MUTATIONS["Func_2c0a8"] = {"source_symbol": "Func_2c0a8", "before": "\thTemp_ffa0 = saved;", "after": "\thTemp_ffa0 = hWhoseTurn;", "case_ids": ["Func_2c0a8-0", "Func_2c0a8-1"]}
# <<< factory-mutation Func_2c0a8
# >>> factory-mutation ShuffleCardsInDeck
MUTATIONS["ShuffleCardsInDeck"] = {"source_symbol": "ShuffleCardsInDeck", "before": "\tShuffleDeckResult sd = ShuffleDeck(r.c, anim.e);", "after": "\tShuffleDeckResult sd = ShuffleDeck(r.c, (uint8_t)r.de);", "case_ids": ["ShuffleCardsInDeck-0", "ShuffleCardsInDeck-1"]}
# <<< factory-mutation ShuffleCardsInDeck
# >>> factory-mutation DrawPlayAreaScreenToShowChanges
MUTATIONS["DrawPlayAreaScreenToShowChanges"] = {
    "source_symbol": "DrawPlayAreaScreenToShowChanges",
    "before": "\tgb_write8(hTempPlayAreaLocation_ff9d_ADDR, a);",
    "after": "\tgb_write8(hTempPlayAreaLocation_ff9d_ADDR, (uint8_t)(a + 1u));",
    "case_ids": ["DrawPlayAreaScreenToShowChanges-0", "DrawPlayAreaScreenToShowChanges-1"],
}
# <<< factory-mutation DrawPlayAreaScreenToShowChanges
# >>> factory-mutation EnergyRemoval_DiscardEffect
MUTATIONS["EnergyRemoval_DiscardEffect"] = {
    "source_symbol": "EnergyRemoval_DiscardEffect",
    "before": "\treturn (EnergyRemovalDiscardEffectResult){turn.a, turn.f, turn.hl};",
    "after": "\treturn (EnergyRemovalDiscardEffectResult){turn.a, 0x00u, turn.hl};",
    "case_ids": ["EnergyRemoval_DiscardEffect-0", "EnergyRemoval_DiscardEffect-1"],
}
# <<< factory-mutation EnergyRemoval_DiscardEffect
# >>> factory-mutation SuperEnergyRemoval_DiscardEffect
MUTATIONS["SuperEnergyRemoval_DiscardEffect"] = {
    "source_symbol": "SuperEnergyRemoval_DiscardEffect",
    "before": "\tPutCardInDiscardPile(gb_read8(hl++));",
    "after": "\tPutCardInDiscardPile(0u);",
    "case_ids": ["SuperEnergyRemoval_DiscardEffect-0", "SuperEnergyRemoval_DiscardEffect-1"],
}
# <<< factory-mutation SuperEnergyRemoval_DiscardEffect
# >>> factory-mutation EnergyTrans_AIEffect
MUTATIONS["EnergyTrans_AIEffect"] = {
    "source_symbol": "EnergyTrans_AIEffect",
    "before": "\t(void)PutHandCardInPlayArea(card, location);",
    "after": "\t(void)PutHandCardInPlayArea((uint8_t)(card + 1u), location);",
    "case_ids": ["EnergyTrans_AIEffect-0", "EnergyTrans_AIEffect-1"],
}
# <<< factory-mutation EnergyTrans_AIEffect
# >>> factory-mutation StrangeBehavior_SwapEffect
MUTATIONS["StrangeBehavior_SwapEffect"] = {
    "source_symbol": "StrangeBehavior_SwapEffect",
    "before": "\tif ((damage.f & 0x10u) != 0u)\n\t\treturn (StrangeBehaviorSwapEffectResult){damage.a, (uint8_t)(damage.a == 0u ? 0x90u : damage.f), damage.hl};",
    "after": "\tif ((damage.f & 0x10u) == 0u)\n\t\treturn (StrangeBehaviorSwapEffectResult){damage.a, (uint8_t)(damage.a == 0u ? 0x90u : damage.f), damage.hl};",
    "case_ids": ["StrangeBehavior_SwapEffect-0", "StrangeBehavior_SwapEffect-1"],
}
# <<< factory-mutation StrangeBehavior_SwapEffect
# >>> factory-mutation Defender_AttachDefenderEffect
MUTATIONS["Defender_AttachDefenderEffect"] = {
    "source_symbol": "Defender_AttachDefenderEffect",
    "before": "\tgb_write8(defender.hl, (uint8_t)(gb_read8(defender.hl) + 1u));",
    "after": "\tgb_write8(defender.hl, gb_read8(defender.hl));",
    "case_ids": ["Defender_AttachDefenderEffect-0", "Defender_AttachDefenderEffect-1"],
}
# <<< factory-mutation Defender_AttachDefenderEffect
# >>> factory-mutation DamageSwap_SwapEffect
MUTATIONS["DamageSwap_SwapEffect"] = {
    "source_symbol": "DamageSwap_SwapEffect",
    "before": "\tif ((damage.f & 0x10u) != 0u)\n\t\treturn (DamageSwap_SwapEffectResult){damage.a, damage.f, damage.hl};",
    "after": "\tif ((damage.f & 0x10u) == 0u)\n\t\treturn (DamageSwap_SwapEffectResult){damage.a, damage.f, damage.hl};",
    "case_ids": ["DamageSwap_SwapEffect-0", "DamageSwap_SwapEffect-1"],
}
# <<< factory-mutation DamageSwap_SwapEffect
# >>> factory-mutation PrintDevolvedCardNameAndLevelText
MUTATIONS["PrintDevolvedCardNameAndLevelText"] = {"source_symbol": "PrintDevolvedCardNameAndLevelText", "before": "\tgb_write8(wTxRam2_b_ADDR, 0u);", "after": "\tgb_write8(wTxRam2_b_ADDR, 1u);", "case_ids": ["PrintDevolvedCardNameAndLevelText-0", "PrintDevolvedCardNameAndLevelText-1"]}
# <<< factory-mutation PrintDevolvedCardNameAndLevelText
# >>> factory-mutation ApplySubstatus2ToDefendingCard
MUTATIONS["ApplySubstatus2ToDefendingCard"] = {"source_symbol": "ApplySubstatus2ToDefendingCard", "before": "\tgb_write8(r.hl, a);\n\tuint16_t last_turn", "after": "\tgb_write8(r.hl, 0u);\n\tuint16_t last_turn", "case_ids": ["ApplySubstatus2ToDefendingCard-0", "ApplySubstatus2ToDefendingCard-1", "ApplySubstatus2ToDefendingCard-2"]}
# <<< factory-mutation ApplySubstatus2ToDefendingCard
# >>> factory-mutation ApplyAmnesiaToAttack
MUTATIONS["ApplyAmnesiaToAttack"] = {"source_symbol": "ApplyAmnesiaToAttack", "before": "\tgb_write8(non_turn.hl, hTemp_ffa0);", "after": "\tgb_write8(non_turn.hl, 0x00u);", "case_ids": ["ApplyAmnesiaToAttack-0", "ApplyAmnesiaToAttack-1"]}
# <<< factory-mutation ApplyAmnesiaToAttack
# >>> factory-mutation MirrorMove_BeforeDamage
MUTATIONS["MirrorMove_BeforeDamage"] = {"source_symbol": "MirrorMove_BeforeDamage", "before": "gb_write8(wDamage_ADDR, damage_lo);", "after": "gb_write8(wDamage_ADDR, 0u);", "case_ids": ["MirrorMove_BeforeDamage-1", "MirrorMove_BeforeDamage-2"]}
# <<< factory-mutation MirrorMove_BeforeDamage
# >>> factory-mutation SpearowMirrorMove_BeforeDamage
MUTATIONS["SpearowMirrorMove_BeforeDamage"] = {"source_symbol": "SpearowMirrorMove_BeforeDamage", "before": "\tMirrorMove_BeforeDamage();", "after": "\treturn;", "case_ids": ["SpearowMirrorMove_BeforeDamage-1", "SpearowMirrorMove_BeforeDamage-2", "SpearowMirrorMove_BeforeDamage-3"]}
# <<< factory-mutation SpearowMirrorMove_BeforeDamage
# >>> factory-mutation PidgeottoMirrorMove_BeforeDamage
MUTATIONS["PidgeottoMirrorMove_BeforeDamage"] = {"source_symbol": "PidgeottoMirrorMove_BeforeDamage", "before": "void PidgeottoMirrorMove_BeforeDamage(void)\n{\n\tMirrorMove_BeforeDamage();", "after": "void PidgeottoMirrorMove_BeforeDamage(void)\n{\n\treturn;", "case_ids": ["PidgeottoMirrorMove_BeforeDamage-1", "PidgeottoMirrorMove_BeforeDamage-2", "PidgeottoMirrorMove_BeforeDamage-3"]}
# <<< factory-mutation PidgeottoMirrorMove_BeforeDamage
# >>> factory-mutation PoliwhirlAmnesia_DisableEffect
MUTATIONS["PoliwhirlAmnesia_DisableEffect"] = {"source_symbol": "PoliwhirlAmnesia_DisableEffect", "before": "\tApplyAmnesiaToAttack(a, f, b, c, d, e, hl);", "after": "\t(void)0;", "case_ids": ["PoliwhirlAmnesia_DisableEffect-0", "PoliwhirlAmnesia_DisableEffect-1"]}
# <<< factory-mutation PoliwhirlAmnesia_DisableEffect
# >>> factory-mutation SlowpokeAmnesia_DisableEffect
MUTATIONS["SlowpokeAmnesia_DisableEffect"] = {"source_symbol": "SlowpokeAmnesia_DisableEffect", "before": "void SlowpokeAmnesia_DisableEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tApplyAmnesiaToAttack(a, f, b, c, d, e, hl);", "after": "void SlowpokeAmnesia_DisableEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)0;", "case_ids": ["SlowpokeAmnesia_DisableEffect-0", "SlowpokeAmnesia_DisableEffect-1"]}
# <<< factory-mutation SlowpokeAmnesia_DisableEffect
# >>> factory-mutation HorseaSmokescreenEffect
MUTATIONS["HorseaSmokescreenEffect"] = {"source_symbol": "HorseaSmokescreenEffect", "before": "return ApplySubstatus2ToDefendingCard(SUBSTATUS2_SMOKESCREEN, hl);", "after": "return ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["HorseaSmokescreenEffect-0", "HorseaSmokescreenEffect-1", "HorseaSmokescreenEffect-2"]}
# <<< factory-mutation HorseaSmokescreenEffect
# >>> factory-mutation PikachuAltLv16GrowlEffect
MUTATIONS["PikachuAltLv16GrowlEffect"] = {"source_symbol": "PikachuAltLv16GrowlEffect", "before": "uint16_t PikachuAltLv16GrowlEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_GROWL, hl);", "after": "uint16_t PikachuAltLv16GrowlEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["PikachuAltLv16GrowlEffect-0", "PikachuAltLv16GrowlEffect-1", "PikachuAltLv16GrowlEffect-2"]}
# <<< factory-mutation PikachuAltLv16GrowlEffect
# >>> factory-mutation MagmarSmokescreenEffect
MUTATIONS["MagmarSmokescreenEffect"] = {"source_symbol": "MagmarSmokescreenEffect", "before": "uint16_t MagmarSmokescreenEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_SMOKESCREEN, hl);", "after": "uint16_t MagmarSmokescreenEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["MagmarSmokescreenEffect-0", "MagmarSmokescreenEffect-1", "MagmarSmokescreenEffect-2"]}
# <<< factory-mutation MagmarSmokescreenEffect
# >>> factory-mutation PikachuLv16GrowlEffect
MUTATIONS["PikachuLv16GrowlEffect"] = {"source_symbol": "PikachuLv16GrowlEffect", "before": "uint16_t PikachuLv16GrowlEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_GROWL, hl);", "after": "uint16_t PikachuLv16GrowlEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["PikachuLv16GrowlEffect-0", "PikachuLv16GrowlEffect-1", "PikachuLv16GrowlEffect-2"]}
# <<< factory-mutation PikachuLv16GrowlEffect
# >>> factory-mutation PounceEffect
MUTATIONS["PounceEffect"] = {"source_symbol": "PounceEffect", "before": "uint16_t PounceEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_POUNCE, hl);", "after": "uint16_t PounceEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["PounceEffect-0", "PounceEffect-1", "PounceEffect-2"]}
# <<< factory-mutation PounceEffect
# >>> factory-mutation SandAttackEffect
MUTATIONS["SandAttackEffect"] = {"source_symbol": "SandAttackEffect", "before": "uint16_t SandAttackEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_SAND_ATTACK, hl);", "after": "uint16_t SandAttackEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["SandAttackEffect-0", "SandAttackEffect-1", "SandAttackEffect-2"]}
# <<< factory-mutation SandAttackEffect
# >>> factory-mutation SnivelEffect
MUTATIONS["SnivelEffect"] = {"source_symbol": "SnivelEffect", "before": "uint16_t SnivelEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(SUBSTATUS2_REDUCE_BY_20, hl);", "after": "uint16_t SnivelEffect(uint16_t hl)\n{\n\treturn ApplySubstatus2ToDefendingCard(0x00u, hl);", "case_ids": ["SnivelEffect-0", "SnivelEffect-1", "SnivelEffect-2"]}
# <<< factory-mutation SnivelEffect
# >>> factory-mutation Conversion1_ChangeWeaknessEffect
MUTATIONS["Conversion1_ChangeWeaknessEffect"] = {"source_symbol": "Conversion1_ChangeWeaknessEffect", "before": "\tgb_write8(nonturn.hl, weakness);", "after": "\tgb_write8(nonturn.hl, (uint8_t)(weakness + 1u));", "case_ids": ["Conversion1_ChangeWeaknessEffect-1", "Conversion1_ChangeWeaknessEffect-2"]}
# <<< factory-mutation Conversion1_ChangeWeaknessEffect
# >>> factory-mutation EnergyRetrieval_DiscardAndAddToHandEffect
MUTATIONS["EnergyRetrieval_DiscardAndAddToHandEffect"] = {"source_symbol": "EnergyRetrieval_DiscardAndAddToHandEffect", "before": "\t\tAddCardToHand(moved.a);", "after": "\t\tAddCardToHand((uint8_t)(moved.a + 1u));", "case_ids": ["EnergyRetrieval_DiscardAndAddToHandEffect-0", "EnergyRetrieval_DiscardAndAddToHandEffect-1"]}
# <<< factory-mutation EnergyRetrieval_DiscardAndAddToHandEffect
# >>> factory-mutation SuperEnergyRetrieval_DiscardAndAddToHandEffect
MUTATIONS["SuperEnergyRetrieval_DiscardAndAddToHandEffect"] = {"source_symbol": "SuperEnergyRetrieval_DiscardAndAddToHandEffect", "before": "\t\tgb_write8(de, a);", "after": "\t\tgb_write8(de, 0u);", "case_ids": ["SuperEnergyRetrieval_DiscardAndAddToHandEffect-0", "SuperEnergyRetrieval_DiscardAndAddToHandEffect-1", "SuperEnergyRetrieval_DiscardAndAddToHandEffect-2"]}
# <<< factory-mutation SuperEnergyRetrieval_DiscardAndAddToHandEffect
# >>> factory-mutation HandleDefendingPokemonAttackSelection
MUTATIONS["HandleDefendingPokemonAttackSelection"] = {"source_symbol": "HandleDefendingPokemonAttackSelection", "before": "\thCurSelectionItem = 0u;", "after": "\thCurSelectionItem = 1u;", "case_ids": ["HandleDefendingPokemonAttackSelection-0", "HandleDefendingPokemonAttackSelection-1"]}
# <<< factory-mutation HandleDefendingPokemonAttackSelection
# >>> factory-mutation HandleEnergyDiscardEffectSelection
MUTATIONS["HandleEnergyDiscardEffectSelection"] = {"source_symbol": "HandleEnergyDiscardEffectSelection", "before": "\t\thTemp_ffa0 = 0xffu;", "after": "\t\thTemp_ffa0 = 0u;", "case_ids": ["HandleEnergyDiscardEffectSelection-0", "HandleEnergyDiscardEffectSelection-1", "HandleEnergyDiscardEffectSelection-2"]}
# <<< factory-mutation HandleEnergyDiscardEffectSelection
# >>> factory-mutation DragonairHyperBeam_PlayerSelectEffect
MUTATIONS["DragonairHyperBeam_PlayerSelectEffect"] = {"source_symbol": "DragonairHyperBeam_PlayerSelectEffect", "before": "\tHandleEnergyDiscardEffectSelection();", "after": "\t(void)0;", "case_ids": ["DragonairHyperBeam_PlayerSelectEffect-0", "DragonairHyperBeam_PlayerSelectEffect-1", "DragonairHyperBeam_PlayerSelectEffect-2"]}
# <<< factory-mutation DragonairHyperBeam_PlayerSelectEffect
# >>> factory-mutation GolduckHyperBeam_PlayerSelectEffect
MUTATIONS["GolduckHyperBeam_PlayerSelectEffect"] = {"source_symbol": "GolduckHyperBeam_PlayerSelectEffect", "before": "\t\thTemp_ffa0 = 0xFFu;", "after": "\t\thTemp_ffa0 = 0u;", "case_ids": ["GolduckHyperBeam_PlayerSelectEffect-0", "GolduckHyperBeam_PlayerSelectEffect-1"]}
# <<< factory-mutation GolduckHyperBeam_PlayerSelectEffect
# >>> factory-mutation MirrorMove_PlayerSelection
MUTATIONS["MirrorMove_PlayerSelection"] = {"source_symbol": "MirrorMove_PlayerSelection", "before": "\tif (r.a == LAST_TURN_EFFECT_DISCARD_ENERGY)", "after": "\tif (r.a == 0x02u)", "case_ids": ["MirrorMove_PlayerSelection-0"]}
# <<< factory-mutation MirrorMove_PlayerSelection
# >>> factory-mutation SpearowMirrorMove_PlayerSelection
MUTATIONS["SpearowMirrorMove_PlayerSelection"] = {"source_symbol": "SpearowMirrorMove_PlayerSelection", "before": "\tMirrorMove_PlayerSelection();", "after": "\treturn;", "case_ids": ["SpearowMirrorMove_PlayerSelection-0", "SpearowMirrorMove_PlayerSelection-2"]}
# <<< factory-mutation SpearowMirrorMove_PlayerSelection
# >>> factory-mutation StrangeBehavior_SelectAndSwapEffect
MUTATIONS["StrangeBehavior_SelectAndSwapEffect"] = {"source_symbol": "StrangeBehavior_SelectAndSwapEffect", "before": "\t\t(void)PrintPlayAreaCardList_EnableLCD();\n\t\treturn;", "after": "\t\treturn;", "case_ids": ["StrangeBehavior_SelectAndSwapEffect-0", "StrangeBehavior_SelectAndSwapEffect-1"]}
# <<< factory-mutation StrangeBehavior_SelectAndSwapEffect
# >>> factory-mutation PidgeottoMirrorMove_PlayerSelection
MUTATIONS["PidgeottoMirrorMove_PlayerSelection"] = {"source_symbol": "PidgeottoMirrorMove_PlayerSelection", "before": "void PidgeottoMirrorMove_PlayerSelection(void)\n{\n\tMirrorMove_PlayerSelection();\n}", "after": "void PidgeottoMirrorMove_PlayerSelection(void)\n{\n\t(void)0;\n}", "case_ids": ["PidgeottoMirrorMove_PlayerSelection-0"]}
# <<< factory-mutation PidgeottoMirrorMove_PlayerSelection
# >>> factory-mutation LookForCardsInDeck
MUTATIONS["LookForCardsInDeck"] = {"source_symbol": "LookForCardsInDeck", "before": "\tuint8_t no_cards = (wDuelTempList == 0xffu);", "after": "\tuint8_t no_cards = (wDuelTempList != 0xffu);", "case_ids": ["LookForCardsInDeck-0", "LookForCardsInDeck-1", "LookForCardsInDeck-2"]}
# <<< factory-mutation LookForCardsInDeck
# >>> factory-mutation KadabraRecover_PlayerSelectEffect
MUTATIONS["KadabraRecover_PlayerSelectEffect"] = {
 "source_symbol": "KadabraRecover_PlayerSelectEffect",
 "before": "\treturn (KadabraRecover_PlayerSelectEffectResult){card, input.f};",
 "after": "\treturn (KadabraRecover_PlayerSelectEffectResult){card, 0x10u};",
 "case_ids": ["KadabraRecover_PlayerSelectEffect-1", "KadabraRecover_PlayerSelectEffect-2"],
}
# <<< factory-mutation KadabraRecover_PlayerSelectEffect
# >>> factory-mutation Scavenge_PlayerSelectEnergyEffect
MUTATIONS["Scavenge_PlayerSelectEnergyEffect"] = {
 "source_symbol": "Scavenge_PlayerSelectEnergyEffect",
 "before": "\treturn (Scavenge_PlayerSelectEnergyEffectResult){card, (uint8_t)(card == 0u ? 0x80u : 0x00u)};",
 "after": "\treturn (Scavenge_PlayerSelectEnergyEffectResult){card, 0x10u};",
 "case_ids": ["Scavenge_PlayerSelectEnergyEffect-1", "Scavenge_PlayerSelectEnergyEffect-2"],
}
# <<< factory-mutation Scavenge_PlayerSelectEnergyEffect
# >>> factory-mutation PlayerPickFireEnergyCardToDiscard
MUTATIONS["PlayerPickFireEnergyCardToDiscard"] = {
 "source_symbol": "PlayerPickFireEnergyCardToDiscard",
 "before": "\treturn (PlayerPickFireEnergyCardToDiscardResult){card, 0x90u};",
 "after": "\treturn (PlayerPickFireEnergyCardToDiscardResult){card, 0u};",
 "case_ids": ["PlayerPickFireEnergyCardToDiscard-0", "PlayerPickFireEnergyCardToDiscard-1"],
}
# <<< factory-mutation PlayerPickFireEnergyCardToDiscard
# >>> factory-mutation ArcanineFlamethrower_PlayerSelectEffect
MUTATIONS["ArcanineFlamethrower_PlayerSelectEffect"] = {"source_symbol": "ArcanineFlamethrower_PlayerSelectEffect", "before": "PlayerPickFireEnergyCardToDiscardResult ArcanineFlamethrower_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();\n}", "after": "PlayerPickFireEnergyCardToDiscardResult ArcanineFlamethrower_PlayerSelectEffect(void)\n{\n\treturn (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};\n}", "case_ids": ["ArcanineFlamethrower_PlayerSelectEffect-0", "ArcanineFlamethrower_PlayerSelectEffect-1"]}
# <<< factory-mutation ArcanineFlamethrower_PlayerSelectEffect
# >>> factory-mutation CharmeleonFlamethrower_PlayerSelectEffect
MUTATIONS["CharmeleonFlamethrower_PlayerSelectEffect"] = {"source_symbol": "CharmeleonFlamethrower_PlayerSelectEffect", "before": "PlayerPickFireEnergyCardToDiscardResult CharmeleonFlamethrower_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();\n}", "after": "PlayerPickFireEnergyCardToDiscardResult CharmeleonFlamethrower_PlayerSelectEffect(void)\n{\n\treturn (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};\n}", "case_ids": ["CharmeleonFlamethrower_PlayerSelectEffect-0", "CharmeleonFlamethrower_PlayerSelectEffect-1"]}
# <<< factory-mutation CharmeleonFlamethrower_PlayerSelectEffect
# >>> factory-mutation Barrier_PlayerSelectEffect
MUTATIONS["Barrier_PlayerSelectEffect"] = {"source_symbol": "Barrier_PlayerSelectEffect", "before": "Barrier_PlayerSelectEffectResult Barrier_PlayerSelectEffect(void)\n{\n\t(void)CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01);\n\t\tDisplayEnergyDiscardScreen(PLAY_AREA_ARENA);\n\t\tBankswitchROM(saved);\n\t}\n\tHandleEnergyDiscardMenuInputResult menu;\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01);\n\t\tmenu = HandleEnergyDiscardMenuInput();\n\t\tBankswitchROM(saved);\n\t}\n\tif (menu.f & 0x10)\n\t\treturn (Barrier_PlayerSelectEffectResult){menu.a, menu.f};\n\thTemp_ffa0 = hTempCardIndex_ff98;", "after": "Barrier_PlayerSelectEffectResult Barrier_PlayerSelectEffect(void)\n{\n\t(void)CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01);\n\t\tDisplayEnergyDiscardScreen(PLAY_AREA_ARENA);\n\t\tBankswitchROM(saved);\n\t}\n\tHandleEnergyDiscardMenuInputResult menu;\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01);\n\t\tmenu = HandleEnergyDiscardMenuInput();\n\t\tBankswitchROM(saved);\n\t}\n\tif (menu.f & 0x10)\n\t\treturn (Barrier_PlayerSelectEffectResult){menu.a, menu.f};\n\thTemp_ffa0 = 0x00;", "case_ids": ["Barrier_PlayerSelectEffect-0", "Barrier_PlayerSelectEffect-1"]}
# <<< factory-mutation Barrier_PlayerSelectEffect
# >>> factory-mutation StarmieRecover_PlayerSelectEffect
MUTATIONS["StarmieRecover_PlayerSelectEffect"] = {
 "source_symbol": "StarmieRecover_PlayerSelectEffect",
 "before": "\treturn (StarmieRecover_PlayerSelectEffectResult){card, input.f};",
 "after": "\treturn (StarmieRecover_PlayerSelectEffectResult){card, 0x10u};",
 "case_ids": ["StarmieRecover_PlayerSelectEffect-0", "StarmieRecover_PlayerSelectEffect-1"],
}
# <<< factory-mutation StarmieRecover_PlayerSelectEffect
# >>> factory-mutation DestinyBond_PlayerSelectEffect
MUTATIONS["DestinyBond_PlayerSelectEffect"] = {"source_symbol": "DestinyBond_PlayerSelectEffect", "before": "DestinyBond_PlayerSelectEffectResult DestinyBond_PlayerSelectEffect(void)\n{\n\t(void)CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x01);\n\tDisplayEnergyDiscardScreen(0x00);\n\tBankswitchROM(saved);\n\tHandleEnergyDiscardMenuInputResult result = HandleEnergyDiscardMenuInput();\n\tif (result.f & 0x10)\n\t\treturn (DestinyBond_PlayerSelectEffectResult){result.a, result.f};\n\thTempList = hTempCardIndex_ff98;", "after": "DestinyBond_PlayerSelectEffectResult DestinyBond_PlayerSelectEffect(void)\n{\n\t(void)CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x01);\n\tDisplayEnergyDiscardScreen(0x00);\n\tBankswitchROM(saved);\n\tHandleEnergyDiscardMenuInputResult result = HandleEnergyDiscardMenuInput();\n\tif (result.f & 0x10)\n\t\treturn (DestinyBond_PlayerSelectEffectResult){result.a, result.f};\n\thTempList = 0x00;", "case_ids": ["DestinyBond_PlayerSelectEffect-0"]}
# <<< factory-mutation DestinyBond_PlayerSelectEffect
# >>> factory-mutation FlamesOfRage_PlayerSelectEffect
MUTATIONS["FlamesOfRage_PlayerSelectEffect"] = {"source_symbol": "FlamesOfRage_PlayerSelectEffect", "before": "void FlamesOfRage_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseAndDiscard2FireEnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateListOfFireEnergyAttachedToArena();\n\t{ uint8_t saved = hBankROM; BankswitchROM(0x01); DisplayEnergyDiscardScreen(PLAY_AREA_ARENA);", "after": "void FlamesOfRage_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseAndDiscard2FireEnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateListOfFireEnergyAttachedToArena();\n\t{ uint8_t saved = hBankROM; BankswitchROM(0x01); DisplayEnergyDiscardScreen(0x01);", "case_ids": ["FlamesOfRage_PlayerSelectEffect-0", "FlamesOfRage_PlayerSelectEffect-1"]}
# <<< factory-mutation FlamesOfRage_PlayerSelectEffect
# >>> factory-mutation HandleColorChangeScreen
MUTATIONS["HandleColorChangeScreen"] = {"source_symbol": "HandleColorChangeScreen", "before": "uint8_t color = (uint8_t)(item + 1u);", "after": "uint8_t color = (uint8_t)(item + 2u);", "case_ids": ["HandleColorChangeScreen-0", "HandleColorChangeScreen-1"]}
# <<< factory-mutation HandleColorChangeScreen
# >>> factory-mutation Ember_PlayerSelectEffect
MUTATIONS["Ember_PlayerSelectEffect"] = {"source_symbol": "Ember_PlayerSelectEffect", "before": "PlayerPickFireEnergyCardToDiscardResult Ember_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();\n}", "after": "PlayerPickFireEnergyCardToDiscardResult Ember_PlayerSelectEffect(void)\n{\n\tPlayerPickFireEnergyCardToDiscardResult r = PlayerPickFireEnergyCardToDiscard();\n\treturn (PlayerPickFireEnergyCardToDiscardResult){r.a, (uint8_t)(r.f ^ 0x01u)};\n}", "case_ids": ["Ember_PlayerSelectEffect-0", "Ember_PlayerSelectEffect-1"]}
# <<< factory-mutation Ember_PlayerSelectEffect
# >>> factory-mutation FireBlast_PlayerSelectEffect
MUTATIONS["FireBlast_PlayerSelectEffect"] = {
 "source_symbol": "FireBlast_PlayerSelectEffect",
 "before": "PlayerPickFireEnergyCardToDiscardResult FireBlast_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();",
 "after": "PlayerPickFireEnergyCardToDiscardResult FireBlast_PlayerSelectEffect(void)\n{\n\t(void)PlayerPickFireEnergyCardToDiscard();\n\treturn (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};",
 "case_ids": ["FireBlast_PlayerSelectEffect-0", "FireBlast_PlayerSelectEffect-1"],
}
# <<< factory-mutation FireBlast_PlayerSelectEffect
# >>> factory-mutation MagmarFlamethrower_PlayerSelectEffect
MUTATIONS["MagmarFlamethrower_PlayerSelectEffect"] = {"source_symbol": "MagmarFlamethrower_PlayerSelectEffect", "before": "PlayerPickFireEnergyCardToDiscardResult MagmarFlamethrower_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();\n}", "after": "PlayerPickFireEnergyCardToDiscardResult MagmarFlamethrower_PlayerSelectEffect(void)\n{\n\treturn (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};\n}", "case_ids": ["MagmarFlamethrower_PlayerSelectEffect-0", "MagmarFlamethrower_PlayerSelectEffect-1"]}
# <<< factory-mutation MagmarFlamethrower_PlayerSelectEffect
# >>> factory-mutation FlareonFlamethrower_PlayerSelectEffect
MUTATIONS["FlareonFlamethrower_PlayerSelectEffect"] = {
 "source_symbol": "FlareonFlamethrower_PlayerSelectEffect",
 "before": "PlayerPickFireEnergyCardToDiscardResult FlareonFlamethrower_PlayerSelectEffect(void)\n{\n\treturn PlayerPickFireEnergyCardToDiscard();",
 "after": "PlayerPickFireEnergyCardToDiscardResult FlareonFlamethrower_PlayerSelectEffect(void)\n{\n\t(void)PlayerPickFireEnergyCardToDiscard();\n\treturn (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};",
 "case_ids": ["FlareonFlamethrower_PlayerSelectEffect-0", "FlareonFlamethrower_PlayerSelectEffect-1"],
}
# <<< factory-mutation FlareonFlamethrower_PlayerSelectEffect
# >>> factory-mutation Conversion1_PlayerSelectEffect
MUTATIONS["Conversion1_PlayerSelectEffect"] = {
 "source_symbol": "Conversion1_PlayerSelectEffect",
 "before": "\thTemp_ffa0 = r.a;\n\treturn r;\n}",
 "after": "\thTemp_ffa0 = (uint8_t)(r.a + 1u);\n\treturn r;\n}",
 "case_ids": ["Conversion1_PlayerSelectEffect-0", "Conversion1_PlayerSelectEffect-1"],
}
# <<< factory-mutation Conversion1_PlayerSelectEffect
# >>> factory-mutation Conversion2_PlayerSelectEffect
MUTATIONS["Conversion2_PlayerSelectEffect"] = {
 "source_symbol": "Conversion2_PlayerSelectEffect",
 "before": "HandleColorChangeScreenResult Conversion2_PlayerSelectEffect(void)\n{\n\tHandleColorChangeScreenResult r =\n\t\tHandleColorChangeScreen(0x80u, 0u, 0u, 0u, 0u, 0u,\n\t\t\t\tChooseResistanceYouWishToChangeText);\n\thTemp_ffa0 = r.a;",
 "after": "HandleColorChangeScreenResult Conversion2_PlayerSelectEffect(void)\n{\n\tHandleColorChangeScreenResult r =\n\t\tHandleColorChangeScreen(0x80u, 0u, 0u, 0u, 0u, 0u,\n\t\t\t\tChooseResistanceYouWishToChangeText);\n\thTemp_ffa0 = (uint8_t)(r.a + 1u);",
 "case_ids": ["Conversion2_PlayerSelectEffect-0", "Conversion2_PlayerSelectEffect-1"]
}
# <<< factory-mutation Conversion2_PlayerSelectEffect
# >>> factory-mutation AskWhetherToQuitSelectingCards
MUTATIONS["AskWhetherToQuitSelectingCards"] = {"source_symbol": "AskWhetherToQuitSelectingCards", "before": "\tuint8_t remaining = (uint8_t)(a - hCurSelectionItem);", "after": "\tuint8_t remaining = (uint8_t)(a - hCurSelectionItem - 1u);", "case_ids": ["AskWhetherToQuitSelectingCards-0", "AskWhetherToQuitSelectingCards-1", "AskWhetherToQuitSelectingCards-2"]}
# <<< factory-mutation AskWhetherToQuitSelectingCards
# >>> factory-mutation Scavenge_AddToHandEffect
MUTATIONS["Scavenge_AddToHandEffect"] = {
 "source_symbol": "Scavenge_AddToHandEffect",
 "before": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(hTempPlayAreaLocation_ffa1);\n\tAddCardToHand(moved.a);",
 "after": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(hTempPlayAreaLocation_ffa1);\n\tAddCardToHand((uint8_t)(moved.a + 1u));",
 "case_ids": ["Scavenge_AddToHandEffect-0", "Scavenge_AddToHandEffect-1"],
}
# <<< factory-mutation Scavenge_AddToHandEffect
# >>> factory-mutation Recycle_AddToHandEffect
MUTATIONS["Recycle_AddToHandEffect"] = {
 "source_symbol": "Recycle_AddToHandEffect",
 "before": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(index);\n\tReturnCardToDeck(moved.a);",
 "after": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(index);\n\tReturnCardToDeck((uint8_t)(moved.a + 1u));",
 "case_ids": ["Recycle_AddToHandEffect-1", "Recycle_AddToHandEffect-2"],
}
# <<< factory-mutation Recycle_AddToHandEffect
# >>> factory-mutation PokemonBreeder_EvolveEffect
MUTATIONS["PokemonBreeder_EvolveEffect"] = {"source_symbol": "PokemonBreeder_EvolveEffect", "before": "PokemonBreederEvolveEffectResult PokemonBreeder_EvolveEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t saved_a = hTempCardIndex_ff9f;\n\tuint8_t entry_f = f;\n\thTempCardIndex_ff98 = hTemp_ffa0;", "after": "PokemonBreederEvolveEffectResult PokemonBreeder_EvolveEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t saved_a = hTempCardIndex_ff9f;\n\tuint8_t entry_f = f;\n\thTempCardIndex_ff98 = 0u;", "case_ids": ["PokemonBreeder_EvolveEffect-0", "PokemonBreeder_EvolveEffect-1", "PokemonBreeder_EvolveEffect-2"]}
# <<< factory-mutation PokemonBreeder_EvolveEffect
# >>> factory-mutation Sprout_PutInPlayAreaEffect
MUTATIONS["Sprout_PutInPlayAreaEffect"] = {
 "source_symbol": "Sprout_PutInPlayAreaEffect",
 "before": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand(index);",
 "after": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand((uint8_t)(index + 1u));",
 "case_ids": ["Sprout_PutInPlayAreaEffect-0", "Sprout_PutInPlayAreaEffect-1"],
}
# <<< factory-mutation Sprout_PutInPlayAreaEffect
# >>> factory-mutation NidoranFCallForFamily_PutInPlayAreaEffect
MUTATIONS["NidoranFCallForFamily_PutInPlayAreaEffect"] = {
 "source_symbol": "NidoranFCallForFamily_PutInPlayAreaEffect",
 "before": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand(index);",
 "after": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand((uint8_t)(index + 1u));",
 "case_ids": ["NidoranFCallForFamily_PutInPlayAreaEffect-0", "NidoranFCallForFamily_PutInPlayAreaEffect-1"],
}
# <<< factory-mutation NidoranFCallForFamily_PutInPlayAreaEffect
# >>> factory-mutation MarowakCallForFamily_PutInPlayAreaEffect
MUTATIONS["MarowakCallForFamily_PutInPlayAreaEffect"] = {
 "source_symbol": "MarowakCallForFamily_PutInPlayAreaEffect",
 "before": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand(index);",
 "after": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand((uint8_t)(index + 1u));",
 "case_ids": ["MarowakCallForFamily_PutInPlayAreaEffect-0", "MarowakCallForFamily_PutInPlayAreaEffect-1"],
}
# <<< factory-mutation MarowakCallForFamily_PutInPlayAreaEffect
# >>> factory-mutation KrabbyCallForFamily_PutInPlayAreaEffect
MUTATIONS["KrabbyCallForFamily_PutInPlayAreaEffect"] = {
 "source_symbol": "KrabbyCallForFamily_PutInPlayAreaEffect",
 "before": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand(index);",
 "after": "\t\tSearchCardInDeckAndAddToHand(index);\n\t\tAddCardToHand((uint8_t)(index + 1u));",
 "case_ids": ["KrabbyCallForFamily_PutInPlayAreaEffect-0", "KrabbyCallForFamily_PutInPlayAreaEffect-1"],
}
# <<< factory-mutation KrabbyCallForFamily_PutInPlayAreaEffect
# >>> factory-mutation PokemonFlute_PlaceInPlayAreaText
MUTATIONS["PokemonFlute_PlaceInPlayAreaText"] = {
    "source_symbol": "PokemonFlute_PlaceInPlayAreaText",
    "before": "void PokemonFlute_PlaceInPlayAreaText(void)\n{\n\tuint8_t index = hTemp_ffa0;",
    "after": "void PokemonFlute_PlaceInPlayAreaText(void)\n{\n\tuint8_t index = (uint8_t)(hTemp_ffa0 + 1u);",
    "case_ids": ["PokemonFlute_PlaceInPlayAreaText-0", "PokemonFlute_PlaceInPlayAreaText-1"],
}
# <<< factory-mutation PokemonFlute_PlaceInPlayAreaText
# >>> factory-mutation Revive_PlaceInPlayAreaEffect
MUTATIONS["Revive_PlaceInPlayAreaEffect"] = {
 "source_symbol": "Revive_PlaceInPlayAreaEffect",
 "before": "\tif ((half & 0x01u) != 0u)\n\t\thalf = (uint8_t)(half + 5u);",
 "after": "\tif ((half & 0x01u) == 0u)\n\t\thalf = (uint8_t)(half + 5u);",
 "case_ids": ["Revive_PlaceInPlayAreaEffect-0", "Revive_PlaceInPlayAreaEffect-1"],
}
# <<< factory-mutation Revive_PlaceInPlayAreaEffect
# >>> factory-mutation ItemFinder_DiscardAddToHandEffect
MUTATIONS["ItemFinder_DiscardAddToHandEffect"] = {
 "source_symbol": "ItemFinder_DiscardAddToHandEffect",
 "before": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(wanted);\n\tAddCardToHand(moved.a);",
 "after": "\tMoveDiscardResult moved = MoveDiscardPileCardToHand(wanted);\n\tAddCardToHand((uint8_t)(moved.a + 1u));",
 "case_ids": ["ItemFinder_DiscardAddToHandEffect-0", "ItemFinder_DiscardAddToHandEffect-1"],
}
# <<< factory-mutation ItemFinder_DiscardAddToHandEffect
# >>> factory-mutation BellsproutCallForFamily_PutInPlayAreaEffect
MUTATIONS["BellsproutCallForFamily_PutInPlayAreaEffect"] = {
 "source_symbol": "BellsproutCallForFamily_PutInPlayAreaEffect",
 "before": "ShuffleCardsInDeckResult BellsproutCallForFamily_PutInPlayAreaEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t index = hTemp_ffa0;\n\tif (index != 0xFFu) {\n\t\tSearchCardInDeckAndAddToHand(index);",
 "after": "ShuffleCardsInDeckResult BellsproutCallForFamily_PutInPlayAreaEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t index = hTemp_ffa0;\n\tif (index != 0xFFu) {\n\t\tSearchCardInDeckAndAddToHand((uint8_t)(index + 1u));",
 "case_ids": ["BellsproutCallForFamily_PutInPlayAreaEffect-0", "BellsproutCallForFamily_PutInPlayAreaEffect-1"],
}
# <<< factory-mutation BellsproutCallForFamily_PutInPlayAreaEffect
# >>> factory-mutation Wildfire_PlayerSelectEffect
MUTATIONS["Wildfire_PlayerSelectEffect"] = {"source_symbol": "Wildfire_PlayerSelectEffect", "before": "Wildfire_PlayerSelectEffectResult Wildfire_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(DiscardOppDeckAsManyFireEnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateListOfFireEnergyAttachedToArena();\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01u);\n\t\tDisplayEnergyDiscardScreen(PLAY_AREA_ARENA);","after":"Wildfire_PlayerSelectEffectResult Wildfire_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(DiscardOppDeckAsManyFireEnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateListOfFireEnergyAttachedToArena();\n\t{\n\t\tuint8_t saved = hBankROM;\n\t\tBankswitchROM(0x01u);\n\t\tDisplayEnergyDiscardScreen(0x01u);","case_ids": ["Wildfire_PlayerSelectEffect-0", "Wildfire_PlayerSelectEffect-1"]}
# <<< factory-mutation Wildfire_PlayerSelectEffect
# >>> factory-mutation Whirlpool_PlayerSelectEffect
MUTATIONS["Whirlpool_PlayerSelectEffect"] = {"source_symbol": "Whirlpool_PlayerSelectEffect", "before": "void Whirlpool_PlayerSelectEffect(void)\n{\n\tSwapTurn();\n\tHandListResult list = CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);\n\tif ((list.f & 0x10u) != 0u) {\n\t\tSwapTurn();\n\t\thTemp_ffa0 = 0xffu;", "after": "void Whirlpool_PlayerSelectEffect(void)\n{\n\tSwapTurn();\n\tHandListResult list = CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);\n\tif ((list.f & 0x10u) != 0u) {\n\t\tSwapTurn();\n\t\thTemp_ffa0 = 0x00u;", "case_ids": ["Whirlpool_PlayerSelectEffect-0", "Whirlpool_PlayerSelectEffect-1"]}
# <<< factory-mutation Whirlpool_PlayerSelectEffect
# >>> factory-mutation FireSpin_PlayerSelectEffect
MUTATIONS["FireSpin_PlayerSelectEffect"] = {"source_symbol": "FireSpin_PlayerSelectEffect", "before": "void FireSpin_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseAndDiscard2EnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);\n\t(void)SortCardsInDuelTempListByID(0u, 0u, 0u);\n\t{ uint8_t saved = hBankROM; BankswitchROM(0x01u); DisplayEnergyDiscardScreen(PLAY_AREA_ARENA); BankswitchROM(saved); }\n\tuint8_t denominator = 2u;", "after": "void FireSpin_PlayerSelectEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseAndDiscard2EnergyCardsText);\n\thCurSelectionItem = 0u;\n\t(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);\n\t(void)SortCardsInDuelTempListByID(0u, 0u, 0u);\n\t{ uint8_t saved = hBankROM; BankswitchROM(0x01u); DisplayEnergyDiscardScreen(PLAY_AREA_ARENA); BankswitchROM(saved); }\n\tuint8_t denominator = 3u;", "case_ids": ["FireSpin_PlayerSelectEffect-0"]}
# <<< factory-mutation FireSpin_PlayerSelectEffect
# >>> factory-mutation EnergySpike_AttachEnergyEffect
MUTATIONS["EnergySpike_AttachEnergyEffect"] = {"source_symbol": "EnergySpike_AttachEnergyEffect", "before": "ShuffleCardsInDeckResult EnergySpike_AttachEnergyEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t index = hTemp_ffa0;\n\tif (index != 0xFFu) {", "after": "ShuffleCardsInDeckResult EnergySpike_AttachEnergyEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t index = hTemp_ffa0;\n\tif (index == 0xFFu) {", "case_ids": ["EnergySpike_AttachEnergyEffect-0", "EnergySpike_AttachEnergyEffect-1"]}
# <<< factory-mutation EnergySpike_AttachEnergyEffect
# >>> factory-mutation ScoopUp_ReturnToHandEffect
MUTATIONS["ScoopUp_ReturnToHandEffect"] = {"source_symbol": "ScoopUp_ReturnToHandEffect", "before": "void ScoopUp_ReturnToHandEffect(void)\n{\n\tuint8_t location = hTemp_ffa0;", "after": "void ScoopUp_ReturnToHandEffect(void)\n{\n\tuint8_t location = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["ScoopUp_ReturnToHandEffect-0", "ScoopUp_ReturnToHandEffect-1", "ScoopUp_ReturnToHandEffect-2"]}
# <<< factory-mutation ScoopUp_ReturnToHandEffect
# >>> factory-mutation EnergyTrans_TransferEffect
MUTATIONS["EnergyTrans_TransferEffect"] = {"source_symbol": "EnergyTrans_TransferEffect", "before": "\t\tuint8_t result = PrintPlayAreaCardList_EnableLCD().a;\n\t\treturn result;", "after": "\t\treturn 0u;", "case_ids": ["EnergyTrans_TransferEffect-0", "EnergyTrans_TransferEffect-1", "EnergyTrans_TransferEffect-2"]}
# <<< factory-mutation EnergyTrans_TransferEffect
# >>> factory-mutation DamageSwap_SelectAndSwapEffect
MUTATIONS["DamageSwap_SelectAndSwapEffect"] = {"source_symbol": "DamageSwap_SelectAndSwapEffect", "before": "void DamageSwap_SelectAndSwapEffect(void)\n{\n\tDuelistVarResult turn = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);\n\tif (turn.a != DUELIST_TYPE_PLAYER) {\n\t\tSetupPlayAreaScreen();\n\t\t(void)PrintPlayAreaCardList_EnableLCD();", "after": "void DamageSwap_SelectAndSwapEffect(void)\n{\n\tDuelistVarResult turn = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);\n\tif (turn.a != DUELIST_TYPE_PLAYER) {\n\t\tSetupPlayAreaScreen();", "case_ids": ["DamageSwap_SelectAndSwapEffect-0", "DamageSwap_SelectAndSwapEffect-1"]}
# <<< factory-mutation DamageSwap_SelectAndSwapEffect
# >>> factory-mutation Gigashock_PlayerSelectEffect
MUTATIONS["Gigashock_PlayerSelectEffect"] = {"source_symbol": "Gigashock_PlayerSelectEffect", "before": "\t\thTempList = 0xffu;", "after": "\t\thTempList = 0x00u;", "case_ids": ["Gigashock_PlayerSelectEffect-0", "Gigashock_PlayerSelectEffect-1"]}
# <<< factory-mutation Gigashock_PlayerSelectEffect
# >>> factory-mutation HandleSwitchDefendingPokemonEffect
MUTATIONS["HandleSwitchDefendingPokemonEffect"] = {"source_symbol": "HandleSwitchDefendingPokemonEffect", "before": "\twDefendingWasForcedToSwitch = 1u;", "after": "\twDefendingWasForcedToSwitch = 0u;", "case_ids": ["HandleSwitchDefendingPokemonEffect-1", "HandleSwitchDefendingPokemonEffect-2"]}
# <<< factory-mutation HandleSwitchDefendingPokemonEffect
# >>> factory-mutation PidgeottoWhirlwind_SwitchEffect
MUTATIONS["PidgeottoWhirlwind_SwitchEffect"] = {
    "source_symbol": "PidgeottoWhirlwind_SwitchEffect",
    "before": "HandleSwitchDefendingPokemonEffectResult PidgeottoWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult result = HandleSwitchDefendingPokemonEffect(input);",
    "after": "HandleSwitchDefendingPokemonEffectResult PidgeottoWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult result = HandleSwitchDefendingPokemonEffect(0xffu);",
    "case_ids": ["PidgeottoWhirlwind_SwitchEffect-1", "PidgeottoWhirlwind_SwitchEffect-2"]
}
# <<< factory-mutation PidgeottoWhirlwind_SwitchEffect
# >>> factory-mutation ButterfreeWhirlwind_SwitchEffect
MUTATIONS["ButterfreeWhirlwind_SwitchEffect"] = {
    "source_symbol": "ButterfreeWhirlwind_SwitchEffect",
    "before": "ButterfreeWhirlwind_SwitchEffectResult ButterfreeWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult callee = HandleSwitchDefendingPokemonEffect(input);",
    "after": "ButterfreeWhirlwind_SwitchEffectResult ButterfreeWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult callee = HandleSwitchDefendingPokemonEffect(0xffu);",
    "case_ids": ["ButterfreeWhirlwind_SwitchEffect-1", "ButterfreeWhirlwind_SwitchEffect-2"]
}
# <<< factory-mutation ButterfreeWhirlwind_SwitchEffect
# >>> factory-mutation PidgeyWhirlwind_SwitchEffect
MUTATIONS["PidgeyWhirlwind_SwitchEffect"] = {
    "source_symbol": "PidgeyWhirlwind_SwitchEffect",
    "before": "HandleSwitchDefendingPokemonEffectResult PidgeyWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult result = HandleSwitchDefendingPokemonEffect(input);",
    "after": "HandleSwitchDefendingPokemonEffectResult PidgeyWhirlwind_SwitchEffect(void)\n{\n\tuint8_t input = hTemp_ffa0;\n\tHandleSwitchDefendingPokemonEffectResult result = HandleSwitchDefendingPokemonEffect(0xffu);",
    "case_ids": ["PidgeyWhirlwind_SwitchEffect-1", "PidgeyWhirlwind_SwitchEffect-2"]
}
# <<< factory-mutation PidgeyWhirlwind_SwitchEffect
# >>> factory-mutation TerrorStrike_SwitchDefendingPokemon
MUTATIONS["TerrorStrike_SwitchDefendingPokemon"] = {"source_symbol": "TerrorStrike_SwitchDefendingPokemon", "before": "HandleSwitchDefendingPokemonEffectResult TerrorStrike_SwitchDefendingPokemon(void)\n{\n\tuint8_t gate = hTemp_ffa0;\n\tif (gate == 0u)\n\t\treturn (HandleSwitchDefendingPokemonEffectResult){0u, 0x80u};\n\tuint8_t input = hTempPlayAreaLocation_ffa1;", "after": "HandleSwitchDefendingPokemonEffectResult TerrorStrike_SwitchDefendingPokemon(void)\n{\n\tuint8_t gate = hTemp_ffa0;\n\tif (gate == 0u)\n\t\treturn (HandleSwitchDefendingPokemonEffectResult){0u, 0x80u};\n\tuint8_t input = 0xffu;", "case_ids": ["TerrorStrike_SwitchDefendingPokemon-2"]}
# <<< factory-mutation TerrorStrike_SwitchDefendingPokemon
# >>> factory-mutation Gale_SwitchEffect
MUTATIONS["Gale_SwitchEffect"] = {"source_symbol": "Gale_SwitchEffect", "before": "\t\twDealtDamage = 0u;\n\t\t*(wDealtDamage_PTR + 1) = 0u;", "after": "\t\twDealtDamage = 1u;\n\t\t*(wDealtDamage_PTR + 1) = 0u;", "case_ids": ["Gale_SwitchEffect-0", "Gale_SwitchEffect-1"]}
# <<< factory-mutation Gale_SwitchEffect
# >>> factory-mutation Shift_PlayerSelectEffect
MUTATIONS["Shift_PlayerSelectEffect"] = {"source_symbol": "Shift_PlayerSelectEffect", "before": "HandleColorChangeScreenResult Shift_PlayerSelectEffect(void)\n{\n\tfor (;;) {\n\t\tHandleColorChangeScreenResult selected =\n\t\t\tHandleColorChangeScreen((uint8_t)(hTemp_ffa0 | 0x80u), 0u, 0u, 0u, 0u, 0u,\n\t\t\t\tChoosePokemonWishToColorChangeText);\n\t\thAIPkmnPowerEffectParam = selected.a;\n\t\tif ((selected.f & 0x10u) != 0u)\n\t\t\treturn selected;\n\n\t\tuint8_t found = 0u;\n\t\tDuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\t\tfor (uint8_t slot = PLAY_AREA_ARENA; slot < count.a; ++slot) {\n\t\t\tif (GetPlayAreaCardColor(slot) == hAIPkmnPowerEffectParam) {\n\t\t\t\tfound = 1u;\n\t\t\t\tbreak;\n\t\t\t}\n\t\t}\n\t\tif (found == 0u) {\n\t\t\tSwapTurn();\n\t\t\tcount = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\t\t\tfor (uint8_t slot = PLAY_AREA_ARENA; slot < count.a; ++slot) {\n\t\t\t\tif (GetPlayAreaCardColor(slot) == hAIPkmnPowerEffectParam) {\n\t\t\t\t\tfound = 1u;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n\t\t\tSwapTurn();\n\t\t}\n\t\tif (found != 0u)\n\t\t\treturn (HandleColorChangeScreenResult){hAIPkmnPowerEffectParam, 0xC0u};","after":"HandleColorChangeScreenResult Shift_PlayerSelectEffect(void)\n{\n\tfor (;;) {\n\t\tHandleColorChangeScreenResult selected =\n\t\t\tHandleColorChangeScreen((uint8_t)(hTemp_ffa0 | 0x80u), 0u, 0u, 0u, 0u, 0u,\n\t\t\t\tChoosePokemonWishToColorChangeText);\n\t\thAIPkmnPowerEffectParam = selected.a;\n\t\tif ((selected.f & 0x10u) != 0u)\n\t\t\treturn selected;\n\n\t\tuint8_t found = 0u;\n\t\tDuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\t\tfor (uint8_t slot = PLAY_AREA_ARENA; slot < count.a; ++slot) {\n\t\t\tif (GetPlayAreaCardColor(slot) == hAIPkmnPowerEffectParam) {\n\t\t\t\tfound = 1u;\n\t\t\t\tbreak;\n\t\t\t}\n\t\t}\n\t\tif (found == 0u) {\n\t\t\tSwapTurn();\n\t\t\tcount = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\t\t\tfor (uint8_t slot = PLAY_AREA_ARENA; slot < count.a; ++slot) {\n\t\t\t\tif (GetPlayAreaCardColor(slot) == hAIPkmnPowerEffectParam) {\n\t\t\t\t\tfound = 1u;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n\t\t\tSwapTurn();\n\t\t}\n\t\tif (found != 0u)\n\t\t\treturn (HandleColorChangeScreenResult){hAIPkmnPowerEffectParam, 0x80u};","case_ids": ["Shift_PlayerSelectEffect-0", "Shift_PlayerSelectEffect-1"]}
# <<< factory-mutation Shift_PlayerSelectEffect
# >>> factory-mutation HandlePlayerMetronomeEffect
MUTATIONS["HandlePlayerMetronomeEffect"] = {"source_symbol": "HandlePlayerMetronomeEffect", "before": "uint8_t HandlePlayerMetronomeEffect(uint8_t a)\n{\n\twMetronomeEnergyCost = a;", "after": "uint8_t HandlePlayerMetronomeEffect(uint8_t a)\n{\n\twMetronomeEnergyCost = (uint8_t)(a + 1u);", "case_ids": ["HandlePlayerMetronomeEffect-0", "HandlePlayerMetronomeEffect-1", "HandlePlayerMetronomeEffect-2", "HandlePlayerMetronomeEffect-3"]}
# <<< factory-mutation HandlePlayerMetronomeEffect
# >>> factory-mutation ClefairyMetronome_UseAttackEffect
MUTATIONS["ClefairyMetronome_UseAttackEffect"] = {"source_symbol": "ClefairyMetronome_UseAttackEffect", "before": "uint8_t ClefairyMetronome_UseAttackEffect(void)\n{\n\tuint8_t energy_cost = 3u;", "after": "uint8_t ClefairyMetronome_UseAttackEffect(void)\n{\n\tuint8_t energy_cost = 0u;", "case_ids": ["ClefairyMetronome_UseAttackEffect-0", "ClefairyMetronome_UseAttackEffect-1"]}
# <<< factory-mutation ClefairyMetronome_UseAttackEffect
# >>> factory-mutation ClefableMetronome_UseAttackEffect
MUTATIONS["ClefableMetronome_UseAttackEffect"] = {"source_symbol": "ClefableMetronome_UseAttackEffect", "before": "uint8_t ClefableMetronome_UseAttackEffect(void)\n{\n\tuint8_t energy_cost = 1u;", "after": "uint8_t ClefableMetronome_UseAttackEffect(void)\n{\n\tuint8_t energy_cost = 0u;", "case_ids": ["ClefableMetronome_UseAttackEffect-0", "ClefableMetronome_UseAttackEffect-1"]}
# <<< factory-mutation ClefableMetronome_UseAttackEffect
# >>> factory-mutation Curse_PlayerSelectEffect
MUTATIONS["Curse_PlayerSelectEffect"] = {"source_symbol": "Curse_PlayerSelectEffect", "before": "Curse_PlayerSelectEffectResult Curse_PlayerSelectEffect(void)\n{\n\tDrawWholeScreenTextBox(ProcedureForCurseText);\n\tSwapTurn();", "after": "Curse_PlayerSelectEffectResult Curse_PlayerSelectEffect(void)\n{\n\tDrawWholeScreenTextBox(ProcedureForCurseText);", "case_ids": ["Curse_PlayerSelectEffect-0", "Curse_PlayerSelectEffect-1"]}
# <<< factory-mutation Curse_PlayerSelectEffect
# >>> factory-mutation MrFuji_ReturnToDeckEffect
MUTATIONS["MrFuji_ReturnToDeckEffect"] = {"source_symbol": "MrFuji_ReturnToDeckEffect", "before": "ShuffleCardsInDeckResult MrFuji_ReturnToDeckEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t location = hTemp_ffa0;", "after": "ShuffleCardsInDeckResult MrFuji_ReturnToDeckEffect(uint8_t b, uint8_t c, uint8_t d,\n\t\t\t\t\t\t\t   uint8_t e, uint16_t hl)\n{\n\tuint8_t location = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["MrFuji_ReturnToDeckEffect-0", "MrFuji_ReturnToDeckEffect-1"]}
# <<< factory-mutation MrFuji_ReturnToDeckEffect
# >>> factory-mutation Serial_TossCoinATimes
MUTATIONS["Serial_TossCoinATimes"] = {"source_symbol": "Serial_TossCoinATimes", "before": "SerialTossCoinATimesResult Serial_TossCoinATimes(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)SetOppAction_SerialSendDuelData(OPPACTION_TOSS_COIN_A_TIMES, (uint16_t)((uint16_t)d << 8 | e));\n\tSerialSend8Bytes(a, f, b, c, (uint16_t)((uint16_t)d << 8 | e), hl);\n\tTossCoinATimesResult result = TossCoinATimes(a, f, b, c, d, e, hl);", "after": "SerialTossCoinATimesResult Serial_TossCoinATimes(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)SetOppAction_SerialSendDuelData(OPPACTION_TOSS_COIN_A_TIMES, (uint16_t)((uint16_t)d << 8 | e));\n\tSerialSend8Bytes(a, f, b, c, (uint16_t)((uint16_t)d << 8 | e), hl);\n\tTossCoinATimesResult result = TossCoinATimes((uint8_t)(a + 1u), f, b, c, d, e, hl);", "case_ids": ["Serial_TossCoinATimes-0", "Serial_TossCoinATimes-1", "Serial_TossCoinATimes-2"]}
# <<< factory-mutation Serial_TossCoinATimes
# >>> factory-mutation TossCoinATimes_BankB
MUTATIONS["TossCoinATimes_BankB"] = {"source_symbol": "TossCoinATimes_BankB", "before": "TossCoinATimes_BankBResult TossCoinATimes_BankB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tTossCoinATimesResult result = TossCoinATimes(a, f, b, c, d, e, hl);", "after": "TossCoinATimes_BankBResult TossCoinATimes_BankB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tTossCoinATimesResult result = TossCoinATimes((uint8_t)(a + 1u), f, b, c, d, e, hl);", "case_ids": ["TossCoinATimes_BankB-0", "TossCoinATimes_BankB-1"]}
# <<< factory-mutation TossCoinATimes_BankB
# >>> factory-mutation Serial_TossZeroCoins
MUTATIONS["Serial_TossZeroCoins"] = {"source_symbol": "Serial_TossZeroCoins", "before": "SerialTossCoinATimesResult Serial_TossZeroCoins(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\treturn Serial_TossCoinATimes(0x00u, 0x80u, b, c, d, e, hl);", "after": "SerialTossCoinATimesResult Serial_TossZeroCoins(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\treturn Serial_TossCoinATimes(0x01u, 0x80u, b, c, d, e, hl);", "case_ids": ["Serial_TossZeroCoins-0", "Serial_TossZeroCoins-1"]}
# <<< factory-mutation Serial_TossZeroCoins
# >>> factory-mutation Serial_TossCoin
MUTATIONS["Serial_TossCoin"] = {"source_symbol": "Serial_TossCoin", "before": "SerialTossCoinATimesResult Serial_TossCoin(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = 1u;", "after": "SerialTossCoinATimesResult Serial_TossCoin(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = 0u;", "case_ids": ["Serial_TossCoin-0", "Serial_TossCoin-1", "Serial_TossCoin-2"]}
# <<< factory-mutation Serial_TossCoin
# >>> factory-mutation NinetalesLure_SwitchEffect
MUTATIONS["NinetalesLure_SwitchEffect"] = {"source_symbol": "NinetalesLure_SwitchEffect", "before": "NinetalesLure_SwitchEffect(void)\n{\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\tHandleNShieldAndTransparencyResult shield = HandleNShieldAndTransparency((uint16_t)e);\n\tif (!(shield.f & 0x10u))\n\t\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\twDuelDisplayedScreen = 0u;", "after": "NinetalesLure_SwitchEffect(void)\n{\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\tHandleNShieldAndTransparencyResult shield = HandleNShieldAndTransparency((uint16_t)e);\n\tif (!(shield.f & 0x10u))\n\t\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\twDuelDisplayedScreen = 1u;", "case_ids": ["NinetalesLure_SwitchEffect-0", "NinetalesLure_SwitchEffect-1"]}
# <<< factory-mutation NinetalesLure_SwitchEffect
# >>> factory-mutation VictreebelLure_SwitchDefendingPokemon
MUTATIONS["VictreebelLure_SwitchDefendingPokemon"] = {"source_symbol": "VictreebelLure_SwitchDefendingPokemon", "before": "void VictreebelLure_SwitchDefendingPokemon(void)\n{\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\tHandleNShieldAndTransparencyResult shield = HandleNShieldAndTransparency((uint16_t)e);\n\tif (!(shield.f & 0x10u))\n\t\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\twDuelDisplayedScreen = 0u;\n}", "after": "void VictreebelLure_SwitchDefendingPokemon(void)\n{\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\tHandleNShieldAndTransparencyResult shield = HandleNShieldAndTransparency((uint16_t)e);\n\tif (!(shield.f & 0x10u))\n\t\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\twDuelDisplayedScreen = 1u;\n}", "case_ids": ["VictreebelLure_SwitchDefendingPokemon-0", "VictreebelLure_SwitchDefendingPokemon-1", "VictreebelLure_SwitchDefendingPokemon-2"]}
# <<< factory-mutation VictreebelLure_SwitchDefendingPokemon
# >>> factory-mutation DancingEmbers_MultiplierEffect
MUTATIONS["DancingEmbers_MultiplierEffect"] = {"source_symbol": "DancingEmbers_MultiplierEffect", "before": "void DancingEmbers_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);", "after": "void DancingEmbers_MultiplierEffect(void)\n{\n\tLoadTxRam3(11u);", "case_ids": ["DancingEmbers_MultiplierEffect-0", "DancingEmbers_MultiplierEffect-1"]}
# <<< factory-mutation DancingEmbers_MultiplierEffect
# >>> factory-mutation NidoranFFurySwipes_MultiplierEffect
MUTATIONS["NidoranFFurySwipes_MultiplierEffect"] = {"source_symbol": "NidoranFFurySwipes_MultiplierEffect", "before": "void NidoranFFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);", "after": "void NidoranFFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(11u);", "case_ids": ["NidoranFFurySwipes_MultiplierEffect-0", "NidoranFFurySwipes_MultiplierEffect-1"]}
# <<< factory-mutation NidoranFFurySwipes_MultiplierEffect
# >>> factory-mutation PsyduckFurySwipes_MultiplierEffect
MUTATIONS["PsyduckFurySwipes_MultiplierEffect"] = {"source_symbol": "PsyduckFurySwipes_MultiplierEffect", "before": "void PsyduckFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tSetDefiniteDamage(ATimes10(result.a));", "after": "void PsyduckFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tSetDefiniteDamage(0u);", "case_ids": ["PsyduckFurySwipes_MultiplierEffect-0", "PsyduckFurySwipes_MultiplierEffect-1"]}
# <<< factory-mutation PsyduckFurySwipes_MultiplierEffect
# >>> factory-mutation JolteonDoubleKick_MultiplierEffect
MUTATIONS["JolteonDoubleKick_MultiplierEffect"] = {"source_symbol": "JolteonDoubleKick_MultiplierEffect", "before": "void JolteonDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 10u);", "after": "void JolteonDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 10u);", "case_ids": ["JolteonDoubleKick_MultiplierEffect-0", "JolteonDoubleKick_MultiplierEffect-1"]}
# <<< factory-mutation JolteonDoubleKick_MultiplierEffect
# >>> factory-mutation CometPunch_MultiplierEffect
MUTATIONS["CometPunch_MultiplierEffect"] = {"source_symbol": "CometPunch_MultiplierEffect", "before": "void CometPunch_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(4u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 20u);", "after": "void CometPunch_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(5u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 20u);", "case_ids": ["CometPunch_MultiplierEffect-0"]}
# <<< factory-mutation CometPunch_MultiplierEffect
# >>> factory-mutation PinMissile_MultiplierEffect
MUTATIONS["PinMissile_MultiplierEffect"] = {"source_symbol": "PinMissile_MultiplierEffect", "before": "void PinMissile_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(4u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = ATimes10((uint8_t)(result.a + result.a));\n\tSetDefiniteDamage(damage);\n}", "after": "void PinMissile_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(4u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = ATimes10((uint8_t)(result.a + result.a + 1u));\n\tSetDefiniteDamage(damage);\n}", "case_ids": ["PinMissile_MultiplierEffect-0", "PinMissile_MultiplierEffect-1"]}
# <<< factory-mutation PinMissile_MultiplierEffect
# >>> factory-mutation PrimeapeFurySwipes_MultiplierEffect
MUTATIONS["PrimeapeFurySwipes_MultiplierEffect"] = {"source_symbol": "PrimeapeFurySwipes_MultiplierEffect", "before": "void PrimeapeFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "after": "void PrimeapeFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(4u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "case_ids": ["PrimeapeFurySwipes_MultiplierEffect-0", "PrimeapeFurySwipes_MultiplierEffect-1"]}
# <<< factory-mutation PrimeapeFurySwipes_MultiplierEffect
# >>> factory-mutation SandslashFurySwipes_MultiplierEffect
MUTATIONS["SandslashFurySwipes_MultiplierEffect"] = {"source_symbol": "SandslashFurySwipes_MultiplierEffect", "before": "void SandslashFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "after": "void SandslashFurySwipes_MultiplierEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(4u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "case_ids": ["SandslashFurySwipes_MultiplierEffect-0", "SandslashFurySwipes_MultiplierEffect-1"]}
# <<< factory-mutation SandslashFurySwipes_MultiplierEffect
# >>> factory-mutation DragoniteLv45Slam_MultiplierEffect
MUTATIONS["DragoniteLv45Slam_MultiplierEffect"] = {"source_symbol": "DragoniteLv45Slam_MultiplierEffect", "before": "void DragoniteLv45Slam_MultiplierEffect(void)\n{\n\tLoadTxRam3(40u);", "after": "void DragoniteLv45Slam_MultiplierEffect(void)\n{\n\tLoadTxRam3(41u);", "case_ids": ["DragoniteLv45Slam_MultiplierEffect-0", "DragoniteLv45Slam_MultiplierEffect-1"]}
# <<< factory-mutation DragoniteLv45Slam_MultiplierEffect
# >>> factory-mutation FuryAttack_MultiplierEffect
MUTATIONS["FuryAttack_MultiplierEffect"] = {"source_symbol": "FuryAttack_MultiplierEffect", "before": "void FuryAttack_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "after": "void FuryAttack_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "case_ids": ["FuryAttack_MultiplierEffect-0", "FuryAttack_MultiplierEffect-1"]}
# <<< factory-mutation FuryAttack_MultiplierEffect
# >>> factory-mutation Bonemerang_MultiplierEffect
MUTATIONS["Bonemerang_MultiplierEffect"] = {"source_symbol": "Bonemerang_MultiplierEffect", "before": "void Bonemerang_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 0u);", "after": "void Bonemerang_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(1u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 0u);", "case_ids": ["Bonemerang_MultiplierEffect-0", "Bonemerang_MultiplierEffect-1"]}
# <<< factory-mutation Bonemerang_MultiplierEffect
# >>> factory-mutation CloysterSpikeCannon_MultiplierEffect
MUTATIONS["CloysterSpikeCannon_MultiplierEffect"] = {"source_symbol": "CloysterSpikeCannon_MultiplierEffect", "before": "void CloysterSpikeCannon_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = result.a;\n\tdamage = (uint8_t)(damage + damage);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10(damage));\n}", "after": "void CloysterSpikeCannon_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = result.a;\n\tdamage = (uint8_t)(damage + damage);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10((uint8_t)(damage + 1u)));\n}", "case_ids": ["CloysterSpikeCannon_MultiplierEffect-0", "CloysterSpikeCannon_MultiplierEffect-1"]}
# <<< factory-mutation CloysterSpikeCannon_MultiplierEffect
# >>> factory-mutation NidorinaDoubleKick_MultiplierEffect
MUTATIONS["NidorinaDoubleKick_MultiplierEffect"] = {"source_symbol": "NidorinaDoubleKick_MultiplierEffect", "before": "void NidorinaDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);", "after": "void NidorinaDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(31u);", "case_ids": ["NidorinaDoubleKick_MultiplierEffect-0", "NidorinaDoubleKick_MultiplierEffect-1"]}
# <<< factory-mutation NidorinaDoubleKick_MultiplierEffect
# >>> factory-mutation DragoniteLv41Slam_MultiplierEffect
MUTATIONS["DragoniteLv41Slam_MultiplierEffect"] = {"source_symbol": "DragoniteLv41Slam_MultiplierEffect", "before": "void DragoniteLv41Slam_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "after": "void DragoniteLv41Slam_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(3u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);", "case_ids": ["DragoniteLv41Slam_MultiplierEffect-0", "DragoniteLv41Slam_MultiplierEffect-1"]}
# <<< factory-mutation DragoniteLv41Slam_MultiplierEffect
# >>> factory-mutation NidorinoDoubleKick_MultiplierEffect
MUTATIONS["NidorinoDoubleKick_MultiplierEffect"] = {"source_symbol": "NidorinoDoubleKick_MultiplierEffect", "before": "void NidorinoDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);", "after": "void NidorinoDoubleKick_MultiplierEffect(void)\n{\n\tLoadTxRam3(31u);", "case_ids": ["NidorinoDoubleKick_MultiplierEffect-0", "NidorinoDoubleKick_MultiplierEffect-1"]}
# <<< factory-mutation NidorinoDoubleKick_MultiplierEffect
# >>> factory-mutation OmastarSpikeCannon_MultiplierEffect
MUTATIONS["OmastarSpikeCannon_MultiplierEffect"] = {"source_symbol": "OmastarSpikeCannon_MultiplierEffect", "before": "void OmastarSpikeCannon_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = result.a;\n\tdamage = (uint8_t)(damage + damage);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10(damage));\n}", "after": "void OmastarSpikeCannon_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(1u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = result.a;\n\tdamage = (uint8_t)(damage + damage);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10(damage));\n}", "case_ids": ["OmastarSpikeCannon_MultiplierEffect-0", "OmastarSpikeCannon_MultiplierEffect-1"]}
# <<< factory-mutation OmastarSpikeCannon_MultiplierEffect
# >>> factory-mutation JynxDoubleslap_MultiplierEffect
MUTATIONS["JynxDoubleslap_MultiplierEffect"] = {"source_symbol": "JynxDoubleslap_MultiplierEffect", "before": "void JynxDoubleslap_MultiplierEffect(void)\n{\n\tLoadTxRam3(10u);", "after": "void JynxDoubleslap_MultiplierEffect(void)\n{\n\tLoadTxRam3(11u);", "case_ids": ["JynxDoubleslap_MultiplierEffect-0", "JynxDoubleslap_MultiplierEffect-1"]}
# <<< factory-mutation JynxDoubleslap_MultiplierEffect
# >>> factory-mutation PoliwhirlDoubleslap_MultiplierEffect
MUTATIONS["PoliwhirlDoubleslap_MultiplierEffect"] = {"source_symbol": "PoliwhirlDoubleslap_MultiplierEffect", "before": "void PoliwhirlDoubleslap_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);", "after": "void PoliwhirlDoubleslap_MultiplierEffect(void)\n{\n\tLoadTxRam3(31u);", "case_ids": ["PoliwhirlDoubleslap_MultiplierEffect-0", "PoliwhirlDoubleslap_MultiplierEffect-1"]}
# <<< factory-mutation PoliwhirlDoubleslap_MultiplierEffect
# >>> factory-mutation Twineedle_MultiplierEffect
MUTATIONS["Twineedle_MultiplierEffect"] = {"source_symbol": "Twineedle_MultiplierEffect", "before": "void Twineedle_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);", "after": "void Twineedle_MultiplierEffect(void)\n{\n\tLoadTxRam3(31u);", "case_ids": ["Twineedle_MultiplierEffect-0", "Twineedle_MultiplierEffect-1"]}
# <<< factory-mutation Twineedle_MultiplierEffect
# >>> factory-mutation DragonairSlam_MultiplierEffect
MUTATIONS["DragonairSlam_MultiplierEffect"] = {"source_symbol": "DragonairSlam_MultiplierEffect", "before": "void DragonairSlam_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = (uint8_t)(result.a + result.a);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10(damage));", "after": "void DragonairSlam_MultiplierEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoinATimes_BankBResult result = TossCoinATimes_BankB(2u, 0u, 0u, 0u, 0x00u, DamageCheckIfHeadsXDamageText, 0u);\n\tuint8_t damage = (uint8_t)(result.a + result.a);\n\tdamage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10((uint8_t)(damage + 1u)));", "case_ids": ["DragonairSlam_MultiplierEffect-0", "DragonairSlam_MultiplierEffect-1"]}
# <<< factory-mutation DragonairSlam_MultiplierEffect
# >>> factory-mutation PetalDance_MultiplierEffect
MUTATIONS["PetalDance_MultiplierEffect"] = {"source_symbol": "PetalDance_MultiplierEffect", "before": "void PetalDance_MultiplierEffect(void)\n{\n\tLoadTxRam3(40u);", "after": "void PetalDance_MultiplierEffect(void)\n{\n\tLoadTxRam3(0x40u);", "case_ids": ["PetalDance_MultiplierEffect-0", "PetalDance_MultiplierEffect-1"]}
# <<< factory-mutation PetalDance_MultiplierEffect
# >>> factory-mutation PlayTrainerEffectAnimation
MUTATIONS["PlayTrainerEffectAnimation"] = {"source_symbol": "PlayTrainerEffectAnimation", "before": "\tPlayAttackAnimation(hWhoseTurn, f, 0u, 0u, d, e, (uint16_t)(((uint16_t)hWhoseTurn << 8) | (hl & 0xffu)));", "after": "\tPlayAttackAnimation(hWhoseTurn, f, 1u, 0u, d, e, (uint16_t)(((uint16_t)hWhoseTurn << 8) | (hl & 0xffu)));", "case_ids": ["PlayTrainerEffectAnimation-0"]}
# <<< factory-mutation PlayTrainerEffectAnimation
# >>> factory-mutation StretchKick_BenchDamageEffect
MUTATIONS["StretchKick_BenchDamageEffect"] = {"source_symbol": "StretchKick_BenchDamageEffect", "before": "StretchKick_BenchDamageEffectResult StretchKick_BenchDamageEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = hTemp_ffa0;", "after": "StretchKick_BenchDamageEffectResult StretchKick_BenchDamageEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["StretchKick_BenchDamageEffect-0", "StretchKick_BenchDamageEffect-1"]}
# <<< factory-mutation StretchKick_BenchDamageEffect
# >>> factory-mutation IceBreath_RandomPokemonDamageEffect
MUTATIONS["IceBreath_RandomPokemonDamageEffect"] = {"source_symbol": "IceBreath_RandomPokemonDamageEffect", "before": "void IceBreath_RandomPokemonDamageEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = random.a;", "after": "void IceBreath_RandomPokemonDamageEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = (uint8_t)(random.a + 1u);", "case_ids": ["IceBreath_RandomPokemonDamageEffect-0", "IceBreath_RandomPokemonDamageEffect-1"]}
# <<< factory-mutation IceBreath_RandomPokemonDamageEffect
# >>> factory-mutation HypnoDarkMind_DamageBenchEffect
MUTATIONS["HypnoDarkMind_DamageBenchEffect"] = {"source_symbol": "HypnoDarkMind_DamageBenchEffect", "before": "HypnoDarkMind_DamageBenchEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = hTemp_ffa0;", "after": "HypnoDarkMind_DamageBenchEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["HypnoDarkMind_DamageBenchEffect-1", "HypnoDarkMind_DamageBenchEffect-2"]}
# <<< factory-mutation HypnoDarkMind_DamageBenchEffect
# >>> factory-mutation GengarDarkMind_DamageBenchEffect
MUTATIONS["GengarDarkMind_DamageBenchEffect"] = {"source_symbol": "GengarDarkMind_DamageBenchEffect", "before": "GengarDarkMind_DamageBenchEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = hTemp_ffa0;", "after": "GengarDarkMind_DamageBenchEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["GengarDarkMind_DamageBenchEffect-1", "GengarDarkMind_DamageBenchEffect-2"]}
# <<< factory-mutation GengarDarkMind_DamageBenchEffect
# >>> factory-mutation Spark_BenchDamageEffect
MUTATIONS["Spark_BenchDamageEffect"] = {"source_symbol": "Spark_BenchDamageEffect", "before": "Spark_BenchDamageEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = hTemp_ffa0;", "after": "Spark_BenchDamageEffect(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t target = (uint8_t)(hTemp_ffa0 + 1u);", "case_ids": ["Spark_BenchDamageEffect-1", "Spark_BenchDamageEffect-2"]}
# <<< factory-mutation Spark_BenchDamageEffect
# >>> factory-mutation CatPunchEffect
MUTATIONS["CatPunchEffect"] = {"source_symbol": "CatPunchEffect", "before": "void CatPunchEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = random.a;\n\twLoadedAttackAnimation = ATK_ANIM_CAT_PUNCH_PLAY_AREA;", "after": "void CatPunchEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = random.a;\n\twLoadedAttackAnimation = (uint8_t)(ATK_ANIM_CAT_PUNCH_PLAY_AREA ^ 1u);", "case_ids": ["CatPunchEffect-0", "CatPunchEffect-1"]}
# <<< factory-mutation CatPunchEffect
# >>> factory-mutation Gigashock_BenchDamageEffect
MUTATIONS["Gigashock_BenchDamageEffect"] = {"source_symbol": "Gigashock_BenchDamageEffect", "before": "void Gigashock_BenchDamageEffect(void)\n{\n\tSwapTurn();\n\tuint16_t hl = hTempList_ADDR;\n\tfor (;;) {\n\t\tuint8_t target = gb_read8(hl++);", "after": "void Gigashock_BenchDamageEffect(void)\n{\n\tSwapTurn();\n\tuint16_t hl = hTempList_ADDR;\n\tfor (;;) {\n\t\tuint8_t target = (uint8_t)(gb_read8(hl++) + 1u);", "case_ids": ["Gigashock_BenchDamageEffect-1", "Gigashock_BenchDamageEffect-2"]}
# <<< factory-mutation Gigashock_BenchDamageEffect
# >>> factory-mutation ChainLightningEffect
MUTATIONS["ChainLightningEffect"] = {"source_symbol": "ChainLightningEffect", "before": "\twIsDamageToSelf = TRUE;", "after": "\twIsDamageToSelf = 0u;", "case_ids": ["ChainLightningEffect-1", "ChainLightningEffect-2", "ChainLightningEffect-3"]}
# <<< factory-mutation ChainLightningEffect
# >>> factory-mutation Firegiver_AddToHandEffect
MUTATIONS["Firegiver_AddToHandEffect"] = {"source_symbol": "Firegiver_AddToHandEffect", "before": "\tgb_write8(list, FG_LIST_TERMINATOR);", "after": "\tgb_write8(list, 0x00u);", "case_ids": ["Firegiver_AddToHandEffect-0", "Firegiver_AddToHandEffect-1"]}
# <<< factory-mutation Firegiver_AddToHandEffect
# >>> factory-mutation PlayAttackAnimationOverAttackingPokemon
MUTATIONS["PlayAttackAnimationOverAttackingPokemon"] = {"source_symbol": "PlayAttackAnimationOverAttackingPokemon", "before": "void PlayAttackAnimationOverAttackingPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\twLoadedAttackAnimation = a;", "after": "void PlayAttackAnimationOverAttackingPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\twLoadedAttackAnimation = (uint8_t)(a + 1u);", "case_ids": ["PlayAttackAnimationOverAttackingPokemon-0", "PlayAttackAnimationOverAttackingPokemon-1"]}
# <<< factory-mutation PlayAttackAnimationOverAttackingPokemon
# >>> factory-mutation PokemonTrader_PlayerHandSelection
MUTATIONS["PokemonTrader_PlayerHandSelection"] = {"source_symbol": "PokemonTrader_PlayerHandSelection", "before": "\thTemp_ffa0 = result.a;", "after": "\thTemp_ffa0 = (uint8_t)(result.a + 1u);", "case_ids": ["PokemonTrader_PlayerHandSelection-0", "PokemonTrader_PlayerHandSelection-1"]}
# <<< factory-mutation PokemonTrader_PlayerHandSelection
# >>> factory-mutation EnergyRetrieval_PlayerDiscardPileSelection
MUTATIONS["EnergyRetrieval_PlayerDiscardPileSelection"] = {"source_symbol": "EnergyRetrieval_PlayerDiscardPileSelection", "before": "EnergyRetrieval_PlayerDiscardPileSelectionResult EnergyRetrieval_PlayerDiscardPileSelection(void)\n{\n\thCurSelectionItem = 1u;", "after": "EnergyRetrieval_PlayerDiscardPileSelectionResult EnergyRetrieval_PlayerDiscardPileSelection(void)\n{\n\thCurSelectionItem = 2u;", "case_ids": ["EnergyRetrieval_PlayerDiscardPileSelection-0", "EnergyRetrieval_PlayerDiscardPileSelection-1"]}
# <<< factory-mutation EnergyRetrieval_PlayerDiscardPileSelection
# >>> factory-mutation EnergyRetrieval_PlayerHandSelection
MUTATIONS["EnergyRetrieval_PlayerHandSelection"] = {"source_symbol": "EnergyRetrieval_PlayerHandSelection", "before": "\thTempList = hTempCardIndex_ff98;", "after": "\thTempList = (uint8_t)(hTempCardIndex_ff98 + 1u);", "case_ids": ["EnergyRetrieval_PlayerHandSelection-0"]}
# <<< factory-mutation EnergyRetrieval_PlayerHandSelection
# >>> factory-mutation HandleEnergyCardsInDiscardPileSelection
MUTATIONS["HandleEnergyCardsInDiscardPileSelection"] = {"source_symbol": "HandleEnergyCardsInDiscardPileSelection", "before": "HandleEnergyCardsInDiscardPileSelectionResult HandleEnergyCardsInDiscardPileSelection(uint16_t hl)\n{\n\thCurSelectionItem = 0u;", "after": "HandleEnergyCardsInDiscardPileSelectionResult HandleEnergyCardsInDiscardPileSelection(uint16_t hl)\n{\n\thCurSelectionItem = 1u;", "case_ids": ["HandleEnergyCardsInDiscardPileSelection-0", "HandleEnergyCardsInDiscardPileSelection-1"]}
# <<< factory-mutation HandleEnergyCardsInDiscardPileSelection
# >>> factory-mutation EnergyConversion_PlayerSelectEffect
MUTATIONS["EnergyConversion_PlayerSelectEffect"] = {"source_symbol": "EnergyConversion_PlayerSelectEffect", "before": "HandleEnergyCardsInDiscardPileSelectionResult EnergyConversion_PlayerSelectEffect(void)\n{\n\treturn HandleEnergyCardsInDiscardPileSelection(Choose2EnergyCardsFromDiscardPileForHandText);\n}", "after": "HandleEnergyCardsInDiscardPileSelectionResult EnergyConversion_PlayerSelectEffect(void)\n{\n\tHandleEnergyCardsInDiscardPileSelectionResult result = HandleEnergyCardsInDiscardPileSelection(Choose2EnergyCardsFromDiscardPileForHandText);\n\tresult.a = (uint8_t)(result.a + 1u);\n\treturn result;\n}", "case_ids": ["EnergyConversion_PlayerSelectEffect-0", "EnergyConversion_PlayerSelectEffect-1"]}
# <<< factory-mutation EnergyConversion_PlayerSelectEffect
# >>> factory-mutation MewtwoAltEnergyAbsorption_PlayerSelectEffect
MUTATIONS["MewtwoAltEnergyAbsorption_PlayerSelectEffect"] = {"source_symbol": "MewtwoAltEnergyAbsorption_PlayerSelectEffect", "before": "\treturn (MewtwoAltEnergyAbsorption_PlayerSelectEffectResult){result.a, result.f, result.hl};", "after": "\treturn (MewtwoAltEnergyAbsorption_PlayerSelectEffectResult){0xffu, result.f, result.hl};", "case_ids": ["MewtwoAltEnergyAbsorption_PlayerSelectEffect-0", "MewtwoAltEnergyAbsorption_PlayerSelectEffect-1"]}
# <<< factory-mutation MewtwoAltEnergyAbsorption_PlayerSelectEffect
# >>> factory-mutation MewtwoEnergyAbsorption_PlayerSelectEffect
MUTATIONS["MewtwoEnergyAbsorption_PlayerSelectEffect"] = {"source_symbol": "MewtwoEnergyAbsorption_PlayerSelectEffect", "before": "\treturn (MewtwoEnergyAbsorption_PlayerSelectEffectResult){result.a, result.f, result.hl};", "after": "\treturn (MewtwoEnergyAbsorption_PlayerSelectEffectResult){0xffu, result.f, result.hl};", "case_ids": ["MewtwoEnergyAbsorption_PlayerSelectEffect-0", "MewtwoEnergyAbsorption_PlayerSelectEffect-1"]}
# <<< factory-mutation MewtwoEnergyAbsorption_PlayerSelectEffect
# >>> factory-mutation FetchEffect
MUTATIONS["FetchEffect"] = {"source_symbol": "FetchEffect", "before": "void FetchEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(Draw1CardFromTheDeckText);\n\tDisplayDrawOneCardScreen(0u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tDrawCardResult draw = DrawCardFromDeck();\n\tif ((draw.f & 0x10u) != 0u)\n\t\treturn;\n\tAddCardToHand(draw.a);", "after": "void FetchEffect(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(Draw1CardFromTheDeckText);\n\tDisplayDrawOneCardScreen(0u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tDrawCardResult draw = DrawCardFromDeck();\n\tif ((draw.f & 0x10u) != 0u)\n\t\treturn;\n\tAddCardToHand((uint8_t)(draw.a + 1u));", "case_ids": ["FetchEffect-0", "FetchEffect-1", "FetchEffect-2"]}
# <<< factory-mutation FetchEffect
# >>> factory-mutation ProfessorOakEffect
MUTATIONS["ProfessorOakEffect"] = {"source_symbol": "ProfessorOakEffect", "before": "\tuint8_t draw_count = 7u;", "after": "\tuint8_t draw_count = 6u;", "case_ids": ["ProfessorOakEffect-0", "ProfessorOakEffect-1"]}
# <<< factory-mutation ProfessorOakEffect
# >>> factory-mutation Maintenance_ReturnToDeckAndDrawEffect
MUTATIONS["Maintenance_ReturnToDeckAndDrawEffect"] = {"source_symbol": "Maintenance_ReturnToDeckAndDrawEffect", "before": "MaintenanceReturnToDeckAndDrawEffectResult Maintenance_ReturnToDeckAndDrawEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t first = hTempList;", "after": "MaintenanceReturnToDeckAndDrawEffectResult Maintenance_ReturnToDeckAndDrawEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t first = (uint8_t)(hTempList + 1u);", "case_ids": ["Maintenance_ReturnToDeckAndDrawEffect-0", "Maintenance_ReturnToDeckAndDrawEffect-1"]}
# <<< factory-mutation Maintenance_ReturnToDeckAndDrawEffect
# >>> factory-mutation ThunderJolt_RecoilEffect
MUTATIONS["ThunderJolt_RecoilEffect"] = {"source_symbol": "ThunderJolt_RecoilEffect", "before": "ThunderJolt_RecoilEffectResult ThunderJolt_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(10u);", "after": "ThunderJolt_RecoilEffectResult ThunderJolt_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(11u);", "case_ids": ["ThunderJolt_RecoilEffect-0", "ThunderJolt_RecoilEffect-1"]}
# <<< factory-mutation ThunderJolt_RecoilEffect
# >>> factory-mutation ZapdosThunder_RecoilEffect
MUTATIONS["ZapdosThunder_RecoilEffect"] = {"source_symbol": "ZapdosThunder_RecoilEffect", "before": "ZapdosThunder_RecoilEffectResult ZapdosThunder_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(30u);", "after": "ZapdosThunder_RecoilEffectResult ZapdosThunder_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(31u);", "case_ids": ["ZapdosThunder_RecoilEffect-0", "ZapdosThunder_RecoilEffect-1"]}
# <<< factory-mutation ZapdosThunder_RecoilEffect
# >>> factory-mutation BillEffect
MUTATIONS["BillEffect"] = {"source_symbol": "BillEffect", "before": "void BillEffect(void)\n{\n\tDisplayDrawNCardsScreen(2u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tuint8_t remaining = 2u;", "after": "void BillEffect(void)\n{\n\tDisplayDrawNCardsScreen(2u, 0u, 0u, 0u, 0u, 0u, 0u);\n\tuint8_t remaining = 1u;", "case_ids": ["BillEffect-0", "BillEffect-1", "BillEffect-2"]}
# <<< factory-mutation BillEffect
# >>> factory-mutation ImposterProfessorOakEffect
MUTATIONS["ImposterProfessorOakEffect"] = {"source_symbol": "ImposterProfessorOakEffect", "before": "\tuint8_t draw_count = 7u;", "after": "\tuint8_t draw_count = 6u;", "case_ids": ["ImposterProfessorOakEffect-0", "ImposterProfessorOakEffect-1"]}
# <<< factory-mutation ImposterProfessorOakEffect
# >>> factory-mutation HandlePlayerSelection2HandCards
MUTATIONS["HandlePlayerSelection2HandCards"] = {"source_symbol": "HandlePlayerSelection2HandCards", "before": "HandlePlayerSelection2HandCardsResult HandlePlayerSelection2HandCards(uint16_t de, uint16_t hl)\n{\n\t(void)DrawWideTextBox_WaitForInput(hl);\n\t(void)CreateHandCardList(0u);\n\tuint8_t trainer = hTempCardIndex_ff9f;\n\t(void)RemoveCardFromDuelTempList(trainer);", "after": "HandlePlayerSelection2HandCardsResult HandlePlayerSelection2HandCards(uint16_t de, uint16_t hl)\n{\n\treturn (HandlePlayerSelection2HandCardsResult){0u, 0u};", "case_ids": ["HandlePlayerSelection2HandCards-0", "HandlePlayerSelection2HandCards-1"]}
# <<< factory-mutation HandlePlayerSelection2HandCards
# >>> factory-mutation HandlePlayerSelection2HandCardsToDiscard
MUTATIONS["HandlePlayerSelection2HandCardsToDiscard"] = {"source_symbol": "HandlePlayerSelection2HandCardsToDiscard", "before": "HandlePlayerSelection2HandCardsResult HandlePlayerSelection2HandCardsToDiscard(void)\n{\n\treturn HandlePlayerSelection2HandCards(ChooseTheCardToDiscardText, Choose2CardsFromHandToDiscardText);\n}", "after": "HandlePlayerSelection2HandCardsResult HandlePlayerSelection2HandCardsToDiscard(void)\n{\n\treturn (HandlePlayerSelection2HandCardsResult){0u, 0u};\n}", "case_ids": ["HandlePlayerSelection2HandCardsToDiscard-0", "HandlePlayerSelection2HandCardsToDiscard-1"]}
# <<< factory-mutation HandlePlayerSelection2HandCardsToDiscard
# >>> factory-mutation SuperEnergyRetrieval_PlayerHandSelection
MUTATIONS["SuperEnergyRetrieval_PlayerHandSelection"] = {"source_symbol": "SuperEnergyRetrieval_PlayerHandSelection", "before": "HandlePlayerSelection2HandCardsResult SuperEnergyRetrieval_PlayerHandSelection(void)\n{\n\treturn HandlePlayerSelection2HandCardsToDiscard();\n}", "after": "HandlePlayerSelection2HandCardsResult SuperEnergyRetrieval_PlayerHandSelection(void)\n{\n\treturn (HandlePlayerSelection2HandCardsResult){0u, 0u};\n}", "case_ids": ["SuperEnergyRetrieval_PlayerHandSelection-0", "SuperEnergyRetrieval_PlayerHandSelection-1"]}
# <<< factory-mutation SuperEnergyRetrieval_PlayerHandSelection
# >>> factory-mutation Maintenance_PlayerSelection
MUTATIONS["Maintenance_PlayerSelection"] = {"source_symbol": "Maintenance_PlayerSelection", "before": "HandlePlayerSelection2HandCardsResult Maintenance_PlayerSelection(void)\n{\n\treturn HandlePlayerSelection2HandCards(ChooseTheCardToPutBackText, Choose2HandCardsFromHandToReturnToDeckText);", "after": "HandlePlayerSelection2HandCardsResult Maintenance_PlayerSelection(void)\n{\n\treturn (HandlePlayerSelection2HandCardsResult){0u, 0u};", "case_ids": ["Maintenance_PlayerSelection-0", "Maintenance_PlayerSelection-1"]}
# <<< factory-mutation Maintenance_PlayerSelection
# >>> factory-mutation ItemFinder_PlayerSelection
MUTATIONS["ItemFinder_PlayerSelection"] = {"source_symbol": "ItemFinder_PlayerSelection", "before": "ItemFinderPlayerSelectionResult ItemFinder_PlayerSelection(void)\n{\n\tHandlePlayerSelection2HandCardsResult hand = HandlePlayerSelection2HandCardsToDiscard();\n\tif ((hand.f & 0x10u) != 0u)\n\t\treturn (ItemFinderPlayerSelectionResult){hand.a, hand.f};\n\t(void)CreateTrainerCardListFromDiscardPile();\n\t(void)InitAndDrawCardListScreenLayout_WithSelectCheckMenu();\n\tSetCardListHeaderText(PlayerDiscardPileText, ChooseCardToPlaceInHandText);\n\tDisplayCardListResult display = DisplayCardList();\n\tgb_write8(hTempList_ADDR + 2u, display.a);\n\treturn (ItemFinderPlayerSelectionResult){display.a, display.f};\n}", "after": "ItemFinderPlayerSelectionResult ItemFinder_PlayerSelection(void)\n{\n\treturn (ItemFinderPlayerSelectionResult){0u, 0u};\n}", "case_ids": ["ItemFinder_PlayerSelection-0", "ItemFinder_PlayerSelection-1"]}
# <<< factory-mutation ItemFinder_PlayerSelection
# >>> factory-mutation SlicingWindEffect
MUTATIONS["SlicingWindEffect"] = {"source_symbol": "SlicingWindEffect", "before": "SlicingWindEffectResult SlicingWindEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = random.a;", "after": "SlicingWindEffectResult SlicingWindEffect(void)\n{\n\tSwapTurn();\n\tPickRandomPlayAreaCardResult random = PickRandomPlayAreaCard();\n\tuint8_t target = (uint8_t)(random.a + 1u);", "case_ids": ["SlicingWindEffect-0"]}
# <<< factory-mutation SlicingWindEffect
# >>> factory-mutation SuperEnergyRetrieval_PlayerDiscardPileSelection
MUTATIONS["SuperEnergyRetrieval_PlayerDiscardPileSelection"] = {"source_symbol": "SuperEnergyRetrieval_PlayerDiscardPileSelection", "before": "\tgb_write8(terminator, 0xffu);", "after": "\tgb_write8(terminator, 0u);", "case_ids": ["SuperEnergyRetrieval_PlayerDiscardPileSelection-0"]}
# <<< factory-mutation SuperEnergyRetrieval_PlayerDiscardPileSelection
# >>> factory-mutation ComputerSearch_PlayerDiscardHandSelection
MUTATIONS["ComputerSearch_PlayerDiscardHandSelection"] = {"source_symbol": "ComputerSearch_PlayerDiscardHandSelection", "before": "HandlePlayerSelection2HandCardsResult ComputerSearch_PlayerDiscardHandSelection(void)\n{\n\treturn HandlePlayerSelection2HandCardsToDiscard();\n}", "after": "HandlePlayerSelection2HandCardsResult ComputerSearch_PlayerDiscardHandSelection(void)\n{\n\treturn (HandlePlayerSelection2HandCardsResult){0u, 0u};\n}", "case_ids": ["ComputerSearch_PlayerDiscardHandSelection-0", "ComputerSearch_PlayerDiscardHandSelection-1"]}
# <<< factory-mutation ComputerSearch_PlayerDiscardHandSelection
# >>> factory-mutation Pokedex_PlayerSelection
MUTATIONS["Pokedex_PlayerSelection"] = {"source_symbol": "Pokedex_PlayerSelection", "before": "\t\t\t\tgb_write8((uint16_t)(hTempList_ADDR + written), 0xFFu);\n\t\t\t\treturn (PokedexPlayerSelectionResult){number,", "after": "\t\t\t\tgb_write8((uint16_t)(hTempList_ADDR + written), 0x00u);\n\t\t\t\treturn (PokedexPlayerSelectionResult){number,", "case_ids": ["Pokedex_PlayerSelection-0", "Pokedex_PlayerSelection-1"]}
# <<< factory-mutation Pokedex_PlayerSelection
# >>> factory-mutation Thrash_RecoilEffect
MUTATIONS["Thrash_RecoilEffect"] = {"source_symbol": "Thrash_RecoilEffect", "before": "Thrash_RecoilEffectResult Thrash_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tuint8_t coin = hTemp_ffa0;\n\tif (coin != 0u)\n\t\treturn (Thrash_RecoilEffectResult){coin, 0x00u};", "after": "Thrash_RecoilEffectResult Thrash_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tuint8_t coin = hTemp_ffa0;\n\tif (coin != 0u)\n\t\treturn (Thrash_RecoilEffectResult){(uint8_t)(coin + 1u), 0x00u};", "case_ids": ["Thrash_RecoilEffect-0", "Thrash_RecoilEffect-1"]}
# <<< factory-mutation Thrash_RecoilEffect
# >>> factory-mutation RaichuThunder_RecoilEffect
MUTATIONS["RaichuThunder_RecoilEffect"] = {"source_symbol": "RaichuThunder_RecoilEffect", "before": "RaichuThunder_RecoilEffectResult RaichuThunder_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(30u);", "after": "RaichuThunder_RecoilEffectResult RaichuThunder_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tLoadTxRam3(31u);", "case_ids": ["RaichuThunder_RecoilEffect-0", "RaichuThunder_RecoilEffect-1"]}
# <<< factory-mutation RaichuThunder_RecoilEffect
# >>> factory-mutation BigEggsplosion_MultiplierEffect
MUTATIONS["BigEggsplosion_MultiplierEffect"] = {"source_symbol": "BigEggsplosion_MultiplierEffect", "before": "void BigEggsplosion_MultiplierEffect(void)\n{\n\tGetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);\n\tLoadTxRam3(20u);", "after": "void BigEggsplosion_MultiplierEffect(void)\n{\n\tGetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);\n\tLoadTxRam3(21u);", "case_ids": ["BigEggsplosion_MultiplierEffect-0", "BigEggsplosion_MultiplierEffect-1"]}
# <<< factory-mutation BigEggsplosion_MultiplierEffect
# >>> factory-mutation PokemonFlute_PlayerSelection
MUTATIONS["PokemonFlute_PlayerSelection"] = {"source_symbol": "PokemonFlute_PlayerSelection", "before": "void PokemonFlute_PlayerSelection(void)\n{\n\tSwapTurn();\n\t(void)CreateBasicPokemonCardListFromDiscardPile();\n\t(void)InitAndDrawCardListScreenLayout_WithSelectCheckMenu();\n\tSetCardListHeaderText(PlayerDiscardPileText, ChoosePokemonToPlaceInPlayText);\n\t(void)DisplayCardList();\n\tSwapTurn();\n\thTemp_ffa0 = hTempCardIndex_ff98;", "after": "void PokemonFlute_PlayerSelection(void)\n{\n\tSwapTurn();\n\t(void)CreateBasicPokemonCardListFromDiscardPile();\n\t(void)InitAndDrawCardListScreenLayout_WithSelectCheckMenu();\n\tSetCardListHeaderText(PlayerDiscardPileText, ChoosePokemonToPlaceInPlayText);\n\t(void)DisplayCardList();\n\tSwapTurn();\n\thTemp_ffa0 = 0u;", "case_ids": ["PokemonFlute_PlayerSelection-0", "PokemonFlute_PlayerSelection-1", "PokemonFlute_PlayerSelection-2"]}
# <<< factory-mutation PokemonFlute_PlayerSelection
# >>> factory-mutation DevolutionBeam_DevolveEffect
MUTATIONS["DevolutionBeam_DevolveEffect"] = {"source_symbol": "DevolutionBeam_DevolveEffect", "before": "void DevolutionBeam_DevolveEffect(void)\n{\n\tuint8_t target = hTemp_ffa0;\n\tif (target == 0xffu) {\n\t\treturn;\n\t}", "after": "void DevolutionBeam_DevolveEffect(void)\n{\n\tuint8_t target = hTemp_ffa0;\n\tif (target == 0xffu) {\n\t\twDuelDisplayedScreen = 1u;\n\t\treturn;\n\t}", "case_ids": ["DevolutionBeam_DevolveEffect-0", "DevolutionBeam_DevolveEffect-1"]}
# <<< factory-mutation DevolutionBeam_DevolveEffect
# >>> factory-mutation MarowakCallForFamily_PlayerSelectEffect
MUTATIONS["MarowakCallForFamily_PlayerSelectEffect"] = {"source_symbol": "MarowakCallForFamily_PlayerSelectEffect", "before": "MarowakCallForFamily_PlayerSelectEffectResult MarowakCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "MarowakCallForFamily_PlayerSelectEffectResult MarowakCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["MarowakCallForFamily_PlayerSelectEffect-0", "MarowakCallForFamily_PlayerSelectEffect-1"]}
# <<< factory-mutation MarowakCallForFamily_PlayerSelectEffect
# >>> factory-mutation DealDamageToAllBenchedPokemon
MUTATIONS["DealDamageToAllBenchedPokemon"] = {"source_symbol": "DealDamageToAllBenchedPokemon", "before": "DealDamageToAllBenchedPokemonResult DealDamageToAllBenchedPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t animation = a;\n\tDuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tuint8_t count_value = count.a;\n\ta = count_value;", "after": "DealDamageToAllBenchedPokemonResult DealDamageToAllBenchedPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t animation = a;\n\tDuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);\n\tuint8_t count_value = count.a;\n\ta = 0u;", "case_ids": ["DealDamageToAllBenchedPokemon-0", "DealDamageToAllBenchedPokemon-1"]}
# <<< factory-mutation DealDamageToAllBenchedPokemon
# >>> factory-mutation HandleProphecyScreen
MUTATIONS["HandleProphecyScreen"] = {"source_symbol": "HandleProphecyScreen", "before": "\t\t\tgb_write8((uint16_t)(hTempList_ADDR + 1u + written), 0xffu);", "after": "\t\t\tgb_write8((uint16_t)(hTempList_ADDR + written), 0xffu);", "case_ids": ["HandleProphecyScreen-0", "HandleProphecyScreen-1"]}
# <<< factory-mutation HandleProphecyScreen
# >>> factory-mutation EarthquakeEffect
MUTATIONS["EarthquakeEffect"] = {"source_symbol": "EarthquakeEffect", "before": "DealDamageToAllBenchedPokemonResult EarthquakeEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\twIsDamageToSelf = TRUE;", "after": "DealDamageToAllBenchedPokemonResult EarthquakeEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\twIsDamageToSelf = 0u;", "case_ids": ["EarthquakeEffect-0", "EarthquakeEffect-1"]}
# <<< factory-mutation EarthquakeEffect
# >>> factory-mutation Blizzard_BenchDamageEffect
MUTATIONS["Blizzard_BenchDamageEffect"] = {"source_symbol": "Blizzard_BenchDamageEffect", "before": "if (hTemp_ffa0 == 0u) {\n\t\twIsDamageToSelf = TRUE;", "after": "if (hTemp_ffa0 == 0u) {\n\t\twIsDamageToSelf = 0x00u;", "case_ids": ["Blizzard_BenchDamageEffect-0", "Blizzard_BenchDamageEffect-2"]}
# <<< factory-mutation Blizzard_BenchDamageEffect
# >>> factory-mutation Thunderpunch_RecoilEffect
MUTATIONS["Thunderpunch_RecoilEffect"] = {"source_symbol": "Thunderpunch_RecoilEffect", "before": "Thunderpunch_RecoilEffectResult Thunderpunch_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tuint8_t coin = hTemp_ffa0;\n\tif (coin != 0u)\n\t\treturn (Thunderpunch_RecoilEffectResult){coin, 0x00u};", "after": "Thunderpunch_RecoilEffectResult Thunderpunch_RecoilEffect(uint8_t f, uint8_t d, uint8_t e)\n{\n\tuint8_t coin = hTemp_ffa0;\n\tif (coin != 0u)\n\t\treturn (Thunderpunch_RecoilEffectResult){(uint8_t)(coin + 1u), 0x00u};", "case_ids": ["Thunderpunch_RecoilEffect-0", "Thunderpunch_RecoilEffect-1"]}
# <<< factory-mutation Thunderpunch_RecoilEffect
# >>> factory-mutation Revive_PlayerSelection
MUTATIONS["Revive_PlayerSelection"] = {"source_symbol": "Revive_PlayerSelection", "before": "void Revive_PlayerSelection(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseBasicPokemonToPlaceOnBenchText);\n\t(void)CreateBasicPokemonCardListFromDiscardPile();\n\t(void)InitAndDrawCardListScreenLayout_WithSelectCheckMenu();\n\tSetCardListHeaderText(PlayerDiscardPileText, PleaseSelectCardText);\n\t(void)DisplayCardList();\n\thTemp_ffa0 = hTempCardIndex_ff98;", "after": "void Revive_PlayerSelection(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ChooseBasicPokemonToPlaceOnBenchText);\n\t(void)CreateBasicPokemonCardListFromDiscardPile();\n\t(void)InitAndDrawCardListScreenLayout_WithSelectCheckMenu();\n\tSetCardListHeaderText(PlayerDiscardPileText, PleaseSelectCardText);\n\t(void)DisplayCardList();\n\thTemp_ffa0 = 0u;", "case_ids": ["Revive_PlayerSelection-0", "Revive_PlayerSelection-1"]}
# <<< factory-mutation Revive_PlayerSelection
# >>> factory-mutation BellsproutCallForFamily_PlayerSelectEffect
MUTATIONS["BellsproutCallForFamily_PlayerSelectEffect"] = {"source_symbol": "BellsproutCallForFamily_PlayerSelectEffect", "before": "BellsproutCallForFamily_PlayerSelectEffectResult BellsproutCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "BellsproutCallForFamily_PlayerSelectEffectResult BellsproutCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["BellsproutCallForFamily_PlayerSelectEffect-0", "BellsproutCallForFamily_PlayerSelectEffect-1"]}
# <<< factory-mutation BellsproutCallForFamily_PlayerSelectEffect
# >>> factory-mutation EnergySearch_PlayerSelection
MUTATIONS["EnergySearch_PlayerSelection"] = {"source_symbol": "EnergySearch_PlayerSelection", "before": "EnergySearch_PlayerSelectionResult EnergySearch_PlayerSelection(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "EnergySearch_PlayerSelectionResult EnergySearch_PlayerSelection(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["EnergySearch_PlayerSelection-0", "EnergySearch_PlayerSelection-1"]}
# <<< factory-mutation EnergySearch_PlayerSelection
# >>> factory-mutation KrabbyCallForFamily_PlayerSelectEffect
MUTATIONS["KrabbyCallForFamily_PlayerSelectEffect"] = {"source_symbol": "KrabbyCallForFamily_PlayerSelectEffect", "before": "KrabbyCallForFamily_PlayerSelectEffectResult KrabbyCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "KrabbyCallForFamily_PlayerSelectEffectResult KrabbyCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["KrabbyCallForFamily_PlayerSelectEffect-0", "KrabbyCallForFamily_PlayerSelectEffect-1"]}
# <<< factory-mutation KrabbyCallForFamily_PlayerSelectEffect
# >>> factory-mutation NidoranFCallForFamily_PlayerSelectEffect
MUTATIONS["NidoranFCallForFamily_PlayerSelectEffect"] = {"source_symbol": "NidoranFCallForFamily_PlayerSelectEffect", "before": "NidoranFCallForFamily_PlayerSelectEffectResult NidoranFCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "NidoranFCallForFamily_PlayerSelectEffectResult NidoranFCallForFamily_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["NidoranFCallForFamily_PlayerSelectEffect-0", "NidoranFCallForFamily_PlayerSelectEffect-1"]}
# <<< factory-mutation NidoranFCallForFamily_PlayerSelectEffect
# >>> factory-mutation TossCoin_BankB
MUTATIONS["TossCoin_BankB"] = {"source_symbol": "TossCoin_BankB", "before": "TossCoin_BankBResult TossCoin_BankB(uint16_t de, uint16_t hl)\n{\n\tTossCoinRoutineResult result = TossCoin(de, hl);\n\treturn (TossCoin_BankBResult){result.a, result.f, result.hl};", "after": "TossCoin_BankBResult TossCoin_BankB(uint16_t de, uint16_t hl)\n{\n\tTossCoinRoutineResult result = TossCoin(de, hl);\n\treturn (TossCoin_BankBResult){(uint8_t)(result.a + 1u), result.f, result.hl};", "case_ids": ["TossCoin_BankB-0", "TossCoin_BankB-1", "TossCoin_BankB-2"]}
# <<< factory-mutation TossCoin_BankB
# >>> factory-mutation GustOfWind_SwitchEffect
MUTATIONS["GustOfWind_SwitchEffect"] = {"source_symbol": "GustOfWind_SwitchEffect", "before": "void GustOfWind_SwitchEffect(void)\n{\n\tPlayTrainerEffectAnimation(ATK_ANIM_GUST_OF_WIND, 0u, 0u, 0u, 0u, 0u, 0u);\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\tClearDamageReductionSubstatus2();\n\twDuelDisplayedScreen = 0u;", "after": "void GustOfWind_SwitchEffect(void)\n{\n\tPlayTrainerEffectAnimation(ATK_ANIM_GUST_OF_WIND, 0u, 0u, 0u, 0u, 0u, 0u);\n\tSwapTurn();\n\tuint8_t e = hTemp_ffa0;\n\t(void)SwapArenaWithBenchPokemon(e);\n\tSwapTurn();\n\tClearDamageReductionSubstatus2();\n\twDuelDisplayedScreen = 1u;", "case_ids": ["GustOfWind_SwitchEffect-0", "GustOfWind_SwitchEffect-1", "GustOfWind_SwitchEffect-2"]}
# <<< factory-mutation GustOfWind_SwitchEffect
# >>> factory-mutation Confusion50PercentEffect
MUTATIONS["Confusion50PercentEffect"] = {"source_symbol": "Confusion50PercentEffect", "before": "uint8_t Confusion50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(ConfusionCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn ConfusionEffect().f;", "after": "uint8_t Confusion50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(ConfusionCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn (uint8_t)(ConfusionEffect().f ^ 0x10u);", "case_ids": ["Confusion50PercentEffect-0", "Confusion50PercentEffect-1"]}
# <<< factory-mutation Confusion50PercentEffect
# >>> factory-mutation Poison50PercentEffect
MUTATIONS["Poison50PercentEffect"] = {"source_symbol": "Poison50PercentEffect", "before": "uint8_t Poison50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn PoisonEffect().f;", "after": "uint8_t Poison50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn (uint8_t)(PoisonEffect().f ^ 0x10u);", "case_ids": ["Poison50PercentEffect-0", "Poison50PercentEffect-1"]}
# <<< factory-mutation Poison50PercentEffect
# >>> factory-mutation ApplyAndAnimateHPRecovery
MUTATIONS["ApplyAndAnimateHPRecovery"] = {"source_symbol": "ApplyAndAnimateHPRecovery", "before": "void ApplyAndAnimateHPRecovery(uint8_t d, uint8_t e)\n{\n\twUnused_HPRecoverAmount = e;", "after": "void ApplyAndAnimateHPRecovery(uint8_t d, uint8_t e)\n{\n\twUnused_HPRecoverAmount = d;", "case_ids": ["ApplyAndAnimateHPRecovery-0", "ApplyAndAnimateHPRecovery-1", "ApplyAndAnimateHPRecovery-2", "ApplyAndAnimateHPRecovery-3"]}
# <<< factory-mutation ApplyAndAnimateHPRecovery
# >>> factory-mutation Paralysis50PercentEffect
MUTATIONS["Paralysis50PercentEffect"] = {"source_symbol": "Paralysis50PercentEffect", "before": "uint8_t Paralysis50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(ParalysisCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn ParalysisEffect().f;", "after": "uint8_t Paralysis50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(ParalysisCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn (uint8_t)(ParalysisEffect().f ^ 0x10u);", "case_ids": ["Paralysis50PercentEffect-0", "Paralysis50PercentEffect-1"]}
# <<< factory-mutation Paralysis50PercentEffect
# >>> factory-mutation PlayerPickAttackForAmnesia
MUTATIONS["PlayerPickAttackForAmnesia"] = {"source_symbol": "PlayerPickAttackForAmnesia", "before": "\tuint8_t attack_index = gb_read8((uint16_t)(wDuelTempList_ADDR + selected + 1u));", "after": "\tuint8_t attack_index = (uint8_t)(gb_read8((uint16_t)(wDuelTempList_ADDR + selected + 1u)) ^ 0xFFu);", "case_ids": ["PlayerPickAttackForAmnesia-0", "PlayerPickAttackForAmnesia-1"]}
# <<< factory-mutation PlayerPickAttackForAmnesia

# >>> factory-mutation ZubatSupersonicEffect
MUTATIONS["ZubatSupersonicEffect"] = {"source_symbol": "ZubatSupersonicEffect", "before": "uint8_t ZubatSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();", "after": "uint8_t ZubatSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) != 0u)\n\t\tSetNoEffectFromStatus();", "case_ids": ["ZubatSupersonicEffect-0", "ZubatSupersonicEffect-1"]}
# <<< factory-mutation ZubatSupersonicEffect
# >>> factory-mutation ShellderSupersonicEffect
MUTATIONS["ShellderSupersonicEffect"] = {"source_symbol": "ShellderSupersonicEffect", "before": "uint8_t ShellderSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();", "after": "uint8_t ShellderSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) != 0u)\n\t\tSetNoEffectFromStatus();", "case_ids": ["ShellderSupersonicEffect-0", "ShellderSupersonicEffect-1"]}
# <<< factory-mutation ShellderSupersonicEffect
# >>> factory-mutation TentacruelSupersonicEffect
MUTATIONS["TentacruelSupersonicEffect"] = {"source_symbol": "TentacruelSupersonicEffect", "before": "uint8_t TentacruelSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();", "after": "uint8_t TentacruelSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) != 0u)\n\t\tSetNoEffectFromStatus();", "case_ids": ["TentacruelSupersonicEffect-0", "TentacruelSupersonicEffect-1"]}
# <<< factory-mutation TentacruelSupersonicEffect

# >>> factory-mutation FirstAid_HealEffect
MUTATIONS["FirstAid_HealEffect"] = {"source_symbol": "FirstAid_HealEffect", "before": "void FirstAid_HealEffect(void)\n{\n\tApplyAndAnimateHPRecovery(0u, 10u);", "after": "void FirstAid_HealEffect(void)\n{\n\tApplyAndAnimateHPRecovery(0u, 20u);", "case_ids": ["FirstAid_HealEffect-0", "FirstAid_HealEffect-1", "FirstAid_HealEffect-2", "FirstAid_HealEffect-3"]}
# <<< factory-mutation FirstAid_HealEffect
# >>> factory-mutation GolbatLeechLifeEffect
MUTATIONS["GolbatLeechLifeEffect"] = {"source_symbol": "GolbatLeechLifeEffect", "before": "void GolbatLeechLifeEffect(void)\n{\n\tuint8_t e = gb_read8(wDealtDamage_ADDR);", "after": "void GolbatLeechLifeEffect(void)\n{\n\tuint8_t e = (uint8_t)(gb_read8(wDealtDamage_ADDR) + 1u);", "case_ids": ["GolbatLeechLifeEffect-0", "GolbatLeechLifeEffect-1", "GolbatLeechLifeEffect-2"]}
# <<< factory-mutation GolbatLeechLifeEffect
# >>> factory-mutation VenonatLeechLifeEffect
MUTATIONS["VenonatLeechLifeEffect"] = {"source_symbol": "VenonatLeechLifeEffect", "before": "void VenonatLeechLifeEffect(void)\n{\n\tuint8_t e = gb_read8(wDealtDamage_ADDR);", "after": "void VenonatLeechLifeEffect(void)\n{\n\tuint8_t e = (uint8_t)(gb_read8(wDealtDamage_ADDR) + 1u);", "case_ids": ["VenonatLeechLifeEffect-0", "VenonatLeechLifeEffect-1", "VenonatLeechLifeEffect-2"]}
# <<< factory-mutation VenonatLeechLifeEffect
# >>> factory-mutation ZubatLeechLifeEffect
MUTATIONS["ZubatLeechLifeEffect"] = {"source_symbol": "ZubatLeechLifeEffect", "before": "void ZubatLeechLifeEffect(void)\n{\n\tuint8_t e = gb_read8(wDealtDamage_ADDR);", "after": "void ZubatLeechLifeEffect(void)\n{\n\tuint8_t e = (uint8_t)(gb_read8(wDealtDamage_ADDR) + 1u);", "case_ids": ["ZubatLeechLifeEffect-0", "ZubatLeechLifeEffect-1", "ZubatLeechLifeEffect-2"]}
# <<< factory-mutation ZubatLeechLifeEffect
# >>> factory-mutation ExeggcuteLeechSeedEffect
MUTATIONS["ExeggcuteLeechSeedEffect"] = {"source_symbol": "ExeggcuteLeechSeedEffect", "before": "void ExeggcuteLeechSeedEffect(void)\n{\n\tuint8_t a = gb_read8(wDealtDamage_ADDR);\n\tif (a == 0u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 10u);", "after": "void ExeggcuteLeechSeedEffect(void)\n{\n\tuint8_t a = gb_read8(wDealtDamage_ADDR);\n\tif (a == 0u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 20u);", "case_ids": ["ExeggcuteLeechSeedEffect-0", "ExeggcuteLeechSeedEffect-2"]}
# <<< factory-mutation ExeggcuteLeechSeedEffect
# >>> factory-mutation BulbasaurLeechSeedEffect
MUTATIONS["BulbasaurLeechSeedEffect"] = {"source_symbol": "BulbasaurLeechSeedEffect", "before": "void BulbasaurLeechSeedEffect(void)\n{\n\tuint8_t a = gb_read8(wDealtDamage_ADDR);\n\tuint8_t h = gb_read8((uint16_t)(wDealtDamage_ADDR + 1u));\n\tif ((a | h) == 0u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 10u);", "after": "void BulbasaurLeechSeedEffect(void)\n{\n\tuint8_t a = gb_read8(wDealtDamage_ADDR);\n\tuint8_t h = gb_read8((uint16_t)(wDealtDamage_ADDR + 1u));\n\tif ((a | h) == 0u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 20u);", "case_ids": ["BulbasaurLeechSeedEffect-0", "BulbasaurLeechSeedEffect-2"]}
# <<< factory-mutation BulbasaurLeechSeedEffect
# >>> factory-mutation PoliwhirlAmnesia_PlayerSelectEffect
MUTATIONS["PoliwhirlAmnesia_PlayerSelectEffect"] = {"source_symbol": "PoliwhirlAmnesia_PlayerSelectEffect", "before": "PlayerPickAttackForAmnesiaResult PoliwhirlAmnesia_PlayerSelectEffect(void)\n{\n\treturn PlayerPickAttackForAmnesia();", "after": "PlayerPickAttackForAmnesiaResult PoliwhirlAmnesia_PlayerSelectEffect(void)\n{\n\treturn (PlayerPickAttackForAmnesiaResult){0u, 0u};", "case_ids": ["PoliwhirlAmnesia_PlayerSelectEffect-0", "PoliwhirlAmnesia_PlayerSelectEffect-1"]}
# <<< factory-mutation PoliwhirlAmnesia_PlayerSelectEffect
# >>> factory-mutation SlowpokeAmnesia_PlayerSelectEffect
MUTATIONS["SlowpokeAmnesia_PlayerSelectEffect"] = {"source_symbol": "SlowpokeAmnesia_PlayerSelectEffect", "before": "PlayerPickAttackForAmnesiaResult SlowpokeAmnesia_PlayerSelectEffect(void)\n{\n\treturn PlayerPickAttackForAmnesia();", "after": "PlayerPickAttackForAmnesiaResult SlowpokeAmnesia_PlayerSelectEffect(void)\n{\n\treturn (PlayerPickAttackForAmnesiaResult){0u, 0u};", "case_ids": ["SlowpokeAmnesia_PlayerSelectEffect-0", "SlowpokeAmnesia_PlayerSelectEffect-1"]}
# <<< factory-mutation SlowpokeAmnesia_PlayerSelectEffect
# >>> factory-mutation LickitungSupersonicEffect
MUTATIONS["LickitungSupersonicEffect"] = {"source_symbol": "LickitungSupersonicEffect", "before": "uint8_t LickitungSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();\n\treturn f;\n}", "after": "uint8_t LickitungSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();\n\treturn (uint8_t)(f ^ 0x01u);\n}", "case_ids": ["LickitungSupersonicEffect-0", "LickitungSupersonicEffect-1"]}
# <<< factory-mutation LickitungSupersonicEffect
# >>> factory-mutation NidorinaSupersonicEffect
MUTATIONS["NidorinaSupersonicEffect"] = {"source_symbol": "NidorinaSupersonicEffect", "before": "uint8_t NidorinaSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();", "after": "uint8_t NidorinaSupersonicEffect(void)\n{\n\tuint8_t f = Confusion50PercentEffect();\n\tif ((f & 0x10u) != 0u)\n\t\tSetNoEffectFromStatus();", "case_ids": ["NidorinaSupersonicEffect-0", "NidorinaSupersonicEffect-1"]}
# <<< factory-mutation NidorinaSupersonicEffect
# >>> factory-mutation Sleep50PercentEffect
MUTATIONS["Sleep50PercentEffect"] = {"source_symbol": "Sleep50PercentEffect", "before": "uint8_t Sleep50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SleepCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn SleepEffect().f;", "after": "uint8_t Sleep50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SleepCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;\n\treturn (uint8_t)(SleepEffect().f ^ 0x10u);", "case_ids": ["Sleep50PercentEffect-0", "Sleep50PercentEffect-1"]}
# <<< factory-mutation Sleep50PercentEffect
# >>> factory-mutation KadabraRecover_HealEffect
MUTATIONS["KadabraRecover_HealEffect"] = {"source_symbol": "KadabraRecover_HealEffect", "before": "void KadabraRecover_HealEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tApplyAndAnimateHPRecovery(0u, damage.a);", "after": "void KadabraRecover_HealEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tApplyAndAnimateHPRecovery(0u, 0u);", "case_ids": ["KadabraRecover_HealEffect-0", "KadabraRecover_HealEffect-1", "KadabraRecover_HealEffect-2", "KadabraRecover_HealEffect-3"]}
# <<< factory-mutation KadabraRecover_HealEffect
# >>> factory-mutation StarmieRecover_HealEffect
MUTATIONS["StarmieRecover_HealEffect"] = {"source_symbol": "StarmieRecover_HealEffect", "before": "void StarmieRecover_HealEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tApplyAndAnimateHPRecovery(0u, damage.a);", "after": "void StarmieRecover_HealEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tApplyAndAnimateHPRecovery(0u, (uint8_t)(damage.a + 1u));", "case_ids": ["StarmieRecover_HealEffect-0", "StarmieRecover_HealEffect-1", "StarmieRecover_HealEffect-2", "StarmieRecover_HealEffect-3"]}
# <<< factory-mutation StarmieRecover_HealEffect
# >>> factory-mutation SingEffect
MUTATIONS["SingEffect"] = {"source_symbol": "SingEffect", "before": "uint8_t SingEffect(void)\n{\n\tuint8_t f = Sleep50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();\n\treturn f;\n}", "after": "uint8_t SingEffect(void)\n{\n\tuint8_t f = Sleep50PercentEffect();\n\tif ((f & 0x10u) != 0u)\n\t\tSetNoEffectFromStatus();\n\treturn f;\n}", "case_ids": ["SingEffect-0", "SingEffect-1"]}
# <<< factory-mutation SingEffect
# >>> factory-mutation SleepingGasEffect
MUTATIONS["SleepingGasEffect"] = {"source_symbol": "SleepingGasEffect", "before": "uint8_t SleepingGasEffect(void)\n{\n\tuint8_t f = Sleep50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();\n\treturn f;\n}", "after": "uint8_t SleepingGasEffect(void)\n{\n\tuint8_t f = Sleep50PercentEffect();\n\tif ((f & 0x10u) == 0u)\n\t\tSetNoEffectFromStatus();\n\treturn (uint8_t)(f ^ 0x01u);\n}", "case_ids": ["SleepingGasEffect-0", "SleepingGasEffect-1"]}
# <<< factory-mutation SleepingGasEffect

# >>> factory-mutation AbsorbEffect
MUTATIONS["AbsorbEffect"] = {"source_symbol": "AbsorbEffect", "before": "\tdealt = (uint16_t)(dealt >> 1);", "after": "\tdealt = (uint16_t)(dealt >> 2);", "case_ids": ["AbsorbEffect-0", "AbsorbEffect-1", "AbsorbEffect-3"]}
# <<< factory-mutation AbsorbEffect
# >>> factory-mutation ButterfreeMegaDrainEffect
MUTATIONS["ButterfreeMegaDrainEffect"] = {"source_symbol": "ButterfreeMegaDrainEffect", "before": "\tdealt = (uint16_t)(dealt >> 1);", "after": "\tdealt = (uint16_t)(dealt >> 2);", "case_ids": ["ButterfreeMegaDrainEffect-0", "ButterfreeMegaDrainEffect-1", "ButterfreeMegaDrainEffect-3"]}
# <<< factory-mutation ButterfreeMegaDrainEffect
# >>> factory-mutation AcidEffect
MUTATIONS["AcidEffect"] = {"source_symbol": "AcidEffect", "before": "\tuint16_t written = ApplySubstatus2ToDefendingCard(SUBSTATUS2_ACID, hl);", "after": "\tuint16_t written = ApplySubstatus2ToDefendingCard(0x0cu, hl);", "case_ids": ["AcidEffect-0", "AcidEffect-2"]}
# <<< factory-mutation AcidEffect
# >>> factory-mutation BoneAttackEffect
MUTATIONS["BoneAttackEffect"] = {"source_symbol": "BoneAttackEffect", "before": "\tuint16_t written = ApplySubstatus2ToDefendingCard(SUBSTATUS2_BONE_ATTACK, hl);", "after": "\tuint16_t written = ApplySubstatus2ToDefendingCard(0x0cu, hl);", "case_ids": ["BoneAttackEffect-0", "BoneAttackEffect-2"]}
# <<< factory-mutation BoneAttackEffect
# >>> factory-mutation ArcanineQuickAttack_DamageBoostEffect
MUTATIONS["ArcanineQuickAttack_DamageBoostEffect"] = {"source_symbol": "ArcanineQuickAttack_DamageBoostEffect", "before": "\tAddToDamage(20u);", "after": "\tAddToDamage(21u);", "case_ids": ["ArcanineQuickAttack_DamageBoostEffect-0"]}
# <<< factory-mutation ArcanineQuickAttack_DamageBoostEffect

# >>> factory-mutation EeveeQuickAttack_DamageBoostEffect
MUTATIONS["EeveeQuickAttack_DamageBoostEffect"] = {"source_symbol": "EeveeQuickAttack_DamageBoostEffect", "before": "void EeveeQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(20u);", "after": "void EeveeQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(21u);", "case_ids": ["EeveeQuickAttack_DamageBoostEffect-0"]}
# <<< factory-mutation EeveeQuickAttack_DamageBoostEffect
# >>> factory-mutation ElectabuzzQuickAttack_DamageBoostEffect
MUTATIONS["ElectabuzzQuickAttack_DamageBoostEffect"] = {"source_symbol": "ElectabuzzQuickAttack_DamageBoostEffect", "before": "void ElectabuzzQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(20u);", "after": "void ElectabuzzQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(21u);", "case_ids": ["ElectabuzzQuickAttack_DamageBoostEffect-0"]}
# <<< factory-mutation ElectabuzzQuickAttack_DamageBoostEffect
# >>> factory-mutation FlareonQuickAttack_DamageBoostEffect
MUTATIONS["FlareonQuickAttack_DamageBoostEffect"] = {"source_symbol": "FlareonQuickAttack_DamageBoostEffect", "before": "void FlareonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(20u);", "after": "void FlareonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(21u);", "case_ids": ["FlareonQuickAttack_DamageBoostEffect-0"]}
# <<< factory-mutation FlareonQuickAttack_DamageBoostEffect
# >>> factory-mutation JolteonQuickAttack_DamageBoostEffect
MUTATIONS["JolteonQuickAttack_DamageBoostEffect"] = {"source_symbol": "JolteonQuickAttack_DamageBoostEffect", "before": "void JolteonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(20u);", "after": "void JolteonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(21u);", "case_ids": ["JolteonQuickAttack_DamageBoostEffect-0"]}
# <<< factory-mutation JolteonQuickAttack_DamageBoostEffect
# >>> factory-mutation FearowAgilityEffect
MUTATIONS["FearowAgilityEffect"] = {"source_symbol": "FearowAgilityEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_AGILITY_PROTECT;", "after": "\twLoadedAttackAnimation = 0x53u;", "case_ids": ["FearowAgilityEffect-0", "FearowAgilityEffect-2"]}
# <<< factory-mutation FearowAgilityEffect
# >>> factory-mutation ClampEffect
MUTATIONS["ClampEffect"] = {"source_symbol": "ClampEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_NONE;\n\tSetDefiniteDamage(0u);", "after": "\twLoadedAttackAnimation = ATK_ANIM_NONE;\n\tSetDefiniteDamage(1u);", "case_ids": ["ClampEffect-1"]}
# <<< factory-mutation ClampEffect

# >>> factory-mutation HideInShellEffect
MUTATIONS["HideInShellEffect"] = {"source_symbol": "HideInShellEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_PROTECT;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_HIDE_IN_SHELL);", "after": "\twLoadedAttackAnimation = 0x50u;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_HIDE_IN_SHELL);", "case_ids": ["HideInShellEffect-0"]}
# <<< factory-mutation HideInShellEffect
# >>> factory-mutation KakunaStiffenEffect
MUTATIONS["KakunaStiffenEffect"] = {"source_symbol": "KakunaStiffenEffect", "before": "uint8_t KakunaStiffenEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsNoDamageNextTurnText, 0u);\n\tif ((toss.f & 0x10u) == 0u) {\n\t\tSetWasUnsuccessful();\n\t\treturn toss.f;\n\t}\n\twLoadedAttackAnimation = ATK_ANIM_PROTECT;", "after": "uint8_t KakunaStiffenEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsNoDamageNextTurnText, 0u);\n\tif ((toss.f & 0x10u) == 0u) {\n\t\tSetWasUnsuccessful();\n\t\treturn toss.f;\n\t}\n\twLoadedAttackAnimation = 0x50u;", "case_ids": ["KakunaStiffenEffect-0"]}
# <<< factory-mutation KakunaStiffenEffect
# >>> factory-mutation MetapodStiffenEffect
MUTATIONS["MetapodStiffenEffect"] = {"source_symbol": "MetapodStiffenEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_PROTECT;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_STIFFEN);\n\treturn toss.f;\n}\n/* <<< factory MetapodStiffenEffect */", "after": "\twLoadedAttackAnimation = 0x50u;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_STIFFEN);\n\treturn toss.f;\n}\n/* <<< factory MetapodStiffenEffect */", "case_ids": ["MetapodStiffenEffect-0"]}
# <<< factory-mutation MetapodStiffenEffect
# >>> factory-mutation LeerEffect
MUTATIONS["LeerEffect"] = {"source_symbol": "LeerEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_LEER;\n\tApplySubstatus2ToDefendingCard(SUBSTATUS2_LEER, hl);", "after": "\twLoadedAttackAnimation = 0x75u;\n\tApplySubstatus2ToDefendingCard(SUBSTATUS2_LEER, hl);", "case_ids": ["LeerEffect-0"]}
# <<< factory-mutation LeerEffect
# >>> factory-mutation Thunderpunch_ModifierEffect
MUTATIONS["Thunderpunch_ModifierEffect"] = {"source_symbol": "Thunderpunch_ModifierEffect", "before": "void Thunderpunch_ModifierEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadPlus10IfTails10ToYourselfText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(10u);", "after": "void Thunderpunch_ModifierEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadPlus10IfTails10ToYourselfText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(11u);", "case_ids": ["Thunderpunch_ModifierEffect-0", "Thunderpunch_ModifierEffect-1"]}
# <<< factory-mutation Thunderpunch_ModifierEffect

# >>> factory-mutation Fly_Success50PercentEffect
MUTATIONS["Fly_Success50PercentEffect"] = {"source_symbol": "Fly_Success50PercentEffect", "before": "\t}\n\twLoadedAttackAnimation = ATK_ANIM_AGILITY_PROTECT;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_FLY);\n\treturn toss.f;\n}\n/* <<< factory Fly_Success50PercentEffect */", "after": "\t}\n\twLoadedAttackAnimation = 0x53u;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_FLY);\n\treturn toss.f;\n}\n/* <<< factory Fly_Success50PercentEffect */", "case_ids": ["Fly_Success50PercentEffect-0"]}
# <<< factory-mutation Fly_Success50PercentEffect
# >>> factory-mutation MoltresLv35DiveBomb_Success50PercentEffect
MUTATIONS["MoltresLv35DiveBomb_Success50PercentEffect"] = {"source_symbol": "MoltresLv35DiveBomb_Success50PercentEffect", "before": "uint8_t MoltresLv35DiveBomb_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = ATK_ANIM_DIVE_BOMB;", "after": "uint8_t MoltresLv35DiveBomb_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = 0x12u;", "case_ids": ["MoltresLv35DiveBomb_Success50PercentEffect-0"]}
# <<< factory-mutation MoltresLv35DiveBomb_Success50PercentEffect
# >>> factory-mutation MoltresLv37DiveBomb_Success50PercentEffect
MUTATIONS["MoltresLv37DiveBomb_Success50PercentEffect"] = {"source_symbol": "MoltresLv37DiveBomb_Success50PercentEffect", "before": "uint8_t MoltresLv37DiveBomb_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = ATK_ANIM_DIVE_BOMB;", "after": "uint8_t MoltresLv37DiveBomb_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = 0x12u;", "case_ids": ["MoltresLv37DiveBomb_Success50PercentEffect-0"]}
# <<< factory-mutation MoltresLv37DiveBomb_Success50PercentEffect
# >>> factory-mutation HornHazard_NoDamage50PercentEffect
MUTATIONS["HornHazard_NoDamage50PercentEffect"] = {"source_symbol": "HornHazard_NoDamage50PercentEffect", "before": "uint8_t HornHazard_NoDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfTailsNoDamageText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = ATK_ANIM_HIT;", "after": "uint8_t HornHazard_NoDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfTailsNoDamageText, 0u);\n\tif ((toss.f & 0x10u) != 0u) {\n\t\twLoadedAttackAnimation = 0x00u;", "case_ids": ["HornHazard_NoDamage50PercentEffect-0"]}
# <<< factory-mutation HornHazard_NoDamage50PercentEffect
# >>> factory-mutation SeadraAgilityEffect
MUTATIONS["SeadraAgilityEffect"] = {
    "source_symbol": "SeadraAgilityEffect",
    "before": "uint16_t SeadraAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.hl;\n\twLoadedAttackAnimation = ATK_ANIM_AGILITY_PROTECT;",
    "after": "uint16_t SeadraAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.hl;\n\twLoadedAttackAnimation = (uint8_t)(ATK_ANIM_AGILITY_PROTECT ^ 1u);",
    "case_ids": ["SeadraAgilityEffect-0", "SeadraAgilityEffect-2"]
}
# <<< factory-mutation SeadraAgilityEffect
# >>> factory-mutation RaichuAgilityEffect
MUTATIONS["RaichuAgilityEffect"] = {"source_symbol": "RaichuAgilityEffect", "before": "uint16_t RaichuAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn 0u;\n\twLoadedAttackAnimation = ATK_ANIM_AGILITY_PROTECT;", "after": "uint16_t RaichuAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn 0u;\n\twLoadedAttackAnimation = 0x53u;", "case_ids": ["RaichuAgilityEffect-0", "RaichuAgilityEffect-2"]}
# <<< factory-mutation RaichuAgilityEffect
# >>> factory-mutation RapidashAgilityEffect
MUTATIONS["RapidashAgilityEffect"] = {"source_symbol": "RapidashAgilityEffect", "before": "uint16_t RapidashAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn 0u;\n\twLoadedAttackAnimation = ATK_ANIM_AGILITY_PROTECT;", "after": "uint16_t RapidashAgilityEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsDoNotReceiveDamageOrEffectText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn 0u;\n\twLoadedAttackAnimation = 0x53u;", "case_ids": ["RapidashAgilityEffect-0", "RapidashAgilityEffect-1", "RapidashAgilityEffect-2"]}
# <<< factory-mutation RapidashAgilityEffect

# >>> factory-mutation RapidashStomp_DamageBoostEffect
MUTATIONS["RapidashStomp_DamageBoostEffect"] = {"source_symbol": "RapidashStomp_DamageBoostEffect", "before": "void RapidashStomp_DamageBoostEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(10u);", "after": "void RapidashStomp_DamageBoostEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(11u);", "case_ids": ["RapidashStomp_DamageBoostEffect-0"]}
# <<< factory-mutation RapidashStomp_DamageBoostEffect
# >>> factory-mutation ScrunchEffect
MUTATIONS["ScrunchEffect"] = {"source_symbol": "ScrunchEffect", "before": "uint8_t ScrunchEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsNoDamageNextTurnText, 0u);\n\tif ((toss.f & 0x10u) == 0u) {\n\t\tSetWasUnsuccessful();\n\t\treturn toss.f;\n\t}\n\twLoadedAttackAnimation = ATK_ANIM_SCRUNCH;", "after": "uint8_t ScrunchEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadsNoDamageNextTurnText, 0u);\n\tif ((toss.f & 0x10u) == 0u) {\n\t\tSetWasUnsuccessful();\n\t\treturn toss.f;\n\t}\n\twLoadedAttackAnimation = 0x6cu;", "case_ids": ["ScrunchEffect-0"]}
# <<< factory-mutation ScrunchEffect
# >>> factory-mutation SquirtleWithdrawEffect
MUTATIONS["SquirtleWithdrawEffect"] = {"source_symbol": "SquirtleWithdrawEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_PROTECT;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);", "after": "\twLoadedAttackAnimation = 0x50u;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);", "case_ids": ["SquirtleWithdrawEffect-0"]}
# <<< factory-mutation SquirtleWithdrawEffect
# >>> factory-mutation TailWagEffect
MUTATIONS["TailWagEffect"] = {"source_symbol": "TailWagEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_LURE;\n\tApplySubstatus2ToDefendingCard(SUBSTATUS2_TAIL_WAG, hl);", "after": "\twLoadedAttackAnimation = 0x47u;\n\tApplySubstatus2ToDefendingCard(SUBSTATUS2_TAIL_WAG, hl);", "case_ids": ["TailWagEffect-0"]}
# <<< factory-mutation TailWagEffect
# >>> factory-mutation TantrumEffect
MUTATIONS["TantrumEffect"] = {"source_symbol": "TantrumEffect", "before": "uint8_t TantrumEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsYourPokemonBecomesConfusedText, 0u);\n\tif ((toss.f & 0x10u) != 0u)\n\t\treturn toss.f;\n\twLoadedAttackAnimation = ATK_ANIM_MULTIPLE_SLASH;", "after": "uint8_t TantrumEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsYourPokemonBecomesConfusedText, 0u);\n\tif ((toss.f & 0x10u) != 0u)\n\t\treturn toss.f;\n\twLoadedAttackAnimation = 0x2au;", "case_ids": ["TantrumEffect-1"]}
# <<< factory-mutation TantrumEffect
# >>> factory-mutation Rampage_Confusion50PercentEffect
MUTATIONS["Rampage_Confusion50PercentEffect"] = {"source_symbol": "Rampage_Confusion50PercentEffect", "before": "void Rampage_Confusion50PercentEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage(damage.a);", "after": "void Rampage_Confusion50PercentEffect(void)\n{\n\tCardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tAddToDamage((uint8_t)(damage.a + 1u));", "case_ids": ["Rampage_Confusion50PercentEffect-0", "Rampage_Confusion50PercentEffect-1"]}
# <<< factory-mutation Rampage_Confusion50PercentEffect
# >>> factory-mutation WartortleWithdrawEffect
MUTATIONS["WartortleWithdrawEffect"] = {"source_symbol": "WartortleWithdrawEffect", "before": "\twLoadedAttackAnimation = ATK_ANIM_PROTECT;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);", "after": "\twLoadedAttackAnimation = 0x50u;\n\tApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);", "case_ids": ["WartortleWithdrawEffect-0"]}
# <<< factory-mutation WartortleWithdrawEffect
# >>> factory-mutation VenusaurMegaDrainEffect
MUTATIONS["VenusaurMegaDrainEffect"] = {"source_symbol": "VenusaurMegaDrainEffect", "before": "\tdealt = (uint16_t)(dealt >> 1);", "after": "\tdealt = (uint16_t)(dealt >> 2);", "case_ids": ["VenusaurMegaDrainEffect-0", "VenusaurMegaDrainEffect-1", "VenusaurMegaDrainEffect-3"]}
# <<< factory-mutation VenusaurMegaDrainEffect
# >>> factory-mutation SpacingOut_Success50PercentEffect
MUTATIONS["SpacingOut_Success50PercentEffect"] = {"source_symbol": "SpacingOut_Success50PercentEffect", "before": "void SpacingOut_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) == 0u) {", "after": "void SpacingOut_Success50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) != 0u) {", "case_ids": ["SpacingOut_Success50PercentEffect-0", "SpacingOut_Success50PercentEffect-1"]}
# <<< factory-mutation SpacingOut_Success50PercentEffect
# >>> factory-mutation VaporeonQuickAttack_DamageBoostEffect
MUTATIONS["VaporeonQuickAttack_DamageBoostEffect"] = {
    "source_symbol": "VaporeonQuickAttack_DamageBoostEffect",
    "before": "void VaporeonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(20u);",
    "after": "void VaporeonQuickAttack_DamageBoostEffect(void)\n{\n\tLoadTxRam3(20u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(21u);",
    "case_ids": ["VaporeonQuickAttack_DamageBoostEffect-0", "VaporeonQuickAttack_DamageBoostEffect-1"]
}
# <<< factory-mutation VaporeonQuickAttack_DamageBoostEffect
# >>> factory-mutation Thrash_ModifierEffect
MUTATIONS["Thrash_ModifierEffect"] = {"source_symbol": "Thrash_ModifierEffect", "before": "void Thrash_ModifierEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadPlus10IfTails10ToYourselfText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(10u);", "after": "void Thrash_ModifierEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfHeadPlus10IfTails10ToYourselfText, 0u);\n\thTemp_ffa0 = toss.a;\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(0u);", "case_ids": ["Thrash_ModifierEffect-0", "Thrash_ModifierEffect-1"]}
# <<< factory-mutation Thrash_ModifierEffect
# >>> factory-mutation ZapdosThunder_Recoil50PercentEffect
MUTATIONS["ZapdosThunder_Recoil50PercentEffect"] = {"source_symbol": "ZapdosThunder_Recoil50PercentEffect", "before": "void ZapdosThunder_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsDamageToYourselfTooText, 0u);\n\thTemp_ffa0 = toss.a;\n}", "after": "void ZapdosThunder_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsDamageToYourselfTooText, 0u);\n\thTemp_ffa0 = (uint8_t)(toss.a + 1u);\n}", "case_ids": ["ZapdosThunder_Recoil50PercentEffect-0", "ZapdosThunder_Recoil50PercentEffect-1", "ZapdosThunder_Recoil50PercentEffect-2"]}
# <<< factory-mutation ZapdosThunder_Recoil50PercentEffect
# >>> factory-mutation RaichuThunder_Recoil50PercentEffect
MUTATIONS["RaichuThunder_Recoil50PercentEffect"] = {"source_symbol": "RaichuThunder_Recoil50PercentEffect", "before": "void RaichuThunder_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoin_BankBResult result = TossCoin_BankB(IfTailsDamageToYourselfTooText, 0u);\n\thTemp_ffa0 = result.a;", "after": "void RaichuThunder_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(30u);\n\tTossCoin_BankBResult result = TossCoin_BankB(IfTailsDamageToYourselfTooText, 0u);\n\thTemp_ffa0 = 0u;", "case_ids": ["RaichuThunder_Recoil50PercentEffect-0", "RaichuThunder_Recoil50PercentEffect-1"]}
# <<< factory-mutation RaichuThunder_Recoil50PercentEffect
# >>> factory-mutation TaurosStomp_DamageBoostEffect
MUTATIONS["TaurosStomp_DamageBoostEffect"] = {"source_symbol": "TaurosStomp_DamageBoostEffect", "before": "void TaurosStomp_DamageBoostEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(10u);", "after": "void TaurosStomp_DamageBoostEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfHeadsPlusDamageText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn;\n\tAddToDamage(11u);", "case_ids": ["TaurosStomp_DamageBoostEffect-0"]}
# <<< factory-mutation TaurosStomp_DamageBoostEffect
# >>> factory-mutation MirrorMove_InitialEffect2
MUTATIONS["MirrorMove_InitialEffect2"] = {"source_symbol": "MirrorMove_InitialEffect2", "before": "PlayerPickAttackForAmnesiaResult MirrorMove_InitialEffect2(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "PlayerPickAttackForAmnesiaResult MirrorMove_InitialEffect2(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["MirrorMove_InitialEffect2-0", "MirrorMove_InitialEffect2-1", "MirrorMove_InitialEffect2-2"]}
# <<< factory-mutation MirrorMove_InitialEffect2
# >>> factory-mutation MysteryAttack_RecoverEffect
MUTATIONS["MysteryAttack_RecoverEffect"] = {"source_symbol": "MysteryAttack_RecoverEffect", "before": "void MysteryAttack_RecoverEffect(void)\n{\n\tuint8_t effect = hTemp_ffa0;\n\tif (effect != 4u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 10u);", "after": "void MysteryAttack_RecoverEffect(void)\n{\n\tuint8_t effect = hTemp_ffa0;\n\tif (effect != 4u)\n\t\treturn;\n\tApplyAndAnimateHPRecovery(0u, 20u);", "case_ids": ["MysteryAttack_RecoverEffect-0", "MysteryAttack_RecoverEffect-3"]}
# <<< factory-mutation MysteryAttack_RecoverEffect
# >>> factory-mutation ThunderJolt_Recoil50PercentEffect
MUTATIONS["ThunderJolt_Recoil50PercentEffect"] = {"source_symbol": "ThunderJolt_Recoil50PercentEffect", "before": "ThunderJolt_Recoil50PercentEffectResult ThunderJolt_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsDamageToYourselfTooText, 10u);\n\thTemp_ffa0 = toss.a;", "after": "ThunderJolt_Recoil50PercentEffectResult ThunderJolt_Recoil50PercentEffect(void)\n{\n\tLoadTxRam3(10u);\n\tTossCoin_BankBResult toss = TossCoin_BankB(IfTailsDamageToYourselfTooText, 10u);\n\thTemp_ffa0 = (uint8_t)(toss.a + 1u);", "case_ids": ["ThunderJolt_Recoil50PercentEffect-0", "ThunderJolt_Recoil50PercentEffect-1", "ThunderJolt_Recoil50PercentEffect-2"]}
# <<< factory-mutation ThunderJolt_Recoil50PercentEffect
# >>> factory-mutation LeekSlap_NoDamage50PercentEffect
MUTATIONS["LeekSlap_NoDamage50PercentEffect"] = {"source_symbol": "LeekSlap_NoDamage50PercentEffect", "before": "uint8_t LeekSlap_NoDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfTailsNoDamageText, 0u);\n\tif ((toss.f & 0x10u) != 0u)\n\t\treturn toss.f;\n\tSetDefiniteDamage(0u);", "after": "uint8_t LeekSlap_NoDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageCheckIfTailsNoDamageText, 0u);\n\tif ((toss.f & 0x10u) != 0u)\n\t\treturn toss.f;\n\tSetDefiniteDamage(1u);", "case_ids": ["LeekSlap_NoDamage50PercentEffect-1"]}
# <<< factory-mutation LeekSlap_NoDamage50PercentEffect
# >>> factory-mutation Blizzard_BenchDamage50PercentEffect
MUTATIONS["Blizzard_BenchDamage50PercentEffect"] = {"source_symbol": "Blizzard_BenchDamage50PercentEffect", "before": "void Blizzard_BenchDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageToOppBenchIfHeadsDamageToYoursIfTailsText, 0u);\n\thTemp_ffa0 = toss.a;", "after": "void Blizzard_BenchDamage50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(DamageToOppBenchIfHeadsDamageToYoursIfTailsText, 0u);\n\thTemp_ffa0 = (uint8_t)(toss.a ^ 0x01u);", "case_ids": ["Blizzard_BenchDamage50PercentEffect-0", "Blizzard_BenchDamage50PercentEffect-1"]}
# <<< factory-mutation Blizzard_BenchDamage50PercentEffect
# >>> factory-mutation SpearowMirrorMove_InitialEffect2
MUTATIONS["SpearowMirrorMove_InitialEffect2"] = {"source_symbol": "SpearowMirrorMove_InitialEffect2", "before": "PlayerPickAttackForAmnesiaResult SpearowMirrorMove_InitialEffect2(void)\n{\n\treturn MirrorMove_InitialEffect2();\n}", "after": "PlayerPickAttackForAmnesiaResult SpearowMirrorMove_InitialEffect2(void)\n{\n\treturn (PlayerPickAttackForAmnesiaResult){0u, 0u};\n}", "case_ids": ["SpearowMirrorMove_InitialEffect2-0", "SpearowMirrorMove_InitialEffect2-1", "SpearowMirrorMove_InitialEffect2-2"]}
# <<< factory-mutation SpearowMirrorMove_InitialEffect2
# >>> factory-mutation PidgeottoMirrorMove_InitialEffect2
MUTATIONS["PidgeottoMirrorMove_InitialEffect2"] = {"source_symbol": "PidgeottoMirrorMove_InitialEffect2", "before": "\treturn MirrorMove_InitialEffect2();", "after": "\treturn (PlayerPickAttackForAmnesiaResult){0};", "case_ids": ["PidgeottoMirrorMove_InitialEffect2-0", "PidgeottoMirrorMove_InitialEffect2-1"]}
# <<< factory-mutation PidgeottoMirrorMove_InitialEffect2
# >>> factory-mutation VenomPowder_PoisonConfusion50PercentEffect
MUTATIONS["VenomPowder_PoisonConfusion50PercentEffect"] = {"source_symbol": "VenomPowder_PoisonConfusion50PercentEffect", "before": "uint8_t VenomPowder_PoisonConfusion50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(VenomPowderCheckText, 0u);\n\tif ((toss.f & 0x10u) == 0u)\n\t\treturn toss.f;", "after": "uint8_t VenomPowder_PoisonConfusion50PercentEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(VenomPowderCheckText, 0u);\n\tif ((toss.f & 0x10u) != 0u)\n\t\treturn toss.f;", "case_ids": ["VenomPowder_PoisonConfusion50PercentEffect-0", "VenomPowder_PoisonConfusion50PercentEffect-1"]}
# <<< factory-mutation VenomPowder_PoisonConfusion50PercentEffect
# >>> factory-mutation ThunderstormEffect
MUTATIONS["ThunderstormEffect"] = {"source_symbol": "ThunderstormEffect", "before": "void ThunderstormEffect(void)\n{\n\thCurSelectionItem = 1u;", "after": "void ThunderstormEffect(void)\n{\n\thCurSelectionItem = 0u;", "case_ids": ["ThunderstormEffect-0", "ThunderstormEffect-1"]}
# <<< factory-mutation ThunderstormEffect
# >>> factory-mutation FoulGas_PoisonOrConfusionEffect
MUTATIONS["FoulGas_PoisonOrConfusionEffect"] = {"source_symbol": "FoulGas_PoisonOrConfusionEffect", "before": "uint8_t FoulGas_PoisonOrConfusionEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonedIfHeadsConfusedIfTailsText, 0u);\n\tif ((toss.f & 0x10u) == 0u)", "after": "uint8_t FoulGas_PoisonOrConfusionEffect(void)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonedIfHeadsConfusedIfTailsText, 0u);\n\tif ((toss.f & 0x10u) != 0u)", "case_ids": ["FoulGas_PoisonOrConfusionEffect-0", "FoulGas_PoisonOrConfusionEffect-1"]}
# <<< factory-mutation FoulGas_PoisonOrConfusionEffect
# >>> factory-mutation Sprout_PlayerSelectEffect
MUTATIONS["Sprout_PlayerSelectEffect"] = {"source_symbol": "Sprout_PlayerSelectEffect", "before": "Sprout_PlayerSelectEffectResult Sprout_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;", "after": "Sprout_PlayerSelectEffectResult Sprout_PlayerSelectEffect(void)\n{\n\thTemp_ffa0 = 0x00u;", "case_ids": ["Sprout_PlayerSelectEffect-0", "Sprout_PlayerSelectEffect-1"]}
# <<< factory-mutation Sprout_PlayerSelectEffect
# >>> factory-mutation FullHeal_ClearStatusEffect
MUTATIONS["FullHeal_ClearStatusEffect"] = {"source_symbol": "FullHeal_ClearStatusEffect", "before": "void FullHeal_ClearStatusEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\tPlayTrainerEffectAnimation(ATK_ANIM_FULL_HEAL, f, b, c, d, e, hl);\n\tDuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);\n\tgb_write8(status.hl, NO_STATUS);","after":"void FullHeal_ClearStatusEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\tPlayTrainerEffectAnimation(ATK_ANIM_FULL_HEAL, f, b, c, d, e, hl);\n\tDuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);\n\tgb_write8(status.hl, 0x01u);","case_ids":["FullHeal_ClearStatusEffect-0","FullHeal_ClearStatusEffect-1"]}
# <<< factory-mutation FullHeal_ClearStatusEffect
# >>> factory-mutation ImakuniEffect
MUTATIONS["ImakuniEffect"] = {"source_symbol": "ImakuniEffect", "before": "\tstatus.a = (uint8_t)((status.a & PSN_DBLPSN) | CONFUSED);", "after": "\tstatus.a = (uint8_t)(status.a & PSN_DBLPSN);", "case_ids": ["ImakuniEffect-0", "ImakuniEffect-3", "ImakuniEffect-4"]}
# <<< factory-mutation ImakuniEffect
# >>> factory-mutation GamblerEffect
MUTATIONS["GamblerEffect"] = {"source_symbol": "GamblerEffect", "before": "\tuint8_t draw_count = hTemp_ffa0 != 0u ? 8u : 1u;", "after": "\tuint8_t draw_count = hTemp_ffa0 != 0u ? 7u : 2u;", "case_ids": ["GamblerEffect-0", "GamblerEffect-1"]}
# <<< factory-mutation GamblerEffect
# >>> factory-mutation HealingWind_PlayAreaHealEffect
MUTATIONS["HealingWind_PlayAreaHealEffect"] = {"source_symbol": "HealingWind_PlayAreaHealEffect", "before": "\ta = ATK_ANIM_HEALING_WIND_PLAY_AREA;\n\twLoadedAttackAnimation = a;", "after": "\ta = 0x00u;\n\twLoadedAttackAnimation = a;", "case_ids": ["HealingWind_PlayAreaHealEffect-0", "HealingWind_PlayAreaHealEffect-1", "HealingWind_PlayAreaHealEffect-2", "HealingWind_PlayAreaHealEffect-3"]}
# <<< factory-mutation HealingWind_PlayAreaHealEffect
# >>> factory-mutation SpitPoison_Poison50PercentEffect
MUTATIONS["SpitPoison_Poison50PercentEffect"] = {
    "source_symbol": "SpitPoison_Poison50PercentEffect",
    "before": "SpitPoison_Poison50PercentEffectResult SpitPoison_Poison50PercentEffect(uint16_t hl)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonCheckText, hl);\n\tif ((toss.f & 0x10u) != 0u) {",
    "after": "SpitPoison_Poison50PercentEffectResult SpitPoison_Poison50PercentEffect(uint16_t hl)\n{\n\tTossCoin_BankBResult toss = TossCoin_BankB(PoisonCheckText, hl);\n\tif ((toss.f & 0x10u) == 0u) {",
    "case_ids": ["SpitPoison_Poison50PercentEffect-0", "SpitPoison_Poison50PercentEffect-1"]
}
# <<< factory-mutation SpitPoison_Poison50PercentEffect
# >>> factory-mutation Peek_SelectEffect
MUTATIONS["Peek_SelectEffect"] = {"source_symbol": "Peek_SelectEffect", "before": "\tgb_write8(arena_flags.hl, (uint8_t)(arena_flags.a | (1u << USED_PKMN_POWER_THIS_TURN_F)));", "after": "\tgb_write8(arena_flags.hl, arena_flags.a);", "case_ids": ["Peek_SelectEffect-0", "Peek_SelectEffect-1"]}
# <<< factory-mutation Peek_SelectEffect
# >>> factory-mutation MagneticStormEffect
MUTATIONS["MagneticStormEffect"] = {"source_symbol": "MagneticStormEffect", "before": "void MagneticStormEffect(void)\n{\n\tDuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);\n\tuint16_t energy_list = wDuelTempList_ADDR;", "after": "void MagneticStormEffect(void)\n{\n\tDuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);\n\tuint16_t energy_list = (uint16_t)(wDuelTempList_ADDR + 1u);", "case_ids": ["MagneticStormEffect-1", "MagneticStormEffect-2"]}
# <<< factory-mutation MagneticStormEffect
# >>> factory-mutation RandomlyDamagePlayAreaPokemon
MUTATIONS["RandomlyDamagePlayAreaPokemon"] = {"source_symbol": "RandomlyDamagePlayAreaPokemon", "before": "RandomlyDamagePlayAreaPokemonResult RandomlyDamagePlayAreaPokemon(uint16_t de)\n{\n\tfor (;;) {\n\t\twNoDamageOrEffect = 0u;", "after": "RandomlyDamagePlayAreaPokemonResult RandomlyDamagePlayAreaPokemon(uint16_t de)\n{\n\tfor (;;) {\n\t\twNoDamageOrEffect = 1u;", "case_ids": ["RandomlyDamagePlayAreaPokemon-0", "RandomlyDamagePlayAreaPokemon-1", "RandomlyDamagePlayAreaPokemon-2"]}
# <<< factory-mutation RandomlyDamagePlayAreaPokemon
# >>> factory-mutation BigThunderEffect
MUTATIONS["BigThunderEffect"] = {"source_symbol": "BigThunderEffect", "before": "RandomlyDamagePlayAreaPokemonResult BigThunderEffect(uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{\n\t(void)ExchangeRNG(b, c, de, hl);\n\treturn RandomlyDamagePlayAreaPokemon(70u);", "after": "RandomlyDamagePlayAreaPokemonResult BigThunderEffect(uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{\n\t(void)ExchangeRNG(b, c, de, hl);\n\treturn RandomlyDamagePlayAreaPokemon(0u);", "case_ids": ["BigThunderEffect-0", "BigThunderEffect-1", "BigThunderEffect-2"]}
# <<< factory-mutation BigThunderEffect
# >>> factory-mutation EnergySearch_AddToHandEffect
MUTATIONS["EnergySearch_AddToHandEffect"] = {"source_symbol": "EnergySearch_AddToHandEffect", "before": "ShuffleCardsInDeckResult EnergySearch_AddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t card = hTemp_ffa0;", "after": "ShuffleCardsInDeckResult EnergySearch_AddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t card = 0xFFu;", "case_ids": ["EnergySearch_AddToHandEffect-0", "EnergySearch_AddToHandEffect-2"]}
# <<< factory-mutation EnergySearch_AddToHandEffect
# >>> factory-mutation LassEffect
MUTATIONS["LassEffect"] = {"source_symbol": "LassEffect", "before": "\thCurSelectionItem = 0u;", "after": "\thCurSelectionItem = 1u;", "case_ids": ["LassEffect-0", "LassEffect-1"]}
# <<< factory-mutation LassEffect
# >>> factory-mutation ComputerSearch_DiscardAddToHandEffect
MUTATIONS["ComputerSearch_DiscardAddToHandEffect"] = {"source_symbol": "ComputerSearch_DiscardAddToHandEffect", "before": "ShuffleCardsInDeckResult ComputerSearch_DiscardAddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\t(void)f;\n\thl = hTempList_ADDR;\n\tuint8_t first = gb_read8(hl++);\n\tRemoveCardFromHand(first);\n\tPutCardInDiscardPile(first);\n\tuint8_t second = gb_read8(hl++);", "after": "ShuffleCardsInDeckResult ComputerSearch_DiscardAddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\t(void)a;\n\t(void)f;\n\thl = hTempList_ADDR;\n\tuint8_t first = (uint8_t)(gb_read8(hl++) + 1u);\n\tRemoveCardFromHand(first);\n\tPutCardInDiscardPile(first);\n\tuint8_t second = gb_read8(hl++);", "case_ids": ["ComputerSearch_DiscardAddToHandEffect-0", "ComputerSearch_DiscardAddToHandEffect-1"]}
# <<< factory-mutation ComputerSearch_DiscardAddToHandEffect
# >>> factory-mutation PokeBall_AddToHandEffect
MUTATIONS["PokeBall_AddToHandEffect"] = {"source_symbol": "PokeBall_AddToHandEffect", "before": "ShuffleCardsInDeckResult PokeBall_AddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t toss = hTempList;\n\tif (toss == 0u)\n\t\treturn (ShuffleCardsInDeckResult){toss, b, c, d, e, 0x80u, hl};", "after": "ShuffleCardsInDeckResult PokeBall_AddToHandEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t toss = hTempList;\n\tif (toss == 0u)\n\t\treturn (ShuffleCardsInDeckResult){toss, b, c, d, e, 0x00u, hl};", "case_ids": ["PokeBall_AddToHandEffect-0", "PokeBall_AddToHandEffect-1"]}
# <<< factory-mutation PokeBall_AddToHandEffect
# >>> factory-mutation HealPlayAreaCardHP
MUTATIONS["HealPlayAreaCardHP"] = {"source_symbol": "HealPlayAreaCardHP", "before": "\twLoadedAttackAnimation = ATK_ANIM_HEALING_WIND_PLAY_AREA;", "after": "\twLoadedAttackAnimation = (uint8_t)(ATK_ANIM_HEALING_WIND_PLAY_AREA + 1u);", "case_ids": ["HealPlayAreaCardHP-0", "HealPlayAreaCardHP-1", "HealPlayAreaCardHP-2"]}
# <<< factory-mutation HealPlayAreaCardHP
# >>> factory-completion HealPlayAreaCardHP
for _record in SCHEMA2_CASES["HealPlayAreaCardHP"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x7494, "bank": 1}
# <<< factory-completion HealPlayAreaCardHP
# >>> factory-mutation Potion_HealEffect
MUTATIONS["Potion_HealEffect"] = {"source_symbol": "Potion_HealEffect", "before": "void Potion_HealEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\thTempPlayAreaLocation_ff9d = hTemp_ffa0;", "after": "void Potion_HealEffect(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\thTempPlayAreaLocation_ff9d = 0u;", "case_ids": ["Potion_HealEffect-0", "Potion_HealEffect-1", "Potion_HealEffect-2"]}
# <<< factory-mutation Potion_HealEffect
# >>> factory-completion Potion_HealEffect
for _record in SCHEMA2_CASES["Potion_HealEffect"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x7EBC, "bank": 11}
# <<< factory-completion Potion_HealEffect
