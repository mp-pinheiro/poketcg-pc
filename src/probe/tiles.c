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

const ProbeEntry probe_entries_tiles[] = {
	{ "FillRectangle", adapt_FillRectangle },
	{ "Copy1bppTiles", adapt_Copy1bppTiles },
	{ NULL, NULL },
};
