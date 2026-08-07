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

#endif /* POKETCG_HOME_CARD_COLLECTION_H */
