#include "home/npc_core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory CheckIfNPCIsRonald */
static void adapt_CheckIfNPCIsRonald(ProbeState *s)
{
	s->f = CheckIfNPCIsRonald(s->a);
}
/* <<< factory CheckIfNPCIsRonald */

/* >>> factory UpdateNPCAnimation */
static void adapt_UpdateNPCAnimation(ProbeState *s)
{
	s->a = UpdateNPCAnimation();
}
/* <<< factory UpdateNPCAnimation */

/* >>> factory ApplyRandomCountToNPCAnim */
static void adapt_ApplyRandomCountToNPCAnim(ProbeState *s)
{
	s->a = ApplyRandomCountToNPCAnim();
}
/* <<< factory ApplyRandomCountToNPCAnim */

const ProbeEntry probe_entries_npc_core[] = {
	{ "CheckIfNPCIsRonald", adapt_CheckIfNPCIsRonald },
	{ "UpdateNPCAnimation", adapt_UpdateNPCAnimation },
	{ "ApplyRandomCountToNPCAnim", adapt_ApplyRandomCountToNPCAnim },
	{ NULL, NULL },
};
