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
#endif /* POKETCG_HOME_EFFECT_FUNCTIONS_H */
