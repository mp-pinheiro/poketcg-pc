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
