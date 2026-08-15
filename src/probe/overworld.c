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

const ProbeEntry probe_entries_overworld[] = {
	{ "Func_c6cc", adapt_Func_c6cc },
	{ "Func_c6d4", adapt_Func_c6d4 },
	{ "Func_c6f7", adapt_Func_c6f7 },
	{ "SetOverworldNPCFlags", adapt_SetOverworldNPCFlags },
	{ "Func_c158", adapt_Func_c158 },
	{ "Func_c184", adapt_Func_c184 },
	{ NULL, NULL },
};
