#include "home/auto_deck_machines.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ReadAutoDeckConfiguration */
static void adapt_ReadAutoDeckConfiguration(ProbeState *s)
{
	(void)s;
	ReadAutoDeckConfiguration();
}
/* <<< factory ReadAutoDeckConfiguration */

/* >>> factory CheckWhichDecksToDismantleToBuildSavedDeck */
static void adapt_CheckWhichDecksToDismantleToBuildSavedDeck(ProbeState *s)
{
	CheckWhichDecksToDismantleToBuildSavedDeckResult r = CheckWhichDecksToDismantleToBuildSavedDeck();
	s->a = r.a; s->f = r.f;
}
/* <<< factory CheckWhichDecksToDismantleToBuildSavedDeck */

const ProbeEntry probe_entries_auto_deck_machines[] = {
	{ "ReadAutoDeckConfiguration", adapt_ReadAutoDeckConfiguration },
	{ "CheckWhichDecksToDismantleToBuildSavedDeck", adapt_CheckWhichDecksToDismantleToBuildSavedDeck },
	{ NULL, NULL },
};
