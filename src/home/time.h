#ifndef POKETCG_HOME_TIME_H
#define POKETCG_HOME_TIME_H

#include <stdint.h>

/* poketcg/src/home/time.asm */

void IncrementPlayTimeCounter(void);
uint8_t CheckForCGB(void);

#endif /* POKETCG_HOME_TIME_H */
