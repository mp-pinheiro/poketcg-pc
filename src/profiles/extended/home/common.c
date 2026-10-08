/* >>> part includes_DUELVARS_ARENA_CARD */
#include "home/card_data.h"
#include "home/card_id_bus.h"
#include "home/core.h"
#include "home/duel.h"
#include "mem.h"
/* <<< part includes_DUELVARS_ARENA_CARD */
/* --- part includes_AI_MEWTWO_MILL */
/* --- part AI_MEWTWO_MILL */
/* >>> part includes_tail */
#include "home/core.h"
#include "generated/wram.h"

#include "home/booster_pack.h"

#include "generated/wram.h"
#include "home/attacks.h"
#include "home/duel.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/sound.h"

#include "home/ir_functions.h"

#include "home/card_pop.h"

#include "home/sound.h"

#include "home/link_duel.h"
#include "home/core.h"
#include "home/load_animation.h"
#include "home/process_text.h"
#include "home/sprite_vblank.h"
#include "home/time.h"
#include "home/lcd.h"
/* <<< part includes_tail */
/* >>> factory LookForCardIDInPlayArea_Bank8 */
LookForCardIDInPlayAreaResult LookForCardIDInPlayArea_Bank8(CardId de, uint8_t b)
{
	gb_write8(wTempCardIDToLook_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wTempCardIDToLook_ADDR + 1u), (uint8_t)(de >> 8));
	for (;;) {
		DuelistVarResult r = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + b));
		if (r.a == 0xffu)
			return (LookForCardIDInPlayAreaResult){0xffu, b, 0xc0u};
		(void)LoadCardDataToBuffer1_FromDeckIndex(r.a);
		if (gb_read8(wTempCardIDToLook_ADDR) == (uint8_t)de
		    && gb_read8((uint16_t)(wTempCardIDToLook_ADDR + 1u)) == (uint8_t)(de >> 8))
			return (LookForCardIDInPlayAreaResult){b, b, 0x90u};
		b++;
		if (b == MAX_PLAY_AREA_POKEMON)
			return (LookForCardIDInPlayAreaResult){MAX_PLAY_AREA_POKEMON, 0xffu, 0x00u};
	}
}
/* <<< factory LookForCardIDInPlayArea_Bank8 */
/* >>> factory CheckIfHasCardIDInHand */
CheckIfHasCardIDInHandResult CheckIfHasCardIDInHand(CardId de)
{
	(void)CreateHandCardList(0u);
	uint8_t *scan = wDuelTempList_PTR;
	uint8_t count = 0u;
	for (;;) {
		uint8_t index = *scan++;
		if (index == 0xFFu)
			return (CheckIfHasCardIDInHandResult){0xFFu, 0xC0u};
		hTempCardIndex_ff98 = index;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card_id_read_at(wLoadedCard1ID_ADDR) != de)
			continue;
		if (count != 0u)
			return (CheckIfHasCardIDInHandResult){hTempCardIndex_ff98, 0x10u};
		count++;
	}
}
/* <<< factory CheckIfHasCardIDInHand */
/* >>> factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
/* common.asm:4-45 */
CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result CheckIfPlayerHasPokemonOtherThanMewtwoLv53(uint8_t b, uint8_t c, uint8_t d, uint16_t hl)
{
	uint8_t e = 0u;
	SwapTurn();
	for (; e < DECK_SIZE; e++) {
		(void)LoadCardDataToBuffer2_FromDeckIndex(e);
		if (wLoadedCard2Type >= TYPE_ENERGY)
			continue;
		CardId card_id = card_id_read_at(wLoadedCard2ID_ADDR);
		if (card_id != MEWTWO_LV53) {
			SwapTurn();
			return (CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result){
				(uint8_t)card_id, F_C, b, c, d, e, wLoadedCard2ID_ADDR};
		}
	}
	SwapTurn();
	return (CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result){
		DECK_SIZE, 0x00u, b, c, d, e, wLoadedCard2ID_ADDR};
}
/* <<< factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
/* >>> factory LookForCardIDInLocation_Bank8 */
LookForCardIDInLocationBank8Result LookForCardIDInLocation_Bank8(uint8_t location, CardId de)
{
	for (uint8_t e = 0u; e < DECK_SIZE; e++) {
		uint8_t loc = GetTurnDuelistVariable((uint8_t)(DUELVARS_CARD_LOCATIONS + e)).a;
		if (loc != location)
			continue;
		if (GetCardIDFromDeckIndex(e) == de)
			return (LookForCardIDInLocationBank8Result){e, 0x90u};
	}
	return (LookForCardIDInLocationBank8Result){DECK_SIZE, 0x00u};
}
/* <<< factory LookForCardIDInLocation_Bank8 */
/* >>> factory LookForCardIDInHandList_Bank8 */
LookForCardIDInHandListResult LookForCardIDInHandList_Bank8(CardId de)
{
	gb_write8(wTempCardIDToLook_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wTempCardIDToLook_ADDR + 1u), (uint8_t)(de >> 8));
	HandListResult list = CreateHandCardList(0u);
	uint8_t d = list.d;
	uint8_t e = list.e;
	uint16_t scan = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(scan++);
		if (index == 0xFFu)
			return (LookForCardIDInHandListResult){0xFFu, 0xC0u, d};
		hTempCardIndex_ff98 = index;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (gb_read8(wTempCardIDToLook_ADDR) == e
		    && gb_read8((uint16_t)(wTempCardIDToLook_ADDR + 1u)) == d)
			return (LookForCardIDInHandListResult){hTempCardIndex_ff98, 0x90u, d};
	}
}
/* <<< factory LookForCardIDInHandList_Bank8 */
/* >>> factory LookForCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInHandAndPlayAreaWithDResult;
static LookForCardIDInHandAndPlayAreaWithDResult look_for_card_id_in_hand_and_play_area_with_d(CardId de)
{
	LookForCardIDInHandListResult r1 = LookForCardIDInHandList_Bank8(de);
	if (r1.f & 0x10u)
		return (LookForCardIDInHandAndPlayAreaWithDResult){r1.a, r1.f, (uint8_t)(de >> 8)};
	LookForCardIDInPlayAreaResult r2 = LookForCardIDInPlayArea_Bank8(de, PLAY_AREA_ARENA);
	if (r2.f & 0x10u)
		return (LookForCardIDInHandAndPlayAreaWithDResult){r2.a, r2.f, (uint8_t)(de >> 8)};
	uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
	return (LookForCardIDInHandAndPlayAreaWithDResult){r2.a, f, (uint8_t)(de >> 8)};
}
LookForCardIDInHandAndPlayAreaResult LookForCardIDInHandAndPlayArea(CardId de)
{
	LookForCardIDInHandAndPlayAreaWithDResult r =
		look_for_card_id_in_hand_and_play_area_with_d(de);
	return (LookForCardIDInHandAndPlayAreaResult){r.a, r.f};
}
/* <<< factory LookForCardIDInHandAndPlayArea */
/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
LookForCardIDToTradeWithDifferentHandCardResult LookForCardIDToTradeWithDifferentHandCard(CardId de, CardId bc)
{
	gb_write8(wTempAI_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wTempAI_ADDR + 1u), (uint8_t)(de >> 8));
	gb_write8(wTempAI2_ADDR, (uint8_t)bc);
	gb_write8((uint16_t)(wTempAI2_ADDR + 1u), (uint8_t)(bc >> 8));
	LookForCardIDInHandListResult r1 = LookForCardIDInHandList_Bank8(de);
	if (r1.f & 0x10u) {
		uint8_t f = (r1.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDToTradeWithDifferentHandCardResult){r1.a, f, 0u, 0xC5u};
	}
	LookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, de);
	if (!(r2.f & 0x10u)) {
		uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDToTradeWithDifferentHandCardResult){r2.a, f, 0u, 0u};
	}
	wTempAI = r2.a;
	(void)CreateHandCardList(0u);
	uint8_t *scan = wDuelTempList_PTR;
	uint8_t out_d = (uint8_t)(wDuelTempList_ADDR >> 8);
	for (;;) {
		uint8_t index = *scan++;
		if (index == 0xFFu)
			return (LookForCardIDToTradeWithDifferentHandCardResult){0xFFu, 0x00u, 0u, out_d};
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
		out_d = (uint8_t)(card_id >> 8);
		if (card_id == bc)
			continue;
		if (wLoadedCard1Type < TYPE_ENERGY)
			return (LookForCardIDToTradeWithDifferentHandCardResult){wTempAI, 0x10u, index, out_d};
	}
}
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
LookForCardIDInDeck_GivenCardIDInHandResult LookForCardIDInDeck_GivenCardIDInHand(CardId de, CardId bc)
{
	gb_write8(wTempAI_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wTempAI_ADDR + 1u), (uint8_t)(de >> 8));
	gb_write8(wTempAI2_ADDR, (uint8_t)bc);
	gb_write8((uint16_t)(wTempAI2_ADDR + 1u), (uint8_t)(bc >> 8));
	LookForCardIDInLocationBank8Result r1 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, de);
	if (!(r1.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r1.a, r1.f, 0u};
	wTempAIPokemonCard = r1.a;
	LookForCardIDInHandListResult r2 = LookForCardIDInHandList_Bank8(bc);
	if (!(r2.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r2.a, r2.f, 0xC5u};
	LookForCardIDInHandAndPlayAreaWithDResult r3 =
		look_for_card_id_in_hand_and_play_area_with_d(de);
	if (r3.f & 0x10u) {
		uint8_t f = (r3.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r3.a, f, r3.d};
	}
	uint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);
	return (LookForCardIDInDeck_GivenCardIDInHandResult){wTempAIPokemonCard, f, r3.d};
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CardId de, CardId bc)
{
	gb_write8(wTempAI_ADDR, (uint8_t)bc);
	gb_write8((uint16_t)(wTempAI_ADDR + 1u), (uint8_t)(bc >> 8));
	gb_write8(wTempAI2_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wTempAI2_ADDR + 1u), (uint8_t)(de >> 8));
	LookForCardIDInLocationBank8Result r1 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, de);
	if (!(r1.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r1.a, r1.f, 0u};
	wTempAIPokemonCard = r1.a;
	LookForCardIDInHandAndPlayAreaWithDResult r2 =
		look_for_card_id_in_hand_and_play_area_with_d(bc);
	if (!(r2.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r2.a, r2.f, r2.d};
	LookForCardIDInHandAndPlayAreaWithDResult r3 =
		look_for_card_id_in_hand_and_play_area_with_d(de);
	if (r3.f & 0x10u) {
		uint8_t f = (r3.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r3.a, f, r3.d};
	}
	uint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);
	return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){wTempAIPokemonCard, f, r3.d};
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
/* --- factory PreparePrinterConnection */
/* --- factory PrintDeckConfiguration */
/* >>> factory ShowPromotionalCardScreen */
/* menus/common.asm:46-48, `farcall _ShowPromotionalCardScreen` / `ret`. The
 * callee's wait loop (promotional_card.asm) never returns under a probe, so the
 * case stops both lanes at AssertSongFinished's entry instead of at a `ret`
 * (src/trace.h trace_set_stop). The whole screen therefore runs here rather
 * than the hand-written prefix that used to stand in for it. */
void ShowPromotionalCardScreen(CardId de)
{
	_ShowPromotionalCardScreen(de);
}
/* <<< factory ShowPromotionalCardScreen */
/* --- factory RequestToPrintCard */
/* --- factory PrintCardList */
/* --- factory ReceiveCard */
/* --- factory ReceiveDeckConfiguration */
/* --- factory DoCardPop */
/* --- factory SendCard */
/* --- factory SendDeckConfiguration */
/* --- factory SetUpAndStartLinkDuel */
/* === factory AIPickEnergyCardToDiscard */
/* === factory PickAttachedEnergyCardToRemove */
/* === factory PickTwoAttachedEnergyCards */
/* === factory FindBasicEnergyCardsInLocation */
/* === factory FindDuplicatePokemonCards */
