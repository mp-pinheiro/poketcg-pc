/* >>> part includes */
#include "home/scroll.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ApplyBackgroundScroll */
static void adapt_ApplyBackgroundScroll(ProbeState *s)
{
	ApplyBackgroundScroll();
	(void)s;
}
/* <<< factory ApplyBackgroundScroll */

/* >>> factory Func_3e44 */
static void adapt_Func_3e44(ProbeState *s)
{
	Func_3e44();
	(void)s;
}
/* <<< factory Func_3e44 */

/* >>> factory GetNextBackgroundScroll */
static void adapt_GetNextBackgroundScroll(ProbeState *s)
{
	s->a = GetNextBackgroundScroll(s->a);
}
/* <<< factory GetNextBackgroundScroll */

/* >>> factory EnableInt_LYCoincidence */
static void adapt_EnableInt_LYCoincidence(ProbeState *s)
{
	EnableInt_LYCoincidence();
	(void)s;
}
/* <<< factory EnableInt_LYCoincidence */

/* >>> factory DisableInt_LYCoincidence */
static void adapt_DisableInt_LYCoincidence(ProbeState *s)
{
	DisableInt_LYCoincidence();
	(void)s;
}
/* <<< factory DisableInt_LYCoincidence */

/* >>> part probe_entries_scroll */
const ProbeEntry probe_entries_scroll[] = {
	{ "ApplyBackgroundScroll", adapt_ApplyBackgroundScroll },
	{ "Func_3e44", adapt_Func_3e44 },
	{ "GetNextBackgroundScroll", adapt_GetNextBackgroundScroll },
	{ "EnableInt_LYCoincidence", adapt_EnableInt_LYCoincidence },
	{ "DisableInt_LYCoincidence", adapt_DisableInt_LYCoincidence },
	{ NULL, NULL },
};
/* <<< part probe_entries_scroll */
