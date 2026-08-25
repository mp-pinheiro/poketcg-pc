#include "home/switch_rom.h"

#include "generated/hram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/switch_rom.h"
#include "generated/hram.h"
/* <<< factory statics */

/* BankswitchROM:: ldh [hBankROM], a / ld [rROMB], a / ret
 * rROMB is the MBC5 low bank latch; g_rom_bank stands in for it. */
void BankswitchROM(uint8_t bank)
{
	hBankROM = bank;
	mbc5_write(0x2000, bank);
}

/* >>> factory BankpushROM */
BankpushROMResult BankpushROM(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)f;
	uint8_t bank_offset = (uint8_t)((hl >> 14) & 3u);
	uint8_t bank = (uint8_t)(a + bank_offset);
	uint16_t sum = (uint16_t)a + bank_offset;
	uint8_t out_a = (uint8_t)sum;
	uint8_t out_f = (uint8_t)((out_a == 0u ? 0x80u : 0u)
		| ((((uint8_t)(a & 0x0Fu) + bank_offset) > 0x0Fu) ? 0x20u : 0u)
		| ((sum > 0xFFu) ? 0x10u : 0u));
	uint16_t out_hl = (uint16_t)((hl & 0x3FFFu) | 0x4000u);
	BankswitchROM(bank);
	return (BankpushROMResult){out_a, out_f, b, c, d, e, out_hl};
}
/* <<< factory BankpushROM */

/* >>> factory BankpushROM2 */
BankpushROM2Result BankpushROM2(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	BankswitchROM(a);
	return (BankpushROM2Result){a, f, b, c, d, e, hl};
}
/* <<< factory BankpushROM2 */
