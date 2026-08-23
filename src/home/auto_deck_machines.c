#include "home/auto_deck_machines.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/random.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "mem.h"
#define DECK_NAME_SIZE 0x18u
#define DECK_STRUCT_SIZE 0x54u
#define NUM_DECK_MACHINE_SLOTS 0x05u
#define AUTO_DECK_MACHINES_BANK 0x06u
#define AUTO_DECK_MACHINE_ENTRIES 0x78E8u
/* <<< factory statics */

/* >>> factory ReadAutoDeckConfiguration */
void ReadAutoDeckConfiguration(void)
{
	EnableSRAM();
	uint8_t machine = wCurAutoDeckMachine;
	uint16_t hl = (uint16_t)(HtimesL((uint16_t)(((uint16_t)(6u * NUM_DECK_MACHINE_SLOTS) << 8) | machine)) + AUTO_DECK_MACHINE_ENTRIES);

	for (uint8_t b = 0; b < NUM_DECK_MACHINE_SLOTS; b++) {
		uint16_t deck_de = (uint16_t)(HtimesL((uint16_t)(((uint16_t)DECK_STRUCT_SIZE << 8) | b)) + sAutoDecks_ADDR);

		const uint8_t *entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		uint16_t src_de = (uint16_t)(entry_ptr[0] | ((uint16_t)entry_ptr[1] << 8));
		uint16_t dst_hl = (uint16_t)(deck_de + DECK_NAME_SIZE);
		for (;;) {
			const uint8_t *cp = rom_ptr(AUTO_DECK_MACHINES_BANK, src_de);
			uint8_t count = cp[0];
			src_de++;
			if (count == 0u)
				break;
			cp = rom_ptr(AUTO_DECK_MACHINES_BANK, src_de);
			uint8_t card = cp[0];
			src_de++;
			for (uint8_t i = 0; i < count; i++) {
				gb_write8(dst_hl, card);
				dst_hl++;
			}
		}
		hl = (uint16_t)(hl + 2u);

		entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		uint16_t text_id = (uint16_t)(entry_ptr[0] | ((uint16_t)entry_ptr[1] << 8));
		(void)CopyText(text_id, wDismantledDeckName_ADDR);
		uint16_t name_hl = deck_de;
		uint16_t name_de = wDismantledDeckName_ADDR;
		for (;;) {
			uint8_t ch = gb_read8(name_de);
			gb_write8(name_hl, ch);
			name_hl++;
			if (ch == 0u)
				break;
			name_de++;
		}
		hl = (uint16_t)(hl + 2u);

		uint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + (uint16_t)b * 2u);
		entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		gb_write8(desc_addr, entry_ptr[0]);
		gb_write8((uint16_t)(desc_addr + 1u), entry_ptr[1]);
		hl = (uint16_t)(hl + 2u);
	}

	DisableSRAM();
}
/* <<< factory ReadAutoDeckConfiguration */
