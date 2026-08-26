#ifndef POKETCG_HOME_DECK_CONFIGURATION_H
#define POKETCG_HOME_DECK_CONFIGURATION_H

#include <stdint.h>

/* >>> factory DecrementDeckCardsInCollection */
uint16_t DecrementDeckCardsInCollection(uint16_t hl);
/* <<< factory DecrementDeckCardsInCollection */
/* >>> factory AddDeckToCollection */
uint16_t AddDeckToCollection(uint16_t hl);
/* <<< factory AddDeckToCollection */
/* >>> factory CopyListFromHLToDE */
void CopyListFromHLToDE(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListFromHLToDE */
/* >>> factory CalculateOnesAndTensDigits */
void CalculateOnesAndTensDigits(uint8_t a);
/* <<< factory CalculateOnesAndTensDigits */
/* >>> factory InitCardSelectionParams */
uint8_t InitCardSelectionParams(uint8_t a, uint16_t *hl);
/* <<< factory InitCardSelectionParams */
/* >>> factory ClearMemory_Bank2 */
void ClearMemory_Bank2(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank2 */
/* >>> factory CheckIfHasOtherValidDecks */
uint8_t CheckIfHasOtherValidDecks(void);
/* <<< factory CheckIfHasOtherValidDecks */
/* >>> factory FillDEWithA */
void FillDEWithA(uint8_t a, uint8_t b, uint16_t de);
/* <<< factory FillDEWithA */
/* >>> factory DrawHandCardsTileAtDE */
void DrawHandCardsTileAtDE(uint16_t de);
/* <<< factory DrawHandCardsTileAtDE */
/* >>> factory CountNumberOfCardsOfType */
uint8_t CountNumberOfCardsOfType(uint8_t a);
/* <<< factory CountNumberOfCardsOfType */
/* >>> factory CopyNBytesFromHLToDE */
void CopyNBytesFromHLToDE(uint16_t *hl, uint16_t *de, uint8_t b);
/* <<< factory CopyNBytesFromHLToDE */
/* >>> factory IncrementDeckCardsInTempCollection */
void IncrementDeckCardsInTempCollection(uint16_t de);
/* <<< factory IncrementDeckCardsInTempCollection */
/* >>> factory CreateCardCollectionListWithDeckCards */
void CreateCardCollectionListWithDeckCards(uint8_t a);
/* <<< factory CreateCardCollectionListWithDeckCards */
/* >>> factory GetSelectedVisibleCardID */
uint8_t GetSelectedVisibleCardID(void);
/* <<< factory GetSelectedVisibleCardID */
/* >>> factory CheckIfDeckHasCards */
uint8_t CheckIfDeckHasCards(uint16_t hl);
/* <<< factory CheckIfDeckHasCards */
/* >>> factory FillBGMapLineWithA */
void FillBGMapLineWithA(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory FillBGMapLineWithA */
/* >>> factory OpenDeckConfigurationMenu */
void OpenDeckConfigurationMenu(void);
/* <<< factory OpenDeckConfigurationMenu */
/* >>> factory PrintTotalNumberOfCardsInCollection */
void PrintTotalNumberOfCardsInCollection(void);
/* <<< factory PrintTotalNumberOfCardsInCollection */
/* >>> factory DrawHorizontalListCursor */
typedef struct {
	uint8_t b;
	uint8_t c;
} DrawHorizontalListCursorResult;

DrawHorizontalListCursorResult DrawHorizontalListCursor(uint8_t a);
/* <<< factory DrawHorizontalListCursor */
/* >>> factory GetCountOfCardInCurDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } GetCountOfCardInCurDeckResult;
GetCountOfCardInCurDeckResult GetCountOfCardInCurDeck(uint8_t e);
/* <<< factory GetCountOfCardInCurDeck */
/* >>> factory DrawListCursor */
typedef struct {
	uint8_t b;
	uint8_t c;
} DrawListCursorResult;

DrawListCursorResult DrawListCursor(uint8_t a);
/* <<< factory DrawListCursor */
/* >>> factory DrawHorizontalListCursor_Invisible */
DrawHorizontalListCursorResult DrawHorizontalListCursor_Invisible(void);
/* <<< factory DrawHorizontalListCursor_Invisible */
/* >>> factory DrawHorizontalListCursor_Visible */
DrawHorizontalListCursorResult DrawHorizontalListCursor_Visible(void);
/* <<< factory DrawHorizontalListCursor_Visible */
/* >>> factory IsCardInAnyDeck */
typedef struct {
	uint8_t f;
	uint8_t b;
} IsCardInAnyDeckResult;

IsCardInAnyDeckResult IsCardInAnyDeck(uint8_t a, uint8_t f, uint8_t e);
/* <<< factory IsCardInAnyDeck */
/* >>> factory DrawListCursor_Invisible */
DrawListCursorResult DrawListCursor_Invisible(void);
/* <<< factory DrawListCursor_Invisible */
/* >>> factory DrawListCursor_Visible */
DrawListCursorResult DrawListCursor_Visible(void);
/* <<< factory DrawListCursor_Visible */
/* >>> factory CountNumberOfCardsForEachCardType */
void CountNumberOfCardsForEachCardType(void);
/* <<< factory CountNumberOfCardsForEachCardType */
/* >>> factory CopyDeckName */
typedef struct { uint16_t hl; uint8_t d; uint8_t e; } CopyDeckNameResult;
CopyDeckNameResult CopyDeckName(uint16_t hl);
/* <<< factory CopyDeckName */
/* >>> factory GetOwnedCardCount */
typedef struct { uint8_t a; uint8_t d; } GetOwnedCardCountResult;
GetOwnedCardCountResult GetOwnedCardCount(uint8_t e);
/* <<< factory GetOwnedCardCount */
/* >>> factory TallyCardsInCardFilterLists */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; uint16_t hl; } TallyCardsInCardFilterListsResult;
TallyCardsInCardFilterListsResult TallyCardsInCardFilterLists(uint8_t d, uint8_t e);
/* <<< factory TallyCardsInCardFilterLists */
/* >>> factory RemoveCardFromDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } RemoveCardFromDeckResult;
RemoveCardFromDeckResult RemoveCardFromDeck(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory RemoveCardFromDeck */
/* >>> factory CheckIfCurrentDeckWasChanged */
typedef struct { uint8_t a; uint8_t f; } CheckIfCurrentDeckWasChangedResult;
CheckIfCurrentDeckWasChangedResult CheckIfCurrentDeckWasChanged(void);
/* <<< factory CheckIfCurrentDeckWasChanged */
/* >>> factory CreateFilteredCardList */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CreateFilteredCardListResult;
CreateFilteredCardListResult CreateFilteredCardList(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CreateFilteredCardList */
/* >>> factory ConfirmSelectionAndReturnCarry */
typedef struct { uint8_t a; uint8_t e; } ConfirmSelectionAndReturnCarryResult;
ConfirmSelectionAndReturnCarryResult ConfirmSelectionAndReturnCarry(void);
/* <<< factory ConfirmSelectionAndReturnCarry */
/* >>> factory AddCardIDToVisibleList */
void AddCardIDToVisibleList(uint8_t b, uint8_t e);
/* <<< factory AddCardIDToVisibleList */
/* >>> factory HandleCardSelectionCursorBlink */
DrawHorizontalListCursorResult HandleCardSelectionCursorBlink(void);
/* <<< factory HandleCardSelectionCursorBlink */
/* >>> factory DrawHandCardsTileOnCurDeck */
void DrawHandCardsTileOnCurDeck(void);
/* <<< factory DrawHandCardsTileOnCurDeck */
/* >>> factory HandleCardSelectionInput */
typedef struct { uint8_t a; uint8_t e; uint8_t b; uint8_t c; uint8_t carry; } HandleCardSelectionInputResult;
HandleCardSelectionInputResult HandleCardSelectionInput(void);
/* <<< factory HandleCardSelectionInput */
/* >>> factory HandleLeftRightInCardList */
typedef struct { uint8_t f; } HandleLeftRightInCardListResult;
HandleLeftRightInCardListResult HandleLeftRightInCardList(void);
/* <<< factory HandleLeftRightInCardList */
/* >>> factory PrintPlayersCardsText */
void PrintPlayersCardsText(void);
/* <<< factory PrintPlayersCardsText */
/* >>> factory AddGiftCenterDeckCardsToCollection */
void AddGiftCenterDeckCardsToCollection(uint16_t hl);
/* <<< factory AddGiftCenterDeckCardsToCollection */
/* >>> factory ConvertToNumericalDigits */
typedef struct { uint8_t a; uint8_t b; uint16_t hl; } ConvertToNumericalDigitsResult;
ConvertToNumericalDigitsResult ConvertToNumericalDigits(uint8_t a, uint16_t hl);
/* <<< factory ConvertToNumericalDigits */
/* >>> factory CopyListFromHLToDEInSRAM */
typedef struct { uint8_t f; uint16_t hl; uint16_t de; } CopyListFromHLToDEInSRAMResult;
CopyListFromHLToDEInSRAMResult CopyListFromHLToDEInSRAM(uint16_t hl, uint16_t de);
/* <<< factory CopyListFromHLToDEInSRAM */
/* >>> factory PrintDeckName */
void PrintDeckName(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintDeckName */
/* >>> factory AppendOwnedCardCountNumber */
void AppendOwnedCardCountNumber(uint16_t hl, uint8_t e);
/* <<< factory AppendOwnedCardCountNumber */
/* >>> factory PrintNumberValueInCursorYPos */
void PrintNumberValueInCursorYPos(uint8_t a);
/* <<< factory PrintNumberValueInCursorYPos */
/* >>> factory AppendOwnedCardCountAndStorageCountNumbers */
void AppendOwnedCardCountAndStorageCountNumbers(uint16_t hl, uint8_t e);
/* <<< factory AppendOwnedCardCountAndStorageCountNumbers */
/* >>> factory PrintCardTypeCounts */
void PrintCardTypeCounts(void);
/* <<< factory PrintCardTypeCounts */
/* >>> factory AppendDeckName */
uint8_t AppendDeckName(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory AppendDeckName */
/* >>> factory DrawDecksScreen */
void DrawDecksScreen(uint8_t a);
/* <<< factory DrawDecksScreen */
/* >>> factory PrintTotalCardCount */
void PrintTotalCardCount(uint8_t d, uint8_t e);
/* <<< factory PrintTotalCardCount */
/* >>> factory RemoveCardFromDeckAndUpdateCount */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } RemoveCardFromDeckAndUpdateCountResult;
RemoveCardFromDeckAndUpdateCountResult RemoveCardFromDeckAndUpdateCount(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory RemoveCardFromDeckAndUpdateCount */
/* >>> factory PrintCardSelectionList */
void PrintCardSelectionList(void);
/* <<< factory PrintCardSelectionList */
/* >>> factory PrintFilteredCardSelectionList */
void PrintFilteredCardSelectionList(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintFilteredCardSelectionList */
/* >>> factory PrintDeckBuildingCardList */
void PrintDeckBuildingCardList(void);
/* <<< factory PrintDeckBuildingCardList */
/* >>> factory PrintFilteredCardList */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PrintFilteredCardListResult;
PrintFilteredCardListResult PrintFilteredCardList(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintFilteredCardList */
/* >>> factory Func_9ced */
void Func_9ced(void);
/* <<< factory Func_9ced */
/* >>> factory OpenCardPageFromCardList */
void OpenCardPageFromCardList(void);
/* <<< factory OpenCardPageFromCardList */
/* >>> factory CheckIfThereAreAnyBasicCardsInDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint16_t hl; } CheckIfThereAreAnyBasicCardsInDeckResult;
CheckIfThereAreAnyBasicCardsInDeckResult CheckIfThereAreAnyBasicCardsInDeck(void);
/* <<< factory CheckIfThereAreAnyBasicCardsInDeck */
/* >>> factory SortCurDeckCardsByID */
typedef struct { uint8_t e; } SortCurDeckCardsByIDResult;
SortCurDeckCardsByIDResult SortCurDeckCardsByID(void);
/* <<< factory SortCurDeckCardsByID */
/* >>> factory GetCardTypeIconPalette */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } GetCardTypeIconPaletteResult;
GetCardTypeIconPaletteResult GetCardTypeIconPalette(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory GetCardTypeIconPalette */
/* >>> factory DrawCardTypeIcons */
void DrawCardTypeIcons(void);
/* <<< factory DrawCardTypeIcons */
/* >>> factory PrintPlayersCardsHeaderInfo */
void PrintPlayersCardsHeaderInfo(void);
/* <<< factory PrintPlayersCardsHeaderInfo */
/* >>> factory PrintConfirmationCardList */
void PrintConfirmationCardList(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
/* <<< factory PrintConfirmationCardList */
/* >>> factory CreateCurDeckUniqueCardList */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CreateCurDeckUniqueCardListResult;
CreateCurDeckUniqueCardListResult CreateCurDeckUniqueCardList(void);
/* <<< factory CreateCurDeckUniqueCardList */
/* >>> factory TryAddCardToDeck */
typedef struct { uint8_t a; uint8_t f; } TryAddCardToDeckResult;
TryAddCardToDeckResult TryAddCardToDeck(uint8_t e);
/* <<< factory TryAddCardToDeck */
/* >>> factory AddCardToDeckAndUpdateCount */
typedef struct { uint8_t a; uint8_t f; uint8_t e; } AddCardToDeckAndUpdateCountResult;
AddCardToDeckAndUpdateCountResult AddCardToDeckAndUpdateCount(uint8_t e);
/* <<< factory AddCardToDeckAndUpdateCount */
#endif /* POKETCG_HOME_DECK_CONFIGURATION_H */
