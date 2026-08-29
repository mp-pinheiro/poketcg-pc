#include "home/boss_deck_set_up.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"
#include "generated/wram.h"
#include "mem.h"
#define DUELVARS_DECK_CARDS 0x7Eu
#define DUELVARS_HAND 0x42u
#define STARTING_HAND_SIZE 0x07u
#define TYPE_ENERGY 0x08u
#define TYPE_TRAINER 0x10u
/* <<< factory statics */

/* >>> factory SetUpBossStartingHandAndDeck */
void SetUpBossStartingHandAndDeck(void)
{
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_HAND);
	uint8_t b = STARTING_HAND_SIZE;
	uint16_t hl = hand.hl;
	while (b != 0u) {
		uint8_t card = gb_read8(hl);
		RemoveCardFromHand(card);
		ReturnCardToDeck(card);
		b = (uint8_t)(b - 1u);
	}

	for (;;) {
		wAISetupBasicPokemonCount = 0u;
		wAISetupEnergyCount = 0u;

		DuelistVarResult deck = GetTurnDuelistVariable(DUELVARS_DECK_CARDS);
		hl = deck.hl;
		b = STARTING_HAND_SIZE;
		while (b != 0u) {
			uint8_t card = gb_read8(hl++);
			(void)LoadCardDataToBuffer1_FromDeckIndex(card);
			if (wLoadedCard1Type < TYPE_ENERGY) {
				if (wLoadedCard1Stage == 0u)
					wAISetupBasicPokemonCount++;
			} else if (wLoadedCard1Type != TYPE_TRAINER) {
				wAISetupEnergyCount++;
			}
			b = (uint8_t)(b - 1u);
		}
		if (wAISetupBasicPokemonCount < 2u || wAISetupEnergyCount < 2u) {
			(void)ShuffleDeck(0u, 0u);
			continue;
		}

		b = 6u;
		while (b != 0u) {
			uint8_t card = gb_read8(hl++);
			uint8_t avoid_high = gb_read8((uint16_t)(wAICardListAvoidPrize_ADDR + 1u));
			if (avoid_high != 0u) {
				uint16_t list = (uint16_t)(gb_read8(wAICardListAvoidPrize_ADDR) |
					((uint16_t)avoid_high << 8));
				(void)GetCardIDFromDeckIndex(card);
				(void)gb_read8(list);
			}
			b = (uint8_t)(b - 1u);
		}

		b = 6u;
		while (b != 0u) {
			uint8_t card = gb_read8(hl++);
			(void)LoadCardDataToBuffer1_FromDeckIndex(card);
			if (wLoadedCard1Type < TYPE_ENERGY) {
				if (wLoadedCard1Stage == 0u)
					wAISetupBasicPokemonCount++;
			} else if (wLoadedCard1Type != TYPE_TRAINER) {
				wAISetupEnergyCount++;
			}
			b = (uint8_t)(b - 1u);
		}
		if (wAISetupBasicPokemonCount < 4u || wAISetupEnergyCount < 4u) {
			(void)ShuffleDeck(0u, 0u);
			continue;
		}

		deck = GetTurnDuelistVariable(DUELVARS_DECK_CARDS);
		hl = deck.hl;
		b = STARTING_HAND_SIZE;
		while (b != 0u) {
			uint8_t card = gb_read8(hl++);
			SearchCardInDeckAndAddToHand(card);
			AddCardToHand(card);
			b = (uint8_t)(b - 1u);
		}
		return;
	}
}
/* <<< factory SetUpBossStartingHandAndDeck */
