"""Oracle-diff cases for poketcg/src/home/ai.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3

wOpponentDeckID = 0xCC0E
wIsPracticeDuel = 0xCC13
wRNG1 = 0xCACA
wRNG2 = 0xCACB
wRNGCounter = 0xCACC
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDeckName = 0xCCE9
wPlayerDuelistType = 0xC2F1
wOpponentDuelistType = 0xC3F1

CONTRACT = {
    "LoadOpponentDeck": ("a", "hl"),
}

CASES = {
    "LoadOpponentDeck": [
        # Sam-normal (deck id 2): forces PRACTICE_PLAYER_DECK onto the OTHER
        # duelist via a swap-load-swap, reseeds the RNG, then loads
        # SAMS_PRACTICE_DECK for the current turn holder.
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x02"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wRNG1: 1, wRNG2: 1,
                  wRNGCounter: 1, wOpponentDeck: 60, wPlayerDeck: 60,
                  wDeckName: 2, wPlayerDuelistType: 1}},
        # Sam-practice (deck id 0): same shape, wIsPracticeDuel ends up 1.
        {"wram": {hWhoseTurn: bytes((OPPONENT_TURN,)), wOpponentDeckID: b"\x00"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wRNG1: 1, wRNG2: 1,
                  wRNGCounter: 1, wOpponentDeck: 60, wPlayerDeck: 60,
                  wDeckName: 2, wOpponentDuelistType: 1}},
        # Plain deck id (not 0 or 2): no Sam handling, no RNG reseed, deck
        # loaded straight onto the current turn holder at deck_id+2.
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x05"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wPlayerDeck: 60,
                  wDeckName: 2, wPlayerDuelistType: 1}},
        # Right at the boundary (deck_id == NUM_DECK_IDS): DeckPointers[55] is
        # NULL in the real ROM, so LoadDeck no-ops (carry, no copy) -- safe to
        # run, and proves the clamp does NOT fire at 53 (53 < NUM_DECK_IDS+1).
        {"wram": {hWhoseTurn: bytes((OPPONENT_TURN,)), wOpponentDeckID: b"\x35"},
         "read": {wOpponentDeckID: 1, wOpponentDuelistType: 1}},
        dict(POISON, wram={hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x09"},
             read={wIsPracticeDuel: 1, wOpponentDeckID: 1, wPlayerDeck: 60,
                   wDeckName: 2, wPlayerDuelistType: 1}),
        # NUM_DECK_IDS+1 clamp (deck_id=54): oracle-unsafe to run for real --
        # DeckPointers[56] (deck_id+2) is a non-NULL pointer into fixed bank 0
        # ($0614), landing on raw code bytes. copy_deck_data's unbounded
        # (quantity, card-id) loop never finds a terminating zero within a
        # sane distance there (traced by hand: 40+ pairs summing past 4700
        # bytes with no end in sight), so it would scribble across most of
        # WRAM on real hardware too. Verified only against the C port's own
        # clamp logic, never against the oracle.
        {"oracle": False,
         "why": "deck_id=54 clamp forces a LoadDeck(56) read of raw code as "
                "deck data (DeckPointers[56]=$0614, fixed bank 0) -- an "
                "unbounded copy loop that would corrupt WRAM broadly on real "
                "hardware too, not something safe to run through the oracle.",
         "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x36"},
         "expect": {wOpponentDeckID: b"\x01", wPlayerDuelistType: b"\x81"},
         "expect_regs": {"a": 0x81}},
    ],
}
