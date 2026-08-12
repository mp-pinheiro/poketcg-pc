#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory SetLineSeparation */
static void adapt_SetLineSeparation(ProbeState *s)
{
	SetLineSeparation(s->a);
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
static void adapt_PlayAreaScreenMenuFunction(ProbeState *s)
{
	s->f = PlayAreaScreenMenuFunction();
}
/* <<< factory PlayAreaScreenMenuFunction */

/* >>> factory SwitchAttackPage */
static void adapt_SwitchAttackPage(ProbeState *s)
{
	(void)s;
	SwitchAttackPage();
}
/* <<< factory SwitchAttackPage */

const ProbeEntry probe_entries_core[] = {
	{ "SetLineSeparation", adapt_SetLineSeparation },
	{ "PlayAreaScreenMenuFunction", adapt_PlayAreaScreenMenuFunction },
	{ "SwitchAttackPage", adapt_SwitchAttackPage },
	{ NULL, NULL },
};
