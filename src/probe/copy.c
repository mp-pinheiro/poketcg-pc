#include "home/copy.h"
#include "probe.h"

/* b is left as the caller passed it: the asm's exit b == 0 is loop residue, so
 * it stays out of CONTRACT instead of being hardcoded here. */
static void adapt_CopyGfxData(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyGfxData(&s->hl, &de, s->b, s->c);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_CopyDataHLtoDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyDataHLtoDE(&s->hl, &de, (uint16_t)(s->b << 8 | s->c));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

/* Nothing is written back: bc/de/hl are inputs the wrapper restores, so a body
 * that clobbered them shows up as a diff. */
static void adapt_CopyDataHLtoDE_SaveRegisters(ProbeState *s)
{
	CopyDataHLtoDE_SaveRegisters(s->hl, (uint16_t)(s->d << 8 | s->e),
				     (uint16_t)(s->b << 8 | s->c));
}

const ProbeEntry probe_entries_copy[] = {
	{ "CopyGfxData", adapt_CopyGfxData },
	{ "CopyDataHLtoDE", adapt_CopyDataHLtoDE },
	{ "CopyDataHLtoDE_SaveRegisters", adapt_CopyDataHLtoDE_SaveRegisters },
	{ NULL, NULL },
};
