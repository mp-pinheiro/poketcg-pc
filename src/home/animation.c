#include "home/animation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/map.h"
#include "home/switch_rom.h"
#include "mem.h"
/* >>> factory statics */
#include "home/animation.h"
#include "generated/wram.h"
#define NUM_OW_FRAMESET_SUBGROUPS 0x03u

#include "home/animation.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */
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
 

/* >>> factory LoadOWFrameTiles */
void LoadOWFrameTiles(void)
{
	uint8_t duration = wCurOWFrameDuration;
	if (duration != 0u) {
		wCurOWFrameDuration = (uint8_t)(duration - 1u);
		return;
	}

	uint16_t frame_base = (uint16_t)(wCurMapOWFrameset |
		((uint16_t)gb_read8((uint16_t)(wCurMapOWFrameset_ADDR + 1u)) << 8));
	uint8_t offset = wCurOWFrameDataOffset;
	uint16_t frame = (uint16_t)(frame_base + offset);
	wCurOWFrameDuration = gb_read8(frame);

	for (;;) {
		uint16_t tile = (uint16_t)(frame + 1u);
		uint8_t vram_tile = (uint8_t)(gb_read8(tile) ^ 0x80u);
		uint8_t vram_bank = gb_read8((uint16_t)(tile + 1u));
		uint16_t destination = (uint16_t)(0x8800u + ((uint16_t)vram_tile << 4));
		uint8_t saved_vram_bank = hBankVRAM;
		hBankVRAM = (uint8_t)(vram_bank & 1u);
		gb_write8(0xff4fu, (uint8_t)(0xfeu | hBankVRAM));

		uint16_t descriptor = (uint16_t)(tile + 2u);
		uint8_t tileset_bank = (uint8_t)(gb_read8(descriptor) + 20u);
		uint16_t tileset = (uint16_t)(gb_read8((uint16_t)(descriptor + 1u)) |
			((uint16_t)gb_read8((uint16_t)(descriptor + 2u)) << 8));
		uint16_t tile_offset = (uint16_t)(gb_read8((uint16_t)(descriptor + 3u)) |
			((uint16_t)gb_read8((uint16_t)(descriptor + 4u)) << 8));
		uint16_t source = (uint16_t)(tileset + (tile_offset << 4));
		wTempPointerBank = tileset_bank;
		CopyGfxDataFromTempBank(&source, &destination, 1u, 16u);

		hBankVRAM = saved_vram_bank;
		gb_write8(0xff4fu, (uint8_t)(0xfeu | (saved_vram_bank & 1u)));
		frame = (uint16_t)(frame + 8u);
		offset = (uint8_t)(offset + 8u);
		uint8_t next_duration = gb_read8(frame);
		if (next_duration != 0u) {
			wCurOWFrameDataOffset = offset;
			if (next_duration == 0xffu) {
				uint8_t saved_duration = wCurOWFrameDuration;
				uint16_t subgroup = (uint16_t)(wCurMapOWFrameset |
					((uint16_t)gb_read8((uint16_t)(wCurMapOWFrameset_ADDR + 1u)) << 8));
				GetOWFramesetSubgroupData(subgroup, 0u);
				wCurOWFrameDuration = saved_duration;
			}
			return;
		}
	}
}
/* <<< factory LoadOWFrameTiles */

/* >>> factory-mutation LoadOWFrameTiles */
/* <<< factory-mutation LoadOWFrameTiles */

/* >>> factory DoLoadedFramesetSubgroupsFrame */
void DoLoadedFramesetSubgroupsFrame(void)
{
	if (wNumLoadedFramesetSubgroups == 0u)
		return;

	uint8_t c = 0u;
	while (c < NUM_OW_FRAMESET_SUBGROUPS) {
		if (LoadOWFramesetSubgroup(c) != 0xffu) {
			LoadOWFrameTiles();
			StoreOWFramesetSubgroup(c);
		}
		c++;
	}
}
/* <<< factory DoLoadedFramesetSubgroupsFrame */

/* >>> factory ProcessOWFrameset */
void ProcessOWFrameset(uint16_t hl)
{
	gb_write8(wCurMapOWFrameset_ADDR, (uint8_t)hl);
	gb_write8((uint16_t)(wCurMapOWFrameset_ADDR + 1u), (uint8_t)(hl >> 8));
	wNumLoadedFramesetSubgroups = 0u;
	ClearOWFramesetSubgroups();
	for (uint8_t c = 0u; c < NUM_OW_FRAMESET_SUBGROUPS; c++) {
		(void)LoadOWFramesetSubgroup(c);
		GetOWFramesetSubgroupData(hl, c);
		if (gb_read8(wCurOWFrameDataOffset_ADDR) == 0xFFu) {
			continue;
		}
		wNumLoadedFramesetSubgroups = (uint8_t)(wNumLoadedFramesetSubgroups + 1u);
		LoadOWFrameTiles();
		StoreOWFramesetSubgroup(c);
	}
}
/* <<< factory ProcessOWFrameset */
