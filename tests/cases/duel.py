from tests.cases._symbols import SRAM_START, deck_entry, sym, sym_bank, sym_pointer
from tests.cases._fixtures import full_heal_trainer_fixture as _full_heal_trainer_fixture, FULL_HEAL_TRAINER_REGS as _FULL_HEAL_TRAINER_REGS
from tests.cases._fixtures import init_duelvar_fixture as _init_duelvar_fixture, INIT_DUELVAR_REGS as _INIT_DUELVAR_REGS
from tests.cases._fixtures import swap_duelvar_fixture as _swap_duelvar_fixture, SWAP_DUELVAR_REGS as _SWAP_DUELVAR_REGS
from tests.cases._fixtures import count_card_id_fixture as _count_card_id_fixture, COUNT_CARD_ID_REGS as _COUNT_CARD_ID_REGS
from tests.cases._fixtures import attack_fixture as _attack_fixture, ATTACK_REGS as _ATTACK_REGS
from tests.cases._fixtures import pkmn_power_fixture as _pkmn_power_fixture, PKMN_POWER_REGS as _PKMN_POWER_REGS

_wTxRam2 = sym("wTxRam2")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# hWhoseTurn (player $C2 / opponent $C3) selects the duel-variables page.
hWhoseTurn = sym("hWhoseTurn")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
wOpponentDuelVariables = sym("wOpponentDuelVariables")
wPlayerDeck = sym("wPlayerDeck")
wOpponentDeck = sym("wOpponentDeck")
wDuelTempList = sym("wDuelTempList")
wDamage_ADDR = sym("wDamage")
wDamageEffectiveness_ADDR = sym("wDamageEffectiveness")
wTempTurnDuelistCardID = sym("wTempTurnDuelistCardID")
wTempNonTurnDuelistCardID = sym("wTempNonTurnDuelistCardID")
wSentAttackDataToLinkOpponent = sym("wSentAttackDataToLinkOpponent")
wStatusConditionQueueIndex = sym("wStatusConditionQueueIndex")
wEffectFailed = sym("wEffectFailed")
wIsDamageToSelf = sym("wIsDamageToSelf")
wDefendingWasForcedToSwitch = sym("wDefendingWasForcedToSwitch")
wMetronomeEnergyCost = sym("wMetronomeEnergyCost")
wNoEffectFromWhichStatus = sym("wNoEffectFromWhichStatus")

CONTRACT = {
    "CopyPlayerName": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "CopyOpponentName": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "GetTurnDuelistVariable": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetNonTurnDuelistVariable": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "SwapTurn": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "_GetCardIDFromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")},
    "GetCardIDFromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    "GetCardIDFromDeckIndex_bc": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")},
    "GetCardInDuelTempList_OnlyDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetCardInDuelTempList": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    "LoadCardDataToBuffer1_FromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "LoadCardDataToBuffer2_FromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SubtractHP": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CreateDeckCardList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CreateDiscardPileCardList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "RemoveCardFromDuelTempList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CountCardsInDuelTempList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FindLastCardInHand": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CreateHandCardList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CreateArenaOrBenchEnergyCardList": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "ShuffleCards": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SortCardsInListByID": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "SortCardsInDuelTempListByID": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "SortHandCardsByID": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "TranslateColorToWR": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CountCardIDInLocation": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "CheckLoadedAttackFlag": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetCardDamageAndMaxHP": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "d", "e", "hl")},
    "CopyDeckData": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CountPrizes": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "ShuffleDeck": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "DrawCardFromDeck": {"compare": ("a", "f"), "preserve": ()},
    "ReturnCardToDeck": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "f", "hl")},
    "SearchCardInDeckAndAddToHand": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "f", "hl")},
    "AddCardToHand": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "f", "hl")},
    "RemoveCardFromHand": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "f", "hl")},
    "MoveHandCardToDiscardPile": {"compare": ("a", "f", "hl"), "preserve": ()},
    "PutCardInDiscardPile": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "f", "hl")},
    "MoveDiscardPileCardToHand": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CheckPrizeTaken": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c")},
    "SortCardsInListByID_CheckForListTerminator": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CheckIfCanEvolveInto": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CheckIfCanEvolveInto_BasicToStage2": {"compare": ("a", "f", "hl"), "preserve": ()},
    "EvolvePokemonCardIfPossible": {"compare": ("a", "c", "d", "e", "f", "hl"), "preserve": ()},
    "EvolvePokemonCard": {"compare": ("a", "c", "e", "f", "hl"), "preserve": ()},
    "ClearAllStatusConditions": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "PutHandCardInPlayArea": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "PutHandPokemonCardInPlayArea": {"compare": ("a", "b", "c", "d", "f", "hl"), "preserve": ()},
    "EmptyPlayAreaSlot": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "EmptyPlayAreaSlot.init_duelvar": {"compare": ("a", "f", "hl"), "preserve": ()},
    "SwapPlayAreaPokemon.swap_duelvar": {"compare": ("a", "c", "f", "hl"), "preserve": ()},
    "SwapPlayAreaPokemon": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SwapArenaWithBenchPokemon": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "ShiftTurnPokemonToFirstPlayAreaSlots": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "ShiftAllPokemonToFirstPlayAreaSlots": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "GetPlayAreaCardAttachedEnergies": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "CopyAttackDataAndDamage": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CopyAttackDataAndDamage_FromDeckIndex": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "CopyAttackDataAndDamage_FromCardID": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "ReturnCarry": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")},
    "LoadNonPokemonCardEffectCommands": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "ApplyAttachedPlusPower": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "ApplyAttachedDefender": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "MoveCardToDiscardPileIfInPlayArea": {"compare": ("a", "b", "c", "f", "hl"), "preserve": ()},
    "ApplyDamageModifiers_DamageToTarget": {"compare": ("d", "e"), "preserve": ()},
    "ApplyDamageModifiers_DamageToSelf": {"compare": ("d", "e"), "preserve": ()},
    "GetPlayAreaCardRetreatCost": {"compare": ("a",), "preserve": ()},
    "DrawWideTextBox_WaitForInput_ReturnCarry": {"compare": ("f",), "preserve": ()},
    "PrintKnockedOut": {"compare": ("f",), "preserve": ()},
    "PrintPlayAreaCardKnockedOutIfNoHP": {"compare": ("a", "f"), "preserve": ()},
    "UpdateArenaCardIDsAndClearTwoTurnDuelVars": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c"),
    },
    "ClearNonTurnTemporaryDuelvars_ResetCarry": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
    "PrintKnockedOutIfHLZero": {"compare": ("f",), "preserve": ()},
    "MovePlayAreaCardToDiscardPile": {
        "compare": ("b", "c", "e"),
        "preserve": ("b", "c", "e"),
    },
}

CASES = {
    "CopyPlayerName": [
        {"d": 0xC1, "e": 0x00, "sram": {0: {sym("sPlayerName"): b"\x21\x22\x00"}},
         "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 3}},
        dict(POISON, d=0xC2, e=0x00,
             sram={2: {SRAM_START + 0x10: b"\x31\x00"}}, wram={sym("hBankSRAM"): b"\x02"},
             read={sym("wPlayerCardLocations"): 2}),
    ],
    "CopyOpponentName": [
        {"d": 0xC1, "e": 0x00, "wram": {sym("wNameBuffer"): b"\x41\x42\x00"},
         "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 3}},
        dict(POISON, d=0xC2, e=0x00, wram={sym("wNameBuffer"): b"\x51\x00"},
             read={sym("wPlayerCardLocations"): 2}),
    ],
    # Player's turn: reads the $C2 page. Opponent's turn: reads the $C3 page.
    "GetTurnDuelistVariable": [
        {"a": 0x05, "wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 5: b"\x77"}},
        {"a": 0x05, "wram": {hWhoseTurn: b"\xC3", wOpponentDuelVariables + 5: b"\x88"}},
        dict(POISON, a=0x00, wram={hWhoseTurn: b"\xC2",
                                   wPlayerDuelVariables: b"\x11"}),
    ],
    # The other player's page: opponent when it's the player's turn and vice versa.
    "GetNonTurnDuelistVariable": [
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC2", wOpponentDuelVariables + 3: b"\x44"}},
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC3", wPlayerDuelVariables + 3: b"\x55"}},
        dict(POISON, a=0x07, wram={hWhoseTurn: b"\xC2",
                                   wOpponentDuelVariables + 7: b"\x66"}),
    ],
    # SwapTurn flips hWhoseTurn between the two pages.
    "SwapTurn": [
        {"wram": {hWhoseTurn: b"\xC2"}, "read": {hWhoseTurn: 1}},
        {"wram": {hWhoseTurn: b"\xC3"}, "read": {hWhoseTurn: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2"}, read={hWhoseTurn: 1}),
    ],
    # Deck index -> id from the turn holder's deck; hl = deck base + index.
    "_GetCardIDFromDeckIndex": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", **deck_entry(0, 0x10, base=wPlayerDeck)}},
        {"a": 5, "wram": {hWhoseTurn: b"\xC3", **deck_entry(5, 0x22, base=wOpponentDeck)}},
        dict(POISON, a=3, wram={hWhoseTurn: b"\xC2", **deck_entry(3, 0x33, base=wPlayerDeck)}),
    ],
    # id in de, af and hl preserved.
    "GetCardIDFromDeckIndex": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", **deck_entry(0, 0x10, base=wPlayerDeck)}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC2", **deck_entry(5, 0x22, base=wPlayerDeck)}),
    ],
    # id in a and c, b = 0, hl preserved.
    "GetCardIDFromDeckIndex_bc": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", **deck_entry(0, 0x10, base=wPlayerDeck)}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC3", **deck_entry(5, 0x22, base=wOpponentDeck)}),
    ],
    # Temp-list entry shadowed in hTempCardIndex_ff98, hl preserved.
    "GetCardInDuelTempList_OnlyDeckIndex": [
        {"a": 0, "wram": {wDuelTempList: b"\x07"}, "read": {sym("hTempCardIndex_ff98"): 1}},
        dict(POISON, a=2, wram={wDuelTempList + 2: b"\x09"}, read={sym("hTempCardIndex_ff98"): 1}),
    ],
    # Entry in a (reloaded), id in de, hl preserved.
    "GetCardInDuelTempList": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wDuelTempList: b"\x01",
                          **deck_entry(1, 0x44, base=wPlayerDeck)}, "read": {sym("hTempCardIndex_ff98"): 1}},
        dict(POISON, a=1, wram={hWhoseTurn: b"\xC3", wDuelTempList + 1: b"\x02",
                                **deck_entry(2, 0x55, base=wOpponentDeck)}, read={sym("hTempCardIndex_ff98"): 1}),
    ],
    # Deck card loaded into wLoadedCard1: the type byte lands in the buffer and
    # exit a is the card id's low byte. wLoadedCard1 = $CC24.
    "LoadCardDataToBuffer1_FromDeckIndex": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", **deck_entry(0, 0x10, base=wPlayerDeck)},
         "read": {sym("wLoadedCard1"): 64}},
        dict(POISON, a=3, wram={hWhoseTurn: b"\xC2", **deck_entry(3, 0x20, base=wPlayerDeck)},
             read={sym("wLoadedCard1"): 64}),
    ],
    "LoadCardDataToBuffer2_FromDeckIndex": [
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", **deck_entry(1, 0x15, base=wPlayerDeck)},
         "read": {sym("wLoadedCard2"): 64}},
        dict(POISON, a=4, wram={hWhoseTurn: b"\xC2", **deck_entry(4, 0x25, base=wPlayerDeck)},
             read={sym("wLoadedCard2"): 64}),
    ],
    # HP minus damage, clamped at zero; carry set iff HP remains.
    "SubtractHP": [
        {"hl": sym("wBoosterCardsDrawn"), "d": 0x00, "e": 3, "wram": {sym("wBoosterCardsDrawn"): b"\x0a"}, "read": {sym("wBoosterCardsDrawn"): 1}},
        {"hl": sym("wBoosterCardsDrawn"), "d": 0x00, "e": 10, "wram": {sym("wBoosterCardsDrawn"): b"\x0a"}, "read": {sym("wBoosterCardsDrawn"): 1}},
        {"hl": sym("wBoosterCardsDrawn"), "d": 0x01, "e": 0, "wram": {sym("wBoosterCardsDrawn"): b"\x0a"}, "read": {sym("wBoosterCardsDrawn"): 1}},
        {"hl": sym("wBoosterCardsDrawn"), "d": 0x00, "e": 0, "wram": {sym("wBoosterCardsDrawn"): b"\x00"}, "read": {sym("wBoosterCardsDrawn"): 1}},
        dict(POISON, hl=sym("wBoosterCardsDrawn"), d=0x00, e=5, wram={sym("wBoosterCardsDrawn"): b"\x64"}, read={sym("wBoosterCardsDrawn"): 1}),
    ],
    # wDuelTempList = $C510. Deck cards occupy $C27E-$C2B9 in the player page.
    "CreateDeckCardList": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x00"},
         "read": {sym("wDuelTempList"): 62}},
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x3c"},
         "read": {sym("wDuelTempList"): 26}},
        # All cards drawn: empty path, terminator only, carry set.
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x3c"},
         "read": {sym("wDuelTempList"): 2}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsNotInDeck"): b"\x05"},
             read={sym("wDuelTempList"): 60}),
    ],
    "CreateDiscardPileCardList": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00"}, "read": {sym("wDuelTempList"): 2}},
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02", sym("wPlayerDeckCards"): b"\x11",
                  sym("wPlayerDeckCards") + 1: b"\x22"}, "read": {sym("wDuelTempList"): 4}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x01", sym("wOpponentDeckCards") + 1: b"\x33"},
             read={sym("wDuelTempList"): 4}),
    ],
    # Remove the card id in a from the FF-terminated wDuelTempList.
    "RemoveCardFromDuelTempList": [
        {"a": 3, "wram": {sym("wDuelTempList"): b"\x01\x02\x03\x04\xff"}, "read": {sym("wDuelTempList"): 5}},
        {"a": 1, "wram": {sym("wDuelTempList"): b"\x01\xff"}, "read": {sym("wDuelTempList"): 2}},
        {"a": 9, "wram": {sym("wDuelTempList"): b"\x01\x02\xff"}, "read": {sym("wDuelTempList"): 4}},
        dict(POISON, a=2, wram={sym("wDuelTempList"): b"\x02\x02\xff"}, read={sym("wDuelTempList"): 3}),
    ],
    "CountCardsInDuelTempList": [
        {"wram": {sym("wDuelTempList"): b"\xff"}},
        {"wram": {sym("wDuelTempList"): b"\x01\x02\x03\xff"}},
        dict(POISON, wram={sym("wDuelTempList"): b"\x01\xff"}),
    ],
    # Hand cards live at $C242+; count at $C2EE. Locations at $C200+.
    "FindLastCardInHand": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x02"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00"}),
    ],
    # Just-drawn cards (location bit 6) are skipped.
    "CreateHandCardList": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x02",
                  sym("wPlayerHand") + 1: b"\x03", sym("wPlayerHand"): b"\x01",
                  sym("wPlayerCardLocations") + 1: b"\x00", sym("wPlayerCardLocations") + 3: b"\x40"},
         "read": {sym("wDuelTempList"): 4}},
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x01",
                  sym("wPlayerHand"): b"\x02", sym("wPlayerCardLocations") + 2: b"\x40"},
         "read": {sym("wDuelTempList"): 3}},
        # Empty hand: carry set, terminator only.
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00"}, "read": {sym("wDuelTempList"): 2}},
        # Poisoned c is preserved (the routine never touches it).
        dict(POISON, wram={hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00"}, read={sym("wDuelTempList"): 2}),
    ],
    # Energy scan: deck index 0 is GRASS_ENERGY (id $01, energy type) in the play
    # area; deck index 1 is CLEFAIRY_DOLL (id $CB, trainer) so it is skipped.
    "CreateArenaOrBenchEnergyCardList": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x10", sym("wPlayerCardLocations") + 1: b"\x10",
                          wPlayerDeck: b"\x01", wPlayerDeck + 1: b"\xCB"},
         "read": {sym("wDuelTempList"): 4}},
        # No cards in the requested location (1 = bench): empty list, carry set.
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x00"}, "read": {sym("wDuelTempList"): 2}},
    ],
    # Shuffle uses Random over the seeded RNG state ($CACA-$CACC), so the
    # outcome is deterministic and diffed against the real ROM.
    "ShuffleCards": [
        {"a": 0, "hl": sym("wPlayerDeckCards"), "wram": {sym("wPlayerDeckCards"): b"\x01\x02\x03\x04"},
         "read": {sym("wPlayerDeckCards"): 4}},
        {"a": 3, "hl": sym("wPlayerDeckCards"),
         "wram": {sym("wPlayerDeckCards"): b"\x01\x02\x03\x04",
                  sym("wRNG1"): b"\x11\x22\x33"},
         "read": {sym("wPlayerDeckCards"): 4}},
        {"a": 4, "hl": sym("wPlayerDeckCards"),
         "wram": {sym("wPlayerDeckCards"): b"\x0a\x0b\x0c\x0d\x0e",
                  sym("wRNG1"): b"\x00\x00\x00"},
         "read": {sym("wPlayerDeckCards"): 5}},
        dict(POISON, a=2, hl=sym("wPlayerDeckCards"),
             wram={sym("wPlayerDeckCards"): b"\x05\x06\x07", sym("wRNG1"): b"\x00\x00\x00"},
             read={sym("wPlayerDeckCards"): 3}),
    ],
    # Sort by card id: deck index -> id at $C400. The sort is unstable (equal ids
    # swap the later card forward), so the deck seeds use distinct ids to pin order.
    "SortCardsInDuelTempListByID": [
        # ids: idx0=$CB, idx1=$01, idx2=$02 -> sorted [1, 2, 0].
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\xCB\x01\x02",
                  sym("wDuelTempList"): b"\x00\x02\x01\xff"},
         "read": {sym("wDuelTempList"): 4, sym("hTempListPtr_ff99"): 2}},
        # Already sorted: identity passes.
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02\xCB",
                  sym("wDuelTempList"): b"\x00\x01\x02\xff"},
         "read": {sym("wDuelTempList"): 4, sym("hTempListPtr_ff99"): 2}},
        # Empty list.
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01", sym("wDuelTempList"): b"\xff"},
         "read": {sym("wDuelTempList"): 2, sym("hTempListPtr_ff99"): 2}},
        # Equal ids: the later card moves to the front (unstable).
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x01",
                  sym("wDuelTempList"): b"\x00\x01\xff"},
         "read": {sym("wDuelTempList"): 3, sym("hTempListPtr_ff99"): 2}},
    ],
    # hTempListPtr_ff99 preselects the list to sort. The direct entry reads [ptr]
    # as a card index and scans from [ptr+1], so a well-formed list ends with the
    # terminator at [ptr+1]; the sort stops once the pointer itself lands on $FF.
    # hTempCardID_ff9b ($FF9B-$FF9C) holds the running lowest id
    # (duel.asm:599-602, 618-622); its final value is the last pass's.
    "SortCardsInListByID": [
        {"wram": {hWhoseTurn: b"\xC2", sym("hTempListPtr_ff99"): b"\x10\xC5", sym("hTempCardID_ff9b"): b"\x55\x55",
                  sym("wDuelTempList"): b"\x02\x01\x00\xff", wPlayerDeck: b"\x03\x02\x01"},
         "read": {sym("wDuelTempList"): 4, sym("hTempListPtr_ff99"): 2}},
        # Single card at [ptr], terminator at [ptr+1].
        {"wram": {hWhoseTurn: b"\xC2", sym("hTempListPtr_ff99"): b"\x00\xC5", sym("hTempCardID_ff9b"): b"\x55\x55",
                  sym("wNameBuffer"): b"\x00\xff", wPlayerDeck: b"\x01"},
         "read": {sym("wNameBuffer"): 2, sym("hTempListPtr_ff99"): 2}},
    ],
    # Hand cards at $C242 (count 2): sorted ascending by id and written back so
    # the lowest id is at the newest slot ($C243).
    "SortHandCardsByID": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x02",
                  sym("wPlayerHand") + 1: b"\x00", sym("wPlayerHand"): b"\x01",
                  wPlayerDeck: b"\xCB\x01"},
         "read": {sym("wPlayerHand"): 2, sym("wDuelTempList"): 4}},
        # Already sorted: the write-back reverses the order.
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x02",
                  sym("wPlayerHand") + 1: b"\x01", sym("wPlayerHand"): b"\x00",
                  wPlayerDeck: b"\x01\x02"},
         "read": {sym("wPlayerHand"): 2, sym("wDuelTempList"): 4}},
    ],
    # Color index -> $80 >> index.
    "TranslateColorToWR": [
        {"a": 0},
        {"a": 3},
        {"a": 7},
        dict(POISON, a=5),
    ],
    # Count cards in location $10 (play area) with id $01; entry hl = $C200 page.
    "CountCardIDInLocation": [
        {"b": 0x10, "e": 0x01, "hl": sym("wPlayerCardLocations"),
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02\x01",
                  sym("wPlayerCardLocations"): b"\x10\x00\x10"}},
        {"b": 0x10, "e": 0x02, "hl": sym("wPlayerCardLocations"),
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02",
                  sym("wPlayerCardLocations"): b"\x10\x00"}},
        dict(POISON, b=0x10, e=0x01, hl=sym("wPlayerCardLocations"),
             wram={hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x01\x01",
                   sym("wPlayerCardLocations"): b"\x10\x10\x00"}),
        # ai-duel-12 33860: entry hl carries a non-zero low byte, which `ld l` discards,
        # so the walk starts at the page's card-location block either way.
        {"b": 0x10, "e": 0x01, "hl": sym("wPlayerCardLocations") + 0x10,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02\x01",
                  sym("wPlayerCardLocations"): b"\x10\x00\x10"}},
        dict(_count_card_id_fixture(vram=False), **_COUNT_CARD_ID_REGS),
    ],
    # Attack flag: a = group<<3 | bit. wLoadedAttackFlag1 = $CCB4.
    "CheckLoadedAttackFlag": [
        {"a": 0x00, "wram": {sym("wLoadedAttackFlag1"): b"\x01"}},
        {"a": 0x03, "wram": {sym("wLoadedAttackFlag1"): b"\x08"}},
        {"a": 0x08, "wram": {sym("wLoadedAttackFlag2"): b"\x02"}},
        {"a": 0x02, "wram": {sym("wLoadedAttackFlag1"): b"\x00"}},
        dict(POISON, a=0x10, wram={sym("wLoadedAttackFlag3"): b"\x80"}),
    ],
    # Arena slot 0: deck index at $C2BB, damage at $C2C8. Deck card $01 loads
    # with max HP $C9 (verified against the ROM).
    "GetCardDamageAndMaxHP": [
        {"e": 0, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): b"\x00",
                          wPlayerDeck: b"\x01"}},
        {"e": 0, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): b"\x05",
                          wPlayerDeck: b"\x01"}},
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench1CardHP"): b"\x00",
                          wPlayerDeck: b"\x01"}},
        # Damage above max HP: full-byte borrow sets C (nibble 9-0 does not set H).
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench1CardHP"): b"\xD0",
                          wPlayerDeck: b"\x01"}},
        # Low-nibble borrow only: H without C.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench1CardHP"): b"\x3A",
                          wPlayerDeck: b"\x01"}},
        # Damage exactly at max HP ($71 for the loaded card): zero, no borrow.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench1CardHP"): b"\x71",
                          wPlayerDeck: b"\x01"}},
        # Damage above max HP with nibble borrow: H and C both.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench"): b"\x00", sym("wPlayerBench1CardHP"): b"\xC9",
                          wPlayerDeck: b"\x01"}},
    ],
    "CopyDeckData": [
        {"d": 0xC1, "e": 0x00, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC2", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x41\x42"},
         "read": {wPlayerDeck: 60, sym("wDeckName"): 2}},
        {"d": 0xC1, "e": 0x50, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC3", sym("wDecompressionSecondaryBufferStart") + 0x61: b"\x02\x05\x00\x10\x20"},
         "read": {wOpponentDeck: 60, sym("wDeckName"): 2}},
        # Exactly DECK_SIZE cards -> last slot becomes nonzero -> carry clear.
        {"d": 0xC1, "e": 0x00, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC2", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x3c\x07\x00\x30\x40"},
         "read": {wPlayerDeck: 60, sym("wDeckName"): 2}},
        # Empty description: c passes through untouched.
        dict(POISON, d=0xC1, e=0x00,
             wram={hWhoseTurn: b"\xC2", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x50\x60"},
             read={wPlayerDeck: 60, sym("wDeckName"): 2}),
    ],
    "CountPrizes": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\x00"}},
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\x3f"}},
        {"wram": {hWhoseTurn: b"\xC3", sym("wOpponentPrizes"): b"\x07"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\xAA"}),
    ],
    "ShuffleDeck": [
        {"c": 0, "e": 0, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x00"},
         "read": {sym("wPlayerDeckCards"): 60}},
        {"c": 0, "e": 0,
         "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x3c", sym("wRNG1"): b"\x11\x22\x33",
                  sym("wPlayerDeckCards"): b"\x01\x02\x03\x04"},
         "read": {sym("wPlayerDeckCards"): 4}},
        dict(POISON, c=0xCC, e=0xEE,
             wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsNotInDeck"): b"\x05", sym("wRNG1"): b"\x00\x00\x00"},
             read={sym("wOpponentDeckCards"): 60}),
    ],
    "DrawCardFromDeck": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x00", sym("wPlayerDeckCards"): b"\x08"},
         "read": {sym("wPlayerNumberOfCardsNotInDeck"): 1, sym("wPlayerCardLocations"): 1}},
        {"wram": {hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsNotInDeck"): b"\x3c"}, "read": {sym("wOpponentNumberOfCardsNotInDeck"): 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x00", sym("wPlayerDeckCards"): b"\x00"},
             read={sym("wPlayerNumberOfCardsNotInDeck"): 1, sym("wPlayerCardLocations"): 1}),
    ],
    "ReturnCardToDeck": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x01"},
         "read": {sym("wPlayerNumberOfCardsNotInDeck"): 1, sym("wPlayerDeckCards"): 1, sym("wPlayerCardLocations"): 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsNotInDeck"): b"\x0a"},
             read={sym("wOpponentNumberOfCardsNotInDeck"): 1, sym("wPlayerDeckCards") + 5 + 0x100: 1}),
    ],
    "SearchCardInDeckAndAddToHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsNotInDeck"): b"\x00",
                              sym("wPlayerDeckCards"): b"\x01\x02\x03"},
         "read": {sym("wPlayerNumberOfCardsNotInDeck"): 1, sym("wPlayerCardLocations") + 2: 1, sym("wPlayerDeckCards"): 3}},
        dict(POISON, a=0x00, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsNotInDeck"): b"\x02",
                                   sym("wOpponentDeckCards") + 2: b"\x01\x02\x03"},
             read={sym("wOpponentNumberOfCardsNotInDeck"): 1, sym("wOpponentDeckCards") + 2: 1, sym("wOpponentCardLocations"): 1}),
    ],
    "AddCardToHand": [
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00"},
         "read": {sym("wPlayerCardLocations"): 1, sym("wPlayerNumberOfCardsInHand"): 1, sym("wPlayerHand"): 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInHand"): b"\x02"},
             read={sym("wOpponentCardLocations") + 5: 1, sym("wOpponentNumberOfCardsInHand"): 1, sym("wOpponentHand") + 2: 1}),
    ],
    "RemoveCardFromHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x03",
                              sym("wPlayerHand"): b"\x01\x02\x03"},
         "read": {sym("wPlayerNumberOfCardsInHand"): 1, sym("wPlayerHand"): 3}},
        {"a": 0x09, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00"},
         "read": {sym("wPlayerNumberOfCardsInHand"): 1}},
        dict(POISON, a=0x01, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInHand"): b"\x02",
                                   sym("wOpponentHand"): b"\x01\x01"},
             read={sym("wOpponentNumberOfCardsInHand"): 1, sym("wOpponentHand"): 2}),
    ],
    "PutCardInDiscardPile": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00"},
         "read": {sym("wPlayerCardLocations"): 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1, sym("wPlayerDeckCards"): 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x02"},
             read={sym("wOpponentCardLocations") + 5: 1, sym("wOpponentNumberOfCardsInDiscardPile"): 1, sym("wOpponentDeckCards") + 2: 1}),
    ],
    "MoveHandCardToDiscardPile": [
        # Card is in hand (masked location == CARD_LOCATION_HAND): moved.
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations") + 3: b"\x01",
                              sym("wPlayerNumberOfCardsInHand"): b"\x01", sym("wPlayerHand"): b"\x03"},
         "read": {sym("wPlayerCardLocations") + 3: 1, sym("wPlayerNumberOfCardsInHand"): 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1}},
        # Card not in hand (in deck): early return.
        {"a": 0x04, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations") + 4: b"\x00"},
         "read": {sym("wPlayerCardLocations") + 4: 1}},
        dict(POISON, a=0x07, wram={hWhoseTurn: b"\xC3", sym("wOpponentCardLocations") + 7: b"\x02"},
             read={sym("wOpponentCardLocations") + 7: 1}),
    ],
    "MoveDiscardPileCardToHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02",
                              sym("wPlayerDeckCards"): b"\x01\x02"},
         "read": {sym("wPlayerCardLocations") + 2: 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1, sym("wPlayerDeckCards"): 2}},
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00"},
         "read": {sym("wPlayerCardLocations"): 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1}},
        # Searched card not present: the scan's last `cp` compares against a
        # higher id, distinguishing the carry-flag's < vs > direction.
        {"a": 0x09, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02",
                              sym("wPlayerDeckCards"): b"\x01\x02"},
         "read": {sym("wPlayerCardLocations") + 9: 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1, sym("wPlayerDeckCards"): 2}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x01",
                                   sym("wOpponentDeckCards"): b"\x05"},
             read={sym("wOpponentCardLocations") + 5: 1, sym("wOpponentNumberOfCardsInDiscardPile"): 1, sym("wOpponentDeckCards"): 1}),
    ],
    "CheckPrizeTaken": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\x01"}},
        {"a": 3, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\x04"}},
        {"a": 7, "wram": {hWhoseTurn: b"\xC3", sym("wOpponentPrizes"): b"\x80"}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC2", sym("wPlayerPrizes"): b"\x00"}),
    ],
    "SortCardsInListByID_CheckForListTerminator": [
        {"wram": {hWhoseTurn: b"\xC2", sym("hTempListPtr_ff99"): sym_pointer("wDuelTempList"),
                  sym("wDuelTempList"): b"\x02\x01\x00\xff", **deck_entry(0, 3, wPlayerDeck), **deck_entry(1, 2, wPlayerDeck), **deck_entry(2, 1, wPlayerDeck)},
         "read": {sym("wDuelTempList"): 4, sym("hTempListPtr_ff99"): 2}},
        {"wram": {hWhoseTurn: b"\xC2", sym("hTempListPtr_ff99"): sym_pointer("wNameBuffer"),
                  sym("wNameBuffer"): b"\xff"}, "read": {sym("hTempListPtr_ff99"): 2}},
        # Poisoned b/c must survive an immediate (empty-list) terminator hit
        # unchanged -- this is the only branch where they're real pass-through
        # inputs rather than loop-derived outputs. f=0 (not full POISON):
        # SortCardsInListByID's shared `bit 7,[hl]` terminator check never
        # touches carry, but the shared C hardcodes f=$20 (C=0) on this
        # branch, so poisoning entry carry would fail through code this
        # routine doesn't own.
        dict(POISON, f=0x00, wram={hWhoseTurn: b"\xC3", sym("hTempListPtr_ff99"): sym_pointer("wNameBuffer"),
                           sym("wNameBuffer"): b"\xff"}, read={sym("hTempListPtr_ff99"): 2}),
    ],
    "CheckIfCanEvolveInto": [
        # card 9 (stage1) evolves from card 8 (basic) currently in play: eligible.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardFlags"): b"\x80"}},
        # Not eligible this turn (CAN_EVOLVE_THIS_TURN flag clear).
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardFlags"): b"\x00"}},
        # Unrelated cards: name mismatch.
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                   sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardFlags"): b"\x80"}),
    ],
    "CheckIfCanEvolveInto_BasicToStage2": [
        # card 10 (stage2) evolves from card 8 (basic) via card 9 (stage1) by name.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x0a",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardFlags"): b"\x80"}},
        # Flag clear: not eligible.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x0a",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardFlags"): b"\x00"}},
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                   sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardFlags"): b"\x80"}),
    ],
    "EvolvePokemonCardIfPossible": [
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardFlags"): b"\x80", sym("wPlayerArenaCardHP"): b"\x0a",
                  sym("hTempCardIndex_ff98"): b"\x01", sym("hTempPlayAreaLocation_ff9d"): b"\x00"},
         "read": {sym("wPlayerArenaCard"): 1, sym("wPlayerArenaCardHP"): 1, sym("wPlayerArenaCardFlags"): 1, sym("wPlayerArenaCardStage"): 1, sym("wPreEvolutionPokemonCard"): 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                           sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardFlags"): b"\x00",
                           sym("hTempCardIndex_ff98"): b"\x01", sym("hTempPlayAreaLocation_ff9d"): b"\x00"},
             read={sym("wOpponentArenaCard"): 1}),
    ],
    "EvolvePokemonCard": [
        # The practice-duel state (tests/cases/_fixtures.py): Seaking (deck
        # card 3, in hand) onto the arena Goldeen (card 6). Card 3 leaves the
        # hand for CARD_LOCATION_ARENA, the hand list and count shrink, the
        # arena card index, HP difference, flags and stage are rewritten.
        dict(_attack_fixture(vram=False, changes={sym("hTempCardIndex_ff98"): b"\x03", sym("hTempPlayAreaLocation_ff9d"): b"\x00"}), **_ATTACK_REGS),
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): b"\x0a",
                  sym("hTempCardIndex_ff98"): b"\x01", sym("hTempPlayAreaLocation_ff9d"): b"\x00"},
         "read": {sym("wPlayerArenaCard"): 1, sym("wPlayerArenaCardHP"): 1, sym("wPlayerArenaCardFlags"): 1, sym("wPlayerArenaCardStage"): 1, sym("wPreEvolutionPokemonCard"): 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                           sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardHP"): b"\x05",
                           sym("hTempCardIndex_ff98"): b"\x00", sym("hTempPlayAreaLocation_ff9d"): b"\x01"},
             read={sym("wOpponentBench"): 1, sym("wOpponentBench1CardHP"): 1, sym("wOpponentBench1CardStage"): 1}),
    ],
    "ClearAllStatusConditions": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wPlayerArenaCardStatus"): b"\x05", sym("wPlayerArenaCardSubstatus1"): b"\x01",
                  sym("wPlayerArenaCardSubstatus2"): b"\x02", sym("wPlayerArenaCardSubstatus3"): b"\x03", sym("wPlayerArenaCardDisabledAttackIndex"): b"\xff\xff\xff\xff\xff\xff\xff\xff"},
         "read": {sym("wPlayerArenaCardStatus"): 1, sym("wPlayerArenaCardSubstatus1"): 1, sym("wPlayerArenaCardSubstatus2"): 1, sym("wPlayerArenaCardChangedWeakness"): 1, sym("wPlayerArenaCardChangedResistance"): 1, sym("wPlayerArenaCardSubstatus3"): 1,
                  sym("wPlayerArenaCardDisabledAttackIndex"): 8}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", sym("wOpponentArenaCardStatus"): b"\x07", sym("wOpponentArenaCardSubstatus3"): b"\x03"},
             read={sym("wOpponentArenaCardStatus"): 1, sym("wOpponentArenaCardSubstatus3"): 1, sym("wOpponentArenaCardDisabledAttackIndex"): 8}),
    ],
    "PutHandCardInPlayArea": [
        {"a": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x01",
                                        sym("wPlayerHand"): b"\x00"},
         "read": {sym("wPlayerCardLocations"): 1, sym("wPlayerNumberOfCardsInHand"): 1}},
        dict(POISON, a=0x02, e=0x03,
             wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfCardsInHand"): b"\x01", sym("wOpponentHand"): b"\x02"},
             read={sym("wOpponentCardLocations") + 2: 1, sym("wOpponentNumberOfCardsInHand"): 1}),
    ],
    "PutHandPokemonCardInPlayArea": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x00",
                             sym("wPlayerNumberOfCardsInHand"): b"\x01", sym("wPlayerHand"): b"\x00", wPlayerDeck: b"\x08"},
         "read": {sym("wPlayerNumberOfPokemonInPlayArea"): 1, sym("wPlayerArenaCard"): 1, sym("wPlayerArenaCardHP"): 1, sym("wPlayerArenaCardStage"): 1, sym("wPlayerArenaCardFlags"): 1, sym("wPlayerArenaCardChangedType"): 1,
                  sym("wPlayerArenaCardAttachedPlusPower"): 1, sym("wPlayerArenaCardAttachedDefender"): 1, sym("wPlayerArenaCardStatus"): 1}},
        # Play area already full: carry set, echoes input a.
        {"a": 0x05, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x06"},
         "read": {sym("wPlayerNumberOfPokemonInPlayArea"): 1}},
        dict(POISON, a=0x00, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x02",
                                   sym("wOpponentNumberOfCardsInHand"): b"\x01", sym("wOpponentHand"): b"\x00",
                                   wOpponentDeck: b"\x08"},
             read={sym("wOpponentNumberOfPokemonInPlayArea"): 1, sym("wOpponentBench") + 1: 1}),
    ],
    "EmptyPlayAreaSlot.init_duelvar": [
        {"a": 0xBB, "d": 0xFF, "e": 0x00, "hl": sym("wPlayerCardLocations"), "wram": {sym("wPlayerArenaCard"): b"\x00"},
         "read": {sym("wPlayerArenaCard"): 1}},
        {"a": 0xC8, "d": 0x00, "e": 0x03, "hl": sym("wPlayerCardLocations"), "wram": {sym("wPlayerBench3CardHP"): b"\x77"},
         "read": {sym("wPlayerBench3CardHP"): 1}},
        dict(POISON, a=0xE0, d=0x00, e=0x05, hl=sym("wOpponentCardLocations"), wram={sym("wOpponentBench5CardAttachedPlusPower"): b"\x42"},
             read={sym("wOpponentBench5CardAttachedPlusPower"): 1}),

        dict(_init_duelvar_fixture(vram=False), **_INIT_DUELVAR_REGS, read={sym("wOpponentBench1CardHP"): 1}),
    ],
    "SwapPlayAreaPokemon.swap_duelvar": [
        {"a": 0xBB, "b": 0xC2, "d": 0x00, "e": 0x01, "hl": sym("wPlayerCardLocations"),
         "wram": {sym("wPlayerArenaCard"): b"\x01\x02"}, "read": {sym("wPlayerArenaCard"): 2}},
        {"a": 0xC8, "b": 0xC2, "d": 0x02, "e": 0x04, "hl": sym("wPlayerCardLocations"),
         "wram": {sym("wPlayerBench2CardHP"): b"\x10", sym("wPlayerBench4CardHP"): b"\x20"}, "read": {sym("wPlayerBench2CardHP"): 3}},
        dict(POISON, a=0xBB, b=0xC3, d=0x01, e=0x00, hl=sym("wOpponentCardLocations"),
             wram={sym("wOpponentArenaCard"): b"\x05\x06"}, read={sym("wOpponentArenaCard"): 2}),

        dict(_swap_duelvar_fixture(vram=False), **_SWAP_DUELVAR_REGS, read={sym("wOpponentArenaCard"): 2}),
    ],
    "EmptyPlayAreaSlot": [
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2"},
         "read": {sym("wPlayerArenaCard"): 1, sym("wPlayerArenaCardHP"): 1, sym("wPlayerArenaCardStage"): 1, sym("wPlayerArenaCardChangedType"): 1, sym("wPlayerArenaCardAttachedDefender"): 1, sym("wPlayerArenaCardAttachedPlusPower"): 1}},
        dict(POISON, e=0x05, wram={hWhoseTurn: b"\xC3"},
             read={sym("wOpponentBench") + 4: 1, sym("wOpponentBench5CardHP"): 1, sym("wOpponentBench5CardStage"): 1, sym("wOpponentBench5CardChangedType"): 1, sym("wOpponentBench5CardAttachedDefender"): 1, sym("wOpponentBench5CardAttachedPlusPower"): 1}),
    ],
    "MovePlayAreaCardToDiscardPile": [
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01",
                             sym("wPlayerCardLocations"): b"\x10", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00"},
         "read": {sym("wPlayerNumberOfPokemonInPlayArea"): 1, sym("wPlayerCardLocations"): 1, sym("wPlayerNumberOfCardsInDiscardPile"): 1, sym("wPlayerDeckCards"): 1}},
        dict(POISON, e=0x01, wram={hWhoseTurn: b"\xC3", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x02",
                                   sym("wOpponentCardLocations") + 1: b"\x11", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
             read={sym("wOpponentNumberOfPokemonInPlayArea"): 1, sym("wOpponentCardLocations") + 1: 1, sym("wOpponentNumberOfCardsInDiscardPile"): 1}),
    ],
    "SwapPlayAreaPokemon": [
        {"d": 0x00, "e": 0x01,
         "wram": {hWhoseTurn: b"\xC2", sym("wPlayerArenaCard"): b"\x01", sym("wPlayerBench"): b"\x02",
                  sym("wPlayerCardLocations"): b"\x10", sym("wPlayerCardLocations") + 1: b"\x11"},
         "read": {sym("wPlayerArenaCard"): 1, sym("wPlayerBench"): 1, sym("wPlayerCardLocations"): 1, sym("wPlayerCardLocations") + 1: 1}},
        # d == e: no-op.
        {"d": 0x02, "e": 0x02, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench") + 1: b"\x03"},
         "read": {sym("wPlayerBench") + 1: 1}},
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", sym("wOpponentArenaCard"): b"\x05", sym("wOpponentBench"): b"\x06",
                   sym("wOpponentCardLocations"): b"\x10", sym("wOpponentCardLocations") + 1: b"\x11"},
             read={sym("wOpponentArenaCard"): 1, sym("wOpponentBench"): 1, sym("wOpponentCardLocations"): 1, sym("wOpponentCardLocations") + 1: 1}),
    ],
    "SwapArenaWithBenchPokemon": [
        {"e": 0x01, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerArenaCard"): b"\x01", sym("wPlayerBench"): b"\x02",
                             sym("wPlayerCardLocations"): b"\x10", sym("wPlayerCardLocations") + 1: b"\x11", sym("wPlayerArenaCardStatus"): b"\x05"},
         "read": {sym("wPlayerArenaCard"): 1, sym("wPlayerBench"): 1, sym("wPlayerArenaCardStatus"): 1}},
        dict(POISON, e=0x00, wram={hWhoseTurn: b"\xC3", sym("wOpponentArenaCard"): b"\x07", sym("wOpponentArenaCardStatus"): b"\x02"},
             read={sym("wOpponentArenaCard"): 1, sym("wOpponentArenaCardStatus"): 1}),
    ],
    "ShiftTurnPokemonToFirstPlayAreaSlots": [
        {"wram": {hWhoseTurn: b"\xC2",
                  sym("wPlayerArenaCard"): b"\xff", sym("wPlayerBench"): b"\x02", sym("wPlayerBench") + 1: b"\xff",
                  sym("wPlayerBench") + 2: b"\x03", sym("wPlayerBench") + 3: b"\xff", sym("wPlayerBench") + 4: b"\xff",
                  sym("wPlayerCardLocations") + 2: b"\x11", sym("wPlayerCardLocations") + 3: b"\x12"},
         "read": {sym("wPlayerArenaCard"): 6, sym("wPlayerCardLocations"): 5}},
        {"wram": {hWhoseTurn: b"\xC3",
                  sym("wOpponentArenaCard"): b"\xff", sym("wOpponentBench"): b"\xff", sym("wOpponentBench") + 1: b"\xff",
                  sym("wOpponentBench") + 2: b"\xff", sym("wOpponentBench") + 3: b"\xff", sym("wOpponentBench") + 4: b"\xff"},
         "read": {sym("wOpponentArenaCard"): 6}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           sym("wPlayerArenaCard"): b"\xff", sym("wPlayerBench"): b"\xff", sym("wPlayerBench") + 1: b"\xff",
                           sym("wPlayerBench") + 2: b"\xff", sym("wPlayerBench") + 3: b"\xff", sym("wPlayerBench") + 4: b"\xff"},
             read={sym("wPlayerArenaCard"): 6}),
    ],
    "ShiftAllPokemonToFirstPlayAreaSlots": [
        {"wram": {hWhoseTurn: b"\xC2",
                  sym("wPlayerArenaCard"): b"\xff", sym("wPlayerBench"): b"\x02", sym("wPlayerBench") + 1: b"\xff",
                  sym("wPlayerBench") + 2: b"\xff", sym("wPlayerBench") + 3: b"\xff", sym("wPlayerBench") + 4: b"\xff",
                  sym("wOpponentArenaCard"): b"\xff", sym("wOpponentBench"): b"\xff", sym("wOpponentBench") + 1: b"\xff",
                  sym("wOpponentBench") + 2: b"\xff", sym("wOpponentBench") + 3: b"\xff", sym("wOpponentBench") + 4: b"\xff",
                  sym("wPlayerCardLocations") + 2: b"\x11"},
         "read": {sym("wPlayerArenaCard"): 6, sym("wOpponentArenaCard"): 6, hWhoseTurn: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3",
                           sym("wPlayerArenaCard"): b"\xff", sym("wPlayerBench"): b"\xff", sym("wPlayerBench") + 1: b"\xff",
                           sym("wPlayerBench") + 2: b"\xff", sym("wPlayerBench") + 3: b"\xff", sym("wPlayerBench") + 4: b"\xff",
                           sym("wOpponentArenaCard"): b"\xff", sym("wOpponentBench"): b"\xff", sym("wOpponentBench") + 1: b"\xff",
                           sym("wOpponentBench") + 2: b"\xff", sym("wOpponentBench") + 3: b"\xff", sym("wOpponentBench") + 4: b"\xff"},
             read={sym("wPlayerArenaCard"): 6, sym("wOpponentArenaCard"): 6, hWhoseTurn: 1}),
    ],
    "GetPlayAreaCardAttachedEnergies": [
        # Slot 0 (arena): deck index 0 -> card id 1 (GRASS_ENERGY, energy).
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x10",
                             wPlayerDeck: b"\x01"},
         "read": {sym("wAttachedEnergies"): 8, sym("wTotalAttachedEnergies"): 1}},
        {"e": 0x01, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x00"},
         "read": {sym("wAttachedEnergies"): 8, sym("wTotalAttachedEnergies"): 1}},
        dict(POISON, e=0x00, wram={hWhoseTurn: b"\xC3", sym("wOpponentCardLocations"): b"\x10",
                                   wOpponentDeck: b"\x01"},
             read={sym("wAttachedEnergies"): 8, sym("wTotalAttachedEnergies"): 1}),
    ],
    "CopyAttackDataAndDamage": [
        {"e": 0, "wram": {sym("wLoadedCard1ID"): b"\x08", sym("wLoadedCard1Atk1"): b"\x01" * 0x13},
         "read": {sym("wTempCardID_ccc2"): 1, sym("wLoadedAttack"): 0x13, sym("wDamage"): 2, sym("wNoDamageOrEffect"): 1, sym("wDealtDamage"): 2}},
        {"e": 1, "wram": {sym("wLoadedCard1ID"): b"\x09", sym("wLoadedCard1Atk2"): b"\x02" * 0x13},
         "read": {sym("wTempCardID_ccc2"): 1, sym("wLoadedAttack"): 0x13, sym("wDamage"): 2, sym("wNoDamageOrEffect"): 1, sym("wDealtDamage"): 2}},
        dict(POISON, e=0, wram={sym("wLoadedCard1ID"): b"\x0a", sym("wLoadedCard1Atk1"): b"\x03" * 0x13},
             read={sym("wTempCardID_ccc2"): 1, sym("wLoadedAttack"): 0x13}),
    ],
    "CopyAttackDataAndDamage_FromDeckIndex": [
        {"d": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08"},
         "read": {sym("hTempCardIndex_ff9f"): 1, sym("wSelectedAttack"): 1, sym("wTempCardID_ccc2"): 1, sym("wLoadedAttack"): 0x13}},
        dict(POISON, d=0x00, e=0x01, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x09"},
             read={sym("hTempCardIndex_ff9f"): 1, sym("wSelectedAttack"): 1, sym("wTempCardID_ccc2"): 1}),
    ],
    "CopyAttackDataAndDamage_FromCardID": [
        {"a": 0x08, "d": 0x00, "e": 0x00,
         "read": {sym("hTempCardIndex_ff9f"): 1, sym("wSelectedAttack"): 1, sym("wTempCardID_ccc2"): 1, sym("wLoadedAttack"): 0x13}},
        dict(POISON, a=0x09, d=0x00, e=0x01,
             read={sym("hTempCardIndex_ff9f"): 1, sym("wSelectedAttack"): 1, sym("wTempCardID_ccc2"): 1}),
    ],
    "ReturnCarry": [
        {"f": 0x00},
        {"f": 0x80},
        dict(POISON),
    ],
    "LoadNonPokemonCardEffectCommands": [
        {"wram": {sym("hTempCardIndex_ff9f"): b"\x00", wPlayerDeck: b"\x08"},
         "read": {sym("wLoadedAttackEffectCommands"): 2}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", sym("hTempCardIndex_ff9f"): b"\x00",
                           wOpponentDeck: b"\x09"},
             read={sym("wLoadedAttackEffectCommands"): 2}),
    ],
    "ApplyAttachedPlusPower": [
        {"b": 0x10, "d": 0x00, "e": 0x0a,
         "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x10\x10",
                  wPlayerDeck: b"\xd8\xd8"},
         "read": {sym("wPlayerCardLocations"): 2}},
        dict(POISON, b=0x10, d=0x00, e=0x00,
             wram={hWhoseTurn: b"\xC3", sym("wOpponentCardLocations"): b"\x00"}),
    ],
    "ApplyAttachedDefender": [
        {"b": 0x10, "d": 0x00, "e": 0x64,
         "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x10",
                  wPlayerDeck: b"\xd9"},
         "read": {sym("wPlayerCardLocations"): 1}},
        dict(POISON, b=0x10, d=0x00, e=0x00,
             wram={hWhoseTurn: b"\xC3", sym("wOpponentCardLocations"): b"\x00"}),
    ],
    "MoveCardToDiscardPileIfInPlayArea": [
        {"d": 0x00, "e": 0xd8, "hl": sym("wPlayerCardLocations"),
         "wram": {hWhoseTurn: b"\xC2", sym("wPlayerCardLocations"): b"\x10\x00",
                  wPlayerDeck: b"\xd8\x01"},
         "read": {sym("wPlayerCardLocations"): 2, sym("wPlayerNumberOfCardsInDiscardPile"): 1}},
        dict(POISON, d=0x00, e=0x00, hl=sym("wOpponentCardLocations"),
             wram={hWhoseTurn: b"\xC3", sym("wOpponentCardLocations"): b"\x00"}),
    ],
    "ApplyDamageModifiers_DamageToTarget": [
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x00\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wOpponentArenaCardChangedWeakness"): b"\x80", sym("wOpponentArenaCardChangedResistance"): b"\x80",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wOpponentArenaCardChangedWeakness"): b"\x40", sym("wOpponentArenaCardChangedResistance"): b"\x80",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x28\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wOpponentArenaCardChangedWeakness"): b"\x80", sym("wOpponentArenaCardChangedResistance"): b"\x40",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x14\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wOpponentArenaCardChangedWeakness"): b"\x80", sym("wOpponentArenaCardChangedResistance"): b"\x40",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x80",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           wDamage_ADDR: b"\x14\x00",
                           sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                           sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
                           sym("wPlayerArenaCardChangedType"): b"\x00",
                           sym("wOpponentArenaCardChangedWeakness"): b"\x80", sym("wOpponentArenaCardChangedResistance"): b"\x80",
                           sym("wPlayerArenaCardStatus"): b"\x00"},
             read={wDamageEffectiveness_ADDR: 1}),
    ],
    "ApplyDamageModifiers_DamageToSelf": [
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x00\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wPlayerArenaCardChangedWeakness"): b"\x80", sym("wPlayerArenaCardChangedResistance"): b"\x80",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wPlayerArenaCardChangedWeakness"): b"\x40", sym("wPlayerArenaCardChangedResistance"): b"\x80",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x28\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wPlayerArenaCardChangedWeakness"): b"\x80", sym("wPlayerArenaCardChangedResistance"): b"\x40",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x14\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerArenaCardChangedType"): b"\x00",
                  sym("wPlayerArenaCardChangedWeakness"): b"\x80", sym("wPlayerArenaCardChangedResistance"): b"\x40",
                  sym("wPlayerArenaCardStatus"): b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           wDamage_ADDR: b"\x14\x00",
                           sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                           sym("wPlayerArenaCardChangedType"): b"\x00",
                           sym("wPlayerArenaCardChangedWeakness"): b"\x80", sym("wPlayerArenaCardChangedResistance"): b"\x80",
                           sym("wPlayerArenaCardStatus"): b"\x00"},
             read={wDamageEffectiveness_ADDR: 1}),
    ],
    "GetPlayAreaCardRetreatCost": [
        {"wram": {hWhoseTurn: b"\xC2",
                  sym("hTempPlayAreaLocation_ff9d"): b"\x00",
                  sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                  sym("wPlayerBench") + 5: b"\xFF"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           sym("hTempPlayAreaLocation_ff9d"): b"\x00",
                           sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                           sym("wPlayerBench") + 5: b"\xFF"}),
    ],
}

HP_ADDR = sym("wPlayerArenaCardHP")  # player page (0xC2) + DUELVARS_ARENA_CARD_HP (0xC8)
CASES.update({
    "PrintPlayAreaCardKnockedOutIfNoHP": [
        # HP=30 (non-zero) → early return, a=30, f=0x00 (no carry)
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", HP_ADDR: b"\x30"}},
        # HP=10, different play area location
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", sym("wPlayerBench1CardHP"): b"\x0A"}},
        # Poisoned registers, HP=50
        dict(POISON, a=2, wram={hWhoseTurn: b"\xC2", sym("wPlayerBench2CardHP"): b"\x32"}),
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", HP_ADDR: b"\x00",
                          sym("wPlayerArenaCard"): b"\x00", wPlayerDeck + 0: b"\x08",
                          sym("wTempNonTurnDuelistCardID"): b"\x08", sym("wDoFrameFunction"): sym_pointer("NoOp")},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
    "PrintKnockedOut": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wTempNonTurnDuelistCardID"): b"\x08", sym("wDoFrameFunction"): sym_pointer("NoOp")},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
    "DrawWideTextBox_WaitForInput_ReturnCarry": [
        {"hl": 0, "keys": 0x01,
         "wram": {sym("wCurDeckCardChanges"): b"\x00"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    ],
})
CASES.update({
    "UpdateArenaCardIDsAndClearTwoTurnDuelVars": [
        {"wram": {
            hWhoseTurn: b"\xC2",
            sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x01",
            wPlayerDeck: b"\x12", wOpponentDeck + 1: b"\x34",
            wTempTurnDuelistCardID: b"\xFF", wTempNonTurnDuelistCardID: b"\xFF",
            wSentAttackDataToLinkOpponent: b"\xFF",
            wStatusConditionQueueIndex: b"\xFF",
            wEffectFailed: b"\xFF",
            wIsDamageToSelf: b"\xFF", wDefendingWasForcedToSwitch: b"\xFF",
            wMetronomeEnergyCost: b"\xFF", wNoEffectFromWhichStatus: b"\xFF",
            sym("wOpponentArenaCardDisabledAttackIndex"): b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"},
         "read": {sym("wTempTurnDuelistCardID"): 1, sym("wTempNonTurnDuelistCardID"): 1, sym("hTempCardIndex_ff9f"): 1,
                  wSentAttackDataToLinkOpponent: 1, wStatusConditionQueueIndex: 1,
                  wEffectFailed: 1, wIsDamageToSelf: 1, wDefendingWasForcedToSwitch: 1,
                  wMetronomeEnergyCost: 1, wNoEffectFromWhichStatus: 1, sym("wOpponentArenaCardDisabledAttackIndex"): 9}},
        dict(POISON, wram={
            hWhoseTurn: b"\xC2", sym("wPlayerArenaCard"): b"\x02", sym("wOpponentArenaCard"): b"\x03",
            wPlayerDeck + 2: b"\x56", wOpponentDeck + 3: b"\x78",
            sym("wOpponentArenaCardDisabledAttackIndex"): b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA"},
             read={sym("wTempTurnDuelistCardID"): 1, sym("wTempNonTurnDuelistCardID"): 1, sym("hTempCardIndex_ff9f"): 1, sym("wOpponentArenaCardDisabledAttackIndex"): 9}),
        {"a": 0x01, "f": 0xF0, "b": 0x10, "c": 0x20, "d": 0x30,
         "e": 0x40, "hl": sym("wDecompressionSecondaryBufferStart") + 0x110,
         "wram": {hWhoseTurn: b"\xC3", sym("wOpponentArenaCard"): b"\x3A",
                  sym("wPlayerArenaCard"): b"\x3B", wOpponentDeck + 0x3A: b"\x9A",
                  wPlayerDeck + 0x3B: b"\x9B", sym("wPlayerArenaCardDisabledAttackIndex"): b"\xCC" * 9},
         "read": {sym("wTempTurnDuelistCardID"): 1, sym("wTempNonTurnDuelistCardID"): 1, sym("hTempCardIndex_ff9f"): 1, sym("wPlayerArenaCardDisabledAttackIndex"): 9}},
    ],
    "ClearNonTurnTemporaryDuelvars_ResetCarry": [
        {"wram": {hWhoseTurn: b"\xC2", sym("wOpponentArenaCardDisabledAttackIndex"): b"\xFF" * 8},
         "read": {sym("wOpponentArenaCardDisabledAttackIndex"): 8}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", sym("wPlayerArenaCardDisabledAttackIndex"): b"\xAA" * 8},
             read={sym("wPlayerArenaCardDisabledAttackIndex"): 8}),
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x110, "wram": {hWhoseTurn: b"\xC2", sym("wOpponentArenaCardDisabledAttackIndex"): b"\x01" * 8},
         "read": {sym("wOpponentArenaCardDisabledAttackIndex"): 8}},
    ],
    "PrintKnockedOutIfHLZero": [
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01"}},
        dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x12, wram={sym("wDecompressionSecondaryBufferStart") + 0x12: b"\x02"}),
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x110, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x110: b"\x7F"}},
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00", wTempNonTurnDuelistCardID: b"\x08",
                                sym("wDoFrameFunction"): b"\x00\x00"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
})

# >>> factory GetFirstSetPrizeCard
CONTRACT["GetFirstSetPrizeCard"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetFirstSetPrizeCard"] = [
    {},
    {"a": 1, "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\x02"}},
    {"a": 3, "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\x00"}},
    {"a": 5, "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\x01"}},
    {"a": 6, "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\x40"}},
    {"a": 8, "wram": {sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\xFF"}},
    dict(POISON, a=4, wram={sym("hWhoseTurn"): b"\xC1", sym("wDecompressionSecondaryBufferStart") + 0xFD: b"\x01"}),
]
# <<< factory GetFirstSetPrizeCard

# >>> factory DrawCheckMenuCursor_YourOrOppPlayArea
CONTRACT["DrawCheckMenuCursor_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawCheckMenuCursor_YourOrOppPlayArea"] = [
    {"a": 0, "wram": {sym("wCheckMenuCursorXPosition"): b"\x00", sym("wCheckMenuCursorYPosition"): b"\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"a": 0x5A, "wram": {sym("wCheckMenuCursorXPosition"): b"\x01", sym("wCheckMenuCursorYPosition"): b"\x02"},
     "vread": {0: {0x9800: 0x400}}},
    {"a": 0xAC, "wram": {sym("wCheckMenuCursorXPosition"): b"\x02", sym("wCheckMenuCursorYPosition"): b"\x03"},
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, a=0x33, wram={sym("wCheckMenuCursorXPosition"): b"\x01", sym("wCheckMenuCursorYPosition"): b"\x01"},
         vread={0: {0x9800: 0x400}}),
]
# <<< factory DrawCheckMenuCursor_YourOrOppPlayArea

# >>> factory ZeroObjectPositionsWithCopyToggleOn
CONTRACT["ZeroObjectPositionsWithCopyToggleOn"] = {"compare": (), "preserve": ()}
CASES["ZeroObjectPositionsWithCopyToggleOn"] = [
    {"wram": {sym("wVBlankOAMCopyToggle"): b"\x00"}, "read": {sym("wDeckToBuild"): 0xA0}},
    dict(POISON, wram={sym("wVBlankOAMCopyToggle"): b"\xFF"}, read={sym("wDeckToBuild"): 0xA0}),
]
# <<< factory ZeroObjectPositionsWithCopyToggleOn

# >>> factory YourOrOppPlayAreaScreen_HandleInput
CONTRACT["YourOrOppPlayAreaScreen_HandleInput"] = {"compare": (), "preserve": ()}
CASES["YourOrOppPlayAreaScreen_HandleInput"] = [
    {"read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x00\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x40", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x00\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x80", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x00\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x10", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x00\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x20", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    dict(POISON,
         wram={sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x02\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x05",
               sym("hDPadHeld"): b"\x40", sym("hKeysPressed"): b"\x00"},
         read={sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}),
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x03\x00\xC3\x00", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x20", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x06\x00\xC3\x05", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x10", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x06\x00\xC3\x01", sym("wDuelInitialPrizes"): b"\x02", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x10", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x06\x00\xC3\x08", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x20", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x06\x00\xC3\x00", sym("wDuelInitialPrizes"): b"\x05", sym("wCheckMenuCursorBlinkCounter"): b"\x00",
               sym("hDPadHeld"): b"\x10", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x02\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x07",
               sym("hDPadHeld"): b"\x00", sym("hKeysPressed"): b"\x01"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x02\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x07",
               sym("hDPadHeld"): b"\x00", sym("hKeysPressed"): b"\x02"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x01\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x10",
               sym("hDPadHeld"): b"\x00", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
    {"wram": {sym("wOpponentCardLocations"): b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               sym("wInPlayAreaCurPosition"): b"\x01\x00\xC3\xFF", sym("wDuelInitialPrizes"): b"\x04", sym("wCheckMenuCursorBlinkCounter"): b"\x03",
               sym("hDPadHeld"): b"\x00", sym("hKeysPressed"): b"\x00"},
     "read": {sym("wInPlayAreaCurPosition"): 1, sym("wPrizeCardCursorTemporaryPosition"): 1, sym("wCheckMenuCursorBlinkCounter"): 1}},
]
# <<< factory YourOrOppPlayAreaScreen_HandleInput

# >>> factory DrawPlayArea_BenchCards
CONTRACT["DrawPlayArea_BenchCards"] = {"compare": (), "preserve": ()}
CASES["DrawPlayArea_BenchCards"] = [
    {"vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x03",
              sym("wPlayerBench1CardStage"): b"\x00\x01\x02\x00"},
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, c=4, d=2, e=2,
         wram={sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x04",
               sym("wPlayerBench1CardStage"): b"\x02\x01\x00\x01"},
         vread={0: {0x9800: 0x400}}),
    {"c": 4, "d": 2, "e": 2,
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC3", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x03",
              sym("wPlayerBench1CardStage"): b"\x00\x01\x02\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 1, "d": 0, "e": 0,
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC2", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x04",
              sym("wPlayerBench1CardStage"): b"\x00\x01\x02\x03", sym("wConsole"): b"\x02"},
     "vread": {0: {0x9800: 0x400}, 1: {0x9800: 0x400}}},
]
# <<< factory DrawPlayArea_BenchCards

# >>> factory EraseCheckMenuCursor_YourOrOppPlayArea
CONTRACT["EraseCheckMenuCursor_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EraseCheckMenuCursor_YourOrOppPlayArea"] = [
    {"vread": {0: {0x9800: 0x400}}},
    dict(POISON, vread={0: {0x9800: 0x400}}),
    {"wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC3"},
     "vread": {0: {0x9800: 0x400}}},
]
# <<< factory EraseCheckMenuCursor_YourOrOppPlayArea

# >>> factory LoadCursorTile
CONTRACT["LoadCursorTile"] = {"compare": (), "preserve": ()}
CASES["LoadCursorTile"] = [
    {"vread": {0: {0x8000: 16}}},
    dict(POISON, vread={0: {0x8000: 16}}),
]
# <<< factory LoadCursorTile

# >>> factory Func_8bf2
CONTRACT["Func_8bf2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c",)}
CASES["Func_8bf2"] = [
    {"vread": {0: {0x9800: 1}}},
    {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "c": 0x33,
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x06\x05\x06\x06", sym("wPlayerPrizes"): b"\x01",
              sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x01"},
     "vread": {0: {0x98A6: 1, 0x98C6: 1}}},
    {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "c": 0x33,
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x06\x05", sym("wPlayerPrizes"): b"\xFF",
              sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wDuelInitialPrizes"): b"\x01", sym("wConsole"): b"\x01"},
     "vread": {0: {0x98A6: 1}}},
    {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "c": 0x33,
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x07\x05", sym("wPlayerPrizes"): b"\x00",
              sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wDuelInitialPrizes"): b"\x01", sym("wConsole"): b"\x02"},
     "vread": {0: {0x98A7: 1}, 1: {0x98A7: 1}}},
    dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x11,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x06\x05", sym("wPlayerPrizes"): b"\x0F",
               sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC2", sym("wDuelInitialPrizes"): b"\x00", sym("wConsole"): b"\x01"},
         vread={0: {0x98A6: 1}}),
]
# <<< factory Func_8bf2

# >>> factory GetDuelInitialPrizesUpperBitsSet
CONTRACT["GetDuelInitialPrizesUpperBitsSet"] = {"compare": (), "preserve": ()}
CASES["GetDuelInitialPrizesUpperBitsSet"] = [
    {"wram": {sym("wDuelInitialPrizes"): b"\x00"}, "read": {sym("wDuelInitialPrizesUpperBitsSet"): 1}},
    dict(POISON, wram={sym("wDuelInitialPrizes"): b"\x01"}, read={sym("wDuelInitialPrizesUpperBitsSet"): 1}),
    {"wram": {sym("wDuelInitialPrizes"): b"\x02"}, "read": {sym("wDuelInitialPrizesUpperBitsSet"): 1}},
    {"wram": {sym("wDuelInitialPrizes"): b"\x06"}, "read": {sym("wDuelInitialPrizesUpperBitsSet"): 1}},
]
# <<< factory GetDuelInitialPrizesUpperBitsSet

# >>> factory DrawYourOrOppPlayArea_DrawArrows
CONTRACT["DrawYourOrOppPlayArea_DrawArrows"] = {"compare": (), "preserve": ()}
CASES["DrawYourOrOppPlayArea_DrawArrows"] = [
    {"a": 0, "b": 0x5A,
     "vread": {0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                    0x994C: 1, 0x9950: 1}}},
    {"a": 1, "b": 0x31, "vread": {0: {0x98DE: 1}}},
    {"a": 2, "b": 0x32, "vread": {0: {0x98BE: 1}}},
    {"a": 3, "b": 0x33,
     "vread": {0: {0x98E5: 1, 0x9860: 1, 0x9864: 1, 0x9868: 1,
                    0x986C: 1, 0x9870: 1}}},
    {"a": 4, "b": 0x34, "vread": {0: {0x98A0: 1}}},
    {"a": 5, "b": 0x35, "vread": {0: {0x9900: 1}}},
    dict(POISON, a=0, vread={0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                                0x994C: 1, 0x9950: 1}}),
]
# <<< factory DrawYourOrOppPlayArea_DrawArrows

# >>> factory-cases-statics
wYourOrOppPlayAreaLastCursorPosition = sym("wYourOrOppPlayAreaLastCursorPosition")

wCheckMenuCursorXPosition = sym("wCheckMenuCursorXPosition")
wCheckMenuCursorYPosition = sym("wCheckMenuCursorYPosition")
wYourOrOppPlayAreaLastCursorPosition = sym("wYourOrOppPlayAreaLastCursorPosition")

hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
hTemp_ffa0 = sym("hTemp_ffa0")
wPlayerAttackingAttackIndex = sym("wPlayerAttackingAttackIndex")
wPlayerAttackingCardIndex = sym("wPlayerAttackingCardIndex")
wSentAttackDataToLinkOpponent = sym("wSentAttackDataToLinkOpponent")

wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wConsole = sym("wConsole")
wDuelInitialPrizes = sym("wDuelInitialPrizes")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
wTileMapFill = sym("wTileMapFill")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")

wConsole = sym("wConsole")
wDecimalDigitsSymbols = sym("wDecimalDigitsSymbols")
wDefaultText = sym("wDefaultText")

hWhoseTurn = sym("hWhoseTurn")
wPlayerDeck = sym("wPlayerDeck")
wOpponentDeck = sym("wOpponentDeck")
wPlayerArenaCard = sym("wPlayerArenaCard")
wOpponentArenaCard = sym("wOpponentArenaCard")
wDuelTurns = sym("wDuelTurns")
wDuelType = sym("wDuelType")
wTempTurnDuelistCardID = sym("wTempTurnDuelistCardID")
wTempNonTurnDuelistCardID = sym("wTempNonTurnDuelistCardID")
s0a008 = sym("s0a008")
sDuelBuffer0 = sym("s0a000")
BULBASAUR = 0x08
IVYSAUR = 0x09

hDPadHeld = sym("hDPadHeld")
hKeysPressed = sym("hKeysPressed")
wMenuInputSFX = sym("wMenuInputSFX")
wCheckMenuCursorXPosition = sym("wCheckMenuCursorXPosition")
wCheckMenuCursorYPosition = sym("wCheckMenuCursorYPosition")
wCheckMenuCursorBlinkCounter = sym("wCheckMenuCursorBlinkCounter")

wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wDefaultText = sym("wDefaultText")

wDefaultText = sym("wDefaultText")

hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
wCurPlayAreaSlot = sym("wCurPlayAreaSlot")
wCurPlayAreaY = sym("wCurPlayAreaY")
wLoadedCard1Atk1Name = sym("wLoadedCard1Atk1Name")
wLoadedCard1Atk1Description = sym("wLoadedCard1Atk1Description")
hWhoseTurn = sym("hWhoseTurn")
PLAYER_TURN = 0xC2
wPlayerDeck = sym("wPlayerDeck")
wPlayerArenaCard = sym("wPlayerArenaCard")
wConsole = sym("wConsole")
wDefaultText = sym("wDefaultText")
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hWhoseTurn = sym("hWhoseTurn")
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3
wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
wIsSwapTurnPending = sym("wIsSwapTurnPending")
wDefaultText = sym("wc700") + 0x30

hWhoseTurn = sym("hWhoseTurn")
wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
wDefaultText = sym("wDefaultText")
wTileMapFill = sym("wTileMapFill")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")

wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
wIsSwapTurnPending = sym("wIsSwapTurnPending")
wMenuInputTablePointer = sym("wMenuInputTablePointer")
wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")
wYourOrOppPlayAreaCurPosition = sym("wYourOrOppPlayAreaCurPosition")
wDefaultText = sym("wDefaultText")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
wPlayerDeck = sym("wPlayerDeck")
wLoadedCard1Name = sym("wLoadedCard1Name")
wLoadedAttackName = sym("wLoadedAttackName")
wDefaultText = sym("wDefaultText")
wTxRam2 = sym("wTxRam2")
TEXT_SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wEffectFailed = sym("wEffectFailed")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wTileMapFill = sym("wTileMapFill")
wDuelDisplayedScreen = sym("wDuelDisplayedScreen")
wCheckMenuPlayAreaWhichDuelist = sym("wCheckMenuPlayAreaWhichDuelist")
wCheckMenuPlayAreaWhichLayout = sym("wCheckMenuPlayAreaWhichLayout")
hWhoseTurn = sym("hWhoseTurn")
wLCDC = sym("wLCDC")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
wDuelDisplayedScreen = sym("wDuelDisplayedScreen")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
wPlayerDeck = sym("wPlayerDeck")
wLoadedCard1Name = sym("wLoadedCard1Name")
wLoadedAttackName = sym("wLoadedAttackName")
wDefaultText = sym("wDefaultText")
wTxRam2 = sym("wTxRam2")
TEXT_SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

hTempCardIndex_ff98 = sym("hTempCardIndex_ff98")
hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
wLoadedAttackCategory = sym("wLoadedAttackCategory")
wLoadedAttackEffectCommands = sym("wLoadedAttackEffectCommands")
wLoadedCard1ID = sym("wLoadedCard1ID")
wLoadedCard1Name = sym("wLoadedCard1Name")
wLoadedAttackName = sym("wLoadedAttackName")
wTempTurnDuelistCardID = sym("wTempTurnDuelistCardID")
wTxRam2 = sym("wTxRam2")
wPlayerDeck = sym("wPlayerDeck")
wOpponentDeck = sym("wOpponentDeck")
hWhoseTurn = sym("hWhoseTurn")

wNumberOfPrizeCardsToSelect = sym("wNumberOfPrizeCardsToSelect")
wYourOrOppPlayAreaCurPosition = sym("wYourOrOppPlayAreaCurPosition")
hTemp_ffa0 = sym("hTemp_ffa0")
hTempPlayAreaLocation_ffa1 = sym("hTempPlayAreaLocation_ffa1")
hWhoseTurn = sym("hWhoseTurn")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
hTempCardIndex_ff98 = sym("hTempCardIndex_ff98")
hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
wLCDC = sym("wLCDC")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
wPlayerArenaCardStatus = sym("wPlayerArenaCardStatus")
wConfusionAttackCheckWasUnsuccessful = sym("wConfusionAttackCheckWasUnsuccessful")

wLoadedAttackCategory = sym("wLoadedAttackCategory")
wNoDamageOrEffect = sym("wNoDamageOrEffect")
wStatusConditionQueueIndex = sym("wStatusConditionQueueIndex")
wTempPlayAreaLocation_cceb = sym("wTempPlayAreaLocation_cceb")
wTempNonTurnDuelistCardID = sym("wTempNonTurnDuelistCardID")
hWhoseTurn = sym("hWhoseTurn")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = sym("hWhoseTurn")
wPlayerDuelVariables = sym("wPlayerDuelVariables")
wPlayerDeck = sym("wPlayerDeck")
wNoDamageOrEffect = sym("wNoDamageOrEffect")
wTempPlayAreaLocation_cceb = sym("wTempPlayAreaLocation_cceb")

wLoadedAttackAnimation = sym("wLoadedAttackAnimation")

# DealRecoilDamageToSelf reuses the confusion-damage fixture, but its own write
# to wLoadedAttackAnimation means the recoil animation really plays, so the
# fixture has to survive PlayAttackAnimation_DealAttackDamageSimple. Measured
# against tools/oracle/gbref/build/gbref_runner, 2026-08-26:
#   - wAnimationsDisabled ($D421) non-zero makes PlayLoadedDuelAnimation skip the
#     hit sprite and makes InitScreenAnimation skip the screen shake. Without it
#     the real ROM spends its whole budget inside bank 4 HandleAnimationFrame
#     ($4:6B39) and never returns.
#   - CopyDMAFunction is mandatory: the animation sets wVBlankOAMCopyToggle, so
#     VBlankHandler starts calling hDMAFunction, and an uncopied HRAM routine
#     derails the reference into junk (measured pc $FFC5, interrupts off).
#   - hWhoseTurn is deliberately NOT seeded. The reference leaves $FF97 holding
#     $47 once the animation's set-screen and damage-text commands have run, and
#     every seed address is implicitly compared, so the turn byte is installed by
#     a SwapTurn setup call instead: both sides start with $00 there and SwapTurn
#     maps $00 to PLAYER_TURN.
#   - wLCDC ($CABB) is not seeded either: it starts at $00 (WaitForVBlank returns
#     at once) and the animation's own EnableLCD leaves it $80, which would
#     diverge from the port.
#   - Damage stays at or below $50. With a=$AA the damage number is three digits,
#     DrawDamageAnimationNumbers then fills every damage-char slot and the
#     reference burns its budget without returning, so the poisoned case poisons
#     f/b/c/d/e/hl and keeps a at $50.
_drdts_arena_hp = sym("wPlayerArenaCardHP")
_drdts_wLoadedAttackAnimation = sym("wLoadedAttackAnimation")
_drdts_wDamage = sym("wDamage")
_drdts_wDamageEffectiveness = sym("wDamageEffectiveness")
_drdts_wTempTurn = sym("wTempTurnDuelistCardID")
_drdts_wTempNonTurn = sym("wTempNonTurnDuelistCardID")
_drdts_wNoDamageOrEffect = sym("wNoDamageOrEffect")
_drdts_wAnimationsDisabled = sym("wAnimationsDisabled")

def _drdts(**kw):
    case = {"wram": {_drdts_arena_hp: b"\x40", _drdts_wDamage: b"\x00\x00",
                     _drdts_wDamageEffectiveness: b"\x00",
                     _drdts_wTempTurn: b"\x01", _drdts_wTempNonTurn: b"\x01",
                     _drdts_wNoDamageOrEffect: b"\x00",
                     _drdts_wAnimationsDisabled: b"\x01"},
            "setup": [{"fn": "CopyDMAFunction"},
                      {"fn": "SetupText", "d": 0x30, "e": 0x7F},
                      {"fn": "SwapTurn"}],
            "instruction_budget": 8000000, "cycle_budget": 32000000,
            "read": {_drdts_arena_hp: 1, _drdts_wLoadedAttackAnimation: 1,
                     _drdts_wDamage: 2, _drdts_wDamageEffectiveness: 1,
                     _drdts_wTempNonTurn: 1, _drdts_wNoDamageOrEffect: 1}}
    case.update(kw)
    return case

# _HandlePeekSelection (engine/menus/duel.asm:1376) runs a menu, a play-area
# cursor and a card page, so it needs the frame-routine setup pair: CopyDMAFunction
# installs the HRAM DMA routine VBlankHandler calls once wVBlankOAMCopyToggle is
# set (without it the reference halts forever in WaitForVBlank at pc $0271), and
# SetupText initialises the glyph cache the text printing walks.
_hps_setup = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# Player turn; wLCDC clear so the waits before the first EnableLCD are no-ops;
# all six prizes still face down so the cursor's prize slot is selectable; prize
# card 0 is deck index 0 and that deck slot holds BULBASAUR, so a real card page
# renders and pages out under the A taps instead of running on garbage card data.
_hps_wram = {
    sym("hWhoseTurn"): b"\xC2",
    sym("wPlayerPrizeCards"): b"\x00",
    sym("wPlayerPrizes"): b"\x3F",
    sym("wBoosterCardsDrawn"): b"\x08",
    sym("wLCDC"): b"\x00",
}
# wYourOrOppPlayAreaCurPosition, wTransitionTablePtr (2), wIsSwapTurnPending and
# wce5c: exactly the bytes this routine writes itself. Nothing here is touched by
# the VBlank handler or by anything inside the card page.
_hps_read = {sym("wInPlayAreaCurPosition"): 1, sym("wMenuInputTablePointer"): 2, sym("wIsSwapTurnPending"): 1, sym("wce5c"): 1}

wce5e = sym("wce5e")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wSelectedAttack = sym("wSelectedAttack")
hTempCardIndex_ff9f = sym("hTempCardIndex_ff9f")
wTempCardID_ccc2 = sym("wTempCardID_ccc2")
wLoadedAttackCategory = sym("wLoadedAttackCategory")
wPlayerAttackingAttackIndex = sym("wPlayerAttackingAttackIndex")
wPlayerAttackingCardIndex = sym("wPlayerAttackingCardIndex")
wPlayerAttackingCardID = sym("wPlayerAttackingCardID")
wLoadedAttackEffectCommands = sym("wLoadedAttackEffectCommands")
hWhoseTurn = sym("hWhoseTurn")
wDuelType = sym("wDuelType")
wOpponentDuelVariables = sym("wOpponentDuelVariables")
# <<< factory-cases-statics

# >>> factory DrawYourOrOppPlayArea_EraseArrows
CONTRACT["DrawYourOrOppPlayArea_EraseArrows"] = {"compare": (), "preserve": ()}
CASES["DrawYourOrOppPlayArea_EraseArrows"] = [
    {"wram": {sym("wYourOrOppPlayAreaLastCursorPosition"): b"\x00"},
     "vread": {0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                    0x994C: 1, 0x9950: 1}}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD,
     "e": 0xEE, "hl": 0x1234,
     "wram": {sym("wYourOrOppPlayAreaLastCursorPosition"): b"\x00"},
     "vread": {0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                    0x994C: 1, 0x9950: 1}}},
]
# <<< factory DrawYourOrOppPlayArea_EraseArrows

# >>> factory DrawYourOrOppPlayArea_RefreshArrows
CONTRACT["DrawYourOrOppPlayArea_RefreshArrows"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawYourOrOppPlayArea_RefreshArrows"] = [
    {"a": 0x00, "wram": {wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, "read": {wYourOrOppPlayAreaLastCursorPosition: 1}},
    {"a": 0x12, "wram": {wCheckMenuCursorXPosition: b"\x01", wCheckMenuCursorYPosition: b"\x02", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, "read": {wYourOrOppPlayAreaLastCursorPosition: 1}},
    dict(POISON, a=0x01, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, read={wYourOrOppPlayAreaLastCursorPosition: 1}),
]
# <<< factory DrawYourOrOppPlayArea_RefreshArrows

# >>> factory SendAttackDataToLinkOpponent
CONTRACT["SendAttackDataToLinkOpponent"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["SendAttackDataToLinkOpponent"] = [
    {"wram": {wSentAttackDataToLinkOpponent: b"\x01", hTempCardIndex_ff9f: b"\x22", hTemp_ffa0: b"\x33"}, "read": {wSentAttackDataToLinkOpponent: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}},
    {"wram": {wSentAttackDataToLinkOpponent: b"\x00", wPlayerAttackingCardIndex: b"\x44", wPlayerAttackingAttackIndex: b"\x05", hTempCardIndex_ff9f: b"\x22", hTemp_ffa0: b"\x33"}, "read": {wSentAttackDataToLinkOpponent: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}},
    dict(POISON, wram={wSentAttackDataToLinkOpponent: b"\x00", wPlayerAttackingCardIndex: b"\x99", wPlayerAttackingAttackIndex: b"\x07", hTempCardIndex_ff9f: b"\x11", hTemp_ffa0: b"\xEE"}, read={wSentAttackDataToLinkOpponent: 1, hTempCardIndex_ff9f: 1, hTemp_ffa0: 1}),
]
# <<< factory SendAttackDataToLinkOpponent

# >>> factory DrawPlayArea_PrizeCards
CONTRACT["DrawPlayArea_PrizeCards"] = {"compare": (), "preserve": ()}
CASES["DrawPlayArea_PrizeCards"] = [
    {"hl": sym("wNameBuffer"),
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wOpponentDeck") + 0x6C: b"\x01", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x00", sym("wNameBuffer"): b"\x00\x00\x00\x02"},
     "vread": {0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}},
    {"hl": sym("wDuelTempList"),
     "wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wOpponentDeck") + 0x6C: b"\x02", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x00", sym("wDuelTempList"): b"\x00\x00\x00\x02"},
     "vread": {0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}},
    dict(POISON,
         hl=sym("wDuelTempList") + 0x10,
         wram={sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wOpponentDeck") + 0x6C: b"\x01", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x02", sym("wDuelTempList") + 0x10: b"\x00\x00\x00\x02"},
         vread={0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2},
                1: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}),
]
# <<< factory DrawPlayArea_PrizeCards

# >>> factory _DrawPlayersPrizeAndBenchCards
CONTRACT["_DrawPlayersPrizeAndBenchCards"] = {"compare": (), "preserve": ()}
# Two prizes each side (wDuelInitialPrizes $CC08, DUELVARS_PRIZES $xxEC):
# PrizeCardsCoordinateData_2 puts the player's at (6,0),(6,2) and the
# opponent's at (4,18),(4,16), 2x2 tiles each. 0xC100 seeded and diffed: the
# asm passes the table by ROM address and writes no WRAM while doing so.
CASES["_DrawPlayersPrizeAndBenchCards"] = [
    {"instruction_budget": 1000000, "cycle_budget": 4000000,
     "wram": {sym("wDuelInitialPrizes"): b"\x02", sym("wPlayerPrizes"): b"\x01", sym("wOpponentPrizes"): b"\x03", sym("wConsole"): b"\x00", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00" * 12},
     "read": {wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "vread": {0: {0x9806: 2, 0x9826: 2, 0x9846: 2, 0x9866: 2, 0x9A04: 2, 0x9A24: 2, 0x9A44: 2, 0x9A64: 2}},
     "expect": {wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}},
    dict(POISON, instruction_budget=1000000, cycle_budget=4000000,
         read={wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         expect={wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}),
]
# <<< factory _DrawPlayersPrizeAndBenchCards

# >>> factory DrawPlayArea_HandText
CONTRACT["DrawPlayArea_HandText"] = {"compare": ("b", "c", "hl"), "preserve": ("c",)}
CASES["DrawPlayArea_HandText"] = [
    {"b": 0x00, "c": 0x07, "hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer"): b"\x01\x02"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {sym("wCurDeckCardChanges"): 7, sym("wDecimalDigitsSymbols"): 2}},
    dict(POISON, b=0x00, c=0x07, hl=sym("wNameBuffer"), wram={sym("wNameBuffer"): b"\x01\x02"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={sym("wCurDeckCardChanges"): 7, sym("wDecimalDigitsSymbols"): 2}),
    {"b": 0x2D, "c": 0x11, "hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer"): b"\x03\x04"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {sym("wCurDeckCardChanges"): 7, sym("wDecimalDigitsSymbols"): 2}},
]
# <<< factory DrawPlayArea_HandText

# >>> factory DrawPlayArea_IconWithValue
CONTRACT["DrawPlayArea_IconWithValue"] = {"compare": ("hl",), "preserve": (), "wram_out": True}
CASES["DrawPlayArea_IconWithValue"] = [
    {"a": 0xD4, "b": 0x2A, "c": 0x33, "hl": sym("wNameBuffer"),
     "wram": {wConsole: b"\x00", sym("wNameBuffer"): b"\x0F\x02"},
     "read": {wDefaultText: 7, wDecimalDigitsSymbols: 2},
     "expect": {wDefaultText: b"\x05\x2D\x05\x32\x05\x20\x00", wDecimalDigitsSymbols: b"\x20\x32"}},
    dict(POISON, a=0xD8, b=0x63, hl=sym("wDuelTempList"),
         wram={wConsole: b"\x02", sym("wDuelTempList"): b"\x01\x09"},
         read={wDefaultText: 7, wDecimalDigitsSymbols: 2},
         expect={wDefaultText: b"\x05\x2D\x05\x36\x05\x26\x00", wDecimalDigitsSymbols: b"\x26\x36"}),
]
# <<< factory DrawPlayArea_IconWithValue

# >>> factory SaveDuelStateToSRAM
CONTRACT["SaveDuelStateToSRAM"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SaveDuelStateToSRAM"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)),
              wOpponentArenaCard: b"\x00", wOpponentDeck: bytes((IVYSAUR,)),
              wDuelTurns: b"\x05", wDuelType: b"\x00"},
     "sram": {0: {s0a008: b"\x00"}},
     "read": {wTempTurnDuelistCardID: 1, wTempNonTurnDuelistCardID: 1},
     "sread": {0: {s0a008: 1}, 3: {sDuelBuffer0: 3, sDuelBuffer0 + 0x10: 4}}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)),
                       wOpponentArenaCard: b"\x00", wOpponentDeck: bytes((IVYSAUR,)),
                       wDuelTurns: b"\x07", wDuelType: b"\x00"},
         sram={0: {s0a008: b"\x05"}},
         read={wTempTurnDuelistCardID: 1, wTempNonTurnDuelistCardID: 1},
         sread={0: {s0a008: 1}, 3: {sDuelBuffer0 + 0x400: 3, sDuelBuffer0 + 0x400 + 0x10: 4}}),
    {"wram": {hWhoseTurn: b"\xC3", wOpponentArenaCard: b"\x01", wOpponentDeck + 1: bytes((BULBASAUR,)),
              wPlayerArenaCard: b"\x01", wPlayerDeck + 1: bytes((IVYSAUR,)),
              wDuelTurns: b"\x0A", wDuelType: b"\x00"},
     "sram": {0: {s0a008: b"\xFF"}},
     "read": {wTempTurnDuelistCardID: 1, wTempNonTurnDuelistCardID: 1},
     "sread": {0: {s0a008: 1}, 3: {sDuelBuffer0 + 0xC00: 3, sDuelBuffer0 + 0xC00 + 0x10: 4}}},
]
# <<< factory SaveDuelStateToSRAM

# >>> factory DisplayCheckMenuCursor_YourOrOppPlayArea
CONTRACT["DisplayCheckMenuCursor_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DisplayCheckMenuCursor_YourOrOppPlayArea"] = [
    {},
    dict(POISON),
]
# <<< factory DisplayCheckMenuCursor_YourOrOppPlayArea

# >>> factory HandleCheckMenuInput_YourOrOppPlayArea
CONTRACT["HandleCheckMenuInput_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleCheckMenuInput_YourOrOppPlayArea"] = [
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCheckMenuCursorBlinkCounter: b"\x00",
              wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00"},
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, wram={hDPadHeld: b"\x00", hKeysPressed: b"\x00", wCheckMenuCursorBlinkCounter: b"\x00",
                       wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00"},
         vread={0: {0x9800: 0x400}}),
    {"wram": {hDPadHeld: b"\x00", hKeysPressed: b"\x02",
              wCheckMenuCursorBlinkCounter: b"\x00",
              wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00"}},
]
for _mode, _y in ((0, 0), (0, 1), (1, 0), (1, 1)):
    CASES["HandleCheckMenuInput_YourOrOppPlayArea"].append({
        "wram": {hDPadHeld: b"\x10", hKeysPressed: b"\x00", sym("wce5e"): bytes([_mode]),
                 wCheckMenuCursorBlinkCounter: b"\x00",
                 wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: bytes([_y])},
        "read": {wCheckMenuCursorXPosition: 1, wCheckMenuCursorYPosition: 1},
    })
# <<< factory HandleCheckMenuInput_YourOrOppPlayArea

# >>> factory DrawYourOrOppPlayArea_Icons
CONTRACT["DrawYourOrOppPlayArea_Icons"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayArea_Icons"] = [
    {"a": 0x00, "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03"},
     "read": {wDefaultText: 7},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, a=0x01, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC3", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
         read={wDefaultText: 7},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayArea_Icons

# >>> factory DrawInPlayArea_Icons
CONTRACT["DrawInPlayArea_Icons"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawInPlayArea_Icons"] = [
    {"hl": sym("wNameBuffer"), "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
              sym("wNameBuffer"): b"\x0F\x02\x0F\x04\x0F\x06"}, "read": {wDefaultText: 7},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=sym("wNameBuffer"), wram={hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
              sym("wNameBuffer"): b"\x0F\x02\x0F\x04\x0F\x06"}, read={wDefaultText: 7},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawInPlayArea_Icons

# >>> factory DisplayUsePokemonPowerScreen_WaitForInput
CONTRACT["DisplayUsePokemonPowerScreen_WaitForInput"] = {"compare": ("f",), "preserve": ()}
CASES["DisplayUsePokemonPowerScreen_WaitForInput"] = [
    {"hl": 0x0000, "keys": 0x01, "hbank_rom": 0x01, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempPlayAreaLocation_ff9d: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0x0000, keys=0x01, hbank_rom=0x01, instruction_budget=5000000, cycle_budget=20000000,
         hram={hTempPlayAreaLocation_ff9d: b"\x00"},
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00",
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DisplayUsePokemonPowerScreen_WaitForInput

# >>> factory _DrawPlayAreaToPlacePrizeCards
CONTRACT["_DrawPlayAreaToPlacePrizeCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["_DrawPlayAreaToPlacePrizeCards"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
              sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
              sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
     "read": {wDefaultText: 7, wIsSwapTurnPending: 1, wCheckMenuPlayAreaWhichLayout: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)),
               sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00"},
         read={wDefaultText: 7, wIsSwapTurnPending: 1, wCheckMenuPlayAreaWhichLayout: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory _DrawPlayAreaToPlacePrizeCards

# >>> factory UsePokemonPower
CONTRACT["UsePokemonPower"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["UsePokemonPower"] = [
    {"sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, sram={0: {}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory UsePokemonPower

# >>> factory DrawYourOrOppPlayArea_ActiveCardGfx
CONTRACT["DrawYourOrOppPlayArea_ActiveCardGfx"] = {"compare": ("d", "e"), "preserve": ("d", "e")}
CASES["DrawYourOrOppPlayArea_ActiveCardGfx"] = [
    {"wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wPlayerBench"): b"\x00"},
     "sram": {}, "vread": {0: {0x8A00: 1, 0x9800: 1}}},
    dict(POISON, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wPlayerBench"): b"\x00"},
         vread={0: {0x8A00: 1, 0x9800: 1}}),
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0x08, "e": 0x06,
     "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", sym("wPlayerArenaCard"): b"\x00", wPlayerDeck: b"\x00"},
     "vread": {0: {0x8A00: 1, 0x98C8: 1}}},
]
# <<< factory DrawYourOrOppPlayArea_ActiveCardGfx

# >>> factory _DrawYourOrOppPlayAreaScreen
CONTRACT["_DrawYourOrOppPlayAreaScreen"] = {"compare": (), "preserve": (), "wram_out": True}
# Case 0 also seeds two player prizes (wDuelInitialPrizes $CC08, DUELVARS_PRIZES
# $C2EC) and reads PrizeCardsCoordinateData_YourOrOppPlayArea.player's slots
# (2,1),(2,3) plus the (12,2) slot a wrong table drew into; 0xC100 seeded and
# diffed because the table is passed by ROM address, never copied to WRAM.
CASES["_DrawYourOrOppPlayAreaScreen"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000, "wram": {hWhoseTurn: b"\xC2", wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16, sym("wDuelInitialPrizes"): b"\x02", sym("wPlayerPrizes"): b"\x01", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00" * 12}, "read": {wDefaultText: 7}, "vread": {0: {0x9822: 2, 0x9842: 2, 0x9862: 2, 0x9882: 2, 0x984C: 2}}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000, wram={hWhoseTurn: b"\xC2", wCheckMenuPlayAreaWhichDuelist: b"\xC3", wCheckMenuPlayAreaWhichLayout: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16}, read={wDefaultText: 7}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory _DrawYourOrOppPlayAreaScreen

# >>> factory DrawYourOrOppPlayAreaScreen
CONTRACT["DrawYourOrOppPlayAreaScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayAreaScreen"] = [
    {"hl": sym("wOpponentArenaCardFlags"), "instruction_budget": 20000000, "cycle_budget": 80000000, "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", sym("wCurDeckCardChanges"): b"\x00" * 16}, "read": {sym("wCurDeckCardChanges"): 7}, "expect": {wCheckMenuPlayAreaWhichDuelist: b"\xC3", wCheckMenuPlayAreaWhichLayout: b"\xC2"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03", sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", sym("wCurDeckCardChanges"): b"\x00" * 16}, read={sym("wCurDeckCardChanges"): 7}, expect={wCheckMenuPlayAreaWhichDuelist: b"\x12", wCheckMenuPlayAreaWhichLayout: b"\x34"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayAreaScreen

# >>> factory _DrawAIPeekScreen
CONTRACT["_DrawAIPeekScreen"] = {"compare": (), "preserve": ()}
CASES["_DrawAIPeekScreen"] = [
    {"b": 0x00, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
     "read": {wIsSwapTurnPending: 1, wMenuInputTablePointer: 2, wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, b=0x80, keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         wram={hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
         read={wIsSwapTurnPending: 1, wMenuInputTablePointer: 2, wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
         vread={0: {0x9800: 32, 0x9C00: 32}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
    {"b": 0xFF, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x05", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x03",
               sym("wOpponentNumberOfCardsInHand"): b"\x02", sym("wOpponentNumberOfCardsNotInDeck"): b"\x37", sym("wOpponentNumberOfCardsInDiscardPile"): b"\x00", wDefaultText: b"\x00" * 16},
     "read": {wIsSwapTurnPending: 1, wMenuInputTablePointer: 2, wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]}]
# <<< factory _DrawAIPeekScreen

# >>> factory PrintPokemonsAttackText
CONTRACT["PrintPokemonsAttackText"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintPokemonsAttackText"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xBB: b"\x00", wPlayerDeck: b"\x08", wLoadedCard1Name: b"\x35\x00", wLoadedAttackName: b"\x35\x00", wDefaultText: b"\x00", wTxRam2: b"\x00\x00\x35\x00"},
     "setup": TEXT_SETUP, "read": {wDefaultText: 64, wTxRam2: 4}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xBB: b"\x00", wPlayerDeck: b"\x08", wLoadedCard1Name: b"\x35\x00", wLoadedAttackName: b"\x35\x00", wDefaultText: b"\x00", wTxRam2: b"\x00\x00\x35\x00"},
         setup=TEXT_SETUP, read={wDefaultText: 64, wTxRam2: 4}),
]
# <<< factory PrintPokemonsAttackText

# >>> factory PrintFailedEffectText
CONTRACT["PrintFailedEffectText"] = {"compare": ("f",), "preserve": ()}
CASES["PrintFailedEffectText"] = [
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0, "wram": {wEffectFailed: b"\x00"}, "expect_regs": {"f": 0x80}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wEffectFailed: b"\x00"}, "expect_regs": {"f": 0x80}},
    # Non-degenerate paths. Both were previously unexercised: without SetupText in
    # `setup` the reference spins in Func_235e's glyph cache (pc~0x2380), which is
    # what made the real-text path look untestable.
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
     "wram": {wEffectFailed: b"\x01", sym("hTempPlayAreaLocation_ff9d"): b"\x00"}, "expect_regs": {"f": 0x10}},
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
     "wram": {wEffectFailed: b"\x02", sym("hTempPlayAreaLocation_ff9d"): b"\x00"}, "expect_regs": {"f": 0x10}},
]
# <<< factory PrintFailedEffectText

# >>> factory DrawInPlayArea_ActiveCardGfx
CONTRACT["DrawInPlayArea_ActiveCardGfx"] = {"compare": (), "preserve": ()}
CASES["DrawInPlayArea_ActiveCardGfx"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wOpponentArenaCard"): b"\xFF"}, "read": {sym("wArenaCardsInPlayArea"): 1}, "expect": {sym("wArenaCardsInPlayArea"): b"\x00"}},
    {"wram": {sym("hWhoseTurn"): b"\xC3", sym("wPlayerArenaCard"): b"\xFF", sym("wOpponentArenaCard"): b"\xFF"}, "read": {sym("wArenaCardsInPlayArea"): 1}, "expect": {sym("wArenaCardsInPlayArea"): b"\x00"}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wOpponentArenaCard"): b"\xFF"}, read={sym("wArenaCardsInPlayArea"): 1}, expect={sym("wArenaCardsInPlayArea"): b"\x00"}),
    # Both arenas hold Bulbasaur (deck index 0, id $08): the card image tiles
    # land at v0Tiles1 $8A00 and $9500, the palette in wCardPalette, and the
    # 6x8 images in the BG map at (9,6) and (2,6).
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wBoosterCardsDrawn"): b"\x08", sym("wOpponentDeck"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wOpponentCardLocations"): b"\x10", sym("wLCDC"): b"\x00"},
         read={sym("wArenaCardsInPlayArea"): 1, sym("wCardPalette"): 8, sym("wBackgroundPalettesCGB") + 0x31: 8}, vread={0: {0x8A00: 0x300, 0x9500: 0x300, 0x9800: 0x400}},
         instruction_budget=3000000, cycle_budget=12000000),
]
# <<< factory DrawInPlayArea_ActiveCardGfx

# >>> factory DrawInPlayAreaScreen
CONTRACT["DrawInPlayAreaScreen"] = {"compare": (), "preserve": (), "wram_out": True}
# The whole BG map is read back: the prize-card and icon coordinate tables are
# ROM literals, and a wrong table draws both lanes' screens differently.
CASES["DrawInPlayAreaScreen"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x00", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wBoosterCardsDrawn"): b"\x08", sym("wOpponentDeck"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wOpponentCardLocations"): b"\x10", sym("wPlayerPrizes"): b"\x3F", sym("wOpponentPrizes"): b"\x0F", sym("wDuelInitialPrizes"): b"\x06"},
     "read": {sym("wTileMapFill"): 1, sym("wDuelDisplayedScreen"): 1, sym("wCheckMenuPlayAreaWhichDuelist"): 1, sym("wCheckMenuPlayAreaWhichLayout"): 1}, "vread": {0: {0x9800: 0x400}}, "instruction_budget": 3000000, "cycle_budget": 12000000},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC3", sym("wLCDC"): b"\x00", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wPlayerArenaCard"): b"\x00", sym("wOpponentArenaCard"): b"\x00", sym("wBoosterCardsDrawn"): b"\x08", sym("wOpponentDeck"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wOpponentCardLocations"): b"\x10", sym("wPlayerPrizes"): b"\x3F", sym("wOpponentPrizes"): b"\x0F", sym("wDuelInitialPrizes"): b"\x06"},
         read={sym("wTileMapFill"): 1, sym("wDuelDisplayedScreen"): 1, sym("wCheckMenuPlayAreaWhichDuelist"): 1, sym("wCheckMenuPlayAreaWhichLayout"): 1}, vread={0: {0x9800: 0x400}}, instruction_budget=3000000, cycle_budget=12000000),
]
# <<< factory DrawInPlayAreaScreen

# >>> factory DrawDuelMainScene_PrintPokemonsAttackText
CONTRACT["DrawDuelMainScene_PrintPokemonsAttackText"] = {"compare": ("hl",), "preserve": ()}
CASES["DrawDuelMainScene_PrintPokemonsAttackText"] = [
    {"wram": {hWhoseTurn: b"\xC2", wDuelDisplayedScreen: b"\x01", wPlayerDuelVariables + 0xBB: b"\x00", wPlayerDeck: b"\x08", wLoadedCard1Name: b"\x35\x00", wLoadedAttackName: b"\x35\x00", wDefaultText: b"\x00", wTxRam2: b"\x00\x00\x35\x00"},
     "setup": TEXT_SETUP, "instruction_budget": 1000000, "cycle_budget": 10000000, "read": {wDefaultText: 64, wTxRam2: 4}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wDuelDisplayedScreen: b"\x01", wPlayerDuelVariables + 0xBB: b"\x00", wPlayerDeck: b"\x08", wLoadedCard1Name: b"\x35\x00", wLoadedAttackName: b"\x35\x00", wDefaultText: b"\x00", wTxRam2: b"\x00\x00\x35\x00"},
         setup=TEXT_SETUP, instruction_budget=1000000, cycle_budget=10000000, read={wDefaultText: 64, wTxRam2: 4}),
]
# <<< factory DrawDuelMainScene_PrintPokemonsAttackText

# >>> factory ProcessPlayedPokemonCard
CONTRACT["ProcessPlayedPokemonCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["ProcessPlayedPokemonCard"] = [
    {"a": 0x11, "f": 0x20, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x4567, "wram": {hTempCardIndex_ff98: b"\x00", hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08"}, "read": {wTempTurnDuelistCardID: 1, hTempCardIndex_ff9f: 1}},
    dict(POISON, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={hTempCardIndex_ff98: b"\x01", hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08"}, read={wTempTurnDuelistCardID: 1, hTempCardIndex_ff9f: 1}),
    dict(_pkmn_power_fixture(), read={_wTxRam2: 4, wTempTurnDuelistCardID: 1, hTempCardIndex_ff9f: 1},
         **_PKMN_POWER_REGS, **{"compare": ()}),
]
# <<< factory ProcessPlayedPokemonCard

# >>> factory _SelectPrizeCards
CONTRACT["_SelectPrizeCards"] = {"compare": (), "preserve": ()}
# One prize to select from the practice-duel state: A takes the first set
# prize, it joins the hand and its page is shown; the list at $FFA1 gets the
# deck index and the terminator, $FFA0 the remaining mask. Nothing to select:
# only the terminator and mask are written.
CASES["_SelectPrizeCards"] = [
    dict(_attack_fixture(changes={sym("wNumberOfPrizeCardsToSelect"): b"\x01"}), read={sym("wPlayerCardLocations"): 0x200, sym("wPracticeDuelTurn"): 0x100, sym("wInPlayAreaCurPosition"): 1, sym("wSelectedPrizeCardListPtr"): 2, sym("hTempList"): 3}, **_ATTACK_REGS),
    dict(_attack_fixture(vram=False, changes={sym("wNumberOfPrizeCardsToSelect"): b"\x00"}), read={sym("wPlayerCardLocations"): 0x200, sym("wInPlayAreaCurPosition"): 1, sym("wSelectedPrizeCardListPtr"): 2, sym("hTempList"): 3}, **POISON),
]
# <<< factory _SelectPrizeCards

# >>> factory PlayTrainerCard
CONTRACT["PlayTrainerCard"] = {"compare": ("f",), "preserve": ()}
CASES["PlayTrainerCard"] = [
    dict(_full_heal_trainer_fixture(vram=False), **_FULL_HEAL_TRAINER_REGS, keys=[0x00, 0x01],
         read={sym("wDamageAnimAmount"): 1, hTempCardIndex_ff9f: 1}, instruction_budget=20000000,
         cycle_budget=80000000),
    dict(POISON, keys=[0x00, 0x01], wram={hWhoseTurn: b"\xC2", sym("wPlayerArenaCardSubstatus3"): b"\x02", hTempCardIndex_ff98: b"\x01", hTempCardIndex_ff9f: b"\x55", wLCDC: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={hTempCardIndex_ff9f: 1}, expect={hTempCardIndex_ff9f: b"\x55"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PlayTrainerCard

# >>> factory CheckSelfConfusionDamage
CONTRACT["CheckSelfConfusionDamage"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["CheckSelfConfusionDamage"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCardStatus: b"\x00"},
     "read": {wConfusionAttackCheckWasUnsuccessful: 1}},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerArenaCardStatus: b"\x02"},
     "read": {wConfusionAttackCheckWasUnsuccessful: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerArenaCardStatus: b"\x00"},
         read={wConfusionAttackCheckWasUnsuccessful: 1}),
]
# <<< factory CheckSelfConfusionDamage

# >>> factory ApplyTransparencyIfApplicable
CONTRACT["ApplyTransparencyIfApplicable"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["ApplyTransparencyIfApplicable"] = [
    {"f": 0x00, "d": 0x12, "e": 0x34, "hl": 0x4567, "wram": {wLoadedAttackCategory: b"\x80", wNoDamageOrEffect: b"\x00", hWhoseTurn: b"\xC2"}, "expect_regs": {"a": 0x80, "f": 0x20, "d": 0x12, "e": 0x34, "hl": 0x4567}},
    {"f": 0x00, "d": 0x00, "e": 0x00, "hl": 0x4567, "wram": {wLoadedAttackCategory: b"\x00", wNoDamageOrEffect: b"\x01", hWhoseTurn: b"\xC2"}, "expect_regs": {"a": 0x01, "f": 0x00, "d": 0x00, "e": 0x00, "hl": 0x4567}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wLoadedAttackCategory: b"\x00", wNoDamageOrEffect: b"\x00", wStatusConditionQueueIndex: b"\x00", wTempNonTurnDuelistCardID: b"\x01", wTempPlayAreaLocation_cceb: b"\xAA", hWhoseTurn: b"\xC2"}, "read": {wTempPlayAreaLocation_cceb: 1}, "expect_regs": {"a": 0x01, "f": 0x00, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}, "expect": {wTempPlayAreaLocation_cceb: b"\x00"}}
]
# <<< factory ApplyTransparencyIfApplicable


#

# >>> factory DealDamageToPlayAreaPokemon
CONTRACT["DealDamageToPlayAreaPokemon"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["DealDamageToPlayAreaPokemon"] = [
    {"b": 0x00, "d": 0x00, "e": 0x14, "wram": {sym("wNoDamageOrEffect"): b"\x01", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, "read": {sym("wTempPlayAreaLocation_cceb"): 1}},
    dict(POISON, b=0x00, d=0x00, e=0x14, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wBoosterCardsDrawn"): b"\x01", sym("wNoDamageOrEffect"): b"\x01", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, read={sym("wTempPlayAreaLocation_cceb"): 1}),
    {"b": 0x00, "d": 0x00, "e": 0x0A, "wram": {sym("wNoDamageOrEffect"): b"\x02", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, "read": {sym("wTempPlayAreaLocation_cceb"): 1}},
]
# <<< factory DealDamageToPlayAreaPokemon

# >>> factory DealDamageToPlayAreaPokemon_RegularAnim
CONTRACT["DealDamageToPlayAreaPokemon_RegularAnim"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["DealDamageToPlayAreaPokemon_RegularAnim"] = [
    {"b": 0x00, "d": 0x00, "e": 0x14, "wram": {sym("wNoDamageOrEffect"): b"\x01", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, "read": {sym("wLoadedAttackAnimation"): 1, sym("wTempPlayAreaLocation_cceb"): 1}},
    dict(POISON, b=0x00, d=0x00, e=0x14, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wBoosterCardsDrawn"): b"\x01", sym("wNoDamageOrEffect"): b"\x01", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, read={sym("wLoadedAttackAnimation"): 1, sym("wTempPlayAreaLocation_cceb"): 1}),
    {"b": 0x00, "d": 0x00, "e": 0x0A, "wram": {sym("wNoDamageOrEffect"): b"\x02", sym("wTempPlayAreaLocation_cceb"): b"\xAA"}, "read": {sym("wLoadedAttackAnimation"): 1, sym("wTempPlayAreaLocation_cceb"): 1}},
]
# <<< factory DealDamageToPlayAreaPokemon_RegularAnim


# >>> factory DealConfusionDamageToSelf
# Needs SetupText: without it the reference spins in Func_235e's glyph cache at
# pc=0x2380 (which is what the old AUTO-RETIRED "BUDGET_EXHAUSTED pc=9088" note
# recorded), and the real run takes ~700k instructions so the default budget is
# far too small.
_dcdts_wDamage = sym("wDamage")
_dcdts_wNoDamageOrEffect = sym("wNoDamageOrEffect")
_dcdts_wTempNonTurn = sym("wTempNonTurnDuelistCardID")
_dcdts_wTempTurn = sym("wTempTurnDuelistCardID")
_dcdts_wDamageEffectiveness = sym("wDamageEffectiveness")
_dcdts_arena_hp = sym("wPlayerArenaCardHP")

def _dcdts(**kw):
    case = {"wram": {sym("hWhoseTurn"): b"\xC2", _dcdts_arena_hp: b"\x40",
                     _dcdts_wDamage: b"\x00\x00", _dcdts_wNoDamageOrEffect: b"\x00",
                     _dcdts_wTempNonTurn: b"\x01", _dcdts_wTempTurn: b"\x01",
                     _dcdts_wDamageEffectiveness: b"\x00"},
            "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
            "instruction_budget": 8000000, "cycle_budget": 32000000,
            "read": {_dcdts_wDamage: 2, _dcdts_wNoDamageOrEffect: 1,
                     _dcdts_wTempNonTurn: 1, _dcdts_arena_hp: 1}}
    case.update(kw)
    return case

CONTRACT["DealConfusionDamageToSelf"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DealConfusionDamageToSelf"] = [
    _dcdts(a=0x10),   # ordinary damage
    _dcdts(a=0x00),   # zero damage takes ApplyDamageModifiers' .no_damage path
    _dcdts(a=0x50),   # exceeds HP: the knocked-out path
    dict(POISON, **_dcdts()),
]
# <<< factory DealConfusionDamageToSelf

# >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile
CONTRACT["OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, "read": {sym("wDuelTempList"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02", sym("wPlayerDeckCards"): b"\x11\x22", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00", sym("wDuelTempList"): b"\xFF", sym("wNoItemSelectionMenuKeys"): b"\x00"}, "read": {sym("wNoItemSelectionMenuKeys"): 1, sym("wDuelTempList"): 3}, "expect": {sym("wNoItemSelectionMenuKeys"): b"\x09"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, read={sym("wDuelTempList"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile

# >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand
CONTRACT["OpenYourOrOppPlayAreaScreen_NonTurnHolderHand"] = {"compare": (), "preserve": ()}
CASES["OpenYourOrOppPlayAreaScreen_NonTurnHolderHand"] = [
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wOpponentNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wOpponentNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}}
]
# <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand

# >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderHand
CONTRACT["OpenYourOrOppPlayAreaScreen_TurnHolderHand"] = {"compare": ("a", "f"), "preserve": ("f",)}
CASES["OpenYourOrOppPlayAreaScreen_TurnHolderHand"] = [
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC1", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1}, "expect": {sym("hWhoseTurn"): b"\xC1"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wLCDC"): b"\x00"}, read={sym("hWhoseTurn"): 1}, expect={sym("hWhoseTurn"): b"\xC2"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderHand

# >>> factory DealRecoilDamageToSelf
CONTRACT["DealRecoilDamageToSelf"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DealRecoilDamageToSelf"] = [
    _drdts(a=0x10),   # ordinary damage: HP $40 -> $30
    _drdts(a=0x00),   # zero damage takes ApplyDamageModifiers' .no_damage path
    _drdts(a=0x50),   # exceeds HP: the knocked-out path
    # Six poisoned registers (f/b/c/d/e/hl); `a` is the damage byte and stays at
    # $50 so the reference's damage-number animation terminates.
    _drdts(a=0x50, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234),
]
# <<< factory DealRecoilDamageToSelf

# >>> factory DuelCheckMenu_Glossary
CONTRACT["DuelCheckMenu_Glossary"] = {"compare": (), "preserve": ()}
CASES["DuelCheckMenu_Glossary"] = [
    {"keys": [0x00, 0x02], "wram": {sym("wGlossaryPageNo"): b"\x00", sym("wInPlayAreaCurPosition"): b"\x00", sym("wDuelInitialPrizesUpperBitsSet"): b"\xFF", sym("wCheckMenuCursorBlinkCounter"): b"\x00", sym("wTileMapFill"): b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x02], "wram": {sym("wGlossaryPageNo"): b"\x01", sym("wInPlayAreaCurPosition"): b"\x00", sym("wDuelInitialPrizesUpperBitsSet"): b"\xFF", sym("wCheckMenuCursorBlinkCounter"): b"\x00", sym("wTileMapFill"): b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("wGlossaryPageNo"): b"\x00", sym("wInPlayAreaCurPosition"): b"\x00", sym("wDuelInitialPrizesUpperBitsSet"): b"\xFF", sym("wCheckMenuCursorBlinkCounter"): b"\x00", sym("wTileMapFill"): b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory DuelCheckMenu_Glossary

# >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile
CONTRACT["OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile"] = [
    {"c": 0x00, "keys": [0x00, 0x01], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, "read": {sym("wDuelTempList"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"c": 0x00, "keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x02", sym("wPlayerDeckCards"): b"\x11\x22", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00", sym("wDuelTempList"): b"\xFF", sym("wNoItemSelectionMenuKeys"): b"\x00"}, "read": {sym("wNoItemSelectionMenuKeys"): 1, sym("wDuelTempList"): 3}, "expect": {sym("wNoItemSelectionMenuKeys"): b"\x09"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, c=0x00, keys=[0x00, 0x01], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInDiscardPile"): b"\x00", sym("wLCDC"): b"\x00", sym("wCurDeckCardChanges"): b"\x00"}, read={sym("wDuelTempList"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile

# >>> factory _HandlePeekSelection
CONTRACT["_HandlePeekSelection"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["_HandlePeekSelection"] = [
    # keys=[0x00, 0x01] taps A: it selects item 0 ("your" Play Area) out of the
    # first menu, confirms prize slot 0 in the play-area cursor, and then pages
    # the card page out until DisplayFirstOrNextCardPage runs out of pages, so
    # the run reaches .ShowSelectedCard's ret with a = $40 = [wce5c].
    {"keys": [0x00, 0x01], "wram": dict(_hps_wram), "read": dict(_hps_read),
     "setup": _hps_setup, "instruction_budget": 30000000, "cycle_budget": 120000000},
    dict(POISON, keys=[0x00, 0x01], wram=dict(_hps_wram), read=dict(_hps_read),
         setup=_hps_setup, instruction_budget=30000000, cycle_budget=120000000),
]
# <<< factory _HandlePeekSelection

# >>> factory _OpenDuelCheckMenu
CONTRACT["_OpenDuelCheckMenu"] = {"compare": (), "preserve": ()}
CASES["_OpenDuelCheckMenu"] = [
    {"keys": [0x00, 0x02], "wram": {sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", wce5e: b"\x55"}, "read": {wce5e: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", wce5e: b"\xAA"}, read={wce5e: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _OpenDuelCheckMenu

# >>> factory DuelCheckMenu_InPlayArea
CONTRACT["DuelCheckMenu_InPlayArea"] = {"compare": (), "preserve": ()}
CASES["DuelCheckMenu_InPlayArea"] = [
    {"wram": {sym("wInPlayAreaFromSelectButton"): b"\x55"}, "read": {sym("wInPlayAreaFromSelectButton"): 1}, "completion": {"mode": "pre-ret", "pc": sym("SafeCopyDataDEtoHL")}},
    dict(POISON, wram={sym("wInPlayAreaFromSelectButton"): b"\xAA"}, read={sym("wInPlayAreaFromSelectButton"): 1}, completion={"mode": "pre-ret", "pc": sym("SafeCopyDataDEtoHL")}),
]
# <<< factory DuelCheckMenu_InPlayArea

# >>> factory DuelCheckMenu_YourPlayArea
CONTRACT["DuelCheckMenu_YourPlayArea"] = {"compare": (), "preserve": ()}
CASES["DuelCheckMenu_YourPlayArea"] = [
    {"keys": [0x00, 0x02], "wram": {sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF", wce5e: b"\x55"}, "read": {wce5e: 1, sym("wYourOrOppPlayAreaLastCursorPosition"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF", wce5e: b"\xAA"}, read={wce5e: 1, sym("wYourOrOppPlayAreaLastCursorPosition"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DuelCheckMenu_YourPlayArea

# >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea
CONTRACT["OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea"] = [
    # The turn holder's play area screen until B; hWhoseTurn survives.
    {"keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardStatus"): b"\x00", sym("wPlayerArenaCardHP"): b"\x28", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wBoosterCardsDrawn"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1, sym("wCurPlayAreaSlot"): 1, sym("wDuelDisplayedScreen"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardStatus"): b"\x00", sym("wPlayerArenaCardHP"): b"\x28", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wBoosterCardsDrawn"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wLCDC"): b"\x00"}, read={sym("hWhoseTurn"): 1, sym("wCurPlayAreaSlot"): 1, sym("wDuelDisplayedScreen"): 1}, expect={sym("hWhoseTurn"): b"\xC2"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea

# >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea
CONTRACT["OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea"] = [
    # The opponent's play area screen until B; hWhoseTurn survives the swap inside.
    {"keys": [0x00, 0x02], "wram": {sym("hWhoseTurn"): b"\xC2", sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardStatus"): b"\x00", sym("wOpponentArenaCardHP"): b"\x28", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentDeck"): b"\x08", sym("wOpponentCardLocations"): b"\x10", sym("wLCDC"): b"\x00"}, "read": {sym("hWhoseTurn"): 1, sym("wCurPlayAreaSlot"): 1, sym("wDuelDisplayedScreen"): 1}, "expect": {sym("hWhoseTurn"): b"\xC2"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("hWhoseTurn"): b"\xC2", sym("wOpponentArenaCard"): b"\x00", sym("wOpponentArenaCardStatus"): b"\x00", sym("wOpponentArenaCardHP"): b"\x28", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01", sym("wOpponentDeck"): b"\x08", sym("wOpponentCardLocations"): b"\x10", sym("wLCDC"): b"\x00"}, read={sym("hWhoseTurn"): 1, sym("wCurPlayAreaSlot"): 1, sym("wDuelDisplayedScreen"): 1}, expect={sym("hWhoseTurn"): b"\xC2"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea

# >>> factory DuelCheckMenu_OppPlayArea
CONTRACT["DuelCheckMenu_OppPlayArea"] = {"compare": (), "preserve": ()}
CASES["DuelCheckMenu_OppPlayArea"] = [
    {"keys": [0x00, 0x02], "wram": {sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wPlayerCardLocations"): b"\x00" * 0x100, sym("wOpponentCardLocations"): b"\x00" * 0x100, sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF", sym("wCurDeckCardChanges"): b"\x00" * 16, wce5e: b"\x55"}, "read": {wce5e: 1, sym("wYourOrOppPlayAreaLastCursorPosition"): 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 30000000, "cycle_budget": 120000000},
    dict(POISON, keys=[0x00, 0x02], wram={sym("hBankROM"): b"\x02", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wPlayerCardLocations"): b"\x00" * 0x100, sym("wOpponentCardLocations"): b"\x00" * 0x100, sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF", sym("wCurDeckCardChanges"): b"\x00" * 16, wce5e: b"\xAA"}, read={wce5e: 1, sym("wYourOrOppPlayAreaLastCursorPosition"): 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=30000000, cycle_budget=120000000),
]
# <<< factory DuelCheckMenu_OppPlayArea

# >>> factory HandleConfusionDamageToSelf
CONTRACT["HandleConfusionDamageToSelf"] = {"compare": ("a", "f"), "preserve": ()}


# Confusion self-damage from the same state: 20 to Goldeen (40 HP -> 20).
CASES["HandleConfusionDamageToSelf"] = [
    dict(_attack_fixture(), **_ATTACK_REGS),
    dict(_attack_fixture(), **POISON)
]
# <<< factory HandleConfusionDamageToSelf

# >>> factory HandleAfterDamageEffects
CONTRACT["HandleAfterDamageEffects"] = {"compare": ("a", "f"), "preserve": ()}
# From the same state after the 10 damage landed (Machop 50 -> 40): no
# knockout, so the chain ends with the play areas untouched and carry clear.
# The second case knocks Machop out (HP 0) with no bench: Sam's replacement
# fails, the duel finishes with the player's win.
CASES["HandleAfterDamageEffects"] = [
    dict(_attack_fixture(changes={sym("wOpponentArenaCardHP"): b"\x28"}), **_ATTACK_REGS),
    dict(_attack_fixture(changes={sym("wOpponentArenaCardHP"): b"\x00", sym("wOpponentBench"): b"\xff" * 5, sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01"}), **POISON),
]
# <<< factory HandleAfterDamageEffects

# >>> factory Func_17ed
CONTRACT["Func_17ed"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_17ed"] = [
    dict(evidence="primary", oracle=False, why="Func_17ed falls through into HandleAfterDamageEffects, whose downstream effect handlers enter the live duel/frame loop and cannot complete as a standalone reference call; this bounded native case checks the derived return and writes.", hl=0x0031, keys=[0x00, 0x01], wram={sym("wLCDC"): b"\x00", sym("wDamage"): b"\x34\x12", sym("wNoDamageOrEffect"): b"\x00"}, read={sym("wDamage"): 3}, expect_regs={"a": 0x03, "f": 0x00}, expect={sym("wDamage"): b"\x00\x00\x01"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, evidence="primary", oracle=False, why="Func_17ed falls through into HandleAfterDamageEffects, whose downstream effect handlers enter the live duel/frame loop and cannot complete as a standalone reference call; this bounded native poison case checks the derived return and writes.", hl=0x0031, keys=[0x00, 0x01], wram={sym("wLCDC"): b"\x00", sym("wDamage"): b"\xFF\xFF", sym("wNoDamageOrEffect"): b"\x7F"}, read={sym("wDamage"): 3}, expect_regs={"a": 0x03, "f": 0x00}, expect={sym("wDamage"): b"\x00\x00\x01"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)
]
# <<< factory Func_17ed

# >>> factory PlayAttackAnimation_DealAttackDamage
CONTRACT["PlayAttackAnimation_DealAttackDamage"] = {"compare": ("a", "f"), "preserve": ()}
# Horn Attack for 10: Machop 50 -> 40, HUD redrawn, no knockout. The second
# case makes it lethal (Machop at 10 HP, no bench) so the prize and duel-end
# path runs too.
CASES["PlayAttackAnimation_DealAttackDamage"] = [
    dict(_attack_fixture(), **_ATTACK_REGS),
    dict(_attack_fixture(changes={sym("wOpponentArenaCardHP"): b"\x0a", sym("wOpponentBench"): b"\xff" * 5, sym("wOpponentNumberOfPokemonInPlayArea"): b"\x01"}), **POISON),
]
# <<< factory PlayAttackAnimation_DealAttackDamage

# >>> factory UseAttackOrPokemonPower
CONTRACT["UseAttackOrPokemonPower"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["UseAttackOrPokemonPower"] = [
    dict(evidence="primary", oracle=False, why="The Pokemon Power path is bounded with an empty effect-command list and a non-link opponent; it exercises the target's dispatch and all three attacking-card bookkeeping writes without entering the frame-driven attack animation.", wram={wSelectedAttack: b"\x01", hTempCardIndex_ff9f: b"\x02", wTempCardID_ccc2: b"\x2A", wLoadedAttackCategory: b"\x04", wLoadedAttackEffectCommands: b"\x00\x00", hWhoseTurn: b"\xC2", wDuelType: b"\x00", wOpponentDuelVariables + 0xF1: b"\x00"}, read={wPlayerAttackingAttackIndex: 1, wPlayerAttackingCardIndex: 1, wPlayerAttackingCardID: 1}, expect={wPlayerAttackingAttackIndex: b"\x01", wPlayerAttackingCardIndex: b"\x02", wPlayerAttackingCardID: b"\x2A"}, expect_regs={"a": 0x00, "f": 0x70, "b": 0x00, "c": 0x03, "d": 0x00, "e": 0x00, "hl": 0x0000}),
    dict(POISON, evidence="primary", oracle=False, why="The poisoned-register Pokemon Power case keeps the same bounded no-effect dispatch while proving that the wrapper reloads the selected attack, card index, and card ID rather than leaking entry-register poison.", wram={wSelectedAttack: b"\x01", hTempCardIndex_ff9f: b"\x02", wTempCardID_ccc2: b"\x2A", wLoadedAttackCategory: b"\x04", wLoadedAttackEffectCommands: b"\x00\x00", hWhoseTurn: b"\xC2", wDuelType: b"\x00", wOpponentDuelVariables + 0xF1: b"\x00"}, read={wPlayerAttackingAttackIndex: 1, wPlayerAttackingCardIndex: 1, wPlayerAttackingCardID: 1}, expect={wPlayerAttackingAttackIndex: b"\x01", wPlayerAttackingCardIndex: b"\x02", wPlayerAttackingCardID: b"\x2A"}, expect_regs={"a": 0x00, "f": 0x70, "b": 0xBB, "c": 0x03, "d": 0xDD, "e": 0xEE, "hl": 0x0000})
]
# <<< factory UseAttackOrPokemonPower

from tests.cases._schema_migration import legacy_to_schema

# >>> factory Func_1bb4
# duel.asm:2214-2223, a straight call sequence. `compare` is ("a",) alone because
# the reference leaves b=0x12 c=0x11 d=0x12 e=0x11 f=0x70 hl=0xCD12 here -- values
# produced inside DrawDuelHUDs / DrawDuelMainScene / WaitForWideTextBoxInput, each
# registered with a contract that returns void or {f} only. Measured 2026-08-26;
# that debt belongs to those callees, and widening them is what lets this grow.
# The `read` span on hTempPlayAreaLocation_ff9d keeps this non-vacuous: it verifies
# this routine's own `xor a` write.
#
# The wram seed is the UNION of DrawDuelHUDs' and DrawDuelMainScene's own registered
# case seeds. 0xC2BB/0xC3BB = 0xFF marks both arena slots empty; without that,
# DrawDuelHUDs draws HP for card ID 0 and never terminates on the native probe.
_F1BB4_HUD = {sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\xFF", sym("wOpponentArenaCard"): b"\xFF",
              sym("wPlayerDuelistType"): b"\x00", sym("wPlayerArenaCardStatus"): b"\x00", sym("wOpponentDuelistType"): b"\x00", sym("wOpponentArenaCardStatus"): b"\x00",
              sym("wPlayerPrizes"): b"\x00", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x00", sym("wOpponentPrizes"): b"\x00", sym("wOpponentNumberOfPokemonInPlayArea"): b"\x00",
              sym("wDuelDisplayedScreen"): b"\x01"}
_F1BB4_SETUP = [{"fn": "SetupText", "d": 0x30, "e": 0x7F}]
CONTRACT["Func_1bb4"] = {"compare": ("a",), "preserve": ()}
CASES["Func_1bb4"] = [
    {"b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000,
     "keys": 0x01, "cycle_budget": 40_000_000, "wram": dict(_F1BB4_HUD),
     "setup": list(_F1BB4_SETUP), "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    dict(POISON, keys=0x01, cycle_budget=40_000_000, wram=dict(_F1BB4_HUD),
         setup=list(_F1BB4_SETUP), read={sym("hTempPlayAreaLocation_ff9d"): 1}),
]
# <<< factory Func_1bb4


# >>> factory Func_82b6
CONTRACT["Func_82b6"] = {"compare": (), "preserve": ()}
CASES["Func_82b6"] = [
    {"wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC4", sym("wOpponentDeck") + 0x6C: b"\x01", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x00", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00" * 12},
     "vread": {0: {0x9822: 2, 0x9842: 2, 0x9862: 2, 0x9882: 2}}},
    {"wram": {sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC3", sym("wOpponentDeck") + 0x6C: b"\x01", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x00"},
     "vread": {0: {0x99E9: 2, 0x9A09: 2, 0x9A29: 2, 0x9A49: 2}}},
    dict(POISON,
         wram={sym("wCheckMenuPlayAreaWhichDuelist"): b"\xC4", sym("wCheckMenuPlayAreaWhichLayout"): b"\xC4", sym("wOpponentDeck") + 0x6C: b"\x02", sym("wDuelInitialPrizes"): b"\x02", sym("wConsole"): b"\x00"},
         vread={0: {0x9822: 2, 0x9842: 2, 0x9862: 2, 0x9882: 2}}),
]
# <<< factory Func_82b6

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CountCardIDInLocation": {
        "source_symbol": "CountCardIDInLocation",
        "before": "\tuint16_t base = (uint16_t)((hl & 0xFF00u) | DUELVARS_CARD_LOCATIONS);",
        "after": "\tuint16_t base = hl;",
        "case_ids": ["CountCardIDInLocation-3"],
    },
    "SortCardsInListByID": {
        "source_symbol": "SortCardsInListByID",
        "before": "\t\tgb_write8(hTempCardID_ff9b_ADDR, (uint8_t)lowest_id);\n\t\tgb_write8((uint16_t)(hTempCardID_ff9b_ADDR + 1u), (uint8_t)(lowest_id >> 8));\n\t\tuint16_t scan",
        "after": "\t\tuint16_t scan",
        "case_ids": ["SortCardsInListByID-0"],
    },
    "SwapTurn": {
        "source_symbol": "SwapTurn",
        "before": "hWhoseTurn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;",
        "after": "hWhoseTurn = hWhoseTurn == PLAYER_TURN ? PLAYER_TURN : OPPONENT_TURN;",
        "case_ids": ["SwapTurn-0", "SwapTurn-1", "SwapTurn-2"],
    },
    "UpdateArenaCardIDsAndClearTwoTurnDuelVars": {
        "source_symbol": "UpdateArenaCardIDsAndClearTwoTurnDuelVars",
        "before": "wNoEffectFromWhichStatus = 0;",
        "after": "wNoEffectFromWhichStatus = 1;",
        "case_ids": ["UpdateArenaCardIDsAndClearTwoTurnDuelVars-0",
                     "UpdateArenaCardIDsAndClearTwoTurnDuelVars-1"],
    },
    "ClearNonTurnTemporaryDuelvars_ResetCarry": {"source_symbol": "ClearNonTurnTemporaryDuelvars_ResetCarry", "before": "\tClearNonTurnTemporaryDuelvars();\n\t(void)a;", "after": "\t(void)0;\n\t(void)a;", "case_ids": ["ClearNonTurnTemporaryDuelvars_ResetCarry-0", "ClearNonTurnTemporaryDuelvars_ResetCarry-1"]},
    "PrintKnockedOutIfHLZero": {
        "source_symbol": "PrintKnockedOutIfHLZero",
        "before": "\t(void)PrintKnockedOut();\n\treturn 0x90u;",
        "after": "\t(void)PrintKnockedOut();\n\treturn 0xd0u;",
        "case_ids": ["PrintKnockedOutIfHLZero-3"],
    },
}
# >>> factory-mutation GetFirstSetPrizeCard
MUTATIONS['EmptyPlayAreaSlot.init_duelvar'] = {"source_symbol": "EmptyPlayAreaSlot_init_duelvar", "before": "\tuint16_t addr = (uint16_t)((hl & 0xFF00u) | offset);", "after": "\tuint16_t addr = (uint16_t)((hl & 0xFF00u) | a);", "case_ids": ["EmptyPlayAreaSlot.init_duelvar-3"]}
MUTATIONS['SwapPlayAreaPokemon.swap_duelvar'] = {"source_symbol": "SwapPlayAreaPokemon_swap_duelvar", "before": "\tuint8_t held = gb_read8(addr_second);", "after": "\tuint8_t held = gb_read8(addr_first);", "case_ids": ["SwapPlayAreaPokemon.swap_duelvar-3"]}
MUTATIONS["CountCardIDInLocation"] = {"source_symbol": "CountCardIDInLocation", "before": "\tuint16_t base = (uint16_t)((hl & 0xFF00u) | DUELVARS_CARD_LOCATIONS);", "after": "\tuint16_t base = hl;", "case_ids": ["CountCardIDInLocation-3"]}
MUTATIONS["EvolvePokemonCard"] = {"source_symbol": "EvolvePokemonCard", "before": "\t(void)PutHandCardInPlayArea(card_idx, slot);", "after": "\t(void)card_idx;", "case_ids": ["EvolvePokemonCard-0"]}
MUTATIONS["GetFirstSetPrizeCard"] = {"source_symbol": "GetFirstSetPrizeCard", "before": "\t\tif ((mask & prizes) != 0u)", "after": "\t\tif ((mask & prizes) == 0u)", "case_ids": ["GetFirstSetPrizeCard-1", "GetFirstSetPrizeCard-2", "GetFirstSetPrizeCard-6"]}
# <<< factory-mutation GetFirstSetPrizeCard
# >>> factory-mutation DrawCheckMenuCursor_YourOrOppPlayArea
MUTATIONS["DrawCheckMenuCursor_YourOrOppPlayArea"] = {
    "source_symbol": "DrawCheckMenuCursor_YourOrOppPlayArea",
    "before": "c = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1) + 14u);",
    "after": "c = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1) + 13u);",
    "case_ids": ["DrawCheckMenuCursor_YourOrOppPlayArea-1",
                 "DrawCheckMenuCursor_YourOrOppPlayArea-2"],
}
# <<< factory-mutation DrawCheckMenuCursor_YourOrOppPlayArea
# >>> factory-mutation ZeroObjectPositionsWithCopyToggleOn
MUTATIONS["ZeroObjectPositionsWithCopyToggleOn"] = {
    "source_symbol": "ZeroObjectPositionsWithCopyToggleOn",
    "before": "wVBlankOAMCopyToggle = TRUE_8BF2;",
    "after": "wVBlankOAMCopyToggle = 0u;",
    "case_ids": ["ZeroObjectPositionsWithCopyToggleOn-0",
                 "ZeroObjectPositionsWithCopyToggleOn-1"],
}
# <<< factory-mutation ZeroObjectPositionsWithCopyToggleOn
# >>> factory-mutation YourOrOppPlayAreaScreen_HandleInput
MUTATIONS["YourOrOppPlayAreaScreen_HandleInput"] = {
    "source_symbol": "YourOrOppPlayAreaScreen_HandleInput",
    "before": "\t\t\tuint16_t tbl = (uint16_t)(hl + 3u);",
    "after": "\t\t\tuint16_t tbl = (uint16_t)(hl + 4u);",
    "case_ids": ["YourOrOppPlayAreaScreen_HandleInput-1", "YourOrOppPlayAreaScreen_HandleInput-2", "YourOrOppPlayAreaScreen_HandleInput-3", "YourOrOppPlayAreaScreen_HandleInput-5"],
}
# <<< factory-mutation YourOrOppPlayAreaScreen_HandleInput
# >>> factory-mutation DrawPlayArea_BenchCards
MUTATIONS["DrawPlayArea_BenchCards"] = {
    "source_symbol": "DrawPlayArea_BenchCards",
    "before": "tile = (uint8_t)((uint8_t)(stage << 2) + BPA_TILE_STAGE_BASE);",
    "after": "tile = (uint8_t)((uint8_t)(stage << 1) + BPA_TILE_STAGE_BASE);",
    "case_ids": ["DrawPlayArea_BenchCards-1", "DrawPlayArea_BenchCards-2",
                 "DrawPlayArea_BenchCards-3", "DrawPlayArea_BenchCards-6"],
}
# <<< factory-mutation DrawPlayArea_BenchCards
# >>> factory-mutation EraseCheckMenuCursor_YourOrOppPlayArea
MUTATIONS["EraseCheckMenuCursor_YourOrOppPlayArea"] = {
    "source_symbol": "EraseCheckMenuCursor_YourOrOppPlayArea",
    "before": "return DrawCheckMenuCursor_YourOrOppPlayArea(BPA_SYM_SPACE);",
    "after": "return DrawCheckMenuCursor_YourOrOppPlayArea(BPA_SYM_CURSOR_R);",
    "case_ids": ["EraseCheckMenuCursor_YourOrOppPlayArea-0",
                 "EraseCheckMenuCursor_YourOrOppPlayArea-1"],
}
# <<< factory-mutation EraseCheckMenuCursor_YourOrOppPlayArea
# >>> factory-mutation LoadCursorTile
MUTATIONS["LoadCursorTile"] = {
    "source_symbol": "LoadCursorTile",
    "before": "0xE0u, 0xC0u, 0x98u, 0xB0u,",
    "after": "0xE1u, 0xC0u, 0x98u, 0xB0u,",
    "case_ids": ["LoadCursorTile-0", "LoadCursorTile-1", "LoadCursorTile-2"],
}
# <<< factory-mutation LoadCursorTile
# >>> factory-mutation Func_8bf2
MUTATIONS["Func_8bf2"] = {
    "source_symbol": "Func_8bf2",
    "before": "FillRectangle(PRIZE_TILE, 1u, 1u, de, 0x0000u);",
    "after": "FillRectangle((uint8_t)(PRIZE_TILE + 1u), 1u, 1u, de, 0x0000u);",
    "case_ids": ["Func_8bf2-1", "Func_8bf2-2", "Func_8bf2-3"],
}
# <<< factory-mutation Func_8bf2
# >>> factory-mutation GetDuelInitialPrizesUpperBitsSet
MUTATIONS["GetDuelInitialPrizesUpperBitsSet"] = {"source_symbol": "GetDuelInitialPrizesUpperBitsSet", "before": "\ta = (uint8_t)(b | 0xC0u);", "after": "\ta = (uint8_t)(b | 0x80u);", "case_ids": ["GetDuelInitialPrizesUpperBitsSet-0", "GetDuelInitialPrizesUpperBitsSet-1", "GetDuelInitialPrizesUpperBitsSet-2", "GetDuelInitialPrizesUpperBitsSet-3"]}
# <<< factory-mutation GetDuelInitialPrizesUpperBitsSet
# >>> factory-mutation DrawYourOrOppPlayArea_DrawArrows
MUTATIONS["DrawYourOrOppPlayArea_DrawArrows"] = {
    "source_symbol": "DrawYourOrOppPlayArea_DrawArrows",
    "before": "WriteByteToBGMap0(tile, 5u, 5u);",
    "after": "WriteByteToBGMap0(tile, 6u, 5u);",
    "case_ids": ["DrawYourOrOppPlayArea_DrawArrows-0",
                 "DrawYourOrOppPlayArea_DrawArrows-6"],
}
# <<< factory-mutation DrawYourOrOppPlayArea_DrawArrows
# >>> factory-mutation DrawYourOrOppPlayArea_EraseArrows
MUTATIONS["DrawYourOrOppPlayArea_EraseArrows"] = {
    "source_symbol": "DrawYourOrOppPlayArea_EraseArrows",
    "before": "\tDrawYourOrOppPlayArea_DrawArrows(a, SYM_SPACE);",
    "after": "\tDrawYourOrOppPlayArea_DrawArrows(a, 0x01u);",
    "case_ids": ["DrawYourOrOppPlayArea_EraseArrows-0",
                 "DrawYourOrOppPlayArea_EraseArrows-1"],
}
# <<< factory-mutation DrawYourOrOppPlayArea_EraseArrows
# >>> factory-mutation DrawYourOrOppPlayArea_RefreshArrows
MUTATIONS["DrawYourOrOppPlayArea_RefreshArrows"] = {
    "source_symbol": "DrawYourOrOppPlayArea_RefreshArrows",
    "before": "\tif (position != gb_read8(wYourOrOppPlayAreaLastCursorPosition_ADDR)) {",
    "after": "\tif (position == gb_read8(wYourOrOppPlayAreaLastCursorPosition_ADDR)) {",
    "case_ids": ["DrawYourOrOppPlayArea_RefreshArrows-1", "DrawYourOrOppPlayArea_RefreshArrows-2"],
}
# <<< factory-mutation DrawYourOrOppPlayArea_RefreshArrows
# >>> factory-mutation SendAttackDataToLinkOpponent
MUTATIONS["SendAttackDataToLinkOpponent"] = {"source_symbol": "SendAttackDataToLinkOpponent", "before": "wSentAttackDataToLinkOpponent = TRUE;", "after": "wSentAttackDataToLinkOpponent = 0u;", "case_ids": ["SendAttackDataToLinkOpponent-1", "SendAttackDataToLinkOpponent-2"]}
# <<< factory-mutation SendAttackDataToLinkOpponent
# >>> factory-mutation DrawPlayArea_PrizeCards
MUTATIONS["DrawPlayArea_PrizeCards"] = {"source_symbol": "DrawPlayArea_PrizeCards", "before": "\t\tuint8_t taken = (uint8_t)(prize_bits & 1u);", "after": "\t\tuint8_t taken = (uint8_t)(prize_bits & 2u);", "case_ids": ["DrawPlayArea_PrizeCards-0", "DrawPlayArea_PrizeCards-1", "DrawPlayArea_PrizeCards-2"]}
# <<< factory-mutation DrawPlayArea_PrizeCards
# >>> factory-mutation _DrawPlayersPrizeAndBenchCards
MUTATIONS["_DrawPlayersPrizeAndBenchCards"] = {"source_symbol": "_DrawPlayersPrizeAndBenchCards", "before": "\twCheckMenuPlayAreaWhichLayout = PLAYER_TURN;", "after": "\twCheckMenuPlayAreaWhichLayout = OPPONENT_TURN;", "case_ids": ["_DrawPlayersPrizeAndBenchCards-0", "_DrawPlayersPrizeAndBenchCards-1"]}
# <<< factory-mutation _DrawPlayersPrizeAndBenchCards
# >>> factory-mutation DrawPlayArea_HandText
MUTATIONS["DrawPlayArea_HandText"] = {"source_symbol": "DrawPlayArea_HandText", "before": "gb_write8(p, tens); p++;", "after": "gb_write8(p, (uint8_t)(tens + 1u)); p++;", "case_ids": ["DrawPlayArea_HandText-0", "DrawPlayArea_HandText-2"]}
# <<< factory-mutation DrawPlayArea_HandText
# >>> factory-mutation DrawPlayArea_IconWithValue
MUTATIONS["DrawPlayArea_IconWithValue"] = {"source_symbol": "DrawPlayArea_IconWithValue", "before": "\tgb_write8((uint16_t)(wDefaultText_ADDR + 1u), SYM_CROSS);", "after": "\tgb_write8((uint16_t)(wDefaultText_ADDR + 1u), 0x2Eu);", "case_ids": ["DrawPlayArea_IconWithValue-0", "DrawPlayArea_IconWithValue-1"]}
# <<< factory-mutation DrawPlayArea_IconWithValue
# >>> factory-mutation SaveDuelStateToSRAM
MUTATIONS["SaveDuelStateToSRAM"] = {"source_symbol": "SaveDuelStateToSRAM", "before": "gb_write8(s0a008_ADDR, (uint8_t)(old + 1u));", "after": "gb_write8(s0a008_ADDR, (uint8_t)(old + 2u));", "case_ids": ["SaveDuelStateToSRAM-0", "SaveDuelStateToSRAM-1"]}
# <<< factory-mutation SaveDuelStateToSRAM
# >>> factory-mutation DisplayCheckMenuCursor_YourOrOppPlayArea
MUTATIONS["DisplayCheckMenuCursor_YourOrOppPlayArea"] = {"source_symbol": "DisplayCheckMenuCursor_YourOrOppPlayArea", "before": "\treturn DrawCheckMenuCursor_YourOrOppPlayArea(SYM_CURSOR_R);", "after": "\treturn DrawCheckMenuCursor_YourOrOppPlayArea((uint8_t)(SYM_CURSOR_R + 1u));", "case_ids": ["DisplayCheckMenuCursor_YourOrOppPlayArea-0", "DisplayCheckMenuCursor_YourOrOppPlayArea-1"]}
# <<< factory-mutation DisplayCheckMenuCursor_YourOrOppPlayArea
# >>> factory-mutation HandleCheckMenuInput_YourOrOppPlayArea
MUTATIONS["HandleCheckMenuInput_YourOrOppPlayArea"] = {
    "source_symbol": "HandleCheckMenuInput_YourOrOppPlayArea",
    "before": "\t\treturn (TempListResult){MENU_CANCEL, 0x90u};",
    "after": "\t\treturn (TempListResult){MENU_CANCEL, 0x10u};",
    "case_ids": ["HandleCheckMenuInput_YourOrOppPlayArea-2"],
}
# <<< factory-mutation HandleCheckMenuInput_YourOrOppPlayArea
# >>> factory-mutation DrawYourOrOppPlayArea_Icons
MUTATIONS["DrawYourOrOppPlayArea_Icons"] = {"source_symbol": "DrawYourOrOppPlayArea_Icons", "before": "\tDrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);", "after": "\tDrawPlayArea_IconWithValue(0xD8u, (uint8_t)(discard_count + 1u), &coords);", "case_ids": ["DrawYourOrOppPlayArea_Icons-0", "DrawYourOrOppPlayArea_Icons-1"]}
# <<< factory-mutation DrawYourOrOppPlayArea_Icons
# >>> factory-mutation DrawInPlayArea_Icons
MUTATIONS["DrawInPlayArea_Icons"] = {"source_symbol": "DrawInPlayArea_Icons", "before": "\tpage = hWhoseTurn;\n\tuint8_t discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));\n\tDrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);", "after": "\tpage = hWhoseTurn;\n\tuint8_t discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));\n\tDrawPlayArea_IconWithValue(0xD8u, (uint8_t)(discard_count + 1u), &coords);", "case_ids": ["DrawInPlayArea_Icons-0", "DrawInPlayArea_Icons-1"]}
# <<< factory-mutation DrawInPlayArea_Icons
# >>> factory-mutation DisplayUsePokemonPowerScreen_WaitForInput
MUTATIONS["DisplayUsePokemonPowerScreen_WaitForInput"] = {"source_symbol": "DisplayUsePokemonPowerScreen_WaitForInput", "before": "\treturn DrawWideTextBox_WaitForInput_ReturnCarry(hl);", "after": "\treturn 0u;", "case_ids": ["DisplayUsePokemonPowerScreen_WaitForInput-0", "DisplayUsePokemonPowerScreen_WaitForInput-1"]}
# <<< factory-mutation DisplayUsePokemonPowerScreen_WaitForInput
# >>> factory-mutation _DrawPlayAreaToPlacePrizeCards
MUTATIONS["_DrawPlayAreaToPlacePrizeCards"] = {"source_symbol": "_DrawPlayAreaToPlacePrizeCards", "before": "\tgb_write8(wIsSwapTurnPending_ADDR, TRUE);", "after": "\tgb_write8(wIsSwapTurnPending_ADDR, 0u);", "case_ids": ["_DrawPlayAreaToPlacePrizeCards-0", "_DrawPlayAreaToPlacePrizeCards-1"]}
# <<< factory-mutation _DrawPlayAreaToPlacePrizeCards
# >>> factory-mutation UsePokemonPower
MUTATIONS["UsePokemonPower"] = {
    "source_symbol": "UsePokemonPower",
    "before": "\treturn (UsePokemonPowerResult){a, f, b, c, d, e, hl};",
    "after": "\treturn (UsePokemonPowerResult){a, 0u, b, c, d, e, hl};",
    "case_ids": ["UsePokemonPower-0", "UsePokemonPower-1"],
}
# <<< factory-mutation UsePokemonPower
# >>> factory-mutation DrawYourOrOppPlayArea_ActiveCardGfx
MUTATIONS["DrawYourOrOppPlayArea_ActiveCardGfx"] = {
    "source_symbol": "DrawYourOrOppPlayArea_ActiveCardGfx",
    "before": "uint8_t arena_card = gb_read8(arena_addr);",
    "after": "uint8_t arena_card = gb_read8((uint16_t)(arena_addr + 1u));",
    "case_ids": ["DrawYourOrOppPlayArea_ActiveCardGfx-0"],
}
# <<< factory-mutation DrawYourOrOppPlayArea_ActiveCardGfx
# >>> factory-mutation _DrawYourOrOppPlayAreaScreen
MUTATIONS["_DrawYourOrOppPlayAreaScreen"] = {"source_symbol": "_DrawYourOrOppPlayAreaScreen", "before": "\tif (wCheckMenuPlayAreaWhichDuelist == PLAYER_TURN) {", "after": "\tif (wCheckMenuPlayAreaWhichDuelist != PLAYER_TURN) {", "case_ids": ["_DrawYourOrOppPlayAreaScreen-0", "_DrawYourOrOppPlayAreaScreen-1"]}
# <<< factory-mutation _DrawYourOrOppPlayAreaScreen
# >>> factory-mutation DrawYourOrOppPlayAreaScreen
MUTATIONS["DrawYourOrOppPlayAreaScreen"] = {"source_symbol": "DrawYourOrOppPlayAreaScreen", "before": "\twCheckMenuPlayAreaWhichDuelist = (uint8_t)(hl >> 8);", "after": "\twCheckMenuPlayAreaWhichDuelist = (uint8_t)hl;", "case_ids": ["DrawYourOrOppPlayAreaScreen-0", "DrawYourOrOppPlayAreaScreen-1"]}
# <<< factory-mutation DrawYourOrOppPlayAreaScreen
# >>> factory-mutation _DrawAIPeekScreen
MUTATIONS["_DrawAIPeekScreen"] = {"source_symbol": "_DrawAIPeekScreen", "before": "\tif ((b & 0x80u) != 0u) {", "after": "\tif ((b & 0x80u) == 0u) {", "case_ids": ["_DrawAIPeekScreen-0", "_DrawAIPeekScreen-1"]}
# <<< factory-mutation _DrawAIPeekScreen
# >>> factory-mutation PrintPokemonsAttackText
MUTATIONS["PrintPokemonsAttackText"] = {"source_symbol": "PrintPokemonsAttackText", "before": "\tgb_write8((uint16_t)(wTxRam2_ADDR + 2u), gb_read8(wLoadedAttackName_ADDR));", "after": "\tgb_write8((uint16_t)(wTxRam2_ADDR + 2u), gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u)));", "case_ids": ["PrintPokemonsAttackText-0", "PrintPokemonsAttackText-1"]}
# <<< factory-mutation PrintPokemonsAttackText
# >>> factory-mutation PrintFailedEffectText
MUTATIONS["PrintFailedEffectText"] = {"source_symbol": "PrintFailedEffectText", "before": "\t\treturn (PrintFailedEffectTextResult){0x80u};", "after": "\t\treturn (PrintFailedEffectTextResult){0x00u};", "case_ids": ["PrintFailedEffectText-0", "PrintFailedEffectText-1"]}
# <<< factory-mutation PrintFailedEffectText
# >>> factory-mutation DrawInPlayArea_ActiveCardGfx
MUTATIONS["DrawInPlayArea_ActiveCardGfx"] = {"source_symbol": "DrawInPlayArea_ActiveCardGfx", "before": "\t\tLoadCardGfx(gfx, 0x8A00u, 0x30u, TILE_SIZE);", "after": "\t\tLoadCardGfx(gfx, 0x8A00u, 0x30u, 0x08u);", "case_ids": ["DrawInPlayArea_ActiveCardGfx-3"]}
# <<< factory-mutation DrawInPlayArea_ActiveCardGfx
# >>> factory-mutation DrawInPlayAreaScreen
MUTATIONS["DrawInPlayAreaScreen"] = {
    "source_symbol": "DrawInPlayAreaScreen",
    "before": "wTileMapFill = 0u;",
    "after": "wTileMapFill = 1u;",
    "case_ids": ["DrawInPlayAreaScreen-0", "DrawInPlayAreaScreen-1"],
}
# <<< factory-mutation DrawInPlayAreaScreen
# >>> factory-mutation DrawDuelMainScene_PrintPokemonsAttackText
MUTATIONS["DrawDuelMainScene_PrintPokemonsAttackText"] = {"source_symbol": "DrawDuelMainScene_PrintPokemonsAttackText", "before": "\treturn PrintPokemonsAttackText();", "after": "\treturn (PrintPokemonsAttackTextResult){0};", "case_ids": ["DrawDuelMainScene_PrintPokemonsAttackText-0", "DrawDuelMainScene_PrintPokemonsAttackText-1"]}
# <<< factory-mutation DrawDuelMainScene_PrintPokemonsAttackText
# >>> factory-mutation ProcessPlayedPokemonCard
MUTATIONS["ProcessPlayedPokemonCard"] = {"source_symbol": "ProcessPlayedPokemonCard", "before": "\thl = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)", "after": "\thl = (uint16_t)(wLoadedCard1Name_ADDR", "case_ids": ["ProcessPlayedPokemonCard-2"]}
# <<< factory-mutation ProcessPlayedPokemonCard
# >>> factory-mutation _SelectPrizeCards
MUTATIONS["_SelectPrizeCards"] = {"source_symbol": "_SelectPrizeCards", "before": "\t\tAddCardToHand(deck_index);", "after": "", "case_ids": ["_SelectPrizeCards-0"]}
# <<< factory-mutation _SelectPrizeCards
# >>> factory-mutation PlayTrainerCard
MUTATIONS["PlayTrainerCard"] = {"source_symbol": "PlayTrainerCard", "before": "\tWaitResult used = DisplayUsedTrainerCardDetailScreen();\n\ta = used.a;\n\tb = used.b;\n\tc = used.c;\n\td = used.d;\n\te = used.e;", "after": "\tWaitResult used = DisplayUsedTrainerCardDetailScreen();\n\ta = used.a;\n\tb = used.b;\n\tc = used.c;\n\t(void)used.d;\n\t(void)used.e;", "case_ids": ["PlayTrainerCard-0"]}
# <<< factory-mutation PlayTrainerCard
# >>> factory-mutation CheckSelfConfusionDamage
MUTATIONS["CheckSelfConfusionDamage"] = {"source_symbol": "CheckSelfConfusionDamage", "before": "\twConfusionAttackCheckWasUnsuccessful = 0u;", "after": "\twConfusionAttackCheckWasUnsuccessful = 0x40u;", "case_ids": ["CheckSelfConfusionDamage-0", "CheckSelfConfusionDamage-2"]}
# <<< factory-mutation CheckSelfConfusionDamage
# >>> factory-mutation ApplyTransparencyIfApplicable
MUTATIONS["ApplyTransparencyIfApplicable"] = {"source_symbol": "ApplyTransparencyIfApplicable", "before": "\tuint8_t loaded_category = wLoadedAttackCategory;", "after": "\tuint8_t loaded_category = 0x80u;", "case_ids": ["ApplyTransparencyIfApplicable-2"]}
# <<< factory-mutation ApplyTransparencyIfApplicable
#
# >>> factory-mutation DealDamageToPlayAreaPokemon
MUTATIONS["DealDamageToPlayAreaPokemon"] = {"source_symbol": "DealDamageToPlayAreaPokemon", "before": "DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon(uint8_t b, uint16_t de, uint16_t hl)\n{\n\twTempPlayAreaLocation_cceb = b;", "after": "DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon(uint8_t b, uint16_t de, uint16_t hl)\n{\n\twTempPlayAreaLocation_cceb = (uint8_t)(b ^ 1u);", "case_ids": ["DealDamageToPlayAreaPokemon-0", "DealDamageToPlayAreaPokemon-1"]}
# <<< factory-mutation DealDamageToPlayAreaPokemon
# >>> factory-mutation DealDamageToPlayAreaPokemon_RegularAnim
MUTATIONS["DealDamageToPlayAreaPokemon_RegularAnim"] = {"source_symbol": "DealDamageToPlayAreaPokemon_RegularAnim", "before": "DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon_RegularAnim(uint8_t b, uint16_t de, uint16_t hl)\n{\n\twLoadedAttackAnimation = ATK_ANIM_BENCH_HIT;", "after": "DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon_RegularAnim(uint8_t b, uint16_t de, uint16_t hl)\n{\n\twLoadedAttackAnimation = (uint8_t)(ATK_ANIM_BENCH_HIT ^ 1u);", "case_ids": ["DealDamageToPlayAreaPokemon_RegularAnim-0", "DealDamageToPlayAreaPokemon_RegularAnim-1"]}
# <<< factory-mutation DealDamageToPlayAreaPokemon_RegularAnim
# >>> factory-mutation DealConfusionDamageToSelf
MUTATIONS["DealConfusionDamageToSelf"] = {"source_symbol": "DealConfusionDamageToSelf", "before": "\tgb_write8(wDamage_ADDR, a);\n\tgb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);", "after": "\tgb_write8(wDamage_ADDR, (uint8_t)(a + 1u));\n\tgb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);", "case_ids": ["DealConfusionDamageToSelf-0", "DealConfusionDamageToSelf-2", "DealConfusionDamageToSelf-3"]}
# <<< factory-mutation DealConfusionDamageToSelf

# >>> factory-mutation Func_1bb4
MUTATIONS["Func_1bb4"] = {
    "source_symbol": "Func_1bb4",
    "before": "\tgb_write8(hTempPlayAreaLocation_ff9d_ADDR, 0u); /* xor a ; PLAY_AREA_ARENA */",
    "after": "\tgb_write8(hTempPlayAreaLocation_ff9d_ADDR, 1u); /* xor a ; PLAY_AREA_ARENA */",
    "case_ids": ["Func_1bb4-0"],
}
# <<< factory-mutation Func_1bb4
# >>> factory-mutation Func_82b6
MUTATIONS["Func_82b6"] = {'source_symbol': 'Func_82b6', 'before': 'duelist == layout ?', 'after': 'duelist != layout ?', 'case_ids': ['Func_82b6-0', 'Func_82b6-1', 'Func_82b6-2']}
# <<< factory-mutation Func_82b6
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile
MUTATIONS["OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile", "before": "void OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;\n\t(void)OpenTurnHolderDiscardPileScreen(c);", "after": "void OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;\n\t(void)0;", "case_ids": ["OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile-0", "OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile-1", "OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile-2"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderHand
MUTATIONS["OpenYourOrOppPlayAreaScreen_NonTurnHolderHand"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_NonTurnHolderHand", "before": "void OpenYourOrOppPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "void OpenYourOrOppPlayAreaScreen_NonTurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenYourOrOppPlayAreaScreen_NonTurnHolderHand-0", "OpenYourOrOppPlayAreaScreen_NonTurnHolderHand-1"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderHand
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderHand
MUTATIONS["OpenYourOrOppPlayAreaScreen_TurnHolderHand"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_TurnHolderHand", "before": "uint8_t OpenYourOrOppPlayAreaScreen_TurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "uint8_t OpenYourOrOppPlayAreaScreen_TurnHolderHand(void)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenYourOrOppPlayAreaScreen_TurnHolderHand-0", "OpenYourOrOppPlayAreaScreen_TurnHolderHand-1", "OpenYourOrOppPlayAreaScreen_TurnHolderHand-2"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderHand
# >>> factory-mutation DealRecoilDamageToSelf
MUTATIONS["DealRecoilDamageToSelf"] = {"source_symbol": "DealRecoilDamageToSelf", "before": "\twLoadedAttackAnimation = ATK_ANIM_RECOIL_HIT;", "after": "\twLoadedAttackAnimation = 0u;", "case_ids": ["DealRecoilDamageToSelf-0", "DealRecoilDamageToSelf-2", "DealRecoilDamageToSelf-3"]}
# <<< factory-mutation DealRecoilDamageToSelf
# >>> factory-mutation DuelCheckMenu_Glossary
MUTATIONS["DuelCheckMenu_Glossary"] = {"source_symbol": "DuelCheckMenu_Glossary", "before": "\tOpenGlossaryScreen();", "after": "\t(void)0;", "case_ids": ["DuelCheckMenu_Glossary-1"]}
# <<< factory-mutation DuelCheckMenu_Glossary
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile
MUTATIONS["OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile", "before": "void OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = hWhoseTurn;", "after": "void OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c)\n{\n\tuint8_t saved_hWhoseTurn = 0u;", "case_ids": ["OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile-0", "OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile-1", "OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile-2"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile
# >>> factory-mutation _HandlePeekSelection
MUTATIONS["_HandlePeekSelection"] = {
    "source_symbol": "_HandlePeekSelection",
    "before": "\t\t\t\twce5c = (uint8_t)(position + 0x40u);",
    "after": "\t\t\t\twce5c = (uint8_t)(position + 0x41u);",
    "case_ids": ["_HandlePeekSelection-0", "_HandlePeekSelection-1"],
}
# <<< factory-mutation _HandlePeekSelection
# >>> factory-mutation _OpenDuelCheckMenu
MUTATIONS["_OpenDuelCheckMenu"] = {"source_symbol": "_OpenDuelCheckMenu", "before": "\t\twce5e = 0u;\n\t\t(void)DrawWideTextBox();", "after": "\t\twce5e = 1u;\n\t\t(void)DrawWideTextBox();", "case_ids": ["_OpenDuelCheckMenu-0", "_OpenDuelCheckMenu-1"]}
# <<< factory-mutation _OpenDuelCheckMenu
# >>> factory-mutation DuelCheckMenu_InPlayArea
MUTATIONS["DuelCheckMenu_InPlayArea"] = {"source_symbol": "DuelCheckMenu_InPlayArea", "before": "void DuelCheckMenu_InPlayArea(void)\n{\n\twInPlayAreaFromSelectButton = 0u;", "after": "void DuelCheckMenu_InPlayArea(void)\n{\n\twInPlayAreaFromSelectButton = 1u;", "case_ids": ["DuelCheckMenu_InPlayArea-0", "DuelCheckMenu_InPlayArea-1"]}
# <<< factory-mutation DuelCheckMenu_InPlayArea
# >>> factory-completion DuelCheckMenu_InPlayArea
# menus/duel.asm:39 now really enters OpenInPlayAreaScreen, whose input loop
# only exits on a keypress, so `pre-ret` stopped the reference while the native
# lane ran into the loop. Both stop at the screen draw the loop opens with.
for _record in SCHEMA2_CASES["DuelCheckMenu_InPlayArea"]:
    _record["completion"] = {"mode": "entry", "pc": sym("DrawInPlayAreaScreen"), "bank": sym_bank("DrawInPlayAreaScreen"),
                             "routine": "DrawInPlayAreaScreen"}
# <<< factory-completion DuelCheckMenu_InPlayArea
# >>> factory-mutation DuelCheckMenu_YourPlayArea
MUTATIONS["DuelCheckMenu_YourPlayArea"] = {"source_symbol": "DuelCheckMenu_YourPlayArea", "before": "void DuelCheckMenu_YourPlayArea(void)\n{\n\tResetCheckMenuCursorPositionAndBlink();\n\twce5e = 0u;", "after": "void DuelCheckMenu_YourPlayArea(void)\n{\n\tResetCheckMenuCursorPositionAndBlink();\n\twce5e = 0x80u;", "case_ids": ["DuelCheckMenu_YourPlayArea-0", "DuelCheckMenu_YourPlayArea-1"]}
# <<< factory-mutation DuelCheckMenu_YourPlayArea
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea
MUTATIONS["OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea", "before": "\t(void)OpenTurnHolderPlayAreaScreen();", "after": "", "case_ids": ["OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea-0"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea
# >>> factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea
MUTATIONS["OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea"] = {"source_symbol": "OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea", "before": "\tOpenNonTurnHolderPlayAreaScreen();", "after": "", "case_ids": ["OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea-0"]}
# <<< factory-mutation OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea
# >>> factory-mutation DuelCheckMenu_OppPlayArea
MUTATIONS["DuelCheckMenu_OppPlayArea"] = {"source_symbol": "DuelCheckMenu_OppPlayArea", "before": "void DuelCheckMenu_OppPlayArea(void)\n{\n\tResetCheckMenuCursorPositionAndBlink();\n\tPkmnPowerCountResult clairvoyance = IsClairvoyanceActive();\n\twce5e = (clairvoyance.f & 0x10u) != 0u ? 0u : 0x80u;", "after": "void DuelCheckMenu_OppPlayArea(void)\n{\n\tResetCheckMenuCursorPositionAndBlink();\n\tPkmnPowerCountResult clairvoyance = IsClairvoyanceActive();\n\twce5e = (clairvoyance.f & 0x10u) != 0u ? 0u : 0x81u;", "case_ids": ["DuelCheckMenu_OppPlayArea-0", "DuelCheckMenu_OppPlayArea-1"]}
# <<< factory-mutation DuelCheckMenu_OppPlayArea
# >>> factory-mutation HandleConfusionDamageToSelf
MUTATIONS["HandleConfusionDamageToSelf"] = {"source_symbol": "HandleConfusionDamageToSelf", "before": "DealConfusionDamageToSelf(20u, 0u, 0u, 0u);", "after": "DealConfusionDamageToSelf(10u, 0u, 0u, 0u);", "case_ids": ["HandleConfusionDamageToSelf-0"]}
# <<< factory-mutation HandleConfusionDamageToSelf
# >>> factory-mutation HandleAfterDamageEffects
MUTATIONS["HandleAfterDamageEffects"] = {"source_symbol": "HandleAfterDamageEffects", "before": "\tHandleBetweenTurnKnockOutsResult knockouts = HandleDestinyBondAndBetweenTurnKnockOuts();", "after": "\tHandleBetweenTurnKnockOutsResult knockouts = {0u, 0x80u};", "case_ids": ["HandleAfterDamageEffects-1"]}
# <<< factory-mutation HandleAfterDamageEffects
# >>> factory-mutation Func_17ed
MUTATIONS["Func_17ed"] = {"source_symbol": "Func_17ed", "before": "HandleAfterDamageEffectsResult Func_17ed(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tWaitResult waited = DrawWideTextBox_WaitForInput(hl);\n\ta = 0u;\n\tf = waited.f;\n\tgb_write8(wDamage_ADDR, 0u);", "after": "HandleAfterDamageEffectsResult Func_17ed(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tWaitResult waited = DrawWideTextBox_WaitForInput(hl);\n\ta = 0u;\n\tf = waited.f;\n\tgb_write8(wDamage_ADDR, 0x01u);", "case_ids": ["Func_17ed-0", "Func_17ed-1"]}
# <<< factory-mutation Func_17ed
# >>> factory-mutation PlayAttackAnimation_DealAttackDamage
MUTATIONS["PlayAttackAnimation_DealAttackDamage"] = {"source_symbol": "PlayAttackAnimation_DealAttackDamage", "before": "\t(void)SubtractHP(hp.hl, de);", "after": "", "case_ids": ["PlayAttackAnimation_DealAttackDamage-0"]}
# <<< factory-mutation PlayAttackAnimation_DealAttackDamage
# >>> factory-mutation UseAttackOrPokemonPower
MUTATIONS["UseAttackOrPokemonPower"] = {"source_symbol": "UseAttackOrPokemonPower", "before": "DuelRoutineResult UseAttackOrPokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = wSelectedAttack;\n\twPlayerAttackingAttackIndex = a;", "after": "DuelRoutineResult UseAttackOrPokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = wSelectedAttack;\n\twPlayerAttackingAttackIndex = (uint8_t)(a ^ 1u);", "case_ids": ["UseAttackOrPokemonPower-0", "UseAttackOrPokemonPower-1"]}
# <<< factory-mutation UseAttackOrPokemonPower
MUTATIONS["AddCardToHand"] = {
    "source_symbol": "AddCardToHand",
    "before": "\tgb_write8((uint16_t)(page | a), CARD_LOCATION_HAND);",
    "after": "\tgb_write8((uint16_t)(page & a), CARD_LOCATION_HAND);",
    "case_ids": ["AddCardToHand-1"],
}
MUTATIONS["ApplyAttachedDefender"] = {
    "source_symbol": "ApplyAttachedDefender",
    "before": "\tuint16_t product = (uint16_t)(count * 20u);",
    "after": "\tuint16_t product = (uint16_t)(count * 21u);",
    "case_ids": ["ApplyAttachedDefender-0"],
}
MUTATIONS["ApplyAttachedPlusPower"] = {
    "source_symbol": "ApplyAttachedPlusPower",
    "before": "\tuint16_t product = (uint16_t)(count * 10u);",
    "after": "\tuint16_t product = (uint16_t)(count * 11u);",
    "case_ids": ["ApplyAttachedPlusPower-0"],
}
MUTATIONS["ApplyDamageModifiers_DamageToSelf"] = {
    "source_symbol": "ApplyDamageModifiers_DamageToSelf",
    "before": "\tuint8_t nonzero = (uint8_t)(hi_byte | lo);",
    "after": "\tuint8_t nonzero = (uint8_t)(hi_byte & lo);",
    "case_ids": ["ApplyDamageModifiers_DamageToSelf-1"],
}
MUTATIONS["ApplyDamageModifiers_DamageToTarget"] = {
    "source_symbol": "ApplyDamageModifiers_DamageToTarget",
    "before": "\t\tde &= (uint16_t)~0x8000u;",
    "after": "\t\tde &= (uint16_t)~0x7FFFu;",
    "case_ids": ["ApplyDamageModifiers_DamageToTarget-5"],
}
MUTATIONS["CheckIfCanEvolveInto"] = {
    "source_symbol": "CheckIfCanEvolveInto",
    "before": "\tif (gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) !=",
    "after": "\tif (gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) ==",
    "case_ids": ["CheckIfCanEvolveInto-0"],
}
MUTATIONS["CheckIfCanEvolveInto_BasicToStage2"] = {
    "source_symbol": "CheckIfCanEvolveInto_BasicToStage2",
    "before": "\tif (byte1 != gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))",
    "after": "\tif (byte1 == gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))",
    "case_ids": ["CheckIfCanEvolveInto_BasicToStage2-0"],
}
MUTATIONS["CheckLoadedAttackFlag"] = {
    "source_symbol": "CheckLoadedAttackFlag",
    "before": "\tuint8_t bit = (uint8_t)(1u << (a & 0x07u));",
    "after": "\tuint8_t bit = (uint8_t)(1u << (a & 0x08u));",
    "case_ids": ["CheckLoadedAttackFlag-1"],
}
MUTATIONS["CheckPrizeTaken"] = {
    "source_symbol": "CheckPrizeTaken",
    "before": "\tuint8_t mask = rom_ptr(PowersOf2_BANK, PowersOf2_ADDR)[a];",
    "after": "\tuint8_t mask = rom_ptr(PowersOf2_BANK, InvertedPowersOf2_ADDR)[a];",
    "case_ids": ["CheckPrizeTaken-0"],
}
MUTATIONS["ClearAllStatusConditions"] = {
    "source_symbol": "ClearAllStatusConditions",
    "before": "\tuint16_t sub3_addr = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS3);",
    "after": "\tuint16_t sub3_addr = (uint16_t)(page & DUELVARS_ARENA_CARD_SUBSTATUS3);",
    "case_ids": ["ClearAllStatusConditions-0"],
}
MUTATIONS["CopyAttackDataAndDamage"] = {
    "source_symbol": "CopyAttackDataAndDamage",
    "before": "\tuint16_t src = (e == 1) ? wLoadedCard1Atk2_ADDR : wLoadedCard1Atk1_ADDR;",
    "after": "\tuint16_t src = (e != 1) ? wLoadedCard1Atk2_ADDR : wLoadedCard1Atk1_ADDR;",
    "case_ids": ["CopyAttackDataAndDamage-0"],
}
MUTATIONS["CopyAttackDataAndDamage_FromCardID"] = {
    "source_symbol": "CopyAttackDataAndDamage_FromCardID",
    "before": "\tLoadCardDataToBuffer1_FromCardID(a);",
    "after": "\t;",
    "case_ids": ["CopyAttackDataAndDamage_FromCardID-0"],
}
MUTATIONS["CopyDeckData"] = {
    "source_symbol": "CopyDeckData",
    "before": "\tf = last_value ? 0x00u : 0x90u;",
    "after": "\tf = last_value ? 0x01u : 0x90u;",
    "case_ids": ["CopyDeckData-2"],
}
MUTATIONS["CopyOpponentName"] = {
    "source_symbol": "CopyOpponentName",
    "before": "\t\treturn copy_name_loop(wNameBuffer_ADDR, de);",
    "after": "\t\treturn copy_name_loop(wNameBuffer_ADDR, (uint16_t)(de ^ 1u));",
    "case_ids": ["CopyOpponentName-0"],
}
MUTATIONS["CopyPlayerName"] = {
    "source_symbol": "CopyPlayerName",
    "before": "\treturn copy_name_loop(sPlayerName_ADDR, de);",
    "after": "\treturn copy_name_loop(sPlayerName_ADDR, (uint16_t)(de ^ 1u));",
    "case_ids": ["CopyPlayerName-0"],
}
MUTATIONS["CountCardsInDuelTempList"] = {
    "source_symbol": "CountCardsInDuelTempList",
    "before": "\twhile (gb_read8((uint16_t)(wDuelTempList_ADDR + count)) != 0xFF)",
    "after": "\twhile (gb_read8((uint16_t)(wDuelTempList_ADDR + count)) == 0xFF)",
    "case_ids": ["CountCardsInDuelTempList-0"],
}
MUTATIONS["CountPrizes"] = {
    "source_symbol": "CountPrizes",
    "before": "\t\tcount = (uint8_t)(count + (mask & 1u));",
    "after": "\t\tcount = (uint8_t)(count - (mask & 1u));",
    "case_ids": ["CountPrizes-1"],
}
MUTATIONS["CreateArenaOrBenchEnergyCardList"] = {
    "source_symbol": "CreateArenaOrBenchEnergyCardList",
    "before": "\t\tif (gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | i)) != location_mask)",
    "after": "\t\tif (gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | i)) == location_mask)",
    "case_ids": ["CreateArenaOrBenchEnergyCardList-0"],
}
MUTATIONS["CreateDeckCardList"] = {
    "source_symbol": "CreateDeckCardList",
    "before": "\tif (not_in_deck.a >= DECK_SIZE) {",
    "after": "\tif (not_in_deck.a > DECK_SIZE) {",
    "case_ids": ["CreateDeckCardList-1"],
}
MUTATIONS["CreateDiscardPileCardList"] = {
    "source_symbol": "CreateDiscardPileCardList",
    "before": "\tuint8_t f = count ? 0x00u : 0x90u;",
    "after": "\tuint8_t f = count ? 0x01u : 0x90u;",
    "case_ids": ["CreateDiscardPileCardList-1"],
}
MUTATIONS["CreateHandCardList"] = {
    "source_symbol": "CreateHandCardList",
    "before": "\tuint8_t f = hand_count ? 0x00u : 0x90u;",
    "after": "\tuint8_t f = hand_count ? 0x01u : 0x90u;",
    "case_ids": ["CreateHandCardList-0"],
}
MUTATIONS["DrawCardFromDeck"] = {
    "source_symbol": "DrawCardFromDeck",
    "before": "\tif (not_in_deck >= DECK_SIZE) {",
    "after": "\tif (not_in_deck > DECK_SIZE) {",
    "case_ids": ["DrawCardFromDeck-1"],
}
MUTATIONS["DrawWideTextBox_WaitForInput_ReturnCarry"] = {
    "source_symbol": "DrawWideTextBox_WaitForInput_ReturnCarry",
    "before": "\treturn (uint8_t)(DrawWideTextBox_WaitForInput(hl).f | 0x10u);",
    "after": "\treturn (uint8_t)(DrawWideTextBox_WaitForInput(hl).f | 0x11u);",
    "case_ids": ["DrawWideTextBox_WaitForInput_ReturnCarry-0"],
}
MUTATIONS["EmptyPlayAreaSlot"] = {
    "source_symbol": "EmptyPlayAreaSlot",
    "before": "\t(void)EmptyPlayAreaSlot_init_duelvar(DUELVARS_ARENA_CARD_HP, 0x00u, e, hl);",
    "after": "\t(void)EmptyPlayAreaSlot_init_duelvar(DUELVARS_ARENA_CARD_HP, 0x01u, e, hl);",
    "case_ids": ["EmptyPlayAreaSlot-0"],
}
MUTATIONS["EvolvePokemonCardIfPossible"] = {
    "source_symbol": "EvolvePokemonCardIfPossible",
    "before": "\tif (check.f & 0x10u)",
    "after": "\tif (check.f | 0x10u)",
    "case_ids": ["EvolvePokemonCardIfPossible-0"],
}
MUTATIONS["FindLastCardInHand"] = {
    "source_symbol": "FindLastCardInHand",
    "before": "\t\t\t\t0x00u, (uint16_t)(((uint16_t)hWhoseTurn << 8) |",
    "after": "\t\t\t\t0x01u, (uint16_t)(((uint16_t)hWhoseTurn << 8) |",
    "case_ids": ["FindLastCardInHand-0"],
}
MUTATIONS["GetCardDamageAndMaxHP"] = {
    "source_symbol": "GetCardDamageAndMaxHP",
    "before": "\tif ((max_hp & 0x0Fu) < (damage & 0x0Fu))",
    "after": "\tif ((max_hp & 0x10u) < (damage & 0x0Fu))",
    "case_ids": ["GetCardDamageAndMaxHP-1"],
}
MUTATIONS["GetNonTurnDuelistVariable"] = {
    "source_symbol": "GetNonTurnDuelistVariable",
    "before": "\tuint8_t turn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;",
    "after": "\tuint8_t turn = hWhoseTurn != PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;",
    "case_ids": ["GetNonTurnDuelistVariable-0"],
}
MUTATIONS["GetPlayAreaCardAttachedEnergies"] = {
    "source_symbol": "GetPlayAreaCardAttachedEnergies",
    "before": "\t\tif (gb_read8((uint16_t)(page | l)) != location)",
    "after": "\t\tif (gb_read8((uint16_t)(page | l)) == location)",
    "case_ids": ["GetPlayAreaCardAttachedEnergies-0"],
}
MUTATIONS["GetTurnDuelistVariable"] = {
    "source_symbol": "GetTurnDuelistVariable",
    "before": "\tuint16_t address = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);",
    "after": "\tuint16_t address = (uint16_t)(((uint16_t)hWhoseTurn << 8) & a);",
    "case_ids": ["GetTurnDuelistVariable-0"],
}
MUTATIONS["CopyAttackDataAndDamage_FromDeckIndex"] = {
    "source_symbol": "CopyAttackDataAndDamage_FromDeckIndex",
    "before": "AttackCopyResult CopyAttackDataAndDamage_FromDeckIndex(uint8_t d, uint8_t e)\n{\n\tgb_write8(wSelectedAttack_ADDR, e);",
    "after": "AttackCopyResult CopyAttackDataAndDamage_FromDeckIndex(uint8_t d, uint8_t e)\n{\n\tgb_write8(wSelectedAttack_ADDR, (uint8_t)(e ^ 1u));",
    "case_ids": ["CopyAttackDataAndDamage_FromDeckIndex-0"],
}
MUTATIONS["GetCardInDuelTempList"] = {
    "source_symbol": "GetCardInDuelTempList",
    "before": "DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl)\n{\n\tuint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));",
    "after": "DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl)\n{\n\tuint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR - a));",
    "case_ids": ["GetCardInDuelTempList-1"],
}
MUTATIONS["GetCardInDuelTempList_OnlyDeckIndex"] = {
    "source_symbol": "GetCardInDuelTempList_OnlyDeckIndex",
    "before": "DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl)\n{\n\tuint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));",
    "after": "DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl)\n{\n\tuint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR - a));",
    "case_ids": ["GetCardInDuelTempList_OnlyDeckIndex-1"],
}
MUTATIONS["GetPlayAreaCardRetreatCost"] = {
    "source_symbol": "GetPlayAreaCardRetreatCost",
    "before": "\tuint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(slot + 0xBBu)).a;\n\tLoadCardDataToBuffer1_FromDeckIndex(deck_idx);",
    "after": "\tuint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(slot + 0xBBu)).a;\n\t;",
    "case_ids": ["GetPlayAreaCardRetreatCost-0"],
}
MUTATIONS["GetCardIDFromDeckIndex"] = {
    "source_symbol": "GetCardIDFromDeckIndex",
    "before": "\treturn card_id_read_at(card_id_index_address(deck, a));",
    "after": "\treturn card_id_read_at(card_id_index_address(deck, (uint8_t)(a ^ 1u)));",
    "case_ids": ["GetCardIDFromDeckIndex-0"],
}
MUTATIONS["GetCardIDFromDeckIndex_bc"] = {
    "source_symbol": "GetCardIDFromDeckIndex_bc",
    "before": "\treturn (DeckCardResult){_GetCardIDFromDeckIndex(a).a, hl};",
    "after": "\treturn (DeckCardResult){(_GetCardIDFromDeckIndex(a).a) ^ 1u, hl};",
    "case_ids": ["GetCardIDFromDeckIndex_bc-0"],
}
MUTATIONS["LoadCardDataToBuffer1_FromDeckIndex"] = {
    "source_symbol": "LoadCardDataToBuffer1_FromDeckIndex",
    "before": "\treturn load_card_data_from_deck_index(a, wLoadedCard1_ADDR,",
    "after": "\treturn load_card_data_from_deck_index((uint8_t)(a ^ 1u), wLoadedCard1_ADDR,",
    "case_ids": ["LoadCardDataToBuffer1_FromDeckIndex-0"],
}
MUTATIONS["LoadCardDataToBuffer2_FromDeckIndex"] = {
    "source_symbol": "LoadCardDataToBuffer2_FromDeckIndex",
    "before": "\treturn load_card_data_from_deck_index(a, wLoadedCard2_ADDR,",
    "after": "\treturn load_card_data_from_deck_index((uint8_t)(a ^ 1u), wLoadedCard2_ADDR,",
    "case_ids": ["LoadCardDataToBuffer2_FromDeckIndex-0"],
}
MUTATIONS["LoadNonPokemonCardEffectCommands"] = {
    "source_symbol": "LoadNonPokemonCardEffectCommands",
    "before": "\tb1 = gb_read8((uint16_t)(wLoadedCard1EffectCommands_ADDR + 1u));",
    "after": "\tb1 = gb_read8((uint16_t)(wLoadedCard1EffectCommands_ADDR - 1u));",
    "case_ids": ["LoadNonPokemonCardEffectCommands-1"],
}
MUTATIONS["MoveCardToDiscardPileIfInPlayArea"] = {
    "source_symbol": "MoveCardToDiscardPileIfInPlayArea",
    "before": "\t\tif ((uint8_t)(id & 0xFFu) != c)",
    "after": "\t\tif ((uint8_t)(id & 0xFFu) == c)",
    "case_ids": ["MoveCardToDiscardPileIfInPlayArea-0"],
}
MUTATIONS["MoveDiscardPileCardToHand"] = {
    "source_symbol": "MoveDiscardPileCardToHand",
    "before": "\t\treturn (MoveDiscardResult){0, 0x80u};",
    "after": "\t\treturn (MoveDiscardResult){0, 0x81u};",
    "case_ids": ["MoveDiscardPileCardToHand-1"],
}
MUTATIONS["MoveHandCardToDiscardPile"] = {
    "source_symbol": "MoveHandCardToDiscardPile",
    "before": "\tif (masked != CARD_LOCATION_HAND) {",
    "after": "\tif (masked == CARD_LOCATION_HAND) {",
    "case_ids": ["MoveHandCardToDiscardPile-0"],
}
MUTATIONS["MovePlayAreaCardToDiscardPile"] = {
    "source_symbol": "MovePlayAreaCardToDiscardPile",
    "before": "\t\tif (gb_read8(addr) == location)",
    "after": "\t\tif (gb_read8(addr) != location)",
    "case_ids": ["MovePlayAreaCardToDiscardPile-0"],
}
MUTATIONS["PrintKnockedOut"] = {
    "source_symbol": "PrintKnockedOut",
    "before": "\tDrawWideTextBox_PrintText(WAS_KNOCKED_OUT_TEXT);",
    "after": "\t;",
    "case_ids": ["PrintKnockedOut-0"],
}
MUTATIONS["PrintPlayAreaCardKnockedOutIfNoHP"] = {
    "source_symbol": "PrintPlayAreaCardKnockedOutIfNoHP",
    "before": "\t\treturn (KnockoutCheckResult){hp, 0x00u};",
    "after": "\t\treturn (KnockoutCheckResult){hp, 0x01u};",
    "case_ids": ["PrintPlayAreaCardKnockedOutIfNoHP-0"],
}
MUTATIONS["PutCardInDiscardPile"] = {
    "source_symbol": "PutCardInDiscardPile",
    "before": "\tgb_write8((uint16_t)(page | a), CARD_LOCATION_DISCARD_PILE);",
    "after": "\tgb_write8((uint16_t)(page & a), CARD_LOCATION_DISCARD_PILE);",
    "case_ids": ["PutCardInDiscardPile-0"],
}
MUTATIONS["PutHandCardInPlayArea"] = {
    "source_symbol": "PutHandCardInPlayArea",
    "before": "\tuint16_t hl = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);",
    "after": "\tuint16_t hl = (uint16_t)(((uint16_t)hWhoseTurn << 8) & a);",
    "case_ids": ["PutHandCardInPlayArea-0"],
}
MUTATIONS["PutHandPokemonCardInPlayArea"] = {
    "source_symbol": "PutHandPokemonCardInPlayArea",
    "before": "\tif (count.a >= MAX_PLAY_AREA_POKEMON) {",
    "after": "\tif (count.a > MAX_PLAY_AREA_POKEMON) {",
    "case_ids": ["PutHandPokemonCardInPlayArea-1"],
}
MUTATIONS["RemoveCardFromDuelTempList"] = {
    "source_symbol": "RemoveCardFromDuelTempList",
    "before": "\t\tif (entry == 0xFF)",
    "after": "\t\tif (entry != 0xFF)",
    "case_ids": ["RemoveCardFromDuelTempList-0"],
}
MUTATIONS["RemoveCardFromHand"] = {
    "source_symbol": "RemoveCardFromHand",
    "before": "\t\tif (card == a) {",
    "after": "\t\tif (card != a) {",
    "case_ids": ["RemoveCardFromHand-0"],
}
MUTATIONS["ReturnCardToDeck"] = {
    "source_symbol": "ReturnCardToDeck",
    "before": "\tuint8_t not_in_deck = (uint8_t)(gb_read8(not_in_deck_addr) - 1u);",
    "after": "\tuint8_t not_in_deck = (uint8_t)(gb_read8(not_in_deck_addr) + 1u);",
    "case_ids": ["ReturnCardToDeck-0"],
}
MUTATIONS["ReturnCarry"] = {
    "source_symbol": "ReturnCarry",
    "before": "\treturn (uint8_t)((f & 0x80u) | 0x10u);",
    "after": "\treturn (uint8_t)((f | 0x80u) | 0x10u);",
    "case_ids": ["ReturnCarry-0"],
}
MUTATIONS["SearchCardInDeckAndAddToHand"] = {
    "source_symbol": "SearchCardInDeckAndAddToHand",
    "before": "\tuint16_t hl = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + DECK_SIZE - 1u));",
    "after": "\tuint16_t hl = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS - DECK_SIZE - 1u));",
    "case_ids": ["SearchCardInDeckAndAddToHand-0"],
}
MUTATIONS["ShiftAllPokemonToFirstPlayAreaSlots"] = {
    "source_symbol": "ShiftAllPokemonToFirstPlayAreaSlots",
    "before": "\t(void)ShiftTurnPokemonToFirstPlayAreaSlots();",
    "after": "\t;",
    "case_ids": ["ShiftAllPokemonToFirstPlayAreaSlots-0"],
}
MUTATIONS["ShiftTurnPokemonToFirstPlayAreaSlots"] = {
    "source_symbol": "ShiftTurnPokemonToFirstPlayAreaSlots",
    "before": "\t\tif (!(gb_read8(addr) & 0x80u)) {",
    "after": "\t\tif (!(gb_read8(addr) & 0x81u)) {",
    "case_ids": ["ShiftTurnPokemonToFirstPlayAreaSlots-0"],
}
MUTATIONS["ShuffleCards"] = {
    "source_symbol": "ShuffleCards",
    "before": "\t\treturn (ShuffleCardsResult){0, 0x80u};",
    "after": "\t\treturn (ShuffleCardsResult){0, 0x81u};",
    "case_ids": ["ShuffleCards-0"],
}
MUTATIONS["ShuffleDeck"] = {
    "source_symbol": "ShuffleDeck",
    "before": "\tuint8_t not_in_deck = gb_read8((uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));",
    "after": "\tuint8_t not_in_deck = gb_read8((uint16_t)(page & DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));",
    "case_ids": ["ShuffleDeck-0"],
}
MUTATIONS["SortCardsInDuelTempListByID"] = {
    "source_symbol": "SortCardsInDuelTempListByID",
    "before": "\tlist_set_ptr(wDuelTempList_ADDR);",
    "after": "\t;",
    "case_ids": ["SortCardsInDuelTempListByID-0"],
}
MUTATIONS["SortHandCardsByID"] = {
    "source_symbol": "SortHandCardsByID",
    "before": "\t\t\t\t0xC0u, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DUELVARS_HAND - 1u)};",
    "after": "\t\t\t\t0xC1u, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DUELVARS_HAND - 1u)};",
    "case_ids": ["SortHandCardsByID-0"],
}
MUTATIONS["SubtractHP"] = {
    "source_symbol": "SubtractHP",
    "before": "\tuint8_t f = remaining ? 0x10u : 0x80u;",
    "after": "\tuint8_t f = remaining ? 0x11u : 0x80u;",
    "case_ids": ["SubtractHP-0"],
}
MUTATIONS["SwapArenaWithBenchPokemon"] = {
    "source_symbol": "SwapArenaWithBenchPokemon",
    "before": "\treturn SwapPlayAreaPokemon(PLAY_AREA_ARENA, e);",
    "after": "\treturn SwapPlayAreaPokemon(PLAY_AREA_ARENA, (uint8_t)(e ^ 1u));",
    "case_ids": ["SwapArenaWithBenchPokemon-0"],
}
MUTATIONS["SwapPlayAreaPokemon"] = {
    "source_symbol": "SwapPlayAreaPokemon",
    "before": "\tif (e == d)",
    "after": "\tif (e != d)",
    "case_ids": ["SwapPlayAreaPokemon-0"],
}
MUTATIONS["TranslateColorToWR"] = {
    "source_symbol": "TranslateColorToWR",
    "before": "\treturn rom_ptr(InvertedPowersOf2_BANK, InvertedPowersOf2_ADDR)[a];",
    "after": "\treturn rom_ptr(InvertedPowersOf2_BANK, PowersOf2_ADDR)[a];",
    "case_ids": ["TranslateColorToWR-0"],
}
MUTATIONS["_GetCardIDFromDeckIndex"] = {
    "source_symbol": "_GetCardIDFromDeckIndex",
    "before": "\treturn (DeckCardResult){(uint8_t)(id & 0xFFu), (uint16_t)(deck + a)};",
    "after": "\treturn (DeckCardResult){(uint8_t)(id & 0xFFu), (uint16_t)(deck + (uint8_t)(a + 1u))};",
    "case_ids": ["_GetCardIDFromDeckIndex-1"],
}
MUTATIONS["SortCardsInListByID_CheckForListTerminator"] = {
    "source_symbol": "SortCardsInListByID_CheckForListTerminator",
    "before": "{\n\treturn SortCardsInListByID(b, c, de);",
    "after": "{\n\treturn SortCardsInListByID((uint8_t)(b ^ 1u), c, de);",
    "case_ids": ["SortCardsInListByID_CheckForListTerminator-1"],
}
