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

const ProbeEntry probe_entries_common[] = {
	{ "CountOppEnergyCardsInHand", adapt_CountOppEnergyCardsInHand },
	{ "ConvertHPToDamageCounters_Bank8", adapt_ConvertHPToDamageCounters_Bank8 },
	{ "CalculateWordTensDigit", adapt_CalculateWordTensDigit },
	{ "PickTwoAttachedEnergyCards", adapt_PickTwoAttachedEnergyCards },
	{ "ClearMemory_Bank8", adapt_ClearMemory_Bank8 },
	{ "PickAttachedEnergyCardToRemove", adapt_PickAttachedEnergyCardToRemove },
	{ "CopyListWithFFTerminatorFromHLToDE_Bank8", adapt_CopyListWithFFTerminatorFromHLToDE_Bank8 },
	{ "LookForCardIDInPlayArea_Bank8", adapt_LookForCardIDInPlayArea_Bank8 },
	{ NULL, NULL },
};
