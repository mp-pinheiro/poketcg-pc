#ifndef POKETCG_HOME_TILES_H
#define POKETCG_HOME_TILES_H

#include <stdint.h>

/* tiles.asm:1-47: exits with hl one row past the rectangle (the last
 * `add hl, de` of TILEMAP_WIDTH), b as given and c counted down to 0; de is
 * popped back. The flags are `add sp, $24`'s and are not modelled. */
uint16_t FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl);

typedef struct {
	uint16_t hl;
	uint16_t de;
} TileCopyResult;

void CopyFontsOrDuelGraphicsTiles(uint16_t *hl, uint16_t *de, uint8_t b);
TileCopyResult LoadSymbolsFont(void);

TileCopyResult LoadCardSet2Tiles(uint8_t a);
TileCopyResult LoadDuelDrawCardsScreenTiles(void);
TileCopyResult LoadCardOrDuelMenuBorderTiles(void);
TileCopyResult LoadCardTypeHeaderTiles(uint8_t a);
TileCopyResult LoadDuelCardSymbolTiles(void);
TileCopyResult LoadDuelCardSymbolTiles2(void);
TileCopyResult LoadDuelFaceDownCardTiles(void);
TileCopyResult LoadDuelCheckPokemonScreenTiles(void);
TileCopyResult LoadPlacingThePrizesScreenTiles(void);
TileCopyResult LoadDeckAndDiscardPileIcons(void);
TileCopyResult LoadDuelCoinTossResultTiles(void);


#endif /* POKETCG_HOME_TILES_H */
