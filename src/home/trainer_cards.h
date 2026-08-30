#ifndef POKETCG_HOME_TRAINER_CARDS_H
#define POKETCG_HOME_TRAINER_CARDS_H

#include <stdint.h>

/* Callee result types used by this file's declarations live in core.h
 * (AIMakeDecisionResult and friends). Packets tell a generator to "include
 * their header", but `statics` lands in the .c only, so a header fragment
 * naming a core.h type could not compile and cost four AIPlay_* attempts one
 * generation each on 2026-08-28. */
#include "home/core.h"

/* >>> factory RemoveCardFromList */
void RemoveCardFromList(uint16_t *hl);
/* <<< factory RemoveCardFromList */
/* >>> factory FindDuplicateCards */
typedef struct { uint8_t a, f; uint16_t hl; } FindDupResult;
FindDupResult FindDuplicateCards(uint16_t hl);
/* <<< factory FindDuplicateCards */
/* >>> factory FindAndRemoveCardFromList */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl);
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
typedef struct { uint8_t a, f; } PickPokedexResult;
PickPokedexResult PickPokedexCards(void);
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Maintenance */
typedef struct { uint8_t a, f; } AIDecideMaintenanceResult;
AIDecideMaintenanceResult AIDecide_Maintenance(void);
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
typedef struct { uint8_t f; } AIDecideResult;
AIDecideResult AIDecide_Lass(void);
/* <<< factory AIDecide_Lass */
/* >>> factory AIDecide_Recycle */
AIDecideResult AIDecide_Recycle(void);
/* <<< factory AIDecide_Recycle */
/* >>> factory AIDecide_Imakuni */
AIDecideResult AIDecide_Imakuni(void);
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_Defender_Phase14 */
AIDecideResult AIDecide_Defender_Phase14(void);
/* <<< factory AIDecide_Defender_Phase14 */
/* >>> factory AIDecide_Bill */
AIDecideResult AIDecide_Bill(void);
/* <<< factory AIDecide_Bill */
/* >>> factory AIDecide_PokemonFlute */
typedef struct { uint8_t a, f; } AIDecidePokemonFluteResult;
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c);
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(void);
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */
/* >>> factory AIDecide_Gambler */
AIDecideResult AIDecide_Gambler(void);
/* <<< factory AIDecide_Gambler */
/* >>> factory AIDecide_Revive */
typedef struct { uint8_t a, f; } AIDecideReviveResult;
AIDecideReviveResult AIDecide_Revive(void);
/* <<< factory AIDecide_Revive */
/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideResult AIDecide_ImposterProfessorOak(void);
/* <<< factory AIDecide_ImposterProfessorOak */
/* >>> factory PickPokedexCards_Unreferenced */
PickPokedexResult PickPokedexCards_Unreferenced(void);
/* <<< factory PickPokedexCards_Unreferenced */
/* >>> factory AIDecide_Pokedex */
typedef struct { uint8_t a; uint8_t f; } AIDecidePokedexResult;
AIDecidePokedexResult AIDecide_Pokedex(void);
/* <<< factory AIDecide_Pokedex */
/* >>> factory AIDecide_ItemFinder */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ItemFinderResult;
AIDecide_ItemFinderResult AIDecide_ItemFinder(void);
/* <<< factory AIDecide_ItemFinder */
/* >>> factory AIDecide_EnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; } AIDecideEnergyRetrievalResult;
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a);
/* <<< factory AIDecide_EnergyRetrieval */
/* >>> factory AIDecide_SuperEnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; } AIDecideSuperEnergyRetrievalResult;
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a);
/* <<< factory AIDecide_SuperEnergyRetrieval */
/* >>> factory AIDecide_PokemonBreeder */
typedef struct { uint8_t a; uint8_t f; } AIDecidePokemonBreederResult;
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in);
/* <<< factory AIDecide_PokemonBreeder */
/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_LegendaryMoltresResult;
AIDecide_PokemonTrader_LegendaryMoltresResult AIDecide_PokemonTrader_LegendaryMoltres(void);
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */
/* >>> factory AIDecide_PokemonTrader_StrangePower */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_StrangePowerResult;
AIDecide_PokemonTrader_StrangePowerResult AIDecide_PokemonTrader_StrangePower(void);
/* <<< factory AIDecide_PokemonTrader_StrangePower */
/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_LegendaryArticunoResult;
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(void);
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */
/* >>> factory AIDecide_ComputerSearch_FireCharge */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ComputerSearch_FireChargeResult;
AIDecide_ComputerSearch_FireChargeResult AIDecide_ComputerSearch_FireCharge(uint8_t b, uint8_t c);
/* <<< factory AIDecide_ComputerSearch_FireCharge */
/* >>> factory AIDecide_ComputerSearch_Anger */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ComputerSearch_AngerResult;
AIDecide_ComputerSearch_AngerResult AIDecide_ComputerSearch_Anger(uint8_t b, uint8_t c);
/* <<< factory AIDecide_ComputerSearch_Anger */
/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ComputerSearch_WondersOfScienceResult;
AIDecide_ComputerSearch_WondersOfScienceResult AIDecide_ComputerSearch_WondersOfScience(uint8_t b, uint8_t c);
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */
/* >>> factory AIDecide_ComputerSearch_RockCrusher */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ComputerSearch_RockCrusherResult;
AIDecide_ComputerSearch_RockCrusherResult AIDecide_ComputerSearch_RockCrusher(uint8_t b, uint8_t c);
/* <<< factory AIDecide_ComputerSearch_RockCrusher */
/* >>> factory AIDecide_ComputerSearch */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ComputerSearchResult;
AIDecide_ComputerSearchResult AIDecide_ComputerSearch(uint8_t b, uint8_t c);
/* <<< factory AIDecide_ComputerSearch */
/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_LegendaryRonaldResult;
AIDecide_PokemonTrader_LegendaryRonaldResult AIDecide_PokemonTrader_LegendaryRonald(void);
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */
/* >>> factory AIDecide_PokemonTrader_SoundOfTheWaves */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_SoundOfTheWavesResult;
AIDecide_PokemonTrader_SoundOfTheWavesResult AIDecide_PokemonTrader_SoundOfTheWaves(void);
/* <<< factory AIDecide_PokemonTrader_SoundOfTheWaves */
/* >>> factory AIDecide_PokemonTrader_LegendaryDragonite */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_LegendaryDragoniteResult;
AIDecide_PokemonTrader_LegendaryDragoniteResult AIDecide_PokemonTrader_LegendaryDragonite(void);
/* <<< factory AIDecide_PokemonTrader_LegendaryDragonite */
/* >>> factory AIDecide_Pokeball */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokeballResult;
AIDecide_PokeballResult AIDecide_Pokeball(void);
/* <<< factory AIDecide_Pokeball */
/* >>> factory AIDecide_MrFuji */
AIDecideResult AIDecide_MrFuji(void);
/* <<< factory AIDecide_MrFuji */
/* >>> factory AIDecide_PokemonTrader_BlisteringPokemon */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_BlisteringPokemonResult;
AIDecide_PokemonTrader_BlisteringPokemonResult AIDecide_PokemonTrader_BlisteringPokemon(void);
/* <<< factory AIDecide_PokemonTrader_BlisteringPokemon */
/* >>> factory AIDecide_PokemonTrader_Flamethrower */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_FlamethrowerResult;
AIDecide_PokemonTrader_FlamethrowerResult AIDecide_PokemonTrader_Flamethrower(void);
/* <<< factory AIDecide_PokemonTrader_Flamethrower */
/* >>> factory AIDecide_PokemonTrader_FlowerGarden */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_FlowerGardenResult;
AIDecide_PokemonTrader_FlowerGardenResult AIDecide_PokemonTrader_FlowerGarden(void);
/* <<< factory AIDecide_PokemonTrader_FlowerGarden */
/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTrader_PowerGeneratorResult;
AIDecide_PokemonTrader_PowerGeneratorResult AIDecide_PokemonTrader_PowerGenerator(void);
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */
/* >>> factory AIDecide_PokemonTrader */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PokemonTraderResult;
AIDecide_PokemonTraderResult AIDecide_PokemonTrader(void);
/* <<< factory AIDecide_PokemonTrader */
/* >>> factory AIDecide_EnergySearch */
typedef struct { uint8_t a; uint8_t f; } AIDecideEnergySearchResult;
AIDecideEnergySearchResult AIDecide_EnergySearch(uint8_t a);
/* <<< factory AIDecide_EnergySearch */
/* >>> factory _AIProcessHandTrainerCards */
typedef struct { uint8_t a; uint8_t f; } AIProcessHandTrainerCardsResult;
AIProcessHandTrainerCardsResult _AIProcessHandTrainerCards(uint8_t a);
/* <<< factory _AIProcessHandTrainerCards */
/* >>> factory AIPlay_Pokeball */
typedef struct { uint8_t f; } AIPlayPokeballResult;
AIPlayPokeballResult AIPlay_Pokeball(void);
/* <<< factory AIPlay_Pokeball */
/* >>> factory AIPlay_Recycle */
AIDecideResult AIPlay_Recycle(void);
/* <<< factory AIPlay_Recycle */

/* >>> factory AIPlay_Bill */
/* trainer_cards.asm:1420-1425. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_Bill(void);
/* <<< factory AIPlay_Bill */
/* >>> factory AIPlay_Defender */
/* trainer_cards.asm:594-601. Stage-only twin of AIPlay_Bill with the extra
 * PLAY_AREA_ARENA byte: wAITrainerCardToPlay goes to hTempCardIndex_ff9f and
 * 0 to hTemp_ffa0, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch; exit f
 * is AIMakeDecision's carry. */
AIDecideResult AIPlay_Defender(void);
/* <<< factory AIPlay_Defender */
/* >>> factory AIPlay_Imakuni */
/* trainer_cards.asm:4520-4525. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_Imakuni(void);
/* <<< factory AIPlay_Imakuni */
/* >>> factory AIPlay_FullHeal */
/* trainer_cards.asm:3771-3776. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_FullHeal(void);
/* <<< factory AIPlay_FullHeal */
/* >>> factory AIDecide_ProfessorOak */
AIDecideResult AIDecide_ProfessorOak(void);
/* <<< factory AIDecide_ProfessorOak */
/* >>> factory AIPlay_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4776-4781. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_ClefairyDollOrMysteriousFossil(void);
/* <<< factory AIPlay_ClefairyDollOrMysteriousFossil */
/* >>> factory AIPlay_ImposterProfessorOak */
/* trainer_cards.asm:3182-3187. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_ImposterProfessorOak(void);
/* <<< factory AIPlay_ImposterProfessorOak */
/* >>> factory AIPlay_PokemonCenter */
/* trainer_cards.asm:3083-3088. Stage-only twin: wAITrainerCardToPlay goes to
 * hTempCardIndex_ff9f, then the OPPACTION_EXECUTE_TRAINER_EFFECTS dispatch;
 * exit f is AIMakeDecision's carry. */
AIDecideResult AIPlay_PokemonCenter(void);
/* <<< factory AIPlay_PokemonCenter */
/* >>> factory AIDecide_PlusPower_Phase14 */
AIDecideResult AIDecide_PlusPower_Phase14(void);
/* <<< factory AIDecide_PlusPower_Phase14 */
/* >>> factory AIDecide_GustOfWind */
/* >>> factory AIDecide_GustOfWind */
AIDecideResult AIDecide_GustOfWind(void);
/* <<< factory AIDecide_GustOfWind */
/* >>> factory AIDecide_Defender_Phase13 */
AIDecideResult AIDecide_Defender_Phase13(void);
/* <<< factory AIDecide_Defender_Phase13 */
/* >>> factory AIDecide_Switch */
typedef struct { uint8_t a; uint8_t f; } AIDecide_SwitchResult;
AIDecide_SwitchResult AIDecide_Switch(void);
/* <<< factory AIDecide_Switch */
/* >>> factory AIDecide_SuperEnergyRemoval */
AIDecideResult AIDecide_SuperEnergyRemoval(void);
/* <<< factory AIDecide_SuperEnergyRemoval */
/* >>> factory AIDecide_ScoopUp */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ScoopUpResult;
AIDecide_ScoopUpResult AIDecide_ScoopUp(void);
/* <<< factory AIDecide_ScoopUp */
/* >>> factory AIDecide_FullHeal */
typedef struct { uint8_t a; uint8_t f; } AIDecideFullHealResult;
AIDecideFullHealResult AIDecide_FullHeal(void);
/* <<< factory AIDecide_FullHeal */
/* >>> factory AIDecide_EnergyRemoval */
typedef struct { uint8_t a; uint8_t f; } AIDecideEnergyRemovalResult;
AIDecideEnergyRemovalResult AIDecide_EnergyRemoval(void);
/* <<< factory AIDecide_EnergyRemoval */
/* >>> factory AIDecide_PokemonCenter */
AIDecideResult AIDecide_PokemonCenter(void);
/* <<< factory AIDecide_PokemonCenter */
/* >>> factory AIDecide_PlusPower_Phase13 */
/* trainer_cards.asm:778.  Two-byte exit: the carry returns put the attack
 * index in a ($00 for the first attack, $01 for the second) while every
 * .no_carry / .unusable exit runs `or a` over whatever the last callee left
 * there, so both a and f have to be reported. */
typedef struct { uint8_t a; uint8_t f; } AIDecide_PlusPower_Phase13Result;
AIDecide_PlusPower_Phase13Result AIDecide_PlusPower_Phase13(void);
/* <<< factory AIDecide_PlusPower_Phase13 */
/* >>> factory AIPlay_PlusPower */
AIDecideResult AIPlay_PlusPower(void);
/* <<< factory AIPlay_PlusPower */
/* >>> factory AIPlay_Potion */
/* >>> factory AIPlay_Potion */
AIDecideResult AIPlay_Potion(void);
/* <<< factory AIPlay_Potion */
/* >>> factory AIPlay_GustOfWind */
AIDecideResult AIPlay_GustOfWind(void);
/* <<< factory AIPlay_GustOfWind */
/* >>> factory AIPlay_Switch */
AIDecideResult AIPlay_Switch(void);
/* <<< factory AIPlay_Switch */
/* >>> factory AIPlay_Maintenance */
/* >>> factory AIPlay_Maintenance */
AIDecideResult AIPlay_Maintenance(void);
/* <<< factory AIPlay_Maintenance */
/* >>> factory AIPlay_ComputerSearch */
AIDecideResult AIPlay_ComputerSearch(void);
/* <<< factory AIPlay_ComputerSearch */
/* >>> factory AIPlay_ItemFinder */
AIDecideResult AIPlay_ItemFinder(void);
/* <<< factory AIPlay_ItemFinder */
/* >>> factory AIPlay_Pokedex */
AIDecideResult AIPlay_Pokedex(void);
/* <<< factory AIPlay_Pokedex */
/* >>> factory AIPlay_Gambler */
AIDecideResult AIPlay_Gambler(void);
/* <<< factory AIPlay_Gambler */
/* >>> factory AIPlay_EnergyRetrieval */
AIDecideResult AIPlay_EnergyRetrieval(void);
/* <<< factory AIPlay_EnergyRetrieval */
/* >>> factory AIPlay_SuperEnergyRemoval */
AIDecideResult AIPlay_SuperEnergyRemoval(void);
/* <<< factory AIPlay_SuperEnergyRemoval */
/* >>> factory AIDecide_SuperPotion_Phase11 */
typedef struct { uint8_t a; uint8_t f; } AIDecideSuperPotionPhase11Result;
AIDecideSuperPotionPhase11Result AIDecide_SuperPotion_Phase11(void);
/* <<< factory AIDecide_SuperPotion_Phase11 */
/* >>> factory AIPlay_EnergySearch */
/* trainer_cards.asm:3218-3233 */
AIDecideResult AIPlay_EnergySearch(void);
/* <<< factory AIPlay_EnergySearch */
/* >>> factory AIPlay_ScoopUp */
AIDecideResult AIPlay_ScoopUp(void);
/* <<< factory AIPlay_ScoopUp */
/* >>> factory AIPlay_PokemonBreeder */
AIDecideResult AIPlay_PokemonBreeder(void);
/* <<< factory AIPlay_PokemonBreeder */
/* >>> factory AIPlay_PokemonFlute */
AIDecideResult AIPlay_PokemonFlute(void);
/* <<< factory AIPlay_PokemonFlute */
/* >>> factory AIPlay_ProfessorOak */
AIDecideResult AIPlay_ProfessorOak(void);
/* <<< factory AIPlay_ProfessorOak */
/* >>> factory AIPlay_PokemonTrader */
AIMakeDecisionResult AIPlay_PokemonTrader(void);
/* <<< factory AIPlay_PokemonTrader */
/* >>> factory AIPlay_EnergyRemoval */
AIDecideResult AIPlay_EnergyRemoval(void);
/* <<< factory AIPlay_EnergyRemoval */
/* >>> factory AIDecide_Potion_Phase10 */
typedef struct { uint8_t a; uint8_t f; } AIDecidePotionPhase10Result;
AIDecidePotionPhase10Result AIDecide_Potion_Phase10(void);
/* <<< factory AIDecide_Potion_Phase10 */
/* >>> factory AIPlay_SuperPotion */
AIDecideResult AIPlay_SuperPotion(void);
/* <<< factory AIPlay_SuperPotion */
/* >>> factory AIDecide_Potion_Phase07 */
typedef struct { uint8_t a; uint8_t f; } AIDecidePotionPhase07Result;
AIDecidePotionPhase07Result AIDecide_Potion_Phase07(void);
/* <<< factory AIDecide_Potion_Phase07 */
/* >>> factory AIPlay_Revive */
AIDecideResult AIPlay_Revive(void);
/* <<< factory AIPlay_Revive */
/* >>> factory AIPlay_Lass */
AIDecideResult AIPlay_Lass(void);
/* <<< factory AIPlay_Lass */
/* >>> factory AIPlay_MrFuji */
AIDecideResult AIPlay_MrFuji(void);
/* <<< factory AIPlay_MrFuji */
/* >>> factory AIDecide_SuperPotion_Phase08 */
typedef struct { uint8_t a; uint8_t f; } AIDecideSuperPotionPhase08Result;
AIDecideSuperPotionPhase08Result AIDecide_SuperPotion_Phase08(void);
/* <<< factory AIDecide_SuperPotion_Phase08 */
#endif /* POKETCG_HOME_TRAINER_CARDS_H */
