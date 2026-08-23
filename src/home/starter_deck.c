#include "home/starter_deck.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_deck.h"
#include "home/print_text.h"
#include "home/switch_sram.h"

#define DECK_NAME_SIZE 24u
#define DECK_SIZE 60u

#include "generated/sram.h"

#define CARDPOP_NAME_LIST_MAX_ELEMS 0x10u
#define CARD_NOT_OWNED 0x80u
#define NAME_BUFFER_LENGTH 0x10u
#define PLAYER_TURN 0xc2u
#define TEXT_SPEED_3 0x02u
#define CHARMANDER_AND_FRIENDS_DECK 0x05u
#define SQUIRTLE_AND_FRIENDS_DECK 0x07u
#define BULBASAUR_AND_FRIENDS_DECK 0x09u
/* <<< factory statics */

/* >>> factory CopyDeckNameAndCards */
/* starter_deck.asm:137-173, .CopyDeckName inlined (:175-182). a = deck ID in
 * (consumed by LoadDeck); hl = SRAM destination for the 24-byte name field
 * (DECK_NAME_SIZE) immediately followed by the 60-byte card array
 * (DECK_SIZE). b/c/d/e/hl are all push/pop-bracketed around the whole body
 * (:138-140/170-172), so they reach the caller unchanged on every path; a
 * and the LoadDeck carry are scratch here -- neither call site
 * (starter_deck.asm:20, :83/85/87) branches on them, so neither is part of
 * the contract. A failed LoadDeck skips both copy loops entirely. */
void CopyDeckNameAndCards(uint8_t a, uint16_t hl)
{
	if (LoadDeck(a))
		return;

	uint16_t nameId = (uint16_t)(gb_read8(wDeckName_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wDeckName_ADDR + 1u)) << 8);
	CopyText(nameId, wDefaultText_ADDR);

	EnableSRAM();
	uint16_t dst = hl;
	uint16_t src = wDefaultText_ADDR;
	uint8_t ch;
	do {
		ch = gb_read8(src++);
		gb_write8(dst++, ch);
	} while (ch != 0);

	dst = (uint16_t)(hl + DECK_NAME_SIZE);
	src = wPlayerDeck_ADDR;
	for (uint8_t i = 0; i < DECK_SIZE; i++)
		gb_write8(dst++, gb_read8(src++));
	DisableSRAM();
}
/* <<< factory CopyDeckNameAndCards */

/* >>> factory InitSaveData */
void InitSaveData(void)
{
	EnableSRAM();
	hWhoseTurn = PLAYER_TURN;
	for (uint16_t addr = sCardAndDeckSaveData_ADDR; addr != sCardAndDeckSaveDataEnd_ADDR; addr++)
		gb_write8(addr, 0u);

	CopyDeckNameAndCards(CHARMANDER_AND_FRIENDS_DECK, sSavedDeck1_ADDR);
	CopyDeckNameAndCards(SQUIRTLE_AND_FRIENDS_DECK, sSavedDeck2_ADDR);
	CopyDeckNameAndCards(BULBASAUR_AND_FRIENDS_DECK, sSavedDeck3_ADDR);

	EnableSRAM();
	for (uint16_t i = 0; i < 256u; i++)
		gb_write8((uint16_t)(sCardCollection_ADDR + i), CARD_NOT_OWNED);

	gb_write8(sCurrentDuel_ADDR, 0u);
	gb_write8((uint16_t)(sCurrentDuel_ADDR + 1u), 0u);
	gb_write8((uint16_t)(sCurrentDuel_ADDR + 2u), 0u);

	for (uint8_t i = 0; i < CARDPOP_NAME_LIST_MAX_ELEMS; i++)
		gb_write8((uint16_t)(sCardPopNameList_ADDR + (uint16_t)i * NAME_BUFFER_LENGTH), 0u);

	gb_write8(sPrinterContrastLevel_ADDR, 2u);
	gb_write8(sTextSpeed_ADDR, TEXT_SPEED_3);
	wTextSpeed = TEXT_SPEED_3;

	gb_write8(sAnimationsDisabled_ADDR, 0u);
	gb_write8(sSkipDelayAllowed_ADDR, 0u);
	gb_write8(0xA004u, 0u);
	gb_write8(sTotalCardPopsDone_ADDR, 0u);
	gb_write8(sReceivedLegendaryCards_ADDR, 0u);
	InitPromotionalCardAndDeckCounterSaveData();
	DisableSRAM();
}
/* <<< factory InitSaveData */
