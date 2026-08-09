#include "home/sprite_animations.h"
#include "probe.h"

static void adapt__ClearSpriteAnimations(ProbeState *s)
{
	(void)s;
	_ClearSpriteAnimations();
}

static void adapt_CreateSpriteAndAnimBufferEntry(ProbeState *s)
{
	s->f = CreateSpriteAndAnimBufferEntry(s->a, s->f);
}

static void adapt_FillNewSpriteAnimBufferEntry(ProbeState *s)
{
	FillNewSpriteAnimBufferEntry(s->hl);
}

static void adapt_DisableCurSpriteAnim(ProbeState *s)
{
	(void)s;
	DisableCurSpriteAnim();
}

static void adapt_DisableSpriteAnim(ProbeState *s)
{
	DisableSpriteAnim(s->a);
}

static void adapt_GetSpriteAnimCounter(ProbeState *s)
{
	s->a = GetSpriteAnimCounter();
}

static void adapt__HandleAllSpriteAnimations(ProbeState *s)
{
	(void)s;
	_HandleAllSpriteAnimations();
}

static void adapt_LoadSpriteDataForAnimationFrame(ProbeState *s)
{
	LoadSpriteDataForAnimationFrame(s->hl);
}

static void adapt_TryHandleSpriteAnimationFrame(ProbeState *s)
{
	TryHandleSpriteAnimationFrame(s->hl);
}

static void adapt_StartNewSpriteAnimation(ProbeState *s)
{
	StartNewSpriteAnimation(s->a);
}

static void adapt_StartSpriteAnimation(ProbeState *s)
{
	StartSpriteAnimation(s->a);
}

static void adapt_Func_12ac9(ProbeState *s)
{
	Func_12ac9(s->a, s->c);
}

static void adapt_LoadSpriteAnimPointers(ProbeState *s)
{
	s->hl = LoadSpriteAnimPointers(s->a);
}

static void adapt_HandleAnimationFrame(ProbeState *s)
{
	HandleAnimationFrame(s->hl);
}

static void adapt_GetAnimFramePointerFromOffset(ProbeState *s)
{
	GetAnimFramePointerFromOffset(s->a, s->hl);
}

static void adapt_SetAnimationCounterAndLoop(ProbeState *s)
{
	s->f = SetAnimationCounterAndLoop(s->a, s->hl);
}

static void adapt_Func_12ba7(ProbeState *s)
{
	(void)s;
	Func_12ba7();
}

static void adapt_Func_12bcd(ProbeState *s)
{
	(void)s;
	Func_12bcd();
}

static void adapt_ClearSpriteVRAMBuffer(ProbeState *s)
{
	(void)s;
	ClearSpriteVRAMBuffer();
}

static void adapt_Func_12c05(ProbeState *s)
{
	SpriteAnimLookupResult r = Func_12c05(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_Func_12c4f(ProbeState *s)
{
	s->a = Func_12c4f(s->a, s->d);
}

static void adapt_Func_12c5e(ProbeState *s)
{
	(void)s;
	Func_12c5e();
}

const ProbeEntry probe_entries_sprite_animations[] = {
	{ "_ClearSpriteAnimations", adapt__ClearSpriteAnimations },
	{ "CreateSpriteAndAnimBufferEntry", adapt_CreateSpriteAndAnimBufferEntry },
	{ "FillNewSpriteAnimBufferEntry", adapt_FillNewSpriteAnimBufferEntry },
	{ "DisableCurSpriteAnim", adapt_DisableCurSpriteAnim },
	{ "DisableSpriteAnim", adapt_DisableSpriteAnim },
	{ "GetSpriteAnimCounter", adapt_GetSpriteAnimCounter },
	{ "_HandleAllSpriteAnimations", adapt__HandleAllSpriteAnimations },
	{ "LoadSpriteDataForAnimationFrame", adapt_LoadSpriteDataForAnimationFrame },
	{ "TryHandleSpriteAnimationFrame", adapt_TryHandleSpriteAnimationFrame },
	{ "StartNewSpriteAnimation", adapt_StartNewSpriteAnimation },
	{ "StartSpriteAnimation", adapt_StartSpriteAnimation },
	{ "Func_12ac9", adapt_Func_12ac9 },
	{ "LoadSpriteAnimPointers", adapt_LoadSpriteAnimPointers },
	{ "HandleAnimationFrame", adapt_HandleAnimationFrame },
	{ "GetAnimFramePointerFromOffset", adapt_GetAnimFramePointerFromOffset },
	{ "SetAnimationCounterAndLoop", adapt_SetAnimationCounterAndLoop },
	{ "Func_12ba7", adapt_Func_12ba7 },
	{ "Func_12bcd", adapt_Func_12bcd },
	{ "ClearSpriteVRAMBuffer", adapt_ClearSpriteVRAMBuffer },
	{ "Func_12c05", adapt_Func_12c05 },
	{ "Func_12c4f", adapt_Func_12c4f },
	{ "Func_12c5e", adapt_Func_12c5e },
	{ NULL, NULL },
};
