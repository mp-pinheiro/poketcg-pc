#ifndef POKETCG_HOME_DEBUG_MAIN_H
#define POKETCG_HOME_DEBUG_MAIN_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} Func126b3Result;

Func126b3Result Func_126b3(void);

#endif
