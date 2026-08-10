POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

H_WHOSE_TURN = 0xFF97
W_WHOSE_TURN = 0xCC05
PLAYER = 0xC200
OPPONENT = 0xC300
INITIAL_PRIZES = 0xCC08
ALREADY_PLAYED = 0xCC0B
CONFUSION_CHECK = 0xCC0C
SAND_ATTACK_CHECK = 0xCC0D
NUMBER_PRIZES = 0xCCC8
PLAYER_DECK = 0xC400
OPPONENT_DECK = 0xC480
PRIZES = 0xEC

CONTRACT = {
    "InitVariablesToBeginTurn": ("a", "b", "c", "d", "e", "hl"),
    "SetAllPlayAreaPokemonCanEvolve": ("a", "b", "c", "d", "e", "hl"),
    "InitializeDuelVariables": ("a", "b", "c", "d", "e", "hl"),
    "InitTurnDuelistPrizes": ("a", "b", "c", "d", "e", "hl"),
    "TakeAPrizes": ("a", "b", "c", "d", "e", "hl"),
    "CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut": ("a", "b", "c", "d", "e", "hl"),
    "CountKnockedOutPokemon": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "InitVariablesToBeginTurn": [
        {"wram": {H_WHOSE_TURN: b"\xC2", ALREADY_PLAYED: b"\xFF",
                  CONFUSION_CHECK: b"\xFF", SAND_ATTACK_CHECK: b"\xFF"},
         "read": {W_WHOSE_TURN: 1, ALREADY_PLAYED: 1, CONFUSION_CHECK: 1,
                  SAND_ATTACK_CHECK: 1}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", ALREADY_PLAYED: b"\xFF",
                           CONFUSION_CHECK: b"\xFF", SAND_ATTACK_CHECK: b"\xFF"},
             read={W_WHOSE_TURN: 1, ALREADY_PLAYED: 1, CONFUSION_CHECK: 1,
                   SAND_ATTACK_CHECK: 1}),
    ],
    "SetAllPlayAreaPokemonCanEvolve": [
        {"wram": {H_WHOSE_TURN: b"\xC2", PLAYER + 0xEF: b"\x01",
                  PLAYER + 0xC2: b"\x20"}, "read": {PLAYER + 0xC2: 1}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", OPPONENT + 0xEF: b"\x05",
                           OPPONENT + 0xC2: b"\xA0"},
             read={OPPONENT + 0xC2: 5}),
    ],
    "InitializeDuelVariables": [
        {"wram": {H_WHOSE_TURN: b"\xC2", PLAYER + 0xF1: b"\x81"},
         "read": {PLAYER: 0x100}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", OPPONENT + 0xF1: b"\x02"},
             read={OPPONENT: 0x100}),
    ],
    "InitTurnDuelistPrizes": [
        {"wram": {H_WHOSE_TURN: b"\xC2", INITIAL_PRIZES: b"\x01",
                  PLAYER + 0xBA: b"\x00", PLAYER_DECK: bytes(range(60))},
         "read": {PLAYER + 0x3C: 2, PLAYER + 0x00: 1}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", INITIAL_PRIZES: b"\x06",
                           OPPONENT + 0xBA: b"\x00", OPPONENT_DECK: bytes(range(60))},
             read={OPPONENT + 0x3C: 7, OPPONENT + 0x00: 1}),
    ],
    "TakeAPrizes": [
        {"a": 1, "wram": {H_WHOSE_TURN: b"\xC2", PLAYER + PRIZES: b"\x3F"},
         "read": {PLAYER + PRIZES: 1}},
        dict(POISON, a=0, wram={H_WHOSE_TURN: b"\xC3", OPPONENT + PRIZES: b"\x3F"},
             read={OPPONENT + PRIZES: 1}),
    ],
    "CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut": [
        {"wram": {H_WHOSE_TURN: b"\xC2", PLAYER + 0xEF: b"\x01",
                  PLAYER + 0xC8: b"\x00"}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", OPPONENT + 0xEF: b"\x05",
                           OPPONENT + 0xC8: b"\x00\x00\x01\x00\x00"}),
    ],
    "CountKnockedOutPokemon": [
        {"wram": {H_WHOSE_TURN: b"\xC2", PLAYER + 0xC8: b"\x00" * 5 + b"\xFF",
                  PLAYER + 0xBB: b"\x00" * 5 + b"\xFF", PLAYER_DECK: bytes(range(60))},
         "oracle": False,
         "why": "GetCardType enters banked card data unavailable to the oracle",
         "expect": {NUMBER_PRIZES: b"\x05"},
         "expect_regs": {"a": 5, "b": 5, "c": 0, "d": 0xC2, "e": 0xC1,
                         "hl": 0xC2CE}},
        dict(POISON, wram={H_WHOSE_TURN: b"\xC3", OPPONENT + 0xC8: b"\x00" * 5 + b"\xFF",
                           OPPONENT + 0xBB: b"\x00" * 5 + b"\xFF",
                           OPPONENT_DECK: bytes(range(60))},
             oracle=False,
             why="GetCardType enters banked card data unavailable to the oracle",
             expect={NUMBER_PRIZES: b"\x05"},
             expect_regs={"a": 5, "b": 5, "c": 0, "d": 0xC3, "e": 0xC1,
                         "hl": 0xC3CE}),
    ],
}
