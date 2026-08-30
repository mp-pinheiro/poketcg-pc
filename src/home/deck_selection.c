#include "home/deck_selection.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/random.h"

#define DECK_CARD_STRIDE 0x54u

#define DECK_STRUCT_SIZE 0x54u

#include "generated/wram.h"

#include "mem.h"

#include "generated/wram.h"
#include "mem.h"

#include "home/switch_sram.h"
#include "mem.h"
#define DECK_SIZE 0x3Cu

#include "home/deck_selection.h"
#define SYM_0 0x20u

#define HandCardsGfx 0x4d15u
#define v0Tiles2_dest 0x9380u

#define TRUE 0x01u

#define ThereIsNoDeckHereText 0x022fu

#include "generated/wram.h"
#define DECK_CONFIG_BUFFER_SIZE 0x50u

#include "generated/wram.h"
#include "home/deck_configuration.h"

#define NUM_FILTERS 0x09u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_check.h"

#define PAD_START 0x08u
#define ALL_DECKS 0xFFu
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/input_name.h"
#include "home/write_number.h"
#include "mem.h"
#define MAX_DECK_NAME_LENGTH 0x14u
#define MAX_UNNAMED_DECK_NUM 0x3e7u
#define INPUT_CUR_DECK_DECK1_DATA 0x6763u
#define INPUT_CUR_DECK_DECK2_DATA 0x676cu
#define INPUT_CUR_DECK_DECK3_DATA 0x6775u
#define INPUT_CUR_DECK_DECK4_DATA 0x677eu
/* <<< factory statics */

/* >>> factory GetPointerToDeckCards */
/* deck_selection.asm:528-545 */
uint16_t GetPointerToDeckCards(void)
{
	uint16_t hl = (uint16_t)(((uint16_t)wCurDeck << 8) | DECK_CARD_STRIDE);
	uint16_t offset = HtimesL(hl);
	return (uint16_t)(sDeck1Cards_ADDR + offset);
}
/* <<< factory GetPointerToDeckCards */

/* >>> factory ResetCheckMenuCursorPositionAndBlink */
/* deck_selection.asm:541-551 */
ResetCheckMenuCursorPositionAndBlinkResult ResetCheckMenuCursorPositionAndBlink(void)
{
	wCheckMenuCursorXPosition = 0u;
	wCheckMenuCursorYPosition = 0u;
	wCheckMenuCursorBlinkCounter = 0u;
	return (ResetCheckMenuCursorPositionAndBlinkResult){0u, 0x80u};
}
/* <<< factory ResetCheckMenuCursorPositionAndBlink */

/* >>> factory GetPointerToDeckName */
uint16_t GetPointerToDeckName(void)
{
	uint8_t deck = wCurDeck;
	uint16_t offset = HtimesL((uint16_t)(((uint16_t)deck << 8) | DECK_STRUCT_SIZE));
	return (uint16_t)(sDeck1Name_ADDR + offset);
}
/* <<< factory GetPointerToDeckName */

/* >>> factory InitDeckBuildingParams */
InitDeckBuildingParamsResult InitDeckBuildingParams(uint16_t *hl, uint8_t f)
{
	uint8_t a = 0u;
	uint8_t b = 7u;
	for (uint8_t i = 0; i < 7u; i++) {
		a = gb_read8((*hl)++);
		wMaxNumCardsAllowed_PTR[i] = a;
		b--;
	}
	return (InitDeckBuildingParamsResult){a, (uint8_t)((f & 0x10u) | 0xC0u), b, 0xCFD8u, *hl};
}
/* <<< factory InitDeckBuildingParams */

/* >>> factory CheckIfCurDeckIsValid */
CheckIfCurDeckIsValidResult CheckIfCurDeckIsValid(void)
{
	uint8_t deck = gb_read8(0xCEB1u);
	uint16_t hl = (uint16_t)(0xCEB2u + deck);
	uint8_t b = 0u;
	uint8_t c = deck;
	uint8_t value = gb_read8(hl);
	uint8_t f = value ? 0x00u : 0x90u;
	return (CheckIfCurDeckIsValidResult){value, f, b, c, hl};
}
/* <<< factory CheckIfCurDeckIsValid */

/* >>> factory CancelDeckSelectionSubMenu */
void CancelDeckSelectionSubMenu(void)
{
	return;
}
/* <<< factory CancelDeckSelectionSubMenu */

/* >>> factory CopyDeckFromSRAM */
CopyDeckFromSRAMResult CopyDeckFromSRAM(uint16_t de, uint16_t hl)
{
	EnableSRAM();
	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		gb_write8(hl, gb_read8(de));
		de++;
		hl++;
	}
	gb_write8(hl, 0u);
	DisableSRAM();
	return (CopyDeckFromSRAMResult){0u, 0x80u, de, hl};
}
/* <<< factory CopyDeckFromSRAM */

/* >>> factory Func_9001 */
Func_9001Result Func_9001(uint16_t hl)
{
	uint16_t de = 0xd00au;
	static const uint16_t steps[3] = {(uint16_t)-100, (uint16_t)-10, (uint16_t)-1};
	uint8_t a = 0u;
	uint8_t f = 0u;
	for (uint8_t i = 0u; i < 3u; i++) {
		uint16_t bc = steps[i];
		uint8_t digit = (uint8_t)(SYM_0 - 1u);
		uint8_t carry;
		do {
			digit++;
			uint32_t sum = (uint32_t)hl + (uint32_t)bc;
			hl = (uint16_t)sum;
			carry = (sum > 0xFFFFu) ? 1u : 0u;
		} while (carry);
		gb_write8(de, digit);
		de++;
		uint8_t bc_lo = (uint8_t)bc;
		uint8_t bc_hi = (uint8_t)(bc >> 8);
		uint8_t l = (uint8_t)hl;
		uint8_t h = (uint8_t)(hl >> 8);
		uint8_t new_l = (uint8_t)(l - bc_lo);
		uint8_t borrow_lo = (l < bc_lo) ? 1u : 0u;
		int result = (int)h - (int)bc_hi - (int)borrow_lo;
		uint8_t new_h = (uint8_t)result;
		uint8_t carry_hi = (result < 0) ? 1u : 0u;
		uint8_t half_hi = (((int)(h & 0xFu) - (int)(bc_hi & 0xFu) - (int)borrow_lo) < 0) ? 1u : 0u;
		f = (uint8_t)((new_h == 0u ? 0x80u : 0u) | 0x40u | (half_hi ? 0x20u : 0u) | (carry_hi ? 0x10u : 0u));
		a = new_h;
		hl = (uint16_t)(((uint16_t)new_h << 8) | new_l);
	}
	return (Func_9001Result){a, f, (uint8_t)(de >> 8), (uint8_t)de, hl};
}
/* <<< factory Func_9001 */

/* >>> factory LoadHandCardsIcon */
LoadHandCardsIconResult LoadHandCardsIcon(void)
{
	gb_write8(0x2000u, 0x02u);
	uint16_t hl = HandCardsGfx;
	uint16_t de = v0Tiles2_dest;
	CopyListFromHLToDE(&hl, &de);
	return (LoadHandCardsIconResult){hl, (uint8_t)(de >> 8), (uint8_t)de};
}
/* <<< factory LoadHandCardsIcon */

/* >>> factory InitPromotionalCardAndDeckCounterSaveData */
LoadHandCardsIconResult InitPromotionalCardAndDeckCounterSaveData(void)
{
	EnableSRAM();
	gb_write8(sHasPromotionalCards_ADDR, 0u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 1u), 1u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 2u), 1u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 3u), 1u);
	gb_write8(sUnnamedDeckCounter_ADDR, 1u);
	DisableSRAM();
	return LoadHandCardsIcon();
}
/* <<< factory InitPromotionalCardAndDeckCounterSaveData */

/* >>> factory PrepareMenuGraphics */
void PrepareMenuGraphics(void)
{
	wTileMapFill = 0u;
	ZeroObjectPositions();
	EmptyScreen();
	wVBlankOAMCopyToggle = TRUE;
	LoadCursorTile();
	LoadSymbolsFont();
	LoadDuelCardSymbolTiles();
	LoadHandCardsIcon();
	SetDefaultConsolePalettes();
	SetupText(0x3cu, 0xbfu);
}
/* <<< factory PrepareMenuGraphics */

/* >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */
void EmptyScreenAndLoadFontDuelAndHandCardsIcons(void)
{
	wTileMapFill = 0u;
	EmptyScreen();
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	LoadSymbolsFont();
	LoadDuelCardSymbolTiles();
	LoadHandCardsIcon();
	SetDefaultConsolePalettes();
	SetupText(0x3cu, 0xbfu);
}
/* <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */

/* >>> factory PrintThereIsNoDeckHereText */
uint8_t PrintThereIsNoDeckHereText(void)
{
	DrawWideTextBox_WaitForInput(ThereIsNoDeckHereText);
	return wCurDeck;
}
/* <<< factory PrintThereIsNoDeckHereText */

/* >>> factory WriteCardListsTerminatorBytes */
WriteCardListsTerminatorBytesResult WriteCardListsTerminatorBytes(void)
{
	uint16_t filtered_terminator = (uint16_t)(wFilteredCardList_ADDR + DECK_SIZE);
	gb_write8(filtered_terminator, 0u);
	uint16_t deck_terminator = (uint16_t)(wCurDeckCards_ADDR + DECK_CONFIG_BUFFER_SIZE);
	gb_write8(deck_terminator, 0u);
	return (WriteCardListsTerminatorBytesResult){0u, 0x80u, 0u, 0x50u, 0xCF67u};
}
/* <<< factory WriteCardListsTerminatorBytes */

/* >>> factory OpenDeckConfirmationMenu */
void OpenDeckConfirmationMenu(uint16_t de, uint16_t hl)
{
	/* copy deck name */
	CopyListFromHLToDEInSRAM(hl, wCurDeckName_ADDR);

	/* copy deck cards */
	CopyDeckFromSRAM(de, wCurDeckCards_ADDR);

	ClearMemory_Bank2(NUM_FILTERS, wCardFilterCounts_ADDR);
	wTotalCardCount = DECK_SIZE;
	wCardFilterCounts = DECK_SIZE;
	HandleDeckConfirmationMenu();
}
/* <<< factory OpenDeckConfirmationMenu */

/* >>> factory HandleStartButtonInDeckSelectionMenu */
HandleStartButtonInDeckSelectionMenuResult HandleStartButtonInDeckSelectionMenu(void)
{
	uint8_t a = (uint8_t)(hDPadHeld & PAD_START);
	if (a == 0u)
		return (HandleStartButtonInDeckSelectionMenuResult){a, 0xA0u};

	wCurDeck = wCurMenuItem;
	CheckIfCurDeckIsValidResult validity = CheckIfCurDeckIsValid();
	if ((validity.f & 0x10u) != 0u) {
		PlaySFXConfirmOrCancel(MENU_CANCEL);
		uint8_t deck = PrintThereIsNoDeckHereText();
		return (HandleStartButtonInDeckSelectionMenuResult){deck, 0x90u};
	}

	PlaySFXConfirmOrCancel(MENU_CONFIRM);
	uint16_t cards = GetPointerToDeckCards();
	uint16_t name = GetPointerToDeckName();
	OpenDeckConfirmationMenu(cards, name);
	DrawDecksScreen(ALL_DECKS);
	return (HandleStartButtonInDeckSelectionMenuResult){wCurDeck, 0x10u};
}
/* <<< factory HandleStartButtonInDeckSelectionMenu */

/* >>> factory InputCurDeckName */
void InputCurDeckName(void)
{
	uint8_t deck = wCurDeck;
	uint16_t question = INPUT_CUR_DECK_DECK4_DATA;
	if (deck == 0u)
		question = INPUT_CUR_DECK_DECK1_DATA;
	else if (deck == 1u)
		question = INPUT_CUR_DECK_DECK2_DATA;
	else if (deck == 2u)
		question = INPUT_CUR_DECK_DECK3_DATA;

	g_rom_bank = 6u;
	(void)InputDeckName(MAX_DECK_NAME_LENGTH, 4u, 1u,
		(uint8_t)(wCurDeckName_ADDR >> 8), (uint8_t)wCurDeckName_ADDR, question);
	if (gb_read8(wCurDeckName_ADDR) != 0u)
		return;

	EnableSRAM();
	uint8_t counter_low = sUnnamedDeckCounter;
	uint8_t counter_high = sUnnamedDeckCounter_PTR[1];
	DisableSRAM();
	uint16_t counter = (uint16_t)(((uint16_t)counter_high << 8) | counter_low);
	uint16_t text = wDefaultText_ADDR;
	TwoByteNumberToText(counter, &text);

	uint16_t name = wCurDeckName_ADDR;
	gb_write8(name++, 0x06u);
	gb_write8(name++, (uint8_t)'D');
	gb_write8(name++, (uint8_t)'e');
	gb_write8(name++, (uint8_t)'c');
	gb_write8(name++, (uint8_t)'k');
	gb_write8(name++, (uint8_t)' ');
	uint16_t digits = (uint16_t)(wDefaultText_ADDR + 2u);
	gb_write8(name++, gb_read8(digits++));
	gb_write8(name++, gb_read8(digits++));
	gb_write8(name++, gb_read8(digits));
	gb_write8(name, 0u);

	EnableSRAM();
	counter = (uint16_t)(((uint16_t)sUnnamedDeckCounter_PTR[1] << 8) | sUnnamedDeckCounter);
	if (counter == MAX_UNNAMED_DECK_NUM)
		counter = 0u;
	counter = (uint16_t)(counter + 1u);
	sUnnamedDeckCounter_PTR[1] = (uint8_t)(counter >> 8);
	sUnnamedDeckCounter = (uint8_t)counter;
	DisableSRAM();
}
/* <<< factory InputCurDeckName */
