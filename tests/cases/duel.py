POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# hWhoseTurn (player $C2 / opponent $C3) selects the duel-variables page.
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wOpponentDuelVariables = 0xC300
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDuelTempList = 0xC510

CONTRACT = {
    "CopyPlayerName": ("a", "b", "c", "d", "e", "hl"),
    "CopyOpponentName": ("a", "b", "c", "d", "e", "hl"),
    "GetTurnDuelistVariable": ("b", "c", "d", "e", "hl"),
    "GetNonTurnDuelistVariable": ("b", "c", "d", "e", "hl"),
    "SwapTurn": ("b", "c", "d", "e", "hl"),
    "_GetCardIDFromDeckIndex": ("a", "b", "c", "d", "e", "hl"),
    "GetCardIDFromDeckIndex": ("a", "b", "c", "d", "e", "hl"),
    "GetCardIDFromDeckIndex_bc": ("a", "b", "c", "d", "e", "hl"),
    "GetCardInDuelTempList_OnlyDeckIndex": ("a", "b", "c", "d", "e", "hl"),
    "GetCardInDuelTempList": ("a", "b", "c", "d", "e", "hl"),
    "LoadCardDataToBuffer1_FromDeckIndex": ("a", "b", "c", "d", "e", "hl"),
    "LoadCardDataToBuffer2_FromDeckIndex": ("a", "b", "c", "d", "e", "hl"),
    "SubtractHP": ("a", "b", "c", "d", "e", "f", "hl"),
    "CreateDeckCardList": ("a", "b", "c", "d", "e", "f", "hl"),
    "CreateDiscardPileCardList": ("a", "b", "c", "d", "e", "f", "hl"),
    "RemoveCardFromDuelTempList": ("a", "b", "c", "d", "e", "f", "hl"),
    "CountCardsInDuelTempList": ("a", "b", "c", "d", "e", "f", "hl"),
    "FindLastCardInHand": ("a", "b", "c", "d", "e", "f", "hl"),
    "CreateHandCardList": ("a", "b", "c", "d", "e", "f", "hl"),
    "CreateArenaOrBenchEnergyCardList": ("a", "b", "c", "d", "e", "f", "hl"),
    "ShuffleCards": ("a", "b", "c", "d", "e", "f", "hl"),
    "SortCardsInListByID": ("a", "b", "c", "d", "e", "f", "hl"),
    "SortCardsInDuelTempListByID": ("a", "b", "c", "d", "e", "f", "hl"),
}

CASES = {
    "CopyPlayerName": [
        {"d": 0xC1, "e": 0x00, "sram": {0: {0xA010: b"\x21\x22\x00"}},
         "read": {0xC100: 3}},
        dict(POISON, d=0xC2, e=0x00,
             sram={2: {0xA010: b"\x31\x00"}}, read={0xC200: 2}),
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
}
