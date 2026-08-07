#include "home/process_text.h"
#include "probe.h"
#include "mem.h"
static void adapt_CopyHalfWidthCharacterToDE(ProbeState *s)
{
	FontTileResult out = CopyHalfWidthCharacterToDE(s->a,
		(uint16_t)(s->d << 8 | s->e));
	s->a = out.a;
	s->d = (uint8_t)(out.de >> 8);
	s->e = (uint8_t)out.de;
	s->hl = out.hl;
}
static void adapt_InitTextFormat(ProbeState *s)
{
	(void)s;
	InitTextFormat();
}
static void adapt_CaseHalfWidthLetter(ProbeState *s)
{
	s->a = CaseHalfWidthLetter(&s->e);
}

static void adapt_ClassifyTextCharacterPair(ProbeState *s)
{
	s->f = ClassifyTextCharacterPair(&s->d, &s->e);
}

static void adapt_GetTextLengthInHalfTiles(ProbeState *s)
{
	TextLength out = GetTextLengthInHalfTiles(s->hl);
	s->a = out.a;
	s->b = out.b;
	s->c = out.c;
}

static void adapt_GetTextLengthInTiles(ProbeState *s)
{
	TextLength out = GetTextLengthInTiles(s->hl);
	s->a = out.a;
	s->b = out.b;
	s->c = out.c;
}


static void adapt_GetFullWidthFontTileOffset(ProbeState *s)
{
	uint8_t d = s->d;
	uint8_t e = s->e;
	s->hl = GetFullWidthFontTileOffset(d, e);
	if (d == 0x0e) {
		s->d = 0;
		s->a = 0x0e;
		s->b = 2;
		s->c = 0x80;
	} else if (d == 0x0f) {
		s->d = 0;
		s->a = (uint8_t)(e - 0x10);
		s->e = s->a;
		s->b = 0;
		s->c = 0;
	} else {
		s->a = d;
		s->b = 2;
		s->c = 0x80;
	}
}
static void adapt_ConvertTileNumberToTileDataAddress(ProbeState *s)
{
	s->hl = ConvertTileNumberToTileDataAddress(&s->b, &s->c);
	s->a = s->b;
}


static void adapt_CreateHalfWidthFontTile(ProbeState *s)
{
	FontTileResult out = CreateHalfWidthFontTile(s->d, s->e);
	s->a = out.a;
	s->d = (uint8_t)(out.de >> 8);
	s->e = (uint8_t)out.de;
	s->hl = out.hl;
}

static void adapt_CreateFullWidthFontTile(ProbeState *s)
{
	FontTileResult out = CreateFullWidthFontTile(s->hl);
	s->a = out.a;
	s->d = (uint8_t)(out.de >> 8);
	s->e = (uint8_t)out.de;
	s->hl = out.hl;
}

static void adapt_CreateFullWidthFontTile_ConvertToTileDataAddress(ProbeState *s)
{
	FontTileResult out = CreateFullWidthFontTile_ConvertToTileDataAddress(s->d, s->e, s->b);
	s->a = out.a;
	s->b = out.b;
	s->c = out.c;
	s->d = (uint8_t)(out.de >> 8);
	s->e = (uint8_t)out.de;
	s->hl = out.hl;
}

static void adapt_GenerateTextTile(ProbeState *s)
{
	s->a = GenerateTextTile(s->b, s->d, s->e);
}
static void adapt_TwoByteNumberToTxSymbol_PadSpace(ProbeState *s)
{
	uint16_t value = s->hl;
	TwoByteNumberToTxSymbol_PadSpace(value);
	if (value == 0) {
		s->a = 0x20;
	} else {
		uint16_t divisor = 10000;
		while (value < divisor) divisor /= 10;
		s->a = (uint8_t)(0x20 + value / divisor);
	}
	s->hl = value >= 10000 ? 0xCAA0 : 0xCAA8;
}

static void adapt_ProcessText(ProbeState *s);
static void adapt_InitTextPrinting_ProcessText(ProbeState *s);
static void adapt_SetupText(ProbeState *s);
static void adapt_InitTextPrinting(ProbeState *s);
static void adapt_InitTextPrintingInTextbox(ProbeState *s);
static void adapt_PlaceNextTextTile(ProbeState *s);
static void adapt_ProcessSpecialTextCharacter(ProbeState *s);
static void adapt_TerminateHalfWidthText(ProbeState *s);
static void adapt_Func_235e(ProbeState *s);
static void adapt_Func_2325(ProbeState *s);
static void adapt_Func_22ca(ProbeState *s)
{
	Func_22ca(s->d, s->e);
}

static void adapt_CopyTextData(ProbeState *s);
const ProbeEntry probe_entries_process_text[] = {
	{"InitTextFormat", adapt_InitTextFormat},
	{"CaseHalfWidthLetter", adapt_CaseHalfWidthLetter},
	{"ClassifyTextCharacterPair", adapt_ClassifyTextCharacterPair},
	{"GetTextLengthInHalfTiles", adapt_GetTextLengthInHalfTiles},
	{"GetTextLengthInTiles", adapt_GetTextLengthInTiles},
	{"GetFullWidthFontTileOffset", adapt_GetFullWidthFontTileOffset},
	{"ConvertTileNumberToTileDataAddress", adapt_ConvertTileNumberToTileDataAddress},
	{"CopyHalfWidthCharacterToDE", adapt_CopyHalfWidthCharacterToDE},
	{"CreateHalfWidthFontTile", adapt_CreateHalfWidthFontTile},
	{"CreateFullWidthFontTile", adapt_CreateFullWidthFontTile},
	{"CreateFullWidthFontTile_ConvertToTileDataAddress", adapt_CreateFullWidthFontTile_ConvertToTileDataAddress},
	{"GenerateTextTile", adapt_GenerateTextTile},
	{"TwoByteNumberToTxSymbol_PadSpace", adapt_TwoByteNumberToTxSymbol_PadSpace},
	{"ProcessText", adapt_ProcessText},
	{"InitTextPrinting_ProcessText", adapt_InitTextPrinting_ProcessText},
	{"SetupText", adapt_SetupText},
	{"InitTextPrinting", adapt_InitTextPrinting},
	{"InitTextPrintingInTextbox", adapt_InitTextPrintingInTextbox},
	{"PlaceNextTextTile", adapt_PlaceNextTextTile},
	{"ProcessSpecialTextCharacter", adapt_ProcessSpecialTextCharacter},
	{"TerminateHalfWidthText", adapt_TerminateHalfWidthText},
	{"Func_235e", adapt_Func_235e},
	{"Func_2325", adapt_Func_2325},
	{"Func_22ca", adapt_Func_22ca},
	{"CopyTextData", adapt_CopyTextData},
	{NULL, NULL},
};

static void adapt_ProcessText(ProbeState *s)
{
	ProcessText(&s->hl);
}

static void adapt_InitTextPrinting_ProcessText(ProbeState *s)
{
	InitTextPrinting_ProcessText(&s->hl);
}

static void adapt_SetupText(ProbeState *s)
{
	s->hl = SetupText(s->d, s->e);
}

static void adapt_InitTextPrinting(ProbeState *s)
{
	InitTextPrinting(s->d, s->e);
}

static void adapt_InitTextPrintingInTextbox(ProbeState *s)
{
	InitTextPrintingInTextbox(s->a, s->d, s->e);
}

static void adapt_PlaceNextTextTile(ProbeState *s)
{
	PlaceTextResult out = PlaceNextTextTile(s->a);
	s->a = out.a;
	s->c = out.c;
	s->d = out.d;
	s->e = out.e;
	s->hl = out.hl;
}

static void adapt_ProcessSpecialTextCharacter(ProbeState *s)
{
	ProcessTextResult out = ProcessSpecialTextCharacter(s->a, s->hl);
	s->a = out.a;
	s->hl = out.hl;
	s->f = out.f;
}

static void adapt_TerminateHalfWidthText(ProbeState *s)
{
	ProcessTextResult out = TerminateHalfWidthText(s->d, s->e, s->hl);
	s->a = out.a;
	s->f = out.f;
}

static void adapt_Func_235e(ProbeState *s)
{
	ProcessTextResult out = Func_235e(s->d, s->e);
	s->a = out.a;
	s->d = out.d;
	s->e = out.e;
	s->f = out.f;
}

static void adapt_Func_2325(ProbeState *s)
{
	ProcessTextResult out = Func_2325(s->d, s->e);
	s->a = out.a;
	s->d = out.d;
	s->e = out.e;
	s->f = out.f;
}

static void adapt_CopyTextData(ProbeState *s)
{
	CopyTextResult out = CopyTextData(s->a, s->hl, (uint16_t)(s->d << 8 | s->e));
	s->a = out.a;
	s->d = out.d;
	s->e = out.e;
	s->hl = out.hl;
}


