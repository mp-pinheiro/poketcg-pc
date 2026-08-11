#include "home/animation.h"

#include "generated/wram.h"
#include "mem.h"

#define NUM_OW_FRAMESET_SUBGROUPS 3u

void ClearNumLoadedFramesetSubgroups(void)
{
	wNumLoadedFramesetSubgroups = 0;
}

void ClearOWFramesetSubgroups(void)
{
	for (uint8_t i = 0; i < NUM_OW_FRAMESET_SUBGROUPS * 2u; i++)
		gb_write8((uint16_t)(wOWFramesetSubgroups_ADDR + i), 0xff);
}

void GetOWFramesetSubgroupData(uint16_t hl, uint8_t c)
{
	uint8_t offset = gb_read8((uint16_t)(hl + c));
	uint8_t frame = gb_read8((uint16_t)(hl + offset));
	if (frame != 0xff) {
		wCurOWFrameDataOffset = offset;
		wCurOWFrameDuration = 0;
	}
}

uint8_t LoadOWFramesetSubgroup(uint8_t c)
{
	uint16_t address = (uint16_t)(wOWFramesetSubgroups_ADDR + (uint16_t)c * 2u);
	wCurOWFrameDataOffset = gb_read8(address);
	wCurOWFrameDuration = gb_read8((uint16_t)(address + 1u));
	return wCurOWFrameDataOffset;
}

void StoreOWFramesetSubgroup(uint8_t c)
{
	uint16_t address = (uint16_t)(wOWFramesetSubgroups_ADDR + (uint16_t)c * 2u);
	gb_write8(address, wCurOWFrameDataOffset);
	gb_write8((uint16_t)(address + 1u), wCurOWFrameDuration);
}
