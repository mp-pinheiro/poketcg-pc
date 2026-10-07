/* >>> part includes */
#include "home/audio.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory GetAudioCmdAndArgs */
static void adapt_GetAudioCmdAndArgs(ProbeState *s)
{
	s->a = GetAudioCmdAndArgs(s->a, s->hl);
}
/* <<< factory GetAudioCmdAndArgs */

/* >>> part probe_entries_audio */
const ProbeEntry probe_entries_audio[] = {
	{ "GetAudioCmdAndArgs", adapt_GetAudioCmdAndArgs },
	{ NULL, NULL },
};
/* <<< part probe_entries_audio */
