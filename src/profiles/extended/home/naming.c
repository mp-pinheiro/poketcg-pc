/* >>> part includes */
#include "home/naming.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/copy.h"
#include "home/input_name.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/memory.h"
#include "home/overworld.h"
#include "home/random.h"
#include "home/switch_sram.h"
#include "generated/sram.h"


#define DEFAULT_PLAYER_NAME (DisplayPlayerNamingScreen__default_name_ADDR)
/* <<< factory statics */

/* >>> factory DisplayPlayerNamingScreen */
/* naming.asm:1-40 (poketcg.sym 04:68a9, 66 bytes of code). Clears the name
 * buffer, hands it to InputPlayerName, and copies either the typed name or
 * the .default_name table into sPlayerName followed by two RNG checksum
 * bytes at +$0e/+$0f. */
DisplayPlayerNamingScreenResult DisplayPlayerNamingScreen(void)
{
	FillMemoryWithA(wNameBuffer_ADDR, NAME_BUFFER_LENGTH, TX_END);
	(void)InputPlayerName(wNameBuffer_ADDR);
	WhiteOutDMGPals();
	DoFrameIfLCDEnabled();
	DisableLCD();
	uint16_t hl = wNameBuffer_ADDR;
	if (gb_read8(hl) == 0u)
		hl = DEFAULT_PLAYER_NAME;
	EnableSRAM();
	CopyDataHLtoDE_SaveRegisters(hl, sPlayerName_ADDR, NAME_BUFFER_LENGTH);
	uint8_t a = UpdateRNGSources();
	gb_write8((uint16_t)(sPlayerName_ADDR + 0x0Eu), a);
	uint8_t counter = wRNGCounter;
	a = UpdateRNGSources();
	gb_write8((uint16_t)(sPlayerName_ADDR + 0x0Fu), a);
	DisableSRAM();
	/* Exit flags are the second call's `inc [hl]` on wRNGCounter: N is
	 * cleared by inc and C still holds the xor's 0, so only Z and H remain. */
	uint8_t f = 0u;
	if (counter == 0xFFu)
		f |= 0x80u; /* Z: the incremented counter wrapped to 0 */
	if ((counter & 0x0Fu) == 0x0Fu)
		f |= 0x20u; /* H: carry out of the low nibble */
	return (DisplayPlayerNamingScreenResult){a, f, 0x00u, 0x10u, 0xA0u, 0x10u, hl};
}
/* <<< factory DisplayPlayerNamingScreen */
