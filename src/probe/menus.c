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
}

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
	{ NULL, NULL },
};
