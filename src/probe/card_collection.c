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

static void adapt_GetAmountOfCardsOwned(ProbeState *s)
{
	s->hl = GetAmountOfCardsOwned();
}

static void adapt_GetCardCountInCollectionAndDecks(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollectionAndDecks(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_GetCardCountInCollection(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollection(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_RemoveCardFromCollection(ProbeState *s)
{
	RemoveCardFromCollection(s->a);
}

const ProbeEntry probe_entries_card_collection[] = {
	{ "CreateTempCardCollection", adapt_CreateTempCardCollection },
	{ "AddCardToCollection", adapt_AddCardToCollection },
	{ "GetCardAlbumProgress", adapt_GetCardAlbumProgress },
	{ "GetAmountOfCardsOwned", adapt_GetAmountOfCardsOwned },
	{ "GetCardCountInCollectionAndDecks", adapt_GetCardCountInCollectionAndDecks },
	{ "GetCardCountInCollection", adapt_GetCardCountInCollection },
	{ "RemoveCardFromCollection", adapt_RemoveCardFromCollection },
	{ NULL, NULL },
};
