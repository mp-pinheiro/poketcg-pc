#ifndef POKETCG_HOME_TILES_H
#define POKETCG_HOME_TILES_H

#include <stdint.h>

/* Func_2057 consumes the selected tile byte, x byte, x-offset byte, and y byte
 * from its caller's stack frame, then writes tile at (x + offset, y). */
uint8_t Func_2057(uint8_t e, uint8_t x, uint8_t offset, uint8_t y);

void FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
void Copy1bppTiles(uint16_t *hl, uint16_t *de);

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

TileCopyResult Func_212f(void);
void DrawDuelBoxMessage(uint8_t a);
void LoadFullWidthFontTiles(void);

#endif /* POKETCG_HOME_TILES_H */
