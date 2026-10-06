#ifndef POKETCG_HOME_GENERAL_H
#define POKETCG_HOME_GENERAL_H

#include <stdint.h>

/* >>> factory AIProcessRetreat */
typedef struct { uint8_t a; uint8_t f; } AIProcessRetreatResult;
AIProcessRetreatResult AIProcessRetreat(void);
/* <<< factory AIProcessRetreat */
/* >>> factory AIMainTurnLogic */
typedef struct { uint8_t f; } AIMainTurnLogicResult;
AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory AIMainTurnLogic */
#endif /* POKETCG_HOME_GENERAL_H */
