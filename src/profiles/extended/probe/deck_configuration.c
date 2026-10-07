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
const ProbeEntry probe_entries_deck_configuration[] = {
	{ "PrintSlashSixty", adapt_PrintSlashSixty },
	{ "DecrementDeckCardsInCollection", adapt_DecrementDeckCardsInCollection },
	{ "AddDeckToCollection", adapt_AddDeckToCollection },
	{ "CopyListFromHLToDE", adapt_CopyListFromHLToDE },
	{ "InitCardSelectionParams", adapt_InitCardSelectionParams },
	{ "CalculateOnesAndTensDigits", adapt_CalculateOnesAndTensDigits },
	{ "CalculateOnesAndTensDigits_Long", adapt_CalculateOnesAndTensDigits_Long },
	{ "ClearMemory_Bank2", adapt_ClearMemory_Bank2 },
	{ "CheckIfHasOtherValidDecks", adapt_CheckIfHasOtherValidDecks },
	{ "FillDEWithA", adapt_FillDEWithA },
	{ "DrawHandCardsTileAtDE", adapt_DrawHandCardsTileAtDE },
	{ "CountNumberOfCardsOfType", adapt_CountNumberOfCardsOfType },
	{ "CopyNBytesFromHLToDE", adapt_CopyNBytesFromHLToDE },
	{ "CopyNBytesFromHLToDE_Long", adapt_CopyNBytesFromHLToDE_Long },
	{ "IncrementDeckCardsInTempCollection", adapt_IncrementDeckCardsInTempCollection },
	{ "CreateCardCollectionListWithDeckCards", adapt_CreateCardCollectionListWithDeckCards },
	{ "GetSelectedVisibleCardID", adapt_GetSelectedVisibleCardID },
	{ "CheckIfDeckHasCards", adapt_CheckIfDeckHasCards },
	{ "FillBGMapLineWithA", adapt_FillBGMapLineWithA },
	{ "OpenDeckConfigurationMenu", adapt_OpenDeckConfigurationMenu },
	{ "PrintTotalNumberOfCardsInCollection", adapt_PrintTotalNumberOfCardsInCollection },
	{ "DrawHorizontalListCursor", adapt_DrawHorizontalListCursor },
	{ "GetCountOfCardInCurDeck", adapt_GetCountOfCardInCurDeck },
	{ "DrawListCursor", adapt_DrawListCursor },
	{ "DrawHorizontalListCursor_Invisible", adapt_DrawHorizontalListCursor_Invisible },
	{ "DrawHorizontalListCursor_Visible", adapt_DrawHorizontalListCursor_Visible },
	{ "IsCardInAnyDeck", adapt_IsCardInAnyDeck },
	{ "DrawListCursor_Invisible", adapt_DrawListCursor_Invisible },
	{ "DrawListCursor_Visible", adapt_DrawListCursor_Visible },
	{ "CountNumberOfCardsForEachCardType", adapt_CountNumberOfCardsForEachCardType },
	{ "CopyDeckName", adapt_CopyDeckName },
	{ "GetOwnedCardCount", adapt_GetOwnedCardCount },
	{ "TallyCardsInCardFilterLists", adapt_TallyCardsInCardFilterLists },
	{ "RemoveCardFromDeck", adapt_RemoveCardFromDeck },
	{ "CheckIfCurrentDeckWasChanged", adapt_CheckIfCurrentDeckWasChanged },
	{ "CreateFilteredCardList", adapt_CreateFilteredCardList },
	{ "ConfirmSelectionAndReturnCarry", adapt_ConfirmSelectionAndReturnCarry },
	{ "AddCardIDToVisibleList", adapt_AddCardIDToVisibleList },
	{ "HandleCardSelectionCursorBlink", adapt_HandleCardSelectionCursorBlink },
	{ "DrawHandCardsTileOnCurDeck", adapt_DrawHandCardsTileOnCurDeck },
	{ "HandleCardSelectionInput", adapt_HandleCardSelectionInput },
	{ "HandleLeftRightInCardList", adapt_HandleLeftRightInCardList },
	{ "PrintPlayersCardsText", adapt_PrintPlayersCardsText },
	{ "ConvertToNumericalDigits", adapt_ConvertToNumericalDigits },
	{ "CopyListFromHLToDEInSRAM", adapt_CopyListFromHLToDEInSRAM },
	{ "PrintDeckName", adapt_PrintDeckName },
	{ "AppendOwnedCardCountNumber", adapt_AppendOwnedCardCountNumber },
	{ "PrintNumberValueInCursorYPos", adapt_PrintNumberValueInCursorYPos },
	{ "AppendOwnedCardCountAndStorageCountNumbers", adapt_AppendOwnedCardCountAndStorageCountNumbers },
	{ "PrintCardTypeCounts", adapt_PrintCardTypeCounts },
	{ "AppendDeckName", adapt_AppendDeckName },
	{ "DrawDecksScreen", adapt_DrawDecksScreen },
	{ "PrintTotalCardCount", adapt_PrintTotalCardCount },
	{ "RemoveCardFromDeckAndUpdateCount", adapt_RemoveCardFromDeckAndUpdateCount },
	{ "PrintCardSelectionList", adapt_PrintCardSelectionList },
	{ "PrintFilteredCardSelectionList", adapt_PrintFilteredCardSelectionList },
	{ "PrintDeckBuildingCardList", adapt_PrintDeckBuildingCardList },
	{ "PrintFilteredCardList", adapt_PrintFilteredCardList },
	{ "OpenCardPageFromCardList", adapt_OpenCardPageFromCardList },
	{ "CheckIfThereAreAnyBasicCardsInDeck", adapt_CheckIfThereAreAnyBasicCardsInDeck },
	{ "SortCurDeckCardsByID", adapt_SortCurDeckCardsByID },
	{ "GetCardTypeIconPalette", adapt_GetCardTypeIconPalette },
	{ "DrawCardTypeIcons", adapt_DrawCardTypeIcons },
	{ "PrintPlayersCardsHeaderInfo", adapt_PrintPlayersCardsHeaderInfo },
	{ "PrintConfirmationCardList", adapt_PrintConfirmationCardList },
	{ "CreateCurDeckUniqueCardList", adapt_CreateCurDeckUniqueCardList },
	{ "TryAddCardToDeck", adapt_TryAddCardToDeck },
	{ "AddCardToDeckAndUpdateCount", adapt_AddCardToDeckAndUpdateCount },
	{ "HandleDeckCardSelectionList", adapt_HandleDeckCardSelectionList },
	{ "PrintCurDeckNumberAndName", adapt_PrintCurDeckNumberAndName },
	{ "UpdateConfirmationCardScreen", adapt_UpdateConfirmationCardScreen },
	{ "ShowDeckInfoHeader", adapt_ShowDeckInfoHeader },
	{ "DrawCardTypeIconsAndPrintCardCounts", adapt_DrawCardTypeIconsAndPrintCardCounts },
	{ "ShowDeckInfoHeaderAndWaitForBButton", adapt_ShowDeckInfoHeaderAndWaitForBButton },
	{ "HandleDeckConfirmationMenu", adapt_HandleDeckConfirmationMenu },
	{ "ConfirmDeckConfiguration", adapt_ConfirmDeckConfiguration },
	{ "ShowConfirmationCardScreen", adapt_ShowConfirmationCardScreen },
	{ "SaveDeckConfiguration", adapt_SaveDeckConfiguration },
	{ "DismantleDeck", adapt_DismantleDeck },
	{ "CancelDeckModifications", adapt_CancelDeckModifications },
	{ "HandleSelectUpAndDownInList", adapt_HandleSelectUpAndDownInList },
	{ "HandleDeckBuildScreen", adapt_HandleDeckBuildScreen },
	{ "HandlePlayersCardsScreen", adapt_HandlePlayersCardsScreen },
	{ "ChangeDeckName", adapt_ChangeDeckName },
	{ "HandleDeckConfigurationMenu", adapt_HandleDeckConfigurationMenu },
	{ "ModifyDeckConfiguration", adapt_ModifyDeckConfiguration },
	{ NULL, NULL },
};
/* <<< part probe_entries_deck_configuration */
