/* >>> part includes */
#include "home/switch_sram.h"

#include "generated/hram.h"
#include "mem.h"
/* <<< part includes */

/* >>> factory BankswitchSRAM */
void BankswitchSRAM(uint8_t bank)
{
	hBankSRAM = bank;
	mbc5_write(0x4000, bank);
	mbc5_write(0x0000, 0x0A);
}
/* <<< factory BankswitchSRAM */

/* >>> part DisableSRAM */
void DisableSRAM(void)
{
	mbc5_write(0x0000, 0x00);
}
/* <<< part DisableSRAM */

/* >>> part EnableSRAM */
/* EnableSRAM:: push af / ld a, RAMG_SRAM_ENABLE / ld [rRAMG], a / pop af / ret */
void EnableSRAM(void)
{
	mbc5_write(0x0000, 0x0A);
}
/* <<< part EnableSRAM */
