#ifndef POKETCG_HOME_CARD_ALBUM_H
#define POKETCG_HOME_CARD_ALBUM_H

#include <stdint.h>

/* >>> factory GetFirstOwnedCardIndex */
typedef struct { uint8_t a; uint8_t b; uint16_t hl; } GetFirstOwnedCardIndexResult;
GetFirstOwnedCardIndexResult GetFirstOwnedCardIndex(void);
/* <<< factory GetFirstOwnedCardIndex */
#endif /* POKETCG_HOME_CARD_ALBUM_H */
