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

/* >>> factory FindDuplicateCards */
static void adapt_FindDuplicateCards(ProbeState *s)
{
	FindDupResult r = FindDuplicateCards(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FindDuplicateCards */


/* >>> factory FindAndRemoveCardFromList */
static void adapt_FindAndRemoveCardFromList(ProbeState *s)
{
	FindAndRemoveCardFromList(s->a, s->hl);
}
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
static void adapt_PickPokedexCards(ProbeState *s)
{
	PickPokedexResult r = PickPokedexCards();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Maintenance */
static void adapt_AIDecide_Maintenance(ProbeState *s)
{
	AIDecideMaintenanceResult r = AIDecide_Maintenance();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_Maintenance */

/* >>> factory AIDecide_Lass */
static void adapt_AIDecide_Lass(ProbeState *s)
{
	s->f = AIDecide_Lass().f;
}
/* <<< factory AIDecide_Lass */

/* >>> factory AIDecide_Imakuni */
static void adapt_AIDecide_Imakuni(ProbeState *s)
{
	s->f = AIDecide_Imakuni().f;
}
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_PokemonFlute */
static void adapt_AIDecide_PokemonFlute(ProbeState *s)
{
	AIDecidePokemonFluteResult r = AIDecide_PokemonFlute(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
static void adapt_AIDecide_ClefairyDollOrMysteriousFossil(ProbeState *s)
{
	AIDecidePokemonFluteResult r = AIDecide_ClefairyDollOrMysteriousFossil();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */
/* >>> factory AIDecide_Defender_Phase14 */
static void adapt_AIDecide_Defender_Phase14(ProbeState *s)
{
	s->f = AIDecide_Defender_Phase14().f;
}
/* <<< factory AIDecide_Defender_Phase14 */
/* >>> factory AIDecide_Bill */
static void adapt_AIDecide_Bill(ProbeState *s)
{
	s->f = AIDecide_Bill().f;
}
/* <<< factory AIDecide_Bill */

const ProbeEntry probe_entries_trainer_cards[] = {
	{ "RemoveCardFromList", adapt_RemoveCardFromList },
	{ "FindAndRemoveCardFromList", adapt_FindAndRemoveCardFromList },
	{ "PickPokedexCards", adapt_PickPokedexCards },
	{ "AIDecide_Maintenance", adapt_AIDecide_Maintenance },
	{ "AIDecide_Lass", adapt_AIDecide_Lass },
	{ "AIDecide_Imakuni", adapt_AIDecide_Imakuni },
	{ "AIDecide_Defender_Phase14", adapt_AIDecide_Defender_Phase14 },
	{ "AIDecide_Bill", adapt_AIDecide_Bill },
	{ "AIDecide_PokemonFlute", adapt_AIDecide_PokemonFlute },
	{ "AIDecide_ClefairyDollOrMysteriousFossil", adapt_AIDecide_ClefairyDollOrMysteriousFossil },
	{ "FindDuplicateCards", adapt_FindDuplicateCards },
	{ NULL, NULL },
};
