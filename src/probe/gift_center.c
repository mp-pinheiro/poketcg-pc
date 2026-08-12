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

const ProbeEntry probe_entries_gift_center[] = {
	{ "Preload_GiftCenterClerk", adapt_Preload_GiftCenterClerk },
	{ NULL, NULL },
};
