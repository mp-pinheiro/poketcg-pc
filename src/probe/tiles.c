#include "home/tiles.h"
#include "probe.h"

static void adapt_FillRectangle(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	FillRectangle(s->a, s->b, s->c, de, s->hl);
}

static void adapt_Copy1bppTiles(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	Copy1bppTiles(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_CopyFontsOrDuelGraphicsTiles(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyFontsOrDuelGraphicsTiles(&s->hl, &de, s->b);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_LoadSymbolsFont(ProbeState *s)
{
	TileCopyResult r = LoadSymbolsFont();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadCardSet2Tiles(ProbeState *s)
{
	TileCopyResult r = LoadCardSet2Tiles(s->a);
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelDrawCardsScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelDrawCardsScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadCardOrDuelMenuBorderTiles(ProbeState *s)
{
	TileCopyResult r = LoadCardOrDuelMenuBorderTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadCardTypeHeaderTiles(ProbeState *s)
{
	TileCopyResult r = LoadCardTypeHeaderTiles(s->a);
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelCardSymbolTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCardSymbolTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelCardSymbolTiles2(ProbeState *s)
{
	TileCopyResult r = LoadDuelCardSymbolTiles2();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelFaceDownCardTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelFaceDownCardTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelCheckPokemonScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCheckPokemonScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadPlacingThePrizesScreenTiles(ProbeState *s)
{
	TileCopyResult r = LoadPlacingThePrizesScreenTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDeckAndDiscardPileIcons(ProbeState *s)
{
	TileCopyResult r = LoadDeckAndDiscardPileIcons();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_LoadDuelCoinTossResultTiles(ProbeState *s)
{
	TileCopyResult r = LoadDuelCoinTossResultTiles();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_Func_212f(ProbeState *s)
{
	TileCopyResult r = Func_212f();
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_DrawDuelBoxMessage(ProbeState *s)
{
	DrawDuelBoxMessage(s->a);
}

static void adapt_LoadFullWidthFontTiles(ProbeState *s)
{
	(void)s;
	LoadFullWidthFontTiles();
}

static void adapt_Func_2057(ProbeState *s)
{
	s->a = Func_2057(s->a, s->b, s->c, s->d);
}

const ProbeEntry probe_entries_tiles[] = {
	{ "FillRectangle", adapt_FillRectangle },
	{ "Copy1bppTiles", adapt_Copy1bppTiles },
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
	{ "Func_212f", adapt_Func_212f },
	{ "DrawDuelBoxMessage", adapt_DrawDuelBoxMessage },
	{ "LoadFullWidthFontTiles", adapt_LoadFullWidthFontTiles },
	{ "Func_2057", adapt_Func_2057 },
	{ NULL, NULL },
};
