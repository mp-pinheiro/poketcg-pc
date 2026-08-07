#include "home/objects.h"

#include "generated/wram.h"
#include "mem.h"

#define OAM_COUNT 40u
#define OAM_SIZE  (OAM_COUNT * 4u)

void SetOneObjectAttributes(uint8_t e, uint8_t d, uint8_t c, uint8_t b)
{
	uint8_t off = wOAMOffset;
	if (off >= OAM_SIZE)
		return;
	uint16_t p = (uint16_t)(wOAM_ADDR + off);
	gb_write8(p++, e);
	gb_write8(p++, d);
	gb_write8(p++, c);
	gb_write8(p, b);
	wOAMOffset = (uint8_t)(off + 4u);
}

/* objects.asm:72-85. Zeroes only Y/X (bytes 0,1); tile and attrs survive. */
void ZeroObjectPositions(void)
{
	wOAMOffset = 0;
	for (uint8_t i = 0; i < OAM_COUNT; i++) {
		uint16_t p = (uint16_t)(wOAM_ADDR + (uint16_t)i * 4u);
		gb_write8(p, 0);
		gb_write8((uint16_t)(p + 1u), 0);
	}
}
