#include "home/effect_functions.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"




/* >>> factory UpdateExpectedAIDamage */
static void adapt_UpdateExpectedAIDamage(ProbeState *s)
{
	UpdateExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage */


/* >>> factory SetExpectedAIDamage */
static void adapt_SetExpectedAIDamage(ProbeState *s)
{
	SetExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory SetExpectedAIDamage */


const ProbeEntry probe_entries_effect_functions[] = {
	{ "UpdateExpectedAIDamage", adapt_UpdateExpectedAIDamage },
	{ "SetExpectedAIDamage", adapt_SetExpectedAIDamage },
	{ NULL, NULL },
};
