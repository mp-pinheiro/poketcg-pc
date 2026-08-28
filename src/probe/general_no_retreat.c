#include "home/general_no_retreat.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDoTurn_GeneralNoRetreat */
static void adapt_AIDoTurn_GeneralNoRetreat(ProbeState *s)
{
	AIDoTurn_GeneralNoRetreatResult r = AIDoTurn_GeneralNoRetreat(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = r.f;
}
/* <<< factory AIDoTurn_GeneralNoRetreat */

const ProbeEntry probe_entries_general_no_retreat[] = {
	{ "AIDoTurn_GeneralNoRetreat", adapt_AIDoTurn_GeneralNoRetreat },
	{ NULL, NULL },
};
