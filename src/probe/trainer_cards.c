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

/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
static void adapt_AIDecide_PokemonTrader_LegendaryArticuno(ProbeState *s)
{
	AIDecide_PokemonTrader_LegendaryArticunoResult r = AIDecide_PokemonTrader_LegendaryArticuno();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */

/* >>> factory AIDecide_ComputerSearch_FireCharge */
static void adapt_AIDecide_ComputerSearch_FireCharge(ProbeState *s)
{
	AIDecide_ComputerSearch_FireChargeResult r = AIDecide_ComputerSearch_FireCharge(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ComputerSearch_FireCharge */

/* >>> factory AIDecide_ComputerSearch_Anger */
static void adapt_AIDecide_ComputerSearch_Anger(ProbeState *s)
{
	AIDecide_ComputerSearch_AngerResult r = AIDecide_ComputerSearch_Anger(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ComputerSearch_Anger */

/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
static void adapt_AIDecide_ComputerSearch_WondersOfScience(ProbeState *s)
{
	AIDecide_ComputerSearch_WondersOfScienceResult r = AIDecide_ComputerSearch_WondersOfScience(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */

/* >>> factory AIDecide_ComputerSearch_RockCrusher */
static void adapt_AIDecide_ComputerSearch_RockCrusher(ProbeState *s)
{
	AIDecide_ComputerSearch_RockCrusherResult r = AIDecide_ComputerSearch_RockCrusher(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ComputerSearch_RockCrusher */

/* >>> factory AIDecide_ComputerSearch */
static void adapt_AIDecide_ComputerSearch(ProbeState *s)
{
	AIDecide_ComputerSearchResult r = AIDecide_ComputerSearch(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ComputerSearch */

/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
static void adapt_AIDecide_PokemonTrader_LegendaryRonald(ProbeState *s)
{
	AIDecide_PokemonTrader_LegendaryRonaldResult r = AIDecide_PokemonTrader_LegendaryRonald();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */

/* >>> factory AIDecide_PokemonTrader_SoundOfTheWaves */
static void adapt_AIDecide_PokemonTrader_SoundOfTheWaves(ProbeState *s)
{
	AIDecide_PokemonTrader_SoundOfTheWavesResult r = AIDecide_PokemonTrader_SoundOfTheWaves();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_SoundOfTheWaves */

/* >>> factory AIDecide_PokemonTrader_LegendaryDragonite */
static void adapt_AIDecide_PokemonTrader_LegendaryDragonite(ProbeState *s)
{
	AIDecide_PokemonTrader_LegendaryDragoniteResult r = AIDecide_PokemonTrader_LegendaryDragonite();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_LegendaryDragonite */

/* >>> factory AIDecide_Pokeball */
static void adapt_AIDecide_Pokeball(ProbeState *s)
{
	AIDecide_PokeballResult r = AIDecide_Pokeball();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_Pokeball */

/* >>> factory AIDecide_MrFuji */
static void adapt_AIDecide_MrFuji(ProbeState *s)
{
	(void)s;
	AIDecideResult r = AIDecide_MrFuji();
	s->f = r.f;
}
/* <<< factory AIDecide_MrFuji */

/* >>> factory AIDecide_PokemonTrader_BlisteringPokemon */
static void adapt_AIDecide_PokemonTrader_BlisteringPokemon(ProbeState *s)
{
	AIDecide_PokemonTrader_BlisteringPokemonResult r = AIDecide_PokemonTrader_BlisteringPokemon();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_BlisteringPokemon */

/* >>> factory AIDecide_PokemonTrader_Flamethrower */
static void adapt_AIDecide_PokemonTrader_Flamethrower(ProbeState *s)
{
	AIDecide_PokemonTrader_FlamethrowerResult r = AIDecide_PokemonTrader_Flamethrower();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_Flamethrower */

/* >>> factory AIDecide_PokemonTrader_FlowerGarden */
static void adapt_AIDecide_PokemonTrader_FlowerGarden(ProbeState *s)
{
	AIDecide_PokemonTrader_FlowerGardenResult r = AIDecide_PokemonTrader_FlowerGarden();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_FlowerGarden */

/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
static void adapt_AIDecide_PokemonTrader_PowerGenerator(ProbeState *s)
{
	AIDecide_PokemonTrader_PowerGeneratorResult r = AIDecide_PokemonTrader_PowerGenerator();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */

/* >>> factory AIDecide_PokemonTrader */
static void adapt_AIDecide_PokemonTrader(ProbeState *s)
{
	AIDecide_PokemonTraderResult r = AIDecide_PokemonTrader();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_PokemonTrader */

/* >>> factory AIDecide_EnergySearch */
static void adapt_AIDecide_EnergySearch(ProbeState *s)
{
	AIDecideEnergySearchResult r = AIDecide_EnergySearch(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_EnergySearch */

/* >>> factory _AIProcessHandTrainerCards */
static void adapt__AIProcessHandTrainerCards(ProbeState *s)
{
	AIProcessHandTrainerCardsResult r = _AIProcessHandTrainerCards(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory _AIProcessHandTrainerCards */

/* >>> factory AIPlay_Pokeball */
static void adapt_AIPlay_Pokeball(ProbeState *s)
{
	AIPlayPokeballResult result = AIPlay_Pokeball();
	s->f = result.f;
}
/* <<< factory AIPlay_Pokeball */

/* >>> factory AIPlay_Recycle */
static void adapt_AIPlay_Recycle(ProbeState *s)
{
	AIDecideResult result = AIPlay_Recycle();
	s->f = result.f;
}
/* <<< factory AIPlay_Recycle */

/* >>> factory AIPlay_Bill */
static void adapt_AIPlay_Bill(ProbeState *s)
{
	AIDecideResult result = AIPlay_Bill();
	s->f = result.f;
}
/* <<< factory AIPlay_Bill */

/* >>> factory AIPlay_Defender */
static void adapt_AIPlay_Defender(ProbeState *s)
{
	AIDecideResult result = AIPlay_Defender();
	s->f = result.f;
}
/* <<< factory AIPlay_Defender */

/* >>> factory AIPlay_Imakuni */
static void adapt_AIPlay_Imakuni(ProbeState *s)
{
	AIDecideResult result = AIPlay_Imakuni();
	s->f = result.f;
}
/* <<< factory AIPlay_Imakuni */

/* >>> factory AIPlay_FullHeal */
static void adapt_AIPlay_FullHeal(ProbeState *s)
{
	AIDecideResult result = AIPlay_FullHeal();
	s->f = result.f;
}
/* <<< factory AIPlay_FullHeal */

/* >>> factory AIPlay_ClefairyDollOrMysteriousFossil */
static void adapt_AIPlay_ClefairyDollOrMysteriousFossil(ProbeState *s)
{
	AIDecideResult result = AIPlay_ClefairyDollOrMysteriousFossil();
	s->f = result.f;
}
/* <<< factory AIPlay_ClefairyDollOrMysteriousFossil */

/* >>> factory AIPlay_ImposterProfessorOak */
static void adapt_AIPlay_ImposterProfessorOak(ProbeState *s)
{
	AIDecideResult result = AIPlay_ImposterProfessorOak();
	s->f = result.f;
}
/* <<< factory AIPlay_ImposterProfessorOak */

/* >>> factory AIPlay_PokemonCenter */
static void adapt_AIPlay_PokemonCenter(ProbeState *s)
{
	AIDecideResult result = AIPlay_PokemonCenter();
	s->f = result.f;
}
/* <<< factory AIPlay_PokemonCenter */


/* >>> factory AIDecide_PlusPower_Phase14 */
static void adapt_AIDecide_PlusPower_Phase14(ProbeState *s)
{
	AIDecideResult result = AIDecide_PlusPower_Phase14();
	s->f = result.f;
}
/* <<< factory AIDecide_PlusPower_Phase14 */

/* >>> factory AIDecide_GustOfWind */
static void adapt_AIDecide_GustOfWind(ProbeState *s)
{
	s->f = AIDecide_GustOfWind().f;
}
/* <<< factory AIDecide_GustOfWind */

/* >>> factory AIDecide_Defender_Phase13 */
static void adapt_AIDecide_Defender_Phase13(ProbeState *s)
{
	AIDecideResult r = AIDecide_Defender_Phase13();
	s->f = r.f;
}
/* <<< factory AIDecide_Defender_Phase13 */

/* >>> factory AIDecide_Switch */
static void adapt_AIDecide_Switch(ProbeState *s)
{
	AIDecide_SwitchResult r = AIDecide_Switch();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_Switch */

/* >>> factory AIDecide_SuperEnergyRemoval */
static void adapt_AIDecide_SuperEnergyRemoval(ProbeState *s)
{
	s->f = AIDecide_SuperEnergyRemoval().f;
}
/* <<< factory AIDecide_SuperEnergyRemoval */

/* >>> factory AIDecide_ScoopUp */
static void adapt_AIDecide_ScoopUp(ProbeState *s)
{
	AIDecide_ScoopUpResult r = AIDecide_ScoopUp();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_ScoopUp */

/* >>> factory AIDecide_FullHeal */
static void adapt_AIDecide_FullHeal(ProbeState *s)
{
	AIDecideFullHealResult result = AIDecide_FullHeal();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIDecide_FullHeal */

/* >>> factory AIDecide_EnergyRemoval */
static void adapt_AIDecide_EnergyRemoval(ProbeState *s)
{
	AIDecideEnergyRemovalResult r = AIDecide_EnergyRemoval();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_EnergyRemoval */

/* >>> factory AIDecide_PokemonCenter */
static void adapt_AIDecide_PokemonCenter(ProbeState *s)
{
	s->f = AIDecide_PokemonCenter().f;
}
/* <<< factory AIDecide_PokemonCenter */

/* >>> factory AIDecide_PlusPower_Phase13 */
static void adapt_AIDecide_PlusPower_Phase13(ProbeState *s)
{
	AIDecide_PlusPower_Phase13Result result = AIDecide_PlusPower_Phase13();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIDecide_PlusPower_Phase13 */

/* >>> factory AIPlay_PlusPower */
static void adapt_AIPlay_PlusPower(ProbeState *s)
{
	AIDecideResult result = AIPlay_PlusPower();
	s->f = result.f;
}
/* <<< factory AIPlay_PlusPower */

/* >>> factory AIPlay_Potion */
static void adapt_AIPlay_Potion(ProbeState *s)
{
	AIDecideResult result = AIPlay_Potion();
	s->f = result.f;
}
/* <<< factory AIPlay_Potion */

/* >>> factory AIPlay_GustOfWind */
static void adapt_AIPlay_GustOfWind(ProbeState *s)
{
	AIDecideResult result = AIPlay_GustOfWind();
	s->f = result.f;
}
/* <<< factory AIPlay_GustOfWind */

/* >>> factory AIPlay_Switch */
static void adapt_AIPlay_Switch(ProbeState *s)
{
	AIDecideResult r = AIPlay_Switch();
	s->f = r.f;
}
/* <<< factory AIPlay_Switch */

/* >>> factory AIPlay_Maintenance */
static void adapt_AIPlay_Maintenance(ProbeState *s)
{
	AIDecideResult result = AIPlay_Maintenance();
	s->f = result.f;
}
/* <<< factory AIPlay_Maintenance */

/* >>> factory AIPlay_ComputerSearch */
static void adapt_AIPlay_ComputerSearch(ProbeState *s)
{
	AIDecideResult result = AIPlay_ComputerSearch();
	s->f = result.f;
}
/* <<< factory AIPlay_ComputerSearch */

/* >>> factory AIPlay_ItemFinder */
static void adapt_AIPlay_ItemFinder(ProbeState *s)
{
	AIDecideResult result = AIPlay_ItemFinder();
	s->f = result.f;
}
/* <<< factory AIPlay_ItemFinder */

/* >>> factory AIPlay_Pokedex */
static void adapt_AIPlay_Pokedex(ProbeState *s)
{
	AIDecideResult result = AIPlay_Pokedex();
	s->f = result.f;
}
/* <<< factory AIPlay_Pokedex */

/* >>> factory AIPlay_Gambler */
static void adapt_AIPlay_Gambler(ProbeState *s)
{
	AIDecideResult result = AIPlay_Gambler();
	s->f = result.f;
}
/* <<< factory AIPlay_Gambler */

/* >>> factory AIPlay_EnergyRetrieval */
static void adapt_AIPlay_EnergyRetrieval(ProbeState *s)
{
	AIDecideResult result = AIPlay_EnergyRetrieval();
	s->f = result.f;
}
/* <<< factory AIPlay_EnergyRetrieval */

/* >>> factory AIPlay_SuperEnergyRemoval */
static void adapt_AIPlay_SuperEnergyRemoval(ProbeState *s)
{
	AIDecideResult result = AIPlay_SuperEnergyRemoval();
	s->f = result.f;
}
/* <<< factory AIPlay_SuperEnergyRemoval */

/* >>> factory AIDecide_SuperPotion_Phase11 */
static void adapt_AIDecide_SuperPotion_Phase11(ProbeState *s)
{
	AIDecideSuperPotionPhase11Result r = AIDecide_SuperPotion_Phase11();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIDecide_SuperPotion_Phase11 */

/* >>> factory AIPlay_EnergySearch */
static void adapt_AIPlay_EnergySearch(ProbeState *s)
{
	AIDecideResult result = AIPlay_EnergySearch();
	s->f = result.f;
}
/* <<< factory AIPlay_EnergySearch */

/* >>> factory AIPlay_ScoopUp */
static void adapt_AIPlay_ScoopUp(ProbeState *s)
{
	AIDecideResult result = AIPlay_ScoopUp();
	s->f = result.f;
}
/* <<< factory AIPlay_ScoopUp */

/* >>> factory AIPlay_PokemonBreeder */
static void adapt_AIPlay_PokemonBreeder(ProbeState *s)
{
	AIDecideResult result = AIPlay_PokemonBreeder();
	s->f = result.f;
}
/* <<< factory AIPlay_PokemonBreeder */

/* >>> factory AIPlay_PokemonFlute */
static void adapt_AIPlay_PokemonFlute(ProbeState *s)
{
	AIDecideResult result = AIPlay_PokemonFlute();
	s->f = result.f;
}
/* <<< factory AIPlay_PokemonFlute */

/* >>> factory AIPlay_ProfessorOak */
static void adapt_AIPlay_ProfessorOak(ProbeState *s)
{
	AIDecideResult result = AIPlay_ProfessorOak();
	s->f = result.f;
}
/* <<< factory AIPlay_ProfessorOak */

/* >>> factory AIPlay_PokemonTrader */
static void adapt_AIPlay_PokemonTrader(ProbeState *s)
{
	AIMakeDecisionResult result = AIPlay_PokemonTrader();
	s->f = result.f;
}
/* <<< factory AIPlay_PokemonTrader */

/* >>> factory AIPlay_EnergyRemoval */
static void adapt_AIPlay_EnergyRemoval(ProbeState *s)
{
	s->f = AIPlay_EnergyRemoval().f;
}
/* <<< factory AIPlay_EnergyRemoval */

/* >>> factory AIDecide_Potion_Phase10 */
static void adapt_AIDecide_Potion_Phase10(ProbeState *s)
{
	AIDecidePotionPhase10Result result = AIDecide_Potion_Phase10();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIDecide_Potion_Phase10 */

/* >>> factory AIPlay_SuperPotion */
static void adapt_AIPlay_SuperPotion(ProbeState *s)
{
	AIDecideResult result = AIPlay_SuperPotion();
	s->f = result.f;
}
/* <<< factory AIPlay_SuperPotion */

/* >>> factory AIDecide_Potion_Phase07 */
static void adapt_AIDecide_Potion_Phase07(ProbeState *s)
{
	AIDecidePotionPhase07Result result = AIDecide_Potion_Phase07();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIDecide_Potion_Phase07 */

/* >>> factory AIPlay_Revive */
static void adapt_AIPlay_Revive(ProbeState *s)
{
	AIDecideResult result = AIPlay_Revive();
	s->f = result.f;
}
/* <<< factory AIPlay_Revive */

/* >>> factory AIPlay_Lass */
static void adapt_AIPlay_Lass(ProbeState *s)
{
	AIDecideResult result = AIPlay_Lass();
	s->f = result.f;
}
/* <<< factory AIPlay_Lass */

/* >>> factory AIPlay_MrFuji */
static void adapt_AIPlay_MrFuji(ProbeState *s)
{
	AIDecideResult result = AIPlay_MrFuji();
	s->f = result.f;
}
/* <<< factory AIPlay_MrFuji */

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
	{ "AIDecide_PokemonTrader_LegendaryArticuno", adapt_AIDecide_PokemonTrader_LegendaryArticuno },
	{ "AIDecide_ComputerSearch_FireCharge", adapt_AIDecide_ComputerSearch_FireCharge },
	{ "AIDecide_ComputerSearch_Anger", adapt_AIDecide_ComputerSearch_Anger },
	{ "AIDecide_ComputerSearch_WondersOfScience", adapt_AIDecide_ComputerSearch_WondersOfScience },
	{ "AIDecide_ComputerSearch_RockCrusher", adapt_AIDecide_ComputerSearch_RockCrusher },
	{ "AIDecide_ComputerSearch", adapt_AIDecide_ComputerSearch },
	{ "AIDecide_PokemonTrader_LegendaryRonald", adapt_AIDecide_PokemonTrader_LegendaryRonald },
	{ "AIDecide_PokemonTrader_SoundOfTheWaves", adapt_AIDecide_PokemonTrader_SoundOfTheWaves },
	{ "AIDecide_PokemonTrader_LegendaryDragonite", adapt_AIDecide_PokemonTrader_LegendaryDragonite },
	{ "AIDecide_Pokeball", adapt_AIDecide_Pokeball },
	{ "AIDecide_MrFuji", adapt_AIDecide_MrFuji },
	{ "AIDecide_PokemonTrader_BlisteringPokemon", adapt_AIDecide_PokemonTrader_BlisteringPokemon },
	{ "AIDecide_PokemonTrader_Flamethrower", adapt_AIDecide_PokemonTrader_Flamethrower },
	{ "AIDecide_PokemonTrader_FlowerGarden", adapt_AIDecide_PokemonTrader_FlowerGarden },
	{ "AIDecide_PokemonTrader_PowerGenerator", adapt_AIDecide_PokemonTrader_PowerGenerator },
	{ "AIDecide_PokemonTrader", adapt_AIDecide_PokemonTrader },
	{ "AIDecide_EnergySearch", adapt_AIDecide_EnergySearch },
	{ "_AIProcessHandTrainerCards", adapt__AIProcessHandTrainerCards },
	{ "AIPlay_Pokeball", adapt_AIPlay_Pokeball },
	{ "AIPlay_Recycle", adapt_AIPlay_Recycle },
	{ "AIPlay_Bill", adapt_AIPlay_Bill },
	{ "AIPlay_Defender", adapt_AIPlay_Defender },
	{ "AIPlay_Imakuni", adapt_AIPlay_Imakuni },
	{ "AIPlay_FullHeal", adapt_AIPlay_FullHeal },
	{ "AIPlay_ClefairyDollOrMysteriousFossil", adapt_AIPlay_ClefairyDollOrMysteriousFossil },
	{ "AIPlay_ImposterProfessorOak", adapt_AIPlay_ImposterProfessorOak },
	{ "AIPlay_PokemonCenter", adapt_AIPlay_PokemonCenter },
	{ "AIDecide_PlusPower_Phase14", adapt_AIDecide_PlusPower_Phase14 },
	{ "AIDecide_GustOfWind", adapt_AIDecide_GustOfWind },
	{ "AIDecide_Defender_Phase13", adapt_AIDecide_Defender_Phase13 },
	{ "AIDecide_Switch", adapt_AIDecide_Switch },
	{ "AIDecide_SuperEnergyRemoval", adapt_AIDecide_SuperEnergyRemoval },
	{ "AIDecide_ScoopUp", adapt_AIDecide_ScoopUp },
	{ "AIDecide_FullHeal", adapt_AIDecide_FullHeal },
	{ "AIDecide_EnergyRemoval", adapt_AIDecide_EnergyRemoval },
	{ "AIDecide_PokemonCenter", adapt_AIDecide_PokemonCenter },
	{ "AIDecide_PlusPower_Phase13", adapt_AIDecide_PlusPower_Phase13 },
	{ "AIPlay_PlusPower", adapt_AIPlay_PlusPower },
	{ "AIPlay_Potion", adapt_AIPlay_Potion },
	{ "AIPlay_GustOfWind", adapt_AIPlay_GustOfWind },
	{ "AIPlay_Switch", adapt_AIPlay_Switch },
	{ "AIPlay_Maintenance", adapt_AIPlay_Maintenance },
	{ "AIPlay_ComputerSearch", adapt_AIPlay_ComputerSearch },
	{ "AIPlay_ItemFinder", adapt_AIPlay_ItemFinder },
	{ "AIPlay_Pokedex", adapt_AIPlay_Pokedex },
	{ "AIPlay_Gambler", adapt_AIPlay_Gambler },
	{ "AIPlay_EnergyRetrieval", adapt_AIPlay_EnergyRetrieval },
	{ "AIPlay_SuperEnergyRemoval", adapt_AIPlay_SuperEnergyRemoval },
	{ "AIDecide_SuperPotion_Phase11", adapt_AIDecide_SuperPotion_Phase11 },
	{ "AIPlay_EnergySearch", adapt_AIPlay_EnergySearch },
	{ "AIPlay_ScoopUp", adapt_AIPlay_ScoopUp },
	{ "AIPlay_PokemonBreeder", adapt_AIPlay_PokemonBreeder },
	{ "AIPlay_PokemonFlute", adapt_AIPlay_PokemonFlute },
	{ "AIPlay_ProfessorOak", adapt_AIPlay_ProfessorOak },
	{ "AIPlay_PokemonTrader", adapt_AIPlay_PokemonTrader },
	{ "AIPlay_EnergyRemoval", adapt_AIPlay_EnergyRemoval },
	{ "AIDecide_Potion_Phase10", adapt_AIDecide_Potion_Phase10 },
	{ "AIPlay_SuperPotion", adapt_AIPlay_SuperPotion },
	{ "AIDecide_Potion_Phase07", adapt_AIDecide_Potion_Phase07 },
	{ "AIPlay_Revive", adapt_AIPlay_Revive },
	{ "AIPlay_Lass", adapt_AIPlay_Lass },
	{ "AIPlay_MrFuji", adapt_AIPlay_MrFuji },
	{ NULL, NULL },
};
