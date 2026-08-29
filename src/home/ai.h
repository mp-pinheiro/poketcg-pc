#ifndef POKETCG_HOME_AI_H
#define POKETCG_HOME_AI_H

#include <stdint.h>

/* poketcg/src/home/ai.asm */

typedef struct { uint8_t a; uint16_t hl; } DeckLoadResult;
DeckLoadResult LoadOpponentDeck(void);

/* >>> factory AIDoAction */
uint8_t AIDoAction(uint8_t a);
/* <<< factory AIDoAction */
/* >>> factory AIDoAction_ForcedSwitch */
uint8_t AIDoAction_ForcedSwitch(void);
/* <<< factory AIDoAction_ForcedSwitch */
/* >>> factory AIDoAction_KOSwitch */
uint8_t AIDoAction_KOSwitch(void);
/* <<< factory AIDoAction_KOSwitch */
/* >>> factory AIDoAction_StartDuel */
uint8_t AIDoAction_StartDuel(void);
/* <<< factory AIDoAction_StartDuel */
#endif /* POKETCG_HOME_AI_H */
