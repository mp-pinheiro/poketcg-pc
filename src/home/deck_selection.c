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
