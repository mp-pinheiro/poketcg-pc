#include "home/gift_center.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_GiftCenterClerk */
static void adapt_Preload_GiftCenterClerk(ProbeState *s)
{
	PreloadGiftCenterClerkResult result = Preload_GiftCenterClerk();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_GiftCenterClerk */


/* >>> factory Func_fc7a */
static void adapt_Func_fc7a(ProbeState *s)
{
	Func_fc7aResult r = Func_fc7a();
	s->a = r.a;
	s->c = r.c;
}
/* <<< factory Func_fc7a */

/* >>> factory Func_fcad */
static void adapt_Func_fcad(ProbeState *s)
{
	Func_fcadResult r = Func_fcad();
	s->a = r.a;
	s->c = r.c;
}
/* <<< factory Func_fcad */

const ProbeEntry probe_entries_gift_center[] = {
	{ "Preload_GiftCenterClerk", adapt_Preload_GiftCenterClerk },
	{ "Func_fc7a", adapt_Func_fc7a },
	{ "Func_fcad", adapt_Func_fcad },
	{ NULL, NULL },
};
