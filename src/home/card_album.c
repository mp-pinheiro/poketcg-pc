#include "home/card_album.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define CARD_NOT_OWNED 0x80u

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/card_data.h"
#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/process_text.h"
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define FALSE 0x00u
#define MEW_LV15 0xA1u
#define TRUE 0x01u
#define TX_SYMBOL 0x05u
#define VENUSAUR_LV64 0x0Au
#define SYM_BOX_TOP_R 0x19u
#define SYM_BOX_BTM_R 0x1Du
#define SYM_CURSOR_U 0x0Cu
#define SYM_CURSOR_D 0x2Fu
/* <<< factory statics */

/* >>> factory GetFirstOwnedCardIndex */
/* card_album.asm:612-624. Scans wOwnedCardsCountList for the first entry
 * that is not CARD_NOT_OWNED; no bound check, so it relies on the caller
 * guaranteeing at least one owned entry (card_album.asm:660-662,717-719).
 * hl exits one past the byte that ended the scan (post-increment ld a,[hli]
 * on every iteration, including the last). */
GetFirstOwnedCardIndexResult GetFirstOwnedCardIndex(void)
{
	uint16_t hl = wOwnedCardsCountList_ADDR;
	uint8_t index = 0;

	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card != CARD_NOT_OWNED)
			break;
		index++;
	}
	gb_write8(wFirstOwnedCardIndex_ADDR, index);
	return (GetFirstOwnedCardIndexResult){ .a = index, .b = index, .hl = hl };
}
/* <<< factory GetFirstOwnedCardIndex */

/* >>> factory PrintCardSetListEntries */
PrintCardSetListEntriesResult PrintCardSetListEntries(void)
{
	uint16_t hl = wCardListCoords_ADDR;
	uint8_t e = gb_read8(hl++);
	uint8_t d = gb_read8(hl);
	uint8_t visible_offset = wCardListVisibleOffset;
	uint8_t tile = visible_offset ? SYM_CURSOR_U : SYM_BOX_TOP_R;
	WriteByteToBGMap0(tile, d, (uint8_t)(e - 2u));
	hl = visible_offset;
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		uint8_t card = gb_read8((uint16_t)(wFilteredCardList_ADDR + hl));
		hl = (uint16_t)(hl + 1u);
		if (card == 0u) break;
		--count;
	}
	hl = (uint16_t)(wFilteredCardList_ADDR + hl);
	if (gb_read8(hl) == 0u) {
		gb_write8(wUnableToScrollDown_ADDR, TRUE);
		tile = SYM_BOX_BTM_R;
	} else {
		gb_write8(wUnableToScrollDown_ADDR, FALSE);
		tile = SYM_CURSOR_D;
	}
	WriteByteToBGMap0(tile, 19u, 17u);
	return (PrintCardSetListEntriesResult){ .hl = hl };
}
/* <<< factory PrintCardSetListEntries */
