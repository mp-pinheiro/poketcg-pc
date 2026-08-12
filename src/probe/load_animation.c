#include "home/load_animation.h"
#include "probe.h"

#include "generated/hram.h"
#include "generated/wram.h"

static void adapt_GetFirstSpriteAnimBufferProperty(ProbeState *s)
{
	s->hl = GetFirstSpriteAnimBufferProperty();
}

static void adapt_GetSpriteAnimBufferProperty(ProbeState *s)
{
	s->hl = GetSpriteAnimBufferProperty(s->c);
}

static void adapt_GetSpriteAnimBufferProperty_SpriteInA(ProbeState *s)
{
	s->hl = GetSpriteAnimBufferProperty_SpriteInA(s->a, s->c);
}

static void adapt_Func_3ddb(ProbeState *s)
{
	Func_3ddb(s->a);
}

static void adapt_Func_3de7(ProbeState *s)
{
	Func_3de7(s->a);
}

static void adapt_DrawSpriteAnimationFrame(ProbeState *s)
{
	DrawSpriteAnimationFrame(&s->hl);
	s->a = hBankROM;
}

static void adapt_GetAnimationFramePointer(ProbeState *s)
{
	GetAnimationFramePointer(s->hl);
	s->a = hBankROM;
}

/* >>> factory ClearSpriteAnimations */
static void adapt_ClearSpriteAnimations(ProbeState *s)
{
	(void)s;
	ClearSpriteAnimations();
}
/* <<< factory ClearSpriteAnimations */

/* >>> factory HandleAllSpriteAnimations */
static void adapt_HandleAllSpriteAnimations(ProbeState *s)
{
	(void)s;
	HandleAllSpriteAnimations();
}
/* <<< factory HandleAllSpriteAnimations */

/* >>> factory EnableAndClearSpriteAnimations */
static void adapt_EnableAndClearSpriteAnimations(ProbeState *s)
{
	(void)s;
	EnableAndClearSpriteAnimations();
}
/* <<< factory EnableAndClearSpriteAnimations */

const ProbeEntry probe_entries_load_animation[] = {
	{ "GetFirstSpriteAnimBufferProperty", adapt_GetFirstSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty", adapt_GetSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty_SpriteInA", adapt_GetSpriteAnimBufferProperty_SpriteInA },
	{ "Func_3ddb", adapt_Func_3ddb },
	{ "Func_3de7", adapt_Func_3de7 },
	{ "DrawSpriteAnimationFrame", adapt_DrawSpriteAnimationFrame },
	{ "GetAnimationFramePointer", adapt_GetAnimationFramePointer },
	{ "ClearSpriteAnimations", adapt_ClearSpriteAnimations },
	{ "HandleAllSpriteAnimations", adapt_HandleAllSpriteAnimations },
	{ "EnableAndClearSpriteAnimations", adapt_EnableAndClearSpriteAnimations },
	{ NULL, NULL },
};
