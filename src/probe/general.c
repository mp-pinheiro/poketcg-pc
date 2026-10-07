/* >>> part includes */
#include "home/general.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory AIProcessRetreat */
static void adapt_AIProcessRetreat(ProbeState *s)
{
	AIProcessRetreatResult result = AIProcessRetreat();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIProcessRetreat */

/* >>> factory AIMainTurnLogic */
static void adapt_AIMainTurnLogic(ProbeState *s)
{
	AIMainTurnLogicResult result = AIMainTurnLogic(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIMainTurnLogic */

/* >>> part probe_entries_general */
const ProbeEntry probe_entries_general[] = {
	{ "AIProcessRetreat", adapt_AIProcessRetreat },
	{ "AIMainTurnLogic", adapt_AIMainTurnLogic },
	{ NULL, NULL },
};
/* <<< part probe_entries_general */
