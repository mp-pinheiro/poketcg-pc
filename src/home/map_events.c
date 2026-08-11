#include "home/map_events.h"

#include <stdint.h>

#include "generated/wram.h"
#include "mem.h"

#define NUM_MAP_EVENTS 11u

void ClearOWMapEvents(void)
{
	uint16_t address = wOWMapEvents_ADDR;

	for (uint8_t i = 0; i < NUM_MAP_EVENTS; i++) {
		gb_write8(address, 0);
		address++;
	}
}
