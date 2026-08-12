#include "home/write_number.h"

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/empty_screen.h"
#include "mem.h"

/* TwoByteNumberToText.get_digit:: poketcg/src/home/write_number.asm:144-158 */
static void get_digit(uint16_t *hl, uint16_t bc, uint16_t *de)
{
	uint8_t digit = (uint8_t)('0' - 1);
	uint16_t h = *hl;
	uint32_t sum;

	do {
		digit++;
		sum = (uint32_t)h + bc;
		h = (uint16_t)sum;
	} while (sum > 0xFFFF); /* carry out of `add hl, bc`, i.e. the subtraction stayed non-negative */

	gb_write8(*de, digit);
	*de = (uint16_t)(*de + 1);
	*hl = (uint16_t)(h - bc); /* undo the final overshooting add */
}

/* TwoByteNumberToText:: poketcg/src/home/write_number.asm:128-143 */
void TwoByteNumberToText(uint16_t hl, uint16_t *de)
{
	static const uint16_t place[5] = {
		(uint16_t)-10000, (uint16_t)-1000, (uint16_t)-100, (uint16_t)-10, (uint16_t)-1,
	};

	for (int i = 0; i < 5; i++)
		get_digit(&hl, place[i], de);

	gb_write8(*de, 0x00); /* TX_END, written without an inc de: six bytes out, de advanced by five */
}

/* WriteBCDDigitInTextFormat:: poketcg/src/home/write_number.asm:78-86 */
uint8_t WriteBCDDigitInTextFormat(uint8_t a, uint16_t *hl)
{
	uint8_t c = (uint8_t)((a & 0x0Fu) + '0');

	if (c > '9')
		c = (uint8_t)(c + 0x07u);
	gb_write8(*hl, c);
	*hl = (uint16_t)(*hl + 1u);
	return c;
}

/* WriteBCDNumberInTextFormat:: poketcg/src/home/write_number.asm:69-74 */
uint8_t WriteBCDNumberInTextFormat(uint8_t a, uint16_t *hl)
{
	uint8_t swapped = (uint8_t)((a << 4) | (a >> 4));

	WriteBCDDigitInTextFormat(swapped, hl);
	return WriteBCDDigitInTextFormat(a, hl);
}

/* WriteTwoDigitBCDNumber:: poketcg/src/home/write_number.asm:3-19 */
void WriteTwoDigitBCDNumber(uint8_t a, uint8_t b, uint8_t c)
{
	uint16_t src = wStringBuffer_ADDR;
	uint16_t dst;

	WriteBCDNumberInTextFormat(a, &src);
	dst = BCCoordToBGMap0Address(b, c);
	src = wStringBuffer_ADDR;
	SafeCopyDataHLtoDE(&src, &dst, 2u);
}

/* WriteFourDigitBCDNumber:: poketcg/src/home/write_number.asm:43-64 */
void WriteFourDigitBCDNumber(uint16_t hl, uint8_t b, uint8_t c)
{
	uint16_t src = wStringBuffer_ADDR;
	uint16_t dst;

	WriteBCDNumberInTextFormat((uint8_t)(hl >> 8), &src);
	WriteBCDNumberInTextFormat((uint8_t)hl, &src);
	dst = BCCoordToBGMap0Address(b, c);
	src = wStringBuffer_ADDR;
	SafeCopyDataHLtoDE(&src, &dst, 4u);
}
