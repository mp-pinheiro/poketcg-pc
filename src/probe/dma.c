#include "home/dma.h"
#include "probe.h"

static void adapt_DMA(ProbeState *s)
{
	DMA();
	(void)s;
}

const ProbeEntry probe_entries_dma[] = {
	{ "DMA", adapt_DMA },
	{ NULL, NULL },
};
