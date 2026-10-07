#include "home/card_collection.h"
#include "probe.h"

static void adapt_CreateTempCardCollection(ProbeState *s)
{
	(void)s;
	CreateTempCardCollection();
}
static void adapt_AddCardToCollection(ProbeState *s)
{
	AddCardToCollection((CardId)(((uint16_t)s->d << 8) | s->e));
}

static void adapt_GetCardAlbumProgress(ProbeState *s)
{
	AlbumProgress p = GetCardAlbumProgress();
	s->b = p.b;
	s->c = p.c;
	s->d = p.d;
	s->e = p.e;
}

static void adapt_GetAmountOfCardsOwned(ProbeState *s)
{
	s->hl = GetAmountOfCardsOwned();
}

static void adapt_GetCardCountInCollectionAndDecks(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollectionAndDecks(
		(CardId)(((uint16_t)s->d << 8) | s->e));
	s->a = r.a;
	s->f = r.f;
}

static void adapt_GetCardCountInCollection(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollection(
		(CardId)(((uint16_t)s->d << 8) | s->e));
	s->a = r.a;
	s->f = r.f;
}

static void adapt_RemoveCardFromCollection(ProbeState *s)
{
	RemoveCardFromCollection((CardId)(((uint16_t)s->d << 8) | s->e));
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
