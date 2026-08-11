#include "home/sgb.h"
#include "probe.h"

static void adapt_Wait(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	s->a = Wait((uint16_t)((uint16_t)s->b << 8 | s->c), &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

const ProbeEntry probe_entries_sgb[] = {
	{ "Wait", adapt_Wait },
	{ NULL, NULL },
};
