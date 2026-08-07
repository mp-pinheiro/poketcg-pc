#ifndef POKETCG_HOME_TIME_H
#define POKETCG_HOME_TIME_H

#include <stdint.h>

/* poketcg/src/home/time.asm */

void IncrementPlayTimeCounter(void);
uint8_t CheckForCGB(void);
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t f;
} TimerSetupResult;
TimerSetupResult SetupTimer(void);

#endif /* POKETCG_HOME_TIME_H */
