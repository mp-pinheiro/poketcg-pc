#include "home/ishiharas_house.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_NikkiInIshiharasHouse */
static void adapt_Preload_NikkiInIshiharasHouse(ProbeState *s)
{
	PreloadNikkiInIshiharasHouseResult r = Preload_NikkiInIshiharasHouse();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_NikkiInIshiharasHouse */

/* >>> factory Preload_IshiharaInIshiharasHouse */
static void adapt_Preload_IshiharaInIshiharasHouse(ProbeState *s)
{
	PreloadIshiharaInIshiharasHouseResult r = Preload_IshiharaInIshiharasHouse();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_IshiharaInIshiharasHouse */

/* >>> factory Preload_Ronald1InIshiharasHouse */
static void adapt_Preload_Ronald1InIshiharasHouse(ProbeState *s)
{
	PreloadRonald1InIshiharasHouseResult r = Preload_Ronald1InIshiharasHouse();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Ronald1InIshiharasHouse */

const ProbeEntry probe_entries_ishiharas_house[] = {
	{ "Preload_NikkiInIshiharasHouse", adapt_Preload_NikkiInIshiharasHouse },
	{ "Preload_IshiharaInIshiharasHouse", adapt_Preload_IshiharaInIshiharasHouse },
	{ "Preload_Ronald1InIshiharasHouse", adapt_Preload_Ronald1InIshiharasHouse },
	{ NULL, NULL },
};
