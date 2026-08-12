#include "home/masters_beaten_list.h"

#include "generated/wram.h"
#include "mem.h"

#define MASTERS_BEATEN_COUNT 10u

uint8_t ClearMasterBeatenList(uint8_t *f)
{
	uint16_t address = wMastersBeatenList_ADDR;
	for (uint8_t count = MASTERS_BEATEN_COUNT; count != 0; --count) {
		gb_write8(address, 0);
		address = (uint16_t)(address + 1u);
	}
	*f = 0xC0u;
	return 0;
}

uint8_t AddMasterBeatenToList(uint8_t a, uint8_t *f)
{
	uint8_t master = a;
	uint16_t address = wMastersBeatenList_ADDR;
	uint8_t count = MASTERS_BEATEN_COUNT;

	while (count != 0) {
		a = gb_read8(address);
		if (a == 0) {
			gb_write8(address, master);
			*f = 0x80u;
			return master;
		}

		uint8_t flags = 0x40u;
		if ((a & 0x0Fu) < (master & 0x0Fu))
			flags |= 0x20u;
		if (a < master)
			flags |= 0x10u;
		if (a == master)
			flags |= 0x80u;
		if (a == master) {
			*f = flags;
			return a;
		}

		address = (uint16_t)(address + 1u);
		--count;
		if (count == 0) {
			*f = (uint8_t)(flags | 0x80u);
			return a;
		}
	}

	*f = 0x80u;
	return a;
}

/* >>> factory AddAllMastersToMastersBeatenList */
/* masters_beaten_list.asm:46-55 */
uint8_t AddAllMastersToMastersBeatenList(uint8_t *f)
{
	uint8_t master_id;
	for (master_id = 1u; master_id <= MASTERS_BEATEN_COUNT; ++master_id) {
		uint8_t discard_f;
		AddMasterBeatenToList(master_id, &discard_f);
	}
	*f = 0xC0u;
	return master_id;
}
/* <<< factory AddAllMastersToMastersBeatenList */
