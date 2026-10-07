#include "home/math.h"

/* poketcg/src/home/math.asm:1-10 — every `add` is 8-bit, so the product is
 * a * 10 mod 256: ATimes10(26) is 4, not 260. Callers rely on the truncation. */
uint8_t ATimes10(uint8_t a)
{
	uint8_t e = a;

	a = (uint8_t)(a + a);
	a = (uint8_t)(a + a);
	a = (uint8_t)(a + e);
	a = (uint8_t)(a + a);
	return a;
}
