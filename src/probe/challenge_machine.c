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

/* >>> factory ChallengeMachine_PickOpponentSequence */
static void adapt_ChallengeMachine_PickOpponentSequence(ProbeState *s)
{
	(void)s;
	ChallengeMachine_PickOpponentSequence();
}
/* <<< factory ChallengeMachine_PickOpponentSequence */

const ProbeEntry probe_entries_challenge_machine[] = {
	{ "ChallengeMachine_CheckIfOpponentAlreadySelected", adapt_ChallengeMachine_CheckIfOpponentAlreadySelected },
	{ "ChallengeMachine_PrintText", adapt_ChallengeMachine_PrintText },
	{ "ChallengeMachine_PickOpponentSequence", adapt_ChallengeMachine_PickOpponentSequence },
	{ NULL, NULL },
};
