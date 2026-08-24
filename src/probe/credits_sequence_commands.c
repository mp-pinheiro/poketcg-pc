#include "home/credits_sequence_commands.h"
#include "probe.h"

static void adapt_SetCreditsSequenceCmdPtr(ProbeState *s)
{
	(void)s;
	SetCreditsSequenceCmdPtr();
}

static void adapt_ExecuteCreditsSequenceCmd(ProbeState *s)
{
	(void)s;
	ExecuteCreditsSequenceCmd();
}

static void adapt_AdvanceCreditsSequenceCmdPtr(ProbeState *s)
{
	AdvanceCreditsSequenceCmdPtr(s->a);
}

/* >>> factory AdvanceCreditsSequenceCmdPtrBy2 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy2(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy2 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy3 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy3(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy3();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy3 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy5 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy5(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy5();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy5 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy6 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy6(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy6 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy4 */
static void adapt_AdvanceCreditsSequenceCmdPtrBy4(ProbeState *s)
{
	(void)s;
	AdvanceCreditsSequenceCmdPtrBy4();
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy4 */

/* >>> factory CreditsSequenceCmd_Wait */
static void adapt_CreditsSequenceCmd_Wait(ProbeState *s)
{
	CreditsSequenceCmd_Wait(s->c);
}
/* <<< factory CreditsSequenceCmd_Wait */


/* >>> factory CreditsSequenceCmd_DisableLCD */
static void adapt_CreditsSequenceCmd_DisableLCD(ProbeState *s)
{
	(void)s;
	CreditsSequenceCmd_DisableLCD();
}
/* <<< factory CreditsSequenceCmd_DisableLCD */


/* >>> factory CreditsSequenceCmd_TransformOverlay */
static void adapt_CreditsSequenceCmd_TransformOverlay(ProbeState *s)
{
	CreditsSequenceCmd_TransformOverlay(s->b, s->c, s->d, s->e);
}
/* <<< factory CreditsSequenceCmd_TransformOverlay */

/* >>> factory CreditsSequenceCmd_FadeIn */
static void adapt_CreditsSequenceCmd_FadeIn(ProbeState *s)
{
	(void)s;
	CreditsSequenceCmd_FadeIn();
}
/* <<< factory CreditsSequenceCmd_FadeIn */

/* >>> factory CreditsSequenceCmd_PrintTextBox */
static void adapt_CreditsSequenceCmd_PrintTextBox(ProbeState *s)
{
	CreditsSequenceCmd_PrintTextBox(s->b, s->c, s->d, s->e);
}
/* <<< factory CreditsSequenceCmd_PrintTextBox */

/* >>> factory CreditsSequenceCmd_InitOverlay */
static void adapt_CreditsSequenceCmd_InitOverlay(ProbeState *s)
{
	CreditsSequenceCmd_InitOverlay(s->b, s->c, s->d, s->e);
}
/* <<< factory CreditsSequenceCmd_InitOverlay */

/* >>> factory CreditsSequenceCmd_InitVolcanoSprite */
static void adapt_CreditsSequenceCmd_InitVolcanoSprite(ProbeState *s)
{
	CreditsSequenceCmd_InitVolcanoSprite(s->f);
}
/* <<< factory CreditsSequenceCmd_InitVolcanoSprite */

/* >>> factory CreditsSequenceCmd_DrawRectangle */
static void adapt_CreditsSequenceCmd_DrawRectangle(ProbeState *s)
{
	CreditsSequenceCmdDrawRectangleResult r = CreditsSequenceCmd_DrawRectangle(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CreditsSequenceCmd_DrawRectangle */

/* >>> factory CreditsSequenceCmd_PrintText */
static void adapt_CreditsSequenceCmd_PrintText(ProbeState *s)
{
	CreditsSequenceCmd_PrintText(s->b, s->c, (uint16_t)(((uint16_t)s->d << 8) | s->e));
}
/* <<< factory CreditsSequenceCmd_PrintText */

/* >>> factory CreditsSequenceCmd_LoadBooster */
static void adapt_CreditsSequenceCmd_LoadBooster(ProbeState *s)
{
	CreditsSequenceCmd_LoadBooster(s->b, s->c, s->d, s->e);
}
/* <<< factory CreditsSequenceCmd_LoadBooster */

const ProbeEntry probe_entries_credits_sequence_commands[] = {
	{ "SetCreditsSequenceCmdPtr", adapt_SetCreditsSequenceCmdPtr },
	{ "ExecuteCreditsSequenceCmd", adapt_ExecuteCreditsSequenceCmd },
	{ "AdvanceCreditsSequenceCmdPtr", adapt_AdvanceCreditsSequenceCmdPtr },
	{ "AdvanceCreditsSequenceCmdPtrBy2", adapt_AdvanceCreditsSequenceCmdPtrBy2 },
	{ "AdvanceCreditsSequenceCmdPtrBy3", adapt_AdvanceCreditsSequenceCmdPtrBy3 },
	{ "AdvanceCreditsSequenceCmdPtrBy5", adapt_AdvanceCreditsSequenceCmdPtrBy5 },
	{ "AdvanceCreditsSequenceCmdPtrBy6", adapt_AdvanceCreditsSequenceCmdPtrBy6 },
	{ "AdvanceCreditsSequenceCmdPtrBy4", adapt_AdvanceCreditsSequenceCmdPtrBy4 },
	{ "CreditsSequenceCmd_Wait", adapt_CreditsSequenceCmd_Wait },
	{ "CreditsSequenceCmd_DisableLCD", adapt_CreditsSequenceCmd_DisableLCD },
	{ "CreditsSequenceCmd_TransformOverlay", adapt_CreditsSequenceCmd_TransformOverlay },
	{ "CreditsSequenceCmd_FadeIn", adapt_CreditsSequenceCmd_FadeIn },
	{ "CreditsSequenceCmd_PrintTextBox", adapt_CreditsSequenceCmd_PrintTextBox },
	{ "CreditsSequenceCmd_InitOverlay", adapt_CreditsSequenceCmd_InitOverlay },
	{ "CreditsSequenceCmd_InitVolcanoSprite", adapt_CreditsSequenceCmd_InitVolcanoSprite },
	{ "CreditsSequenceCmd_DrawRectangle", adapt_CreditsSequenceCmd_DrawRectangle },
	{ "CreditsSequenceCmd_PrintText", adapt_CreditsSequenceCmd_PrintText },
	{ "CreditsSequenceCmd_LoadBooster", adapt_CreditsSequenceCmd_LoadBooster },
	{ NULL, NULL },
};
