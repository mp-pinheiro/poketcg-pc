#include "home/card_collection.h"
#include "probe.h"

static void adapt_CreateTempCardCollection(ProbeState *s)
{
	(void)s;
	CreateTempCardCollection();
}

static void adapt_AddCardToCollection(ProbeState *s)
{
	AddCardToCollection(s->a);
}

static void adapt_GetCardAlbumProgress(ProbeState *s)
{
	AlbumProgress p = GetCardAlbumProgress();
	s->d = p.d;
	s->e = p.e;
}

const ProbeEntry probe_entries_card_collection[] = {
	{ "CreateTempCardCollection", adapt_CreateTempCardCollection },
	{ "AddCardToCollection", adapt_AddCardToCollection },
	{ "GetCardAlbumProgress", adapt_GetCardAlbumProgress },
	{ NULL, NULL },
};
