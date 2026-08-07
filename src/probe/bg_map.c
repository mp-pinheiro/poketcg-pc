#include "home/bg_map.h"
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

static void adapt_WriteDataBlocksToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	WriteDataBlocksToBGMap0(&s->hl, &de, &s->a, &s->b, &s->c);
	split(de, &s->d, &s->e);
}

static void adapt_WriteDataBlockToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	WriteDataBlockToBGMap0(&s->hl, &de, &s->a, &s->b, &s->c);
	split(de, &s->d, &s->e);
}

static void adapt_WriteByteToBGMap0(ProbeState *s)
{
	WriteByteToBGMap0(s->a, s->b, s->c);
}

static void adapt_HblankWriteByteToBGMap0(ProbeState *s)
{
	s->a = HblankWriteByteToBGMap0(s->a, s->b, s->c);
}

static void adapt_CopyDataToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	CopyDataToBGMap0(s->a, &s->hl, &de, s->b, s->c);
	split(de, &s->d, &s->e);
}

static void adapt_SafeCopyDataHLtoDE(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	SafeCopyDataHLtoDE(&s->hl, &de, s->b);
	split(de, &s->d, &s->e);
}

const ProbeEntry probe_entries_bg_map[] = {
	{ "WriteDataBlocksToBGMap0", adapt_WriteDataBlocksToBGMap0 },
	{ "WriteDataBlockToBGMap0", adapt_WriteDataBlockToBGMap0 },
	{ "WriteByteToBGMap0", adapt_WriteByteToBGMap0 },
	{ "HblankWriteByteToBGMap0", adapt_HblankWriteByteToBGMap0 },
	{ "CopyDataToBGMap0", adapt_CopyDataToBGMap0 },
	{ "SafeCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ "JPHblankCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ NULL, NULL },
};
