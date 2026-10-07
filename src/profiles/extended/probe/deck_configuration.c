/* === factory CalculateOnesAndTensDigits */
/* >>> factory CalculateOnesAndTensDigits_Long */
static void adapt_CalculateOnesAndTensDigits_Long(ProbeState *s)
{
	CalculateOnesAndTensDigits_Long(s->hl);
}
/* <<< factory CalculateOnesAndTensDigits_Long */
/* === factory CopyNBytesFromHLToDE */
/* >>> factory CopyNBytesFromHLToDE_Long */
static void adapt_CopyNBytesFromHLToDE_Long(ProbeState *s)
{
	uint16_t hl = s->hl;
	uint16_t de = (uint16_t)(((uint16_t)s->d << 8) | s->e);
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8) | s->c);
	CopyNBytesFromHLToDELongResult r =
		CopyNBytesFromHLToDE_Long(&hl, &de, bc);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CopyNBytesFromHLToDE_Long */
/* >>> factory GetSelectedVisibleCardID */
static void adapt_GetSelectedVisibleCardID(ProbeState *s)
{
	GetSelectedVisibleCardIDResult result = GetSelectedVisibleCardID();
	s->a = result.a;
	s->f = result.f;
	s->d = (uint8_t)(result.id >> 8);
	s->e = (uint8_t)result.id;
	s->hl = result.hl;
}
/* <<< factory GetSelectedVisibleCardID */
/* >>> factory GetCountOfCardInCurDeck */
static void adapt_GetCountOfCardInCurDeck(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	GetCountOfCardInCurDeckResult r = GetCountOfCardInCurDeck(id);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory GetCountOfCardInCurDeck */
/* >>> factory IsCardInAnyDeck */
static void adapt_IsCardInAnyDeck(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	IsCardInAnyDeckResult r = IsCardInAnyDeck(s->a, s->f, id);
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory IsCardInAnyDeck */
/* >>> factory GetOwnedCardCount */
static void adapt_GetOwnedCardCount(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	GetOwnedCardCountResult r = GetOwnedCardCount(id);
	s->a = r.a;
	s->d = r.d;
}
/* <<< factory GetOwnedCardCount */
/* >>> factory AddCardIDToVisibleList */
static void adapt_AddCardIDToVisibleList(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	AddCardIDToVisibleList(s->b, id);
}
/* <<< factory AddCardIDToVisibleList */
/* --- factory AddGiftCenterDeckCardsToCollection */
/* --- factory Func_9ced */
/* >>> factory TryAddCardToDeck */
static void adapt_TryAddCardToDeck(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	TryAddCardToDeckResult r = TryAddCardToDeck(id);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TryAddCardToDeck */
/* >>> factory AddCardToDeckAndUpdateCount */
static void adapt_AddCardToDeckAndUpdateCount(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	AddCardToDeckAndUpdateCountResult r = AddCardToDeckAndUpdateCount(id);
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
}
/* <<< factory AddCardToDeckAndUpdateCount */
/* --- factory HandleSendDeckConfigurationMenu */
/* --- factory PrepareToBuildDeckConfigurationToSend */
/* >>> part probe_entries_deck_configuration */
	{ "CalculateOnesAndTensDigits_Long", adapt_CalculateOnesAndTensDigits_Long },
	{ "CopyNBytesFromHLToDE_Long", adapt_CopyNBytesFromHLToDE_Long },
/* <<< part probe_entries_deck_configuration */
