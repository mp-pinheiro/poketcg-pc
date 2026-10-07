/* >>> part includes */
#include "home/give_booster_pack.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _PauseMenu_Exit */
/* _PauseMenu_Exit is a bare ret: all registers are preserved. */
static void adapt_PauseMenu_Exit(ProbeState *s)
{
	(void)s;
	_PauseMenu_Exit();
}
/* <<< factory _PauseMenu_Exit */

/* >>> factory GiveBoosterPack */
static void adapt_GiveBoosterPack(ProbeState *s)
{
	GiveBoosterPackResult result = GiveBoosterPack(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory GiveBoosterPack */

/* >>> part probe_entries_give_booster_pack */
const ProbeEntry probe_entries_give_booster_pack[] = {
	{ "_PauseMenu_Exit", adapt_PauseMenu_Exit },
	{ "GiveBoosterPack", adapt_GiveBoosterPack },
	{ NULL, NULL },
};
/* <<< part probe_entries_give_booster_pack */
