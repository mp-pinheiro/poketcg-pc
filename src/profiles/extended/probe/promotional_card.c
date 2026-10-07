/* >>> part includes */
#include "home/promotional_card.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> part probe_card_id */
static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}
/* <<< part probe_card_id */

/* >>> factory _ShowPromotionalCardScreen */
static void adapt__ShowPromotionalCardScreen(ProbeState *s)
{
	_ShowPromotionalCardScreen(probe_card_id(s));
}
/* <<< factory _ShowPromotionalCardScreen */

/* >>> part probe_entries_promotional_card */
const ProbeEntry probe_entries_promotional_card[] = {
	{ "_ShowPromotionalCardScreen", adapt__ShowPromotionalCardScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_promotional_card */
