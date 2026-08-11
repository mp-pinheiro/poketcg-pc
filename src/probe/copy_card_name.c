#include "home/copy_card_name.h"
#include "probe.h"

static void adapt_CopyCardNameAndLevel_HalfwidthText(ProbeState *s)
{
	CopyCardNameResult result = _CopyCardNameAndLevel_HalfwidthText();
	s->a = result.a;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_copy_card_name[] = {
	{"_CopyCardNameAndLevel_HalfwidthText", adapt_CopyCardNameAndLevel_HalfwidthText},
	{NULL, NULL},
};
