#include "home/sound.h"
#include "probe.h"

static void adapt_Func_37c5(ProbeState *s)
{
	uint8_t carry_in = (uint8_t)((s->f & 0x10u) ? 1u : 0u);
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TileConvertResult r = Func_37c5(s->hl, de, s->a, carry_in);
	s->hl = r.hl;
	s->a = r.a;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_Func_37a5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TileConvertWrapResult r = Func_37a5(s->hl, de);
	s->hl = r.hl;
	s->a = r.a;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

const ProbeEntry probe_entries_sound[] = {
	{ "Func_37c5", adapt_Func_37c5 },
	{ "Func_37a5", adapt_Func_37a5 },
	{ NULL, NULL },
};
