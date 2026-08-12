"""Oracle-diff cases for poketcg/src/engine/starter_deck.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory CopyDeckNameAndCards
CONTRACT["CopyDeckNameAndCards"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CopyDeckNameAndCards"] = [
    # All-zero: deck id 0 (UnnamedDeck, valid) with hl=0. Writes below $8000
    # decode as MBC5 register hits rather than SRAM -- the same
    # degenerate-but-well-defined path tests/cases/copy.py's
    # CopyDataHLtoDE exercises with hl=de=0. hWhoseTurn=0 != PLAYER_TURN, so
    # LoadDeck fills wOpponentDeck; wPlayerDeck (the routine's own
    # unconditional card source) stays zero, and that zero is exactly what
    # gets copied.
    {},
    # Poisoned b/c/d/e/f must survive LoadDeck, CopyText, EnableSRAM/
    # DisableSRAM and both copy loops. a and hl are the two consumed inputs
    # (deck id, destination), so they are overridden to a real deck id and a
    # real SRAM address; hWhoseTurn=PLAYER_TURN so LoadDeck fills wPlayerDeck.
    # Destination is seeded across the whole 84-byte slot plus 4 trailing
    # guard bytes.
    dict(POISON, a=5, hl=0xA400,
         wram={0xFF97: bytes((0xC2,))},
         sram={0: {0xA400: bytes((i * 2 + 9) & 0xFF for i in range(88))}}),
    # Valid deck id: the full 24-byte name field plus 60-byte card array
    # actually land in SRAM. The 88-byte seed (84 payload + 4 trailing guard
    # bytes) catches both an under-write and an overflow past
    # DECK_NAME_SIZE+DECK_SIZE.
    {"a": 12, "hl": 0xA200,
     "wram": {0xFF97: bytes((0xC2,))},
     "sram": {0: {0xA200: bytes((i * 3 + 1) & 0xFF for i in range(88))}}},
    # Invalid deck id (57 = the DeckPointers NULL terminator,
    # poketcg/src/data/decks.asm:58): LoadDeck's carry must skip both copy
    # loops entirely, leaving the destination exactly as seeded.
    {"a": 57, "hl": 0xA800,
     "wram": {0xFF97: bytes((0xC2,))},
     "sram": {0: {0xA800: bytes((i * 5 + 3) & 0xFF for i in range(88))}}},
    # SRAM latch starts disabled: the routine's own EnableSRAM must still
    # make the write land, or the seeded bytes read back untouched.
    {"a": 20, "hl": 0xA600, "ramg": False,
     "wram": {0xFF97: bytes((0xC2,))},
     "sram": {0: {0xA600: bytes((i * 7 + 2) & 0xFF for i in range(88))}}},
]
# <<< factory CopyDeckNameAndCards

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CopyDeckNameAndCards
MUTATIONS["CopyDeckNameAndCards"] = {
    "source_symbol": "CopyDeckNameAndCards",
    "before": "if (LoadDeck(a))",
    "after": "if (!LoadDeck(a))",
    "case_ids": ["CopyDeckNameAndCards-1", "CopyDeckNameAndCards-2",
                 "CopyDeckNameAndCards-3", "CopyDeckNameAndCards-4"],
}
# <<< factory-mutation CopyDeckNameAndCards
