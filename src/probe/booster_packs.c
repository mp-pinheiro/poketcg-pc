#include "home/booster_packs.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetCurrentRarityAmount */
static void adapt_GetCurrentRarityAmount(ProbeState *s)
{
	RarityAmount r = GetCurrentRarityAmount();
	s->a = r.a;
	s->hl = r.hl;
}
/* <<< factory GetCurrentRarityAmount */

/* >>> factory GetBoosterCardType */
static void adapt_GetBoosterCardType(ProbeState *s)
{
	s->a = GetBoosterCardType(s->a);
}
/* <<< factory GetBoosterCardType */

/* >>> factory CalculateTypeChances */
static void adapt_CalculateTypeChances(ProbeState *s)
{
	s->a = CalculateTypeChances();
}
/* <<< factory CalculateTypeChances */

const ProbeEntry probe_entries_booster_packs[] = {
	{ "GetCurrentRarityAmount", adapt_GetCurrentRarityAmount },
	{ "GetBoosterCardType", adapt_GetBoosterCardType },
	{ "CalculateTypeChances", adapt_CalculateTypeChances },
	{ NULL, NULL },
};
