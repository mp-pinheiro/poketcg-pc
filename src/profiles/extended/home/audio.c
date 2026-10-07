/* >>> part includes */
#include "home/audio.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"
/* <<< part includes */

/* >>> factory GetAudioCmdAndArgs */
/* audio.asm:3-26 */
uint8_t GetAudioCmdAndArgs(uint8_t bank, uint16_t hl)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(bank);
	uint8_t command = gb_read8(hl);
	uint8_t arg0 = gb_read8((uint16_t)(hl + 1u));
	uint8_t arg1 = gb_read8((uint16_t)(hl + 2u));
	gb_write8(wAudioCmd_ADDR, command);
	gb_write8(wAudioArg_ADDR, arg0);
	gb_write8((uint16_t)(wAudioArg_ADDR + 1u), arg1);
	BankswitchROM(saved_bank);
	return command;
}
/* <<< factory GetAudioCmdAndArgs */
