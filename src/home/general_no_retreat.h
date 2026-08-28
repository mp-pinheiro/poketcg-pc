#ifndef POKETCG_HOME_GENERAL_NO_RETREAT_H
#define POKETCG_HOME_GENERAL_NO_RETREAT_H

#include <stdint.h>

/* >>> factory AIDoTurn_GeneralNoRetreat */
typedef struct { uint8_t f; } AIDoTurn_GeneralNoRetreatResult;
AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory AIDoTurn_GeneralNoRetreat */
#endif /* POKETCG_HOME_GENERAL_NO_RETREAT_H */
