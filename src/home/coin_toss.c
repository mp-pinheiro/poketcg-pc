#include "home/coin_toss.h"
/* >>> factory statics */
#include "home/core.h"
#include "generated/wram.h"
/* <<< factory statics */

static uint8_t cp_flags(uint8_t a, uint8_t n)
{
	return (uint8_t)(0x40u
		| ((a == n) ? 0x80u : 0u)
		| (((a & 0x0Fu) < (n & 0x0Fu)) ? 0x20u : 0u)
		| ((a < n) ? 0x10u : 0u));
}

/* coin_toss.asm:32-39. Returns the exit F register from the deciding cp. */
uint8_t CompareDEtoBC(uint8_t d, uint8_t e, uint8_t b, uint8_t c)
{
	if (d != b)
		return cp_flags(d, b);
	return cp_flags(e, c);
}

/* >>> factory TossCoinATimes */
TossCoinATimesResult TossCoinATimes(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	wCoinTossScreenTextID = e;
	gb_write8((uint16_t)(wCoinTossScreenTextID_ADDR + 1u), d);
	TossCoinResult result = _TossCoin(a);
	return (TossCoinATimesResult){result.a, result.f, hl};
}
/* <<< factory TossCoinATimes */
