/* >>> part includes */
#include "home/dma.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory DMA */
static void adapt_DMA(ProbeState *s)
{
	DMA();
	s->a = 0;
	s->f = (uint8_t)(0xC0u | (s->f & 0x10u));
}
/* <<< factory DMA */

/* >>> factory CopyDMAFunction */
static void adapt_CopyDMAFunction(ProbeState *s)
{
	(void)s;
	CopyDMAFunction();
}
/* <<< factory CopyDMAFunction */

/* >>> part probe_entries_dma */
const ProbeEntry probe_entries_dma[] = {
	{ "DMA", adapt_DMA },
	{ "CopyDMAFunction", adapt_CopyDMAFunction },
	{ NULL, NULL },
};
/* <<< part probe_entries_dma */
