/* >>> part includes */
#include "home/card_collection.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory CreateTempCardCollection */
static void adapt_CreateTempCardCollection(ProbeState *s)
{
	(void)s;
	CreateTempCardCollection();
}
/* <<< factory CreateTempCardCollection */
/* >>> factory AddCardToCollection */
static void adapt_AddCardToCollection(ProbeState *s)
{
	AddCardToCollection((CardId)(((uint16_t)s->d << 8) | s->e));
}
/* <<< factory AddCardToCollection */

/* >>> factory GetCardAlbumProgress */
static void adapt_GetCardAlbumProgress(ProbeState *s)
{
	AlbumProgress p = GetCardAlbumProgress();
	s->b = p.b;
	s->c = p.c;
	s->d = p.d;
	s->e = p.e;
}
/* <<< factory GetCardAlbumProgress */

/* >>> factory GetAmountOfCardsOwned */
static void adapt_GetAmountOfCardsOwned(ProbeState *s)
{
	s->hl = GetAmountOfCardsOwned();
}
/* <<< factory GetAmountOfCardsOwned */

/* >>> factory GetCardCountInCollectionAndDecks */
static void adapt_GetCardCountInCollectionAndDecks(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollectionAndDecks(
		(CardId)(((uint16_t)s->d << 8) | s->e));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory GetCardCountInCollectionAndDecks */

/* >>> factory GetCardCountInCollection */
static void adapt_GetCardCountInCollection(ProbeState *s)
{
	CardCountResult r = GetCardCountInCollection(
		(CardId)(((uint16_t)s->d << 8) | s->e));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory GetCardCountInCollection */

/* >>> factory RemoveCardFromCollection */
static void adapt_RemoveCardFromCollection(ProbeState *s)
{
	RemoveCardFromCollection((CardId)(((uint16_t)s->d << 8) | s->e));
}
/* <<< factory RemoveCardFromCollection */

/* >>> part probe_entries_card_collection */
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
/* <<< part probe_entries_card_collection */
