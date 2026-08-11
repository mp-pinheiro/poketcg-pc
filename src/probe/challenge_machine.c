#include "home/challenge_machine.h"
#include "probe.h"

static void adapt_ChallengeMachine_CheckIfOpponentAlreadySelected(ProbeState *s)
{
	ChallengeMachineCheckResult result = ChallengeMachine_CheckIfOpponentAlreadySelected(s->a, s->c);
	s->f = result.f;
	s->hl = result.hl;
}

static void adapt_ChallengeMachine_PrintText(ProbeState *s)
{
	ChallengeMachinePrintResult result = ChallengeMachine_PrintText(s->hl, s->b, s->c);
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_challenge_machine[] = {
	{ "ChallengeMachine_CheckIfOpponentAlreadySelected", adapt_ChallengeMachine_CheckIfOpponentAlreadySelected },
	{ "ChallengeMachine_PrintText", adapt_ChallengeMachine_PrintText },
	{ NULL, NULL },
};
