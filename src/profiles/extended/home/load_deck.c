#include "home/load_deck.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/switch_rom.h"
#include "home/card_id_bus.h"
#include "mem.h"

#define BANK_DECK_DATA 0x0cu
#define DECK_POINTERS  DeckPointers_ADDR
#define PLAYER_TURN    ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))

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

/* >>> factory CompressDeckToSRAM */
void CompressDeckToSRAM(uint16_t de, uint16_t hl)
{
	uint16_t source = de;
	uint16_t destination = hl;
	for (uint8_t block = 0u; block < 7u; block++) {
		uint8_t command = 0u;
		uint16_t look = source;
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			uint8_t high = gb_read8((uint16_t)(look + 1u));
			look = (uint16_t)(look + 2u);
			command = (uint8_t)((command << 1) | (high & 0x01u));
		}
		gb_write8(destination++, command);
		for (uint8_t card = 0u; card < 8u; card++) {
			gb_write8(destination++, gb_read8(source));
			source = (uint16_t)(source + 2u);
		}
	}
	uint8_t command = 0u;
	uint16_t look = source;
	for (uint8_t bit = 0u; bit < 4u; bit++) {
		uint8_t high = gb_read8((uint16_t)(look + 1u));
		look = (uint16_t)(look + 2u);
		command = (uint8_t)((command << 1) | (high & 0x01u));
	}
	gb_write8(destination++, (uint8_t)(command << 4));
	for (uint8_t card = 0u; card < 4u; card++) {
		gb_write8(destination++, gb_read8(source));
		source = (uint16_t)(source + 2u);
	}
}
/* <<< factory CompressDeckToSRAM */

/* >>> factory DecompressSRAMDeck */
void DecompressSRAMDeck(uint16_t de, uint16_t hl)
{
	uint16_t source = de;
	uint16_t destination = hl;
	wDecompSavedDeckCount = DECK_SIZE;
	for (;;) {
		uint8_t command = gb_read8(source++);
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			gb_write8(destination++, gb_read8(source++));
			gb_write8(destination++, (uint8_t)(command >> 7));
			command = (uint8_t)(command << 1);
			wDecompSavedDeckCount = (uint8_t)(wDecompSavedDeckCount - 1u);
			if (wDecompSavedDeckCount == 0u)
				return;
		}
	}
}
/* <<< factory DecompressSRAMDeck */
