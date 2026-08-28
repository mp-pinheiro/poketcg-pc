#include "home/general.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIProcessRetreat */
static void adapt_AIProcessRetreat(ProbeState *s)
{
	AIProcessRetreatResult result = AIProcessRetreat();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIProcessRetreat */

const ProbeEntry probe_entries_general[] = {
	{ "AIProcessRetreat", adapt_AIProcessRetreat },
	{ NULL, NULL },
};
