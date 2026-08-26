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
/* >>> factory HandleCardAlbumCardPage */
typedef struct { uint8_t a; uint8_t f; } HandleCardAlbumCardPageResult;
HandleCardAlbumCardPageResult HandleCardAlbumCardPage(uint8_t d, uint8_t e);
/* <<< factory HandleCardAlbumCardPage */
/* >>> factory CreateCardSetListAndInitListCoords */
void CreateCardSetListAndInitListCoords(uint8_t a);
/* <<< factory CreateCardSetListAndInitListCoords */
/* >>> factory CardAlbum */
void CardAlbum(void);
/* <<< factory CardAlbum */
#endif /* POKETCG_HOME_CARD_ALBUM_H */
