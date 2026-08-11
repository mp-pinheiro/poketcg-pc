#include "home/mason_laboratory.h"

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_collection.h"
#include "mem.h"

static uint8_t event_value(uint8_t event)
{
	uint16_t addr;
	uint8_t mask;
	uint8_t shift = 0;

	if (event == 0x22) {
		addr = (uint16_t)(wEventVars_ADDR + 6u);
		mask = 0x02;
	} else if (event == 0x3e) {
		addr = (uint16_t)(wEventVars_ADDR + 0x0du);
		mask = 0x0e;
	} else {
		return 0;
	}
	while ((mask & 1u) == 0) {
		mask >>= 1;
		shift++;
	}
	gb_write8(wLoadedEventBits_ADDR, mask);
	return (uint8_t)((gb_read8(addr) & mask) >> shift);
}

static void set_challenge_machine(void)
{
	gb_write8((uint16_t)(wOWMapEvents_ADDR + 0x0au), 1);
	gb_write8(wWriteBGMapToSRAM_ADDR, 0);
}

void Script_Tech1(void)
{
	static const uint8_t energies[] = { 1, 2, 3, 4, 5, 6 };
	uint8_t total = 0;

	for (uint8_t i = 0; i < sizeof energies; i++)
		total = (uint8_t)(total + GetCardCountInCollection(energies[i]).a);
	if (total >= 10)
		return;
	for (uint8_t i = 0; i < sizeof energies; i++)
		for (uint8_t j = 0; j < 10; j++)
			AddCardToCollection(energies[i]);
}
PreloadDrMasonResult Preload_DrMason(void)
{
	if (event_value(0x22) != 0)
		set_challenge_machine();
	uint8_t state = event_value(0x3e);
	if (state == 1) {
		gb_write8(wLoadNPCXPos_ADDR, 6);
		gb_write8(wLoadNPCYPos_ADDR, 0x0c);
	}
	return (PreloadDrMasonResult){ .a = state, .f = state == 1 ? 0xD0 : state == 0 ? 0x70 : 0x50 };
}
