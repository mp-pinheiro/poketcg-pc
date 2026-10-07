#ifndef POKETCG_HOME_PROCESS_TEXT_H
#define POKETCG_HOME_PROCESS_TEXT_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part TextLength */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
} TextLength;
/* <<< part TextLength */

/* >>> factory InitTextFormat */
void InitTextFormat(void);
/* <<< factory InitTextFormat */
/* >>> factory CaseHalfWidthLetter */
uint8_t CaseHalfWidthLetter(uint8_t *e);
/* <<< factory CaseHalfWidthLetter */
/* >>> factory ClassifyTextCharacterPair */
uint8_t ClassifyTextCharacterPair(uint8_t *d, uint8_t *e);
/* <<< factory ClassifyTextCharacterPair */
/* >>> factory GetTextLengthInHalfTiles */
TextLength GetTextLengthInHalfTiles(uint16_t hl);
/* <<< factory GetTextLengthInHalfTiles */
/* >>> factory GetTextLengthInTiles */
TextLength GetTextLengthInTiles(uint16_t hl);
/* <<< factory GetTextLengthInTiles */
/* >>> part FullWidthOffsetResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} FullWidthOffsetResult;
/* <<< part FullWidthOffsetResult */
/* >>> factory GetFullWidthFontTileOffset */
FullWidthOffsetResult GetFullWidthFontTileOffset(uint8_t d, uint8_t e);
/* <<< factory GetFullWidthFontTileOffset */
/* >>> factory ConvertTileNumberToTileDataAddress */
uint16_t ConvertTileNumberToTileDataAddress(uint8_t *b, uint8_t *c);
/* <<< factory ConvertTileNumberToTileDataAddress */
/* >>> part FontTileResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t de;
	uint16_t hl;
} FontTileResult;
/* <<< part FontTileResult */
/* >>> factory CopyHalfWidthCharacterToDE */
FontTileResult CopyHalfWidthCharacterToDE(uint8_t a, uint16_t de);
/* <<< factory CopyHalfWidthCharacterToDE */
/* >>> factory CreateHalfWidthFontTile */
FontTileResult CreateHalfWidthFontTile(uint8_t d, uint8_t e);
/* <<< factory CreateHalfWidthFontTile */
/* >>> factory CreateFullWidthFontTile */
FontTileResult CreateFullWidthFontTile(uint16_t hl);
/* <<< factory CreateFullWidthFontTile */
/* >>> factory CreateFullWidthFontTile_ConvertToTileDataAddress */
FontTileResult CreateFullWidthFontTile_ConvertToTileDataAddress(uint8_t d, uint8_t e,
	uint8_t b);
/* <<< factory CreateFullWidthFontTile_ConvertToTileDataAddress */
/* >>> factory GenerateTextTile */
uint8_t GenerateTextTile(uint8_t b, uint8_t d, uint8_t e);
/* <<< factory GenerateTextTile */
/* >>> part NumberTextResult */
typedef struct {
	uint8_t a;
	uint16_t hl;
} NumberTextResult;
/* <<< part NumberTextResult */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
NumberTextResult TwoByteNumberToTxSymbol_TrimLeadingZeros(uint16_t hl);
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
/* >>> part ProcessTextResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ProcessTextResult;
/* <<< part ProcessTextResult */
/* >>> factory ProcessText */
ProcessTextResult ProcessText(uint16_t *hl);
/* <<< factory ProcessText */
/* >>> factory SetupText */
uint16_t SetupText(uint8_t d, uint8_t e);
/* <<< factory SetupText */
/* >>> factory InitTextPrinting */
void InitTextPrinting(uint8_t d, uint8_t e);
/* <<< factory InitTextPrinting */
/* >>> factory InitTextPrintingInTextbox */
void InitTextPrintingInTextbox(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory InitTextPrintingInTextbox */
/* >>> part PlaceTextResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PlaceTextResult;
/* <<< part PlaceTextResult */
/* >>> factory PlaceNextTextTile */
PlaceTextResult PlaceNextTextTile(uint8_t a);
/* <<< factory PlaceNextTextTile */
/* >>> factory ProcessSpecialTextCharacter */
ProcessTextResult ProcessSpecialTextCharacter(uint8_t a, uint16_t hl);
/* <<< factory ProcessSpecialTextCharacter */
/* >>> factory TerminateHalfWidthText */
ProcessTextResult TerminateHalfWidthText(uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory TerminateHalfWidthText */
/* >>> factory Func_235e */
ProcessTextResult Func_235e(uint8_t d, uint8_t e);
/* <<< factory Func_235e */
/* >>> factory Func_2325 */
ProcessTextResult Func_2325(uint8_t d, uint8_t e);
/* <<< factory Func_2325 */
/* >>> part CopyTextResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyTextResult;
/* <<< part CopyTextResult */
/* >>> factory CopyTextData */
CopyTextResult CopyTextData(uint8_t a, uint16_t hl, uint16_t de);
/* <<< factory CopyTextData */

/* >>> factory Func_22ca */
uint8_t Func_22ca(uint8_t d, uint8_t e);
/* <<< factory Func_22ca */

#endif
