#ifndef POKETCG_HOME_COIN_TOSS_H
#define POKETCG_HOME_COIN_TOSS_H

#include <stdint.h>

/* poketcg/src/home/coin_toss.asm */

uint8_t CompareDEtoBC(uint8_t d, uint8_t e, uint8_t b, uint8_t c);

/* >>> factory TossCoinATimes */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} TossCoinATimesResult;

TossCoinATimesResult TossCoinATimes(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory TossCoinATimes */
/* >>> factory TossCoin */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} TossCoinRoutineResult;

TossCoinRoutineResult TossCoin(uint16_t de, uint16_t hl);
/* <<< factory TossCoin */
#endif /* POKETCG_HOME_COIN_TOSS_H */
