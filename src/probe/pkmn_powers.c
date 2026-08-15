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

const ProbeEntry probe_entries_pkmn_powers[] = {
	{ "HandleAIShift", adapt_HandleAIShift },
	{ NULL, NULL },
};
