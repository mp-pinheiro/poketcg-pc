#include "home/card_collection.h"

#include "generated/constants.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/card_id_bus.h"
#include "home/load_deck.h"
#include "home/switch_sram.h"
#include "mem.h"

#define CARD_SLOT(table, id) ((uint16_t)((table) + (uint16_t)(id)))

/* card_collection.asm:129-146 .AddDeckCards. */
static void add_deck_cards(uint16_t de)
{
	if ((uint8_t)(gb_read8(de) | gb_read8((uint16_t)(de + 1u))) == 0u)
		return;
	uint16_t source = (uint16_t)(de + 24u);
	uint16_t cards = wCurDeckCards_ADDR;
	DecompressSRAMDeck(source, cards);
	for (uint8_t i = 0; i < 60; i++) {
		CardId card = card_id_read(&cards);
		uint16_t hl = CARD_SLOT(wTempCardCollection_ADDR, card);
		gb_write8(hl, (uint8_t)(gb_read8(hl) + 1));
	}
}

void CreateTempCardCollection(void)
{
	EnableSRAM();
	uint16_t hl = sCardCollection_ADDR;
	uint16_t de = wTempCardCollection_ADDR;
	CopyDataHLtoDE(&hl, &de, card_id_collection_bytes());
	add_deck_cards(sDeck1Name_ADDR);
	add_deck_cards(sDeck2Name_ADDR);
	add_deck_cards(sDeck3Name_ADDR);
	add_deck_cards(sDeck4Name_ADDR);
	DisableSRAM();
}

void AddCardToCollection(CardId a)
{
	CreateTempCardCollection();
	EnableSRAM();
	uint16_t temp_hl = CARD_SLOT(wTempCardCollection_ADDR, a);
	uint8_t owned = (uint8_t)(gb_read8(temp_hl) & 0x7Fu); /* CARD_COUNT_MASK */
	if (owned < 99) { /* MAX_AMOUNT_OF_CARD */
		uint16_t coll_hl = CARD_SLOT(sCardCollection_ADDR, a);
		uint8_t count = (uint8_t)(gb_read8(coll_hl) & 0x7Fu);
		gb_write8(coll_hl, (uint8_t)(count + 1));
	}
	DisableSRAM();
}

AlbumProgress GetCardAlbumProgress(void)
{
	EnableSRAM();
	uint16_t owned = 0u;
	for (uint16_t i = 0u; i < CARD_COLLECTION_SIZE; i++) {
		if ((gb_read8((uint16_t)(sCardCollection_ADDR + i)) & 0x80u) == 0u)
			owned++;
	}
	uint16_t total = NUM_CARDS;
	if ((gb_read8((uint16_t)(sCardCollection_ADDR + VENUSAUR_LV64)) & 0x80u) != 0u)
		total--;
	if ((gb_read8((uint16_t)(sCardCollection_ADDR + MEW_LV15)) & 0x80u) != 0u)
		total--;
	DisableSRAM();
	return (AlbumProgress){
		(uint8_t)(total >> 8), (uint8_t)total,
		(uint8_t)(owned >> 8), (uint8_t)owned};
}

/* card_collection.asm:2-41. Sums DECK_SIZE for every deck whose first card slot
 * (not its name byte, unlike .AddDeckCards) is non-zero, plus every owned card's
 * raw count byte in sCardCollection (CARD_NOT_OWNED_F clear). */
uint16_t GetAmountOfCardsOwned(void)
{
	EnableSRAM();
	uint16_t hl = 0u;
	uint16_t de = sDeck1Cards_ADDR;
	for (uint8_t i = 0u; i < 4u; i++) {
		if (card_id_read_at(de) != 0u)
			hl = (uint16_t)(hl + DECK_SIZE);
		de = (uint16_t)(de + (sDeck2Cards_ADDR - sDeck1Cards_ADDR));
	}
	for (uint16_t i = 0; i < card_id_collection_bytes(); i++) { /* CARD_COLLECTION_SIZE */
		uint8_t card = gb_read8((uint16_t)(sCardCollection_ADDR + i));
		if (!(card & 0x80u)) /* CARD_NOT_OWNED_F */
			hl = (uint16_t)(hl + card);
	}
	DisableSRAM();
	return hl;
}

/* card_collection.asm:46-93. id = card ID in (consumed). Counts matches of id
 * across all four decks' Cards arrays, each walked from its Cards-array base --
 * the inner `ld a,[hli]` walk advances a copy of hl that gets discarded by the
 * `pop hl` after the loop, so the per-deck base used for the next stride add is
 * always the deck's original start, never the post-walk position. Adds the match
 * count onto the collection's owned count unless CARD_NOT_OWNED_F is set, masks
 * to CARD_COUNT_MASK, and returns carry set iff the masked result is 0. */
CardCountResult GetCardCountInCollectionAndDecks(CardId id)
{
	EnableSRAM();
	uint8_t matches = 0u;
	uint16_t de = sDeck1Cards_ADDR;
	for (uint8_t i = 0u; i < 4u; i++) {
		uint16_t compressed = de;
		if (card_id_read_at(compressed) != 0u) {
			DecompressSRAMDeck(compressed, wCurDeckCards_ADDR);
			uint16_t cards = wCurDeckCards_ADDR;
			for (uint8_t k = 0u; k < DECK_SIZE; k++) {
				if (card_id_read(&cards) == id)
					matches = (uint8_t)(matches + 1u);
			}
		}
		de = (uint16_t)(de + (sDeck2Cards_ADDR - sDeck1Cards_ADDR));
	}
	uint16_t coll_hl = CARD_SLOT(sCardCollection_ADDR, id);
	uint8_t a = gb_read8(coll_hl);
	if (!(a & 0x80u))
		a = (uint8_t)(a + matches);
	a &= 0x7Fu;
	DisableSRAM();
	return (CardCountResult){ .a = a, .f = (uint8_t)(a == 0u ? 0x90u : 0x00u) };
}

/* card_collection.asm:97-108. id = card ID in (consumed), hl preserved. Real
 * outputs: a (masked owned count) and carry (set iff a==0). Returns straight
 * after `and CARD_COUNT_MASK` with no intervening `or a`, so H stays set by the
 * `and` on the nonzero exit (0x20), unlike the *AndDecks sibling above. */
CardCountResult GetCardCountInCollection(CardId id)
{
	EnableSRAM();
	uint8_t a = (uint8_t)(gb_read8(CARD_SLOT(sCardCollection_ADDR, id)) & 0x7Fu); /* CARD_COUNT_MASK */
	DisableSRAM();
	return (CardCountResult){ .a = a, .f = (uint8_t)(a == 0 ? 0x90u : 0x20u) };
}

/* card_collection.asm:177-190. id = card ID in, hl preserved via push/pop.
 * Decrements the masked count in place unless it is already 0. Exit a/f are
 * whatever DisableSRAM leaves behind -- no caller reads either (grep:
 * scripting.asm:1068-1069/1110-1111/1229-1230), so neither is part of the
 * contract; b/c/d/e are never referenced at all and pass through untouched. */
void RemoveCardFromCollection(CardId id)
{
	EnableSRAM();
	uint16_t hl = CARD_SLOT(sCardCollection_ADDR, id);
	uint8_t count = (uint8_t)(gb_read8(hl) & 0x7Fu); /* CARD_COUNT_MASK */
	if (count != 0)
		gb_write8(hl, (uint8_t)(count - 1));
	DisableSRAM();
}
