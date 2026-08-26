#include "home/sfx.h"
#include "probe.h"

static void adapt_SFX_PlaySFX(ProbeState *s)
{
	SFX_Play(s->a);
}

static void adapt_SFX_UpdateSFX(ProbeState *s)
{
	(void)s;
	SFX_Update();
}

/* >>> factory Func_fc105 */
static void adapt_Func_fc105(ProbeState *s)
{
	s->hl = Func_fc105((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory Func_fc105 */

/* >>> factory SFX_end */
static void adapt_SFX_end(ProbeState *s)
{
	SFX_endResult result = SFX_end(s->b, s->c, s->stack[0]);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory SFX_end */

/* >>> factory SFX_frequency */
static void adapt_SFX_frequency(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8u) | s->c);
	SFX_frequency(bc, s->stack[0], s->a);
}
/* <<< factory SFX_frequency */

/* >>> factory ExecuteNextSFXCommand */
static void adapt_ExecuteNextSFXCommand(ProbeState *s)
{
	ExecuteNextSFXCommand(s->hl, (uint16_t)(((uint16_t)s->b << 8u) | s->c));
}
/* <<< factory ExecuteNextSFXCommand */

const ProbeEntry probe_entries_sfx[] = {
	{ "SFX_PlaySFX", adapt_SFX_PlaySFX },
	{ "SFX_UpdateSFX", adapt_SFX_UpdateSFX },
	{ "Func_fc105", adapt_Func_fc105 },
	{ "SFX_end", adapt_SFX_end },
	{ "SFX_frequency", adapt_SFX_frequency },
	{ "ExecuteNextSFXCommand", adapt_ExecuteNextSFXCommand },
	{ NULL, NULL },
};
