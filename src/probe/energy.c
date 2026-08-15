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

/* >>> factory FindPlayAreaCardWithHighestAIScore */
static void adapt_FindPlayAreaCardWithHighestAIScore(ProbeState *s)
{
	AIScoreResult r = FindPlayAreaCardWithHighestAIScore(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FindPlayAreaCardWithHighestAIScore */

const ProbeEntry probe_entries_energy[] = {
	{ "RetrievePlayAreaAIScoreFromBackup1", adapt_RetrievePlayAreaAIScoreFromBackup1 },
	{ "FindPlayAreaCardWithHighestAIScore", adapt_FindPlayAreaCardWithHighestAIScore },
	{ NULL, NULL },
};
