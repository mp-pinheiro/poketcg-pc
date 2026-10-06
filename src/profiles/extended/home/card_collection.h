#ifndef POKETCG_HOME_CARD_COLLECTION_H
#define POKETCG_HOME_CARD_COLLECTION_H

#include <stdint.h>
#include "home/card_id.h"

void CreateTempCardCollection(void);
void AddCardToCollection(CardId a);

typedef struct {
	uint8_t d;
	uint8_t e;
} AlbumProgress;

AlbumProgress GetCardAlbumProgress(void);

uint16_t GetAmountOfCardsOwned(void);

typedef struct {
	uint8_t a;
	uint8_t f;
} CardCountResult;

CardCountResult GetCardCountInCollectionAndDecks(CardId a);
CardCountResult GetCardCountInCollection(CardId a);
void RemoveCardFromCollection(CardId a);

#endif /* POKETCG_HOME_CARD_COLLECTION_H */
