#ifndef POKETCG_HOME_CARD_COLLECTION_H
#define POKETCG_HOME_CARD_COLLECTION_H

#include <stdint.h>

void CreateTempCardCollection(void);
void AddCardToCollection(uint8_t a);

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

CardCountResult GetCardCountInCollectionAndDecks(uint8_t a);
CardCountResult GetCardCountInCollection(uint8_t a);
void RemoveCardFromCollection(uint8_t a);

#endif /* POKETCG_HOME_CARD_COLLECTION_H */
