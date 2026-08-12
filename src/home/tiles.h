#ifndef POKETCG_HOME_TILES_H
#define POKETCG_HOME_TILES_H

#include <stdint.h>

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

/* >>> factory Func_2057 */
uint8_t Func_2057(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi);
/* <<< factory Func_2057 */
#endif /* POKETCG_HOME_TILES_H */
