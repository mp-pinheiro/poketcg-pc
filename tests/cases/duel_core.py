POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
CARD = 0xC100  # stand-in for wLoadedCard1
LOCATION = 0xC200  # player duel variables page

CONTRACT = {
    "ConvertSpecialTrainerCardToPokemon": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "ConvertSpecialTrainerCardToPokemon": [
        # Not a trainer: a = card type, hl untouched, nothing written.
        {"a": 0, "hl": CARD, "d": 0, "e": 0,
         "wram": {CARD: b"\x06", hWhoseTurn: b"\xC2"},
         "read": {CARD: 1}},
        # Trainer but not in the play area: early return, a = 0.
        {"a": 1, "hl": CARD, "d": 0, "e": 0,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 1: b"\x00"},
         "read": {CARD: 1}},
        # Trainer in the play area, wrong card id: a = id high byte.
        {"a": 1, "hl": CARD, "d": 0x01, "e": 0x02,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 1: b"\x10"},
         "read": {CARD: 1}},
        # Mysterious Fossil in play area: card rewritten to colorless Pokemon.
        {"a": 2, "hl": CARD, "d": 0x00, "e": 0xCC,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 2: b"\x10"},
         "read": {CARD: 64}},
        # Clefairy Doll in play area: same overwrite path.
        {"a": 3, "hl": CARD, "d": 0x00, "e": 0xCB,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 3: b"\x10"},
         "read": {CARD: 64}},
        # Fossil with a non-zero id high byte: exits with a = d, no overwrite.
        {"a": 4, "hl": CARD, "d": 0x02, "e": 0xCC,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 4: b"\x10"},
         "read": {CARD: 1}},
        # Poisoned registers: preserved b/d/e on the not-a-trainer path.
        dict(POISON, a=0, hl=CARD, d=0x00, e=0x01,
             wram={CARD: b"\x06", hWhoseTurn: b"\xC2"}, read={CARD: 1}),
    ],
}
