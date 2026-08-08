POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

# hWhoseTurn (player $C2 / opponent $C3) selects the duel-variables page.
hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wOpponentDuelVariables = 0xC300

CONTRACT = {
    "CopyPlayerName": ("a", "b", "c", "d", "e", "hl"),
    "CopyOpponentName": ("a", "b", "c", "d", "e", "hl"),
    "GetTurnDuelistVariable": ("b", "c", "d", "e", "hl"),
    "GetNonTurnDuelistVariable": ("b", "c", "d", "e", "hl"),
    "SwapTurn": ("b", "c", "d", "e", "hl"),
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
}
