#include "home/start.h"
#include "probe.h"

static void adapt_ShowCardPopCGBDisclaimer(ProbeState *s)
{
	s->f = ShowCardPopCGBDisclaimer();
}

/* >>> factory CheckIfHasSaveData */
static void adapt_CheckIfHasSaveData(ProbeState *s)
{
	CheckIfHasSaveDataResult r = CheckIfHasSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasSaveData */

/* >>> factory PrintStartMenuDescriptionText */
static void adapt_PrintStartMenuDescriptionText(ProbeState *s)
{
	PrintStartMenuDescriptionTextResult r = PrintStartMenuDescriptionText(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PrintStartMenuDescriptionText */

/* >>> factory AskToContinueFromDiaryWithDuelData */
static void adapt_AskToContinueFromDiaryWithDuelData(ProbeState *s)
{
	AskToContinueFromDiaryWithDuelDataResult result = AskToContinueFromDiaryWithDuelData();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AskToContinueFromDiaryWithDuelData */

const ProbeEntry probe_entries_start[] = {
	{ "ShowCardPopCGBDisclaimer", adapt_ShowCardPopCGBDisclaimer },
	{ "CheckIfHasSaveData", adapt_CheckIfHasSaveData },
	{ "PrintStartMenuDescriptionText", adapt_PrintStartMenuDescriptionText },
	{ "AskToContinueFromDiaryWithDuelData", adapt_AskToContinueFromDiaryWithDuelData },
	{ NULL, NULL },
};
