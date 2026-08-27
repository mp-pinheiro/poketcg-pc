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

const ProbeEntry probe_entries_attacks[] = {
	{ "RetrievePlayAreaAIScoreFromBackup2", adapt_RetrievePlayAreaAIScoreFromBackup2 },
	{ "GetAIScoreOfAttack", adapt_GetAIScoreOfAttack },
	{ NULL, NULL },
};
