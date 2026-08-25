#include "home/menus.h"
#include "probe.h"
#include "generated/wram.h"

static void adapt_InitializeCardListParameters(ProbeState *s)
{
	InitializeCardListParameters(s->a, s->d, s->e, &s->hl);
}

static void adapt_InitializeMenuParameters(ProbeState *s)
{
	InitializeMenuParameters(s->a, &s->hl);
}

static void adapt_SetMenuItem(ProbeState *s)
{
	SetMenuItem(s->a);
}

static void adapt_OneByteNumberToTxSymbol(ProbeState *s)
{
	TxSymbolResult result = OneByteNumberToTxSymbol(s->a);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_OneByteNumberToTxSymbol_PadSpace(ProbeState *s)
{
	TxSymbolResult result = OneByteNumberToTxSymbol_PadSpace(s->a);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign(ProbeState *s)
{
	TxSymbolResult result = OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign(s->a);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_CardTypeToSymbolID(ProbeState *s)
{
	s->a = CardTypeToSymbolID();
}

static void adapt_GetCardSymbolData(ProbeState *s)
{
	uint8_t id = CardTypeToSymbolID();
	s->a = GetCardSymbolData();
	s->b = 0;
	s->c = (uint8_t)(id * 2);
	s->hl = (uint16_t)(0x29dd + id * 2);
}

static void adapt_SetCursorParametersForTextBox(ProbeState *s)
{
	CursorTileResult result = SetCursorParametersForTextBox(s->d, s->e, s->b, s->c);
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}

static void adapt_SetCursorParametersForTextBox_Default(ProbeState *s)
{
	CursorTileResult result = SetCursorParametersForTextBox_Default(s->d, s->e);
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
	s->f = result.f;
}

static void adapt_DrawCursor(ProbeState *s)
{
	DrawCursor(s->a);
}

static void adapt_EraseCursor(ProbeState *s)
{
	(void)s;
	EraseCursor();
}

static void adapt_DrawCursor2(ProbeState *s)
{
	(void)s;
	DrawCursor2();
}

static void adapt_RefreshMenuCursor(ProbeState *s)
{
	(void)s;
	RefreshMenuCursor();
}

static void adapt_DrawCardSymbol(ProbeState *s)
{
	DrawCardSymbol(s->d, s->e);
}

static void adapt_DrawNarrowTextBox(ProbeState *s)
{
	s->hl = DrawNarrowTextBox();
}

static void adapt_DrawWideTextBox(ProbeState *s)
{
	s->hl = DrawWideTextBox();
}

static void adapt_DrawNarrowTextBox_PrintTextNoDelay(ProbeState *s)
{
	s->hl = DrawNarrowTextBox_PrintTextNoDelay(s->hl).hl;
}

static void adapt_DrawWideTextBox_PrintTextNoDelay(ProbeState *s)
{
	s->hl = DrawWideTextBox_PrintTextNoDelay(s->hl).hl;
}

static void adapt_DrawWideTextBox_PrintText(ProbeState *s)
{
	s->hl = DrawWideTextBox_PrintText(s->hl).hl;
}

static void adapt_PrintYesOrNoItems(ProbeState *s)
{
	ProcessTextHeaderResult r = PrintYesOrNoItems(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_WaitForButtonAorB(ProbeState *s)
{
	s->f = WaitForButtonAorB().f;
}

static void adapt_DrawWideTextBox_PrintTextNoDelay_Wait(ProbeState *s)
{
	DrawWideTextBox_PrintTextNoDelay_Wait(s->hl);
}

static void adapt_DrawNarrowTextBox_WaitForInput(ProbeState *s)
{
	DrawNarrowTextBox_WaitForInput(s->hl);
}

static void adapt_DrawWideTextBox_WaitForInput(ProbeState *s)
{
	DrawWideTextBox_WaitForInput(s->hl);
}

static void adapt_WaitForWideTextBoxInput(ProbeState *s)
{
	(void)s;
	WaitForWideTextBoxInput();
}

/* >>> factory RefreshMenuCursor_CheckPlaySFX */
static void adapt_RefreshMenuCursor_CheckPlaySFX(ProbeState *s)
{
	(void)s;
	RefreshMenuCursor_CheckPlaySFX();
}
/* <<< factory RefreshMenuCursor_CheckPlaySFX */

/* >>> factory PlayOpenOrExitScreenSFX */
static void adapt_PlayOpenOrExitScreenSFX(ProbeState *s)
{
	PlayOpenOrExitScreenSFXResult r = PlayOpenOrExitScreenSFX(s->a, s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PlayOpenOrExitScreenSFX */

/* >>> factory HandleYesOrNoMenu */
static void adapt_HandleYesOrNoMenu(ProbeState *s)
{
	HandleYesOrNoMenuResult result = HandleYesOrNoMenu(s->d, s->e, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory HandleYesOrNoMenu */

/* >>> factory CopyCardNameAndLevel */
static void adapt_CopyCardNameAndLevel(ProbeState *s)
{
	CopyCardNameAndLevelResult result =
		CopyCardNameAndLevel(s->a, s->b, s->c, s->d, s->e);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory CopyCardNameAndLevel */

/* >>> factory ReloadCardListItems */
static void adapt_ReloadCardListItems(ProbeState *s)
{
	ReloadCardListItems();
}
/* <<< factory ReloadCardListItems */

/* >>> factory Func_2827 */
static void adapt_Func_2827(ProbeState *s)
{
	(void)s;
	Func_2827();
}
/* <<< factory Func_2827 */

/* >>> factory PrintCardListItems */
static void adapt_PrintCardListItems(ProbeState *s)
{
	PrintCardListItems(s->a, s->d, s->e, &s->hl);
}
/* <<< factory PrintCardListItems */

/* >>> factory CardListMenuFunction */
static void adapt_CardListMenuFunction(ProbeState *s)
{
	CardListMenuFunctionResult r = CardListMenuFunction();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CardListMenuFunction */

/* >>> factory HandleMenuInput */
static void adapt_HandleMenuInput(ProbeState *s)
{
	HandleMenuInputResult r = HandleMenuInput();
	s->a = r.a;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory HandleMenuInput */

/* >>> factory HandleCardListInput */
static void adapt_HandleCardListInput(ProbeState *s)
{
	HandleCardListInputResult r = HandleCardListInput();
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory HandleCardListInput */

/* >>> factory HandleDuelMenuInput */
static void adapt_HandleDuelMenuInput(ProbeState *s)
{
	HandleMenuInputResult r = HandleDuelMenuInput(s->e);
	s->a = r.a;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory HandleDuelMenuInput */

/* >>> factory YesOrNoMenuWithText_LeftAligned */
static void adapt_YesOrNoMenuWithText_LeftAligned(ProbeState *s)
{
	HandleYesOrNoMenuResult r = YesOrNoMenuWithText_LeftAligned(s->hl, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory YesOrNoMenuWithText_LeftAligned */

const ProbeEntry probe_entries_menus[] = {
	{ "InitializeCardListParameters", adapt_InitializeCardListParameters },
	{ "InitializeMenuParameters", adapt_InitializeMenuParameters },
	{ "SetMenuItem", adapt_SetMenuItem },
	{ "OneByteNumberToTxSymbol", adapt_OneByteNumberToTxSymbol },
	{ "OneByteNumberToTxSymbol_PadSpace", adapt_OneByteNumberToTxSymbol_PadSpace },
	{ "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign", adapt_OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign },
	{ "CardTypeToSymbolID", adapt_CardTypeToSymbolID },
	{ "GetCardSymbolData", adapt_GetCardSymbolData },
	{ "SetCursorParametersForTextBox", adapt_SetCursorParametersForTextBox },
	{ "SetCursorParametersForTextBox_Default", adapt_SetCursorParametersForTextBox_Default },
	{ "DrawCursor", adapt_DrawCursor },
	{ "EraseCursor", adapt_EraseCursor },
	{ "DrawCursor2", adapt_DrawCursor2 },
	{ "RefreshMenuCursor", adapt_RefreshMenuCursor },
	{ "DrawCardSymbol", adapt_DrawCardSymbol },
	{ "DrawNarrowTextBox", adapt_DrawNarrowTextBox },
	{ "DrawWideTextBox", adapt_DrawWideTextBox },
	{ "DrawNarrowTextBox_PrintTextNoDelay", adapt_DrawNarrowTextBox_PrintTextNoDelay },
	{ "DrawWideTextBox_PrintTextNoDelay", adapt_DrawWideTextBox_PrintTextNoDelay },
	{ "DrawWideTextBox_PrintText", adapt_DrawWideTextBox_PrintText },
	{ "PrintYesOrNoItems", adapt_PrintYesOrNoItems },
	{ "WaitForButtonAorB", adapt_WaitForButtonAorB },
	{ "DrawWideTextBox_PrintTextNoDelay_Wait", adapt_DrawWideTextBox_PrintTextNoDelay_Wait },
	{ "DrawNarrowTextBox_WaitForInput", adapt_DrawNarrowTextBox_WaitForInput },
	{ "DrawWideTextBox_WaitForInput", adapt_DrawWideTextBox_WaitForInput },
	{ "WaitForWideTextBoxInput", adapt_WaitForWideTextBoxInput },
	{ "RefreshMenuCursor_CheckPlaySFX", adapt_RefreshMenuCursor_CheckPlaySFX },
	{ "PlayOpenOrExitScreenSFX", adapt_PlayOpenOrExitScreenSFX },
	{ "HandleYesOrNoMenu", adapt_HandleYesOrNoMenu },
	{ "CopyCardNameAndLevel", adapt_CopyCardNameAndLevel },
	{ "ReloadCardListItems", adapt_ReloadCardListItems },
	{ "Func_2827", adapt_Func_2827 },
	{ "PrintCardListItems", adapt_PrintCardListItems },
	{ "CardListMenuFunction", adapt_CardListMenuFunction },
	{ "HandleMenuInput", adapt_HandleMenuInput },
	{ "HandleCardListInput", adapt_HandleCardListInput },
	{ "HandleDuelMenuInput", adapt_HandleDuelMenuInput },
	{ "YesOrNoMenuWithText_LeftAligned", adapt_YesOrNoMenuWithText_LeftAligned },
	{ NULL, NULL },
};
