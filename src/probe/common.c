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

const ProbeEntry probe_entries_common[] = {
	{ "CountOppEnergyCardsInHand", adapt_CountOppEnergyCardsInHand },
	{ "ConvertHPToDamageCounters_Bank8", adapt_ConvertHPToDamageCounters_Bank8 },
	{ "CalculateWordTensDigit", adapt_CalculateWordTensDigit },
	{ NULL, NULL },
};
