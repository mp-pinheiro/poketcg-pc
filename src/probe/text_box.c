#include "home/text_box.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)(hi << 8 | lo);
}

static void split(uint16_t value, uint8_t *hi, uint8_t *lo)
{
	*hi = (uint8_t)(value >> 8);
	*lo = (uint8_t)value;
}

static void adapt_SafeCopyDataDEtoHL(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	SafeCopyDataDEtoHL(&de, &s->hl, s->c);
	split(de, &s->d, &s->e);
}

static void adapt_DECoordToBGMap0Address(ProbeState *s)
{
	s->hl = DECoordToBGMap0Address(s->d, s->e);
}

static void adapt_AdjustCoordinatesForBGScroll(ProbeState *s)
{
	AdjustCoordinatesForBGScroll(&s->d, &s->e);
}
static void adapt_CopyLine(ProbeState *s)
{
	uint16_t original_hl = s->hl;
	CopyLine(&s->hl, s->a, s->b, s->d, s->e);
	split(original_hl, &s->d, &s->e);
}

const ProbeEntry probe_entries_text_box[] = {
	{ "SafeCopyDataDEtoHL", adapt_SafeCopyDataDEtoHL },
	{ "DECoordToBGMap0Address", adapt_DECoordToBGMap0Address },
	{ "AdjustCoordinatesForBGScroll", adapt_AdjustCoordinatesForBGScroll },
	{ "CopyLine", adapt_CopyLine },
	{ NULL, NULL },
};
