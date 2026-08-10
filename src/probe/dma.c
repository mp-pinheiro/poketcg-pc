#include "home/dma.h"
#include "probe.h"

static void adapt_DMA(ProbeState *s)
{
	DMA();
	s->a = 0;
	s->f = (uint8_t)(0xC0u | (s->f & 0x10u));
}

const ProbeEntry probe_entries_dma[] = {
	{ "DMA", adapt_DMA },
	{ NULL, NULL },
};
