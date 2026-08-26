#include "home/booster_pack.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"
#include "home/process_text.h"
#include "generated/hram.h"
#include "generated/wram.h"

#define DECK_SIZE 0x3Cu
#define PLAYER_TURN 0xC2u
#define BoosterPackText 0x0196u
#define ChooseTheCardYouWishToExamineText 0x0056u
#define PAD_A 0x01u
#define PAD_START 0x08u
/* <<< factory statics */

/* >>> factory _OpenBoosterPack */
void _OpenBoosterPack(void)
{
	hWhoseTurn = PLAYER_TURN;
	uint8_t *variables = wPlayerDuelVariables_PTR;
	for (uint8_t i = 0u; i < DECK_SIZE; i++)
		variables[i] = 0u;

	uint8_t *cards = wBoosterCardsDrawn_PTR;
	uint8_t *list = wDuelTempList_PTR;
	uint8_t index = 0u;
	while (*cards != 0u) {
		*list++ = index;
		cards++;
		index++;
	}
	*list = 0xFFu;

	(void)SetupText(0x38u, 0x9Fu);
	(void)InitAndDrawCardListScreenLayout();
	SetCardListHeaderText(BoosterPackText, ChooseTheCardYouWishToExamineText);
	wNoItemSelectionMenuKeys = (uint8_t)(PAD_A | PAD_START);
	(void)DisplayCardList();
}
/* <<< factory _OpenBoosterPack */
