#ifndef POKETCG_HOME_CARD_STORAGE_H
#define POKETCG_HOME_CARD_STORAGE_H

#include <stdint.h>

#include "home/card_id.h"

#define CARD_DECK_SIZE 60u
#define CARD_DECK_COMPRESSED_SIZE 68u

uint8_t CompressCardIdDeck(const CardId *cards, uint8_t *compressed);
uint8_t DecompressCardIdDeck(const uint8_t *compressed, CardId *cards);

#endif
