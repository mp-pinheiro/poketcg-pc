/* >>> part includes */
#include "home/default_palettes.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Func_12871 */
static void adapt_Func_12871(ProbeState *s)
{
	(void)s;
	Func_12871();
}
/* <<< factory Func_12871 */

/* >>> factory SetDefaultPalettes */
static void adapt_SetDefaultPalettes(ProbeState *s)
{
	(void)s;
	SetDefaultPalettes();
}
/* <<< factory SetDefaultPalettes */

/* >>> part probe_entries_default_palettes */
const ProbeEntry probe_entries_default_palettes[] = {
	{ "Func_12871", adapt_Func_12871 },
	{ "SetDefaultPalettes", adapt_SetDefaultPalettes },
	{ NULL, NULL },
};
/* <<< part probe_entries_default_palettes */
