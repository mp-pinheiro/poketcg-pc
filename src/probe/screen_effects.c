#include "home/screen_effects.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DecrementScreenAnimDuration */
static void adapt_DecrementScreenAnimDuration(ProbeState *s)
{
	DecrementDurResult r = DecrementScreenAnimDuration(s->f);
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory DecrementScreenAnimDuration */

/* >>> factory UpdateShakeOffset */
static void adapt_UpdateShakeOffset(ProbeState *s)
{
	UpdateShakeOffsetResult r = UpdateShakeOffset();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory UpdateShakeOffset */

/* >>> factory DefaultScreenAnimationUpdate */
static void adapt_DefaultScreenAnimationUpdate(ProbeState *s)
{
	DefaultScreenAnimationUpdate();
	(void)s;
}
/* <<< factory DefaultScreenAnimationUpdate */

/* >>> factory DoScreenAnimationUpdate */
static void adapt_DoScreenAnimationUpdate(ProbeState *s)
{
	DoScreenAnimationUpdate();
	(void)s;
}
/* <<< factory DoScreenAnimationUpdate */

/* >>> factory LoadDefaultScreenAnimationUpdateWhenFinished */
static void adapt_LoadDefaultScreenAnimationUpdateWhenFinished(ProbeState *s)
{
	LoadDefaultScreenAnimationUpdateWhenFinished();
	(void)s;
}
/* <<< factory LoadDefaultScreenAnimationUpdateWhenFinished */

/* >>> factory ShakeScreenX */
static void adapt_ShakeScreenX(ProbeState *s)
{
	ShakeScreenX(s->hl);
}
/* <<< factory ShakeScreenX */

/* >>> factory Func_1ce03 */
static void adapt_Func_1ce03(ProbeState *s)
{
	Func_1ce03(s->a);
	s->a = 0x80u;
	s->f = 0x80u;
}
/* <<< factory Func_1ce03 */

/* >>> factory ShakeScreenX_Big */
static void adapt_ShakeScreenX_Big(ProbeState *s)
{
	ShakeScreenX_Big();
}
/* <<< factory ShakeScreenX_Big */

/* >>> factory ShakeScreenX_Small */
static void adapt_ShakeScreenX_Small(ProbeState *s)
{
	ShakeScreenX_Small();
}
/* <<< factory ShakeScreenX_Small */

/* >>> factory DistortScreen */
static void adapt_DistortScreen(ProbeState *s)
{
	DistortScreen();
	(void)s;
}
/* <<< factory DistortScreen */

/* >>> factory WhiteFlashScreen */
static void adapt_WhiteFlashScreen(ProbeState *s)
{
	WhiteFlashScreen();
	(void)s;
}
/* <<< factory WhiteFlashScreen */

/* >>> factory ShakeScreenY */
static void adapt_ShakeScreenY(ProbeState *s)
{
	ShakeScreenY(s->hl);
}
/* <<< factory ShakeScreenY */

/* >>> factory ShakeScreenY_Big */
static void adapt_ShakeScreenY_Big(ProbeState *s)
{
	(void)s;
	ShakeScreenY_Big();
}
/* <<< factory ShakeScreenY_Big */

/* >>> factory ShakeScreenY_Small */
static void adapt_ShakeScreenY_Small(ProbeState *s)
{
	(void)s;
	ShakeScreenY_Small();
}
/* <<< factory ShakeScreenY_Small */

/* >>> factory InitScreenAnimation */
static void adapt_InitScreenAnimation(ProbeState *s)
{
	InitScreenAnimation();
	(void)s;
}
/* <<< factory InitScreenAnimation */

const ProbeEntry probe_entries_screen_effects[] = {
	{ "DecrementScreenAnimDuration", adapt_DecrementScreenAnimDuration },
	{ "UpdateShakeOffset", adapt_UpdateShakeOffset },
	{ "DefaultScreenAnimationUpdate", adapt_DefaultScreenAnimationUpdate },
	{ "DoScreenAnimationUpdate", adapt_DoScreenAnimationUpdate },
	{ "LoadDefaultScreenAnimationUpdateWhenFinished", adapt_LoadDefaultScreenAnimationUpdateWhenFinished },
	{ "ShakeScreenX", adapt_ShakeScreenX },
	{ "Func_1ce03", adapt_Func_1ce03 },
	{ "ShakeScreenX_Big", adapt_ShakeScreenX_Big },
	{ "ShakeScreenX_Small", adapt_ShakeScreenX_Small },
	{ "DistortScreen", adapt_DistortScreen },
	{ "WhiteFlashScreen", adapt_WhiteFlashScreen },
	{ "ShakeScreenY", adapt_ShakeScreenY },
	{ "ShakeScreenY_Big", adapt_ShakeScreenY_Big },
	{ "ShakeScreenY_Small", adapt_ShakeScreenY_Small },
	{ "InitScreenAnimation", adapt_InitScreenAnimation },
	{ NULL, NULL },
};
