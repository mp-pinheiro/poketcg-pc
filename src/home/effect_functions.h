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
#endif /* POKETCG_HOME_EFFECT_FUNCTIONS_H */
