/* >>> part includes */
#include "home/write_number.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory TwoByteNumberToText */
static void adapt_TwoByteNumberToText(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TwoByteNumberToText(s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory TwoByteNumberToText */

/* >>> part probe_entries_write_number */
const ProbeEntry probe_entries_write_number[] = {
	{ "TwoByteNumberToText", adapt_TwoByteNumberToText },
	{ NULL, NULL },
};
/* <<< part probe_entries_write_number */
