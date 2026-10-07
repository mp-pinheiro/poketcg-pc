#ifndef POKETCG_HOME_TIME_H
#define POKETCG_HOME_TIME_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory IncrementPlayTimeCounter */
/* poketcg/src/home/time.asm */

void IncrementPlayTimeCounter(void);
/* <<< factory IncrementPlayTimeCounter */
/* >>> factory CheckForCGB */
uint8_t CheckForCGB(void);
/* <<< factory CheckForCGB */
/* >>> part SwitchToCGBDoubleSpeed */
void SwitchToCGBDoubleSpeed(void);
/* <<< part SwitchToCGBDoubleSpeed */
/* >>> part SwitchToCGBNormalSpeed */
void SwitchToCGBNormalSpeed(void);
/* <<< part SwitchToCGBNormalSpeed */
/* >>> part TimerSetupResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t f;
} TimerSetupResult;
/* <<< part TimerSetupResult */
/* >>> factory SetupTimer */
TimerSetupResult SetupTimer(void);
/* <<< factory SetupTimer */

/* >>> factory TimerHandler */
void TimerHandler(void);
/* <<< factory TimerHandler */
#endif /* POKETCG_HOME_TIME_H */
