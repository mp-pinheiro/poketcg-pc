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
/* >>> factory ChallengeMachine_PrintFinalConsecutiveWinStreak */
typedef struct { uint8_t f; uint16_t hl; } ChallengeMachinePrintFinalConsecutiveWinStreakResult;
ChallengeMachinePrintFinalConsecutiveWinStreakResult ChallengeMachine_PrintFinalConsecutiveWinStreak(uint16_t hl);
/* <<< factory ChallengeMachine_PrintFinalConsecutiveWinStreak */
/* >>> factory ChallengeMachine_ShowNewRecord */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } ChallengeMachineShowNewRecordResult;
ChallengeMachineShowNewRecordResult ChallengeMachine_ShowNewRecord(uint16_t hl);
/* <<< factory ChallengeMachine_ShowNewRecord */
/* >>> factory ChallengeMachine_DuelWon */
typedef struct { uint8_t f; } ChallengeMachineDuelWonResult;
ChallengeMachineDuelWonResult ChallengeMachine_DuelWon(void);
/* <<< factory ChallengeMachine_DuelWon */
/* >>> factory ChallengeMachine_GetOpponentNameAndDeck */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ChallengeMachine_GetOpponentNameAndDeckResult;
ChallengeMachine_GetOpponentNameAndDeckResult ChallengeMachine_GetOpponentNameAndDeck(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ChallengeMachine_GetOpponentNameAndDeck */
/* >>> factory ChallengeMachine_PrintScores */
void ChallengeMachine_PrintScores(uint16_t hl);
/* <<< factory ChallengeMachine_PrintScores */
/* >>> factory ChallengeMachine_PrintOpponentName */
ChallengeMachinePrintResult ChallengeMachine_PrintOpponentName(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ChallengeMachine_PrintOpponentName */
/* >>> factory ChallengeMachine_PrintOpponentClubStatus */
typedef struct { uint16_t hl; uint8_t b; uint8_t c; } ChallengeMachine_PrintOpponentClubStatusResult;
ChallengeMachine_PrintOpponentClubStatusResult ChallengeMachine_PrintOpponentClubStatus(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ChallengeMachine_PrintOpponentClubStatus */
/* >>> factory ChallengeMachine_PrintOpponentInfo */
void ChallengeMachine_PrintOpponentInfo(uint8_t f, uint8_t d, uint8_t e);
/* <<< factory ChallengeMachine_PrintOpponentInfo */

/* >>> factory ChallengeMachine_PrepareDuel */
void ChallengeMachine_PrepareDuel(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ChallengeMachine_PrepareDuel */
/* >>> factory ChallengeMachine_DrawScoreScreen */
void ChallengeMachine_DrawScoreScreen(void);
/* <<< factory ChallengeMachine_DrawScoreScreen */
/* >>> factory ChallengeMachine_AreYouReady */
typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeMachine_AreYouReadyResult;
ChallengeMachine_AreYouReadyResult ChallengeMachine_AreYouReady(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ChallengeMachine_AreYouReady */
/* >>> factory ChallengeMachine_PrintDuelResultIcons */
void ChallengeMachine_PrintDuelResultIcons(void);
/* <<< factory ChallengeMachine_PrintDuelResultIcons */
/* >>> factory ChallengeMachine_DrawOpponentList */
void ChallengeMachine_DrawOpponentList(void);
/* <<< factory ChallengeMachine_DrawOpponentList */
#endif
