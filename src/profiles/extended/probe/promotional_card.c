#include "home/promotional_card.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}

static void adapt__ShowPromotionalCardScreen(ProbeState *s)
{
	_ShowPromotionalCardScreen(probe_card_id(s));
}
/* <<< factory _ShowPromotionalCardScreen */

const ProbeEntry probe_entries_promotional_card[] = {
	{ "_ShowPromotionalCardScreen", adapt__ShowPromotionalCardScreen },
	{ NULL, NULL },
};
