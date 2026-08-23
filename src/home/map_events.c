#include "home/map_events.h"

#include <stdint.h>

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define TRUE 0x01u
#define CONSOLE_CGB 0x02u

static const uint8_t kSetOWMapEventTilemapPointers[44] = {
	0x16u, 0x00u, 0x34u, 0x35u, /* PokemonDomeDoor */
	0x0eu, 0x00u, 0x38u, 0x39u, /* HallOfHonorDoor */
	0x06u, 0x02u, 0x08u, 0x09u, /* FightingDeckMachine */
	0x0au, 0x02u, 0x08u, 0x09u, /* RockDeckMachine */
	0x0eu, 0x02u, 0x08u, 0x09u, /* WaterDeckMachine */
	0x12u, 0x02u, 0x08u, 0x09u, /* LightningDeckMachine */
	0x0eu, 0x0au, 0x08u, 0x09u, /* GrassDeckMachine */
	0x12u, 0x0au, 0x08u, 0x09u, /* PsychicDeckMachine */
	0x0eu, 0x12u, 0x08u, 0x09u, /* ScienceDeckMachine */
	0x12u, 0x12u, 0x08u, 0x09u, /* FireDeckMachine */
	0x0au, 0x00u, 0x04u, 0x05u, /* ChallengeMachine */
};
/* <<< factory statics */

#define NUM_MAP_EVENTS 11u

void ClearOWMapEvents(void)
{
	uint16_t address = wOWMapEvents_ADDR;

	for (uint8_t i = 0; i < NUM_MAP_EVENTS; i++) {
		gb_write8(address, 0);
		address++;
	}
}

/* >>> factory SetOWMapEvent_SRAMOrVRAM */
uint8_t SetOWMapEvent_SRAMOrVRAM(uint8_t a)
{
	/* rebuild after map_events.h stdint.h fix */
	uint8_t event_index = a;
	uint8_t saved_tilemap = wCurTilemap;
	uint8_t saved_bank = wBGMapBank;
	uint8_t saved_width = wBGMapWidth;
	uint8_t saved_height = wBGMapHeight;
	uint8_t saved_ptr_lo = gb_read8(wBGMapPermissionDataPtr_ADDR);
	uint8_t saved_ptr_hi = gb_read8((uint16_t)(wBGMapPermissionDataPtr_ADDR + 1u));

	gb_write8((uint16_t)(wOWMapEvents_ADDR + event_index), TRUE);

	uint8_t idx4 = (uint8_t)(event_index * 4u);
	uint8_t x = kSetOWMapEventTilemapPointers[idx4];
	uint8_t y = kSetOWMapEventTilemapPointers[(uint8_t)(idx4 + 1u)];
	uint8_t tilemap = (wConsole == CONSOLE_CGB)
		? kSetOWMapEventTilemapPointers[(uint8_t)(idx4 + 3u)]
		: kSetOWMapEventTilemapPointers[(uint8_t)(idx4 + 2u)];
	wCurTilemap = tilemap;

	LoadTilemap(x, y);

	uint8_t bx = (uint8_t)(x >> 1);
	uint8_t rrca_y = (uint8_t)((y >> 1) | ((y & 1u) << 7));
	uint8_t masked = (uint8_t)(rrca_y & 0x0Fu);
	uint8_t swapped = (uint8_t)(masked << 4);
	uint8_t offset = (uint8_t)(swapped + bx);
	DecompressPermissionMap((uint16_t)(wPermissionMap_ADDR + offset));

	gb_write8((uint16_t)(wBGMapPermissionDataPtr_ADDR + 1u), saved_ptr_hi);
	gb_write8(wBGMapPermissionDataPtr_ADDR, saved_ptr_lo);
	wBGMapHeight = saved_height;
	wBGMapWidth = saved_width;
	wBGMapBank = saved_bank;
	wCurTilemap = saved_tilemap;
	return saved_tilemap;
}
/* <<< factory SetOWMapEvent_SRAMOrVRAM */

/* >>> factory ApplyOWMapEventChangeIfEventSet */
void ApplyOWMapEventChangeIfEventSet(uint8_t a)
{
	uint8_t event_index = a;
	gb_write8(wWriteBGMapToSRAM_ADDR, TRUE);
	if (gb_read8((uint16_t)(wOWMapEvents_ADDR + event_index)) != 0u)
		SetOWMapEvent_SRAMOrVRAM(event_index);
}
/* <<< factory ApplyOWMapEventChangeIfEventSet */

/* >>> factory SetOWMapEvent */
uint8_t SetOWMapEvent(uint8_t a)
{
	gb_write8(wWriteBGMapToSRAM_ADDR, 0u);
	return SetOWMapEvent_SRAMOrVRAM(a);
}
/* <<< factory SetOWMapEvent */
