#include "home/clear_saved_duel.h"

#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"

/* engine/duel/core.asm:6183-6191. No bank switch: writes whichever SRAM bank is
 * currently selected. sCurrentDuelChecksum is 2 bytes; the second has no symbol. */
void ClearSavedDuel(void)
{
	EnableSRAM();
	gb_write8(sCurrentDuelValid_ADDR, 0x00);
	gb_write8(sCurrentDuelChecksum_ADDR, 0x00);
	gb_write8((uint16_t)(sCurrentDuelChecksum_ADDR + 1u), 0x00);
	DisableSRAM();
}
