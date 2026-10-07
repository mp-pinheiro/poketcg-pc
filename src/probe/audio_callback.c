/* >>> part includes */
#include "home/audio_callback.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Bankswitch3dTo3f */
static void adapt_Bankswitch3dTo3f(ProbeState *s)
{
	Bankswitch3dTo3f();
	(void)s;
}
/* <<< factory Bankswitch3dTo3f */

/* >>> part probe_entries_audio_callback */
const ProbeEntry probe_entries_audio_callback[] = {
	{ "Bankswitch3dTo3f", adapt_Bankswitch3dTo3f },
	{ NULL, NULL },
};
/* <<< part probe_entries_audio_callback */
