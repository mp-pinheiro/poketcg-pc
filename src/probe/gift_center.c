#include "home/gift_center.h"
#include "probe.h"

static void adapt_Preload_GiftCenterClerk(ProbeState *s)
{
	GiftCenterPreloadResult result = Preload_GiftCenterClerk(s->f);
	s->a = result.a;
	s->f = result.f;
}

static void adapt_Func_fcad(ProbeState *s)
{
	Func_fcad();
}

const ProbeEntry probe_entries_gift_center[] = {
	{"Func_fcad", adapt_Func_fcad},
	{"Preload_GiftCenterClerk", adapt_Preload_GiftCenterClerk},
	{NULL, NULL},
};
