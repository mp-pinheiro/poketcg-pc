#include "home/decompress.h"

#include "generated/wram.h"
#include "mem.h"

static uint16_t source_pos(void)
{
	return (uint16_t)(gb_read8(wDecompSourcePosPtr_ADDR + 1) << 8
			  | gb_read8(wDecompSourcePosPtr_ADDR));
}

static void set_source_pos(uint16_t pos)
{
	gb_write8(wDecompSourcePosPtr_ADDR, (uint8_t)pos);
	gb_write8(wDecompSourcePosPtr_ADDR + 1, (uint8_t)(pos >> 8));
}

/* decompress.asm:81-91. Both accesses keep b at wDecompSecondaryBufferPtrHigh, so only
 * the low bytes move: they wrap inside the $100-byte page instead of spilling into the
 * next one, and the read precedes the write when the two low bytes are equal. */
static uint8_t repeat_byte(void)
{
	uint8_t page = wDecompSecondaryBufferPtrHigh;
	uint8_t from = wDecompRepeatSeqOffset;

	wDecompRepeatSeqOffset = (uint8_t)(from + 1);

	uint8_t a = gb_read8((uint16_t)(page << 8 | from));
	uint8_t to = wDecompSecondaryBufferPtrLow;

	wDecompSecondaryBufferPtrLow = (uint8_t)(to + 1);
	gb_write8((uint16_t)(page << 8 | to), a);
	return a;
}

/* decompress.asm:5-31 */
void InitDataDecompression(uint16_t de, uint8_t b)
{
	set_source_pos(de);
	wDecompNumCommandBitsLeft = 1; /* the first .Decompress decrements this to 0, which
					* is what pulls the first command byte */
	wDecompCommandByte = 0;
	wDecompRepeatModeToggle = 0;
	wDecompRepeatLengths = 0;
	wDecompNumBytesToRepeat = 0;
	wDecompSecondaryBufferPtrHigh = b;
	wDecompRepeatSeqOffset = 0;
	wDecompSecondaryBufferPtrLow = (uint8_t)wDecompressionSecondaryBufferStart_ADDR;

	for (unsigned low = 0; low < 0x100; low++)
		gb_write8((uint16_t)(b << 8 | low), 0);
}

/* decompress.asm:39-54. Nothing is reset here: the state is the caller's, carried
 * across calls. bc and a end at 0 as loop residue, not as outputs. */
void DecompressData(uint16_t bc, uint16_t de)
{
	uint32_t n = bc ? bc : 0x10000;

	do {
		gb_write8(de, DecompressData_Decompress());
		de = (uint16_t)(de + 1);
	} while (--n);
}

/* decompress.asm:72-159. A repeat command emits nybble + 2 bytes in total: one here,
 * plus the nybble + 1 that wDecompNumBytesToRepeat owes later calls. */
uint8_t DecompressData_Decompress(void)
{
	if (wDecompNumBytesToRepeat != 0) {
		wDecompNumBytesToRepeat--;
		return repeat_byte();
	}

	uint16_t src = source_pos();

	wDecompNumCommandBitsLeft--;
	if (wDecompNumCommandBitsLeft == 0) {
		wDecompNumCommandBitsLeft = 8;
		wDecompCommandByte = gb_read8(src);
		src = (uint16_t)(src + 1);
	}

	/* `rl [hl]` runs with carry clear (the `or a` above cleared it), so the command
	 * bits are consumed MSB first with 0 shifted in behind them. */
	uint8_t command = wDecompCommandByte;

	wDecompCommandByte = (uint8_t)(command << 1);

	uint8_t a = gb_read8(src);

	src = (uint16_t)(src + 1);

	if (command & 0x80) {
		set_source_pos(src);

		uint8_t page = wDecompSecondaryBufferPtrHigh;
		uint8_t to = wDecompSecondaryBufferPtrLow;

		wDecompSecondaryBufferPtrLow = (uint8_t)(to + 1);
		gb_write8((uint16_t)(page << 8 | to), a);
		return a;
	}

	wDecompRepeatSeqOffset = a;

	uint8_t lengths;

	if (wDecompRepeatModeToggle & 1) {
		wDecompRepeatModeToggle &= (uint8_t)~1u;
		lengths = wDecompRepeatLengths; /* reuses the byte the previous repeat read */
	} else {
		wDecompRepeatModeToggle |= 1;
		lengths = gb_read8(src);
		src = (uint16_t)(src + 1);
		wDecompRepeatLengths = lengths;
		lengths = (uint8_t)(lengths >> 4 | lengths << 4); /* swap a */
	}
	wDecompNumBytesToRepeat = (uint8_t)((lengths & 0xF) + 1);
	set_source_pos(src);
	return repeat_byte();
}
