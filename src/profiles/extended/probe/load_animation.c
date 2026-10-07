/* >>> part includes */
#include "home/load_animation.h"
#include "probe.h"

#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes */

/* >>> factory GetFirstSpriteAnimBufferProperty */
static void adapt_GetFirstSpriteAnimBufferProperty(ProbeState *s)
{
	s->hl = GetFirstSpriteAnimBufferProperty();
}
/* <<< factory GetFirstSpriteAnimBufferProperty */

/* >>> factory GetSpriteAnimBufferProperty */
static void adapt_GetSpriteAnimBufferProperty(ProbeState *s)
{
	s->hl = GetSpriteAnimBufferProperty(s->c);
}
/* <<< factory GetSpriteAnimBufferProperty */

/* >>> factory GetSpriteAnimBufferProperty_SpriteInA */
static void adapt_GetSpriteAnimBufferProperty_SpriteInA(ProbeState *s)
{
	s->hl = GetSpriteAnimBufferProperty_SpriteInA(s->a, s->c);
}
/* <<< factory GetSpriteAnimBufferProperty_SpriteInA */

/* >>> factory DrawSpriteAnimationFrame */
static void adapt_DrawSpriteAnimationFrame(ProbeState *s)
{
	DrawSpriteAnimationFrame(&s->hl);
	s->a = hBankROM;
}
/* <<< factory DrawSpriteAnimationFrame */

/* >>> factory GetAnimationFramePointer */
static void adapt_GetAnimationFramePointer(ProbeState *s)
{
	GetAnimationFramePointer(s->hl);
	s->a = hBankROM;
}
/* <<< factory GetAnimationFramePointer */

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

/* >>> factory DrawPortrait */
static void adapt_DrawPortrait(ProbeState *s)
{
	DrawPortrait(s->a, s->b, s->c);
}
/* <<< factory DrawPortrait */

/* >>> factory DrawOpponentPortrait */
static void adapt_DrawOpponentPortrait(ProbeState *s)
{
	DrawOpponentPortrait(s->a, s->b, s->c, s->e);
}
/* <<< factory DrawOpponentPortrait */

/* >>> factory DrawPlayerPortrait */
static void adapt_DrawPlayerPortrait(ProbeState *s)
{
	DrawPlayerPortrait(s->b, s->c);
	(void)s;
}
/* <<< factory DrawPlayerPortrait */

/* >>> factory Func_3e31 */
static void adapt_Func_3e31(ProbeState *s)
{
	uint8_t entry_f = s->f;
	Func_3e31();
	s->a = hBankROM;
	s->f = entry_f;
}
/* <<< factory Func_3e31 */

/* >>> factory LoadScene */
static void adapt_LoadScene(ProbeState *s)
{
	LoadSceneResult r = LoadScene(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory LoadScene */

/* >>> part probe_entries_load_animation */
const ProbeEntry probe_entries_load_animation[] = {
	{ "GetFirstSpriteAnimBufferProperty", adapt_GetFirstSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty", adapt_GetSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty_SpriteInA", adapt_GetSpriteAnimBufferProperty_SpriteInA },
	{ "DrawSpriteAnimationFrame", adapt_DrawSpriteAnimationFrame },
	{ "GetAnimationFramePointer", adapt_GetAnimationFramePointer },
	{ "ClearSpriteAnimations", adapt_ClearSpriteAnimations },
	{ "HandleAllSpriteAnimations", adapt_HandleAllSpriteAnimations },
	{ "EnableAndClearSpriteAnimations", adapt_EnableAndClearSpriteAnimations },
	{ "DrawPortrait", adapt_DrawPortrait },
	{ "DrawOpponentPortrait", adapt_DrawOpponentPortrait },
	{ "DrawPlayerPortrait", adapt_DrawPlayerPortrait },
	{ "Func_3e31", adapt_Func_3e31 },
	{ "LoadScene", adapt_LoadScene },
	{ NULL, NULL },
};
/* <<< part probe_entries_load_animation */
