#include "home/deck_machine.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/switch_sram.h"

#define DECK_NAME_SIZE 0x18u
#define NUM_DECK_MACHINE_SLOTS 0x05u
/* <<< factory statics */

/* >>> factory CheckIfSelectedDeckMachineEntryIsEmpty */
/* deck_machine.asm:772-789 */
uint8_t CheckIfSelectedDeckMachineEntryIsEmpty(void)
{
	uint16_t entry = (uint16_t)(wMachineDeckPtrs_ADDR
		+ (uint16_t)wSelectedDeckMachineEntry * 2u);
	uint16_t deck = (uint16_t)(gb_read8(entry)
		| (uint16_t)(gb_read8((uint16_t)(entry + 1u)) << 8));
	uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);

	EnableSRAM();
	uint8_t value = gb_read8(name);
	DisableSRAM();

	return value ? 0u : 0x90u;
}
/* <<< factory CheckIfSelectedDeckMachineEntryIsEmpty */
