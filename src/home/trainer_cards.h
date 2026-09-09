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
typedef struct { uint8_t a, f; uint16_t hl; uint8_t d; } FindDupResult;
FindDupResult FindDuplicateCards(uint16_t hl, uint8_t d);
/* <<< factory FindDuplicateCards */
/* >>> factory FindAndRemoveCardFromList */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl);
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
typedef struct { uint8_t a, f, d; } PickPokedexResult;
PickPokedexResult PickPokedexCards(void);
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Maintenance */
typedef struct { uint8_t a, f; uint8_t d; } AIDecideMaintenanceResult;
AIDecideMaintenanceResult AIDecide_Maintenance(uint8_t d);
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
typedef struct { uint8_t f; } AIDecideResult;
/* A trainer-card decision whose a register _AIProcessHandTrainerCards stores as
 * wAITrainerCardParameter when the carry says play: the asm leaves a there on
 * every exit, so every exit models it. */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideParameterResult;
AIDecideParameterResult AIDecide_Lass(uint8_t d);
/* <<< factory AIDecide_Lass */
/* >>> factory AIDecide_Recycle */
AIDecideParameterResult AIDecide_Recycle(uint8_t d);
/* <<< factory AIDecide_Recycle */
/* >>> factory AIDecide_Imakuni */
AIDecideParameterResult AIDecide_Imakuni(uint8_t d);
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_Defender_Phase14 */
AIDecideParameterResult AIDecide_Defender_Phase14(uint8_t d);
/* <<< factory AIDecide_Defender_Phase14 */
/* >>> factory AIDecide_Bill */
AIDecideParameterResult AIDecide_Bill(uint8_t d);
/* <<< factory AIDecide_Bill */
/* >>> factory AIDecide_PokemonFlute */
typedef struct { uint8_t a, f; uint8_t d; } AIDecidePokemonFluteResult;
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c, uint8_t d);
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(uint8_t d);
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */
/* >>> factory AIDecide_Gambler */
AIDecideParameterResult AIDecide_Gambler(uint8_t d);
/* <<< factory AIDecide_Gambler */
/* >>> factory AIDecide_Revive */
typedef struct { uint8_t a, f; uint8_t d; } AIDecideReviveResult;
AIDecideReviveResult AIDecide_Revive(uint8_t d);
/* <<< factory AIDecide_Revive */
/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideParameterResult AIDecide_ImposterProfessorOak(uint8_t d);
/* <<< factory AIDecide_ImposterProfessorOak */
/* >>> factory PickPokedexCards_Unreferenced */
PickPokedexResult PickPokedexCards_Unreferenced(void);
/* <<< factory PickPokedexCards_Unreferenced */
/* >>> factory AIDecide_Pokedex */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecidePokedexResult;
AIDecidePokedexResult AIDecide_Pokedex(uint8_t d);
/* <<< factory AIDecide_Pokedex */
/* >>> factory AIDecide_ItemFinder */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ItemFinderResult;
AIDecide_ItemFinderResult AIDecide_ItemFinder(uint8_t d);
/* <<< factory AIDecide_ItemFinder */
/* >>> factory AIDecide_EnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideEnergyRetrievalResult;
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a, uint8_t d);
/* <<< factory AIDecide_EnergyRetrieval */
/* >>> factory AIDecide_SuperEnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideSuperEnergyRetrievalResult;
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a, uint8_t d);
/* <<< factory AIDecide_SuperEnergyRetrieval */
/* >>> factory AIDecide_PokemonBreeder */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecidePokemonBreederResult;
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in, uint8_t d);
/* <<< factory AIDecide_PokemonBreeder */
/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_LegendaryMoltresResult;
AIDecide_PokemonTrader_LegendaryMoltresResult AIDecide_PokemonTrader_LegendaryMoltres(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */
/* >>> factory AIDecide_PokemonTrader_StrangePower */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_StrangePowerResult;
AIDecide_PokemonTrader_StrangePowerResult AIDecide_PokemonTrader_StrangePower(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_StrangePower */
/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_LegendaryArticunoResult;
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */
/* >>> factory AIDecide_ComputerSearch_FireCharge */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ComputerSearch_FireChargeResult;
AIDecide_ComputerSearch_FireChargeResult AIDecide_ComputerSearch_FireCharge(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory AIDecide_ComputerSearch_FireCharge */
/* >>> factory AIDecide_ComputerSearch_Anger */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ComputerSearch_AngerResult;
AIDecide_ComputerSearch_AngerResult AIDecide_ComputerSearch_Anger(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory AIDecide_ComputerSearch_Anger */
/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ComputerSearch_WondersOfScienceResult;
AIDecide_ComputerSearch_WondersOfScienceResult AIDecide_ComputerSearch_WondersOfScience(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */
/* >>> factory AIDecide_ComputerSearch_RockCrusher */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ComputerSearch_RockCrusherResult;
AIDecide_ComputerSearch_RockCrusherResult AIDecide_ComputerSearch_RockCrusher(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory AIDecide_ComputerSearch_RockCrusher */
/* >>> factory AIDecide_ComputerSearch */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ComputerSearchResult;
AIDecide_ComputerSearchResult AIDecide_ComputerSearch(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory AIDecide_ComputerSearch */
/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_LegendaryRonaldResult;
AIDecide_PokemonTrader_LegendaryRonaldResult AIDecide_PokemonTrader_LegendaryRonald(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */
/* >>> factory AIDecide_PokemonTrader_SoundOfTheWaves */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_SoundOfTheWavesResult;
AIDecide_PokemonTrader_SoundOfTheWavesResult AIDecide_PokemonTrader_SoundOfTheWaves(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_SoundOfTheWaves */
/* >>> factory AIDecide_PokemonTrader_LegendaryDragonite */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_LegendaryDragoniteResult;
AIDecide_PokemonTrader_LegendaryDragoniteResult AIDecide_PokemonTrader_LegendaryDragonite(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_LegendaryDragonite */
/* >>> factory AIDecide_Pokeball */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokeballResult;
AIDecide_PokeballResult AIDecide_Pokeball(uint8_t d);
/* <<< factory AIDecide_Pokeball */
/* >>> factory AIDecide_MrFuji */
AIDecideParameterResult AIDecide_MrFuji(uint8_t d);
/* <<< factory AIDecide_MrFuji */
/* >>> factory AIDecide_PokemonTrader_BlisteringPokemon */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_BlisteringPokemonResult;
AIDecide_PokemonTrader_BlisteringPokemonResult AIDecide_PokemonTrader_BlisteringPokemon(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_BlisteringPokemon */
/* >>> factory AIDecide_PokemonTrader_Flamethrower */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_FlamethrowerResult;
AIDecide_PokemonTrader_FlamethrowerResult AIDecide_PokemonTrader_Flamethrower(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_Flamethrower */
/* >>> factory AIDecide_PokemonTrader_FlowerGarden */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_FlowerGardenResult;
AIDecide_PokemonTrader_FlowerGardenResult AIDecide_PokemonTrader_FlowerGarden(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_FlowerGarden */
/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTrader_PowerGeneratorResult;
AIDecide_PokemonTrader_PowerGeneratorResult AIDecide_PokemonTrader_PowerGenerator(uint8_t d);
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */
/* >>> factory AIDecide_PokemonTrader */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PokemonTraderResult;
AIDecide_PokemonTraderResult AIDecide_PokemonTrader(uint8_t d);
/* <<< factory AIDecide_PokemonTrader */
/* >>> factory AIDecide_EnergySearch */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideEnergySearchResult;
AIDecideEnergySearchResult AIDecide_EnergySearch(uint8_t a, uint8_t d);
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
AIDecideParameterResult AIDecide_ProfessorOak(uint8_t d);
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
AIDecideParameterResult AIDecide_PlusPower_Phase14(uint8_t d);
/* <<< factory AIDecide_PlusPower_Phase14 */
/* >>> factory AIDecide_GustOfWind */
/* >>> factory AIDecide_GustOfWind */
AIDecideParameterResult AIDecide_GustOfWind(uint8_t d);
/* <<< factory AIDecide_GustOfWind */
/* >>> factory AIDecide_Defender_Phase13 */
AIDecideParameterResult AIDecide_Defender_Phase13(uint8_t d);
/* <<< factory AIDecide_Defender_Phase13 */
/* >>> factory AIDecide_Switch */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_SwitchResult;
AIDecide_SwitchResult AIDecide_Switch(uint8_t d);
/* <<< factory AIDecide_Switch */
/* >>> factory AIDecide_SuperEnergyRemoval */
AIDecideParameterResult AIDecide_SuperEnergyRemoval(uint8_t d);
/* <<< factory AIDecide_SuperEnergyRemoval */
/* >>> factory AIDecide_ScoopUp */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_ScoopUpResult;
AIDecide_ScoopUpResult AIDecide_ScoopUp(uint8_t d);
/* <<< factory AIDecide_ScoopUp */
/* >>> factory AIDecide_FullHeal */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideFullHealResult;
AIDecideFullHealResult AIDecide_FullHeal(uint8_t d);
/* <<< factory AIDecide_FullHeal */
/* >>> factory AIDecide_EnergyRemoval */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideEnergyRemovalResult;
AIDecideEnergyRemovalResult AIDecide_EnergyRemoval(uint8_t d);
/* <<< factory AIDecide_EnergyRemoval */
/* >>> factory AIDecide_PokemonCenter */
AIDecideParameterResult AIDecide_PokemonCenter(uint8_t d);
/* <<< factory AIDecide_PokemonCenter */
/* >>> factory AIDecide_PlusPower_Phase13 */
/* trainer_cards.asm:778.  Two-byte exit: the carry returns put the attack
 * index in a ($00 for the first attack, $01 for the second) while every
 * .no_carry / .unusable exit runs `or a` over whatever the last callee left
 * there, so both a and f have to be reported. */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecide_PlusPower_Phase13Result;
AIDecide_PlusPower_Phase13Result AIDecide_PlusPower_Phase13(uint8_t d);
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
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideSuperPotionPhase11Result;
AIDecideSuperPotionPhase11Result AIDecide_SuperPotion_Phase11(uint8_t d);
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
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecidePotionPhase10Result;
AIDecidePotionPhase10Result AIDecide_Potion_Phase10(uint8_t d);
/* <<< factory AIDecide_Potion_Phase10 */
/* >>> factory AIPlay_SuperPotion */
AIDecideResult AIPlay_SuperPotion(void);
/* <<< factory AIPlay_SuperPotion */
/* >>> factory AIDecide_Potion_Phase07 */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecidePotionPhase07Result;
AIDecidePotionPhase07Result AIDecide_Potion_Phase07(uint8_t d);
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
typedef struct { uint8_t a; uint8_t f; uint8_t d; } AIDecideSuperPotionPhase08Result;
AIDecideSuperPotionPhase08Result AIDecide_SuperPotion_Phase08(uint8_t d);
/* <<< factory AIDecide_SuperPotion_Phase08 */
/* >>> factory AIPlay_SuperEnergyRetrieval */
AIDecideResult AIPlay_SuperEnergyRetrieval(void);
/* <<< factory AIPlay_SuperEnergyRetrieval */
#endif /* POKETCG_HOME_TRAINER_CARDS_H */
