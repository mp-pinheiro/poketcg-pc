#include "home/intro_sequence_commands.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AnimateRandomTitleScreenOrb */
static void adapt_AnimateRandomTitleScreenOrb(ProbeState *s)
{
	s->a = AnimateRandomTitleScreenOrb();
}
/* <<< factory AnimateRandomTitleScreenOrb */

const ProbeEntry probe_entries_intro_sequence_commands[] = {
	{ "AnimateRandomTitleScreenOrb", adapt_AnimateRandomTitleScreenOrb },
	{ NULL, NULL },
};
