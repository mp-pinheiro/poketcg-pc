#include "home/credits_sequence_commands.h"
#include "probe.h"

static void adapt_SetCreditsSequenceCmdPtr(ProbeState *s)
{
	(void)s;
	SetCreditsSequenceCmdPtr();
}

static void adapt_ExecuteCreditsSequenceCmd(ProbeState *s)
{
	(void)s;
	ExecuteCreditsSequenceCmd();
}

static void adapt_AdvanceCreditsSequenceCmdPtr(ProbeState *s)
{
	AdvanceCreditsSequenceCmdPtr(s->a);
}

/* >>> factory AdvanceCreditsSequenceCmdPtrBy2 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy2(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy2 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy3 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy3(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy3();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy3 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy5 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy5(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy5();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy5 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy6 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy6(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy6 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy4 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy4(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy4();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy4 */

const ProbeEntry probe_entries_credits_sequence_commands[] = {
	{ "SetCreditsSequenceCmdPtr", adapt_SetCreditsSequenceCmdPtr },
	{ "ExecuteCreditsSequenceCmd", adapt_ExecuteCreditsSequenceCmd },
	{ "AdvanceCreditsSequenceCmdPtr", adapt_AdvanceCreditsSequenceCmdPtr },
	{ "AdvanceCreditsSequenceCmdPtrBy2", adapt_AdvanceCreditsSequenceCmdPtrBy2 },
	{ "AdvanceCreditsSequenceCmdPtrBy3", adapt_AdvanceCreditsSequenceCmdPtrBy3 },
	{ "AdvanceCreditsSequenceCmdPtrBy5", adapt_AdvanceCreditsSequenceCmdPtrBy5 },
	{ "AdvanceCreditsSequenceCmdPtrBy6", adapt_AdvanceCreditsSequenceCmdPtrBy6 },
	{ "AdvanceCreditsSequenceCmdPtrBy4", adapt_AdvanceCreditsSequenceCmdPtrBy4 },
	{ NULL, NULL },
};
