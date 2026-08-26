#ifndef POKETCG_HOME_CARD_ALBUM_H
#define POKETCG_HOME_CARD_ALBUM_H

#include <stdint.h>

/* >>> factory GetFirstOwnedCardIndex */
typedef struct { uint8_t a; uint8_t b; uint16_t hl; } GetFirstOwnedCardIndexResult;
GetFirstOwnedCardIndexResult GetFirstOwnedCardIndex(void);
/* <<< factory GetFirstOwnedCardIndex */
/* >>> factory PrintCardSetListEntries */
typedef struct { uint16_t hl; } PrintCardSetListEntriesResult;
PrintCardSetListEntriesResult PrintCardSetListEntries(void);
/* <<< factory PrintCardSetListEntries */
/* >>> factory CreateCardSetList */
void CreateCardSetList(uint8_t a);
/* <<< factory CreateCardSetList */
#endif /* POKETCG_HOME_CARD_ALBUM_H */
