#include "home/card_pop.h"
#include "generated/wram.h"
#include "probe.h"

static void adapt_CreateCardPopCandidateList(ProbeState *s)
{
	s->a = CreateCardPopCandidateList(s->a);
	s->hl = wCardPopCardCandidates_ADDR;
}

static void adapt_CalculateNameHash(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CalculateNameHash(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

const ProbeEntry probe_entries_card_pop[] = {
	{ "CreateCardPopCandidateList", adapt_CreateCardPopCandidateList },
	{ "CalculateNameHash", adapt_CalculateNameHash },
	{ NULL, NULL },
};
