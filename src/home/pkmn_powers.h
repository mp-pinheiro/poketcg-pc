#ifndef POKETCG_HOME_PKMN_POWERS_H
#define POKETCG_HOME_PKMN_POWERS_H

#include <stdint.h>

/* >>> factory HandleAIShift */
typedef struct { uint8_t a; uint8_t f; } AIShiftResult;
AIShiftResult HandleAIShift(uint8_t c);
/* <<< factory HandleAIShift */
/* >>> factory HandleAIPeek */
typedef struct { uint8_t a; uint8_t f; } AIPeekResult;
AIPeekResult HandleAIPeek(uint8_t c);
/* <<< factory HandleAIPeek */
/* >>> factory HandleAIStrangeBehavior */
typedef struct { uint8_t a; uint8_t f; } HandleAIStrangeBehaviorResult;
HandleAIStrangeBehaviorResult HandleAIStrangeBehavior(uint8_t c);
/* <<< factory HandleAIStrangeBehavior */
/* >>> factory HandleAICurse */
typedef struct { uint8_t a; uint8_t f; } HandleAICurseResult;
HandleAICurseResult HandleAICurse(uint8_t c);
/* <<< factory HandleAICurse */
/* >>> factory HandleAIDamageSwap */
typedef struct { uint8_t a; uint8_t f; } HandleAIDamageSwapResult;
HandleAIDamageSwapResult HandleAIDamageSwap(uint8_t f);
/* <<< factory HandleAIDamageSwap */
/* >>> factory HandleAIHeal */
typedef struct { uint8_t a; uint8_t f; } HandleAIHealResult;
HandleAIHealResult HandleAIHeal(uint8_t c);
/* <<< factory HandleAIHeal */
/* >>> factory HandleAIPkmnPowers */
typedef struct { uint8_t a; uint8_t f; } HandleAIPkmnPowersResult;
HandleAIPkmnPowersResult HandleAIPkmnPowers(void);
/* <<< factory HandleAIPkmnPowers */
#endif /* POKETCG_HOME_PKMN_POWERS_H */
