#include "home/decompress.h"
#include "probe.h"

static void adapt_InitDataDecompression(ProbeState *s)
{
	InitDataDecompression((uint16_t)(s->d << 8 | s->e), s->b);
}

static void adapt_DecompressData(ProbeState *s)
{
	DecompressData((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
}

static void adapt_DecompressData_Decompress(ProbeState *s)
{
	s->a = DecompressData_Decompress();
}

const ProbeEntry probe_entries_decompress[] = {
	{ "InitDataDecompression", adapt_InitDataDecompression },
	{ "DecompressData", adapt_DecompressData },
	{ "DecompressData.Decompress", adapt_DecompressData_Decompress },
	{ NULL, NULL },
};
