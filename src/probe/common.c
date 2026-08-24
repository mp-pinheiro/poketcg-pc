#include "home/common.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory CountOppEnergyCardsInHand */
static void adapt_CountOppEnergyCardsInHand(ProbeState *s)
{
	CountOppEnergyResult r = CountOppEnergyCardsInHand(s->a, s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
}
/* <<< factory CountOppEnergyCardsInHand */

/* >>> factory ConvertHPToDamageCounters_Bank8 */
static void adapt_ConvertHPToDamageCounters_Bank8(ProbeState *s)
{
	s->a = ConvertHPToDamageCounters_Bank8(s->a);
}
/* <<< factory ConvertHPToDamageCounters_Bank8 */

/* >>> factory CalculateWordTensDigit */
static void adapt_CalculateWordTensDigit(ProbeState *s)
{
	s->hl = CalculateWordTensDigit(s->hl);
}
/* <<< factory CalculateWordTensDigit */

/* >>> factory PickTwoAttachedEnergyCards */
static void adapt_PickTwoAttachedEnergyCards(ProbeState *s)
{
	PickTwoResult r = PickTwoAttachedEnergyCards(s->a);
	s->a = r.a;
	if (r.b_valid)
		s->b = r.b;
}
/* <<< factory PickTwoAttachedEnergyCards */

/* >>> factory ClearMemory_Bank8 */
static void adapt_ClearMemory_Bank8(ProbeState *s)
{
	ClearMemory_Bank8(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank8 */

/* >>> factory PickAttachedEnergyCardToRemove */
static void adapt_PickAttachedEnergyCardToRemove(ProbeState *s)
{
	s->a = PickAttachedEnergyCardToRemove(s->a);
}
/* <<< factory PickAttachedEnergyCardToRemove */

/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
static void adapt_CopyListWithFFTerminatorFromHLToDE_Bank8(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyListBank8Result r = CopyListWithFFTerminatorFromHLToDE_Bank8(&s->hl, &de);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank8 */

/* >>> factory LookForCardIDInPlayArea_Bank8 */
static void adapt_LookForCardIDInPlayArea_Bank8(ProbeState *s)
{
	LookForCardIDInPlayAreaResult r = LookForCardIDInPlayArea_Bank8(s->a, s->b);
	s->a = r.a;
	s->b = r.b;
	s->f = r.f;
}
/* <<< factory LookForCardIDInPlayArea_Bank8 */

/* >>> factory CheckIfHasCardIDInHand */
static void adapt_CheckIfHasCardIDInHand(ProbeState *s)
{
	CheckIfHasCardIDInHandResult r = CheckIfHasCardIDInHand(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasCardIDInHand */

/* >>> factory FindBasicEnergyCardsInLocation */
static void adapt_FindBasicEnergyCardsInLocation(ProbeState *s)
{
	FindBasicEnergyCardsInLocationResult r = FindBasicEnergyCardsInLocation(s->a);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FindBasicEnergyCardsInLocation */

/* >>> factory CalculateBDividedByA_Bank8 */
static void adapt_CalculateBDividedByA_Bank8(ProbeState *s)
{
	CalculateBDividedByA_Bank8Result r = CalculateBDividedByA_Bank8(s->a, s->b);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CalculateBDividedByA_Bank8 */

/* >>> factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
static void adapt_CheckIfPlayerHasPokemonOtherThanMewtwoLv53(ProbeState *s)
{
	CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result r = CheckIfPlayerHasPokemonOtherThanMewtwoLv53(s->b, s->c, s->d, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */

/* >>> factory RemoveFromListDifferentCardOfGivenType */
static void adapt_RemoveFromListDifferentCardOfGivenType(ProbeState *s)
{
	RemoveFromListDifferentCardOfGivenTypeResult r =
		RemoveFromListDifferentCardOfGivenType(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory RemoveFromListDifferentCardOfGivenType */

/* >>> factory CountPokemonCardsInHandAndInPlayArea */
static void adapt_CountPokemonCardsInHandAndInPlayArea(ProbeState *s)
{
	s->a = CountPokemonCardsInHandAndInPlayArea(s->c);
}
/* <<< factory CountPokemonCardsInHandAndInPlayArea */

/* >>> factory LookForCardIDInLocation_Bank8 */
static void adapt_LookForCardIDInLocation_Bank8(ProbeState *s)
{
	LookForCardIDInLocationBank8Result r = LookForCardIDInLocation_Bank8(s->a, s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInLocation_Bank8 */

/* >>> factory LookForCardIDInHandList_Bank8 */
static void adapt_LookForCardIDInHandList_Bank8(ProbeState *s)
{
	LookForCardIDInHandListResult r = LookForCardIDInHandList_Bank8(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHandList_Bank8 */

/* >>> factory LookForCardIDInHandAndPlayArea */
static void adapt_LookForCardIDInHandAndPlayArea(ProbeState *s)
{
	LookForCardIDInHandAndPlayAreaResult r = LookForCardIDInHandAndPlayArea(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHandAndPlayArea */

/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
static void adapt_LookForCardIDToTradeWithDifferentHandCard(ProbeState *s)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(s->a, s->e);
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
}
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */

/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
static void adapt_LookForCardIDInDeck_GivenCardIDInHand(ProbeState *s)
{
	LookForCardIDInDeck_GivenCardIDInHandResult r = LookForCardIDInDeck_GivenCardIDInHand(s->a, s->b);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */

/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
static void adapt_LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ProbeState *s)
{
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(s->a, s->b);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */

/* >>> factory AddStarterDeck */
static void adapt_AddStarterDeck(ProbeState *s)
{
	AddStarterDeck(s->a);
}
/* <<< factory AddStarterDeck */

/* >>> factory FindDuplicatePokemonCards */
static void adapt_FindDuplicatePokemonCards(ProbeState *s)
{
	FindDuplicatePokemonCardsResult r = FindDuplicatePokemonCards();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FindDuplicatePokemonCards */

/* >>> factory AIPickEnergyCardToDiscard */
static void adapt_AIPickEnergyCardToDiscard(ProbeState *s)
{
	s->a = AIPickEnergyCardToDiscard(s->a);
}
/* <<< factory AIPickEnergyCardToDiscard */

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
	{ NULL, NULL },
};
