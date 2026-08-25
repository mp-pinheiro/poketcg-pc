#include "home/card_album.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetFirstOwnedCardIndex */
static void adapt_GetFirstOwnedCardIndex(ProbeState *s)
{
	GetFirstOwnedCardIndexResult r = GetFirstOwnedCardIndex();
	s->a = r.a;
	s->b = r.b;
	s->hl = r.hl;
}
/* <<< factory GetFirstOwnedCardIndex */

/* >>> factory PrintCardSetListEntries */
static void adapt_PrintCardSetListEntries(ProbeState *s)
{
	PrintCardSetListEntriesResult r = PrintCardSetListEntries();
	s->hl = r.hl;
}
/* <<< factory PrintCardSetListEntries */

const ProbeEntry probe_entries_card_album[] = {
	{ "GetFirstOwnedCardIndex", adapt_GetFirstOwnedCardIndex },
	{ "PrintCardSetListEntries", adapt_PrintCardSetListEntries },
	{ NULL, NULL },
};
