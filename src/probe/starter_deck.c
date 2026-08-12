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

const ProbeEntry probe_entries_starter_deck[] = {
	{ "CopyDeckNameAndCards", adapt_CopyDeckNameAndCards },
	{ NULL, NULL },
};
