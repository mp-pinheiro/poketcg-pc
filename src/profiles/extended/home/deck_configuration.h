/* === factory CalculateOnesAndTensDigits */
/* >>> factory CalculateOnesAndTensDigits_Long */
void CalculateOnesAndTensDigits_Long(uint16_t hl);
/* <<< factory CalculateOnesAndTensDigits_Long */
/* === factory CopyNBytesFromHLToDE */
/* >>> factory CopyNBytesFromHLToDE_Long */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint16_t de;
} CopyNBytesFromHLToDELongResult;
CopyNBytesFromHLToDELongResult CopyNBytesFromHLToDE_Long(
	uint16_t *hl, uint16_t *de, uint16_t bc);
/* <<< factory CopyNBytesFromHLToDE_Long */
/* >>> factory GetSelectedVisibleCardID */
typedef struct {
	CardId id;
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} GetSelectedVisibleCardIDResult;
GetSelectedVisibleCardIDResult GetSelectedVisibleCardID(void);
/* <<< factory GetSelectedVisibleCardID */
/* >>> factory GetCountOfCardInCurDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } GetCountOfCardInCurDeckResult;
GetCountOfCardInCurDeckResult GetCountOfCardInCurDeck(CardId de);
/* <<< factory GetCountOfCardInCurDeck */
/* >>> factory IsCardInAnyDeck */
typedef struct {
	uint8_t f;
	uint8_t b;
	uint8_t c;
} IsCardInAnyDeckResult;

IsCardInAnyDeckResult IsCardInAnyDeck(uint8_t a, uint8_t f, CardId de);
/* <<< factory IsCardInAnyDeck */
/* >>> factory GetOwnedCardCount */
typedef struct { uint8_t a; uint8_t d; } GetOwnedCardCountResult;
GetOwnedCardCountResult GetOwnedCardCount(CardId de);
/* <<< factory GetOwnedCardCount */
/* >>> factory AddCardIDToVisibleList */
void AddCardIDToVisibleList(uint8_t b, CardId de);
/* <<< factory AddCardIDToVisibleList */
/* --- factory AddGiftCenterDeckCardsToCollection */
/* >>> factory AppendOwnedCardCountNumber */
void AppendOwnedCardCountNumber(uint16_t hl, CardId de);
/* <<< factory AppendOwnedCardCountNumber */
/* >>> factory AppendOwnedCardCountAndStorageCountNumbers */
void AppendOwnedCardCountAndStorageCountNumbers(uint16_t hl, CardId de);
/* <<< factory AppendOwnedCardCountAndStorageCountNumbers */
/* --- factory Func_9ced */
/* >>> factory TryAddCardToDeck */
typedef struct { uint8_t a; uint8_t f; } TryAddCardToDeckResult;
TryAddCardToDeckResult TryAddCardToDeck(CardId de);
/* <<< factory TryAddCardToDeck */
/* >>> factory AddCardToDeckAndUpdateCount */
typedef struct { uint8_t a; uint8_t f; uint8_t e; } AddCardToDeckAndUpdateCountResult;
AddCardToDeckAndUpdateCountResult AddCardToDeckAndUpdateCount(CardId de);
/* <<< factory AddCardToDeckAndUpdateCount */
/* --- factory HandleSendDeckConfigurationMenu */
/* --- factory PrepareToBuildDeckConfigurationToSend */
