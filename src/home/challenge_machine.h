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
/* >>> factory ChallengeMachine_GetCurrentOpponent */
typedef struct {
	uint16_t hl;
	uint8_t d;
	uint8_t e;
} ChallengeMachineOpponentResult;

ChallengeMachineOpponentResult ChallengeMachine_GetCurrentOpponent(void);
/* <<< factory ChallengeMachine_GetCurrentOpponent */
/* >>> factory ChallengeMachine_IncrementHLMax999 */
uint16_t ChallengeMachine_IncrementHLMax999(uint16_t hl);
/* <<< factory ChallengeMachine_IncrementHLMax999 */
/* >>> factory ChallengeMachine_CheckForNewRecord */
typedef struct {
	uint16_t hl;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
} ChallengeMachineRecordResult;

ChallengeMachineRecordResult ChallengeMachine_CheckForNewRecord(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory ChallengeMachine_CheckForNewRecord */
/* >>> factory ChallengeMachine_RecordDuelResult */
void ChallengeMachine_RecordDuelResult(void);
/* <<< factory ChallengeMachine_RecordDuelResult */
/* >>> factory ChallengeMachine_Initialize */
typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeMachineInitializeResult;

ChallengeMachineInitializeResult ChallengeMachine_Initialize(void);
/* <<< factory ChallengeMachine_Initialize */
/* >>> factory ChallengeMachine_Reset */
void ChallengeMachine_Reset(void);
/* <<< factory ChallengeMachine_Reset */
#endif
