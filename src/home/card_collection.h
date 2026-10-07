#ifndef POKETCG_HOME_CARD_COLLECTION_H
#define POKETCG_HOME_CARD_COLLECTION_H

/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"
/* <<< part includes */

/* >>> factory CreateTempCardCollection */
void CreateTempCardCollection(void);
/* <<< factory CreateTempCardCollection */
/* >>> factory AddCardToCollection */
void AddCardToCollection(CardId a);
/* <<< factory AddCardToCollection */

/* >>> part AlbumProgress */
typedef struct {
	uint8_t d;
	uint8_t e;
} AlbumProgress;
/* <<< part AlbumProgress */

/* >>> factory GetCardAlbumProgress */
AlbumProgress GetCardAlbumProgress(void);
/* <<< factory GetCardAlbumProgress */

/* >>> factory GetAmountOfCardsOwned */
uint16_t GetAmountOfCardsOwned(void);
/* <<< factory GetAmountOfCardsOwned */

/* >>> part CardCountResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} CardCountResult;
/* <<< part CardCountResult */

/* >>> factory GetCardCountInCollectionAndDecks */
CardCountResult GetCardCountInCollectionAndDecks(CardId a);
/* <<< factory GetCardCountInCollectionAndDecks */
/* >>> factory GetCardCountInCollection */
CardCountResult GetCardCountInCollection(CardId a);
/* <<< factory GetCardCountInCollection */
/* >>> factory RemoveCardFromCollection */
void RemoveCardFromCollection(CardId a);
/* <<< factory RemoveCardFromCollection */

#endif /* POKETCG_HOME_CARD_COLLECTION_H */
