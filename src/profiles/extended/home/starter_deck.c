/* >>> part includes */
#include "home/starter_deck.h"
#include "home/deck_selection.h"
#include "home/duel.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "generated/sram.h"
#include "home/load_deck.h"
#include "home/print_text.h"
#include "home/switch_sram.h"

#define PLAYER_TURN 0xc2u
#define CHARMANDER_AND_FRIENDS_DECK 0x05u
#define SQUIRTLE_AND_FRIENDS_DECK 0x07u
#define BULBASAUR_AND_FRIENDS_DECK 0x09u

static const uint8_t kStarterCardIDs[6] = {3u, 4u, 5u, 6u, 7u, 8u};

static uint16_t collection_slot(CardId id)
{
	return (uint16_t)(card_id_index_address(sCardCollection_ADDR,
		(uint8_t)(id >> 1)) + (id & 1u));
}

static void store_deck_id_in_sram(uint8_t deck_id, uint16_t destination)
{
	if (LoadDeck(deck_id))
		return;

	uint16_t name = (uint16_t)(gb_read8(wDeckName_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wDeckName_ADDR + 1u)) << 8));
	CopyText(name, wDefaultText_ADDR);
	EnableSRAM();

	uint16_t src = wDefaultText_ADDR;
	uint16_t dst = destination;
	uint8_t value;
	do {
		value = gb_read8(src++);
		gb_write8(dst++, value);
	} while (value != 0u);

	uint16_t compressed = (uint16_t)(destination + DECK_NAME_SIZE);
	for (uint8_t group = 0u; group < 7u; group++) {
		uint8_t command = 0u;
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			uint8_t index = (uint8_t)(group * 8u + bit);
			CardId id = card_id_read_at(card_id_index_address(wPlayerDeck_ADDR, index));
			if ((id & 0x0100u) != 0u)
				command |= (uint8_t)(1u << (7u - bit));
		}
		gb_write8(compressed++, command);
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			uint8_t index = (uint8_t)(group * 8u + bit);
			CardId id = card_id_read_at(card_id_index_address(wPlayerDeck_ADDR, index));
			gb_write8(compressed++, (uint8_t)id);
		}
	}

	uint8_t command = 0u;
	for (uint8_t bit = 0u; bit < 4u; bit++) {
		uint8_t index = (uint8_t)(56u + bit);
		CardId id = card_id_read_at(card_id_index_address(wPlayerDeck_ADDR, index));
		if ((id & 0x0100u) != 0u)
			command |= (uint8_t)(1u << (7u - bit));
	}
	gb_write8(compressed++, (uint8_t)(command << 4));
	for (uint8_t bit = 0u; bit < 4u; bit++) {
		uint8_t index = (uint8_t)(56u + bit);
		CardId id = card_id_read_at(card_id_index_address(wPlayerDeck_ADDR, index));
		gb_write8(compressed++, (uint8_t)id);
	}
	DisableSRAM();
}

/* <<< factory statics */
/* >>> factory InitSaveData */
void InitSaveData(void)
{
	EnableSRAM();
	hWhoseTurn = PLAYER_TURN;
	for (uint16_t addr = sCardAndDeckSaveData_ADDR;
		addr != sCardAndDeckSaveDataEnd_ADDR; addr++)
		gb_write8(addr, 0u);

	store_deck_id_in_sram(CHARMANDER_AND_FRIENDS_DECK, sSavedDeck1_ADDR);
	store_deck_id_in_sram(SQUIRTLE_AND_FRIENDS_DECK, sSavedDeck2_ADDR);
	store_deck_id_in_sram(BULBASAUR_AND_FRIENDS_DECK, sSavedDeck3_ADDR);

	EnableSRAM();
	for (uint16_t i = 0u; i < card_id_collection_bytes(); i++)
		gb_write8((uint16_t)(sCardCollection_ADDR + i), CARD_NOT_OWNED);

	gb_write8(sCurrentDuel_ADDR, 0u);
	gb_write8((uint16_t)(sCurrentDuel_ADDR + 1u), 0u);
	gb_write8((uint16_t)(sCurrentDuel_ADDR + 2u), 0u);
	gb_write8(sTextSpeed_ADDR, TEXT_SPEED_3);
	wTextSpeed = TEXT_SPEED_3;
	gb_write8(sAnimationsDisabled_ADDR, 0u);
	gb_write8(sSkipDelayAllowed_ADDR, 0u);
	gb_write8(s0a004_ADDR, 0u);
	gb_write8(sReceivedLegendaryCards_ADDR, 0u);
	InitPromotionalCardAndDeckCounterSaveData();
	DisableSRAM();
}
/* <<< factory InitSaveData */

/* >>> factory _AddStarterDeck */
void _AddStarterDeck(uint8_t a)
{
	uint8_t idx = (uint8_t)(a * 2u);
	hWhoseTurn = PLAYER_TURN;
	store_deck_id_in_sram((uint8_t)(kStarterCardIDs[idx] + 2u), sDeck1_ADDR);
	SwapTurn();
	LoadDeck((uint8_t)(kStarterCardIDs[(uint8_t)(idx + 1u)] + 2u));
	SwapTurn();

	EnableSRAM();
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		CardId id = card_id_read_at(card_id_index_address(wPlayerDeck_ADDR, i));
		uint16_t slot = collection_slot(id);
		gb_write8(slot, (uint8_t)(gb_read8(slot) &
			(uint8_t)~(1u << CARD_NOT_OWNED_F)));
	}
	for (uint8_t i = 0u; i < 30u; i++) {
		CardId id = card_id_read_at(card_id_index_address(wOpponentDeck_ADDR, i));
		uint16_t slot = collection_slot(id);
		uint8_t value = (uint8_t)(gb_read8(slot) &
			(uint8_t)~(1u << CARD_NOT_OWNED_F));
		gb_write8(slot, (uint8_t)(value + 1u));
	}
	DisableSRAM();
}
/* <<< factory _AddStarterDeck */
