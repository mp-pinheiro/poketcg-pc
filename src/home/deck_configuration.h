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
#endif /* POKETCG_HOME_DECK_CONFIGURATION_H */
