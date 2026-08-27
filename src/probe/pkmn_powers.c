#include "home/pkmn_powers.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory HandleAIShift */
static void adapt_HandleAIShift(ProbeState *s)
{
	AIShiftResult r = HandleAIShift(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIShift */

/* >>> factory HandleAIPeek */
static void adapt_HandleAIPeek(ProbeState *s)
{
	AIPeekResult r = HandleAIPeek(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIPeek */

/* >>> factory HandleAIStrangeBehavior */
static void adapt_HandleAIStrangeBehavior(ProbeState *s)
{
	HandleAIStrangeBehaviorResult r = HandleAIStrangeBehavior(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIStrangeBehavior */

/* >>> factory HandleAICurse */
static void adapt_HandleAICurse(ProbeState *s)
{
	HandleAICurseResult r = HandleAICurse(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAICurse */

/* >>> factory HandleAIDamageSwap */
static void adapt_HandleAIDamageSwap(ProbeState *s)
{
	HandleAIDamageSwapResult r = HandleAIDamageSwap(s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIDamageSwap */

/* >>> factory HandleAIHeal */
static void adapt_HandleAIHeal(ProbeState *s)
{
	HandleAIHealResult result = HandleAIHeal(s->c);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory HandleAIHeal */

/* >>> factory HandleAIPkmnPowers */
static void adapt_HandleAIPkmnPowers(ProbeState *s)
{
	HandleAIPkmnPowersResult r = HandleAIPkmnPowers();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIPkmnPowers */

const ProbeEntry probe_entries_pkmn_powers[] = {
	{ "HandleAIShift", adapt_HandleAIShift },
	{ "HandleAIPeek", adapt_HandleAIPeek },
	{ "HandleAIStrangeBehavior", adapt_HandleAIStrangeBehavior },
	{ "HandleAICurse", adapt_HandleAICurse },
	{ "HandleAIDamageSwap", adapt_HandleAIDamageSwap },
	{ "HandleAIHeal", adapt_HandleAIHeal },
	{ "HandleAIPkmnPowers", adapt_HandleAIPkmnPowers },
	{ NULL, NULL },
};
