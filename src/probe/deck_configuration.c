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


/* >>> factory CalculateOnesAndTensDigits */
static void adapt_CalculateOnesAndTensDigits(ProbeState *s)
{
	CalculateOnesAndTensDigits(s->a);
}
/* <<< factory CalculateOnesAndTensDigits */




/* >>> factory InitCardSelectionParams */
static void adapt_InitCardSelectionParams(ProbeState *s)
{
	s->a = InitCardSelectionParams(s->a, &s->hl);
}
/* <<< factory InitCardSelectionParams */


/* >>> factory ClearMemory_Bank2 */
static void adapt_ClearMemory_Bank2(ProbeState *s)
{
	ClearMemory_Bank2(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank2 */

/* >>> factory CheckIfHasOtherValidDecks */
static void adapt_CheckIfHasOtherValidDecks(ProbeState *s)
{
	s->f = CheckIfHasOtherValidDecks();
}
/* <<< factory CheckIfHasOtherValidDecks */

/* >>> factory FillDEWithA */
static void adapt_FillDEWithA(ProbeState *s)
{
	FillDEWithA(s->a, s->b, (uint16_t)(s->d << 8 | s->e));
	s->b = 0;
	s->f = (uint8_t)(0xC0u | (s->f & 0x10u));
}
/* <<< factory FillDEWithA */

/* >>> factory DrawHandCardsTileAtDE */
static void adapt_DrawHandCardsTileAtDE(ProbeState *s)
{
	DrawHandCardsTileAtDE((uint16_t)((uint16_t)s->d << 8 | s->e));
}
/* <<< factory DrawHandCardsTileAtDE */

/* >>> factory CountNumberOfCardsOfType */
static void adapt_CountNumberOfCardsOfType(ProbeState *s)
{
	uint8_t input_type = s->a;
	s->a = CountNumberOfCardsOfType(input_type);
	s->b = input_type;
	s->c = s->a;
}
/* <<< factory CountNumberOfCardsOfType */

/* >>> factory CopyNBytesFromHLToDE */
static void adapt_CopyNBytesFromHLToDE(ProbeState *s)
{
	uint16_t hl = s->hl;
	uint16_t de = (uint16_t)(((uint16_t)s->d << 8) | s->e);
	CopyNBytesFromHLToDE(&hl, &de, s->b);
	s->hl = hl;
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyNBytesFromHLToDE */

/* >>> factory IncrementDeckCardsInTempCollection */
static void adapt_IncrementDeckCardsInTempCollection(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	IncrementDeckCardsInTempCollection(de);
}
/* <<< factory IncrementDeckCardsInTempCollection */

/* >>> factory CreateCardCollectionListWithDeckCards */
static void adapt_CreateCardCollectionListWithDeckCards(ProbeState *s)
{
	CreateCardCollectionListWithDeckCards(s->a);
}
/* <<< factory CreateCardCollectionListWithDeckCards */

const ProbeEntry probe_entries_deck_configuration[] = {
	{ "DecrementDeckCardsInCollection", adapt_DecrementDeckCardsInCollection },
	{ "AddDeckToCollection", adapt_AddDeckToCollection },
	{ "CopyListFromHLToDE", adapt_CopyListFromHLToDE },
	{ "InitCardSelectionParams", adapt_InitCardSelectionParams },
	{ "CalculateOnesAndTensDigits", adapt_CalculateOnesAndTensDigits },
	{ "ClearMemory_Bank2", adapt_ClearMemory_Bank2 },
	{ "CheckIfHasOtherValidDecks", adapt_CheckIfHasOtherValidDecks },
	{ "FillDEWithA", adapt_FillDEWithA },
	{ "DrawHandCardsTileAtDE", adapt_DrawHandCardsTileAtDE },
	{ "CountNumberOfCardsOfType", adapt_CountNumberOfCardsOfType },
	{ "CopyNBytesFromHLToDE", adapt_CopyNBytesFromHLToDE },
	{ "IncrementDeckCardsInTempCollection", adapt_IncrementDeckCardsInTempCollection },
	{ "CreateCardCollectionListWithDeckCards", adapt_CreateCardCollectionListWithDeckCards },
	{ NULL, NULL },
};
