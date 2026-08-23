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
/* >>> factory AIDecide_Recycle */
static void adapt_AIDecide_Recycle(ProbeState *s)
{
	s->f = AIDecide_Recycle().f;
}
/* <<< factory AIDecide_Recycle */
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


/* >>> factory AIDecide_Gambler */
static void adapt_AIDecide_Gambler(ProbeState *s)
{
	s->f = AIDecide_Gambler().f;
}
/* <<< factory AIDecide_Gambler */

/* >>> factory AIDecide_Revive */
static void adapt_AIDecide_Revive(ProbeState *s)
{
	AIDecideReviveResult result = AIDecide_Revive();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIDecide_Revive */

/* >>> factory AIDecide_ImposterProfessorOak */
static void adapt_AIDecide_ImposterProfessorOak(ProbeState *s)
{
	s->f = AIDecide_ImposterProfessorOak().f;
}
/* <<< factory AIDecide_ImposterProfessorOak */

/* >>> factory PickPokedexCards_Unreferenced */
static void adapt_PickPokedexCards_Unreferenced(ProbeState *s)
{
	PickPokedexResult r = PickPokedexCards_Unreferenced();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PickPokedexCards_Unreferenced */

/* >>> factory AIDecide_Pokedex */
static void adapt_AIDecide_Pokedex(ProbeState *s)
{
	AIDecidePokedexResult r = AIDecide_Pokedex();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_Pokedex */

/* >>> factory AIDecide_ItemFinder */
static void adapt_AIDecide_ItemFinder(ProbeState *s)
{
	AIDecide_ItemFinderResult r = AIDecide_ItemFinder();
	s->a = r.a; s->f = r.f;
}
/* <<< factory AIDecide_ItemFinder */

/* >>> factory AIDecide_EnergyRetrieval */
static void adapt_AIDecide_EnergyRetrieval(ProbeState *s)
{
	AIDecideEnergyRetrievalResult r = AIDecide_EnergyRetrieval(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_EnergyRetrieval */

/* >>> factory AIDecide_SuperEnergyRetrieval */
static void adapt_AIDecide_SuperEnergyRetrieval(ProbeState *s)
{
	AIDecideSuperEnergyRetrievalResult r = AIDecide_SuperEnergyRetrieval(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_SuperEnergyRetrieval */

/* >>> factory AIDecide_PokemonBreeder */
static void adapt_AIDecide_PokemonBreeder(ProbeState *s)
{
	AIDecidePokemonBreederResult r = AIDecide_PokemonBreeder(s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonBreeder */

/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
static void adapt_AIDecide_PokemonTrader_LegendaryMoltres(ProbeState *s)
{
	AIDecide_PokemonTrader_LegendaryMoltresResult r = AIDecide_PokemonTrader_LegendaryMoltres();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */

/* >>> factory AIDecide_PokemonTrader_StrangePower */
static void adapt_AIDecide_PokemonTrader_StrangePower(ProbeState *s)
{
	AIDecide_PokemonTrader_StrangePowerResult r = AIDecide_PokemonTrader_StrangePower();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_StrangePower */

const ProbeEntry probe_entries_trainer_cards[] = {
	{ "FindAndRemoveCardFromList", adapt_FindAndRemoveCardFromList },
	{ "PickPokedexCards", adapt_PickPokedexCards },
	{ "AIDecide_Recycle", adapt_AIDecide_Recycle },
	{ "AIDecide_Maintenance", adapt_AIDecide_Maintenance },
	{ "AIDecide_Lass", adapt_AIDecide_Lass },
	{ "AIDecide_Imakuni", adapt_AIDecide_Imakuni },
	{ "AIDecide_PokemonFlute", adapt_AIDecide_PokemonFlute },
	{ "AIDecide_ClefairyDollOrMysteriousFossil", adapt_AIDecide_ClefairyDollOrMysteriousFossil },
	{ "FindDuplicateCards", adapt_FindDuplicateCards },
	{ "AIDecide_Gambler", adapt_AIDecide_Gambler },
	{ "AIDecide_Revive", adapt_AIDecide_Revive },
	{ "AIDecide_Defender_Phase14", adapt_AIDecide_Defender_Phase14 },
	{ "AIDecide_Bill", adapt_AIDecide_Bill },
	{ "RemoveCardFromList", adapt_RemoveCardFromList },
	{ "AIDecide_ImposterProfessorOak", adapt_AIDecide_ImposterProfessorOak },
	{ "PickPokedexCards_Unreferenced", adapt_PickPokedexCards_Unreferenced },
	{ "AIDecide_Pokedex", adapt_AIDecide_Pokedex },
	{ "AIDecide_ItemFinder", adapt_AIDecide_ItemFinder },
	{ "AIDecide_EnergyRetrieval", adapt_AIDecide_EnergyRetrieval },
	{ "AIDecide_SuperEnergyRetrieval", adapt_AIDecide_SuperEnergyRetrieval },
	{ "AIDecide_PokemonBreeder", adapt_AIDecide_PokemonBreeder },
	{ "AIDecide_PokemonTrader_LegendaryMoltres", adapt_AIDecide_PokemonTrader_LegendaryMoltres },
	{ "AIDecide_PokemonTrader_StrangePower", adapt_AIDecide_PokemonTrader_StrangePower },
	{ NULL, NULL },
};
