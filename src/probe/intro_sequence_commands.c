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

/* >>> factory AdvanceIntroSequenceCmdPtrBy2 */
static void adapt_AdvanceIntroSequenceCmdPtrBy2(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrBy2();
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy2 */

/* >>> factory AdvanceIntroSequenceCmdPtrBy4 */
static void adapt_AdvanceIntroSequenceCmdPtrBy4(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrBy4();
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy4 */

/* >>> factory IntroSequenceEmptyFunc */
static void adapt_IntroSequenceEmptyFunc(ProbeState *s)
{
	(void)s;
	IntroSequenceEmptyFunc();
}
/* <<< factory IntroSequenceEmptyFunc */

const ProbeEntry probe_entries_intro_sequence_commands[] = {
	{ "AnimateRandomTitleScreenOrb", adapt_AnimateRandomTitleScreenOrb },
	{ "AdvanceIntroSequenceCmdPtr", adapt_AdvanceIntroSequenceCmdPtr },
	{ "AdvanceIntroSequenceCmdPtrBy2", adapt_AdvanceIntroSequenceCmdPtrBy2 },
	{ "AdvanceIntroSequenceCmdPtrBy4", adapt_AdvanceIntroSequenceCmdPtrBy4 },
	{ "IntroSequenceEmptyFunc", adapt_IntroSequenceEmptyFunc },
	{ NULL, NULL },
};
