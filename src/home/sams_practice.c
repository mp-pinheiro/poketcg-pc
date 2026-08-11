#include "home/sams_practice.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"

#define MACHOP 0x7Du

IsAIPracticeScriptedTurnResult IsAIPracticeScriptedTurn(void)
{
	uint8_t a = (uint8_t)(wDuelTurns >> 1);
	uint8_t f = (a == 7u) ? 0x90u : (a < 7u ? 0x00u : 0x10u);
	return (IsAIPracticeScriptedTurnResult){a, f};
}

SamsPracticeResult SetSamsStartingPlayArea(uint8_t c, uint8_t b, uint8_t d,
                                           uint8_t e, uint16_t hl)
{
	HandListResult list = CreateHandCardList(c);
	uint8_t a = list.a;
	b = list.b;
	c = list.c;
	d = list.d;
	e = list.e;
	hl = list.hl;
	for (uint8_t i = 0;; i++) {
		uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + i));
		hTempCardIndex_ff98 = entry;
		if (entry == 0xFFu)
			return (SamsPracticeResult){entry, b, c, d, e, 0xC0u, hl};
		a = LoadCardDataToBuffer1_FromDeckIndex(entry);
		if (a != MACHOP)
			continue;
		PutHandPokemonResult put = PutHandPokemonCardInPlayArea(entry, 0xC0u);
		wDuelInitialPrizes = 2;
		return (SamsPracticeResult){put.a, b, c, d, e, put.f, put.hl};
	}
}
