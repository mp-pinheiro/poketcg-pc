#include "home/card_collection.h"

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/switch_sram.h"
#include "mem.h"

#define CARD_SLOT(table, id) ((uint16_t)(((table) & 0xFF00u) | (uint8_t)(id)))

/* card_collection.asm:129-146 .AddDeckCards. */
static void add_deck_cards(uint16_t de)
{
	if (gb_read8(de) == 0)
		return;
	de = (uint16_t)(de + 24); /* DECK_NAME_SIZE: sDeck1Cards - sDeck1Name */
	for (uint8_t i = 0; i < 60; i++) { /* DECK_SIZE */
		uint8_t card = gb_read8(de);
		de++;
		uint16_t hl = CARD_SLOT(wTempCardCollection_ADDR, card);
		gb_write8(hl, (uint8_t)(gb_read8(hl) + 1));
	}
}

void CreateTempCardCollection(void)
{
	EnableSRAM();
	uint16_t hl = sCardCollection_ADDR;
	uint16_t de = wTempCardCollection_ADDR;
	CopyDataHLtoDE(&hl, &de, 0x0100u); /* CARD_COLLECTION_SIZE */
	add_deck_cards(sDeck1Name_ADDR);
	add_deck_cards(sDeck2Name_ADDR);
	add_deck_cards(sDeck3Name_ADDR);
	add_deck_cards(sDeck4Name_ADDR);
	DisableSRAM();
}

void AddCardToCollection(uint8_t a)
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
	uint8_t e = 228; /* NUM_CARDS */
	if (gb_read8(CARD_SLOT(sCardCollection_ADDR, 0x0A)) & 0x80u) /* VENUSAUR_LV64 */
		e--;
	if (gb_read8(CARD_SLOT(sCardCollection_ADDR, 0xA1)) & 0x80u) /* MEW_LV15 */
		e--;
	/* d is seeded from LOW(sCardCollection) = 0 and doubles as the loop index and the
	 * owned counter, so a fully owned collection wraps it back to 0 after 256 steps.
	 * The loop ends when `inc l` wraps, not on a sentinel. */
	uint8_t d = 0;
	for (uint16_t i = 0; i < 256; i++) {
		if (!(gb_read8(CARD_SLOT(sCardCollection_ADDR, i)) & 0x80u))
			d++;
	}
	DisableSRAM();
	return (AlbumProgress){ .d = d, .e = e };
}
