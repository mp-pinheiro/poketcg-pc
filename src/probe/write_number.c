#include "home/write_number.h"
#include "probe.h"

static void adapt_TwoByteNumberToText(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TwoByteNumberToText(s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

const ProbeEntry probe_entries_write_number[] = {
	{ "TwoByteNumberToText", adapt_TwoByteNumberToText },
	{ NULL, NULL },
};
