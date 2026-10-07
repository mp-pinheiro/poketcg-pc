/* >>> part includes */
#include "home/duel_init.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Duel_Init */
static void adapt_Duel_Init(ProbeState *s)
{
	DuelInitResult result = Duel_Init(s->f);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Duel_Init */

/* >>> part probe_entries_duel_init */
const ProbeEntry probe_entries_duel_init[] = {
	{ "Duel_Init", adapt_Duel_Init },
	{ NULL, NULL },
};
/* <<< part probe_entries_duel_init */
