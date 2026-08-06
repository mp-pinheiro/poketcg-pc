#include "home/division.h"
#include "probe.h"

static void adapt_DivideBCbyDE(ProbeState *s)
{
	DivResult r = DivideBCbyDE((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
	s->b = (uint8_t)(r.quotient >> 8);
	s->c = (uint8_t)r.quotient;
	s->hl = r.remainder;
}

const ProbeEntry probe_entries_division[] = {
	{ "DivideBCbyDE", adapt_DivideBCbyDE },
	{ NULL, NULL },
};
