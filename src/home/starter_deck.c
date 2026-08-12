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
