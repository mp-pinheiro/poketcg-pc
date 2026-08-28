#include "home/attacks.h"
#include "probe.h"

static void adapt_RetrievePlayAreaAIScoreFromBackup2(ProbeState *s)
{
	(void)s;
	RetrievePlayAreaAIScoreFromBackup2();
}

/* >>> factory GetAIScoreOfAttack */
static void adapt_GetAIScoreOfAttack(ProbeState *s)
{
	GetAIScoreOfAttack(s->a);
}
/* <<< factory GetAIScoreOfAttack */

/* >>> factory AIProcessAttacks */
static void adapt_AIProcessAttacks(ProbeState *s)
{
	AIProcessAttacksResult result = AIProcessAttacks();
	s->f = result.f;
}
/* <<< factory AIProcessAttacks */

/* >>> factory AIProcessAndTryToUseAttack */
static void adapt_AIProcessAndTryToUseAttack(ProbeState *s)
{
	AIProcessAttacksResult result = AIProcessAndTryToUseAttack();
	s->f = result.f;
}
/* <<< factory AIProcessAndTryToUseAttack */

/* >>> factory AIProcessButDontUseAttack */
static void adapt_AIProcessButDontUseAttack(ProbeState *s)
{
	AIProcessAttacksResult result = AIProcessButDontUseAttack();
	s->f = result.f;
}
/* <<< factory AIProcessButDontUseAttack */

const ProbeEntry probe_entries_attacks[] = {
	{ "RetrievePlayAreaAIScoreFromBackup2", adapt_RetrievePlayAreaAIScoreFromBackup2 },
	{ "GetAIScoreOfAttack", adapt_GetAIScoreOfAttack },
	{ "AIProcessAttacks", adapt_AIProcessAttacks },
	{ "AIProcessAndTryToUseAttack", adapt_AIProcessAndTryToUseAttack },
	{ "AIProcessButDontUseAttack", adapt_AIProcessButDontUseAttack },
	{ NULL, NULL },
};
