#include "home/clear_sram.h"

#include "home/switch_sram.h"
#include "mem.h"

/* clear_sram.asm:60-74 */
ClearSRAMResult ClearSRAMBank(uint8_t bank, uint8_t f)
{
	BankswitchSRAM(bank);
	EnableSRAM();
	for (uint16_t i = 0; i < 0x2000u; i++)
		gb_write8((uint16_t)(0xA000u + i), 0);
	return (ClearSRAMResult){bank, f, 0, 0, 0xC000u};
}

/* clear_sram.asm:44-57. Clears banks 3,2,1,0 then stamps the signature into bank 0,
 * which the loop's final ClearSRAMBank(0) left selected. */
ClearSRAMResult RestartSRAM(void)
{
	for (uint8_t bank = 3u; bank != 0xFFu; bank--)
		(void)ClearSRAMBank(bank, 0);
	gb_write8(0xA000u, 0x04);
	gb_write8(0xA001u, 0x21);
	gb_write8(0xA002u, 0x05);
	return (ClearSRAMResult){0xFFu, 0xC0u, 0, 0, 0xA002u};
}
