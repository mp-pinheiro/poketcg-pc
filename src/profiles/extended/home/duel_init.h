#ifndef POKETCG_HOME_DUEL_INIT_H
#define POKETCG_HOME_DUEL_INIT_H

#include <stdint.h>

/* >>> factory Duel_Init */
typedef struct { uint8_t a; uint8_t f; } DuelInitResult;
DuelInitResult Duel_Init(uint8_t f);
/* <<< factory Duel_Init */
#endif /* POKETCG_HOME_DUEL_INIT_H */
