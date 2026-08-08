#ifndef POKETCG_HOME_AI_H
#define POKETCG_HOME_AI_H

#include <stdint.h>

/* poketcg/src/home/ai.asm */

typedef struct { uint8_t a; uint16_t hl; } DeckLoadResult;
DeckLoadResult LoadOpponentDeck(void);

#endif /* POKETCG_HOME_AI_H */
