#include "home/unsafe_bg_map.h"
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

static void adapt_UnsafeWriteDataBlockToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);

	UnsafeWriteDataBlockToBGMap0(&s->hl, &de);
	split(de, &s->d, &s->e);
}

const ProbeEntry probe_entries_unsafe_bg_map[] = {
	{ "UnsafeWriteDataBlockToBGMap0", adapt_UnsafeWriteDataBlockToBGMap0 },
	{ NULL, NULL },
};
