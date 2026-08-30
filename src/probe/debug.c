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

/* >>> factory DebugCreateBoosterPack */
static void adapt_DebugCreateBoosterPack(ProbeState *s)
{
	(void)s;
	DebugCreateBoosterPack();
	s->f = 0x10u;
}
/* <<< factory DebugCreateBoosterPack */

/* >>> factory DebugCredits */
static void adapt_DebugCredits(ProbeState *s)
{
	(void)s;
	DebugCredits();
}
/* <<< factory DebugCredits */

/* >>> factory _DebugLookAtSprite */
static void adapt__DebugLookAtSprite(ProbeState *s)
{
	(void)s;
	_DebugLookAtSprite();
}
/* <<< factory _DebugLookAtSprite */

/* >>> factory DebugLookAtSprite */
static void adapt_DebugLookAtSprite(ProbeState *s)
{
	(void)s;
	DebugLookAtSprite();
}
/* <<< factory DebugLookAtSprite */

/* >>> factory DebugDuelMode */
static void adapt_DebugDuelMode(ProbeState *s)
{
	DebugDuelModeResult result = DebugDuelMode();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory DebugDuelMode */

const ProbeEntry probe_entries_debug[] = {
	{"DebugSGBFrame", adapt_DebugSGBFrame},
	{"DebugStandardBGCharacter", adapt_DebugStandardBGCharacter},
	{"DebugQuit", adapt_DebugQuit},
	{ "UnreferencedFillVRAMWithRandomData", adapt_UnreferencedFillVRAMWithRandomData },
	{ "_DebugVEffect", adapt_DebugVEffect },
	{ "Func_80c64", adapt_Func_80c64 },
	{ "DebugVEffect", adapt_DebugVEffectOuter },
	{ "DebugCGBTest", adapt_DebugCGBTest },
	{ "DebugCreateBoosterPack", adapt_DebugCreateBoosterPack },
	{ "DebugCredits", adapt_DebugCredits },
	{ "_DebugLookAtSprite", adapt__DebugLookAtSprite },
	{ "DebugLookAtSprite", adapt_DebugLookAtSprite },
	{ "DebugDuelMode", adapt_DebugDuelMode },
	{NULL, NULL},
};
