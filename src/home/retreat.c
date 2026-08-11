#include "home/retreat.h"

#include "generated/wram.h"
#include "mem.h"

#define POKEMON_POWER 0x04u
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))

static uint8_t flag_cp(uint8_t a, uint8_t value)
{
	uint8_t f = 0x40u;
	if (a == value)
		f |= 0x80u;
	if ((a & 0x0fu) < (value & 0x0fu))
		f |= 0x20u;
	if (a < value)
		f |= 0x10u;
	return f;
}

SetAIRetreatFlagsResult SetAIRetreatFlags(void)
{
	gb_write8(wAIRetreatFlags_ADDR, 0);
	uint8_t turn = gb_read8(wWhoseTurn_ADDR);
	if (turn == OPPONENT_TURN) {
		uint8_t tried = gb_read8(wAITriedAttack_ADDR);
		uint8_t f = tried ? 0x00u : 0x80u;
		if (tried)
			return (SetAIRetreatFlagsResult){tried, f};
		gb_write8(wAIRetreatFlags_ADDR, 0x80u);
		return (SetAIRetreatFlagsResult){0x80u, f};
	}

	uint8_t category = gb_read8(wLoadedAttackCategory_ADDR);
	uint8_t f = flag_cp(category, POKEMON_POWER);
	if (category == POKEMON_POWER)
		return (SetAIRetreatFlagsResult){category, f};
	gb_write8(wAIRetreatFlags_ADDR, 0x80u);
	return (SetAIRetreatFlagsResult){0x80u, f};
}
