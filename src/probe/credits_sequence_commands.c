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

const ProbeEntry probe_entries_credits_sequence_commands[] = {
	{ "SetCreditsSequenceCmdPtr", adapt_SetCreditsSequenceCmdPtr },
	{ "ExecuteCreditsSequenceCmd", adapt_ExecuteCreditsSequenceCmd },
	{ "AdvanceCreditsSequenceCmdPtr", adapt_AdvanceCreditsSequenceCmdPtr },
	{ NULL, NULL },
};
