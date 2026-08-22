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

/* >>> factory AdvanceIntroSequenceCmdPtr */
static void adapt_AdvanceIntroSequenceCmdPtr(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrResult result = AdvanceIntroSequenceCmdPtr(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AdvanceIntroSequenceCmdPtr */

const ProbeEntry probe_entries_intro_sequence_commands[] = {
	{ "AnimateRandomTitleScreenOrb", adapt_AnimateRandomTitleScreenOrb },
	{ "AdvanceIntroSequenceCmdPtr", adapt_AdvanceIntroSequenceCmdPtr },
	{ NULL, NULL },
};
