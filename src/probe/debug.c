#include "home/debug.h"
#include "probe.h"

static void adapt_DebugSGBFrame(ProbeState *s)
{
	DebugSGBFrameResult result = DebugSGBFrame(s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

static void adapt_DebugStandardBGCharacter(ProbeState *s)
{
	DebugStandardBGCharacterResult result = DebugStandardBGCharacter(
		s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}

static void adapt_DebugQuit(ProbeState *s)
{
	DebugQuitResult result = DebugQuit(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
}

/* >>> factory UnreferencedFillVRAMWithRandomData */
static void adapt_UnreferencedFillVRAMWithRandomData(ProbeState *s)
{
	UnreferencedFillVRAMWithRandomDataResult result = UnreferencedFillVRAMWithRandomData();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory UnreferencedFillVRAMWithRandomData */

/* >>> factory _DebugVEffect */
static void adapt_DebugVEffect(ProbeState *s)
{
	(void)s;
	_DebugVEffect();
}
/* <<< factory _DebugVEffect */

/* >>> factory Func_80c64 */
static void adapt_Func_80c64(ProbeState *s)
{
	(void)s;
	Func_80c64();
}
/* <<< factory Func_80c64 */

/* >>> factory DebugVEffect */
static void adapt_DebugVEffectOuter(ProbeState *s)
{
	DebugVEffectResult result = DebugVEffect(s->a, s->f, s->b, s->c,
		s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory DebugVEffect */

/* >>> factory DebugCGBTest */
static void adapt_DebugCGBTest(ProbeState *s)
{
	DebugCGBTestResult result = DebugCGBTest(s->a, s->f, s->b, s->c,
		s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory DebugCGBTest */

const ProbeEntry probe_entries_debug[] = {
	{"DebugSGBFrame", adapt_DebugSGBFrame},
	{"DebugStandardBGCharacter", adapt_DebugStandardBGCharacter},
	{"DebugQuit", adapt_DebugQuit},
	{ "UnreferencedFillVRAMWithRandomData", adapt_UnreferencedFillVRAMWithRandomData },
	{ "_DebugVEffect", adapt_DebugVEffect },
	{ "Func_80c64", adapt_Func_80c64 },
	{ "DebugVEffect", adapt_DebugVEffectOuter },
	{ "DebugCGBTest", adapt_DebugCGBTest },
	{NULL, NULL},
};
