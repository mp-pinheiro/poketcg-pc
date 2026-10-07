/* >>> part includes */
#include "home/bg_map.h"
#include "probe.h"
/* <<< part includes */

/* >>> part pair */
static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)(hi << 8 | lo);
}
/* <<< part pair */

/* >>> part split */
static void split(uint16_t value, uint8_t *hi, uint8_t *lo)
{
	*hi = (uint8_t)(value >> 8);
	*lo = (uint8_t)value;
}
/* <<< part split */

/* >>> factory WriteDataBlocksToBGMap0 */
static void adapt_WriteDataBlocksToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	WriteDataBlocksToBGMap0(&s->hl, &de, &s->a, &s->b, &s->c);
	split(de, &s->d, &s->e);
}
/* <<< factory WriteDataBlocksToBGMap0 */

/* >>> factory WriteDataBlockToBGMap0 */
static void adapt_WriteDataBlockToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	WriteDataBlockToBGMap0(&s->hl, &de, &s->a, &s->b, &s->c);
	split(de, &s->d, &s->e);
}
/* <<< factory WriteDataBlockToBGMap0 */

/* >>> factory WriteByteToBGMap0 */
static void adapt_WriteByteToBGMap0(ProbeState *s)
{
	s->a = WriteByteToBGMap0(s->a, s->b, s->c);
}
/* <<< factory WriteByteToBGMap0 */

/* >>> factory CopyDataToBGMap0 */
static void adapt_CopyDataToBGMap0(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	CopyDataToBGMap0(s->a, &s->hl, &de, s->b, s->c);
	split(de, &s->d, &s->e);
}
/* <<< factory CopyDataToBGMap0 */

/* >>> factory JPHblankCopyDataHLtoDE */
static void adapt_SafeCopyDataHLtoDE(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	SafeCopyDataHLtoDE(&s->hl, &de, s->b);
	split(de, &s->d, &s->e);
}
/* <<< factory JPHblankCopyDataHLtoDE */

/* >>> part probe_entries_bg_map */
const ProbeEntry probe_entries_bg_map[] = {
	{ "WriteDataBlocksToBGMap0", adapt_WriteDataBlocksToBGMap0 },
	{ "WriteDataBlockToBGMap0", adapt_WriteDataBlockToBGMap0 },
	{ "WriteByteToBGMap0", adapt_WriteByteToBGMap0 },
	{ "CopyDataToBGMap0", adapt_CopyDataToBGMap0 },
	{ "SafeCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ "JPHblankCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ NULL, NULL },
};
/* <<< part probe_entries_bg_map */
