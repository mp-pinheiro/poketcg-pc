#ifndef POKETCG_HOME_PROCESS_TEXT_H
#define POKETCG_HOME_PROCESS_TEXT_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
} TextLength;

void InitTextFormat(void);
uint8_t CaseHalfWidthLetter(uint8_t *e);
uint8_t ClassifyTextCharacterPair(uint8_t *d, uint8_t *e);
TextLength GetTextLengthInHalfTiles(uint16_t hl);
TextLength GetTextLengthInTiles(uint16_t hl);
uint16_t GetFullWidthFontTileOffset(uint8_t d, uint8_t e);
uint16_t ConvertTileNumberToTileDataAddress(uint8_t *b, uint8_t *c);
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t de;
	uint16_t hl;
} FontTileResult;
FontTileResult CopyHalfWidthCharacterToDE(uint8_t a, uint16_t de);
FontTileResult CreateHalfWidthFontTile(uint8_t d, uint8_t e);
FontTileResult CreateFullWidthFontTile(uint16_t hl);
FontTileResult CreateFullWidthFontTile_ConvertToTileDataAddress(uint8_t d, uint8_t e,
	uint8_t b);
uint8_t GenerateTextTile(uint8_t b, uint8_t d, uint8_t e);
typedef struct {
	uint8_t a;
	uint16_t hl;
} NumberTextResult;
NumberTextResult TwoByteNumberToTxSymbol_PadSpace(uint16_t hl);
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ProcessTextResult;
void ProcessText(uint16_t *hl);
void InitTextPrinting_ProcessText(uint16_t *hl);
uint16_t SetupText(uint8_t d, uint8_t e);
void InitTextPrinting(uint8_t d, uint8_t e);
void InitTextPrintingInTextbox(uint8_t a, uint8_t d, uint8_t e);
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PlaceTextResult;
PlaceTextResult PlaceNextTextTile(uint8_t a);
ProcessTextResult ProcessSpecialTextCharacter(uint8_t a, uint16_t hl);
ProcessTextResult TerminateHalfWidthText(uint8_t d, uint8_t e, uint16_t hl);
ProcessTextResult Func_235e(uint8_t d, uint8_t e);
ProcessTextResult Func_2325(uint8_t d, uint8_t e);
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyTextResult;
CopyTextResult CopyTextData(uint8_t a, uint16_t hl, uint16_t de);

void Func_22ca(uint8_t d, uint8_t e);

#endif
