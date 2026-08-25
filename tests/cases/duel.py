POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# hWhoseTurn (player $C2 / opponent $C3) selects the duel-variables page.
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wOpponentDuelVariables = 0xC300
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDuelTempList = 0xC510
wDamage_ADDR = 0xCCB9
wDamageEffectiveness_ADDR = 0xCCC1
wTempTurnDuelistCardID = 0xCCC3
wTempNonTurnDuelistCardID = 0xCCC4
wSentAttackDataToLinkOpponent = 0xCCEC
wStatusConditionQueueIndex = 0xCCCD
wEffectFailed = 0xCCED
wIsDamageToSelf = 0xCCE6
wDefendingWasForcedToSwitch = 0xCCEF
wMetronomeEnergyCost = 0xCCF0
wNoEffectFromWhichStatus = 0xCCF1

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
        {"d": 0xC1, "e": 0x00, "sram": {0: {0xA010: b"\x21\x22\x00"}},
         "read": {0xC100: 3}},
        dict(POISON, d=0xC2, e=0x00,
             sram={2: {0xA010: b"\x31\x00"}}, wram={0xFF81: b"\x02"},
             read={0xC200: 2}),
    ],
    "CopyOpponentName": [
        {"d": 0xC1, "e": 0x00, "wram": {0xC500: b"\x41\x42\x00"},
         "read": {0xC100: 3}},
        dict(POISON, d=0xC2, e=0x00, wram={0xC500: b"\x51\x00"},
             read={0xC200: 2}),
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
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x10"}},
        {"a": 5, "wram": {hWhoseTurn: b"\xC3", wOpponentDeck + 5: b"\x22"}},
        dict(POISON, a=3, wram={hWhoseTurn: b"\xC2", wPlayerDeck + 3: b"\x33"}),
    ],
    # id in de, af and hl preserved.
    "GetCardIDFromDeckIndex": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x10"}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC2", wPlayerDeck + 5: b"\x22"}),
    ],
    # id in a and c, b = 0, hl preserved.
    "GetCardIDFromDeckIndex_bc": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x10"}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC3", wOpponentDeck + 5: b"\x22"}),
    ],
    # Temp-list entry shadowed in hTempCardIndex_ff98, hl preserved.
    "GetCardInDuelTempList_OnlyDeckIndex": [
        {"a": 0, "wram": {wDuelTempList: b"\x07"}, "read": {0xFF98: 1}},
        dict(POISON, a=2, wram={wDuelTempList + 2: b"\x09"}, read={0xFF98: 1}),
    ],
    # Entry in a (reloaded), id in de, hl preserved.
    "GetCardInDuelTempList": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wDuelTempList: b"\x01",
                          wPlayerDeck + 1: b"\x44"}, "read": {0xFF98: 1}},
        dict(POISON, a=1, wram={hWhoseTurn: b"\xC3", wDuelTempList + 1: b"\x02",
                                wOpponentDeck + 2: b"\x55"}, read={0xFF98: 1}),
    ],
    # Deck card loaded into wLoadedCard1: the type byte lands in the buffer and
    # exit a is the card id's low byte. wLoadedCard1 = $CC24.
    "LoadCardDataToBuffer1_FromDeckIndex": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x10"},
         "read": {0xCC24: 64}},
        dict(POISON, a=3, wram={hWhoseTurn: b"\xC2", wPlayerDeck + 3: b"\x20"},
             read={0xCC24: 64}),
    ],
    "LoadCardDataToBuffer2_FromDeckIndex": [
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck + 1: b"\x15"},
         "read": {0xCC65: 64}},
        dict(POISON, a=4, wram={hWhoseTurn: b"\xC2", wPlayerDeck + 4: b"\x25"},
             read={0xCC65: 64}),
    ],
    # HP minus damage, clamped at zero; carry set iff HP remains.
    "SubtractHP": [
        {"hl": 0xC400, "d": 0x00, "e": 3, "wram": {0xC400: b"\x0a"}, "read": {0xC400: 1}},
        {"hl": 0xC400, "d": 0x00, "e": 10, "wram": {0xC400: b"\x0a"}, "read": {0xC400: 1}},
        {"hl": 0xC400, "d": 0x01, "e": 0, "wram": {0xC400: b"\x0a"}, "read": {0xC400: 1}},
        {"hl": 0xC400, "d": 0x00, "e": 0, "wram": {0xC400: b"\x00"}, "read": {0xC400: 1}},
        dict(POISON, hl=0xC400, d=0x00, e=5, wram={0xC400: b"\x64"}, read={0xC400: 1}),
    ],
    # wDuelTempList = $C510. Deck cards occupy $C27E-$C2B9 in the player page.
    "CreateDeckCardList": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x00"},
         "read": {0xC510: 62}},
        {"wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x3c"},
         "read": {0xC510: 26}},
        # All cards drawn: empty path, terminator only, carry set.
        {"wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x3c"},
         "read": {0xC510: 2}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC3BA: b"\x05"},
             read={0xC510: 60}),
    ],
    "CreateDiscardPileCardList": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x00"}, "read": {0xC510: 2}},
        {"wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x02", 0xC27E: b"\x11",
                  0xC27F: b"\x22"}, "read": {0xC510: 4}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC3ED: b"\x01", 0xC37F: b"\x33"},
             read={0xC510: 4}),
    ],
    # Remove the card id in a from the FF-terminated wDuelTempList.
    "RemoveCardFromDuelTempList": [
        {"a": 3, "wram": {0xC510: b"\x01\x02\x03\x04\xff"}, "read": {0xC510: 5}},
        {"a": 1, "wram": {0xC510: b"\x01\xff"}, "read": {0xC510: 2}},
        {"a": 9, "wram": {0xC510: b"\x01\x02\xff"}, "read": {0xC510: 4}},
        dict(POISON, a=2, wram={0xC510: b"\x02\x02\xff"}, read={0xC510: 3}),
    ],
    "CountCardsInDuelTempList": [
        {"wram": {0xC510: b"\xff"}},
        {"wram": {0xC510: b"\x01\x02\x03\xff"}},
        dict(POISON, wram={0xC510: b"\x01\xff"}),
    ],
    # Hand cards live at $C242+; count at $C2EE. Locations at $C200+.
    "FindLastCardInHand": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}),
    ],
    # Just-drawn cards (location bit 6) are skipped.
    "CreateHandCardList": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02",
                  0xC243: b"\x03", 0xC242: b"\x01",
                  0xC201: b"\x00", 0xC203: b"\x40"},
         "read": {0xC510: 4}},
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01",
                  0xC242: b"\x02", 0xC202: b"\x40"},
         "read": {0xC510: 3}},
        # Empty hand: carry set, terminator only.
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 2}},
        # Poisoned c is preserved (the routine never touches it).
        dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, read={0xC510: 2}),
    ],
    # Energy scan: deck index 0 is GRASS_ENERGY (id $01, energy type) in the play
    # area; deck index 1 is CLEFAIRY_DOLL (id $CB, trainer) so it is skipped.
    "CreateArenaOrBenchEnergyCardList": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10", 0xC201: b"\x10",
                          wPlayerDeck: b"\x01", wPlayerDeck + 1: b"\xCB"},
         "read": {0xC510: 4}},
        # No cards in the requested location (1 = bench): empty list, carry set.
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x00"}, "read": {0xC510: 2}},
    ],
    # Shuffle uses Random over the seeded RNG state ($CACA-$CACC), so the
    # outcome is deterministic and diffed against the real ROM.
    "ShuffleCards": [
        {"a": 0, "hl": 0xC27E, "wram": {0xC27E: b"\x01\x02\x03\x04"},
         "read": {0xC27E: 4}},
        {"a": 3, "hl": 0xC27E,
         "wram": {0xC27E: b"\x01\x02\x03\x04",
                  0xCACA: b"\x11\x22\x33"},
         "read": {0xC27E: 4}},
        {"a": 4, "hl": 0xC27E,
         "wram": {0xC27E: b"\x0a\x0b\x0c\x0d\x0e",
                  0xCACA: b"\x00\x00\x00"},
         "read": {0xC27E: 5}},
        dict(POISON, a=2, hl=0xC27E,
             wram={0xC27E: b"\x05\x06\x07", 0xCACA: b"\x00\x00\x00"},
             read={0xC27E: 3}),
    ],
    # Sort by card id: deck index -> id at $C400. The sort is unstable (equal ids
    # swap the later card forward), so the deck seeds use distinct ids to pin order.
    "SortCardsInDuelTempListByID": [
        # ids: idx0=$CB, idx1=$01, idx2=$02 -> sorted [1, 2, 0].
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\xCB\x01\x02",
                  0xC510: b"\x00\x02\x01\xff"},
         "read": {0xC510: 4, 0xFF99: 2}},
        # Already sorted: identity passes.
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02\xCB",
                  0xC510: b"\x00\x01\x02\xff"},
         "read": {0xC510: 4, 0xFF99: 2}},
        # Empty list.
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01", 0xC510: b"\xff"},
         "read": {0xC510: 2, 0xFF99: 2}},
        # Equal ids: the later card moves to the front (unstable).
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x01",
                  0xC510: b"\x00\x01\xff"},
         "read": {0xC510: 3, 0xFF99: 2}},
    ],
    # hTempListPtr_ff99 preselects the list to sort. The direct entry reads [ptr]
    # as a card index and scans from [ptr+1], so a well-formed list ends with the
    # terminator at [ptr+1]; the sort stops once the pointer itself lands on $FF.
    "SortCardsInListByID": [
        {"wram": {hWhoseTurn: b"\xC2", 0xFF99: b"\x10\xC5",
                  0xC510: b"\x02\x01\x00\xff", wPlayerDeck: b"\x03\x02\x01"},
         "read": {0xC510: 4, 0xFF99: 2}},
        # Single card at [ptr], terminator at [ptr+1].
        {"wram": {hWhoseTurn: b"\xC2", 0xFF99: b"\x00\xC5",
                  0xC500: b"\x00\xff", wPlayerDeck: b"\x01"},
         "read": {0xC500: 2, 0xFF99: 2}},
    ],
    # Hand cards at $C242 (count 2): sorted ascending by id and written back so
    # the lowest id is at the newest slot ($C243).
    "SortHandCardsByID": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02",
                  0xC243: b"\x00", 0xC242: b"\x01",
                  wPlayerDeck: b"\xCB\x01"},
         "read": {0xC242: 2, 0xC510: 4}},
        # Already sorted: the write-back reverses the order.
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02",
                  0xC243: b"\x01", 0xC242: b"\x00",
                  wPlayerDeck: b"\x01\x02"},
         "read": {0xC242: 2, 0xC510: 4}},
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
        {"b": 0x10, "e": 0x01, "hl": 0xC200,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02\x01",
                  0xC200: b"\x10\x00\x10"}},
        {"b": 0x10, "e": 0x02, "hl": 0xC200,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x02",
                  0xC200: b"\x10\x00"}},
        dict(POISON, b=0x10, e=0x01, hl=0xC200,
             wram={hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01\x01\x01",
                   0xC200: b"\x10\x10\x00"}),
    ],
    # Attack flag: a = group<<3 | bit. wLoadedAttackFlag1 = $CCB4.
    "CheckLoadedAttackFlag": [
        {"a": 0x00, "wram": {0xCCB4: b"\x01"}},
        {"a": 0x03, "wram": {0xCCB4: b"\x08"}},
        {"a": 0x08, "wram": {0xCCB5: b"\x02"}},
        {"a": 0x02, "wram": {0xCCB4: b"\x00"}},
        dict(POISON, a=0x10, wram={0xCCB6: b"\x80"}),
    ],
    # Arena slot 0: deck index at $C2BB, damage at $C2C8. Deck card $01 loads
    # with max HP $C9 (verified against the ROM).
    "GetCardDamageAndMaxHP": [
        {"e": 0, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x00",
                          wPlayerDeck: b"\x01"}},
        {"e": 0, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2C8: b"\x05",
                          wPlayerDeck: b"\x01"}},
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2BC: b"\x00", 0xC2C9: b"\x00",
                          wPlayerDeck: b"\x01"}},
        # Damage above max HP: full-byte borrow sets C (nibble 9-0 does not set H).
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2BC: b"\x00", 0xC2C9: b"\xD0",
                          wPlayerDeck: b"\x01"}},
        # Low-nibble borrow only: H without C.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2BC: b"\x00", 0xC2C9: b"\x3A",
                          wPlayerDeck: b"\x01"}},
        # Damage exactly at max HP ($71 for the loaded card): zero, no borrow.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2BC: b"\x00", 0xC2C9: b"\x71",
                          wPlayerDeck: b"\x01"}},
        # Damage above max HP with nibble borrow: H and C both.
        {"e": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2BC: b"\x00", 0xC2C9: b"\xC9",
                          wPlayerDeck: b"\x01"}},
    ],
    "CopyDeckData": [
        {"d": 0xC1, "e": 0x00, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC2", 0xC100: b"\x00\x41\x42"},
         "read": {wPlayerDeck: 60, 0xCCE9: 2}},
        {"d": 0xC1, "e": 0x50, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC3", 0xC150: b"\x02\x05\x00\x10\x20"},
         "read": {wOpponentDeck: 60, 0xCCE9: 2}},
        # Exactly DECK_SIZE cards -> last slot becomes nonzero -> carry clear.
        {"d": 0xC1, "e": 0x00, "c": 0x00,
         "wram": {hWhoseTurn: b"\xC2", 0xC100: b"\x3c\x07\x00\x30\x40"},
         "read": {wPlayerDeck: 60, 0xCCE9: 2}},
        # Empty description: c passes through untouched.
        dict(POISON, d=0xC1, e=0x00,
             wram={hWhoseTurn: b"\xC2", 0xC100: b"\x00\x50\x60"},
             read={wPlayerDeck: 60, 0xCCE9: 2}),
    ],
    "CountPrizes": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EC: b"\x00"}},
        {"wram": {hWhoseTurn: b"\xC2", 0xC2EC: b"\x3f"}},
        {"wram": {hWhoseTurn: b"\xC3", 0xC3EC: b"\x07"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EC: b"\xAA"}),
    ],
    "ShuffleDeck": [
        {"c": 0, "e": 0, "wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x00"},
         "read": {0xC27E: 60}},
        {"c": 0, "e": 0,
         "wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x3c", 0xCACA: b"\x11\x22\x33",
                  0xC27E: b"\x01\x02\x03\x04"},
         "read": {0xC27E: 4}},
        dict(POISON, c=0xCC, e=0xEE,
             wram={hWhoseTurn: b"\xC3", 0xC3BA: b"\x05", 0xCACA: b"\x00\x00\x00"},
             read={0xC37E: 60}),
    ],
    "DrawCardFromDeck": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x00", 0xC27E: b"\x08"},
         "read": {0xC2BA: 1, 0xC200: 1}},
        {"wram": {hWhoseTurn: b"\xC3", 0xC3BA: b"\x3c"}, "read": {0xC3BA: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BA: b"\x00", 0xC27E: b"\x00"},
             read={0xC2BA: 1, 0xC200: 1}),
    ],
    "ReturnCardToDeck": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x01"},
         "read": {0xC2BA: 1, 0xC27E: 1, 0xC200: 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", 0xC3BA: b"\x0a"},
             read={0xC3BA: 1, 0xC283 + 0x100: 1}),
    ],
    "SearchCardInDeckAndAddToHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BA: b"\x00",
                              0xC27E: b"\x01\x02\x03"},
         "read": {0xC2BA: 1, 0xC202: 1, 0xC27E: 3}},
        dict(POISON, a=0x00, wram={hWhoseTurn: b"\xC3", 0xC3BA: b"\x02",
                                   0xC380: b"\x01\x02\x03"},
             read={0xC3BA: 1, 0xC380: 1, 0xC300: 1}),
    ],
    "AddCardToHand": [
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"},
         "read": {0xC200: 1, 0xC2EE: 1, 0xC242: 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", 0xC3EE: b"\x02"},
             read={0xC305: 1, 0xC3EE: 1, 0xC344: 1}),
    ],
    "RemoveCardFromHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x03",
                              0xC242: b"\x01\x02\x03"},
         "read": {0xC2EE: 1, 0xC242: 3}},
        {"a": 0x09, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"},
         "read": {0xC2EE: 1}},
        dict(POISON, a=0x01, wram={hWhoseTurn: b"\xC3", 0xC3EE: b"\x02",
                                   0xC342: b"\x01\x01"},
             read={0xC3EE: 1, 0xC342: 2}),
    ],
    "PutCardInDiscardPile": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x00"},
         "read": {0xC200: 1, 0xC2ED: 1, 0xC27E: 1}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", 0xC3ED: b"\x02"},
             read={0xC305: 1, 0xC3ED: 1, 0xC380: 1}),
    ],
    "MoveHandCardToDiscardPile": [
        # Card is in hand (masked location == CARD_LOCATION_HAND): moved.
        {"a": 0x03, "wram": {hWhoseTurn: b"\xC2", 0xC203: b"\x01",
                              0xC2EE: b"\x01", 0xC242: b"\x03"},
         "read": {0xC203: 1, 0xC2EE: 1, 0xC2ED: 1}},
        # Card not in hand (in deck): early return.
        {"a": 0x04, "wram": {hWhoseTurn: b"\xC2", 0xC204: b"\x00"},
         "read": {0xC204: 1}},
        dict(POISON, a=0x07, wram={hWhoseTurn: b"\xC3", 0xC307: b"\x02"},
             read={0xC307: 1}),
    ],
    "MoveDiscardPileCardToHand": [
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x02",
                              0xC27E: b"\x01\x02"},
         "read": {0xC202: 1, 0xC2ED: 1, 0xC27E: 2}},
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x00"},
         "read": {0xC200: 1, 0xC2ED: 1}},
        # Searched card not present: the scan's last `cp` compares against a
        # higher id, distinguishing the carry-flag's < vs > direction.
        {"a": 0x09, "wram": {hWhoseTurn: b"\xC2", 0xC2ED: b"\x02",
                              0xC27E: b"\x01\x02"},
         "read": {0xC209: 1, 0xC2ED: 1, 0xC27E: 2}},
        dict(POISON, a=0x05, wram={hWhoseTurn: b"\xC3", 0xC3ED: b"\x01",
                                   0xC37E: b"\x05"},
             read={0xC305: 1, 0xC3ED: 1, 0xC37E: 1}),
    ],
    "CheckPrizeTaken": [
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", 0xC2EC: b"\x01"}},
        {"a": 3, "wram": {hWhoseTurn: b"\xC2", 0xC2EC: b"\x04"}},
        {"a": 7, "wram": {hWhoseTurn: b"\xC3", 0xC3EC: b"\x80"}},
        dict(POISON, a=5, wram={hWhoseTurn: b"\xC2", 0xC2EC: b"\x00"}),
    ],
    "SortCardsInListByID_CheckForListTerminator": [
        {"wram": {hWhoseTurn: b"\xC2", 0xFF99: b"\x10\xC5",
                  0xC510: b"\x02\x01\x00\xff", wPlayerDeck: b"\x03\x02\x01"},
         "read": {0xC510: 4, 0xFF99: 2}},
        {"wram": {hWhoseTurn: b"\xC2", 0xFF99: b"\x00\xC5",
                  0xC500: b"\xff"}, "read": {0xFF99: 2}},
        # Poisoned b/c must survive an immediate (empty-list) terminator hit
        # unchanged -- this is the only branch where they're real pass-through
        # inputs rather than loop-derived outputs. f=0 (not full POISON):
        # SortCardsInListByID's shared `bit 7,[hl]` terminator check never
        # touches carry, but the shared C hardcodes f=$20 (C=0) on this
        # branch, so poisoning entry carry would fail through code this
        # routine doesn't own.
        dict(POISON, f=0x00, wram={hWhoseTurn: b"\xC3", 0xFF99: b"\x00\xC5",
                           0xC500: b"\xff"}, read={0xFF99: 2}),
    ],
    "CheckIfCanEvolveInto": [
        # card 9 (stage1) evolves from card 8 (basic) currently in play: eligible.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  0xC2BB: b"\x00", 0xC2C2: b"\x80"}},
        # Not eligible this turn (CAN_EVOLVE_THIS_TURN flag clear).
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  0xC2BB: b"\x00", 0xC2C2: b"\x00"}},
        # Unrelated cards: name mismatch.
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                   0xC3BB: b"\x00", 0xC3C2: b"\x80"}),
    ],
    "CheckIfCanEvolveInto_BasicToStage2": [
        # card 10 (stage2) evolves from card 8 (basic) via card 9 (stage1) by name.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x0a",
                  0xC2BB: b"\x00", 0xC2C2: b"\x80"}},
        # Flag clear: not eligible.
        {"d": 0x01, "e": 0x00,
         "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x0a",
                  0xC2BB: b"\x00", 0xC2C2: b"\x00"}},
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                   0xC3BB: b"\x00", 0xC3C2: b"\x80"}),
    ],
    "EvolvePokemonCardIfPossible": [
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  0xC2BB: b"\x00", 0xC2C2: b"\x80", 0xC2C8: b"\x0a",
                  0xFF98: b"\x01", 0xFF9D: b"\x00"},
         "read": {0xC2BB: 1, 0xC2C8: 1, 0xC2C2: 1, 0xC2CE: 1, 0xCCEE: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                           0xC3BB: b"\x00", 0xC3C2: b"\x00",
                           0xFF98: b"\x01", 0xFF9D: b"\x00"},
             read={0xC3BB: 1}),
    ],
    "EvolvePokemonCard": [
        {"wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08\x09",
                  0xC2BB: b"\x00", 0xC2C8: b"\x0a",
                  0xFF98: b"\x01", 0xFF9D: b"\x00"},
         "read": {0xC2BB: 1, 0xC2C8: 1, 0xC2C2: 1, 0xC2CE: 1, 0xCCEE: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x01\x02",
                           0xC3BB: b"\x00", 0xC3C8: b"\x05",
                           0xFF98: b"\x00", 0xFF9D: b"\x01"},
             read={0xC3BC: 1, 0xC3C9: 1, 0xC3CF: 1}),
    ],
    "ClearAllStatusConditions": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC2F0: b"\x05", 0xC2E7: b"\x01",
                  0xC2E8: b"\x02", 0xC2EB: b"\x03", 0xC2F2: b"\xff\xff\xff\xff\xff\xff\xff\xff"},
         "read": {0xC2F0: 1, 0xC2E7: 1, 0xC2E8: 1, 0xC2E9: 1, 0xC2EA: 1, 0xC2EB: 1,
                  0xC2F2: 8}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC3F0: b"\x07", 0xC3EB: b"\x03"},
             read={0xC3F0: 1, 0xC3EB: 1, 0xC3F2: 8}),
    ],
    "PutHandCardInPlayArea": [
        {"a": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01",
                                        0xC242: b"\x00"},
         "read": {0xC200: 1, 0xC2EE: 1}},
        dict(POISON, a=0x02, e=0x03,
             wram={hWhoseTurn: b"\xC3", 0xC3EE: b"\x01", 0xC342: b"\x02"},
             read={0xC302: 1, 0xC3EE: 1}),
    ],
    "PutHandPokemonCardInPlayArea": [
        {"a": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x00",
                             0xC2EE: b"\x01", 0xC242: b"\x00", wPlayerDeck: b"\x08"},
         "read": {0xC2EF: 1, 0xC2BB: 1, 0xC2C8: 1, 0xC2CE: 1, 0xC2C2: 1, 0xC2D4: 1,
                  0xC2E0: 1, 0xC2DA: 1, 0xC2F0: 1}},
        # Play area already full: carry set, echoes input a.
        {"a": 0x05, "wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x06"},
         "read": {0xC2EF: 1}},
        dict(POISON, a=0x00, wram={hWhoseTurn: b"\xC3", 0xC3EF: b"\x02",
                                   0xC3EE: b"\x01", 0xC342: b"\x00",
                                   wOpponentDeck: b"\x08"},
             read={0xC3EF: 1, 0xC3BD: 1}),
    ],
    "EmptyPlayAreaSlot": [
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2"},
         "read": {0xC2BB: 1, 0xC2C8: 1, 0xC2CE: 1, 0xC2D4: 1, 0xC2DA: 1, 0xC2E0: 1}},
        dict(POISON, e=0x05, wram={hWhoseTurn: b"\xC3"},
             read={0xC3C0: 1, 0xC3CD: 1, 0xC3D3: 1, 0xC3D9: 1, 0xC3DF: 1, 0xC3E5: 1}),
    ],
    "MovePlayAreaCardToDiscardPile": [
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x01",
                             0xC200: b"\x10", 0xC2ED: b"\x00"},
         "read": {0xC2EF: 1, 0xC200: 1, 0xC2ED: 1, 0xC27E: 1}},
        dict(POISON, e=0x01, wram={hWhoseTurn: b"\xC3", 0xC3EF: b"\x02",
                                   0xC301: b"\x11", 0xC3ED: b"\x00"},
             read={0xC3EF: 1, 0xC301: 1, 0xC3ED: 1}),
    ],
    "SwapPlayAreaPokemon": [
        {"d": 0x00, "e": 0x01,
         "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x01", 0xC2BC: b"\x02",
                  0xC200: b"\x10", 0xC201: b"\x11"},
         "read": {0xC2BB: 1, 0xC2BC: 1, 0xC200: 1, 0xC201: 1}},
        # d == e: no-op.
        {"d": 0x02, "e": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BD: b"\x03"},
         "read": {0xC2BD: 1}},
        dict(POISON, d=0x01, e=0x00,
             wram={hWhoseTurn: b"\xC3", 0xC3BB: b"\x05", 0xC3BC: b"\x06",
                   0xC300: b"\x10", 0xC301: b"\x11"},
             read={0xC3BB: 1, 0xC3BC: 1, 0xC300: 1, 0xC301: 1}),
    ],
    "SwapArenaWithBenchPokemon": [
        {"e": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x01", 0xC2BC: b"\x02",
                             0xC200: b"\x10", 0xC201: b"\x11", 0xC2F0: b"\x05"},
         "read": {0xC2BB: 1, 0xC2BC: 1, 0xC2F0: 1}},
        dict(POISON, e=0x00, wram={hWhoseTurn: b"\xC3", 0xC3BB: b"\x07", 0xC3F0: b"\x02"},
             read={0xC3BB: 1, 0xC3F0: 1}),
    ],
    "ShiftTurnPokemonToFirstPlayAreaSlots": [
        {"wram": {hWhoseTurn: b"\xC2",
                  0xC2BB: b"\xff", 0xC2BC: b"\x02", 0xC2BD: b"\xff",
                  0xC2BE: b"\x03", 0xC2BF: b"\xff", 0xC2C0: b"\xff",
                  0xC202: b"\x11", 0xC203: b"\x12"},
         "read": {0xC2BB: 6, 0xC200: 5}},
        {"wram": {hWhoseTurn: b"\xC3",
                  0xC3BB: b"\xff", 0xC3BC: b"\xff", 0xC3BD: b"\xff",
                  0xC3BE: b"\xff", 0xC3BF: b"\xff", 0xC3C0: b"\xff"},
         "read": {0xC3BB: 6}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           0xC2BB: b"\xff", 0xC2BC: b"\xff", 0xC2BD: b"\xff",
                           0xC2BE: b"\xff", 0xC2BF: b"\xff", 0xC2C0: b"\xff"},
             read={0xC2BB: 6}),
    ],
    "ShiftAllPokemonToFirstPlayAreaSlots": [
        {"wram": {hWhoseTurn: b"\xC2",
                  0xC2BB: b"\xff", 0xC2BC: b"\x02", 0xC2BD: b"\xff",
                  0xC2BE: b"\xff", 0xC2BF: b"\xff", 0xC2C0: b"\xff",
                  0xC3BB: b"\xff", 0xC3BC: b"\xff", 0xC3BD: b"\xff",
                  0xC3BE: b"\xff", 0xC3BF: b"\xff", 0xC3C0: b"\xff",
                  0xC202: b"\x11"},
         "read": {0xC2BB: 6, 0xC3BB: 6, hWhoseTurn: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC3",
                           0xC2BB: b"\xff", 0xC2BC: b"\xff", 0xC2BD: b"\xff",
                           0xC2BE: b"\xff", 0xC2BF: b"\xff", 0xC2C0: b"\xff",
                           0xC3BB: b"\xff", 0xC3BC: b"\xff", 0xC3BD: b"\xff",
                           0xC3BE: b"\xff", 0xC3BF: b"\xff", 0xC3C0: b"\xff"},
             read={0xC2BB: 6, 0xC3BB: 6, hWhoseTurn: 1}),
    ],
    "GetPlayAreaCardAttachedEnergies": [
        # Slot 0 (arena): deck index 0 -> card id 1 (GRASS_ENERGY, energy).
        {"e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10",
                             wPlayerDeck: b"\x01"},
         "read": {0xCC1B: 8, 0xCC23: 1}},
        {"e": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x00"},
         "read": {0xCC1B: 8, 0xCC23: 1}},
        dict(POISON, e=0x00, wram={hWhoseTurn: b"\xC3", 0xC300: b"\x10",
                                   wOpponentDeck: b"\x01"},
             read={0xCC1B: 8, 0xCC23: 1}),
    ],
    "CopyAttackDataAndDamage": [
        {"e": 0, "wram": {0xCC2B: b"\x08", 0xCC30: b"\x01" * 0x13},
         "read": {0xCCC2: 1, 0xCCA6: 0x13, 0xCCB9: 2, 0xCCC7: 1, 0xCCBF: 2}},
        {"e": 1, "wram": {0xCC2B: b"\x09", 0xCC43: b"\x02" * 0x13},
         "read": {0xCCC2: 1, 0xCCA6: 0x13, 0xCCB9: 2, 0xCCC7: 1, 0xCCBF: 2}},
        dict(POISON, e=0, wram={0xCC2B: b"\x0a", 0xCC30: b"\x03" * 0x13},
             read={0xCCC2: 1, 0xCCA6: 0x13}),
    ],
    "CopyAttackDataAndDamage_FromDeckIndex": [
        {"d": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x08"},
         "read": {0xFF9F: 1, 0xCCC6: 1, 0xCCC2: 1, 0xCCA6: 0x13}},
        dict(POISON, d=0x00, e=0x01, wram={hWhoseTurn: b"\xC3", wOpponentDeck: b"\x09"},
             read={0xFF9F: 1, 0xCCC6: 1, 0xCCC2: 1}),
    ],
    "CopyAttackDataAndDamage_FromCardID": [
        {"a": 0x08, "d": 0x00, "e": 0x00,
         "read": {0xFF9F: 1, 0xCCC6: 1, 0xCCC2: 1, 0xCCA6: 0x13}},
        dict(POISON, a=0x09, d=0x00, e=0x01,
             read={0xFF9F: 1, 0xCCC6: 1, 0xCCC2: 1}),
    ],
    "ReturnCarry": [
        {"f": 0x00},
        {"f": 0x80},
        dict(POISON),
    ],
    "LoadNonPokemonCardEffectCommands": [
        {"wram": {0xFF9F: b"\x00", wPlayerDeck: b"\x08"},
         "read": {0xCCB2: 2}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xFF9F: b"\x00",
                           wOpponentDeck: b"\x09"},
             read={0xCCB2: 2}),
    ],
    "ApplyAttachedPlusPower": [
        {"b": 0x10, "d": 0x00, "e": 0x0a,
         "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10\x10",
                  wPlayerDeck: b"\xd8\xd8"},
         "read": {0xC200: 2}},
        dict(POISON, b=0x10, d=0x00, e=0x00,
             wram={hWhoseTurn: b"\xC3", 0xC300: b"\x00"}),
    ],
    "ApplyAttachedDefender": [
        {"b": 0x10, "d": 0x00, "e": 0x64,
         "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10",
                  wPlayerDeck: b"\xd9"},
         "read": {0xC200: 1}},
        dict(POISON, b=0x10, d=0x00, e=0x00,
             wram={hWhoseTurn: b"\xC3", 0xC300: b"\x00"}),
    ],
    "MoveCardToDiscardPileIfInPlayArea": [
        {"d": 0x00, "e": 0xd8, "hl": 0xC200,
         "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10\x00",
                  wPlayerDeck: b"\xd8\x01"},
         "read": {0xC200: 2, 0xC2ED: 1}},
        dict(POISON, d=0x00, e=0x00, hl=0xC300,
             wram={hWhoseTurn: b"\xC3", 0xC300: b"\x00"}),
    ],
    "ApplyDamageModifiers_DamageToTarget": [
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x00\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                  0xC2D4: b"\x00",
                  0xC3E9: b"\x80", 0xC3EA: b"\x80",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                  0xC2D4: b"\x00",
                  0xC3E9: b"\x40", 0xC3EA: b"\x80",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x28\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                  0xC2D4: b"\x00",
                  0xC3E9: b"\x80", 0xC3EA: b"\x40",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x14\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                  0xC2D4: b"\x00",
                  0xC3E9: b"\x80", 0xC3EA: b"\x40",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x80",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                  0xC2D4: b"\x00",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           wDamage_ADDR: b"\x14\x00",
                           0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                           0xC2BC: b"\xFF", 0xC3BC: b"\xFF",
                           0xC2D4: b"\x00",
                           0xC3E9: b"\x80", 0xC3EA: b"\x80",
                           0xC2F0: b"\x00"},
             read={wDamageEffectiveness_ADDR: 1}),
    ],
    "ApplyDamageModifiers_DamageToSelf": [
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x00\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2D4: b"\x00",
                  0xC2E9: b"\x80", 0xC2EA: b"\x80",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x0A\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2D4: b"\x00",
                  0xC2E9: b"\x40", 0xC2EA: b"\x80",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x28\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2D4: b"\x00",
                  0xC2E9: b"\x80", 0xC2EA: b"\x40",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        {"wram": {hWhoseTurn: b"\xC2",
                  wDamage_ADDR: b"\x14\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2D4: b"\x00",
                  0xC2E9: b"\x80", 0xC2EA: b"\x40",
                  0xC2F0: b"\x00"},
         "read": {wDamageEffectiveness_ADDR: 1}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           wDamage_ADDR: b"\x14\x00",
                           0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                           0xC2D4: b"\x00",
                           0xC2E9: b"\x80", 0xC2EA: b"\x80",
                           0xC2F0: b"\x00"},
             read={wDamageEffectiveness_ADDR: 1}),
    ],
    "GetPlayAreaCardRetreatCost": [
        {"wram": {hWhoseTurn: b"\xC2",
                  0xFF9D: b"\x00",
                  0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                  0xC2C1: b"\xFF"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           0xFF9D: b"\x00",
                           0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                           0xC2C1: b"\xFF"}),
    ],
}

HP_ADDR = 0xC2C8  # player page (0xC2) + DUELVARS_ARENA_CARD_HP (0xC8)
CASES.update({
    "PrintPlayAreaCardKnockedOutIfNoHP": [
        # HP=30 (non-zero) → early return, a=30, f=0x00 (no carry)
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", HP_ADDR: b"\x30"}},
        # HP=10, different play area location
        {"a": 1, "wram": {hWhoseTurn: b"\xC2", 0xC2C9: b"\x0A"}},
        # Poisoned registers, HP=50
        dict(POISON, a=2, wram={hWhoseTurn: b"\xC2", 0xC2CA: b"\x32"}),
        {"a": 0, "wram": {hWhoseTurn: b"\xC2", HP_ADDR: b"\x00",
                          0xC2BB: b"\x00", wPlayerDeck + 0: b"\x08",
                          0xCCC4: b"\x08", 0xCAD3: b"\x48\x03"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
    "PrintKnockedOut": [
        {"wram": {hWhoseTurn: b"\xC2", 0xCCC4: b"\x08", 0xCAD3: b"\x48\x03"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
    "DrawWideTextBox_WaitForInput_ReturnCarry": [
        {"hl": 0, "keys": 0x01,
         "wram": {0xC590: b"\x00"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    ],
})
CASES.update({
    "UpdateArenaCardIDsAndClearTwoTurnDuelVars": [
        {"wram": {
            hWhoseTurn: b"\xC2",
            0xC2BB: b"\x00", 0xC3BB: b"\x01",
            wPlayerDeck: b"\x12", wOpponentDeck + 1: b"\x34",
            wTempTurnDuelistCardID: b"\xFF", wTempNonTurnDuelistCardID: b"\xFF",
            wSentAttackDataToLinkOpponent: b"\xFF",
            wStatusConditionQueueIndex: b"\xFF",
            wEffectFailed: b"\xFF",
            wIsDamageToSelf: b"\xFF", wDefendingWasForcedToSwitch: b"\xFF",
            wMetronomeEnergyCost: b"\xFF", wNoEffectFromWhichStatus: b"\xFF",
            0xC3F2: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"},
         "read": {0xCCC3: 1, 0xCCC4: 1, 0xFF9F: 1,
                  wSentAttackDataToLinkOpponent: 1, wStatusConditionQueueIndex: 1,
                  wEffectFailed: 1, wIsDamageToSelf: 1, wDefendingWasForcedToSwitch: 1,
                  wMetronomeEnergyCost: 1, wNoEffectFromWhichStatus: 1, 0xC3F2: 9}},
        dict(POISON, wram={
            hWhoseTurn: b"\xC2", 0xC2BB: b"\x02", 0xC3BB: b"\x03",
            wPlayerDeck + 2: b"\x56", wOpponentDeck + 3: b"\x78",
            0xC3F2: b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA"},
             read={0xCCC3: 1, 0xCCC4: 1, 0xFF9F: 1, 0xC3F2: 9}),
        {"a": 0x01, "f": 0xF0, "b": 0x10, "c": 0x20, "d": 0x30,
         "e": 0x40, "hl": 0xC1FF,
         "wram": {hWhoseTurn: b"\xC3", 0xC3BB: b"\x3A",
                  0xC2BB: b"\x3B", wOpponentDeck + 0x3A: b"\x9A",
                  wPlayerDeck + 0x3B: b"\x9B", 0xC2F2: b"\xCC" * 9},
         "read": {0xCCC3: 1, 0xCCC4: 1, 0xFF9F: 1, 0xC2F2: 9}},
    ],
    "ClearNonTurnTemporaryDuelvars_ResetCarry": [
        {"wram": {hWhoseTurn: b"\xC2", 0xC3F2: b"\xFF" * 8},
         "read": {0xC3F2: 8}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC2F2: b"\xAA" * 8},
             read={0xC2F2: 8}),
        {"hl": 0xC1FF, "wram": {hWhoseTurn: b"\xC2", 0xC3F2: b"\x01" * 8},
         "read": {0xC3F2: 8}},
    ],
    "PrintKnockedOutIfHLZero": [
        {"hl": 0xC100, "wram": {0xC100: b"\x01"}},
        dict(POISON, hl=0xC101, wram={0xC101: b"\x02"}),
        {"hl": 0xC1FF, "wram": {0xC1FF: b"\x7F"}},
        {"hl": 0xC100, "wram": {0xC100: b"\x00", wTempNonTurnDuelistCardID: b"\x08",
                                0xCAD3: b"\x48\x03"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         "instruction_budget": 1000000, "cycle_budget": 4000000,
         "vread": {0: {0x9980: 1}}},
    ],
})

# >>> factory GetFirstSetPrizeCard
CONTRACT["GetFirstSetPrizeCard"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetFirstSetPrizeCard"] = [
    {},
    {"a": 1, "wram": {0xFF97: b"\xC1", 0xC1EC: b"\x02"}},
    {"a": 3, "wram": {0xFF97: b"\xC1", 0xC1EC: b"\x00"}},
    {"a": 5, "wram": {0xFF97: b"\xC1", 0xC1EC: b"\x01"}},
    {"a": 6, "wram": {0xFF97: b"\xC1", 0xC1EC: b"\x40"}},
    {"a": 8, "wram": {0xFF97: b"\xC1", 0xC1EC: b"\xFF"}},
    dict(POISON, a=4, wram={0xFF97: b"\xC1", 0xC1EC: b"\x01"}),
]
# <<< factory GetFirstSetPrizeCard

# >>> factory DrawCheckMenuCursor_YourOrOppPlayArea
CONTRACT["DrawCheckMenuCursor_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawCheckMenuCursor_YourOrOppPlayArea"] = [
    {"a": 0, "wram": {0xCEAF: b"\x00", 0xCEB0: b"\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"a": 0x5A, "wram": {0xCEAF: b"\x01", 0xCEB0: b"\x02"},
     "vread": {0: {0x9800: 0x400}}},
    {"a": 0xAC, "wram": {0xCEAF: b"\x02", 0xCEB0: b"\x03"},
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, a=0x33, wram={0xCEAF: b"\x01", 0xCEB0: b"\x01"},
         vread={0: {0x9800: 0x400}}),
]
# <<< factory DrawCheckMenuCursor_YourOrOppPlayArea

# >>> factory ZeroObjectPositionsWithCopyToggleOn
CONTRACT["ZeroObjectPositionsWithCopyToggleOn"] = {"compare": (), "preserve": ()}
CASES["ZeroObjectPositionsWithCopyToggleOn"] = [
    {"wram": {0xCAC0: b"\x00"}, "read": {0xC000: 0xA0}},
    dict(POISON, wram={0xCAC0: b"\xFF"}, read={0xC000: 0xA0}),
]
# <<< factory ZeroObjectPositionsWithCopyToggleOn

# >>> factory YourOrOppPlayAreaScreen_HandleInput
CONTRACT["YourOrOppPlayAreaScreen_HandleInput"] = {"compare": (), "preserve": ()}
CASES["YourOrOppPlayAreaScreen_HandleInput"] = [
    {"read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x00\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x40", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x00\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x80", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x00\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x10", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x00\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x20", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    dict(POISON,
         wram={0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x02\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x05",
               0xFF8F: b"\x40", 0xFF91: b"\x00"},
         read={0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}),
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x03\x00\xC3\x00", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x20", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x06\x00\xC3\x05", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x10", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x06\x00\xC3\x01", 0xCC08: b"\x02", 0xCEA3: b"\x00",
               0xFF8F: b"\x10", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x06\x00\xC3\x08", 0xCC08: b"\x04", 0xCEA3: b"\x00",
               0xFF8F: b"\x20", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x06\x00\xC3\x00", 0xCC08: b"\x05", 0xCEA3: b"\x00",
               0xFF8F: b"\x10", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x02\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x07",
               0xFF8F: b"\x00", 0xFF91: b"\x01"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x02\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x07",
               0xFF8F: b"\x00", 0xFF91: b"\x02"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x01\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x10",
               0xFF8F: b"\x00", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
    {"wram": {0xC300: b"\x10\x20\x30\x01\x02\x03\x04\x11\x21\x31\x00\x03\x02\x05\x12\x22\x32\x01\x04\x03\x06\x13\x23\x33\x02\x05\x04\x09\x14\x24\x34\x03\x06\x05\x01\x15\x25\x35\x04\x00\x06\x02\x16\x26\x36\x05\x01\x01\x05\x17\x27\x37\x06\x02\x00\x03",
               0xCE52: b"\x01\x00\xC3\xFF", 0xCC08: b"\x04", 0xCEA3: b"\x03",
               0xFF8F: b"\x00", 0xFF91: b"\x00"},
     "read": {0xCE52: 1, 0xCE61: 1, 0xCEA3: 1}},
]
# <<< factory YourOrOppPlayAreaScreen_HandleInput

# >>> factory DrawPlayArea_BenchCards
CONTRACT["DrawPlayArea_BenchCards"] = {"compare": (), "preserve": ()}
CASES["DrawPlayArea_BenchCards"] = [
    {"vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {0xCE50: b"\xC2", 0xCE51: b"\xC2", 0xC2EF: b"\x03",
              0xC2CF: b"\x00\x01\x02\x00"},
     "vread": {0: {0x9800: 0x400}}},
    dict(POISON, c=4, d=2, e=2,
         wram={0xCE50: b"\xC2", 0xCE51: b"\xC2", 0xC2EF: b"\x04",
               0xC2CF: b"\x02\x01\x00\x01"},
         vread={0: {0x9800: 0x400}}),
    {"c": 4, "d": 2, "e": 2,
     "wram": {0xCE50: b"\xC2", 0xCE51: b"\xC3", 0xC2EF: b"\x03",
              0xC2CF: b"\x00\x01\x02\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 1, "d": 0, "e": 0,
     "wram": {0xCE50: b"\xC2", 0xCE51: b"\xC2", 0xC2EF: b"\x00"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {0xCE50: b"\xC2", 0xCE51: b"\xC2", 0xC2EF: b"\x01"},
     "vread": {0: {0x9800: 0x400}}},
    {"c": 4, "d": 2, "e": 2,
     "wram": {0xCE50: b"\xC2", 0xCE51: b"\xC2", 0xC2EF: b"\x04",
              0xC2CF: b"\x00\x01\x02\x03", 0xCAB4: b"\x02"},
     "vread": {0: {0x9800: 0x400}, 1: {0x9800: 0x400}}},
]
# <<< factory DrawPlayArea_BenchCards

# >>> factory EraseCheckMenuCursor_YourOrOppPlayArea
CONTRACT["EraseCheckMenuCursor_YourOrOppPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["EraseCheckMenuCursor_YourOrOppPlayArea"] = [
    {"vread": {0: {0x9800: 0x400}}},
    dict(POISON, vread={0: {0x9800: 0x400}}),
    {"wram": {0xCE50: b"\xC2", 0xCE51: b"\xC3"},
     "vread": {0: {0x9800: 0x400}}},
]
# <<< factory EraseCheckMenuCursor_YourOrOppPlayArea

# >>> factory LoadCursorTile
CONTRACT["LoadCursorTile"] = {"compare": (), "preserve": ()}
CASES["LoadCursorTile"] = [
    {"keys": 1, "vread": {0: {0x8000: 16}}},
    {"keys": 2, "vread": {0: {0x8000: 16}}},
    dict(POISON, keys=1, vread={0: {0x8000: 16}}),
]
# <<< factory LoadCursorTile

# >>> factory Func_8bf2
CONTRACT["Func_8bf2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c",)}
CASES["Func_8bf2"] = [
    {"vread": {0: {0x9800: 1}}},
    {"hl": 0xC100, "c": 0x33,
     "wram": {0xC100: b"\x06\x05\x06\x06", 0xC2EC: b"\x01",
              0xCE50: b"\xC2", 0xCC08: b"\x02", 0xCAB4: b"\x01"},
     "vread": {0: {0x98A6: 1, 0x98C6: 1}}},
    {"hl": 0xC100, "c": 0x33,
     "wram": {0xC100: b"\x06\x05", 0xC2EC: b"\xFF",
              0xCE50: b"\xC2", 0xCC08: b"\x01", 0xCAB4: b"\x01"},
     "vread": {0: {0x98A6: 1}}},
    {"hl": 0xC100, "c": 0x33,
     "wram": {0xC100: b"\x07\x05", 0xC2EC: b"\x00",
              0xCE50: b"\xC2", 0xCC08: b"\x01", 0xCAB4: b"\x02"},
     "vread": {0: {0x98A7: 1}, 1: {0x98A7: 1}}},
    dict(POISON, hl=0xC100,
         wram={0xC100: b"\x06\x05", 0xC2EC: b"\x0F",
               0xCE50: b"\xC2", 0xCC08: b"\x00", 0xCAB4: b"\x01"},
         vread={0: {0x98A6: 1}}),
]
# <<< factory Func_8bf2

# >>> factory GetDuelInitialPrizesUpperBitsSet
CONTRACT["GetDuelInitialPrizesUpperBitsSet"] = {"compare": (), "preserve": ()}
CASES["GetDuelInitialPrizesUpperBitsSet"] = [
    {"wram": {0xCC08: b"\x00"}, "read": {0xCE55: 1}},
    dict(POISON, wram={0xCC08: b"\x01"}, read={0xCE55: 1}),
    {"wram": {0xCC08: b"\x02"}, "read": {0xCE55: 1}},
    {"wram": {0xCC08: b"\x06"}, "read": {0xCE55: 1}},
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
wYourOrOppPlayAreaLastCursorPosition = 0xCE5F

wCheckMenuCursorXPosition = 0xCEAF
wCheckMenuCursorYPosition = 0xCEB0
wYourOrOppPlayAreaLastCursorPosition = 0xCE5F

hTempCardIndex_ff9f = 0xFF9F
hTemp_ffa0 = 0xFFA0
wPlayerAttackingAttackIndex = 0xCC10
wPlayerAttackingCardIndex = 0xCC11
wSentAttackDataToLinkOpponent = 0xCCEC

wCheckMenuPlayAreaWhichDuelist = 0xCE50
wConsole = 0xCAB4
wDuelInitialPrizes = 0xCC08
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCheckMenuPlayAreaWhichLayout = 0xCE51
wTileMapFill = 0xCAB6
wVBlankOAMCopyToggle = 0xCAC0

wConsole = 0xCAB4
wDecimalDigitsSymbols = 0xCEB6
wDefaultText = 0xC590

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wPlayerArenaCard = 0xC2BB
wOpponentArenaCard = 0xC3BB
wDuelTurns = 0xCC06
wDuelType = 0xCC09
wTempTurnDuelistCardID = 0xCCC3
wTempNonTurnDuelistCardID = 0xCCC4
s0a008 = 0xA008
sDuelBuffer0 = 0xA000
BULBASAUR = 0x08
IVYSAUR = 0x09

hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
wMenuInputSFX = 0xCFE3
wCheckMenuCursorXPosition = 0xCEAF
wCheckMenuCursorYPosition = 0xCEB0
wCheckMenuCursorBlinkCounter = 0xCEA3

wCheckMenuPlayAreaWhichDuelist = 0xCE50
wDefaultText = 0xC590

wDefaultText = 0xC590

hTempPlayAreaLocation_ff9d = 0xFF9D
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wLoadedCard1Atk1Name = 0xCC34
wLoadedCard1Atk1Description = 0xCC36
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
wDefaultText = 0xC590
wLoadedCard1HP = 0xCC2C
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3
wCheckMenuPlayAreaWhichDuelist = 0xCE50
wCheckMenuPlayAreaWhichLayout = 0xCE51
wIsSwapTurnPending = 0xCE56
wDefaultText = 0xC730

hWhoseTurn = 0xFF97
wCheckMenuPlayAreaWhichDuelist = 0xCE50
wCheckMenuPlayAreaWhichLayout = 0xCE51
wDefaultText = 0xC590
wTileMapFill = 0xCAB6
wVBlankOAMCopyToggle = 0xCAC0

wCheckMenuPlayAreaWhichDuelist = 0xCE50
wCheckMenuPlayAreaWhichLayout = 0xCE51
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wIsSwapTurnPending = 0xCE56
wMenuInputTablePointer = 0xCE53
wVBlankOAMCopyToggle = 0xCAC0
wYourOrOppPlayAreaCurPosition = 0xCE52
wDefaultText = 0xC590

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wLoadedCard1Name = 0xCC27
wLoadedAttackName = 0xCCAA
wDefaultText = 0xC590
wTxRam2 = 0xCE3F
wTxRam2_b = 0xCE41
TEXT_SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wEffectFailed = 0xCCED
# <<< factory-cases-statics

# >>> factory DrawYourOrOppPlayArea_EraseArrows
CONTRACT["DrawYourOrOppPlayArea_EraseArrows"] = {"compare": (), "preserve": ()}
CASES["DrawYourOrOppPlayArea_EraseArrows"] = [
    {"wram": {0xCE5F: b"\x00"},
     "vread": {0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                    0x994C: 1, 0x9950: 1}}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD,
     "e": 0xEE, "hl": 0x1234,
     "wram": {0xCE5F: b"\x00"},
     "vread": {0: {0x98A5: 1, 0x9940: 1, 0x9944: 1, 0x9948: 1,
                    0x994C: 1, 0x9950: 1}}},
]
# <<< factory DrawYourOrOppPlayArea_EraseArrows

# >>> factory DrawYourOrOppPlayArea_RefreshArrows
CONTRACT["DrawYourOrOppPlayArea_RefreshArrows"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawYourOrOppPlayArea_RefreshArrows"] = [
    {"a": 0x00, "wram": {wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, "read": {wYourOrOppPlayAreaLastCursorPosition: 1}},
    {"a": 0x12, "wram": {wCheckMenuCursorXPosition: b"\x01", wCheckMenuCursorYPosition: b"\x02", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, "read": {wYourOrOppPlayAreaLastCursorPosition: 1}},
    dict(POISON, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={wCheckMenuCursorXPosition: b"\x00", wCheckMenuCursorYPosition: b"\x00", wYourOrOppPlayAreaLastCursorPosition: b"\x00"}, read={wYourOrOppPlayAreaLastCursorPosition: 1}),
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
    {"hl": 0xC500,
     "wram": {0xCE50: b"\xC4", 0xC4EC: b"\x01", 0xCC08: b"\x02", 0xCAB4: b"\x00", 0xC500: b"\x00\x00\x00\x02"},
     "vread": {0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}},
    {"hl": 0xC510,
     "wram": {0xCE50: b"\xC4", 0xC4EC: b"\x02", 0xCC08: b"\x02", 0xCAB4: b"\x00", 0xC510: b"\x00\x00\x00\x02"},
     "vread": {0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}},
    dict(POISON,
         hl=0xC520,
         wram={0xCE50: b"\xC4", 0xC4EC: b"\x01", 0xCC08: b"\x02", 0xCAB4: b"\x02", 0xC520: b"\x00\x00\x00\x02"},
         vread={0: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2},
                1: {0x9800: 2, 0x9820: 2, 0x9840: 2, 0x9860: 2}}),
]
# <<< factory DrawPlayArea_PrizeCards

# >>> factory _DrawPlayersPrizeAndBenchCards
CONTRACT["_DrawPlayersPrizeAndBenchCards"] = {"compare": (), "preserve": ()}
CASES["_DrawPlayersPrizeAndBenchCards"] = [
    {"instruction_budget": 1000000, "cycle_budget": 4000000,
     "read": {wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
     "expect": {wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}},
    dict(POISON, instruction_budget=1000000, cycle_budget=4000000,
         read={wCheckMenuPlayAreaWhichLayout: 1, wTileMapFill: 1, wVBlankOAMCopyToggle: 1},
         expect={wCheckMenuPlayAreaWhichLayout: b"\xC2", wTileMapFill: b"\x00", wVBlankOAMCopyToggle: b"\x01"}),
]
# <<< factory _DrawPlayersPrizeAndBenchCards

# >>> factory DrawPlayArea_HandText
CONTRACT["DrawPlayArea_HandText"] = {"compare": ("b", "c", "hl"), "preserve": ("c",)}
CASES["DrawPlayArea_HandText"] = [
    {"b": 0x00, "c": 0x07, "hl": 0xC500, "wram": {0xC500: b"\x01\x02"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC590: 7, 0xCEB6: 2}},
    dict(POISON, b=0x00, c=0x07, hl=0xC500, wram={0xC500: b"\x01\x02"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC590: 7, 0xCEB6: 2}),
    {"b": 0x2D, "c": 0x11, "hl": 0xC500, "wram": {0xC500: b"\x03\x04"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC590: 7, 0xCEB6: 2}},
]
# <<< factory DrawPlayArea_HandText

# >>> factory DrawPlayArea_IconWithValue
CONTRACT["DrawPlayArea_IconWithValue"] = {"compare": ("hl",), "preserve": (), "wram_out": True}
CASES["DrawPlayArea_IconWithValue"] = [
    {"a": 0xD4, "b": 0x2A, "c": 0x33, "hl": 0xC500,
     "wram": {wConsole: b"\x00", 0xC500: b"\x0F\x02"},
     "read": {wDefaultText: 7, wDecimalDigitsSymbols: 2},
     "expect": {wDefaultText: b"\x05\x2D\x05\x32\x05\x20\x00", wDecimalDigitsSymbols: b"\x20\x32"}},
    dict(POISON, a=0xD8, b=0x63, hl=0xC510,
         wram={wConsole: b"\x02", 0xC510: b"\x01\x09"},
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
]
# <<< factory HandleCheckMenuInput_YourOrOppPlayArea

# >>> factory DrawYourOrOppPlayArea_Icons
CONTRACT["DrawYourOrOppPlayArea_Icons"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayArea_Icons"] = [
    {"a": 0x00, "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03"},
     "read": {wDefaultText: 7},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, a=0x01, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC3", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00"},
         read={wDefaultText: 7},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayArea_Icons

# >>> factory DrawInPlayArea_Icons
CONTRACT["DrawInPlayArea_Icons"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawInPlayArea_Icons"] = [
    {"hl": 0xC500, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
              0xC500: b"\x0F\x02\x0F\x04\x0F\x06"}, "read": {wDefaultText: 7},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0xC500, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
              0xC500: b"\x0F\x02\x0F\x04\x0F\x06"}, read={wDefaultText: 7},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawInPlayArea_Icons

# >>> factory DisplayUsePokemonPowerScreen_WaitForInput
CONTRACT["DisplayUsePokemonPowerScreen_WaitForInput"] = {"compare": ("f",), "preserve": ()}
CASES["DisplayUsePokemonPowerScreen_WaitForInput"] = [
    {"hl": 0x0000, "keys": 0x01, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempPlayAreaLocation_ff9d: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0x0000, keys=0x01, instruction_budget=5000000, cycle_budget=20000000,
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
              0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
              0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00"},
     "read": {wDefaultText: 7, wIsSwapTurnPending: 1, wCheckMenuPlayAreaWhichLayout: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)),
               0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00"},
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
    {"wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", 0xC2BB: b"\xFF", 0xC2BC: b"\x00"},
     "sram": {}, "vread": {0: {0x8A00: 1, 0x9800: 1}}},
    dict(POISON, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC2", 0xC2BB: b"\xFF", 0xC2BC: b"\x00"},
         vread={0: {0x8A00: 1, 0x9800: 1}}),
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0x08, "e": 0x06,
     "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", 0xC2BB: b"\x00", wPlayerDeck: b"\x00"},
     "vread": {0: {0x8A00: 1, 0x98C8: 1}}},
]
# <<< factory DrawYourOrOppPlayArea_ActiveCardGfx

# >>> factory _DrawYourOrOppPlayAreaScreen
CONTRACT["_DrawYourOrOppPlayAreaScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["_DrawYourOrOppPlayAreaScreen"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000, "wram": {hWhoseTurn: b"\xC2", wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16}, "read": {wDefaultText: 7}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000, wram={hWhoseTurn: b"\xC2", wCheckMenuPlayAreaWhichDuelist: b"\xC3", wCheckMenuPlayAreaWhichLayout: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16}, read={wDefaultText: 7}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory _DrawYourOrOppPlayAreaScreen

# >>> factory DrawYourOrOppPlayAreaScreen
CONTRACT["DrawYourOrOppPlayAreaScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawYourOrOppPlayAreaScreen"] = [
    {"hl": 0xC3C2, "instruction_budget": 20000000, "cycle_budget": 80000000, "wram": {wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", 0xC590: b"\x00" * 16}, "read": {0xC590: 7}, "expect": {wCheckMenuPlayAreaWhichDuelist: b"\xC3", wCheckMenuPlayAreaWhichLayout: b"\xC2"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000, wram={wCheckMenuPlayAreaWhichDuelist: b"\xC2", wCheckMenuPlayAreaWhichLayout: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03", 0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", 0xC590: b"\x00" * 16}, read={0xC590: 7}, expect={wCheckMenuPlayAreaWhichDuelist: b"\x12", wCheckMenuPlayAreaWhichLayout: b"\x34"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DrawYourOrOppPlayAreaScreen

# >>> factory _DrawAIPeekScreen
CONTRACT["_DrawAIPeekScreen"] = {"compare": (), "preserve": ()}
CASES["_DrawAIPeekScreen"] = [
    {"b": 0x00, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
     "read": {wIsSwapTurnPending: 1, wMenuInputTablePointer: 2, wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
     "vread": {0: {0x9800: 32, 0x9C00: 32}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, b=0x80, keys=0x01, instruction_budget=20000000, cycle_budget=80000000,
         wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
         read={wIsSwapTurnPending: 1, wMenuInputTablePointer: 2, wYourOrOppPlayAreaCurPosition: 1, wVBlankOAMCopyToggle: 1, wDefaultText: 7},
         vread={0: {0x9800: 32, 0x9C00: 32}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
    {"b": 0xFF, "keys": 0x01, "instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x05", 0xC2BA: b"\x0A", 0xC2ED: b"\x03",
               0xC3EE: b"\x02", 0xC3BA: b"\x37", 0xC3ED: b"\x00", wDefaultText: b"\x00" * 16},
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
]
# <<< factory PrintFailedEffectText

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
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
    "ClearNonTurnTemporaryDuelvars_ResetCarry": {
        "source_symbol": "ClearNonTurnTemporaryDuelvars_ResetCarry",
        "before": "ClearNonTurnTemporaryDuelvars();",
        "after": "(void)0;",
        "case_ids": ["ClearNonTurnTemporaryDuelvars_ResetCarry-0",
                     "ClearNonTurnTemporaryDuelvars_ResetCarry-1"],
    },
    "PrintKnockedOutIfHLZero": {
        "source_symbol": "PrintKnockedOutIfHLZero",
        "before": "\t(void)PrintKnockedOut();\n\treturn 0x90u;",
        "after": "\t(void)PrintKnockedOut();\n\treturn 0xd0u;",
        "case_ids": ["PrintKnockedOutIfHLZero-0",
                     "PrintKnockedOutIfHLZero-1",
                     "PrintKnockedOutIfHLZero-3"],
    },
}
# >>> factory-mutation GetFirstSetPrizeCard
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
    "before": "\tif ((new_counter & (1u << B_CURSOR_BLINK_PERIOD)) == 0u) {",
    "after": "\tif ((new_counter & (1u << B_CURSOR_BLINK_PERIOD)) != 0u) {",
    "case_ids": ["HandleCheckMenuInput_YourOrOppPlayArea-0", "HandleCheckMenuInput_YourOrOppPlayArea-1"],
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
