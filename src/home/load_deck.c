/* >>> part includes */
#include "home/load_deck.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/switch_rom.h"
#include "home/card_id_bus.h"
#include "mem.h"
/* <<< part includes */

/* >>> part BANK_DECK_DATA */
#define BANK_DECK_DATA 0x0cu
#define DECK_POINTERS  DeckPointers_ADDR
#define PLAYER_TURN    ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))
/* <<< part BANK_DECK_DATA */

/* >>> part copy_deck_data */
/* load_deck.asm + duel.asm:60-104. CopyDeckData is inlined: it expands the
 * (quantity, card-id) pair stream from banked ROM into the turn holder's deck and
 * appends the 2 name bytes to wDeckName. */
static void copy_deck_data(uint16_t src)
{
	uint16_t dest = (hWhoseTurn == PLAYER_TURN) ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	uint16_t h = dest;
	uint16_t d = src;
	gb_write8((uint16_t)(dest + card_id_deck_bytes(DECK_SIZE) - 1u), 0);
	for (;;) {
		uint8_t qty = gb_read8(d++);
		if (qty == 0)
			break;
		CardId cardid = card_id_read(&d);
		do {
			card_id_write(&h, cardid);
		} while (--qty);
	}
	gb_write8(wDeckName_ADDR, gb_read8(d++));
	gb_write8((uint16_t)(wDeckName_ADDR + 1u), gb_read8(d));
}
/* <<< part copy_deck_data */

/* >>> factory LoadDeck */
/* load_deck.asm:4-32. Returns the carry flag (set if DeckPointers[id] is NULL). */
uint8_t LoadDeck(uint8_t a)
{
	uint8_t saved = hBankROM;
	BankswitchROM(BANK_DECK_DATA);
	uint16_t dp = (uint16_t)(DECK_POINTERS + (uint16_t)a * 2u);
	uint16_t ptr = (uint16_t)(gb_read8(dp) | (uint16_t)gb_read8((uint16_t)(dp + 1u)) << 8);
	uint8_t carry = 1;
	if (ptr != 0) {
		copy_deck_data(ptr);
		carry = 0;
	}
	BankswitchROM(saved);
	return carry;
}
/* <<< factory LoadDeck */
