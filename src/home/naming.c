#include "home/naming.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
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

#define NAME_BUFFER_LENGTH 0x10u
#define TX_END 0x00u

/* poketcg.sym: 04:68a9 DisplayPlayerNamingScreen, 04:68eb
 * DisplayPlayerNamingScreen.default_name. The routine shares bank 4 with its
 * data; the NAME_BUFFER_LENGTH copy runs past the 12-byte "MARK" fixed-width
 * label into the first four bytes of Unknown_128f7. */
#define NAMING_BANK 0x04u
#define DEFAULT_PLAYER_NAME 0x68EBu
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
	if (hl == DEFAULT_PLAYER_NAME) {
		/* rom_ptr, not the bus: the ROM executes this copy with bank
		 * NAMING_BANK mapped (FarCall restored it after InputPlayerName),
		 * while the native bank latch holds whatever the naming screen's
		 * ported callees last wrote, so the window address alone does not
		 * name these bytes on both sides. */
		const uint8_t *name = rom_ptr(NAMING_BANK, DEFAULT_PLAYER_NAME);
		for (uint8_t i = 0u; i < NAME_BUFFER_LENGTH; i++)
			gb_write8((uint16_t)(sPlayerName_ADDR + i), name[i]);
	} else {
		CopyDataHLtoDE_SaveRegisters(hl, sPlayerName_ADDR, NAME_BUFFER_LENGTH);
	}
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
