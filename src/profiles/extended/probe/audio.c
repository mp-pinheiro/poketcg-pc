#include "home/audio.h"
#include "probe.h"

static void adapt_GetAudioCmdAndArgs(ProbeState *s)
{
	s->a = GetAudioCmdAndArgs(s->a, s->hl);
}

const ProbeEntry probe_entries_audio[] = {
	{ "GetAudioCmdAndArgs", adapt_GetAudioCmdAndArgs },
	{ NULL, NULL },
};
