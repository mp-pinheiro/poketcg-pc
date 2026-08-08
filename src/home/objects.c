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

/* objects.asm:1-42. n==0 means 256 (post-test loop). Exit hl is always
 * &wOAMOffset regardless of path. */
SetManyObjResult SetManyObjectsAttributes(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t off = wOAMOffset;
	if (off >= OAM_SIZE)
		return (SetManyObjResult){wOAMOffset_ADDR, 1};

	uint32_t n = gb_read8(hl++);
	n = n ? n : 0x100u;
	uint16_t oam = (uint16_t)(wOAM_ADDR + off);
	uint8_t carry = 0;
	for (uint32_t i = 0; i < n; i++) {
		gb_write8(oam++, (uint8_t)(gb_read8(hl++) + e));
		gb_write8(oam++, (uint8_t)(gb_read8(hl++) + d));
		gb_write8(oam++, gb_read8(hl++));
		gb_write8(oam++, gb_read8(hl++));
		if ((uint8_t)(oam - wOAM_ADDR) >= OAM_SIZE) {
			carry = 1;
			break;
		}
	}
	wOAMOffset = (uint8_t)(oam - wOAM_ADDR);
	return (SetManyObjResult){wOAMOffset_ADDR, carry};
}
