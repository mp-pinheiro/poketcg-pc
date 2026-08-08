#include "home/substatus.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_CheckSandAttackOrSmokescreenSubstatus(ProbeState *s)
{
	SandAttackCheckResult r = CheckSandAttackOrSmokescreenSubstatus(pair(s->d, s->e));
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_substatus[] = {
	{ "CheckSandAttackOrSmokescreenSubstatus", adapt_CheckSandAttackOrSmokescreenSubstatus },
	{ NULL, NULL },
};
