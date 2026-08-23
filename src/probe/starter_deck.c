#include "home/starter_deck.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory CopyDeckNameAndCards */
static void adapt_CopyDeckNameAndCards(ProbeState *s)
{
	CopyDeckNameAndCards(s->a, s->hl);
}
/* <<< factory CopyDeckNameAndCards */

/* >>> factory InitSaveData */
static void adapt_InitSaveData(ProbeState *s)
{
	(void)s;
	InitSaveData();
}
/* <<< factory InitSaveData */

const ProbeEntry probe_entries_starter_deck[] = {
	{ "CopyDeckNameAndCards", adapt_CopyDeckNameAndCards },
	{ "InitSaveData", adapt_InitSaveData },
	{ NULL, NULL },
};
