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
