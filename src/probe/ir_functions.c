#include "home/ir_functions.h"
#include "probe.h"

static void adapt_PlayCardPopSong(ProbeState *s)
{
	PlayCardPopSong();
	(void)s;
}

const ProbeEntry probe_entries_ir_functions[] = {
	{ "PlayCardPopSong", adapt_PlayCardPopSong },
	{ NULL, NULL },
};
