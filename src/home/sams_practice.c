#include "home/sams_practice.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

SamsPracticeResult IsAIPracticeScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t shifted = (uint8_t)(gb_read8(wDuelTurns_ADDR) >> 1);
	uint8_t flags = (uint8_t)((shifted == 7 ? 0x80u : 0u) |
					 (shifted >= 7 ? 0x10u : 0u));
	return (SamsPracticeResult){shifted, flags, b, c, d, e, hl};
}

SamsPracticeResult SetSamsStartingPlayArea(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	HandListResult list = CreateHandCardList(c);
	uint16_t scan = wDuelTempList_ADDR;

	b = list.b;
	d = list.d;
	e = list.e;
	c = list.c;
	for (;;) {
		a = gb_read8(scan++);
		hTempCardIndex_ff98 = a;
		if (a == 0xffu)
			return (SamsPracticeResult){a, 0xe0u, b, c, d, e, scan};
		if (LoadCardDataToBuffer1_FromDeckIndex(a) == 0x7du) {
			f = 0xc0u;
			break;
		}
	}

	a = hTempCardIndex_ff98;
	PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(a, f);
	gb_write8(wDuelInitialPrizes_ADDR, 2);
	return (SamsPracticeResult){2, placed.f, b, c, d, e, placed.hl};
}
