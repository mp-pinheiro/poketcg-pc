#include "home/deck_configuration.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DecrementDeckCardsInCollection */
static void adapt_DecrementDeckCardsInCollection(ProbeState *s)
{
	s->hl = DecrementDeckCardsInCollection(s->hl);
}
/* <<< factory DecrementDeckCardsInCollection */


/* >>> factory AddDeckToCollection */
static void adapt_AddDeckToCollection(ProbeState *s)
{
	s->hl = AddDeckToCollection(s->hl);
}
/* <<< factory AddDeckToCollection */


/* >>> factory CopyListFromHLToDE */
static void adapt_CopyListFromHLToDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyListFromHLToDE(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyListFromHLToDE */


const ProbeEntry probe_entries_deck_configuration[] = {
	{ "DecrementDeckCardsInCollection", adapt_DecrementDeckCardsInCollection },
	{ "AddDeckToCollection", adapt_AddDeckToCollection },
	{ "CopyListFromHLToDE", adapt_CopyListFromHLToDE },
	{ NULL, NULL },
};
