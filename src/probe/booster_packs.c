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

/* >>> factory UpdateBoosterCardTypesChanceByte */
static void adapt_UpdateBoosterCardTypesChanceByte(ProbeState *s)
{
	s->a = UpdateBoosterCardTypesChanceByte();
}
/* <<< factory UpdateBoosterCardTypesChanceByte */

/* >>> factory AppendCurrentCardToHL */
static void adapt_AppendCurrentCardToHL(ProbeState *s)
{
	AppendCurrentCardToHL(&s->hl);
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory AppendCurrentCardToHL */

const ProbeEntry probe_entries_booster_packs[] = {
	{ "GetCurrentRarityAmount", adapt_GetCurrentRarityAmount },
	{ "GetBoosterCardType", adapt_GetBoosterCardType },
	{ "CalculateTypeChances", adapt_CalculateTypeChances },
	{ "UpdateBoosterCardTypesChanceByte", adapt_UpdateBoosterCardTypesChanceByte },
	{ "AppendCurrentCardToHL", adapt_AppendCurrentCardToHL },
	{ NULL, NULL },
};
