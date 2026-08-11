#include "home/debug_player_coordinates.h"
#include "probe.h"

static void adapt_JumpSetWindowOff(ProbeState *s)
{
	JumpSetWindowOff();
	(void)s;
}

const ProbeEntry probe_entries_debug_player_coordinates[] = {
	{ "JumpSetWindowOff", adapt_JumpSetWindowOff },
	{ NULL, NULL },
};
