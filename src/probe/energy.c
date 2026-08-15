#include "home/energy.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
static void adapt_RetrievePlayAreaAIScoreFromBackup1(ProbeState *s)
{
	Backup1Result r = RetrievePlayAreaAIScoreFromBackup1();
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */

const ProbeEntry probe_entries_energy[] = {
	{ "RetrievePlayAreaAIScoreFromBackup1", adapt_RetrievePlayAreaAIScoreFromBackup1 },
	{ NULL, NULL },
};
