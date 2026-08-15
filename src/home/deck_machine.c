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

#include "home/switch_sram.h"

#define CARD_NOT_OWNED 0x80u
#define DECK_SIZE 0x3Cu

#include "home/deck_configuration.h"
#include "generated/sram.h"

#define DECK_STRUCT_SIZE            0x54u
#define NUM_DECK_SAVE_MACHINE_SLOTS 0x3cu
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

/* >>> factory SafelySwitchToSRAM1 */
/* deck_machine.asm:1261-1271. */
void SafelySwitchToSRAM1(void)
{
	if (hBankSRAM != 1u) {
		wTempBankSRAM = hBankSRAM;
		BankswitchSRAM(1u);
	}
}
/* <<< factory SafelySwitchToSRAM1 */

/* >>> factory SafelySwitchToTempSRAMBank */
/* deck_machine.asm:1273-1285. */
void SafelySwitchToTempSRAMBank(void)
{
	if (hBankSRAM != wTempBankSRAM)
		BankswitchSRAM(wTempBankSRAM);
}
/* <<< factory SafelySwitchToTempSRAMBank */

/* >>> factory CheckIfHasEnoughCardsToBuildDeck */
/* deck_machine.asm:1290-1323. */
DeckBuildCheckResult CheckIfHasEnoughCardsToBuildDeck(uint16_t *hl)
{
	EnableSRAM();
	uint16_t deck = *hl;
	uint16_t collection = wTempCardCollection_ADDR;

	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		uint8_t card = gb_read8(deck);
		deck = (uint16_t)(deck + 1u);
		uint16_t slot = (uint16_t)(collection + card);
		uint8_t count = gb_read8(slot);
		if (count == 0u || count == CARD_NOT_OWNED) {
			*hl = deck;
			DisableSRAM();
			return (DeckBuildCheckResult){ .a = count, .f = 0x90u };
		}
		gb_write8(slot, (uint8_t)(count - 1u));
	}

	*hl = deck;
	DisableSRAM();
	return (DeckBuildCheckResult){ .a = DECK_SIZE, .f = 0x00u };
}
/* <<< factory CheckIfHasEnoughCardsToBuildDeck */

/* >>> factory GetSavedDeckPointers */
/* deck_machine.asm:827-860. Clears the wMachineDeckPtrs array (2 bytes per
 * slot), then fills it with little-endian pointers to each consecutive
 * DECK_STRUCT_SIZE-byte saved-deck struct in sSavedDecks. Exits with hl/de
 * advanced past the table/structs processed. */
void GetSavedDeckPointers(uint16_t *hl, uint16_t *de)
{
	ClearMemory_Bank2((uint8_t)(NUM_DECK_SAVE_MACHINE_SLOTS * 2u), wMachineDeckPtrs_ADDR);
	uint16_t d = wMachineDeckPtrs_ADDR;
	uint16_t h = sSavedDecks_ADDR;
	for (uint8_t i = 0; i < NUM_DECK_SAVE_MACHINE_SLOTS; i++) {
		gb_write8(d++, (uint8_t)h);
		gb_write8(d++, (uint8_t)(h >> 8));
		h = (uint16_t)(h + DECK_STRUCT_SIZE);
	}
	*hl = h;
	*de = d;
}
/* <<< factory GetSavedDeckPointers */
