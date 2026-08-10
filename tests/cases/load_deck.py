"""Oracle-diff cases for poketcg/src/home/load_deck.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDeckName = 0xCCE9

CONTRACT = {
    "LoadDeck": {"compare": ("f", "hl"), "preserve": ("hl",)},
}

CASES = {
    "LoadDeck": [
        {"a": 1, "wram": {hWhoseTurn: bytes((PLAYER_TURN,))},
         "read": {wPlayerDeck: 60, wDeckName: 2}},
        {"a": 8, "wram": {hWhoseTurn: bytes((OPPONENT_TURN,))},
         "read": {wOpponentDeck: 60, wDeckName: 2}},
        {"a": 2, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerDeck: b"\xff" * 8},
         "read": {wPlayerDeck: 60, wDeckName: 2}},
        {"a": 55, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerDeck: b"\xee" * 60},
         "read": {wPlayerDeck: 60}},
        dict(POISON, a=55, wram={hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerDeck: b"\xee" * 60},
             read={wPlayerDeck: 60}),
        dict(POISON, a=3, wram={hWhoseTurn: bytes((PLAYER_TURN,))},
             read={wPlayerDeck: 60, wDeckName: 2}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "LoadDeck": {
        "source_symbol": "LoadDeck",
        "before": "uint8_t carry = 1;",
        "after": "uint8_t carry = 0;",
        "case_ids": ["LoadDeck-0", "LoadDeck-1", "LoadDeck-2", "LoadDeck-3", "LoadDeck-4", "LoadDeck-5"],
    },
}
