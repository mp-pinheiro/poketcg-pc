"""Oracle-diff cases for poketcg/src/home/card_collection.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sCardCollection = 0xA100
CARD_COLLECTION_SIZE = 0x100
wTempCardCollection = 0xC000
hBankSRAM = 0xFF81

sDeck1Name = 0xA200
sDeck2Name = 0xA254
sDeck3Name = 0xA2A8
sDeck4Name = 0xA2FC
DECK_SIZE = 60

sDeck1Cards = 0xA218
sDeck2Cards = 0xA26C
sDeck3Cards = 0xA2C0
sDeck4Cards = 0xA314


def deck(built, cards=None):
    """24-byte name field (first byte nonzero iff built) + 60 card-id bytes."""
    name = (b"\x01" if built else b"\x00") + b"\x00" * 23
    body = bytes(cards) if cards is not None else b"\x00" * DECK_SIZE
    assert len(body) == DECK_SIZE
    return name + body


CONTRACT = {
    # No register contract at all: there is no push/pop anywhere in :111-146, so
    # a/f/b/c/de/hl are all clobbered and none is preserved. The residue is not even
    # constant -- a and f split on whether deck 4 is built, de ends $A2FC or $A350,
    # hl ends $A200 or $C000+lastcard -- but no caller consumes any of it
    # (printer.asm:691 overwrites de; card_collection.asm:155 push/pops hl and
    # reloads h/a), so naming any of them would only hardcode a value into the
    # adapter. The memory image is the whole contract.
    "CreateTempCardCollection": {"compare": (), "preserve": ()},
    # hl/de/bc are pushed/popped around the whole body; a is scratch (never
    # restored), f is clobbered by `and`/`cp`/`inc` with no restore.
    "AddCardToCollection": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    # a/b/c are never referenced by the asm at all, so they pass through
    # untouched; hl is pushed/popped. f is clobbered by `bit` with no restore.
    "GetCardAlbumProgress": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "hl")},
    # hl is the sum output; b/c/d/e are push/pop-preserved (:3-4/39-40). a/f scratch.
    "GetAmountOfCardsOwned": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    # a/f are real outputs (masked count, carry set iff a==0); hl/de/bc are
    # push/pop-preserved around the whole body (:47-49/86-89).
    "GetCardCountInCollectionAndDecks": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    # a/f are real outputs; hl is push/pop-preserved (:98/104); b/c/d/e are never
    # referenced by the asm at all, so they pass through untouched.
    "GetCardCountInCollection": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    # hl is push/pop-preserved (:178/189); b/c/d/e are never referenced. a/f are
    # scratch -- no caller reads either (scripting.asm:1068-1069/1110-1111/1229-1230).
    "RemoveCardFromCollection": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "CreateTempCardCollection": [
        # All decks empty (default-zero name fields): temp collection is a
        # straight copy of sCardCollection, which is itself left untouched.
        {"sram": {0: {sCardCollection: bytes(range(256))}},
         "sread": {0: {sCardCollection: CARD_COLLECTION_SIZE}},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # All four decks built and non-overlapping: each deck's 60 ids get a
        # single increment on top of a zeroed collection. Poisoned registers,
        # since the routine takes no arguments and must ignore them.
        dict(POISON,
             sram={0: {
                 sCardCollection: b"\x00" * 256,
                 sDeck1Name: deck(True, range(0, 60)),
                 sDeck2Name: deck(True, range(60, 120)),
                 sDeck3Name: deck(True, range(120, 180)),
                 sDeck4Name: deck(True, range(180, 240)),
             }},
             read={wTempCardCollection: CARD_COLLECTION_SIZE}),
        # Mix: deck 2 empty but with garbage (id 0xFF) card bytes seeded anyway,
        # to prove an empty deck's card data is never read.
        {"sram": {0: {
            sCardCollection: b"\x00" * 256,
            sDeck1Name: deck(True, range(10, 70)),
            sDeck2Name: deck(False, [0xFF] * DECK_SIZE),
            sDeck3Name: deck(True, range(70, 130)),
            sDeck4Name: deck(True, range(130, 190)),
        }},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # Collision: deck 1 lists the same card id 60 times, so its temp entry
        # is incremented 60 times over.
        {"sram": {0: {
            sCardCollection: b"\x00" * 256,
            sDeck1Name: deck(True, [42] * DECK_SIZE),
        }},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # High and adjacent card ids. This does NOT exercise a page-index wrap: l is
        # reloaded from the card byte every iteration and never incremented, so no
        # wrap exists to drive. It stands as a distinct-high-ids case.
        {"sram": {0: {
            sCardCollection: b"\x00" * 256,
            sDeck1Name: deck(True, [0xFE] * 15 + [0xFF] * 15 + [0x00] * 15 + [0x01] * 15),
        }},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # `inc [hl]` is a plain 8-bit increment with no CARD_COUNT_MASK anywhere on
        # this path, unlike AddCardToCollection three lines away in the asm. Every
        # case above increments from a zero base, so a port that masked here would
        # diff clean. Card 42 starts at $FF and takes 59 increments ($FF + 59 = $3A
        # after the wrap); card 7 starts at $80 and takes one, so bit 7 must survive
        # into $81 rather than being masked down to $01.
        {"sram": {0: {
            sCardCollection: bytes(0xFF if i == 42 else 0x80 if i == 7 else 0x00
                                   for i in range(256)),
            sDeck1Name: deck(True, [42] * 59 + [7]),
        }},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # The routine calls EnableSRAM, not BankswitchSRAM: the wTempCardCollection
        # output proves which bank was live. Bank 2 is seeded last, so it is live,
        # and its collection and deck must be the ones copied. A bank-0-hardcoded port
        # or one that used BankswitchSRAM to enable would fail here and nowhere else.
        {"sram": {0: {sCardCollection: b"\x11" * 256,
                      sDeck1Name: deck(True, [200] * DECK_SIZE)},
                  2: {sCardCollection: bytes(range(256)),
                      sDeck1Name: deck(True, [99] * DECK_SIZE)}},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # No `sram` key at all, so the RAMG latch is off at entry on both sides: this
        # is the only case where the routine's own EnableSRAM is load-bearing. Without
        # it every read is open bus $FF, so all four decks read as built and their card
        # bytes as $FF, and the temp collection ends up garbage instead of all zero.
        {"ramg": False, "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
    ],
    "AddCardToCollection": [
        # All-zero: card 0 with an empty collection and no decks. Increments 0 -> 1.
        {"sram": {0: {sCardCollection: b"\x00" * 256}},
         "sread": {0: {sCardCollection + 0: 1}}},
        # Poisoned hl/de/bc must survive both the internal CreateTempCardCollection
        # call and the increment itself.
        dict(POISON, a=0x10,
             sram={0: {sCardCollection: b"\x00" * 256}},
             sread={0: {sCardCollection + 0x10: 1}},
             read={wTempCardCollection: CARD_COLLECTION_SIZE}),
        # Count below 99: increments.
        {"a": 0x05, "sram": {0: {sCardCollection: bytes([5 if i == 5 else 0 for i in range(256)])}},
         "sread": {0: {sCardCollection + 5: 1}}},
        # Count exactly 99: cp 99 / jr nc takes the already_max branch, no increment.
        {"a": 0x06, "sram": {0: {sCardCollection: bytes([99 if i == 6 else 0 for i in range(256)])}},
         "sread": {0: {sCardCollection + 6: 1}}},
        # Count above 99 (masked value 110): also already_max, no increment.
        {"a": 0x07, "sram": {0: {sCardCollection: bytes([110 if i == 7 else 0 for i in range(256)])}},
         "sread": {0: {sCardCollection + 7: 1}}},
        # Not-owned bit set (0x80, masked count 0): increment stores the
        # masked-then-incremented value, so bit 7 is dropped on the way out.
        {"a": 0xFF, "sram": {0: {sCardCollection: bytes([0x80 if i == 0xFF else 0 for i in range(256)])}},
         "sread": {0: {sCardCollection + 0xFF: 1}}},
        # Deck contributions push the temp count to exactly 99 while
        # sCardCollection alone reads 50: still already_max, sCardCollection
        # must not be incremented past 50.
        {"a": 0x00,
         "sram": {0: {
             sCardCollection: bytes([50 if i == 0 else 0 for i in range(256)]),
             sDeck1Name: deck(True, [0x00] * 49 + list(range(1, 12))),
         }},
         "sread": {0: {sCardCollection + 0: 1}}, "read": {wTempCardCollection + 0: 1}},
        # 98 is the largest masked temp count that still increments. Without it the
        # threshold is only pinned from above (99 skips), so `owned < 98` -- or any
        # cut in [6, 99] -- would diff clean.
        {"a": 0x08, "sram": {0: {sCardCollection: bytes([98 if i == 8 else 0 for i in range(256)])}},
         "sread": {0: {sCardCollection + 8: 1}}},
        # The stored value is RE-READ from sCardCollection (asm :164-168); only the
        # threshold test reads wTempCardCollection. Every case above leaves the decks
        # empty, so the two tables are byte-identical and a port that incremented the
        # temp value instead would diff clean. Here one deck copy of card 5 wraps
        # temp[5] from $FF to $00, so the masked temp is 0 (increment path) while the
        # collection byte is still $FF: the store must be ($FF & $7F) + 1 = $80, not 1.
        {"a": 0x05,
         "sram": {0: {
             sCardCollection: bytes([0xFF if i == 5 else 0 for i in range(256)]),
             sDeck1Name: deck(True, [5] + [0] * 59),
         }},
         "sread": {0: {sCardCollection + 5: 1}},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
        # Neither this routine nor CreateTempCardCollection bank-switches, so both
        # tables resolve under whichever bank the caller left selected -- bank 2 on
        # the shipped path (save.asm:536-539). Bank 2 is seeded last, so it is live:
        # its card 3 must go 10 -> 11 while bank 0's distinct byte is untouched. A
        # port using the flat bank-0 lvalue would pass every case above.
        {"a": 0x03,
         "wram": {hBankSRAM: b"\x02"},
         "sram": {0: {sCardCollection: bytes([77 if i == 3 else 0x11 for i in range(256)])},
                  2: {sCardCollection: bytes([10 if i == 3 else 0 for i in range(256)])}},
         "read": {wTempCardCollection: CARD_COLLECTION_SIZE}},
    ],
    "GetCardAlbumProgress": [
        # All-zero, and deliberately with no `sram` key: seeding latches RAMG on in
        # both worlds, so this is the only case that enters with SRAM disabled and
        # therefore the only one giving the routine's own EnableSRAM teeth. Without
        # it, gb_read8 would return open-bus $FF and both special bytes would read as
        # not-owned. Every collection byte is 0, so all 256 count as owned and d wraps
        # back to 0, while e stays at NUM_CARDS.
        {},
        # Neither special card owned, and nothing else owned either.
        {"sram": {0: {sCardCollection: b"\x80" * 256}}},
        # Every one of the 256 collection bytes owned: d wraps a full 8-bit
        # counter back to 0 after 256 increments, and both special cards count.
        {"sram": {0: {sCardCollection: b"\x01" * 256}}},
        # Venusaur owned, Mew not: only Venusaur's byte is unset.
        dict(POISON, a=0xAA,
             sram={0: {sCardCollection: bytes(0x00 if i == 0x0A else 0x80 for i in range(256))}}),
        # Mew owned, Venusaur not: mirror of the above.
        {"sram": {0: {sCardCollection: bytes(0x00 if i == 0xA1 else 0x80 for i in range(256))}}},
        # Both special cards owned, nothing else.
        {"sram": {0: {sCardCollection: bytes(0x00 if i in (0x0A, 0xA1) else 0x80 for i in range(256))}}},
        # Exactly one card unowned: d = 255, the largest value the 8-bit counter
        # reaches without wrapping, and the only case where its high bits are set.
        {"sram": {0: {sCardCollection: bytes(0x80 if i == 0 else 0x00 for i in range(256))}}},
        # The routine calls EnableSRAM, not BankswitchSRAM, so it reads whichever bank
        # the caller left selected and must leave hBankSRAM alone. Bank 2 is seeded
        # last, so it is live: the answer must come from bank 2 (Venusaur owned there,
        # nothing owned in bank 0). A bank-0-hardcoded port reports d=0/e=226 instead
        # of d=1/e=227, and a port that bank-switched would move hBankSRAM off 3.
        {"wram": {hBankSRAM: b"\x02"},
         "sram": {0: {sCardCollection: b"\x80" * 256},
                  2: {sCardCollection: bytes(0x00 if i == 0x0A else 0x80 for i in range(256))}},
         "read": {hBankSRAM: 1}},
    ],
    "GetAmountOfCardsOwned": [
        # All-zero: all four decks empty (first Cards byte 0) and every collection
        # byte owned with a 0 count.
        {"sram": {0: {sCardCollection: b"\x00" * 256, sDeck1Cards: b"\x00" * DECK_SIZE,
                      sDeck2Cards: b"\x00" * DECK_SIZE, sDeck3Cards: b"\x00" * DECK_SIZE,
                      sDeck4Cards: b"\x00" * DECK_SIZE}}},
        # Poisoned b/c/d/e must survive; all four decks built (first byte nonzero)
        # contribute DECK_SIZE each regardless of their actual card ids, plus every
        # collection byte's own count.
        dict(POISON,
             sram={0: {
                 sCardCollection: bytes((i * 3) & 0x7F for i in range(256)),
                 sDeck1Cards: bytes(((i + 1) % 256) for i in range(DECK_SIZE)),
                 sDeck2Cards: bytes(((i + 5) % 256) for i in range(DECK_SIZE)),
                 sDeck3Cards: bytes(((i + 9) % 256) for i in range(DECK_SIZE)),
                 sDeck4Cards: bytes(((i + 13) % 256) for i in range(DECK_SIZE)),
             }}),
        # Deck 1's built check reads only offset +0 (`ld a,[de]`): its first byte is
        # 0 despite 59 nonzero bytes after it, so it must count as empty and
        # contribute nothing. Deck 2 is built; decks 3/4 stay empty.
        {"sram": {0: {
            sCardCollection: b"\x00" * 256,
            sDeck1Cards: bytes([0] + [0xFF] * (DECK_SIZE - 1)),
            sDeck2Cards: bytes([7] * DECK_SIZE),
            sDeck3Cards: b"\x00" * DECK_SIZE,
            sDeck4Cards: b"\x00" * DECK_SIZE,
        }}},
        # CARD_NOT_OWNED_F set with nonzero low bits: excluded from the sum
        # entirely, not added as its masked low-7-bit value.
        {"sram": {0: {
            sCardCollection: bytes(0xB3 if i == 9 else 0x00 for i in range(256)),
            sDeck1Cards: b"\x00" * DECK_SIZE, sDeck2Cards: b"\x00" * DECK_SIZE,
            sDeck3Cards: b"\x00" * DECK_SIZE, sDeck4Cards: b"\x00" * DECK_SIZE,
        }}},
        # ramg:False after seeding: the routine's own EnableSRAM must still make
        # the all-zero pattern above observable, or every read comes back as open
        # bus $FF (nonzero, so both the deck-built checks and the sum would be
        # very different from 0).
        {"ramg": False,
         "sram": {0: {sCardCollection: b"\x00" * 256, sDeck1Cards: b"\x00" * DECK_SIZE,
                      sDeck2Cards: b"\x00" * DECK_SIZE, sDeck3Cards: b"\x00" * DECK_SIZE,
                      sDeck4Cards: b"\x00" * DECK_SIZE}}},
    ],
    "GetCardCountInCollectionAndDecks": [
        # All-zero: id 0, decks empty, collection[0] owned with count 0.
        {"sram": {0: {sCardCollection: b"\x00" * 256, sDeck1Cards: b"\x00" * DECK_SIZE,
                      sDeck2Cards: b"\x00" * DECK_SIZE, sDeck3Cards: b"\x00" * DECK_SIZE,
                      sDeck4Cards: b"\x00" * DECK_SIZE}}},
        # Poisoned entry (id = 0xAA); collection[0xAA] owned with a nonzero count,
        # decks left empty.
        dict(POISON,
             sram={0: {sCardCollection: bytes(11 if i == 0xAA else 0 for i in range(256))}}),
        # Deck 1 built and lists id 7 three times: matches add onto the owned count.
        {"a": 0x07,
         "sram": {0: {
             sCardCollection: bytes(10 if i == 7 else 0 for i in range(256)),
             sDeck1Cards: bytes([7, 7, 1] + [2] * 56 + [7]),
         }}},
        # collection[20] has CARD_NOT_OWNED_F set: the add is skipped entirely, so
        # deck 2's five matches of id 20 must not appear in the result at all.
        {"a": 20,
         "sram": {0: {
             sCardCollection: bytes(0x80 if i == 20 else 0 for i in range(256)),
             sDeck2Cards: bytes([20] * 5 + [0] * (DECK_SIZE - 5)),
         }}},
        # 8-bit wraparound in the un-masked `add b` before the final mask:
        # 0x7F + 2 matches wraps to 0x81, masked down to 0x01.
        {"a": 3,
         "sram": {0: {
             sCardCollection: bytes(0x7F if i == 3 else 0 for i in range(256)),
             sDeck1Cards: bytes([3, 3] + [0] * (DECK_SIZE - 2)),
         }}},
        # ramg:False after seeding, over the deck-1-matches-id-7 case above.
        {"a": 0x07, "ramg": False,
         "sram": {0: {
             sCardCollection: bytes(10 if i == 7 else 0 for i in range(256)),
             sDeck1Cards: bytes([7, 7, 1] + [2] * 56 + [7]),
         }}},
    ],
    "GetCardCountInCollection": [
        {"sram": {0: {sCardCollection: b"\x00" * 256}}},
        dict(POISON, sram={0: {sCardCollection: bytes(42 if i == 0xAA else 0 for i in range(256))}}),
        # CARD_NOT_OWNED_F set but nonzero low bits: unlike *AndDecks, this routine
        # never tests the bit, only masks it, so the low 7 bits still come through.
        {"a": 5, "sram": {0: {sCardCollection: bytes(0xAA if i == 5 else 0 for i in range(256))}}},
        # Masked-zero via the not-owned flag alone (low 7 bits also 0): carry set.
        {"a": 6, "sram": {0: {sCardCollection: bytes(0x80 if i == 6 else 0 for i in range(256))}}},
        # id 0xFF: last byte of the page-aligned collection table.
        {"a": 0xFF, "sram": {0: {sCardCollection: bytes(0x33 if i == 0xFF else 0 for i in range(256))}}},
        {"a": 5, "ramg": False, "sram": {0: {sCardCollection: bytes(0xAA if i == 5 else 0 for i in range(256))}}},
    ],
    "RemoveCardFromCollection": [
        # All-zero: count already 0, so the store is skipped and the byte is
        # unchanged (idempotent at the floor).
        {"sram": {0: {sCardCollection: b"\x00" * 256}}},
        # Poisoned b/c/d/e/hl must survive; id 5 decrements 10 -> 9.
        dict(POISON, a=5, sram={0: {sCardCollection: bytes(10 if i == 5 else 0 for i in range(256))}}),
        # Decrement to exactly 0.
        {"a": 6, "sram": {0: {sCardCollection: bytes(1 if i == 6 else 0 for i in range(256))}}},
        # CARD_NOT_OWNED_F set alongside a nonzero masked count (0x81 = flag + 1):
        # the stored result is the masked-then-decremented value, so the flag bit
        # is dropped -- the byte lands on $00, not $80.
        {"a": 8, "sram": {0: {sCardCollection: bytes(0x81 if i == 8 else 0 for i in range(256))}}},
        # Boundary: max masked value 0x7F decrements to 0x7E.
        {"a": 9, "sram": {0: {sCardCollection: bytes(0x7F if i == 9 else 0 for i in range(256))}}},
        # ramg:False: the write only lands if the routine's own EnableSRAM/DisableSRAM
        # pair actually gates it.
        {"a": 5, "ramg": False, "sram": {0: {sCardCollection: bytes(10 if i == 5 else 0 for i in range(256))}}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GetCardCountInCollection": {
        "source_symbol": "GetCardCountInCollection",
        "before": "\tuint8_t a = (uint8_t)(gb_read8(CARD_SLOT(sCardCollection_ADDR, id)) & 0x7Fu);",
        "after": "\tuint8_t a = (uint8_t)(gb_read8(CARD_SLOT(sCardCollection_ADDR, id)) & 0xFFu);",
        "case_ids": ["GetCardCountInCollection-2", "GetCardCountInCollection-0", "GetCardCountInCollection-1", "GetCardCountInCollection-3", "GetCardCountInCollection-4", "GetCardCountInCollection-5"],
    },
}
