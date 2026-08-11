#include "home/mail.h"
#include "generated/wram.h"
#include "mem.h"

#define NUM_PC_PACKS 15
#define PACK_UNOPENED 0x80

static const uint8_t pc_mail_coordinates[NUM_PC_PACKS][2] = {
	{1, 2}, {7, 2}, {13, 2},
	{1, 4}, {7, 4}, {13, 4},
	{1, 6}, {7, 6}, {13, 6},
	{1, 8}, {7, 8}, {13, 8},
	{1, 10}, {7, 10}, {13, 10},
};

PCPackCoordinates GePCPackSelectionCoordinates(void)
{
	uint8_t selection = gb_read8(wPCPackSelection_ADDR);
	return (PCPackCoordinates){
		pc_mail_coordinates[selection][0],
		pc_mail_coordinates[selection][1],
	};
}

void TryGivePCPack(uint8_t id)
{
	uint16_t slot = wPCPacks_ADDR;
	uint8_t count = NUM_PC_PACKS;

	do {
		if ((uint8_t)(gb_read8(slot) & 0x7f) == id)
			return;
		slot++;
	} while (--count);

	slot = wPCPacks_ADDR;
	count = NUM_PC_PACKS;
	do {
		if ((uint8_t)(gb_read8(slot) & 0x7f) == 0) {
			gb_write8(slot, (uint8_t)(id | PACK_UNOPENED));
			return;
		}
		slot++;
	} while (--count);
}
