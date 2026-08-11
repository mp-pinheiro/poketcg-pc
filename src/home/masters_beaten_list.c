#include "home/masters_beaten_list.h"

#include "generated/wram.h"
#include "mem.h"

#define MASTERS_BEATEN_LIST_SIZE 0x0Au

/* engine/masters_beaten_list.asm:1-15. */
MasterBeatenListResult ClearMasterBeatenList(void)
{
	for (uint8_t i = 0; i < MASTERS_BEATEN_LIST_SIZE; i++)
		gb_write8((uint16_t)(wMastersBeatenList_ADDR + i), 0);
	return (MasterBeatenListResult){0, 0xC0u};
}

/* engine/masters_beaten_list.asm:17-43. */
MasterBeatenListResult AddMasterBeatenToList(uint8_t a)
{
	for (uint8_t i = 0; i < MASTERS_BEATEN_LIST_SIZE; i++) {
		uint8_t entry = gb_read8((uint16_t)(wMastersBeatenList_ADDR + i));
		if (entry == 0) {
			gb_write8((uint16_t)(wMastersBeatenList_ADDR + i), a);
			return (MasterBeatenListResult){a, 0x80u};
		}
		if (entry == a)
			return (MasterBeatenListResult){entry, 0xC0u};
	}
	return (MasterBeatenListResult){gb_read8((uint16_t)(wMastersBeatenList_ADDR + 9u)), 0xC0u};
}
