#include "home/switch_sram.h"

#include "generated/hram.h"
#include "mem.h"

/* rRAMB and rRAMG are set directly rather than through gb_write8, as BankswitchROM sets
 * g_rom_bank: writes below $8000 stay inert on the bus, so a routine that sweeps the whole
 * address space cannot silently re-bank the cart. */
void BankswitchSRAM(uint8_t bank)
{
	hBankSRAM = bank;
	g_sram_bank = bank;
	g_sram_enabled = 1;
}

void DisableSRAM(void)
{
	g_sram_enabled = 0;
}
