#ifndef POKETCG_HOME_MENUS_H
#define POKETCG_HOME_MENUS_H

/* >>> part includes */
#include <stdint.h>

#include "home/copy_card_name.h"
#include "home/print_text.h"
/* <<< part includes */

/* >>> part TxSymbolResult */
typedef struct {
	uint8_t a;
	uint16_t hl;
} TxSymbolResult;
/* <<< part TxSymbolResult */

/* >>> factory InitializeCardListParameters */
void InitializeCardListParameters(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
/* <<< factory InitializeCardListParameters */
/* >>> factory InitializeMenuParameters */
void InitializeMenuParameters(uint8_t a, uint16_t *hl);
/* <<< factory InitializeMenuParameters */
/* >>> factory SetMenuItem */
void SetMenuItem(uint8_t a);
/* <<< factory SetMenuItem */
/* >>> factory OneByteNumberToTxSymbol */
TxSymbolResult OneByteNumberToTxSymbol(uint8_t a);
/* <<< factory OneByteNumberToTxSymbol */
/* >>> factory OneByteNumberToTxSymbol_TrimLeadingZeros */
TxSymbolResult OneByteNumberToTxSymbol_TrimLeadingZeros(uint8_t a);
/* <<< factory OneByteNumberToTxSymbol_TrimLeadingZeros */
/* >>> factory CardTypeToSymbolID */
uint8_t CardTypeToSymbolID(void);
/* <<< factory CardTypeToSymbolID */
/* >>> factory GetCardSymbolData */
uint8_t GetCardSymbolData(void);
/* <<< factory GetCardSymbolData */
/* >>> part CursorTileResult */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} CursorTileResult;
/* <<< part CursorTileResult */
/* >>> factory SetCursorParametersForTextBox */
CursorTileResult SetCursorParametersForTextBox(uint8_t d, uint8_t e, uint8_t b, uint8_t c);
/* <<< factory SetCursorParametersForTextBox */
/* >>> factory SetCursorParametersForTextBox_Default */
CursorTileResult SetCursorParametersForTextBox_Default(uint8_t d, uint8_t e);
/* <<< factory SetCursorParametersForTextBox_Default */

/* >>> factory DrawCursor */
void DrawCursor(uint8_t a);
/* <<< factory DrawCursor */
/* >>> factory EraseCursor */
void EraseCursor(void);
/* <<< factory EraseCursor */
/* >>> factory DrawCursor2 */
void DrawCursor2(void);
/* <<< factory DrawCursor2 */
/* >>> factory RefreshMenuCursor */
void RefreshMenuCursor(void);
/* <<< factory RefreshMenuCursor */
/* >>> factory DrawCardSymbol */
void DrawCardSymbol(uint8_t d, uint8_t e);
/* <<< factory DrawCardSymbol */
/* >>> factory DrawNarrowTextBox */
uint16_t DrawNarrowTextBox(void);
/* <<< factory DrawNarrowTextBox */
/* >>> factory DrawWideTextBox */
uint16_t DrawWideTextBox(void);
/* <<< factory DrawWideTextBox */
/* >>> factory DrawTextBox_PrintTextNoDelay */
TextResult DrawTextBox_PrintTextNoDelay(uint8_t a, uint16_t hl);
/* <<< factory DrawTextBox_PrintTextNoDelay */
/* >>> factory DrawNarrowTextBox_PrintTextNoDelay */
TextResult DrawNarrowTextBox_PrintTextNoDelay(uint16_t hl);
/* <<< factory DrawNarrowTextBox_PrintTextNoDelay */
/* >>> factory DrawWideTextBox_PrintTextNoDelay */
TextResult DrawWideTextBox_PrintTextNoDelay(uint16_t hl);
/* <<< factory DrawWideTextBox_PrintTextNoDelay */
/* >>> factory DrawWideTextBox_PrintText */
TextResult DrawWideTextBox_PrintText(uint16_t hl);
/* <<< factory DrawWideTextBox_PrintText */
/* >>> factory PrintYesOrNoItems */
ProcessTextHeaderResult PrintYesOrNoItems(uint8_t d, uint8_t e);
/* <<< factory PrintYesOrNoItems */

/* >>> factory WaitForButtonAorB */
WaitResult WaitForButtonAorB(void);
/* <<< factory WaitForButtonAorB */
/* >>> part DrawWideTextBox_PrintTextNoDelay_Wait */
void DrawWideTextBox_PrintTextNoDelay_Wait(uint16_t hl);
/* <<< part DrawWideTextBox_PrintTextNoDelay_Wait */
/* >>> factory DrawWideTextBox_WaitForInput */
WaitResult DrawWideTextBox_WaitForInput(uint16_t hl);
/* <<< factory DrawWideTextBox_WaitForInput */
/* >>> factory WaitForWideTextBoxInput */
WaitResult WaitForWideTextBoxInput(void);
/* <<< factory WaitForWideTextBoxInput */
/* >>> factory RefreshMenuCursor_CheckPlaySFX */
void RefreshMenuCursor_CheckPlaySFX(void);
/* <<< factory RefreshMenuCursor_CheckPlaySFX */
/* >>> factory PlayOpenOrExitScreenSFX */
typedef struct { uint8_t a; uint8_t f; } PlayOpenOrExitScreenSFXResult;
PlayOpenOrExitScreenSFXResult PlayOpenOrExitScreenSFX(uint8_t a, uint8_t f);
/* <<< factory PlayOpenOrExitScreenSFX */
/* >>> factory HandleYesOrNoMenu */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } HandleYesOrNoMenuResult;
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
/* >>> factory PrintCardListItems */
void PrintCardListItems(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
/* <<< factory PrintCardListItems */
/* >>> factory CardListMenuFunction */
typedef struct { uint8_t a; uint8_t f; } CardListMenuFunctionResult;
CardListMenuFunctionResult CardListMenuFunction(void);
/* <<< factory CardListMenuFunction */
/* >>> factory HandleMenuInput */
typedef struct { uint8_t a; uint8_t e; uint8_t f; uint8_t d; } HandleMenuInputResult;
HandleMenuInputResult HandleMenuInput(void);
/* <<< factory HandleMenuInput */
/* >>> factory HandleCardListInput */
typedef struct { uint8_t a; uint8_t d; uint8_t e; uint8_t f; } HandleCardListInputResult;
HandleCardListInputResult HandleCardListInput(void);
/* <<< factory HandleCardListInput */
/* >>> factory HandleDuelMenuInput */
HandleMenuInputResult HandleDuelMenuInput(uint8_t e);
/* <<< factory HandleDuelMenuInput */
/* >>> factory YesOrNoMenuWithText_LeftAligned */
HandleYesOrNoMenuResult YesOrNoMenuWithText_LeftAligned(uint16_t hl, uint8_t b, uint8_t c);
/* <<< factory YesOrNoMenuWithText_LeftAligned */
/* >>> factory TwoItemHorizontalMenu */
HandleYesOrNoMenuResult TwoItemHorizontalMenu(uint16_t hl);
/* <<< factory TwoItemHorizontalMenu */
/* >>> factory YesOrNoMenu */
HandleYesOrNoMenuResult YesOrNoMenu(void);
/* <<< factory YesOrNoMenu */
/* >>> factory YesOrNoMenuWithText */
HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl);
/* <<< factory YesOrNoMenuWithText */
/* >>> factory YesOrNoMenuWithText_SetCursorToYes */
HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl);
/* <<< factory YesOrNoMenuWithText_SetCursorToYes */
#endif
