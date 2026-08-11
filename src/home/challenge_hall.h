#ifndef POKETCG_HOME_CHALLENGE_HALL_H
#define POKETCG_HOME_CHALLENGE_HALL_H

#include <stdint.h>

typedef struct {
	uint16_t hl;
	uint8_t b;
} FuncF5E9Result;

void Func_f5db(void);
FuncF5E9Result Func_f5e9(uint8_t c);
void Script_Host(void);

#endif
