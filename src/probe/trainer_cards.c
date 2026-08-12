#include "home/trainer_cards.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory RemoveCardFromList */
static void adapt_RemoveCardFromList(ProbeState *s)
{
	RemoveCardFromList(&s->hl);
}
/* <<< factory RemoveCardFromList */

const ProbeEntry probe_entries_trainer_cards[] = {
	{ "RemoveCardFromList", adapt_RemoveCardFromList },
	{ NULL, NULL },
};
