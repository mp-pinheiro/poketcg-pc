#include "home/trainer_cards.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "mem.h"

#define TYPE_ENERGY 0x08u

#include "home/card_data.h"
#include "home/duel.h"

#include "home/duel.h"
#include "home/card_data.h"

#include "home/trainer_cards.h"

#include "home/duel.h"
#include "home/card_data.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory RemoveCardFromList */
/* trainer_cards.asm:2760-2776. Shifts the $ff-terminated list down by one byte,
 * removing the entry just before hl. Leaves hl decremented; de preserved. */
void RemoveCardFromList(uint16_t *hl)
{
	uint16_t src = *hl;
	uint16_t dst = (uint16_t)(src - 1u);
	uint8_t v;
	do {
		v = gb_read8(src);
		src = (uint16_t)(src + 1u);
		gb_write8(dst, v);
		dst = (uint16_t)(dst + 1u);
	} while (v != 0xFFu);
	*hl = (uint16_t)(*hl - 1u);
}
/* <<< factory RemoveCardFromList */

/* >>> factory FindDuplicateCards */
/* trainer_cards.asm:2788-2859 */
FindDupResult FindDuplicateCards(uint16_t hl)
{
	wce0f = 0xFFu;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0xFFu);
	uint16_t outer = hl;
	for (;;) {
		uint8_t idx = gb_read8(outer);
		outer = (uint16_t)(outer + 1u);
		if (idx == 0xFFu)
			break;
		uint8_t b = (uint8_t)GetCardIDFromDeckIndex(idx);
		uint16_t inner = outer;
		for (;;) {
			uint8_t c = gb_read8(inner);
			inner = (uint16_t)(inner + 1u);
			if (c == 0xFFu)
				break;
			if ((uint8_t)GetCardIDFromDeckIndex(c) != b)
				continue;
			if (GetCardType(b) < TYPE_ENERGY)
				wce0f = c;
			else
				gb_write8((uint16_t)(wce0f_ADDR + 1u), c);
			break;
		}
	}
	uint8_t lo = wce0f;
	uint8_t hi = gb_read8((uint16_t)(wce0f_ADDR + 1u));
	if (lo == 0xFFu && hi == 0xFFu)
		return (FindDupResult){0xFFu, 0x90u};
	uint8_t a = (lo != 0xFFu) ? lo : hi;
	return (FindDupResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory FindDuplicateCards */

/* >>> factory FindAndRemoveCardFromList */
/* trainer_cards.asm:3072-3082 */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl)
{
	uint16_t p = hl;
	uint8_t v;
	do {
		v = gb_read8(p);
		p = (uint16_t)(p + 1u);
	} while (v != a);
	RemoveCardFromList(&p);
}
/* <<< factory FindAndRemoveCardFromList */
