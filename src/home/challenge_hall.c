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

/* >>> factory Func_f5cc */
/* challenge_hall.asm:517-523 */
ChallengeHallTestBitResult Func_f5cc(uint8_t c)
{
	ChallengeHallBitResult bit = Func_f5e9(c);
	uint8_t a = (uint8_t)(gb_read8(bit.hl) & bit.b);
	uint8_t f = a ? 0x10u : 0xA0u;
	return (ChallengeHallTestBitResult){a, f};
}
/* <<< factory Func_f5cc */

/* >>> factory Func_f5d4 */
/* challenge_hall.asm:525-530 */
ChallengeHallSetBitResult Func_f5d4(uint8_t c)
{
	ChallengeHallBitResult bit = Func_f5e9(c);
	uint8_t a = (uint8_t)(gb_read8(bit.hl) | bit.b);
	gb_write8(bit.hl, a);
	uint8_t f = a ? 0x00u : 0x80u;
	return (ChallengeHallSetBitResult){a, f};
}
/* <<< factory Func_f5d4 */
