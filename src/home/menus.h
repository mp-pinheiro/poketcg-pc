#ifndef POKETCG_HOME_MENUS_H
#define POKETCG_HOME_MENUS_H

#include <stdint.h>

#include "home/copy_card_name.h"
#include "home/print_text.h"

typedef struct {
	uint8_t a;
	uint16_t hl;
} TxSymbolResult;

void InitializeCardListParameters(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
void InitializeMenuParameters(uint8_t a, uint16_t *hl);
void SetMenuItem(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol_PadSpace(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign(uint8_t a);
uint8_t CardTypeToSymbolID(void);
uint8_t GetCardSymbolData(void);
typedef struct {
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} CursorTileResult;
CursorTileResult SetCursorParametersForTextBox(uint8_t d, uint8_t e, uint8_t b, uint8_t c);
CursorTileResult SetCursorParametersForTextBox_Default(uint8_t d, uint8_t e);

void DrawCursor(uint8_t a);
void EraseCursor(void);
void DrawCursor2(void);
void RefreshMenuCursor(void);
void DrawCardSymbol(uint8_t d, uint8_t e);
uint16_t DrawNarrowTextBox(void);
uint16_t DrawWideTextBox(void);
TextResult DrawNarrowTextBox_PrintTextNoDelay(uint16_t hl);
TextResult DrawWideTextBox_PrintTextNoDelay(uint16_t hl);
TextResult DrawWideTextBox_PrintText(uint16_t hl);
ProcessTextHeaderResult PrintYesOrNoItems(uint8_t d, uint8_t e);

WaitResult WaitForButtonAorB(void);
void DrawWideTextBox_PrintTextNoDelay_Wait(uint16_t hl);
void DrawNarrowTextBox_WaitForInput(uint16_t hl);
WaitResult DrawWideTextBox_WaitForInput(uint16_t hl);
WaitResult WaitForWideTextBoxInput(void);
/* >>> factory RefreshMenuCursor_CheckPlaySFX */
void RefreshMenuCursor_CheckPlaySFX(void);
/* <<< factory RefreshMenuCursor_CheckPlaySFX */
/* >>> factory PlayOpenOrExitScreenSFX */
typedef struct { uint8_t a; uint8_t f; } PlayOpenOrExitScreenSFXResult;
PlayOpenOrExitScreenSFXResult PlayOpenOrExitScreenSFX(uint8_t a, uint8_t f);
/* <<< factory PlayOpenOrExitScreenSFX */
/* >>> factory HandleYesOrNoMenu */
typedef struct { uint8_t a; uint8_t f; } HandleYesOrNoMenuResult;
HandleYesOrNoMenuResult HandleYesOrNoMenu(uint8_t d, uint8_t e, uint8_t b, uint8_t c);
/* <<< factory HandleYesOrNoMenu */
/* >>> factory CopyCardNameAndLevel */
/* menus.asm:702 is `farcall _CopyCardNameAndLevel; ret` -- the home-bank entry
 * that 19 callers use. Result shape is the callee's, declared in
 * home/copy_card_name.h. */
CopyCardNameAndLevelResult CopyCardNameAndLevel(uint8_t a, uint8_t b, uint8_t c,
						uint8_t d, uint8_t e);
/* <<< factory CopyCardNameAndLevel */
/* >>> factory ReloadCardListItems */
void ReloadCardListItems(void);
/* <<< factory ReloadCardListItems */
/* >>> factory Func_2827 */
void Func_2827(void);
/* <<< factory Func_2827 */
/* >>> factory PrintCardListItems */
void PrintCardListItems(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
/* <<< factory PrintCardListItems */
#endif
