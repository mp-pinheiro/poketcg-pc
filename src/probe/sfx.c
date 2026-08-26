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

/* >>> factory SFX_loop */
static void adapt_SFX_loop(ProbeState *s)
{
	uint16_t bc = (uint16_t)((uint16_t)s->b << 8 | s->c);
	SFX_loop(bc, s->stack[0]);
}
/* <<< factory SFX_loop */

/* >>> factory SFX_pan */
static void adapt_SFX_pan(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8u) | s->c);
	SFX_pan(bc, s->stack[0]);
}
/* <<< factory SFX_pan */

/* >>> factory SFX_unused */
static void adapt_SFX_unused(ProbeState *s)
{
	SFX_unused(s->hl, (uint16_t)(((uint16_t)s->b << 8u) | s->c));
}
/* <<< factory SFX_unused */

/* >>> factory SFX_pitch_offset */
static void adapt_SFX_pitch_offset(ProbeState *s)
{
	SFX_pitch_offset((uint16_t)(((uint16_t)s->b << 8u) | s->c), s->stack[0]);
}
/* <<< factory SFX_pitch_offset */

/* >>> factory SFX_wave */
static void adapt_SFX_wave(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8u) | s->c);
	SFX_wave(s->a, bc, s->stack[0]);
}
/* <<< factory SFX_wave */

/* >>> factory SFX_duty */
static void adapt_SFX_duty(ProbeState *s)
{
	SFX_duty(s->a, (uint16_t)(((uint16_t)s->b << 8u) | s->c), s->stack[0]);
}
/* <<< factory SFX_duty */

/* >>> factory SFX_envelope */
static void adapt_SFX_envelope(ProbeState *s)
{
	uint16_t bc = (uint16_t)((uint16_t)s->b << 8 | s->c);
	SFX_envelope(bc, s->stack[0]);
}
/* <<< factory SFX_envelope */

const ProbeEntry probe_entries_sfx[] = {
	{ "SFX_PlaySFX", adapt_SFX_PlaySFX },
	{ "SFX_UpdateSFX", adapt_SFX_UpdateSFX },
	{ "Func_fc105", adapt_Func_fc105 },
	{ "SFX_end", adapt_SFX_end },
	{ "SFX_frequency", adapt_SFX_frequency },
	{ "ExecuteNextSFXCommand", adapt_ExecuteNextSFXCommand },
	{ "SFX_loop", adapt_SFX_loop },
	{ "SFX_pan", adapt_SFX_pan },
	{ "SFX_unused", adapt_SFX_unused },
	{ "SFX_pitch_offset", adapt_SFX_pitch_offset },
	{ "SFX_wave", adapt_SFX_wave },
	{ "SFX_duty", adapt_SFX_duty },
	{ "SFX_envelope", adapt_SFX_envelope },
	{ NULL, NULL },
};
