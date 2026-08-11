#include "home/science_club_lobby.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "home/random.h"
#include "mem.h"

static const uint8_t science_club_cards[] = {0xBDu, 0xBBu, 0x27u, 0x2Bu};

void Script_Specs2(void)
{
	uint8_t card = science_club_cards[UpdateRNGSources() & 3u];
	uint16_t name = GetCardName(card);

	gb_write8(wTxRam2_ADDR, (uint8_t)name);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), (uint8_t)(name >> 8));
}
