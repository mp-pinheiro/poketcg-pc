#include "home/sgb.h"
#include "probe.h"

static void adapt_Wait(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8) | s->c);
	SGBWaitResult r = Wait(bc);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}

/* >>> factory SendSGB */
static void adapt_SendSGB(ProbeState *s)
{
	SendSGBResult r = SendSGB(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SendSGB */

/* >>> factory InitSGB */
static void adapt_InitSGB(ProbeState *s)
{
	InitSGBResult r = InitSGB(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory InitSGB */

const ProbeEntry probe_entries_sgb[] = {
	{ "Wait", adapt_Wait },
	{ "SendSGB", adapt_SendSGB },
	{ "InitSGB", adapt_InitSGB },
	{ NULL, NULL },
};
