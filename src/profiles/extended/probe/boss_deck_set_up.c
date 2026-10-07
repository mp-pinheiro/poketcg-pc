/* >>> part includes */
#include "home/boss_deck_set_up.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetUpBossStartingHandAndDeck */
static void adapt_SetUpBossStartingHandAndDeck(ProbeState *s)
{
	(void)s;
	SetUpBossStartingHandAndDeck();
}
/* <<< factory SetUpBossStartingHandAndDeck */

/* >>> part probe_entries_boss_deck_set_up */
const ProbeEntry probe_entries_boss_deck_set_up[] = {
	{ "SetUpBossStartingHandAndDeck", adapt_SetUpBossStartingHandAndDeck },
	{ NULL, NULL },
};
/* <<< part probe_entries_boss_deck_set_up */
