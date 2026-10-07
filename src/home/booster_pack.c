/* >>> part includes */
#include "home/booster_pack.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/core.h"
#include "home/process_text.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_2 */

/* >>> part PLAYER_TURN */
#define PLAYER_TURN 0xC2u
/* <<< part PLAYER_TURN */
/* >>> part PAD_A */
#define PAD_A 0x01u
/* <<< part PAD_A */
/* >>> part PAD_START */
#define PAD_START 0x08u
/* <<< part PAD_START */

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
