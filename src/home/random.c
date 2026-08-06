#include "home/random.h"

#include "generated/wram.h"
#include "mem.h"

/* UpdateRNGSources:: poketcg/src/home/random.asm:34-66
 *
 *   ld a, d / rlca / rlca / xor e / rra   -> carry = bit0 of (rotl(r2,2) ^ r1)
 *                                          = bit6(r2) ^ bit0(r1)
 *   rl e  with e = ctr ^ r1               -> new wRNG1, carry = bit7(ctr ^ r1)
 *   rl d  with d = r2  ^ r1               -> new wRNG2
 *   inc [hl] on wRNGCounter happens after the pre-increment value is consumed.
 */
uint8_t UpdateRNGSources(void)
{
	uint8_t r1 = wRNG1;
	uint8_t r2 = wRNG2;
	uint8_t ctr = wRNGCounter;

	uint8_t feedback = (uint8_t)(((r2 >> 6) ^ r1) & 1);
	uint8_t new_r1 = (uint8_t)(((ctr ^ r1) << 1) | feedback);
	uint8_t new_r2 = (uint8_t)(((r2 ^ r1) << 1) | ((ctr ^ r1) >> 7));

	wRNGCounter = (uint8_t)(ctr + 1);
	wRNG2 = new_r2;
	wRNG1 = new_r1;
	return (uint8_t)(new_r2 ^ new_r1);
}

/* HtimesL:: poketcg/src/home/random.asm:2-20
 *
 * a = h (multiplier), de = l (multiplicand, shifted left each round), hl = 0.
 * Entry jumps straight to the `srl a` test, so the loop is:
 *
 *   srl a            ; carry = old bit0
 *   jr c, .asm_882   ; add hl, de  then fall through to the de shift
 *   jr nz, .asm_883  ; shift de only
 *   ret              ; carry clear and a == 0
 *
 * The carry branch does its `add hl, de` before re-testing a, so the final
 * partial product is still accumulated on the iteration where a reaches 0.
 * de is 16-bit so bits shifted out of d are lost; irrelevant for 8x8 since
 * l << 7 still fits in 15 bits. Exit a is always 0 — loop residue, not output.
 */
uint16_t HtimesL(uint16_t hl)
{
	uint8_t a = (uint8_t)(hl >> 8);
	uint16_t de = (uint8_t)hl;
	uint16_t acc = 0;

	for (;;) {
		uint8_t carry = (uint8_t)(a & 1);
		a = (uint8_t)(a >> 1);
		if (carry) {
			acc = (uint16_t)(acc + de);
		} else if (a == 0) {
			return acc;
		}
		de = (uint16_t)(de << 1);
	}
}

/* Random:: poketcg/src/home/random.asm:23-31
 *
 * h = a, l = UpdateRNGSources(), then the high byte of h * l — i.e. the RNG
 * byte scaled into [0, a). a == 0 yields 0. Preserves bc/de/hl.
 */
uint8_t Random(uint8_t a)
{
	uint8_t l = UpdateRNGSources();

	return (uint8_t)(HtimesL((uint16_t)(a << 8 | l)) >> 8);
}
