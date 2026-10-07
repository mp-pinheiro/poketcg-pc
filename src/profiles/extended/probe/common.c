/* === part includes */
/* >>> part probe_card_id */
static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}
/* <<< part probe_card_id */
/* >>> factory LookForCardIDInPlayArea_Bank8 */
static void adapt_LookForCardIDInPlayArea_Bank8(ProbeState *s)
{
	LookForCardIDInPlayAreaResult r = LookForCardIDInPlayArea_Bank8(probe_card_id(s), s->b);
	s->a = r.a;
	s->b = r.b;
	s->f = r.f;
}
/* <<< factory LookForCardIDInPlayArea_Bank8 */
/* >>> factory CheckIfHasCardIDInHand */
static void adapt_CheckIfHasCardIDInHand(ProbeState *s)
{
	CheckIfHasCardIDInHandResult r = CheckIfHasCardIDInHand(probe_card_id(s));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasCardIDInHand */
/* >>> factory LookForCardIDInLocation_Bank8 */
static void adapt_LookForCardIDInLocation_Bank8(ProbeState *s)
{
	LookForCardIDInLocationBank8Result r = LookForCardIDInLocation_Bank8(s->a, probe_card_id(s));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInLocation_Bank8 */
/* >>> factory LookForCardIDInHandList_Bank8 */
static void adapt_LookForCardIDInHandList_Bank8(ProbeState *s)
{
	LookForCardIDInHandListResult r = LookForCardIDInHandList_Bank8(probe_card_id(s));
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory LookForCardIDInHandList_Bank8 */
/* >>> factory LookForCardIDInHandAndPlayArea */
static void adapt_LookForCardIDInHandAndPlayArea(ProbeState *s)
{
	LookForCardIDInHandAndPlayAreaResult r = LookForCardIDInHandAndPlayArea(probe_card_id(s));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHandAndPlayArea */
/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
static void adapt_LookForCardIDToTradeWithDifferentHandCard(ProbeState *s)
{
	LookForCardIDToTradeWithDifferentHandCardResult r =
		LookForCardIDToTradeWithDifferentHandCard(probe_card_id(s), (CardId)((uint16_t)s->b << 8 | s->c));
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
static void adapt_LookForCardIDInDeck_GivenCardIDInHand(ProbeState *s)
{
	LookForCardIDInDeck_GivenCardIDInHandResult r =
		LookForCardIDInDeck_GivenCardIDInHand(probe_card_id(s), (CardId)((uint16_t)s->b << 8 | s->c));
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
static void adapt_LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ProbeState *s)
{
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(probe_card_id(s),
			(CardId)((uint16_t)s->b << 8 | s->c));
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
/* --- factory PreparePrinterConnection */
/* --- factory PrintDeckConfiguration */
/* >>> factory ShowPromotionalCardScreen */
static void adapt_ShowPromotionalCardScreen(ProbeState *s)
{
	ShowPromotionalCardScreen(probe_card_id(s));
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
/* >>> part probe_entries_common */
const ProbeEntry probe_entries_common[] = {
	{ "CountOppEnergyCardsInHand", adapt_CountOppEnergyCardsInHand },
	{ "ConvertHPToDamageCounters_Bank8", adapt_ConvertHPToDamageCounters_Bank8 },
	{ "CalculateWordTensDigit", adapt_CalculateWordTensDigit },
	{ "PickTwoAttachedEnergyCards", adapt_PickTwoAttachedEnergyCards },
	{ "ClearMemory_Bank8", adapt_ClearMemory_Bank8 },
	{ "PickAttachedEnergyCardToRemove", adapt_PickAttachedEnergyCardToRemove },
	{ "CopyListWithFFTerminatorFromHLToDE_Bank8", adapt_CopyListWithFFTerminatorFromHLToDE_Bank8 },
	{ "LookForCardIDInPlayArea_Bank8", adapt_LookForCardIDInPlayArea_Bank8 },
	{ "CheckIfHasCardIDInHand", adapt_CheckIfHasCardIDInHand },
	{ "FindBasicEnergyCardsInLocation", adapt_FindBasicEnergyCardsInLocation },
	{ "CalculateBDividedByA_Bank8", adapt_CalculateBDividedByA_Bank8 },
	{ "CheckIfPlayerHasPokemonOtherThanMewtwoLv53", adapt_CheckIfPlayerHasPokemonOtherThanMewtwoLv53 },
	{ "RemoveFromListDifferentCardOfGivenType", adapt_RemoveFromListDifferentCardOfGivenType },
	{ "CountPokemonCardsInHandAndInPlayArea", adapt_CountPokemonCardsInHandAndInPlayArea },
	{ "LookForCardIDInLocation_Bank8", adapt_LookForCardIDInLocation_Bank8 },
	{ "LookForCardIDInHandList_Bank8", adapt_LookForCardIDInHandList_Bank8 },
	{ "LookForCardIDInHandAndPlayArea", adapt_LookForCardIDInHandAndPlayArea },
	{ "LookForCardIDToTradeWithDifferentHandCard", adapt_LookForCardIDToTradeWithDifferentHandCard },
	{ "LookForCardIDInDeck_GivenCardIDInHand", adapt_LookForCardIDInDeck_GivenCardIDInHand },
	{ "LookForCardIDInDeck_GivenCardIDInHandAndPlayArea", adapt_LookForCardIDInDeck_GivenCardIDInHandAndPlayArea },
	{ "AddStarterDeck", adapt_AddStarterDeck },
	{ "FindDuplicatePokemonCards", adapt_FindDuplicatePokemonCards },
	{ "AIPickEnergyCardToDiscard", adapt_AIPickEnergyCardToDiscard },
	{ "HandleAIAntiMewtwoDeckStrategy", adapt_HandleAIAntiMewtwoDeckStrategy },
	{ "OpenBoosterPack", adapt_OpenBoosterPack },
	{ "AICheckIfAttackIsHighRecoil", adapt_AICheckIfAttackIsHighRecoil },
	{ "ShowPromotionalCardScreen", adapt_ShowPromotionalCardScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_common */
