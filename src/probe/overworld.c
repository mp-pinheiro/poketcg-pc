#include "home/overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Func_c6cc */
static void adapt_Func_c6cc(ProbeState *s)
{
	s->a = Func_c6cc(s->a);
}
/* <<< factory Func_c6cc */

/* >>> factory Func_c6d4 */
static void adapt_Func_c6d4(ProbeState *s)
{
	s->a = Func_c6d4(s->a);
}
/* <<< factory Func_c6d4 */

/* >>> factory Func_c6f7 */
static void adapt_Func_c6f7(ProbeState *s)
{
	s->a = Func_c6f7(&s->hl);
}
/* <<< factory Func_c6f7 */

/* >>> factory SetOverworldNPCFlags */
static void adapt_SetOverworldNPCFlags(ProbeState *s)
{
	OverworldNPCFlagsResult result = SetOverworldNPCFlags(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetOverworldNPCFlags */

/* >>> factory Func_c158 */
static void adapt_Func_c158(ProbeState *s)
{
	s->a = Func_c158();
}
/* <<< factory Func_c158 */

/* >>> factory Func_c184 */
static void adapt_Func_c184(ProbeState *s)
{
	Func_c184();
}
/* <<< factory Func_c184 */

/* >>> factory WhiteOutDMGPals */
static void adapt_WhiteOutDMGPals(ProbeState *s)
{
	(void)s;
	WhiteOutDMGPals();
}
/* <<< factory WhiteOutDMGPals */

/* >>> factory Func_c1f8 */
static void adapt_Func_c1f8(ProbeState *s)
{
	(void)s;
	Func_c1f8();
}
/* <<< factory Func_c1f8 */

/* >>> factory BackupPlayerPosition */
static void adapt_BackupPlayerPosition(ProbeState *s)
{
	(void)s;
	BackupPlayerPosition();
}
/* <<< factory BackupPlayerPosition */

/* >>> factory Func_c469 */
static void adapt_Func_c469(ProbeState *s)
{
	Func_c469();
}
/* <<< factory Func_c469 */



/* >>> factory SetScreenScrollWram */
static void adapt_SetScreenScrollWram(ProbeState *s)
{
	s->a = SetScreenScrollWram();
}
/* <<< factory SetScreenScrollWram */



/* >>> factory SetScreenScroll */
static void adapt_SetScreenScroll(ProbeState *s)
{
	SetScreenScroll();
}
/* <<< factory SetScreenScroll */



/* >>> factory Func_c70d */
static void adapt_Func_c70d(ProbeState *s)
{
	FuncC70dResult r = Func_c70d();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_c70d */

/* >>> factory Func_c430 */
static void adapt_Func_c430(ProbeState *s)
{
	(void)s;
	Func_c430();
}
/* <<< factory Func_c430 */

/* >>> factory Func_c41c */
static void adapt_Func_c41c(ProbeState *s)
{
	(void)s;
	Func_c41c();
}
/* <<< factory Func_c41c */

/* >>> factory Func_c3ca */
static void adapt_Func_c3ca(ProbeState *s)
{
	FuncC3caResult result = Func_c3ca(s->b, s->c, s->d, s->e);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_c3ca */

/* >>> factory GetDirectionFromDPad */
static void adapt_GetDirectionFromDPad(ProbeState *s)
{
	GetDirectionFromDPadResult result = GetDirectionFromDPad(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory GetDirectionFromDPad */

const ProbeEntry probe_entries_overworld[] = {
	{ "Func_c6cc", adapt_Func_c6cc },
	{ "Func_c6d4", adapt_Func_c6d4 },
	{ "Func_c6f7", adapt_Func_c6f7 },
	{ "SetOverworldNPCFlags", adapt_SetOverworldNPCFlags },
	{ "Func_c158", adapt_Func_c158 },
	{ "Func_c184", adapt_Func_c184 },
	{ "WhiteOutDMGPals", adapt_WhiteOutDMGPals },
	{ "Func_c1f8", adapt_Func_c1f8 },
	{ "BackupPlayerPosition", adapt_BackupPlayerPosition },
	{ "Func_c469", adapt_Func_c469 },
	{ "SetScreenScrollWram", adapt_SetScreenScrollWram },
	{ "SetScreenScroll", adapt_SetScreenScroll },
	{ "Func_c70d", adapt_Func_c70d },
	{ "Func_c430", adapt_Func_c430 },
	{ "Func_c41c", adapt_Func_c41c },
	{ "Func_c3ca", adapt_Func_c3ca },
	{ "GetDirectionFromDPad", adapt_GetDirectionFromDPad },
	{ NULL, NULL },
};
