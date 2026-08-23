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

/* >>> factory ChallengeMachine_GetCurrentOpponent */
static void adapt_ChallengeMachine_GetCurrentOpponent(ProbeState *s)
{
	ChallengeMachineOpponentResult r = ChallengeMachine_GetCurrentOpponent();
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ChallengeMachine_GetCurrentOpponent */

/* >>> factory ChallengeMachine_IncrementHLMax999 */
static void adapt_ChallengeMachine_IncrementHLMax999(ProbeState *s)
{
	s->hl = ChallengeMachine_IncrementHLMax999(s->hl);
}
/* <<< factory ChallengeMachine_IncrementHLMax999 */

/* >>> factory ChallengeMachine_CheckForNewRecord */
static void adapt_ChallengeMachine_CheckForNewRecord(ProbeState *s)
{
	ChallengeMachineRecordResult r = ChallengeMachine_CheckForNewRecord(s->b, s->c, s->d, s->e);
	s->hl = r.hl;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ChallengeMachine_CheckForNewRecord */

/* >>> factory ChallengeMachine_RecordDuelResult */
static void adapt_ChallengeMachine_RecordDuelResult(ProbeState *s)
{
	(void)s;
	ChallengeMachine_RecordDuelResult();
}
/* <<< factory ChallengeMachine_RecordDuelResult */

/* >>> factory ChallengeMachine_Initialize */
static void adapt_ChallengeMachine_Initialize(ProbeState *s)
{
	ChallengeMachineInitializeResult result = ChallengeMachine_Initialize();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ChallengeMachine_Initialize */

const ProbeEntry probe_entries_challenge_machine[] = {
	{ "ChallengeMachine_CheckIfOpponentAlreadySelected", adapt_ChallengeMachine_CheckIfOpponentAlreadySelected },
	{ "ChallengeMachine_PrintText", adapt_ChallengeMachine_PrintText },
	{ "ChallengeMachine_PickOpponentSequence", adapt_ChallengeMachine_PickOpponentSequence },
	{ "ChallengeMachine_GetCurrentOpponent", adapt_ChallengeMachine_GetCurrentOpponent },
	{ "ChallengeMachine_IncrementHLMax999", adapt_ChallengeMachine_IncrementHLMax999 },
	{ "ChallengeMachine_CheckForNewRecord", adapt_ChallengeMachine_CheckForNewRecord },
	{ "ChallengeMachine_RecordDuelResult", adapt_ChallengeMachine_RecordDuelResult },
	{ "ChallengeMachine_Initialize", adapt_ChallengeMachine_Initialize },
	{ NULL, NULL },
};
