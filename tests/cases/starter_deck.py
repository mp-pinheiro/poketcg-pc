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

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
sAnimationsDisabled = 0xA007
sCardAndDeckSaveData = 0xA100
sCardCollection = 0xA100
sCardPopNameList = 0xBB00
sCurrentDuel = 0xBC00
sPrinterContrastLevel = 0xA003
sReceivedLegendaryCards = 0xA00A
sSavedDeck1 = 0xA350
sSavedDeck2 = 0xA3A4
sSavedDeck3 = 0xA3F8
sSkipDelayAllowed = 0xA009
sTextSpeed = 0xA006
sTotalCardPopsDone = 0xA005
wTextSpeed = 0xCE47
# <<< factory-cases-statics

# >>> factory InitSaveData
CONTRACT["InitSaveData"] = {"compare": (), "preserve": ()}
CASES["InitSaveData"] = [
    {"wram": {hWhoseTurn: b"\xFF"},
     "sram": {0: {sCardAndDeckSaveData: bytes([0xAA] * 32), sCardCollection: bytes([0x11] * 256),
                  sCurrentDuel: b"\xAA\xBB\xCC", sCardPopNameList: bytes([0x22] * 256),
                  sPrinterContrastLevel: b"\xFF", sTextSpeed: b"\xFF", sAnimationsDisabled: b"\xFF",
                  sSkipDelayAllowed: b"\xFF", 0xA004: b"\xFF", sTotalCardPopsDone: b"\xFF",
                  sReceivedLegendaryCards: b"\xFF"}},
     "read": {hWhoseTurn: 1, wTextSpeed: 1},
     "sread": {0: {sCardAndDeckSaveData: 32, sCardCollection: 256, sSavedDeck1: 32, sSavedDeck2: 32,
                   sSavedDeck3: 32, sCurrentDuel: 3, sCardPopNameList: 256, sPrinterContrastLevel: 1,
                   sTextSpeed: 1, sAnimationsDisabled: 1, sSkipDelayAllowed: 1, 0xA004: 1,
                   sTotalCardPopsDone: 1, sReceivedLegendaryCards: 1}},
     "vread": {0: {0x9380: 32}}},
    dict(POISON, wram={hWhoseTurn: b"\xFF"},
         sram={0: {sCardAndDeckSaveData: bytes([0x55] * 32), sCardCollection: bytes([0x33] * 256),
                   sCurrentDuel: b"\x11\x22\x33", sCardPopNameList: bytes([0x44] * 256)}},
         read={hWhoseTurn: 1, wTextSpeed: 1},
         sread={0: {sCardAndDeckSaveData: 32, sCardCollection: 256, sSavedDeck1: 32, sSavedDeck2: 32,
                    sSavedDeck3: 32, sCurrentDuel: 3, sCardPopNameList: 256, sPrinterContrastLevel: 1,
                    sTextSpeed: 1, sAnimationsDisabled: 1, sSkipDelayAllowed: 1, 0xA004: 1,
                    sTotalCardPopsDone: 1, sReceivedLegendaryCards: 1}},
         vread={0: {0x9380: 32}}),
]
# <<< factory InitSaveData

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
# >>> factory-mutation InitSaveData
MUTATIONS["InitSaveData"] = {"source_symbol": "InitSaveData", "before": "\tgb_write8(sPrinterContrastLevel_ADDR, 2u);", "after": "\tgb_write8(sPrinterContrastLevel_ADDR, 3u);", "case_ids": ["InitSaveData-0", "InitSaveData-1"]}
# <<< factory-mutation InitSaveData
