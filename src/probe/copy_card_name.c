#include "home/copy_card_name.h"
#include "probe.h"

/* >>> factory _CopyCardNameAndLevel_HalfwidthText */
static void adapt__CopyCardNameAndLevel_HalfwidthText(ProbeState *s)
{
	/* stack[0] is the caller's `push bc`, stack[1] its `push de`: push order,
	 * so the routine's first pop reads the last word. */
	CopyCardNameAndLevelResult result =
		_CopyCardNameAndLevel_HalfwidthText(s->stack[0], s->stack[1]);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory _CopyCardNameAndLevel_HalfwidthText */

const ProbeEntry probe_entries_copy_card_name[] = {
	{ "_CopyCardNameAndLevel_HalfwidthText", adapt__CopyCardNameAndLevel_HalfwidthText },
	{NULL, NULL},
};
