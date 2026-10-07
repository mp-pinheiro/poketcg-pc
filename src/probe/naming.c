/* >>> part includes */
#include "home/naming.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory DisplayPlayerNamingScreen */
static void adapt_DisplayPlayerNamingScreen(ProbeState *s)
{
	DisplayPlayerNamingScreenResult r = DisplayPlayerNamingScreen();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DisplayPlayerNamingScreen */

/* >>> part probe_entries_naming */
const ProbeEntry probe_entries_naming[] = {
	{ "DisplayPlayerNamingScreen", adapt_DisplayPlayerNamingScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_naming */
