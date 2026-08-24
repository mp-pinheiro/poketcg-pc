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

#include "home/deck_machine.h"
#define DECK_1 0x01u
#define DECK_2 0x02u
#define DECK_3 0x04u
#define DECK_4 0x08u
#define NUM_DECKS 0x04u
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

/* >>> factory CheckWhichDecksToDismantleToBuildSavedDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t failed; } CheckResult_wDDTBSD;

static CheckResult_wDDTBSD check_if_can_build_wDDTBSD(uint8_t a_in, uint8_t f_in)
{
	uint8_t b = gb_read8(wSelectedDeckMachineEntry_ADDR);
	DeckBuildCheckResult r = CheckIfCanBuildSavedDeck(a_in, b);
	if (r.f & 0x10u) {
		uint8_t f_out = (uint8_t)((f_in & 0x80u) | 0x10u);
		return (CheckResult_wDDTBSD){a_in, f_out, 1u};
	}
	gb_write8(wDecksToBeDismantled_ADDR, a_in);
	uint8_t f_out = (uint8_t)(a_in == 0u ? 0x80u : 0u);
	return (CheckResult_wDDTBSD){a_in, f_out, 0u};
}

static uint8_t cp_flags_wDDTBSD(uint8_t a, uint8_t n)
{
	uint8_t z = (a == n) ? 0x80u : 0u;
	uint8_t h = ((a & 0x0Fu) < (n & 0x0Fu)) ? 0x20u : 0u;
	uint8_t c = (a < n) ? 0x10u : 0u;
	return (uint8_t)(z | 0x40u | h | c);
}

CheckWhichDecksToDismantleToBuildSavedDeckResult CheckWhichDecksToDismantleToBuildSavedDeck(void)
{
	gb_write8(wDecksToBeDismantled_ADDR, 0u);
	uint8_t f = 0x80u;

	uint8_t a = DECK_1;
	for (;;) {
		CheckResult_wDDTBSD cr = check_if_can_build_wDDTBSD(a, f);
		a = cr.a; f = cr.f;
		if (!cr.failed) {
			return (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};
		}
		a = (uint8_t)(a << 1);
		f = cp_flags_wDDTBSD(a, (uint8_t)(1u << NUM_DECKS));
		if (a == (uint8_t)(1u << NUM_DECKS)) {
			break;
		}
	}

	uint8_t two_deck_combos[6] = {
		(uint8_t)(DECK_1 | DECK_2), (uint8_t)(DECK_1 | DECK_3), (uint8_t)(DECK_1 | DECK_4),
		(uint8_t)(DECK_2 | DECK_3), (uint8_t)(DECK_2 | DECK_4), (uint8_t)(DECK_3 | DECK_4),
	};
	for (uint8_t i = 0u; i < 6u; i++) {
		a = two_deck_combos[i];
		CheckResult_wDDTBSD cr = check_if_can_build_wDDTBSD(a, f);
		a = cr.a; f = cr.f;
		if (!cr.failed) {
			return (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};
		}
	}

	a = (uint8_t)(0xFFu ^ DECK_4);
	for (;;) {
		CheckResult_wDDTBSD cr = check_if_can_build_wDDTBSD(a, f);
		a = cr.a; f = cr.f;
		if (!cr.failed) {
			return (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};
		}
		a = (uint8_t)((int8_t)a >> 1);
		f = cp_flags_wDDTBSD(a, 0xFFu);
		if (a == 0xFFu) {
			break;
		}
	}

	a = 0xFFu;
	CheckResult_wDDTBSD cr = check_if_can_build_wDDTBSD(a, f);
	a = cr.a; f = cr.f;
	if (!cr.failed) {
		return (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};
	}

	f = (uint8_t)((f & 0x80u) | 0x10u);
	return (CheckWhichDecksToDismantleToBuildSavedDeckResult){a, f};
}
/* <<< factory CheckWhichDecksToDismantleToBuildSavedDeck */
