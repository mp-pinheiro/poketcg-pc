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
	s->a = ClassifyTextCharacterPair(&s->d, &s->e);
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
	{NULL, NULL},
};


