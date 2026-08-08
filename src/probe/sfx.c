#include "home/sfx.h"
#include "probe.h"

static void adapt_SFX_PlaySFX(ProbeState *s)
{
	SFX_Play(s->a);
}

static void adapt_SFX_UpdateSFX(ProbeState *s)
{
	(void)s;
	SFX_Update();
}

const ProbeEntry probe_entries_sfx[] = {
	{ "SFX_PlaySFX", adapt_SFX_PlaySFX },
	{ "SFX_UpdateSFX", adapt_SFX_UpdateSFX },
	{ NULL, NULL },
};
