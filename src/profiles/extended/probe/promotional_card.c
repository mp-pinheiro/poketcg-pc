#include "home/promotional_card.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory _ShowPromotionalCardScreen */
static void adapt__ShowPromotionalCardScreen(ProbeState *s)
{
	_ShowPromotionalCardScreen(s->a);
}
/* <<< factory _ShowPromotionalCardScreen */

const ProbeEntry probe_entries_promotional_card[] = {
	{ "_ShowPromotionalCardScreen", adapt__ShowPromotionalCardScreen },
	{ NULL, NULL },
};
