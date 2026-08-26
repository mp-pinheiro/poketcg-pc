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

/* >>> factory CreateCardSetList */
static void adapt_CreateCardSetList(ProbeState *s)
{
	CreateCardSetList(s->a);
	s->a = 0xFFu;
	s->f = 0x80u;
}
/* <<< factory CreateCardSetList */

const ProbeEntry probe_entries_card_album[] = {
	{ "GetFirstOwnedCardIndex", adapt_GetFirstOwnedCardIndex },
	{ "PrintCardSetListEntries", adapt_PrintCardSetListEntries },
	{ "CreateCardSetList", adapt_CreateCardSetList },
	{ NULL, NULL },
};
