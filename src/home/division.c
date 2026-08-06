#include "home/division.h"

/* Restoring division hand-ported from poketcg/src/home/division.asm.
 *
 * Divisor 0 yields quotient $FFFF and remainder = dividend. Bug-compatible with
 * the asm on purpose; callers rely on nothing else.
 *
 * Exit carry equals entry carry, so carry is not an output: bc is rotated 17
 * times in total and no iteration consumes the bit rotated in before the loop.
 *
 * The asm holds its loop counter in `hffb6`; nothing in poketcg reads that byte,
 * so $FFB6 is deliberately left untouched.
 *
 * Dropping the bit shifted out of hl is safe, not lossy: after iteration i the
 * remainder is below 2^i, so it never exceeds $7FFF before the last shift.
 */
DivResult DivideBCbyDE(uint16_t bc, uint16_t de)
{
	const uint8_t d = (uint8_t)(de >> 8), e = (uint8_t)de;
	uint16_t hl = 0;
	int cf, out;

	cf = bc >> 15;
	bc = (uint16_t)(bc << 1);

	for (int i = 0; i < 16; i++) {
		uint8_t l, h, a;
		int borrow;

		hl = (uint16_t)(hl << 1 | cf);

		l = (uint8_t)(hl - e);
		borrow = (uint8_t)hl < e;
		h = (uint8_t)(hl >> 8);
		a = (uint8_t)(h - d - borrow);
		borrow = h < d + borrow;

		cf = !borrow;
		if (cf)
			hl = (uint16_t)(a << 8 | l);

		out = bc >> 15;
		bc = (uint16_t)(bc << 1 | cf);
		cf = out;
	}

	return (DivResult){ .quotient = bc, .remainder = hl };
}
