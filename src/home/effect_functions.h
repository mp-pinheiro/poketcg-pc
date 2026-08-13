#ifndef POKETCG_HOME_EFFECT_FUNCTIONS_H
#define POKETCG_HOME_EFFECT_FUNCTIONS_H

#include <stdint.h>

/* >>> factory UpdateExpectedAIDamage */
void UpdateExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory UpdateExpectedAIDamage */
/* >>> factory SetExpectedAIDamage */
void SetExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory SetExpectedAIDamage */
/* >>> factory IsPlayerTurn */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } IsPlayerTurnResult;
IsPlayerTurnResult IsPlayerTurn(void);
/* <<< factory IsPlayerTurn */
/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
void UpdateExpectedAIDamage_AccountForPoison(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */
/* >>> factory ApplySubstatus1ToAttackingCard */
uint16_t ApplySubstatus1ToAttackingCard(uint8_t a);
/* <<< factory ApplySubstatus1ToAttackingCard */
/* >>> factory SetNoEffectFromStatus */
void SetNoEffectFromStatus(void);
/* <<< factory SetNoEffectFromStatus */
/* >>> factory SetDefiniteAIDamage */
void SetDefiniteAIDamage(void);
/* <<< factory SetDefiniteAIDamage */
/* >>> factory PickRandomPlayAreaCard */
typedef struct { uint8_t a; uint8_t f; } PickRandomPlayAreaCardResult;
PickRandomPlayAreaCardResult PickRandomPlayAreaCard(void);
/* <<< factory PickRandomPlayAreaCard */
/* >>> factory GetNextPositionInTempList */
uint16_t GetNextPositionInTempList(void);
/* <<< factory GetNextPositionInTempList */
/* >>> factory QueueStatusCondition */
typedef struct { uint8_t f; } QueueStatusConditionResult;
QueueStatusConditionResult QueueStatusCondition(uint8_t b, uint8_t c);
/* <<< factory QueueStatusCondition */
/* >>> factory CommentedOut_2c086 */
uint8_t CommentedOut_2c086(uint8_t a);
/* <<< factory CommentedOut_2c086 */
/* >>> factory SetWasUnsuccessful */
void SetWasUnsuccessful(void);
/* <<< factory SetWasUnsuccessful */
/* >>> factory Teleport_SwitchEffect */
/* >>> factory Teleport_SwitchEffect */
void Teleport_SwitchEffect(void);
/* <<< factory Teleport_SwitchEffect */
/* >>> factory SetDamageToATimes20 */
/* >>> factory SetDamageToATimes20 */
void SetDamageToATimes20(uint8_t a);
/* <<< factory SetDamageToATimes20 */
/* >>> factory CreateTrainerCardListFromDiscardPile */
typedef struct { uint16_t hl; uint8_t f; } CreateTrainerCardListFromDiscardPileResult;
CreateTrainerCardListFromDiscardPileResult CreateTrainerCardListFromDiscardPile(void);
/* <<< factory CreateTrainerCardListFromDiscardPile */
/* >>> factory CreateEnergyCardListFromDiscardPile */
typedef struct { uint16_t hl; uint8_t f; } CreateEnergyCardListFromDiscardPileResult;
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile(uint8_t c);
/* <<< factory CreateEnergyCardListFromDiscardPile */
/* >>> factory GetAttackName */
uint16_t GetAttackName(uint8_t d, uint8_t e);
/* <<< factory GetAttackName */
/* >>> factory ClefableMinimizeEffect */
uint16_t ClefableMinimizeEffect(void);
/* <<< factory ClefableMinimizeEffect */
/* >>> factory HandleAIMetronomeEffect */
void HandleAIMetronomeEffect(void);
/* <<< factory HandleAIMetronomeEffect */
/* >>> factory ParalysisEffect */
QueueStatusConditionResult ParalysisEffect(void);
/* <<< factory ParalysisEffect */
/* >>> factory ConfusionEffect */
QueueStatusConditionResult ConfusionEffect(void);
/* <<< factory ConfusionEffect */
/* >>> factory InvisibleWallEffect */
uint8_t InvisibleWallEffect(uint8_t f);
/* <<< factory InvisibleWallEffect */
/* >>> factory CheckIfDefendingPokemonHasAnyAttack */
typedef struct { uint8_t f; } CheckAttackResult;
CheckAttackResult CheckIfDefendingPokemonHasAnyAttack(void);
/* <<< factory CheckIfDefendingPokemonHasAnyAttack */
/* >>> factory UpdateDevolvedCardHPAndStage */
void UpdateDevolvedCardHPAndStage(uint8_t a);
/* <<< factory UpdateDevolvedCardHPAndStage */
/* >>> factory DodrioRage_DamageBoostEffect */
void DodrioRage_DamageBoostEffect(void);
/* <<< factory DodrioRage_DamageBoostEffect */
/* >>> factory DragonairSlam_AIEffect */
void DragonairSlam_AIEffect(void);
/* <<< factory DragonairSlam_AIEffect */
/* >>> factory CheckIfPlayAreaHasAnyDamage */
typedef struct { uint8_t f; uint16_t hl; } CheckIfPlayAreaHasAnyDamageResult;
CheckIfPlayAreaHasAnyDamageResult CheckIfPlayAreaHasAnyDamage(void);
/* <<< factory CheckIfPlayAreaHasAnyDamage */
/* >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile_OnlyBasic(void);
/* <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
/* >>> factory KabutoArmorEffect */
uint8_t KabutoArmorEffect(uint8_t f);
/* <<< factory KabutoArmorEffect */
/* >>> factory CuboneRage_DamageBoostEffect */
void CuboneRage_DamageBoostEffect(void);
/* <<< factory CuboneRage_DamageBoostEffect */
/* >>> factory PoisonEffect */
QueueStatusConditionResult PoisonEffect(void);
/* <<< factory PoisonEffect */
/* >>> factory DoublePoisonEffect */
QueueStatusConditionResult DoublePoisonEffect(void);
/* <<< factory DoublePoisonEffect */
/* >>> factory LoadCardNameAndInputColor */
void LoadCardNameAndInputColor(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory LoadCardNameAndInputColor */
/* >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon */
typedef struct { uint8_t a; } AIPickEnergyCardToDiscardResult;
AIPickEnergyCardToDiscardResult AIPickEnergyCardToDiscardFromDefendingPokemon(void);
/* <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon */
/* >>> factory AIFindTargetForBenchAttack */
typedef struct { uint8_t a; } AIFindTargetForBenchAttackResult;
AIFindTargetForBenchAttackResult AIFindTargetForBenchAttack(void);
/* <<< factory AIFindTargetForBenchAttack */
/* >>> factory ApplyExtraWaterEnergyDamageBonus */
void ApplyExtraWaterEnergyDamageBonus(uint8_t b, uint8_t c);
/* <<< factory ApplyExtraWaterEnergyDamageBonus */
/* >>> factory OmastarSpikeCannon_AIEffect */
void OmastarSpikeCannon_AIEffect(void);
/* <<< factory OmastarSpikeCannon_AIEffect */
/* >>> factory ClairvoyanceEffect */
uint8_t ClairvoyanceEffect(uint8_t f);
/* <<< factory ClairvoyanceEffect */
/* >>> factory KrabbyCallForFamily_AISelectEffect */
void KrabbyCallForFamily_AISelectEffect(uint8_t c, uint16_t de);
/* <<< factory KrabbyCallForFamily_AISelectEffect */
/* >>> factory CreateListOfEnergyAttachedToArena */
typedef struct { uint8_t a; uint8_t c; uint16_t hl; uint8_t f; } CreateListOfEnergyAttachedToArenaResult;
CreateListOfEnergyAttachedToArenaResult CreateListOfEnergyAttachedToArena(uint8_t a);
/* <<< factory CreateListOfEnergyAttachedToArena */
/* >>> factory HandleNoDamageOrEffect */
typedef struct { uint8_t f; uint16_t hl; } HandleNoDamageOrEffectResult;
HandleNoDamageOrEffectResult HandleNoDamageOrEffect(uint16_t hl);
/* <<< factory HandleNoDamageOrEffect */
#endif /* POKETCG_HOME_EFFECT_FUNCTIONS_H */
