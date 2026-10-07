/* >>> part includes */
#include "home/decompress.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory InitDataDecompression */
static void adapt_InitDataDecompression(ProbeState *s)
{
	InitDataDecompression((uint16_t)(s->d << 8 | s->e), s->b);
}
/* <<< factory InitDataDecompression */

/* >>> factory DecompressData */
static void adapt_DecompressData(ProbeState *s)
{
	DecompressData((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory DecompressData */

/* >>> factory DecompressData_Decompress */
static void adapt_DecompressData_Decompress(ProbeState *s)
{
	s->a = DecompressData_Decompress();
}
/* <<< factory DecompressData_Decompress */

/* >>> part probe_entries_decompress */
const ProbeEntry probe_entries_decompress[] = {
	{ "InitDataDecompression", adapt_InitDataDecompression },
	{ "DecompressData", adapt_DecompressData },
	{ "DecompressData.Decompress", adapt_DecompressData_Decompress },
	{ NULL, NULL },
};
/* <<< part probe_entries_decompress */
