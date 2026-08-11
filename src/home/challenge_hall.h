#ifndef POKETCG_HOME_CHALLENGE_HALL_H
#define POKETCG_HOME_CHALLENGE_HALL_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeHallClearResult;

typedef struct {
	uint8_t b;
	uint16_t hl;
} ChallengeHallBitResult;

ChallengeHallClearResult Func_f5db(void);
ChallengeHallBitResult Func_f5e9(uint8_t c);
void Script_Host(void);

#endif
