#include "home/attacks.h"
#include "probe.h"

static void adapt_RetrievePlayAreaAIScoreFromBackup2(ProbeState *s)
{
	(void)s;
	RetrievePlayAreaAIScoreFromBackup2();
}

const ProbeEntry probe_entries_attacks[] = {
	{ "RetrievePlayAreaAIScoreFromBackup2", adapt_RetrievePlayAreaAIScoreFromBackup2 },
	{ NULL, NULL },
};
