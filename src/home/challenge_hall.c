#include "home/challenge_hall.h"

#include "generated/wram.h"
#include "mem.h"

ChallengeHallClearResult Func_f5db(void)
{
	gb_write8(wd698_ADDR + 0u, 0);
	gb_write8(wd698_ADDR + 1u, 0);
	gb_write8(wd698_ADDR + 2u, 0);
	gb_write8(wd698_ADDR + 3u, 0);
	return (ChallengeHallClearResult){0, 0x80u};
}

ChallengeHallBitResult Func_f5e9(uint8_t c)
{
	uint16_t hl = (uint16_t)(wd698_ADDR + (uint16_t)(c / 8u));
	uint8_t b = (uint8_t)(0x80u >> (c & 7u));
	return (ChallengeHallBitResult){b, hl};
}

void Script_Host(void)
{
}
