#include "home/audio_callback.h"
#include "probe.h"

static void adapt_Bankswitch3dTo3f(ProbeState *s)
{
	Bankswitch3dTo3f();
	(void)s;
}

const ProbeEntry probe_entries_audio_callback[] = {
	{ "Bankswitch3dTo3f", adapt_Bankswitch3dTo3f },
	{ NULL, NULL },
};
