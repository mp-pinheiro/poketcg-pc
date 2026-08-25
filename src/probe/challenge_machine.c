#include "home/challenge_machine.h"
#include "probe.h"

static void adapt_ChallengeMachine_CheckIfOpponentAlreadySelected(ProbeState *s)
{
	ChallengeMachineCheckResult result = ChallengeMachine_CheckIfOpponentAlreadySelected(s->a, s->c);
	s->f = result.f;
	s->hl = result.hl;
}

static void adapt_ChallengeMachine_PrintText(ProbeState *s)
{
	ChallengeMachinePrintResult result = ChallengeMachine_PrintText(s->hl, s->b, s->c);
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

/* >>> factory ChallengeMachine_PickOpponentSequence */
static void adapt_ChallengeMachine_PickOpponentSequence(ProbeState *s)
{
	(void)s;
	ChallengeMachine_PickOpponentSequence();
}
/* <<< factory ChallengeMachine_PickOpponentSequence */

/* >>> factory ChallengeMachine_GetCurrentOpponent */
static void adapt_ChallengeMachine_GetCurrentOpponent(ProbeState *s)
{
	ChallengeMachineOpponentResult r = ChallengeMachine_GetCurrentOpponent();
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ChallengeMachine_GetCurrentOpponent */

/* >>> factory ChallengeMachine_IncrementHLMax999 */
static void adapt_ChallengeMachine_IncrementHLMax999(ProbeState *s)
{
	s->hl = ChallengeMachine_IncrementHLMax999(s->hl);
}
/* <<< factory ChallengeMachine_IncrementHLMax999 */

/* >>> factory ChallengeMachine_CheckForNewRecord */
static void adapt_ChallengeMachine_CheckForNewRecord(ProbeState *s)
{
	ChallengeMachineRecordResult r = ChallengeMachine_CheckForNewRecord(s->b, s->c, s->d, s->e);
	s->hl = r.hl;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ChallengeMachine_CheckForNewRecord */

/* >>> factory ChallengeMachine_RecordDuelResult */
static void adapt_ChallengeMachine_RecordDuelResult(ProbeState *s)
{
	(void)s;
	ChallengeMachine_RecordDuelResult();
}
/* <<< factory ChallengeMachine_RecordDuelResult */

/* >>> factory ChallengeMachine_Initialize */
static void adapt_ChallengeMachine_Initialize(ProbeState *s)
{
	ChallengeMachineInitializeResult result = ChallengeMachine_Initialize();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ChallengeMachine_Initialize */

/* >>> factory ChallengeMachine_Reset */
static void adapt_ChallengeMachine_Reset(ProbeState *s)
{
	(void)s;
	ChallengeMachine_Reset();
}
/* <<< factory ChallengeMachine_Reset */

/* >>> factory ChallengeMachine_PrintFinalConsecutiveWinStreak */
static void adapt_ChallengeMachine_PrintFinalConsecutiveWinStreak(ProbeState *s)
{
	ChallengeMachinePrintFinalConsecutiveWinStreakResult r = ChallengeMachine_PrintFinalConsecutiveWinStreak(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ChallengeMachine_PrintFinalConsecutiveWinStreak */

/* >>> factory ChallengeMachine_ShowNewRecord */
static void adapt_ChallengeMachine_ShowNewRecord(ProbeState *s)
{
	ChallengeMachineShowNewRecordResult r = ChallengeMachine_ShowNewRecord(s->hl);
	s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory ChallengeMachine_ShowNewRecord */

/* >>> factory ChallengeMachine_DuelWon */
static void adapt_ChallengeMachine_DuelWon(ProbeState *s)
{
	ChallengeMachineDuelWonResult r = ChallengeMachine_DuelWon();
	s->f = r.f;
}
/* <<< factory ChallengeMachine_DuelWon */

/* >>> factory ChallengeMachine_GetOpponentNameAndDeck */
static void adapt_ChallengeMachine_GetOpponentNameAndDeck(ProbeState *s)
{
	ChallengeMachine_GetOpponentNameAndDeckResult r = ChallengeMachine_GetOpponentNameAndDeck(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ChallengeMachine_GetOpponentNameAndDeck */

/* >>> factory ChallengeMachine_PrintScores */
static void adapt_ChallengeMachine_PrintScores(ProbeState *s)
{
	ChallengeMachine_PrintScores(s->hl);
}
/* <<< factory ChallengeMachine_PrintScores */

/* >>> factory ChallengeMachine_PrintOpponentName */
static void adapt_ChallengeMachine_PrintOpponentName(ProbeState *s)
{
	ChallengeMachinePrintResult r = ChallengeMachine_PrintOpponentName(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ChallengeMachine_PrintOpponentName */

/* >>> factory ChallengeMachine_PrintOpponentClubStatus */
static void adapt_ChallengeMachine_PrintOpponentClubStatus(ProbeState *s)
{
	ChallengeMachine_PrintOpponentClubStatusResult r = ChallengeMachine_PrintOpponentClubStatus(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->hl = r.hl;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ChallengeMachine_PrintOpponentClubStatus */

/* >>> factory ChallengeMachine_PrepareDuel */
static void adapt_ChallengeMachine_PrepareDuel(ProbeState *s)
{
	ChallengeMachine_PrepareDuel(s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory ChallengeMachine_PrepareDuel */

/* >>> factory ChallengeMachine_DrawScoreScreen */
static void adapt_ChallengeMachine_DrawScoreScreen(ProbeState *s)
{
	ChallengeMachine_DrawScoreScreen();
}
/* <<< factory ChallengeMachine_DrawScoreScreen */

/* >>> factory ChallengeMachine_AreYouReady */
static void adapt_ChallengeMachine_AreYouReady(ProbeState *s)
{
	ChallengeMachine_AreYouReadyResult r = ChallengeMachine_AreYouReady(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ChallengeMachine_AreYouReady */

const ProbeEntry probe_entries_challenge_machine[] = {
	{ "ChallengeMachine_CheckIfOpponentAlreadySelected", adapt_ChallengeMachine_CheckIfOpponentAlreadySelected },
	{ "ChallengeMachine_PrintText", adapt_ChallengeMachine_PrintText },
	{ "ChallengeMachine_PickOpponentSequence", adapt_ChallengeMachine_PickOpponentSequence },
	{ "ChallengeMachine_GetCurrentOpponent", adapt_ChallengeMachine_GetCurrentOpponent },
	{ "ChallengeMachine_IncrementHLMax999", adapt_ChallengeMachine_IncrementHLMax999 },
	{ "ChallengeMachine_CheckForNewRecord", adapt_ChallengeMachine_CheckForNewRecord },
	{ "ChallengeMachine_RecordDuelResult", adapt_ChallengeMachine_RecordDuelResult },
	{ "ChallengeMachine_Initialize", adapt_ChallengeMachine_Initialize },
	{ "ChallengeMachine_Reset", adapt_ChallengeMachine_Reset },
	{ "ChallengeMachine_PrintFinalConsecutiveWinStreak", adapt_ChallengeMachine_PrintFinalConsecutiveWinStreak },
	{ "ChallengeMachine_ShowNewRecord", adapt_ChallengeMachine_ShowNewRecord },
	{ "ChallengeMachine_DuelWon", adapt_ChallengeMachine_DuelWon },
	{ "ChallengeMachine_GetOpponentNameAndDeck", adapt_ChallengeMachine_GetOpponentNameAndDeck },
	{ "ChallengeMachine_PrintScores", adapt_ChallengeMachine_PrintScores },
	{ "ChallengeMachine_PrintOpponentName", adapt_ChallengeMachine_PrintOpponentName },
	{ "ChallengeMachine_PrintOpponentClubStatus", adapt_ChallengeMachine_PrintOpponentClubStatus },
	{ "ChallengeMachine_PrepareDuel", adapt_ChallengeMachine_PrepareDuel },
	{ "ChallengeMachine_DrawScoreScreen", adapt_ChallengeMachine_DrawScoreScreen },
	{ "ChallengeMachine_AreYouReady", adapt_ChallengeMachine_AreYouReady },
	{ NULL, NULL },
};
