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
/* >>> factory GetFullWidthFontTileOffset */
uint16_t GetFullWidthFontTileOffset(uint8_t d, uint8_t e);
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
/* >>> factory TwoByteNumberToTxSymbol_PadSpace */
NumberTextResult TwoByteNumberToTxSymbol_PadSpace(uint16_t hl);
/* <<< factory TwoByteNumberToTxSymbol_PadSpace */
/* >>> part ProcessTextResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ProcessTextResult;
/* <<< part ProcessTextResult */
/* >>> part ProcessText */
ProcessTextResult ProcessText(uint16_t *hl);
/* <<< part ProcessText */
/* >>> part InitTextPrinting_ProcessText */
void InitTextPrinting_ProcessText(uint16_t *hl);
/* <<< part InitTextPrinting_ProcessText */
/* >>> part SetupText */
uint16_t SetupText(uint8_t d, uint8_t e);
/* <<< part SetupText */
/* >>> part InitTextPrinting */
void InitTextPrinting(uint8_t d, uint8_t e);
/* <<< part InitTextPrinting */
/* >>> part InitTextPrintingInTextbox */
void InitTextPrintingInTextbox(uint8_t a, uint8_t d, uint8_t e);
/* <<< part InitTextPrintingInTextbox */
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
/* >>> part PlaceNextTextTile */
PlaceTextResult PlaceNextTextTile(uint8_t a);
/* <<< part PlaceNextTextTile */
/* >>> part ProcessSpecialTextCharacter */
ProcessTextResult ProcessSpecialTextCharacter(uint8_t a, uint16_t hl);
/* <<< part ProcessSpecialTextCharacter */
/* >>> part TerminateHalfWidthText */
ProcessTextResult TerminateHalfWidthText(uint8_t d, uint8_t e, uint16_t hl);
/* <<< part TerminateHalfWidthText */
/* >>> part Func_235e */
ProcessTextResult Func_235e(uint8_t d, uint8_t e);
/* <<< part Func_235e */
/* >>> part Func_2325 */
ProcessTextResult Func_2325(uint8_t d, uint8_t e);
/* <<< part Func_2325 */
/* >>> part CopyTextResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyTextResult;
/* <<< part CopyTextResult */
/* >>> part CopyTextData */
CopyTextResult CopyTextData(uint8_t a, uint16_t hl, uint16_t de);
/* <<< part CopyTextData */

/* >>> part Func_22ca */
uint8_t Func_22ca(uint8_t d, uint8_t e);
/* <<< part Func_22ca */

#endif
