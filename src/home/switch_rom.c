#include "home/switch_rom.h"

#include "generated/hram.h"
#include "mem.h"

/* BankswitchROM:: ldh [hBankROM], a / ld [rROMB], a / ret
 * rROMB is the MBC5 low bank latch; g_rom_bank stands in for it. */
void BankswitchROM(uint8_t bank)
{
	hBankROM = bank;
	mbc5_write(0x2000, bank);
}
