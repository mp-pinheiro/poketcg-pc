#include "home/coin_toss.h"

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
