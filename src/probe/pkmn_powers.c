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

const ProbeEntry probe_entries_pkmn_powers[] = {
	{ "HandleAIShift", adapt_HandleAIShift },
	{ "HandleAIPeek", adapt_HandleAIPeek },
	{ "HandleAIStrangeBehavior", adapt_HandleAIStrangeBehavior },
	{ NULL, NULL },
};
