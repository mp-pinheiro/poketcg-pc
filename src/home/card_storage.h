#ifndef POKETCG_HOME_CARD_STORAGE_H
#define POKETCG_HOME_CARD_STORAGE_H

/* >>> part includes */
#include <stdint.h>

#include "home/card_id.h"
/* <<< part includes */

/* >>> part CARD_DECK_SIZE */
#define CARD_DECK_SIZE 60u
/* <<< part CARD_DECK_SIZE */
/* >>> part CARD_DECK_COMPRESSED_SIZE */
#define CARD_DECK_COMPRESSED_SIZE 68u
/* <<< part CARD_DECK_COMPRESSED_SIZE */

/* >>> part CompressCardIdDeck */
uint8_t CompressCardIdDeck(const CardId *cards, uint8_t *compressed);
/* <<< part CompressCardIdDeck */
/* >>> part DecompressCardIdDeck */
uint8_t DecompressCardIdDeck(const uint8_t *compressed, CardId *cards);
/* <<< part DecompressCardIdDeck */

#endif
