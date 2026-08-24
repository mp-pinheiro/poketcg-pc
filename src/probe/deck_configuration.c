#include "home/deck_configuration.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DecrementDeckCardsInCollection */
static void adapt_DecrementDeckCardsInCollection(ProbeState *s)
{
	s->hl = DecrementDeckCardsInCollection(s->hl);
}
/* <<< factory DecrementDeckCardsInCollection */


/* >>> factory AddDeckToCollection */
static void adapt_AddDeckToCollection(ProbeState *s)
{
	s->hl = AddDeckToCollection(s->hl);
}
/* <<< factory AddDeckToCollection */


/* >>> factory CopyListFromHLToDE */
static void adapt_CopyListFromHLToDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyListFromHLToDE(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyListFromHLToDE */


/* >>> factory CalculateOnesAndTensDigits */
static void adapt_CalculateOnesAndTensDigits(ProbeState *s)
{
	CalculateOnesAndTensDigits(s->a);
}
/* <<< factory CalculateOnesAndTensDigits */




/* >>> factory InitCardSelectionParams */
static void adapt_InitCardSelectionParams(ProbeState *s)
{
	s->a = InitCardSelectionParams(s->a, &s->hl);
}
/* <<< factory InitCardSelectionParams */


/* >>> factory ClearMemory_Bank2 */
static void adapt_ClearMemory_Bank2(ProbeState *s)
{
	ClearMemory_Bank2(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank2 */

/* >>> factory CheckIfHasOtherValidDecks */
static void adapt_CheckIfHasOtherValidDecks(ProbeState *s)
{
	s->f = CheckIfHasOtherValidDecks();
}
/* <<< factory CheckIfHasOtherValidDecks */

/* >>> factory FillDEWithA */
static void adapt_FillDEWithA(ProbeState *s)
{
	FillDEWithA(s->a, s->b, (uint16_t)(s->d << 8 | s->e));
	s->b = 0;
	s->f = (uint8_t)(0xC0u | (s->f & 0x10u));
}
/* <<< factory FillDEWithA */

/* >>> factory DrawHandCardsTileAtDE */
static void adapt_DrawHandCardsTileAtDE(ProbeState *s)
{
	DrawHandCardsTileAtDE((uint16_t)((uint16_t)s->d << 8 | s->e));
}
/* <<< factory DrawHandCardsTileAtDE */

/* >>> factory CountNumberOfCardsOfType */
static void adapt_CountNumberOfCardsOfType(ProbeState *s)
{
	uint8_t input_type = s->a;
	s->a = CountNumberOfCardsOfType(input_type);
	s->b = input_type;
	s->c = s->a;
}
/* <<< factory CountNumberOfCardsOfType */

/* >>> factory CopyNBytesFromHLToDE */
static void adapt_CopyNBytesFromHLToDE(ProbeState *s)
{
	uint16_t hl = s->hl;
	uint16_t de = (uint16_t)(((uint16_t)s->d << 8) | s->e);
	CopyNBytesFromHLToDE(&hl, &de, s->b);
	s->hl = hl;
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyNBytesFromHLToDE */

/* >>> factory IncrementDeckCardsInTempCollection */
static void adapt_IncrementDeckCardsInTempCollection(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	IncrementDeckCardsInTempCollection(de);
}
/* <<< factory IncrementDeckCardsInTempCollection */

/* >>> factory CreateCardCollectionListWithDeckCards */
static void adapt_CreateCardCollectionListWithDeckCards(ProbeState *s)
{
	CreateCardCollectionListWithDeckCards(s->a);
}
/* <<< factory CreateCardCollectionListWithDeckCards */

/* >>> factory GetSelectedVisibleCardID */
static void adapt_GetSelectedVisibleCardID(ProbeState *s)
{
	uint8_t cursor = gb_read8(wCardListCursorPos_ADDR);
	uint16_t hl = (uint16_t)(wVisibleListCardIDs_ADDR + cursor);
	uint8_t z = (uint8_t)(s->f & 0x80u);
	s->e = GetSelectedVisibleCardID();
	s->a = cursor;
	s->d = 0;
	s->hl = hl;
	s->f = z;
}
/* <<< factory GetSelectedVisibleCardID */

/* >>> factory CheckIfDeckHasCards */
static void adapt_CheckIfDeckHasCards(ProbeState *s)
{
	s->f = CheckIfDeckHasCards(s->hl);
}
/* <<< factory CheckIfDeckHasCards */

/* >>> factory FillBGMapLineWithA */
static void adapt_FillBGMapLineWithA(ProbeState *s)
{
	FillBGMapLineWithA(s->a, s->b, s->c);
}
/* <<< factory FillBGMapLineWithA */

/* >>> factory OpenDeckConfigurationMenu */
static void adapt_OpenDeckConfigurationMenu(ProbeState *s)
{
	OpenDeckConfigurationMenu();
	(void)s;
}
/* <<< factory OpenDeckConfigurationMenu */

/* >>> factory PrintTotalNumberOfCardsInCollection */
static void adapt_PrintTotalNumberOfCardsInCollection(ProbeState *s)
{
	PrintTotalNumberOfCardsInCollection();
	(void)s;
}
/* <<< factory PrintTotalNumberOfCardsInCollection */

/* >>> factory DrawHorizontalListCursor */
static void adapt_DrawHorizontalListCursor(ProbeState *s)
{
	DrawHorizontalListCursorResult result = DrawHorizontalListCursor(s->a);
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawHorizontalListCursor */

/* >>> factory GetCountOfCardInCurDeck */
static void adapt_GetCountOfCardInCurDeck(ProbeState *s)
{
	GetCountOfCardInCurDeckResult r = GetCountOfCardInCurDeck(s->e);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory GetCountOfCardInCurDeck */

/* >>> factory DrawListCursor */
static void adapt_DrawListCursor(ProbeState *s)
{
	DrawListCursorResult result = DrawListCursor(s->a);
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawListCursor */

/* >>> factory DrawHorizontalListCursor_Invisible */
static void adapt_DrawHorizontalListCursor_Invisible(ProbeState *s)
{
	DrawHorizontalListCursorResult result = DrawHorizontalListCursor_Invisible();
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawHorizontalListCursor_Invisible */

/* >>> factory DrawHorizontalListCursor_Visible */
static void adapt_DrawHorizontalListCursor_Visible(ProbeState *s)
{
	DrawHorizontalListCursorResult result = DrawHorizontalListCursor_Visible();
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawHorizontalListCursor_Visible */

/* >>> factory IsCardInAnyDeck */
static void adapt_IsCardInAnyDeck(ProbeState *s)
{
	IsCardInAnyDeckResult r = IsCardInAnyDeck(s->a, s->f, s->e);
	s->f = r.f;
	s->b = r.b;
}
/* <<< factory IsCardInAnyDeck */

/* >>> factory DrawListCursor_Invisible */
static void adapt_DrawListCursor_Invisible(ProbeState *s)
{
	DrawListCursorResult result = DrawListCursor_Invisible();
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawListCursor_Invisible */

/* >>> factory DrawListCursor_Visible */
static void adapt_DrawListCursor_Visible(ProbeState *s)
{
	DrawListCursorResult result = DrawListCursor_Visible();
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory DrawListCursor_Visible */

/* >>> factory CountNumberOfCardsForEachCardType */
static void adapt_CountNumberOfCardsForEachCardType(ProbeState *s)
{
	(void)s;
	CountNumberOfCardsForEachCardType();
}
/* <<< factory CountNumberOfCardsForEachCardType */

/* >>> factory CopyDeckName */
static void adapt_CopyDeckName(ProbeState *s)
{
	CopyDeckNameResult r = CopyDeckName(s->hl);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory CopyDeckName */

/* >>> factory GetOwnedCardCount */
static void adapt_GetOwnedCardCount(ProbeState *s)
{
	GetOwnedCardCountResult r = GetOwnedCardCount(s->e);
	s->a = r.a;
	s->d = r.d;
}
/* <<< factory GetOwnedCardCount */

/* >>> factory TallyCardsInCardFilterLists */
static void adapt_TallyCardsInCardFilterLists(ProbeState *s)
{
	TallyCardsInCardFilterListsResult r = TallyCardsInCardFilterLists(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory TallyCardsInCardFilterLists */

/* >>> factory RemoveCardFromDeck */
static void adapt_RemoveCardFromDeck(ProbeState *s)
{
	RemoveCardFromDeckResult r = RemoveCardFromDeck(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory RemoveCardFromDeck */

/* >>> factory CheckIfCurrentDeckWasChanged */
static void adapt_CheckIfCurrentDeckWasChanged(ProbeState *s)
{
	CheckIfCurrentDeckWasChangedResult r = CheckIfCurrentDeckWasChanged();
	s->a = r.a; s->f = r.f;
}
/* <<< factory CheckIfCurrentDeckWasChanged */

/* >>> factory CreateFilteredCardList */
static void adapt_CreateFilteredCardList(ProbeState *s)
{
	CreateFilteredCardListResult r =
		CreateFilteredCardList(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CreateFilteredCardList */

/* >>> factory ConfirmSelectionAndReturnCarry */
static void adapt_ConfirmSelectionAndReturnCarry(ProbeState *s)
{
	ConfirmSelectionAndReturnCarryResult r = ConfirmSelectionAndReturnCarry();
	s->a = r.a;
	s->e = r.e;
}
/* <<< factory ConfirmSelectionAndReturnCarry */

/* >>> factory AddCardIDToVisibleList */
static void adapt_AddCardIDToVisibleList(ProbeState *s)
{
	AddCardIDToVisibleList(s->b, s->e);
}
/* <<< factory AddCardIDToVisibleList */

/* >>> factory HandleCardSelectionCursorBlink */
static void adapt_HandleCardSelectionCursorBlink(ProbeState *s)
{
	DrawHorizontalListCursorResult r = HandleCardSelectionCursorBlink();
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory HandleCardSelectionCursorBlink */

/* >>> factory DrawHandCardsTileOnCurDeck */
static void adapt_DrawHandCardsTileOnCurDeck(ProbeState *s)
{
	(void)s;
	DrawHandCardsTileOnCurDeck();
}
/* <<< factory DrawHandCardsTileOnCurDeck */

/* >>> factory HandleCardSelectionInput */
static void adapt_HandleCardSelectionInput(ProbeState *s)
{
	HandleCardSelectionInputResult r = HandleCardSelectionInput();
	s->a = r.a;
	s->e = r.e;
	s->b = r.b;
	s->c = r.c;
	s->f = r.carry ? 0x10u : 0x00u;
}
/* <<< factory HandleCardSelectionInput */

/* >>> factory HandleLeftRightInCardList */
static void adapt_HandleLeftRightInCardList(ProbeState *s)
{
	HandleLeftRightInCardListResult r = HandleLeftRightInCardList();
	s->f = r.f;
}
/* <<< factory HandleLeftRightInCardList */

/* >>> factory PrintPlayersCardsText */
static void adapt_PrintPlayersCardsText(ProbeState *s)
{
	(void)s;
	PrintPlayersCardsText();
}
/* <<< factory PrintPlayersCardsText */

/* >>> factory AddGiftCenterDeckCardsToCollection */
static void adapt_AddGiftCenterDeckCardsToCollection(ProbeState *s)
{
	AddGiftCenterDeckCardsToCollection(s->hl);
}
/* <<< factory AddGiftCenterDeckCardsToCollection */

/* >>> factory ConvertToNumericalDigits */
static void adapt_ConvertToNumericalDigits(ProbeState *s)
{
	ConvertToNumericalDigitsResult r = ConvertToNumericalDigits(s->a, s->hl);
	s->a = r.a; s->b = r.b; s->hl = r.hl;
}
/* <<< factory ConvertToNumericalDigits */

/* >>> factory CopyListFromHLToDEInSRAM */
static void adapt_CopyListFromHLToDEInSRAM(ProbeState *s)
{
	CopyListFromHLToDEInSRAMResult r = CopyListFromHLToDEInSRAM(s->hl, (uint16_t)(s->d << 8 | s->e));
	s->f = r.f; s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8); s->e = (uint8_t)r.de;
}
/* <<< factory CopyListFromHLToDEInSRAM */

/* >>> factory PrintDeckName */
static void adapt_PrintDeckName(ProbeState *s)
{
	PrintDeckName(s->hl, s->d, s->e);
}
/* <<< factory PrintDeckName */

/* >>> factory AppendOwnedCardCountNumber */
static void adapt_AppendOwnedCardCountNumber(ProbeState *s)
{
	AppendOwnedCardCountNumber(s->hl, s->e);
}
/* <<< factory AppendOwnedCardCountNumber */

/* >>> factory PrintNumberValueInCursorYPos */
static void adapt_PrintNumberValueInCursorYPos(ProbeState *s)
{
	PrintNumberValueInCursorYPos(s->a);
}
/* <<< factory PrintNumberValueInCursorYPos */

/* >>> factory AppendOwnedCardCountAndStorageCountNumbers */
static void adapt_AppendOwnedCardCountAndStorageCountNumbers(ProbeState *s)
{
	AppendOwnedCardCountAndStorageCountNumbers(s->hl, s->e);
}
/* <<< factory AppendOwnedCardCountAndStorageCountNumbers */

/* >>> factory PrintCardTypeCounts */
static void adapt_PrintCardTypeCounts(ProbeState *s)
{
	PrintCardTypeCounts();
}
/* <<< factory PrintCardTypeCounts */

const ProbeEntry probe_entries_deck_configuration[] = {
	{ "DecrementDeckCardsInCollection", adapt_DecrementDeckCardsInCollection },
	{ "AddDeckToCollection", adapt_AddDeckToCollection },
	{ "CopyListFromHLToDE", adapt_CopyListFromHLToDE },
	{ "InitCardSelectionParams", adapt_InitCardSelectionParams },
	{ "CalculateOnesAndTensDigits", adapt_CalculateOnesAndTensDigits },
	{ "ClearMemory_Bank2", adapt_ClearMemory_Bank2 },
	{ "CheckIfHasOtherValidDecks", adapt_CheckIfHasOtherValidDecks },
	{ "FillDEWithA", adapt_FillDEWithA },
	{ "DrawHandCardsTileAtDE", adapt_DrawHandCardsTileAtDE },
	{ "CountNumberOfCardsOfType", adapt_CountNumberOfCardsOfType },
	{ "CopyNBytesFromHLToDE", adapt_CopyNBytesFromHLToDE },
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
	{ "AddGiftCenterDeckCardsToCollection", adapt_AddGiftCenterDeckCardsToCollection },
	{ "ConvertToNumericalDigits", adapt_ConvertToNumericalDigits },
	{ "CopyListFromHLToDEInSRAM", adapt_CopyListFromHLToDEInSRAM },
	{ "PrintDeckName", adapt_PrintDeckName },
	{ "AppendOwnedCardCountNumber", adapt_AppendOwnedCardCountNumber },
	{ "PrintNumberValueInCursorYPos", adapt_PrintNumberValueInCursorYPos },
	{ "AppendOwnedCardCountAndStorageCountNumbers", adapt_AppendOwnedCardCountAndStorageCountNumbers },
	{ "PrintCardTypeCounts", adapt_PrintCardTypeCounts },
	{ NULL, NULL },
};
