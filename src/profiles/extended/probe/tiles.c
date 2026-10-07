/* >>> part includes */
#include "home/tiles.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory FillRectangle */
static void adapt_FillRectangle(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	FillRectangle(s->a, s->b, s->c, de, s->hl);
}
/* <<< factory FillRectangle */

/* >>> factory CopyFontsOrDuelGraphicsTiles */
static void adapt_CopyFontsOrDuelGraphicsTiles(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyFontsOrDuelGraphicsTiles(&s->hl, &de, s->b);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyFontsOrDuelGraphicsTiles */

/* >>> factory LoadSymbolsFont */
static void adapt_LoadSymbolsFont(ProbeState *s)
{
	TileCopyResult r = LoadSymbolsFont();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadSymbolsFont */

/* >>> factory LoadCardSet2Tiles */
static void adapt_LoadCardSet2Tiles(ProbeState *s)
{
	TileCopyResult r = LoadCardSet2Tiles(s->a);
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadCardSet2Tiles */

/* >>> factory LoadDuelDrawCardsScreenTiles */
static void adapt_LoadDuelDrawCardsScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelDrawCardsScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelDrawCardsScreenTiles */

/* >>> factory LoadCardOrDuelMenuBorderTiles */
static void adapt_LoadCardOrDuelMenuBorderTiles(ProbeState *s)
{
	TileCopyResult r = LoadCardOrDuelMenuBorderTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadCardOrDuelMenuBorderTiles */

/* >>> factory LoadCardTypeHeaderTiles */
static void adapt_LoadCardTypeHeaderTiles(ProbeState *s)
{
	TileCopyResult r = LoadCardTypeHeaderTiles(s->a);
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadCardTypeHeaderTiles */

/* >>> factory LoadDuelCardSymbolTiles */
static void adapt_LoadDuelCardSymbolTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCardSymbolTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelCardSymbolTiles */

/* >>> factory LoadDuelCardSymbolTiles2 */
static void adapt_LoadDuelCardSymbolTiles2(ProbeState *s)
{
	TileCopyResult r = LoadDuelCardSymbolTiles2();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelCardSymbolTiles2 */

/* >>> factory LoadDuelFaceDownCardTiles */
static void adapt_LoadDuelFaceDownCardTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelFaceDownCardTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelFaceDownCardTiles */

/* >>> factory LoadDuelCheckPokemonScreenTiles */
static void adapt_LoadDuelCheckPokemonScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCheckPokemonScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelCheckPokemonScreenTiles */

/* >>> factory LoadPlacingThePrizesScreenTiles */
static void adapt_LoadPlacingThePrizesScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadPlacingThePrizesScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadPlacingThePrizesScreenTiles */

/* >>> factory LoadDeckAndDiscardPileIcons */
static void adapt_LoadDeckAndDiscardPileIcons(ProbeState *s)
{
	TileCopyResult r = LoadDeckAndDiscardPileIcons();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDeckAndDiscardPileIcons */

/* >>> factory LoadDuelCoinTossResultTiles */
static void adapt_LoadDuelCoinTossResultTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCoinTossResultTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory LoadDuelCoinTossResultTiles */

/* >>> factory DrawDuelBoxMessage */
static void adapt_DrawDuelBoxMessage(ProbeState *s)
{
	DrawDuelBoxMessage(s->a);
}
/* <<< factory DrawDuelBoxMessage */

/* >>> part probe_entries_tiles */
const ProbeEntry probe_entries_tiles[] = {
	{ "FillRectangle", adapt_FillRectangle },
	{ "CopyFontsOrDuelGraphicsTiles", adapt_CopyFontsOrDuelGraphicsTiles },
	{ "LoadSymbolsFont", adapt_LoadSymbolsFont },
	{ "LoadCardSet2Tiles", adapt_LoadCardSet2Tiles },
	{ "LoadDuelDrawCardsScreenTiles", adapt_LoadDuelDrawCardsScreenTiles },
	{ "LoadCardOrDuelMenuBorderTiles", adapt_LoadCardOrDuelMenuBorderTiles },
	{ "LoadCardTypeHeaderTiles", adapt_LoadCardTypeHeaderTiles },
	{ "LoadDuelCardSymbolTiles", adapt_LoadDuelCardSymbolTiles },
	{ "LoadDuelCardSymbolTiles2", adapt_LoadDuelCardSymbolTiles2 },
	{ "LoadDuelFaceDownCardTiles", adapt_LoadDuelFaceDownCardTiles },
	{ "LoadDuelCheckPokemonScreenTiles", adapt_LoadDuelCheckPokemonScreenTiles },
	{ "LoadPlacingThePrizesScreenTiles", adapt_LoadPlacingThePrizesScreenTiles },
	{ "LoadDeckAndDiscardPileIcons", adapt_LoadDeckAndDiscardPileIcons },
	{ "LoadDuelCoinTossResultTiles", adapt_LoadDuelCoinTossResultTiles },
	{ "DrawDuelBoxMessage", adapt_DrawDuelBoxMessage },
	{ NULL, NULL },
};
/* <<< part probe_entries_tiles */
