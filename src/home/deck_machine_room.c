#include "home/deck_machine_room.h"

#include "generated/wram.h"
#include "mem.h"

#define CLUB_MAP_NAMES 0x5985u
#define CLUB_MAP_NAMES_BANK 3u
#define EVENT_AARON_BOOSTER_REWARD_OFFSET 0x1Au
#define EVENT_AARON_BOOSTER_REWARD_MASK 0x03u

FuncD96cResult Func_d96c(uint8_t a)
{
	uint8_t offset = (uint8_t)((uint8_t)(a - 2u) << 1);
	uint16_t hl = (uint16_t)(CLUB_MAP_NAMES + offset);
	const uint8_t *entry = rom_ptr(CLUB_MAP_NAMES_BANK, hl);
	uint8_t lo = entry[0];
	uint8_t hi = entry[1];

	gb_write8(wTxRam2_ADDR, lo);
	gb_write8(wTxRam2_b_ADDR, lo);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), hi);
	return (FuncD96cResult){hi, 0, offset, (uint16_t)(hl + 1u)};
}

void Script_BeatAaron(void)
{
	uint8_t value = gb_read8(wMultichoiceTextboxResult_ChooseDeckToDuelAgainst_ADDR);
	uint16_t event_addr = (uint16_t)(wEventVars_ADDR + EVENT_AARON_BOOSTER_REWARD_OFFSET);
	uint8_t event = gb_read8(event_addr);

	gb_write8(wLoadedEventBits_ADDR, EVENT_AARON_BOOSTER_REWARD_MASK);
	gb_write8(event_addr, (uint8_t)((event & (uint8_t)~EVENT_AARON_BOOSTER_REWARD_MASK) |
			(value & EVENT_AARON_BOOSTER_REWARD_MASK)));
}
