/* --- factory AIDecide_Defender_Phase14 */
/* --- factory PickPokedexCards_Unreferenced */
/* === factory AIPlay_Bill */
/* >>> part AIDecide_Defender1 */
static void adapt_AIDecide_Defender1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_Defender1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_Defender1 */
/* >>> part AIDecide_Defender2 */
static void adapt_AIDecide_Defender2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_Defender2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_Defender2 */
/* >>> part AIDecide_PlusPower1 */
static void adapt_AIDecide_PlusPower1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_PlusPower1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_PlusPower1 */
/* >>> part AIDecide_PlusPower2 */
static void adapt_AIDecide_PlusPower2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_PlusPower2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_PlusPower2 */
/* >>> part AIDecide_SuperPotion1 */
static void adapt_AIDecide_SuperPotion1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_SuperPotion1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_SuperPotion1 */
/* >>> part AIDecide_SuperPotion2 */
static void adapt_AIDecide_SuperPotion2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_SuperPotion2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_SuperPotion2 */
/* --- factory AIDecide_PlusPower_Phase14 */
/* --- factory AIDecide_Defender_Phase13 */
/* --- factory AIDecide_PlusPower_Phase13 */
/* --- factory AIDecide_SuperPotion_Phase11 */
/* --- factory AIDecide_SuperPotion_Phase08 */
/* >>> part probe_entries_trainer_cards */
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
	{ "AIDecide_Bill", adapt_AIDecide_Bill },
	{ "RemoveCardFromList", adapt_RemoveCardFromList },
	{ "AIDecide_ImposterProfessorOak", adapt_AIDecide_ImposterProfessorOak },
	{ "AIDecide_Pokedex", adapt_AIDecide_Pokedex },
	{ "AIDecide_ItemFinder", adapt_AIDecide_ItemFinder },
	{ "AIDecide_ProfessorOak", adapt_AIDecide_ProfessorOak },
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
	{ "AIDecide_Defender1", adapt_AIDecide_Defender1 },
	{ "AIDecide_Defender2", adapt_AIDecide_Defender2 },
	{ "AIDecide_PlusPower1", adapt_AIDecide_PlusPower1 },
	{ "AIDecide_PlusPower2", adapt_AIDecide_PlusPower2 },
	{ "AIDecide_SuperPotion1", adapt_AIDecide_SuperPotion1 },
	{ "AIDecide_SuperPotion2", adapt_AIDecide_SuperPotion2 },
	{ "AIPlay_Defender", adapt_AIPlay_Defender },
	{ "AIPlay_Imakuni", adapt_AIPlay_Imakuni },
	{ "AIPlay_FullHeal", adapt_AIPlay_FullHeal },
	{ "AIPlay_ClefairyDollOrMysteriousFossil", adapt_AIPlay_ClefairyDollOrMysteriousFossil },
	{ "AIPlay_ImposterProfessorOak", adapt_AIPlay_ImposterProfessorOak },
	{ "AIPlay_PokemonCenter", adapt_AIPlay_PokemonCenter },
	{ "AIDecide_GustOfWind", adapt_AIDecide_GustOfWind },
	{ "AIDecide_Switch", adapt_AIDecide_Switch },
	{ "AIDecide_SuperEnergyRemoval", adapt_AIDecide_SuperEnergyRemoval },
	{ "AIDecide_ScoopUp", adapt_AIDecide_ScoopUp },
	{ "AIDecide_FullHeal", adapt_AIDecide_FullHeal },
	{ "AIDecide_EnergyRemoval", adapt_AIDecide_EnergyRemoval },
	{ "AIDecide_PokemonCenter", adapt_AIDecide_PokemonCenter },
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
	{ "AIPlay_SuperEnergyRetrieval", adapt_AIPlay_SuperEnergyRetrieval },
	{ NULL, NULL },
};
/* <<< part probe_entries_trainer_cards */
