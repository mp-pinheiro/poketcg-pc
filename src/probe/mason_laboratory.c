#include "home/mason_laboratory.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_DrMason */
static void adapt_Preload_DrMason(ProbeState *s)
{
	PreloadDrMasonResult result = Preload_DrMason();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_DrMason */

/* >>> factory Preload_Sam */
static void adapt_Preload_Sam(ProbeState *s)
{
	PreloadSamResult result = Preload_Sam();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_Sam */

/* >>> factory Preload_Tech5 */
static void adapt_Preload_Tech5(ProbeState *s)
{
	PreloadTech5Result result = Preload_Tech5(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Preload_Tech5 */

/* >>> factory MasonLaboratoryAfterDuel */
static void adapt_MasonLaboratoryAfterDuel(ProbeState *s)
{
	MasonLaboratoryAfterDuelResult r = MasonLaboratoryAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory MasonLaboratoryAfterDuel */

/* >>> factory MasonLabCloseTextBox */
static void adapt_MasonLabCloseTextBox(ProbeState *s)
{
	(void)s;
	MasonLabCloseTextBox();
}
/* <<< factory MasonLabCloseTextBox */


/* >>> factory MasonLabLoadMap */
static void adapt_MasonLabLoadMap(ProbeState *s)
{
	(void)s;
	MasonLabLoadMap();
}
/* <<< factory MasonLabLoadMap */

/* >>> factory MasonLabPressedA */
static void adapt_MasonLabPressedA(ProbeState *s)
{
	MasonLabPressedAResult r = MasonLabPressedA(s->b, s->c, s->d, s->e, s->hl);
	s->hl = r.hl;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory MasonLabPressedA */

/* >>> factory Script_Tech1 */
static void adapt_Script_Tech1(ProbeState *s)
{
	ScriptTech1Result r = Script_Tech1();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory Script_Tech1 */

const ProbeEntry probe_entries_mason_laboratory[] = {
	{ "Script_Tech1", adapt_Script_Tech1 },
	{ "Preload_DrMason", adapt_Preload_DrMason },
	{ "Preload_Sam", adapt_Preload_Sam },
	{ "Preload_Tech5", adapt_Preload_Tech5 },
	{ "MasonLaboratoryAfterDuel", adapt_MasonLaboratoryAfterDuel },
	{ "MasonLabCloseTextBox", adapt_MasonLabCloseTextBox },
	{ "MasonLabLoadMap", adapt_MasonLabLoadMap },
	{ "MasonLabPressedA", adapt_MasonLabPressedA },
	{ NULL, NULL },
};
