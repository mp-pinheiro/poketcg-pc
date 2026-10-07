/* >>> part includes */
#include "home/starter_deck.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory InitSaveData */
static void adapt_InitSaveData(ProbeState *s)
{
	(void)s;
	InitSaveData();
}
/* <<< factory InitSaveData */

/* >>> factory _AddStarterDeck */
static void adapt__AddStarterDeck(ProbeState *s)
{
	_AddStarterDeck(s->a);
}
/* <<< factory _AddStarterDeck */

/* >>> part probe_entries_starter_deck */
const ProbeEntry probe_entries_starter_deck[] = {
	{ "InitSaveData", adapt_InitSaveData },
	{ "_AddStarterDeck", adapt__AddStarterDeck },
	{ NULL, NULL },
};
/* <<< part probe_entries_starter_deck */
