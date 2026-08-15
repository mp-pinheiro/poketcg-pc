#ifndef POKETCG_HOME_CHALLENGE_MACHINE_H
#define POKETCG_HOME_CHALLENGE_MACHINE_H

#include <stdint.h>

typedef struct {
	uint16_t hl;
	uint8_t f;
} ChallengeMachineCheckResult;

ChallengeMachineCheckResult ChallengeMachine_CheckIfOpponentAlreadySelected(uint8_t a, uint8_t c);

typedef struct {
	uint16_t hl;
	uint8_t d;
	uint8_t e;
} ChallengeMachinePrintResult;

ChallengeMachinePrintResult ChallengeMachine_PrintText(uint16_t hl, uint8_t b, uint8_t c);
/* >>> factory ChallengeMachine_PickOpponentSequence */
void ChallengeMachine_PickOpponentSequence(void);
/* <<< factory ChallengeMachine_PickOpponentSequence */
#endif
