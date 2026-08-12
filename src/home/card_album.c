#include "home/card_album.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define CARD_NOT_OWNED 0x80u
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
