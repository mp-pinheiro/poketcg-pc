#include "home/scripting.h"
#include "probe.h"

/* >>> factory IncreaseScriptPointer */
static void adapt_IncreaseScriptPointer(ProbeState *s)
{
	IncreaseScriptPointerResult result = IncreaseScriptPointer(s->a);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory IncreaseScriptPointer */


/* >>> factory SetScriptPointer */
static void adapt_SetScriptPointer(ProbeState *s)
{
	s->hl = SetScriptPointer((uint16_t)(s->b << 8 | s->c));
}
/* <<< factory SetScriptPointer */


/* >>> factory GetScriptArgsAfterPointer */
static void adapt_GetScriptArgsAfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult result = GetScriptArgsAfterPointer(s->a);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory GetScriptArgsAfterPointer */


/* >>> factory GetEventVar */
static void adapt_GetEventVar(ProbeState *s)
{
	GetEventVarResult result = GetEventVar(s->a, s->f, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory GetEventVar */


/* >>> factory IncreaseScriptPointerBy1 */
static void adapt_IncreaseScriptPointerBy1(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy1();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy1 */

/* >>> factory IncreaseScriptPointerBy2 */
static void adapt_IncreaseScriptPointerBy2(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy2();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy2 */

/* >>> factory IncreaseScriptPointerBy4 */
static void adapt_IncreaseScriptPointerBy4(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy4 */

/* >>> factory IncreaseScriptPointerBy3 */
static void adapt_IncreaseScriptPointerBy3(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy3 */

/* >>> factory GetScriptArgs5AfterPointer */
static void adapt_GetScriptArgs5AfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgs5AfterPointer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetScriptArgs5AfterPointer */

/* >>> factory SetScriptControlByteFail */
static void adapt_SetScriptControlByteFail(ProbeState *s)
{
	SetScriptControlByteFailResult r = SetScriptControlByteFail();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SetScriptControlByteFail */

const ProbeEntry probe_entries_scripting[] = {
	{ "IncreaseScriptPointer", adapt_IncreaseScriptPointer },
	{ "SetScriptPointer", adapt_SetScriptPointer },
	{ "GetScriptArgsAfterPointer", adapt_GetScriptArgsAfterPointer },
	{ "GetEventVar", adapt_GetEventVar },
	{ "IncreaseScriptPointerBy1", adapt_IncreaseScriptPointerBy1 },
	{ "IncreaseScriptPointerBy2", adapt_IncreaseScriptPointerBy2 },
	{ "IncreaseScriptPointerBy4", adapt_IncreaseScriptPointerBy4 },
	{ "IncreaseScriptPointerBy3", adapt_IncreaseScriptPointerBy3 },
	{ "GetScriptArgs5AfterPointer", adapt_GetScriptArgs5AfterPointer },
	{ "SetScriptControlByteFail", adapt_SetScriptControlByteFail },
	{ NULL, NULL },
};
