#ifndef POKETCG_HOME_SGB_H
#define POKETCG_HOME_SGB_H

#include <stdint.h>

typedef struct {
	uint8_t a, f, b, c, d, e;
} SGBWaitResult;

SGBWaitResult Wait(uint16_t bc);

#endif /* POKETCG_HOME_SGB_H */
