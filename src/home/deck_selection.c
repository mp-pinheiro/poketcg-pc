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
