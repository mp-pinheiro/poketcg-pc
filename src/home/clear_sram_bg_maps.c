#include "home/clear_sram_bg_maps.h"

#include "generated/hram.h"
#include "home/memory.h"
#include "home/switch_sram.h"

/* sGfxBuffer0 is SRAM bank 1 at $A000 (poketcg.sym: 01:a000); it and sGfxBuffer1 span $800
 * bytes. BankswitchSRAM selects the bank, so FillMemoryWithA takes the plain $A000 address. */
void ClearSRAMBGMaps(void)
{
	uint8_t saved = hBankSRAM;
	BankswitchSRAM(0x01);
	FillMemoryWithA(0xA000u, 0x0800u, 0x00);
	BankswitchSRAM(saved);
	DisableSRAM();
}
