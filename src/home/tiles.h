#ifndef POKETCG_HOME_TILES_H
#define POKETCG_HOME_TILES_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory FillRectangle */
/* tiles.asm:1-47: exits with hl one row past the rectangle (the last
 * `add hl, de` of TILEMAP_WIDTH), b as given and c counted down to 0; de is
 * popped back. The flags are `add sp, $24`'s and are not modelled. */
uint16_t FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
/* <<< factory FillRectangle */
/* >>> factory Copy1bppTiles */
void Copy1bppTiles(uint16_t *hl, uint16_t *de);
/* <<< factory Copy1bppTiles */

/* >>> part TileCopyResult */
typedef struct {
	uint16_t hl;
	uint16_t de;
} TileCopyResult;
/* <<< part TileCopyResult */

/* >>> factory CopyFontsOrDuelGraphicsTiles */
void CopyFontsOrDuelGraphicsTiles(uint16_t *hl, uint16_t *de, uint8_t b);
/* <<< factory CopyFontsOrDuelGraphicsTiles */
/* >>> factory LoadSymbolsFont */
TileCopyResult LoadSymbolsFont(void);
/* <<< factory LoadSymbolsFont */

/* >>> factory LoadCardSet2Tiles */
TileCopyResult LoadCardSet2Tiles(uint8_t a);
/* <<< factory LoadCardSet2Tiles */
/* >>> factory LoadDuelDrawCardsScreenTiles */
TileCopyResult LoadDuelDrawCardsScreenTiles(void);
/* <<< factory LoadDuelDrawCardsScreenTiles */
/* >>> factory LoadCardOrDuelMenuBorderTiles */
TileCopyResult LoadCardOrDuelMenuBorderTiles(void);
/* <<< factory LoadCardOrDuelMenuBorderTiles */
/* >>> factory LoadCardTypeHeaderTiles */
TileCopyResult LoadCardTypeHeaderTiles(uint8_t a);
/* <<< factory LoadCardTypeHeaderTiles */
/* >>> factory LoadDuelCardSymbolTiles */
TileCopyResult LoadDuelCardSymbolTiles(void);
/* <<< factory LoadDuelCardSymbolTiles */
/* >>> factory LoadDuelCardSymbolTiles2 */
TileCopyResult LoadDuelCardSymbolTiles2(void);
/* <<< factory LoadDuelCardSymbolTiles2 */
/* >>> factory LoadDuelFaceDownCardTiles */
TileCopyResult LoadDuelFaceDownCardTiles(void);
/* <<< factory LoadDuelFaceDownCardTiles */
/* >>> factory LoadDuelCheckPokemonScreenTiles */
TileCopyResult LoadDuelCheckPokemonScreenTiles(void);
/* <<< factory LoadDuelCheckPokemonScreenTiles */
/* >>> factory LoadPlacingThePrizesScreenTiles */
TileCopyResult LoadPlacingThePrizesScreenTiles(void);
/* <<< factory LoadPlacingThePrizesScreenTiles */
/* >>> factory LoadDeckAndDiscardPileIcons */
TileCopyResult LoadDeckAndDiscardPileIcons(void);
/* <<< factory LoadDeckAndDiscardPileIcons */
/* >>> factory LoadDuelCoinTossResultTiles */
TileCopyResult LoadDuelCoinTossResultTiles(void);
/* <<< factory LoadDuelCoinTossResultTiles */

/* >>> factory Func_212f */
TileCopyResult Func_212f(void);
/* <<< factory Func_212f */
/* >>> factory DrawDuelBoxMessage */
void DrawDuelBoxMessage(uint8_t a);
/* <<< factory DrawDuelBoxMessage */
/* >>> factory LoadFullWidthFontTiles */
void LoadFullWidthFontTiles(void);
/* <<< factory LoadFullWidthFontTiles */

/* >>> factory Func_2057 */
uint8_t Func_2057(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi);
/* <<< factory Func_2057 */
/* >>> factory Func_2051 */
uint8_t Func_2051(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi);
/* <<< factory Func_2051 */
/* >>> factory Func_2055 */
uint8_t Func_2055(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi);
/* <<< factory Func_2055 */
/* >>> factory Func_2046 */
void Func_2046(uint16_t counter_addr, uint16_t hl8, uint8_t frame_c,
	uint8_t frame_lo, uint8_t frame_hi);
/* <<< factory Func_2046 */
/* >>> factory Func_1f96 */
typedef struct {
	uint8_t a;
	uint8_t f;
} Func1f96Result;

Func1f96Result Func_1f96(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
/* <<< factory Func_1f96 */
#endif /* POKETCG_HOME_TILES_H */
